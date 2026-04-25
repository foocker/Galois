from __future__ import annotations

from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]


def _markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in (
        REPO_ROOT / "three_horse" / "reasoning",
        REPO_ROOT / "three_horse" / "verification",
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
    for area in ("reasoning", "verification"):
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
