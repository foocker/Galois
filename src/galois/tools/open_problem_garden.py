"""Fetch and normalize problems from openproblemgarden.org."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import requests
import yaml


OPEN_PROBLEM_GARDEN_BASE_URL = "http://www.openproblemgarden.org"
DEFAULT_OUTPUT_DIR = Path("benchmarks/problems/open_problem_garden")
DEFAULT_CACHE_DIR = Path(".cache/open_problem_garden")


@dataclass(frozen=True, slots=True)
class OpenProblemGardenCategory:
    slug: str
    name: str
    path: str

    @property
    def url(self) -> str:
        return urljoin(OPEN_PROBLEM_GARDEN_BASE_URL, self.path)


OPEN_PROBLEM_GARDEN_CATEGORIES: tuple[OpenProblemGardenCategory, ...] = (
    OpenProblemGardenCategory("algebra", "Algebra", "/category/algebra"),
    OpenProblemGardenCategory("analysis", "Analysis", "/category/analysis"),
    OpenProblemGardenCategory("combinatorics", "Combinatorics", "/category/combinatorics"),
    OpenProblemGardenCategory("geometry", "Geometry", "/category/geometry"),
    OpenProblemGardenCategory("graph_theory", "Graph Theory", "/category/graph_theory"),
    OpenProblemGardenCategory("group_theory", "Group Theory", "/category/group_theory"),
    OpenProblemGardenCategory("logic", "Logic", "/category/logic"),
    OpenProblemGardenCategory("number_theory", "Number Theory", "/category/number_theory_0"),
    OpenProblemGardenCategory("pdes", "PDEs", "/category/pdes"),
    OpenProblemGardenCategory("probability", "Probability", "/category/probability"),
    OpenProblemGardenCategory(
        "theoretical_computer_science",
        "Theoretical Comp. Sci.",
        "/category/theoretical_computer_science",
    ),
    OpenProblemGardenCategory("topology", "Topology", "/topology"),
    OpenProblemGardenCategory("unsorted", "Unsorted", "/category/unsorted"),
)
CATEGORY_BY_SLUG = {category.slug: category for category in OPEN_PROBLEM_GARDEN_CATEGORIES}


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


SPAM_TITLE_PATTERNS = (
    "assignment help",
    "buy ",
    "casino",
    "cheap ",
    "coursework",
    "coupon",
    "dissertation",
    "essay",
    "exam help",
    "homework",
    "pay someone",
    "porn",
    "seo ",
    "slot",
    "thesis writing",
    "viagra",
    "weight loss",
    "write my",
)


@dataclass(slots=True)
class OpenProblemGardenLink:
    title: str
    url: str
    slug: str
    category: str


@dataclass(slots=True)
class OpenProblemGardenPage:
    title: str = ""
    statement: str = ""
    discussion: str = ""
    bibliography: list[str] = field(default_factory=list)
    related_links: list[dict[str, str]] = field(default_factory=list)
    subjects: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    importance: str = ""


@dataclass(slots=True)
class OpenProblemGardenCrawlResult:
    problems: list[dict[str, Any]]
    skipped: list[dict[str, str]]
    errors: list[str]
    source_urls: list[str]


def _clean_text(value: str) -> str:
    value = re.sub(r"\xa0", " ", value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n\s*\n\s*\n+", "\n\n", value)
    return value.strip()


def _clean_lines(value: str) -> list[str]:
    return [line for line in (_clean_text(part) for part in value.splitlines()) if line]


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1]


def _safe_filename(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "problem"


def is_probable_spam(title: str, url: str = "") -> bool:
    sample = f"{title} {urlparse(url).path}".lower()
    if any(pattern in sample for pattern in SPAM_TITLE_PATTERNS):
        return True
    if len(title.strip()) > 180:
        return True
    words = re.findall(r"[a-zA-Z]{3,}", title)
    if len(words) >= 5:
        uppercase_words = sum(1 for word in words if word.isupper())
        if uppercase_words >= len(words) * 0.8:
            return True
    return False


class _CategoryPageParser(HTMLParser):
    def __init__(self, category: OpenProblemGardenCategory) -> None:
        super().__init__(convert_charrefs=True)
        self.category = category
        self.links: list[OpenProblemGardenLink] = []
        self.max_page = 0
        self._in_title_cell = False
        self._cell_depth = 0
        self._capture_link: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        class_names = set((attr.get("class") or "").split())
        if tag == "td" and "view-field-node-title" in class_names:
            self._in_title_cell = True
            self._cell_depth = 1
            return
        if self._in_title_cell and tag not in VOID_TAGS:
            self._cell_depth += 1
        if tag == "a":
            href = attr.get("href") or ""
            parsed = parse_qs(urlparse(href).query)
            if "page" in parsed:
                try:
                    self.max_page = max(self.max_page, int(parsed["page"][0]))
                except (TypeError, ValueError):
                    pass
            if self._in_title_cell and urlparse(href).path.startswith("/op/"):
                self._capture_link = {"href": href, "text": []}

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture_link is not None:
            should_decrement_cell = self._in_title_cell and self._cell_depth > 0
            title = _clean_text("".join(self._capture_link["text"]))
            href = str(self._capture_link["href"])
            url = urljoin(OPEN_PROBLEM_GARDEN_BASE_URL, href)
            slug = _slug_from_url(url)
            if title and slug and not any(link.slug == slug for link in self.links):
                self.links.append(
                    OpenProblemGardenLink(
                        title=title,
                        url=url,
                        slug=slug,
                        category=self.category.slug,
                    )
                )
            self._capture_link = None
            if should_decrement_cell:
                self._cell_depth -= 1
                if self._cell_depth <= 0:
                    self._in_title_cell = False
                    self._cell_depth = 0
            return
        if self._in_title_cell:
            self._cell_depth -= 1
            if self._cell_depth <= 0:
                self._in_title_cell = False
                self._cell_depth = 0

    def handle_data(self, data: str) -> None:
        if self._capture_link is not None:
            self._capture_link["text"].append(data)


class _ProblemPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_chunks: list[str] = []
        self.section_chunks: dict[str, list[str]] = {
            "problem": [],
            "discussion": [],
            "bibliography": [],
            "metatable": [],
            "related": [],
        }
        self.related_links: list[dict[str, str]] = []
        self.subjects: list[str] = []
        self.keywords: list[str] = []
        self._capture_title = False
        self._title_depth = 0
        self._section: str | None = None
        self._section_depth = 0
        self._link: dict[str, Any] | None = None
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        class_names = set((attr.get("class") or "").split())
        if tag == "h1" and "title" in class_names:
            self._capture_title = True
            self._title_depth = 1
            return
        section = next(
            (name for name in ("problem", "discussion", "bibliography", "metatable", "related") if name in class_names),
            None,
        )
        if section and self._section is None:
            self._section = section
            self._section_depth = 1
            return
        if self._capture_title and tag not in VOID_TAGS:
            self._title_depth += 1
        if self._section is not None:
            if tag == "img":
                formula_text = attr.get("alt") or attr.get("title") or ""
                if formula_text:
                    self.section_chunks[self._section].append(f" {formula_text} ")
            if tag not in VOID_TAGS:
                self._section_depth += 1
            if tag in {"br", "p", "div", "li", "tr", "h2", "h3"}:
                self.section_chunks[self._section].append("\n")
            if tag == "a":
                href = attr.get("href") or ""
                self._link = {"href": href, "text": [], "section": self._section}

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._section is not None and tag == "img":
            attr = dict(attrs)
            formula_text = attr.get("alt") or attr.get("title") or ""
            if formula_text:
                self.section_chunks[self._section].append(f" {formula_text} ")
        if self._section is not None and tag in {"br", "p", "div", "li", "tr"}:
            self.section_chunks[self._section].append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth and tag in {"script", "style"}:
            self._skip_depth -= 1
            return
        if tag == "a" and self._link is not None:
            self._finish_link()
            if self._section is not None:
                self._section_depth -= 1
                if self._section_depth <= 0:
                    self._section = None
                    self._section_depth = 0
            return
        if self._capture_title:
            self._title_depth -= 1
            if self._title_depth <= 0:
                self._capture_title = False
            return
        if self._section is not None:
            if tag in {"p", "div", "li", "tr", "h2", "h3"}:
                self.section_chunks[self._section].append("\n")
            self._section_depth -= 1
            if self._section_depth <= 0:
                self._section = None
                self._section_depth = 0

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._capture_title:
            self.title_chunks.append(data)
        if self._section is not None:
            self.section_chunks[self._section].append(data)
        if self._link is not None:
            self._link["text"].append(data)

    def _finish_link(self) -> None:
        if self._link is None:
            return
        href = str(self._link.get("href") or "")
        text = _clean_text("".join(self._link.get("text") or []))
        section = str(self._link.get("section") or "")
        absolute_url = urljoin(OPEN_PROBLEM_GARDEN_BASE_URL, href)
        if section == "metatable":
            path = urlparse(href).path
            if path.startswith("/category/") or path == "/topology":
                self.subjects.append(text)
            elif path.startswith("/keywords/") or path.startswith("/keyword/"):
                self.keywords.append(text)
        elif section in {"discussion", "problem", "bibliography", "related"} and urlparse(href).path.startswith("/op/"):
            self.related_links.append({"title": text, "url": absolute_url, "slug": _slug_from_url(absolute_url)})
        self._link = None

    def page(self) -> OpenProblemGardenPage:
        metatable = _clean_text("".join(self.section_chunks["metatable"]))
        importance = ""
        match = re.search(r"Importance\s*:?\s*([^\n]+)", metatable, flags=re.IGNORECASE)
        if match:
            importance = _clean_text(match.group(1))
        bibliography_text = _clean_text("".join(self.section_chunks["bibliography"]))
        bibliography = [
            line
            for line in _clean_lines(bibliography_text)
            if line.lower() not in {"bibliography", "references"}
        ]
        return OpenProblemGardenPage(
            title=_clean_text("".join(self.title_chunks)),
            statement=_clean_text("".join(self.section_chunks["problem"])),
            discussion=_clean_text("".join(self.section_chunks["discussion"])),
            bibliography=bibliography,
            related_links=self.related_links,
            subjects=list(dict.fromkeys(subject for subject in self.subjects if subject)),
            keywords=list(dict.fromkeys(keyword for keyword in self.keywords if keyword)),
            importance=importance,
        )


def category_cache_path(cache_dir: Path, category: OpenProblemGardenCategory, page_index: int) -> Path:
    return cache_dir / "categories" / category.slug / f"page-{page_index}.html"


def problem_cache_path(cache_dir: Path, slug: str) -> Path:
    return cache_dir / "problems" / f"{_safe_filename(slug)}.html"


def fetch_page(
    url: str,
    *,
    cache_path: Path | None = None,
    use_cache: bool = True,
    timeout: float = 10.0,
) -> str:
    if use_cache and cache_path is not None and cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Galois Open Problem Garden importer/0.1"},
    )
    response.raise_for_status()
    text = response.text
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(text, encoding="utf-8")
    return text


def parse_category_page(html: str, category: OpenProblemGardenCategory) -> tuple[list[OpenProblemGardenLink], int]:
    parser = _CategoryPageParser(category)
    parser.feed(html)
    return parser.links, parser.max_page


def parse_problem_page(html: str) -> OpenProblemGardenPage:
    parser = _ProblemPageParser()
    parser.feed(html)
    return parser.page()


def _category_page_url(category: OpenProblemGardenCategory, page_index: int) -> str:
    if page_index <= 0:
        return category.url
    separator = "&" if "?" in category.url else "?"
    return f"{category.url}{separator}page={page_index}"


def discover_category_problem_links(
    category: OpenProblemGardenCategory,
    *,
    pages: int | None = None,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    timeout: float = 10.0,
    delay: float = 0.0,
) -> tuple[list[OpenProblemGardenLink], list[str], list[str]]:
    links: list[OpenProblemGardenLink] = []
    errors: list[str] = []
    source_urls: list[str] = []
    page_index = 0
    max_page: int | None = None
    while True:
        if pages is not None and page_index >= pages:
            break
        url = _category_page_url(category, page_index)
        source_urls.append(url)
        try:
            html = fetch_page(
                url,
                cache_path=category_cache_path(cache_dir, category, page_index),
                use_cache=use_cache,
                timeout=timeout,
            )
            page_links, parsed_max_page = parse_category_page(html, category)
            max_page = max_page if max_page is not None else parsed_max_page
            for link in page_links:
                if not any(existing.slug == link.slug for existing in links):
                    links.append(link)
        except requests.RequestException as exc:
            errors.append(f"{category.slug} page {page_index}: {exc}")
            break
        if max_page is None or page_index >= max_page:
            break
        page_index += 1
        if delay:
            time.sleep(delay)
    return links, errors, source_urls


def normalize_opg_status(page: OpenProblemGardenPage) -> str:
    discussion = page.discussion.lower()
    solved_patterns = (
        r"\bhas been solved\b",
        r"\bwas solved\b",
        r"\bis solved\b",
        r"\bthis problem is solved\b",
        r"\bsolution is known\b",
        r"\bhas a solution\b",
    )
    if any(re.search(pattern, discussion) for pattern in solved_patterns):
        return "solved"
    return "open"


def normalize_opg_difficulty(importance: str) -> str:
    normalized = importance.lower()
    if "outstanding" in normalized or "high" in normalized:
        return "frontier"
    if "low" in normalized:
        return "graduate"
    return "research"


def opg_problem_to_garden_problem(
    link: OpenProblemGardenLink,
    page: OpenProblemGardenPage,
    *,
    category: OpenProblemGardenCategory,
) -> dict[str, Any]:
    title = page.title or link.title
    statement = page.statement or f"Open Problem Garden entry without extracted statement. Source: {link.url}"
    progress = [page.discussion] if page.discussion else ["Status: open."]
    source_literature = [link.url]
    source_literature.extend(page.bibliography)
    domains = [category.name, *page.subjects, *page.keywords]
    domains = list(dict.fromkeys(domain for domain in domains if domain))
    graph_links = [
        {"from": "Problem", "relation": "stated_in", "to": "Open Problem Garden"},
        {"from": "Problem", "relation": "imported_from", "to": "openproblemgarden.org"},
    ]
    graph_links.extend({"from": "Problem", "relation": "belongs_to_domain", "to": domain} for domain in domains)
    graph_links.extend(
        {"from": "Problem", "relation": "related_to", "to": related["title"] or related["slug"]}
        for related in page.related_links
        if related.get("title") or related.get("slug")
    )
    return {
        "id": f"opg-{link.slug}",
        "title": title,
        "status": normalize_opg_status(page),
        "difficulty": normalize_opg_difficulty(page.importance),
        "domains": domains or [category.name],
        "source": "Open Problem Garden",
        "source_url": link.url,
        "statement": statement,
        "source_literature": source_literature,
        "progress": progress,
        "community_reactions": [],
        "graph_links": graph_links,
    }


def selected_categories(category_slugs: list[str] | None = None) -> list[OpenProblemGardenCategory]:
    if not category_slugs:
        return list(OPEN_PROBLEM_GARDEN_CATEGORIES)
    categories: list[OpenProblemGardenCategory] = []
    for slug in category_slugs:
        if slug not in CATEGORY_BY_SLUG:
            raise ValueError(f"unknown Open Problem Garden category: {slug}")
        categories.append(CATEGORY_BY_SLUG[slug])
    return categories


def crawl_open_problem_garden(
    *,
    category_slugs: list[str] | None = None,
    limit: int | None = None,
    pages: int | None = None,
    include_spam: bool = False,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
    timeout: float = 10.0,
    delay: float = 0.0,
) -> OpenProblemGardenCrawlResult:
    problems: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    errors: list[str] = []
    source_urls: list[str] = []
    seen_slugs: set[str] = set()
    categories = selected_categories(category_slugs)

    for category in categories:
        links, category_errors, category_source_urls = discover_category_problem_links(
            category,
            pages=pages,
            cache_dir=cache_dir,
            use_cache=use_cache,
            timeout=timeout,
            delay=delay,
        )
        errors.extend(category_errors)
        source_urls.extend(category_source_urls)
        for link in links:
            if limit is not None and len(problems) >= limit:
                break
            if link.slug in seen_slugs:
                continue
            seen_slugs.add(link.slug)
            if not include_spam and is_probable_spam(link.title, link.url):
                skipped.append({"slug": link.slug, "title": link.title, "reason": "probable spam"})
                continue
            try:
                html = fetch_page(
                    link.url,
                    cache_path=problem_cache_path(cache_dir, link.slug),
                    use_cache=use_cache,
                    timeout=timeout,
                )
                page = parse_problem_page(html)
                problems.append(opg_problem_to_garden_problem(link, page, category=category))
            except (requests.RequestException, ValueError) as exc:
                errors.append(f"{link.slug}: {exc}")
            if delay:
                time.sleep(delay)
        if limit is not None and len(problems) >= limit:
            break

    return OpenProblemGardenCrawlResult(
        problems=problems,
        skipped=skipped,
        errors=errors,
        source_urls=source_urls,
    )


def problem_markdown(problem: dict[str, Any]) -> str:
    frontmatter = {
        "id": problem["id"],
        "title": problem["title"],
        "status": problem["status"],
        "difficulty": problem["difficulty"],
        "domains": problem["domains"],
        "source": problem["source"],
        "source_url": problem["source_url"],
    }
    lines = ["---", yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip(), "---", ""]
    lines.extend(["# Statement", "", str(problem.get("statement", "")).strip(), ""])
    lines.extend(["# Source literature", ""])
    for item in problem.get("source_literature") or []:
        lines.append(f"- {item}")
    lines.extend(["", "# Progress", ""])
    for item in problem.get("progress") or []:
        lines.append(f"- {item}")
    graph_links = problem.get("graph_links") or []
    if graph_links:
        lines.extend(["", "# Graph links", "", "| From | Relation | To |", "| --- | --- | --- |"])
        for edge in graph_links:
            lines.append(f"| {edge.get('from', '')} | {edge.get('relation', '')} | {edge.get('to', '')} |")
    return "\n".join(lines).rstrip() + "\n"


def write_problem_files(
    problems: list[dict[str, Any]],
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    errors: list[str] | None = None,
    skipped: list[dict[str, str]] | None = None,
) -> list[Path]:
    written: list[Path] = []
    for problem in problems:
        domains = problem.get("domains") or ["unsorted"]
        category_slug = _safe_filename(str(domains[0]))
        path = output_dir / category_slug / f"{_safe_filename(str(problem['id']))}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(problem_markdown(problem), encoding="utf-8")
        written.append(path)
    index_payload = {
        "source": "Open Problem Garden",
        "source_url": OPEN_PROBLEM_GARDEN_BASE_URL,
        "count": len(problems),
        "problems": problems,
        "skipped": skipped or [],
        "errors": errors or [],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.json").write_text(json.dumps(index_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written.append(output_dir / "index.json")
    return written


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and normalize openproblemgarden.org.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--category", choices=sorted(CATEGORY_BY_SLUG), action="append", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--pages", type=int, default=None)
    parser.add_argument("--include-spam", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-write-files", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = crawl_open_problem_garden(
        category_slugs=args.category,
        limit=args.limit,
        pages=args.pages,
        include_spam=args.include_spam,
        cache_dir=args.cache_dir,
        use_cache=not args.no_cache,
        timeout=args.timeout,
        delay=args.delay,
    )
    written: list[Path] = []
    if not args.dry_run and not args.no_write_files:
        written = write_problem_files(
            result.problems,
            output_dir=args.output_dir,
            errors=result.errors,
            skipped=result.skipped,
        )
    print(
        json.dumps(
            {
                **asdict(result),
                "written": [str(path) for path in written],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not result.errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
