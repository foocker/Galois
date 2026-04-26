from __future__ import annotations

from pathlib import Path
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_local_docs_use_uv_run_cli_entrypoint() -> None:
    legacy_script = "run" + ".sh"
    legacy_shell_invocation = "sh " + "run"
    legacy_cli = "galois" + "-run"

    assert not (REPO_ROOT / legacy_script).exists()

    checked_files = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs" / "GALOIS_SYSTEM_DESIGN.md",
        REPO_ROOT / "docs" / "superpowers" / "plans" / "2026-04-25-galois-research-workbench.md",
        REPO_ROOT / "docs" / "superpowers" / "specs" / "2026-04-25-galois-research-workbench-design.md",
    ]
    stale_references: list[str] = []
    for path in checked_files:
        text = path.read_text(encoding="utf-8")
        if legacy_script in text or legacy_shell_invocation in text or legacy_cli in text:
            stale_references.append(str(path.relative_to(REPO_ROOT)))

    assert stale_references == []


def test_package_exposes_single_galois_console_script() -> None:
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"] == {
        "galois": "galois.platform.cli:main",
    }
