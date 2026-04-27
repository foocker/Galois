from __future__ import annotations

from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]


def _markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in (
        REPO_ROOT / "three_horse" / "reasoning",
        REPO_ROOT / "three_horse" / "verification",
        REPO_ROOT / "three_horse" / "writing",
    ):
        files.extend(base.rglob("*.md"))
    return sorted(files)


def test_markdown_asset_links_resolve() -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    missing: list[str] = []

    for path in _markdown_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in link_re.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean or clean.startswith("/"):
                continue
            if any(part.startswith("<") or part.startswith("$") for part in Path(clean).parts):
                continue
            if not (path.parent / clean).resolve().exists():
                missing.append(f"{path.relative_to(REPO_ROOT)} -> {target}")

    assert missing == []


def test_rethlas_skill_references_resolve() -> None:
    missing: list[str] = []
    for area in ("reasoning", "verification", "writing"):
        base = REPO_ROOT / "three_horse" / area
        skill_names = {path.parent.name for path in (base / ".agents" / "skills").glob("*/SKILL.md")}
        docs = [base / "AGENTS.md", *sorted((base / ".agents" / "skills").glob("*/SKILL.md"))]
        for doc in docs:
            if not doc.exists():
                continue
            text = doc.read_text(encoding="utf-8", errors="ignore")
            for name in sorted(set(re.findall(r"\$([a-z][a-z0-9-]+)", text))):
                if name not in skill_names:
                    missing.append(f"{doc.relative_to(REPO_ROOT)} -> ${name}")

    assert missing == []


def test_writing_runtime_assets_do_not_depend_on_ignored_references() -> None:
    path_re = re.compile(r"`((?:\.\./)*references/[^`]+)`")
    runtime_docs = [
        REPO_ROOT / "three_horse" / "writing" / "AGENTS.md",
        *sorted((REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills").glob("*/SKILL.md")),
    ]
    offenders: list[str] = []
    for doc in runtime_docs:
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for match in path_re.finditer(text):
            target = (doc.parent / match.group(1)).resolve()
            try:
                target.relative_to(REPO_ROOT)
            except ValueError:
                offenders.append(f"{doc.relative_to(REPO_ROOT)} -> {match.group(1)}")
                continue
            if not target.exists():
                offenders.append(f"{doc.relative_to(REPO_ROOT)} -> {match.group(1)}")

    assert offenders == []


def test_math_paper_writing_skill_covers_detailed_guide_modules() -> None:
    text = (REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "math-paper-writing" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    required_phrases = [
        "deletion pass",
        "paragraph transitions",
        "journal fit",
        "proof stage",
        "reading report",
        "thesis mode",
        "submission checklist",
        "notation table",
        "equation label audit",
        "reviewer response matrix",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text.lower()]

    assert missing == []


def test_math_paper_writing_skill_has_supporting_references_without_pdfs() -> None:
    base = REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "math-paper-writing"
    required = [
        base / "references" / "principles.md",
        base / "references" / "guide.md",
        base / "references" / "case-library.md",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    pdfs = sorted(base.rglob("*.pdf"))

    assert missing == []
    assert pdfs == []


def test_math_review_skill_covers_detailed_review_modules() -> None:
    base = REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "math-review"
    required_modules = [
        base / "review-methodology" / "principles.md",
        base / "review-methodology" / "deep-review.md",
        base / "review-methodology" / "proof-verification.md",
        base / "review-methodology" / "specialized-reviews.md",
        base / "review-methodology" / "output-contracts.md",
        base / "review-methodology" / "writing-standards.md",
    ]
    missing_modules = [str(path.relative_to(REPO_ROOT)) for path in required_modules if not path.exists()]
    skill_text = (base / "SKILL.md").read_text(encoding="utf-8").lower()
    module_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore").lower()
        for path in required_modules
        if path.exists()
    )
    combined_text = f"{skill_text}\n{module_text}"
    required_phrases = [
        "standalone mathematical paper review module",
        "review-methodology/principles.md",
        "review-methodology/deep-review.md",
        "review-methodology/proof-verification.md",
        "review-methodology/specialized-reviews.md",
        "review-methodology/output-contracts.md",
        "review-methodology/writing-standards.md",
        "review task classification",
        "five iron rules",
        "seven review principles",
        "independent coordinate system",
        "credit attribution",
        "full-text prior work",
        "actual inspection of figures and tables",
        "silence as signal",
        "benchmark over absolutes",
        "signal cost",
        "strong claim",
        "assumption-use table",
        "line-by-line verification",
        "paper writing page artifact mapping",
        "revision task contract",
        "do not depend on the root-level",
        "pre-delivery self-check",
    ]
    forbidden_phrases = [
        "this file only adapts",
        "load the copied source files and apply them directly",
        "source loading policy",
        "vendored snapshot",
        "retained for provenance",
        "provenance and audit",
        "copied source snapshot",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in combined_text]
    forbidden = [phrase for phrase in forbidden_phrases if phrase in combined_text]

    assert missing_modules == []
    assert missing == []
    assert forbidden == []


def test_math_review_skill_has_no_vendored_references_snapshot() -> None:
    base = REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "math-review"
    pdfs = sorted(base.rglob("*.pdf"))

    assert not (base / "references").exists()
    assert pdfs == []


def test_math_review_is_separate_from_galois_run_outputs() -> None:
    docs = [
        REPO_ROOT / "three_horse" / "writing" / "AGENTS.md",
        REPO_ROOT / "three_horse" / "writing" / "ASSET_MANIFEST.md",
        REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "math-review" / "SKILL.md",
        REPO_ROOT
        / "three_horse"
        / "writing"
        / ".agents"
        / "skills"
        / "math-review"
        / "review-methodology"
        / "output-contracts.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8", errors="ignore").lower() for path in docs)
    required = [
        "paper writing page",
        "independent of galois reasoning runs",
        "does not consume galois run artifacts",
        "does not depend on proof-system outputs",
        "not the downstream of the galois proof system",
    ]
    forbidden = [
        "galois run may be imported",
        "imported later as optional source material",
        "proof-system outputs are optional source material",
    ]

    assert [phrase for phrase in required if phrase not in text] == []
    assert [phrase for phrase in forbidden if phrase in text] == []


def test_literature_citation_integrates_scientific_skill_sources() -> None:
    base = REPO_ROOT / "three_horse" / "writing" / ".agents" / "skills" / "literature-citation"
    required_files = [
        base / "scientific-skills" / "literature-review" / "SKILL.md",
        base / "scientific-skills" / "literature-review" / "references" / "database_strategies.md",
        base / "scientific-skills" / "literature-review" / "references" / "citation_styles.md",
        base / "scientific-skills" / "literature-review" / "assets" / "review_template.md",
        base / "scientific-skills" / "citation-management" / "SKILL.md",
        base / "scientific-skills" / "citation-management" / "references" / "bibtex_formatting.md",
        base / "scientific-skills" / "citation-management" / "references" / "citation_validation.md",
        base / "scientific-skills" / "citation-management" / "references" / "metadata_extraction.md",
        base / "scientific-skills" / "citation-management" / "assets" / "citation_checklist.md",
        base / "scientific-skills" / "citation-management" / "assets" / "bibtex_template.bib",
        base / "scientific-skills" / "paper-lookup" / "SKILL.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "arxiv.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "crossref.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "openalex.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "semantic-scholar.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "unpaywall.md",
        base / "scientific-skills" / "paper-lookup" / "references" / "core.md",
        base / "paper-writing-page.md",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required_files if not path.exists()]
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore").lower()
        for path in [base / "SKILL.md", base / "paper-writing-page.md"]
        if path.exists()
    )
    required_phrases = [
        "standalone literature and citation module for the galois paper writing page",
        "scientific-skills/literature-review/skill.md",
        "scientific-skills/citation-management/skill.md",
        "scientific-skills/paper-lookup/skill.md",
        "does not consume galois run artifacts",
        "does not depend on proof-system outputs",
        "do not depend on root-level references/scientific-agent-skills",
        "mathematical literature positioning",
        "citation_report.md",
        "lookup_needed",
        "post /api/citations/resolve",
        "post /api/citations/search",
        "post /api/citations/validate",
        "arxiv",
        "crossref",
        "openalex",
        "default chain: `arxiv`, `crossref`, and `openalex`",
        "execution chain",
    ]
    forbidden_phrases = [
        "../references/scientific-agent-skills",
        "/references/scientific-agent-skills",
        "root-level references/scientific-agent-skills as runtime",
    ]
    pdfs = sorted(base.rglob("*.pdf"))

    assert missing == []
    assert [phrase for phrase in required_phrases if phrase not in text] == []
    assert [phrase for phrase in forbidden_phrases if phrase in text] == []
    assert pdfs == []
