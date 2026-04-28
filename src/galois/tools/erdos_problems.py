"""Fetch and normalize the teorth/erdosproblems dataset."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from typing import Any

import requests
import yaml


ERDOS_PROBLEMS_YAML_URL = (
    "https://raw.githubusercontent.com/teorth/erdosproblems/master/data/problems.yaml"
)
ERDOS_PROBLEM_PAGE_URL = "https://www.erdosproblems.com/{number}"
DEFAULT_CACHE_PATH = Path(".cache/erdosproblems/problems.yaml")
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


@dataclass(slots=True)
class ErdosProblemPage:
    statement: str = ""
    remarks: str = ""
    references: list[str] | None = None
    community_reactions: list[dict[str, Any]] | None = None


class _ProblemPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capture_id: str | None = None
        self._capture_depth = 0
        self._chunks: dict[str, list[str]] = {"content": [], "remarks": [], "refs": []}
        self._seen_ids: set[str] = set()
        self._skip_depth = 0
        self._reaction_depth = 0
        self._reaction_cell: str | None = None
        self._reaction_cell_depth = 0
        self._reaction: dict[str, Any] | None = None
        self._reaction_chunks: dict[str, list[str]] = {"label": [], "users": []}
        self._reactions: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        class_names = set((attr.get("class") or "").split())
        if "problem-reaction-row" in class_names:
            self._reaction_depth = 1
            self._reaction = {"type": attr.get("data-reaction-type", "")}
            self._reaction_chunks = {"label": [], "users": []}
            return
        if self._reaction_depth:
            self._reaction_depth += 1
            if "problem-reaction-label-cell" in class_names:
                self._reaction_cell = "label"
                self._reaction_cell_depth = 1
            elif "problem-reaction-users" in class_names:
                self._reaction_cell = "users"
                self._reaction_cell_depth = 1
            elif self._reaction_cell:
                self._reaction_cell_depth += 1
            if tag in {"br", "p", "div", "li", "tr"} and self._reaction_cell:
                self._reaction_chunks[self._reaction_cell].append("\n")
            return
        element_id = attr.get("id")
        if element_id in self._chunks:
            if element_id in self._seen_ids:
                return
            self._seen_ids.add(element_id)
            self._capture_id = element_id
            self._capture_depth = 1
            return
        if self._capture_id is not None:
            if tag in {"br", "p", "div", "li", "tr"}:
                self._chunks[self._capture_id].append("\n")
            if tag not in VOID_TAGS:
                self._capture_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._skip_depth or self._capture_id is None:
            return
        if tag in {"br", "p", "div", "li", "tr"}:
            self._chunks[self._capture_id].append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth and tag in {"script", "style"}:
            self._skip_depth -= 1
            return
        if self._reaction_depth:
            if tag in {"p", "div", "li", "tr"} and self._reaction_cell:
                self._reaction_chunks[self._reaction_cell].append("\n")
            if self._reaction_cell:
                self._reaction_cell_depth -= 1
                if self._reaction_cell_depth <= 0:
                    self._reaction_cell = None
            self._reaction_depth -= 1
            if self._reaction_depth <= 0 and self._reaction is not None:
                label = _clean_text("".join(self._reaction_chunks["label"]))
                users_text = _clean_text("".join(self._reaction_chunks["users"]))
                users = [item.strip() for item in users_text.split(",") if item.strip()]
                if label:
                    self._reactions.append(
                        {
                            "type": self._reaction.get("type", ""),
                            "label": label,
                            "users": [] if users_text.lower() in {"none", "none yet"} else users,
                        }
                    )
                self._reaction = None
                self._reaction_cell = None
                self._reaction_cell_depth = 0
            return
        if self._capture_id is None:
            return
        self._capture_depth -= 1
        if tag in {"p", "div", "li", "tr"}:
            self._chunks[self._capture_id].append("\n")
        if self._capture_depth <= 0:
            self._capture_id = None

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._reaction_depth and self._reaction_cell:
            self._reaction_chunks[self._reaction_cell].append(data)
            return
        if self._capture_id is None:
            return
        self._chunks[self._capture_id].append(data)

    def page(self) -> ErdosProblemPage:
        return ErdosProblemPage(
            statement=_clean_text("".join(self._chunks["content"])),
            remarks=_clean_text("".join(self._chunks["remarks"])),
            references=[
                item
                for item in (_clean_text(part) for part in "".join(self._chunks["refs"]).splitlines())
                if item
            ]
            or None,
            community_reactions=self._reactions or None,
        )


def _clean_text(value: str) -> str:
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n\s*\n\s*\n+", "\n\n", value)
    value = re.sub(r" *\n *", "\n", value)
    return value.strip()


def _clean_list(values: Any) -> list[str]:
    if not values:
        return []
    if not isinstance(values, list):
        values = [values]
    return [str(value).strip() for value in values if str(value).strip()]


def _source_url(number: str) -> str:
    return ERDOS_PROBLEM_PAGE_URL.format(number=number)


def fetch_yaml(url: str = ERDOS_PROBLEMS_YAML_URL, *, timeout: float = 30.0) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def write_yaml_cache(text: str, path: Path = DEFAULT_CACHE_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"expected YAML list in {path}")
    return [item for item in payload if isinstance(item, dict)]


def fetch_problem_page(number: str, *, timeout: float = 20.0) -> ErdosProblemPage:
    response = requests.get(_source_url(number), timeout=timeout)
    response.raise_for_status()
    parser = _ProblemPageParser()
    parser.feed(response.text)
    return parser.page()


def normalize_erdos_status(raw_status: str) -> str:
    status = raw_status.strip().lower()
    if status in {"open", "decidable", "falsifiable", "verifiable", "not provable", "not disprovable", "independent"}:
        return status
    if status.startswith("open"):
        return "open"
    if "disproved" in status:
        return "disproved"
    if "proved" in status:
        return "proved"
    if "solved" in status:
        return "solved"
    return status or "open"


def record_status(record: dict[str, Any]) -> str:
    status_payload = record.get("status") if isinstance(record.get("status"), dict) else {}
    return normalize_erdos_status(str(status_payload.get("state", "open")))


def select_records(
    records: list[dict[str, Any]],
    *,
    status: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    selected = records
    if status:
        normalized_status = normalize_erdos_status(status)
        selected = [record for record in selected if record_status(record) == normalized_status]
    return selected[:limit] if limit is not None else selected


def erdos_problem_to_garden_problem(
    record: dict[str, Any],
    *,
    page: ErdosProblemPage | None = None,
) -> dict[str, Any]:
    number = str(record.get("number", "")).strip()
    if not number:
        raise ValueError(f"missing Erdős problem number: {record!r}")
    status_payload = record.get("status") if isinstance(record.get("status"), dict) else {}
    raw_status = str(status_payload.get("state", "open"))
    status = normalize_erdos_status(raw_status)
    tags = _clean_list(record.get("tags"))
    oeis = [value for value in _clean_list(record.get("oeis")) if re.fullmatch(r"A\d+", value)]
    comments = str(record.get("comments", "")).strip()
    title_suffix = f": {comments}" if comments else ""
    title = f"Erdős problem #{number}{title_suffix}"
    source_url = _source_url(number)
    statement = page.statement if page and page.statement else (
        f"Metadata-only entry for Erdős problem #{number}. "
        f"Open the source page for the full problem statement: {source_url}"
    )
    progress = [f"Status: {status}."]

    source_literature = [source_url]
    source_literature.extend(f"OEIS {code}: https://oeis.org/{code}" for code in oeis if code.startswith("A"))
    if page and page.references:
        source_literature.extend(page.references[:20])

    graph_links = [
        {"from": "Problem", "relation": "stated_in", "to": "erdosproblems.com"},
        {"from": "Problem", "relation": "imported_from", "to": "teorth/erdosproblems"},
    ]
    graph_links.extend({"from": "Problem", "relation": "belongs_to_domain", "to": tag} for tag in tags)
    graph_links.extend({"from": "Problem", "relation": "linked_to_oeis", "to": code} for code in oeis)

    return {
        "id": f"erdos-{number}",
        "title": title,
        "status": status,
        "difficulty": "research",
        "domains": tags or ["number theory"],
        "source": "teorth/erdosproblems",
        "source_url": source_url,
        "statement": statement,
        "source_literature": source_literature,
        "progress": progress,
        "community_reactions": page.community_reactions if page and page.community_reactions else [],
        "graph_links": graph_links,
    }


def build_garden_problems(
    records: list[dict[str, Any]],
    *,
    fetch_pages: bool = False,
    limit: int | None = None,
    status: str | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    problems: list[dict[str, Any]] = []
    errors: list[str] = []
    selected = select_records(records, status=status, limit=limit)
    for record in selected:
        number = str(record.get("number", "")).strip()
        page = None
        if fetch_pages and number:
            try:
                page = fetch_problem_page(number)
            except requests.RequestException as exc:
                errors.append(f"{number}: {exc}")
        try:
            problems.append(erdos_problem_to_garden_problem(record, page=page))
        except ValueError as exc:
            errors.append(str(exc))
    return problems, errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and normalize teorth/erdosproblems.")
    parser.add_argument("--source-url", default=ERDOS_PROBLEMS_YAML_URL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE_PATH)
    parser.add_argument("--no-fetch-yaml", action="store_true", help="Use the existing cached YAML file.")
    parser.add_argument("--fetch-pages", action="store_true", help="Fetch erdosproblems.com pages for statements and remarks.")
    parser.add_argument("--status", default="open", help="Filter by normalized status. Use an empty value for all statuses.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=Path, default=None, help="Write normalized Problem Garden JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not args.no_fetch_yaml:
        write_yaml_cache(fetch_yaml(args.source_url), args.cache)
    records = load_yaml_records(args.cache)
    status = args.status.strip() or None
    problems, errors = build_garden_problems(records, fetch_pages=args.fetch_pages, limit=args.limit, status=status)
    payload = {"source_url": args.source_url, "problems": problems, "errors": errors}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
