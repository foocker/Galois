from __future__ import annotations

import json
from pathlib import Path

import httpx

from galois.writing.citation_lookup import CitationLookupService, parse_bibtex_entries


def _json_response(data: object) -> httpx.Response:
    return httpx.Response(200, json=data)


def test_parse_bibtex_entries_extracts_fields() -> None:
    entries = parse_bibtex_entries(
        """
@article{noether1921,
  author = {Noether, Emmy},
  title = {Invariante Variationsprobleme},
  year = {1918},
  doi = {10.1234/noether}
}
"""
    )

    assert entries == [
        {
            "entry_type": "article",
            "key": "noether1921",
            "fields": {
                "author": "Noether, Emmy",
                "title": "Invariante Variationsprobleme",
                "year": "1918",
                "doi": "10.1234/noether",
            },
        }
    ]


def test_resolve_doi_cross_checks_crossref_and_openalex_and_writes_cache(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "api.crossref.org/works/10.1234%2Fpaper" in url or "api.crossref.org/works/10.1234/paper" in url:
            return _json_response(
                {
                    "message": {
                        "DOI": "10.1234/paper",
                        "title": ["A Sample Mathematical Paper"],
                        "author": [{"given": "Emmy", "family": "Noether"}],
                        "issued": {"date-parts": [[1918]]},
                        "container-title": ["Mathematische Annalen"],
                        "volume": "1",
                        "page": "1-10",
                    }
                }
            )
        if "api.openalex.org/works" in url:
            return _json_response(
                {
                    "results": [
                        {
                            "doi": "https://doi.org/10.1234/paper",
                            "title": "A Sample Mathematical Paper",
                            "publication_year": 1918,
                            "authorships": [{"author": {"display_name": "Emmy Noether"}}],
                            "primary_location": {"source": {"display_name": "Mathematische Annalen"}},
                        }
                    ]
                }
            )
        raise AssertionError(url)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        service = CitationLookupService(client=client, cache_dir=tmp_path)
        result = service.resolve("https://doi.org/10.1234/paper")

    assert result["identifier_type"] == "doi"
    assert result["normalized_identifier"] == "10.1234/paper"
    assert result["verification_level"] == "metadata_cross_checked"
    assert {record["source"] for record in result["records"]} == {"crossref", "openalex"}
    assert all(record["status"] == "ok" for record in result["records"])
    assert list(tmp_path.glob("*.json"))


def test_search_queries_arxiv_crossref_and_openalex() -> None:
    arxiv_xml = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2103.00001v2</id>
    <title> A theorem search result </title>
    <published>2021-03-01T00:00:00Z</published>
    <author><name>A. Author</name></author>
  </entry>
</feed>"""

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "export.arxiv.org/api/query" in url:
            return httpx.Response(200, text=arxiv_xml)
        if "api.crossref.org/works" in url:
            return _json_response(
                {
                    "message": {
                        "items": [
                            {
                                "DOI": "10.5555/example",
                                "title": ["Crossref Result"],
                                "author": [{"given": "C.", "family": "Author"}],
                                "issued": {"date-parts": [[2020]]},
                            }
                        ]
                    }
                }
            )
        if "api.openalex.org/works" in url:
            return _json_response({"results": [{"title": "OpenAlex Result", "publication_year": 2019}]})
        raise AssertionError(url)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        service = CitationLookupService(client=client)
        result = service.search(
            "compactness theorem",
            sources=["arxiv", "crossref", "openalex"],
            limit=3,
        )

    assert result["query"] == "compactness theorem"
    assert {record["source"] for record in result["records"]} == {"arxiv", "crossref", "openalex"}
    assert all(record["status"] == "ok" for record in result["records"])


def test_default_search_runs_mandatory_external_source_chain() -> None:
    seen_hosts: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        seen_hosts.append(request.url.host or "")
        if "export.arxiv.org/api/query" in url:
            return httpx.Response(
                200,
                text="""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"></feed>""",
            )
        if "api.crossref.org/works" in url:
            return _json_response({"message": {"items": []}})
        if "api.openalex.org/works" in url:
            return _json_response({"results": []})
        raise AssertionError(url)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        service = CitationLookupService(client=client)
        result = service.search("fixed point theorem")

    assert result["sources"] == ["arxiv", "crossref", "openalex"]
    assert [record["source"] for record in result["records"]] == result["sources"]
    assert set(seen_hosts) == {
        "export.arxiv.org",
        "api.crossref.org",
        "api.openalex.org",
    }


def test_non_runtime_search_source_is_lookup_needed_without_http() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(str(request.url))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        service = CitationLookupService(client=client)
        result = service.search("fixed point theorem", sources=["pubmed"])

    assert result["records"] == [
        {"source": "pubmed", "status": "lookup_needed", "error": "unsupported search source: pubmed"}
    ]


def test_validate_bibtex_marks_missing_identifier_lookup_needed() -> None:
    service = CitationLookupService(client=httpx.Client(transport=httpx.MockTransport(lambda request: _json_response({}))))

    result = service.validate_bibtex(
        """
@article{missingid,
  author = {Doe, Jane},
  title = {A Claim With No Identifier},
  year = {2024}
}
"""
    )

    assert result["entries"][0]["key"] == "missingid"
    assert result["entries"][0]["status"] == "lookup_needed"
    assert "missing doi, arxiv id, or url" in result["entries"][0]["issues"]


def test_validate_bibtex_resolves_doi_and_reports_title_mismatch() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return _json_response(
            {
                "message": {
                    "DOI": "10.1234/paper",
                    "title": ["Correct Title"],
                    "author": [{"given": "A.", "family": "Author"}],
                    "issued": {"date-parts": [[2024]]},
                }
            }
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        service = CitationLookupService(client=client)
        result = service.validate_bibtex(
            """
@article{badtitle,
  author = {Author, A.},
  title = {Wrong Title},
  year = {2024},
  doi = {10.1234/paper}
}
""",
            sources=["crossref"],
        )

    entry = result["entries"][0]
    assert entry["status"] == "mismatch"
    assert "title mismatch against crossref" in entry["issues"]
    assert entry["lookup"]["verification_level"] == "metadata_found"
