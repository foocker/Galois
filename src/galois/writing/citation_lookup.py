"""Deterministic citation lookup and validation helpers for paper writing."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
import json
import re
import xml.etree.ElementTree as ET

import httpx


DEFAULT_RESOLVE_SOURCES = {
    "doi": ["crossref", "openalex"],
    "arxiv": ["arxiv", "openalex"],
    "unknown": ["crossref", "openalex"],
}
DEFAULT_SEARCH_SOURCES = ["arxiv", "crossref", "openalex"]


def normalize_doi(value: str) -> str:
    doi = value.strip()
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^doi\.org/", "", doi, flags=re.IGNORECASE)
    return doi.strip().rstrip(".")


def normalize_arxiv_id(value: str) -> str:
    arxiv_id = value.strip()
    arxiv_id = re.sub(r"^arxiv:\s*", "", arxiv_id, flags=re.IGNORECASE)
    arxiv_id = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", arxiv_id, flags=re.IGNORECASE)
    arxiv_id = arxiv_id.removesuffix(".pdf")
    return arxiv_id.strip()


def identifier_type(value: str) -> str:
    stripped = value.strip()
    doi = normalize_doi(stripped)
    if re.match(r"^10\.\d{4,9}/\S+$", doi, flags=re.IGNORECASE):
        return "doi"
    arxiv_id = normalize_arxiv_id(stripped)
    if re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", arxiv_id) or re.match(
        r"^[a-z.-]+/\d{7}(v\d+)?$", arxiv_id, flags=re.IGNORECASE
    ):
        return "arxiv"
    return "unknown"


def parse_bibtex_entries(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    entry_re = re.compile(r"@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+)\s*,(?P<body>.*?)\n\}", re.DOTALL)
    field_re = re.compile(
        r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?:\{(?P<braced>.*?)\}|\"(?P<quoted>.*?)\")\s*,?",
        re.DOTALL,
    )
    for match in entry_re.finditer(text):
        fields: dict[str, str] = {}
        for field in field_re.finditer(match.group("body")):
            value = field.group("braced") if field.group("braced") is not None else field.group("quoted")
            fields[field.group("name").lower()] = re.sub(r"\s+", " ", (value or "").strip())
        entries.append(
            {
                "entry_type": match.group("type").lower(),
                "key": match.group("key").strip(),
                "fields": fields,
            }
        )
    return entries


def _author_name(author: dict[str, Any]) -> str:
    given = author.get("given") or author.get("first") or ""
    family = author.get("family") or author.get("last") or ""
    literal = author.get("name") or author.get("display_name") or ""
    return " ".join(part for part in (given, family) if part).strip() or str(literal)


def _year_from_crossref(message: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (message.get(key) or {}).get("date-parts") or []
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                return None
    return None


def _clean_title(title: Any) -> str:
    if isinstance(title, list):
        return str(title[0]).strip() if title else ""
    return str(title or "").strip()


def _compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _title_matches(left: str, right: str) -> bool:
    left_compact = _compact(left)
    right_compact = _compact(right)
    if not left_compact or not right_compact:
        return True
    return left_compact == right_compact or left_compact in right_compact or right_compact in left_compact


def _safe_slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", text).strip("-")[:120] or "lookup"


class CitationLookupService:
    """HTTP-backed citation lookup service with small, deterministic adapters."""

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        cache_dir: Path | None = None,
    ) -> None:
        self.client = client or httpx.Client(timeout=20.0, follow_redirects=True)
        self._owns_client = client is None
        self.cache_dir = cache_dir

    def __enter__(self) -> "CitationLookupService":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self.client.close()

    def resolve(self, identifier: str, sources: list[str] | None = None) -> dict[str, Any]:
        kind = identifier_type(identifier)
        normalized = normalize_doi(identifier) if kind == "doi" else normalize_arxiv_id(identifier)
        selected = sources or DEFAULT_RESOLVE_SOURCES[kind]
        records = [self._resolve_with_source(source, normalized, kind) for source in selected]
        result = {
            "operation": "resolve",
            "identifier": identifier,
            "identifier_type": kind,
            "normalized_identifier": normalized,
            "sources": selected,
            "records": records,
            "verification_level": self._verification_level(records),
        }
        self._cache("resolve", normalized, result)
        return result

    def search(self, query: str, *, sources: list[str] | None = None, limit: int = 10) -> dict[str, Any]:
        selected = sources or DEFAULT_SEARCH_SOURCES
        records = [self._search_source(source, query, limit) for source in selected]
        result = {
            "operation": "search",
            "query": query,
            "sources": selected,
            "records": records,
            "lookup_needed": [
                {"source": record["source"], "reason": record.get("error")}
                for record in records
                if record["status"] in {"error", "lookup_needed"}
            ],
        }
        self._cache("search", query, result)
        return result

    def validate_bibtex(self, bibtex: str, *, sources: list[str] | None = None) -> dict[str, Any]:
        entries = parse_bibtex_entries(bibtex)
        validated = [self._validate_entry(entry, sources=sources) for entry in entries]
        return {
            "operation": "validate_bibtex",
            "entry_count": len(entries),
            "entries": validated,
            "summary": {
                "verified": sum(1 for entry in validated if entry["status"] == "verified"),
                "mismatch": sum(1 for entry in validated if entry["status"] == "mismatch"),
                "lookup_needed": sum(1 for entry in validated if entry["status"] == "lookup_needed"),
            },
        }

    def _resolve_with_source(self, source: str, identifier: str, kind: str) -> dict[str, Any]:
        try:
            if source == "crossref":
                return self._resolve_crossref(identifier, kind)
            if source == "openalex":
                return self._resolve_openalex(identifier, kind)
            if source == "arxiv":
                return self._resolve_arxiv(identifier, kind)
        except httpx.HTTPStatusError as exc:
            return self._record(source, "error", error=f"http {exc.response.status_code}", raw=_response_text(exc.response))
        except (httpx.RequestError, ValueError, ET.ParseError) as exc:
            return self._record(source, "error", error=str(exc))
        return self._record(source, "lookup_needed", error=f"unsupported source for {kind}: {source}")

    def _search_source(self, source: str, query: str, limit: int) -> dict[str, Any]:
        try:
            if source == "arxiv":
                return self._search_arxiv(query, limit)
            if source == "crossref":
                return self._search_crossref(query, limit)
            if source == "openalex":
                return self._search_openalex(query, limit)
        except httpx.HTTPStatusError as exc:
            return self._record(source, "error", error=f"http {exc.response.status_code}", raw=_response_text(exc.response))
        except (httpx.RequestError, ValueError, ET.ParseError) as exc:
            return self._record(source, "error", error=str(exc))
        return self._record(source, "lookup_needed", error=f"unsupported search source: {source}")

    def _resolve_crossref(self, doi: str, kind: str) -> dict[str, Any]:
        if kind != "doi":
            return self._record("crossref", "lookup_needed", error="Crossref resolve requires DOI")
        response = self.client.get(f"https://api.crossref.org/works/{quote(doi, safe='/')}")
        response.raise_for_status()
        raw = response.json()
        message = raw.get("message") or {}
        metadata = self._metadata_from_crossref(message)
        return self._record("crossref", "ok" if metadata.get("title") else "not_found", metadata=metadata, raw=raw)

    def _search_crossref(self, query: str, limit: int) -> dict[str, Any]:
        response = self.client.get("https://api.crossref.org/works", params={"query.bibliographic": query, "rows": limit})
        response.raise_for_status()
        raw = response.json()
        items = (raw.get("message") or {}).get("items") or []
        return self._record(
            "crossref",
            "ok",
            results=[self._metadata_from_crossref(item) for item in items],
            raw=raw,
        )

    def _resolve_openalex(self, identifier: str, kind: str) -> dict[str, Any]:
        params = {"per-page": 1}
        if kind == "doi":
            params["filter"] = f"doi:https://doi.org/{identifier}"
        else:
            params["search"] = identifier
        response = self.client.get("https://api.openalex.org/works", params=params)
        response.raise_for_status()
        raw = response.json()
        results = raw.get("results") or []
        metadata = self._metadata_from_openalex(results[0]) if results else {}
        return self._record("openalex", "ok" if metadata else "not_found", metadata=metadata, raw=raw)

    def _search_openalex(self, query: str, limit: int) -> dict[str, Any]:
        response = self.client.get("https://api.openalex.org/works", params={"search": query, "per-page": limit})
        response.raise_for_status()
        raw = response.json()
        return self._record(
            "openalex",
            "ok",
            results=[self._metadata_from_openalex(item) for item in raw.get("results") or []],
            raw=raw,
        )

    def _resolve_arxiv(self, arxiv_id: str, kind: str) -> dict[str, Any]:
        if kind != "arxiv":
            return self._record("arxiv", "lookup_needed", error="arXiv resolve requires arXiv ID")
        response = self.client.get("https://export.arxiv.org/api/query", params={"id_list": arxiv_id})
        response.raise_for_status()
        entries = self._parse_arxiv_entries(response.text)
        metadata = entries[0] if entries else {}
        return self._record("arxiv", "ok" if metadata else "not_found", metadata=metadata, raw=response.text)

    def _search_arxiv(self, query: str, limit: int) -> dict[str, Any]:
        response = self.client.get(
            "https://export.arxiv.org/api/query",
            params={"search_query": f"all:{query}", "start": 0, "max_results": limit},
        )
        response.raise_for_status()
        return self._record("arxiv", "ok", results=self._parse_arxiv_entries(response.text), raw=response.text)

    def _validate_entry(self, entry: dict[str, Any], *, sources: list[str] | None) -> dict[str, Any]:
        fields = entry["fields"]
        issues: list[str] = []
        for required in ("author", "title", "year"):
            if not fields.get(required):
                issues.append(f"missing required field: {required}")
        identifier = fields.get("doi") or fields.get("arxiv") or fields.get("eprint") or fields.get("url") or ""
        if not identifier:
            issues.append("missing doi, arxiv id, or url")
            return {**entry, "status": "lookup_needed", "issues": issues, "lookup": None}
        lookup = self.resolve(identifier, sources=sources)
        ok_records = [record for record in lookup["records"] if record["status"] == "ok" and record.get("metadata")]
        if not ok_records:
            issues.append("identifier did not resolve")
            return {**entry, "status": "lookup_needed", "issues": issues, "lookup": lookup}
        title = fields.get("title", "")
        year = fields.get("year", "")
        for record in ok_records:
            metadata = record.get("metadata") or {}
            source = record["source"]
            if title and metadata.get("title") and not _title_matches(title, str(metadata["title"])):
                issues.append(f"title mismatch against {source}")
            if year and metadata.get("year") and str(metadata["year"]) != str(year):
                issues.append(f"year mismatch against {source}")
        status = "mismatch" if any("mismatch" in issue for issue in issues) else "verified"
        return {**entry, "status": status, "issues": issues, "lookup": lookup}

    def _verification_level(self, records: list[dict[str, Any]]) -> str:
        ok_records = [record for record in records if record["status"] == "ok" and record.get("metadata")]
        if len(ok_records) >= 2:
            titles = [str((record.get("metadata") or {}).get("title") or "") for record in ok_records]
            if titles and all(_title_matches(titles[0], title) for title in titles[1:]):
                return "metadata_cross_checked"
        if ok_records:
            return "metadata_found"
        if any(record["status"] == "lookup_needed" for record in records):
            return "lookup_needed"
        return "unverified"

    def _record(
        self,
        source: str,
        status: str,
        *,
        metadata: dict[str, Any] | None = None,
        results: list[dict[str, Any]] | None = None,
        raw: Any | None = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        record: dict[str, Any] = {"source": source, "status": status}
        if metadata is not None:
            record["metadata"] = metadata
        if results is not None:
            record["results"] = results
        if error:
            record["error"] = error
        if raw is not None:
            record["raw"] = raw
        return record

    def _cache(self, operation: str, key: str, payload: dict[str, Any]) -> None:
        if self.cache_dir is None:
            return
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.cache_dir / f"{timestamp}-{operation}-{_safe_slug(key)}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    def _metadata_from_crossref(self, message: dict[str, Any]) -> dict[str, Any]:
        return {
            "title": _clean_title(message.get("title")),
            "authors": [_author_name(author) for author in message.get("author") or []],
            "year": _year_from_crossref(message),
            "venue": _clean_title(message.get("container-title")),
            "doi": message.get("DOI"),
            "volume": message.get("volume"),
            "issue": message.get("issue"),
            "pages": message.get("page"),
            "url": message.get("URL"),
        }

    def _metadata_from_openalex(self, item: dict[str, Any]) -> dict[str, Any]:
        source = ((item.get("primary_location") or {}).get("source") or {}).get("display_name")
        return {
            "title": item.get("title") or item.get("display_name"),
            "authors": [
                ((authorship.get("author") or {}).get("display_name") or "")
                for authorship in item.get("authorships") or []
            ],
            "year": item.get("publication_year"),
            "venue": source,
            "doi": normalize_doi(str(item.get("doi") or "")) if item.get("doi") else None,
            "url": item.get("id"),
        }

    def _parse_arxiv_entries(self, text: str) -> list[dict[str, Any]]:
        root = ET.fromstring(text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries: list[dict[str, Any]] = []
        for entry in root.findall("atom:entry", ns):
            raw_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
            published = entry.findtext("atom:published", default="", namespaces=ns)
            year = int(published[:4]) if published and published[:4].isdigit() else None
            entries.append(
                {
                    "title": re.sub(r"\s+", " ", entry.findtext("atom:title", default="", namespaces=ns) or "").strip(),
                    "authors": [
                        name.text.strip()
                        for name in entry.findall("atom:author/atom:name", ns)
                        if name.text
                    ],
                    "year": year,
                    "arxiv_id": normalize_arxiv_id(raw_id),
                    "url": raw_id,
                }
            )
        return entries


def _response_text(response: httpx.Response) -> str:
    try:
        return response.text
    except Exception:
        return ""
