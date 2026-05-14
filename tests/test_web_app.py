from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient


def _write_config(path: Path, run_root: Path) -> None:
    path.write_text(
        f"""
backend = "codex"
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
personality = "pragmatic"

[codex]
bin = "codex"
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gpt-5.4"]
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gpt-5.5"]
base_url_env = "OPENAI_BASE_URL"
api_key_env = "OPENAI_API_KEY"

[models."gemini-pro-3.1"]
base_url_env = "GEMINI_BASE_URL"
api_key_env = "GEMINI_API_KEY"

[reasoning]
enabled = true
workdir = "three_horse/reasoning"

[verification]
enabled = true
workdir = "three_horse/verification"

[writing]
enabled = true
workdir = "three_horse/writing"

[database]
url_env = "DATABASE_URL"
url = "postgresql://galois:galois_dev@127.0.0.1:5432/galois"

[platform]
resume_enabled = true
max_repair_rounds = 1
benchmark_root = "benchmarks"
project_root = "{run_root.parent}"
run_root = "{run_root.name}"
""".lstrip(),
        encoding="utf-8",
    )


def test_config_loads_problem_garden_database_url(monkeypatch, tmp_path: Path) -> None:
    from galois.platform.config import load_config

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.example/v1")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")

    monkeypatch.delenv("DATABASE_URL", raising=False)
    config = load_config(config_path)
    assert config.database.connection_url == "postgresql://galois:galois_dev@127.0.0.1:5432/galois"

    monkeypatch.setenv("DATABASE_URL", "postgresql://override:secret@127.0.0.1:5432/override")
    config = load_config(config_path)
    assert config.database.connection_url == "postgresql://override:secret@127.0.0.1:5432/override"


def test_index_serves_research_workbench(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert "Galois" in response.text
    assert "Mathematics" in response.text
    assert "Learning &amp;" in response.text
    assert "<span>Research</span>" in response.text
    assert "Research Platform" not in response.text
    assert 'id="problem-title"' in response.text
    title_input = response.text[response.text.index('id="problem-title"') : response.text.index('id="problem-markdown"')]
    assert "required" in title_input


def test_index_loads_katex_assets(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert "katex.min.css" in response.text
    assert "auto-render.min.js" in response.text


def test_index_loads_markdown_rendering_assets(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert "marked.min.js" in response.text
    assert "purify.min.js" in response.text
    assert '/assets/styles.css?v=garden-graph-modal-1' in response.text
    assert '/assets/app.js?v=garden-graph-modal-1' in response.text


def test_index_contains_current_product_views(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert 'data-view="problem-solving"' in response.text
    assert 'data-view="dashboard"' in response.text
    assert 'data-view="problem-garden"' in response.text
    assert 'data-view="math-learning"' in response.text
    assert 'data-view="theorem-searching"' in response.text
    assert 'data-view="paper-writing"' in response.text
    assert 'class="problem-garden-view app-view" data-view="problem-garden"' in response.text
    assert 'id="garden-problems"' in response.text
    assert 'id="garden-detail"' in response.text
    assert 'id="garden-graph"' in response.text
    assert 'id="garden-graph-modal"' in response.text
    assert "data-garden-open-graph" in response.text
    assert "data-garden-close-graph" in response.text
    assert 'id="garden-search-form"' in response.text
    assert 'id="garden-query"' in response.text
    assert 'id="garden-status-filter"' in response.text
    assert 'id="garden-domain-filter"' in response.text
    assert 'id="garden-difficulty-filter"' in response.text
    assert 'id="garden-submit-form"' in response.text
    assert 'id="garden-submit-title"' in response.text
    assert 'id="garden-submit-statement"' in response.text
    assert 'data-garden-submit-render="statement"' in response.text
    assert 'data-garden-submit-text="statement"' in response.text
    assert 'class="garden-render-surface markdown-output"' in response.text
    assert 'id="garden-submit-source"' in response.text
    assert 'id="garden-submit-source-literature"' in response.text
    assert 'id="garden-submit-progress"' in response.text
    assert 'id="garden-submit-references"' not in response.text
    assert 'id="garden-submit-context"' not in response.text
    assert 'id="garden-edit-form"' not in response.text
    assert 'id="garden-edit-title"' not in response.text
    assert 'id="garden-edit-statement"' not in response.text
    assert "data-garden-edit-render" not in response.text
    assert "data-garden-edit-text" not in response.text
    assert "data-garden-edit-problem" not in response.text
    assert "data-garden-cancel-edit" not in response.text
    assert 'data-garden-problem-id="pfr-finite-fields"' in response.text
    assert 'data-garden-use-problem' in response.text
    assert "Polynomial Freiman-Ruzsa conjecture" in response.text
    assert "open" in response.text
    assert "frontier" in response.text
    assert 'class="paper-writing-view app-view" data-view="paper-writing"' in response.text
    assert 'id="paper-submit-button"' in response.text
    assert 'id="paper-draft"' in response.text
    assert 'id="paper-draft-preview"' in response.text
    assert 'data-paper-edit-target="draft"' in response.text
    assert 'id="paper-references-preview"' in response.text
    assert 'data-paper-edit-target="references"' in response.text
    assert 'id="paper-reviewer-preview"' in response.text
    assert 'data-paper-edit-target="reviewer"' in response.text
    assert 'data-paper-edit-target="output"' in response.text
    assert 'data-paper-draft-view="edit"' not in response.text
    assert 'data-paper-draft-view="preview"' not in response.text
    assert 'id="paper-references"' in response.text
    assert 'id="paper-references" class="paper-input paper-input-editor"' in response.text
    assert 'id="paper-reviewer"' in response.text
    assert 'id="paper-reviewer" class="paper-input paper-input-editor"' in response.text
    assert 'id="paper-min-refs"' in response.text
    assert 'id="paper-max-refs"' in response.text
    assert 'id="paper-min-pages"' in response.text
    assert 'id="paper-max-pages"' in response.text
    assert 'id="paper-review-rounds"' in response.text
    assert 'id="paper-manuscript"' not in response.text
    assert 'id="paper-theorem"' not in response.text
    assert 'id="paper-proof"' not in response.text
    assert 'id="paper-status-pill"' in response.text
    assert 'id="paper-run-id"' not in response.text
    assert 'id="paper-run-pipeline"' not in response.text
    assert 'data-paper-output="manuscript_draft"' not in response.text
    assert 'data-paper-output="citation_report"' not in response.text
    assert 'data-paper-output="review_report"' not in response.text
    assert 'data-i18n="paper.outputReview"' not in response.text
    assert "Writing agent output will appear here." not in response.text
    assert "写作 agent 输出会显示在这里。" not in response.text
    assert 'id="ledger-runs"' in response.text
    assert 'id="problem-title"' in response.text
    assert 'placeholder="Riemann Hypothesis"' not in response.text
    assert 'data-i18n-placeholder="problem.titlePlaceholder"' not in response.text
    assert 'id="problem-preview"' in response.text
    assert 'data-problem-edit-target="problem"' in response.text
    assert 'id="proof-sheet" class="output-sheet" aria-labelledby="output-title" hidden' in response.text
    assert 'id="current-run-title"' not in response.text
    assert 'id="status-pill"' not in response.text
    assert 'id="progress-ladder"' not in response.text
    assert 'id="run-id"' not in response.text
    assert 'id="run-pipeline"' not in response.text
    assert 'id="event-list"' not in response.text
    assert "Event Trail" not in response.text
    assert "事件轨迹" not in response.text
    assert 'data-i18n="config.description"' not in response.text
    assert 'data-i18n="pipeline.reasoningVerificationDesc"' not in response.text
    assert 'data-i18n="pipeline.reasoningOnlyDesc"' not in response.text
    assert 'data-i18n="pipeline.formalCheck"' not in response.text
    assert 'data-i18n="pipeline.fastDraft"' not in response.text
    assert "Time Limit" not in response.text
    assert "Heuristic Model" not in response.text
    assert "Auto-Import Context" not in response.text
    assert 'id="model-select"' in response.text
    assert ">Model Selection<" in response.text
    assert '<option value="gpt-5.4">GPT-5.4</option>' in response.text
    assert '<option value="gpt-5.5" selected>GPT-5.5</option>' in response.text
    assert '<option value="gemini-pro-3.1">Gemini Pro 3.1</option>' in response.text
    assert "gpt-5.4-mini" not in response.text
    assert "gpt-5.3-codex" not in response.text
    assert "gpt-5.2" not in response.text
    assert "base_url" not in response.text
    assert "api_key" not in response.text
    assert "300s" not in response.text
    assert "Galois-Core-v2" not in response.text
    assert 'id="problem-source"' not in response.text
    assert 'id="artifact-path"' not in response.text
    assert "Problem Statement" not in response.text
    assert "Verified Proof" not in response.text
    assert "reasoning blueprint" not in response.text
    assert "Submit a problem to produce" not in response.text
    assert ">Title<" in response.text
    assert ">Problem<" in response.text
    assert ">Preview<" not in response.text
    assert "Riemann Hypothesis" not in response.text
    assert "Draft Obligation" not in response.text
    assert "Problem Markdown" not in response.text
    assert "Live Preview" not in response.text
    assert "Example:" not in response.text
    assert "Lemma 4.2: Topological Equivalence" not in response.text
    assert "引理 4.2：拓扑等价" not in response.text
    assert 'class="main-grid app-view active" data-view="problem-solving"' in response.text
    assert 'data-view-target="problem-solving"' in response.text
    assert 'data-view-target="problem-garden"' in response.text
    assert 'data-view-target="theorem-searching"' in response.text
    assert 'data-view="problem-solution"' not in response.text
    assert 'data-view="theorem-search"' not in response.text
    assert ">Problem Solving<" in response.text
    assert ">Problem Garden<" in response.text
    assert ">Math Learning<" in response.text
    assert ">Theorem Searching<" in response.text
    assert ">Paper Writing<" in response.text
    assert ">Dashboard<" in response.text
    assert "History" in response.text
    assert 'class="login-placeholder"' in response.text
    assert "Sign In" in response.text
    assert 'data-view-target="dashboard">History' not in response.text
    assert 'class="verify-link" data-new-proof' not in response.text
    assert 'data-language-toggle' not in response.text
    assert 'data-theme-toggle' not in response.text
    assert 'id="refresh-runs"' not in response.text
    assert 'data-i18n="actions.refresh"' not in response.text
    assert "待实现" in response.text
    assert "Problem Configuration" in response.text
    assert ">Repository<" not in response.text
    assert ">Proofs<" not in response.text
    assert ">Drafts<" not in response.text
    assert response.text.index('data-view-target="problem-solving"') < response.text.index('data-view-target="problem-garden"')
    assert response.text.index('data-view-target="problem-garden"') < response.text.index('data-view-target="math-learning"')


def test_index_contains_matlas_theorem_search_workspace(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert 'class="matlas-view app-view" data-view="theorem-searching"' in response.text
    assert 'id="matlas-form"' in response.text
    assert 'id="matlas-query"' in response.text
    assert 'class="matlas-settings"' in response.text
    assert 'id="matlas-count"' in response.text
    assert 'id="matlas-results"' in response.text
    assert "Search for theorems, definitions, or related mathematical results" in response.text
    assert 'data-i18n="placeholder.theoremSearching"' not in response.text
    assert 'data-i18n="matlas.empty"' not in response.text
    assert 'data-matlas-shell="true"' not in response.text


def test_frontend_sanitizes_local_artifact_paths(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/assets/app.js")

    assert response.status_code == 200
    assert "formatArtifactLabel" not in response.text
    assert "renderLedgerRuns" in response.text
    assert "extractMathSegments" in response.text
    assert "math-source display" in response.text
    assert "isVerifiedRun" in response.text
    assert "getViewFromHash" in response.text
    assert "problem-solving" in response.text
    assert "dashboard" in response.text
    assert "math-learning" in response.text
    assert "theorem-searching" in response.text
    assert "paper-writing" in response.text
    assert "applyLocale" in response.text
    assert "applyTheme" in response.text
    assert "updateProblemPreview" in response.text
    assert "data-i18n-html" in response.text
    assert "数学学习与研究" in response.text
    assert "event-list" not in response.text
    assert "events.title" not in response.text
    assert "events.empty" not in response.text
    assert "config.timeLimit" not in response.text
    assert "config.heuristicModel" not in response.text
    assert "config.autoImport" not in response.text
    assert "config.modelSelection" in response.text
    assert "模型选择" in response.text
    assert "model: elements.model.value" in response.text
    assert "base_url" not in response.text
    assert "api_key" not in response.text
    assert "data-i18n" in response.text
    assert "snapshot.output?.content" in response.text
    assert "snapshot.problem_input?.content" in response.text
    assert "problemSource" not in response.text


def test_writing_project_api_creates_independent_writing_run(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    launches = []

    def fake_start_run_thread(**kwargs):
      launches.append(kwargs)

    monkeypatch.setattr(web, "_start_run_thread", fake_start_run_thread)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/writing/projects",
        json={
            "title": "Compactness paper",
            "project_type": "paper",
            "draft_markdown": "We prove the result.",
            "references_markdown": "@article{sample, title={Sample}}",
            "reviewer_comments": "",
            "target_journal": "",
            "requested_work": "Improve and review.",
            "min_references": 5,
            "max_references": 12,
            "min_pages": 6,
            "max_pages": 10,
            "review_rounds": 2,
            "model": "gpt-5.4",
        },
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["pipeline"] == "writing-only"
    assert payload["project_id"] == "compactness-paper"
    assert launches
    launch = launches[0]["launches"][0]
    assert launch.kind.value == "writing"
    assert launches[0]["feature_flags"].pipeline.value == "writing-only"
    input_path = Path(payload["input_path"])
    assert input_path.exists()
    input_text = input_path.read_text(encoding="utf-8")
    assert "## Draft" in input_text
    assert "We prove the result." in input_text
    assert "## References" in input_text
    assert "@article{sample" in input_text
    assert "## Writing Parameters" in input_text
    assert "min_references: 5" in input_text
    assert "max_references: 12" in input_text
    assert "min_pages: 6" in input_text
    assert "max_pages: 10" in input_text
    assert "review_rounds: 2" in input_text


def test_problem_garden_api_lists_filters_and_details(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    class FakeProblemGardenStore:
        def __init__(self, database_url: str):
            calls.append(("init", database_url))

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return None

        def initialize(self):
            calls.append(("initialize",))

        def list_problems(self, *, query=None, status=None, domain=None, difficulty=None, limit=20):
            calls.append(("list", query, status, domain, difficulty, limit))
            return [
                {
                    "id": "pfr-finite-fields",
                    "title": "Polynomial Freiman-Ruzsa conjecture",
                    "status": "open",
                    "difficulty": "frontier",
                    "domains": ["additive combinatorics", "finite fields"],
                    "source": "Peluse 2024 survey",
                    "source_url": "https://example.test/peluse",
                    "statement": "Let $A \\subseteq \\mathbb{F}_p^n$ have small doubling.",
                    "latest_progress": "Equivalent finite-field formulations are known.",
                }
            ]

        def get_problem(self, problem_id: str):
            calls.append(("get", problem_id))
            return {
                "id": problem_id,
                "title": "Polynomial Freiman-Ruzsa conjecture",
                "status": "open",
                "difficulty": "frontier",
                "domains": ["additive combinatorics", "finite fields"],
                "source": "Peluse 2024 survey",
                "source_url": "https://example.test/peluse",
                "statement": "Let $A \\subseteq \\mathbb{F}_p^n$ have small doubling.",
                "source_literature": ["Peluse 2024"],
                "progress": ["Equivalent formulations known."],
                "graph_links": [
                    {"from": "Problem", "relation": "stated_in", "to": "Peluse 2024 survey"},
                ],
            }

    monkeypatch.setattr(web, "ProblemGardenStore", FakeProblemGardenStore)
    client = TestClient(web.create_app(config_path=config_path))

    response = client.get(
        "/api/problem-garden/problems",
        params={"q": "freiman", "status": "open", "domain": "finite fields", "difficulty": "frontier"},
    )
    assert response.status_code == 200
    assert response.json()["problems"][0]["id"] == "pfr-finite-fields"
    assert calls[:2] == [
        ("init", "postgresql://galois:galois_dev@127.0.0.1:5432/galois"),
        ("initialize",),
    ]
    assert calls[2] == ("list", "freiman", "open", "finite fields", "frontier", 20)

    detail = client.get("/api/problem-garden/problems/pfr-finite-fields")
    assert detail.status_code == 200
    assert detail.json()["problem"]["graph_links"][0]["relation"] == "stated_in"


def test_problem_garden_api_submits_candidates_to_review_queue(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    class FakeProblemGardenStore:
        def __init__(self, database_url: str):
            calls.append(("init", database_url))

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return None

        def initialize(self):
            calls.append(("initialize",))

        def create_submission(self, payload):
            calls.append(("create_submission", payload))
            return {"submission_id": "submission-1", "status": "pending_review"}

    monkeypatch.setattr(web, "ProblemGardenStore", FakeProblemGardenStore)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/problem-garden/submissions",
        json={
            "title": "A new finite-field problem",
            "statement": "Determine whether every object has property $P$.",
            "source_url": "https://example.test/problem",
            "domain": "finite fields",
            "source_literature": ["A. Author, A useful survey."],
            "progress": ["Collected from a survey."],
        },
    )

    assert response.status_code == 202
    assert response.json() == {"submission_id": "submission-1", "status": "pending_review"}
    assert calls[-1][0] == "create_submission"
    submission = calls[-1][1]
    assert submission["title"] == "A new finite-field problem"
    assert submission["source_literature"] == ["A. Author, A useful survey."]
    assert submission["progress"] == ["Collected from a survey."]
    assert submission["status"] == "pending_review"

    invalid = client.post(
        "/api/problem-garden/submissions",
        json={"title": "No source", "statement": "A problem.", "source_url": " "},
    )
    assert invalid.status_code == 400
    assert invalid.json()["detail"] == "source_url must not be blank"


def test_erdos_problem_tool_normalizes_metadata_and_page_html() -> None:
    from galois.tools.erdos_problems import _ProblemPageParser, erdos_problem_to_garden_problem

    parser = _ProblemPageParser()
    parser.feed(
        """
        <html><body>
          <div id="content">If $A$ is large then\\[N \\gg 2^n.\\]</div>
          <div class="citationbox"><div id="content">Additional thanks to the web site.</div></div>
          <div id="remarks">Known remarks with <a href="/350">[350]</a>.</div>
          <div id="refs">Erdos 1931<br>Dubroff-Fox-Xu 2021</div>
          <table class="problem-reactions-table"><tbody>
            <tr class="problem-reaction-row" data-reaction-type="like">
              <td class="problem-reaction-label-cell"><strong>Likes this problem</strong></td>
              <td><span class="problem-reaction-users">old-bielefelder, Sayan_Dutta</span></td>
            </tr>
            <tr class="problem-reaction-row" data-reaction-type="collab">
              <td class="problem-reaction-label-cell"><strong>Interested in collaborating</strong></td>
              <td><span class="problem-reaction-users">None</span></td>
            </tr>
          </tbody></table>
        </body></html>
        """
    )
    page = parser.page()
    problem = erdos_problem_to_garden_problem(
        {
            "number": "1",
            "prize": "$500",
            "status": {"state": "open", "last_update": "2025-08-31"},
            "formalized": {"state": "yes", "last_update": "2025-08-31"},
            "oeis": ["A276661"],
            "tags": ["number theory", "additive combinatorics"],
        },
        page=page,
    )

    assert problem["id"] == "erdos-1"
    assert problem["title"] == "Erdős problem #1"
    assert problem["statement"] == "If $A$ is large then\\[N \\gg 2^n.\\]"
    assert "Additional thanks" not in problem["statement"]
    assert page.references == ["Erdos 1931", "Dubroff-Fox-Xu 2021"]
    assert problem["status"] == "open"
    assert problem["domains"] == ["number theory", "additive combinatorics"]
    assert "OEIS A276661: https://oeis.org/A276661" in problem["source_literature"]
    assert "related_literature" not in problem
    assert any(edge["relation"] == "linked_to_oeis" and edge["to"] == "A276661" for edge in problem["graph_links"])
    assert problem["progress"] == ["Status: open."]
    assert problem["community_reactions"] == [
        {"type": "like", "label": "Likes this problem", "users": ["old-bielefelder", "Sayan_Dutta"]},
        {"type": "collab", "label": "Interested in collaborating", "users": []},
    ]


def test_erdos_problem_tool_builds_metadata_only_entries() -> None:
    from galois.tools.erdos_problems import build_garden_problems

    problems, errors = build_garden_problems(
        [
            {
                "number": "4",
                "prize": "$10000",
                "status": {"state": "proved"},
                "formalized": {"state": "yes"},
                "tags": ["number theory"],
            },
            {
                "number": "20",
                "prize": "$1000",
                "status": {"state": "open"},
                "formalized": {"state": "yes"},
                "oeis": ["A332077"],
                "tags": ["combinatorics"],
                "comments": "sunflower conjecture",
            }
        ],
        status="open",
        limit=10,
    )

    assert errors == []
    assert problems[0]["id"] == "erdos-20"
    assert problems[0]["title"] == "Erdős problem #20: sunflower conjecture"
    assert "Metadata-only entry" in problems[0]["statement"]
    assert problems[0]["source_url"] == "https://www.erdosproblems.com/20"


def test_cli_garden_import_erdos_dry_run_uses_tools_cache(monkeypatch, tmp_path: Path, capsys) -> None:
    from galois.platform.cli import cmd_import_erdos_problems

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    cache = tmp_path / "problems.yaml"
    cache.write_text(
        """
        - number: "1"
          prize: "$500"
          status:
            state: "open"
          formalized:
            state: "yes"
          oeis: ["A276661"]
          tags: ["number theory"]
        """,
        encoding="utf-8",
    )

    result = cmd_import_erdos_problems(
        config_path=config_path,
        source_url=None,
        cache_path=cache,
        no_fetch_yaml=True,
        fetch_pages=False,
        status="open",
        limit=None,
        dry_run=True,
    )

    assert result == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["records"] == 1
    assert payload["parsed"] == 1
    assert payload["sample_ids"] == ["erdos-1"]


def test_open_problem_garden_tool_parses_category_and_problem_html() -> None:
    from galois.tools.open_problem_garden import (
        CATEGORY_BY_SLUG,
        opg_problem_to_garden_problem,
        parse_category_page,
        parse_problem_page,
    )

    category = CATEGORY_BY_SLUG["algebra"]
    links, max_page = parse_category_page(
        """
        <table><tbody>
          <tr><td class="view-field view-field-node-title">
            <a href="/op/finite_congruence_lattice_problem">Finite Lattice Representation Problem</a>
          </td></tr>
        </tbody></table>
        <div id="pager"><a href="/category/algebra?page=1">2</a><a href="/category/algebra?page=2">3</a></div>
        """,
        category,
    )
    assert max_page == 2
    assert links[0].slug == "finite_congruence_lattice_problem"
    assert links[0].url == "http://www.openproblemgarden.org/op/finite_congruence_lattice_problem"

    page = parse_problem_page(
        """
        <html><body>
          <h1 class="title">Finite Lattice Representation Problem</h1>
          <div class="metatable">
            <table><tr><td>Importance:</td><td>High</td></tr>
            <tr><td>Subject:</td><td><a href="/category/algebra">Algebra</a></td></tr>
            <tr><td>Keywords:</td><td><a href="/keywords/lattices">lattices</a></td></tr></table>
          </div>
          <div class="problem"><p>Represent every finite lattice as <img class="teximage" alt="$Con A$" />.</p></div>
          <div class="discussion"><p>Known for several restricted classes.</p></div>
          <div class="related"><h2 class="OP">Related problems</h2><a href="/op/other_problem">Other problem</a></div>
          <div class="bibliography"><h2 class="OP">Bibliography</h2><p>[GS] Grätzer and Schmidt.</p></div>
        </body></html>
        """
    )
    problem = opg_problem_to_garden_problem(links[0], page, category=category)

    assert problem["id"] == "opg-finite_congruence_lattice_problem"
    assert problem["title"] == "Finite Lattice Representation Problem"
    assert problem["status"] == "open"
    assert problem["difficulty"] == "frontier"
    assert problem["domains"] == ["Algebra", "lattices"]
    assert problem["statement"] == "Represent every finite lattice as $Con A$ ."
    assert problem["progress"] == ["Known for several restricted classes."]
    assert "[GS] Grätzer and Schmidt." in problem["source_literature"]
    assert "graph_links" not in problem


def test_open_problem_garden_tool_skips_spam_and_writes_problem_files(tmp_path: Path) -> None:
    from galois.tools.open_problem_garden import is_probable_spam, write_problem_files

    assert is_probable_spam("Write my essay assignment help", "/op/write_my_essay_assignment_help")
    assert not is_probable_spam("Finite Lattice Representation Problem")

    written = write_problem_files(
        [
            {
                "id": "opg-finite_lattice",
                "title": "Finite Lattice Representation Problem",
                "status": "open",
                "difficulty": "frontier",
                "domains": ["Algebra", "lattices"],
                "source": "Open Problem Garden",
                "source_url": "http://www.openproblemgarden.org/op/finite_lattice",
                "statement": "Represent every finite lattice as $Con A$.",
                "source_literature": ["http://www.openproblemgarden.org/op/finite_lattice", "[GS] Grätzer and Schmidt."],
                "progress": ["Status: open."],
            }
        ],
        output_dir=tmp_path / "open_problem_garden",
        skipped=[{"slug": "spam", "title": "Write my essay", "reason": "probable spam"}],
    )

    assert tmp_path / "open_problem_garden" / "algebra" / "opg-finite_lattice.md" in written
    markdown = (tmp_path / "open_problem_garden" / "algebra" / "opg-finite_lattice.md").read_text(encoding="utf-8")
    assert "# Statement" in markdown
    assert "# Source literature" in markdown
    assert "# Progress" in markdown
    assert "Related literature" not in markdown
    assert "Graph links" not in markdown
    index = json.loads((tmp_path / "open_problem_garden" / "index.json").read_text(encoding="utf-8"))
    assert index["count"] == 1
    assert index["skipped"][0]["reason"] == "probable spam"
    stale = tmp_path / "open_problem_garden" / "algebra" / "opg-stale.md"
    stale.write_text("stale", encoding="utf-8")
    write_problem_files([], output_dir=tmp_path / "open_problem_garden")
    assert not stale.exists()


def test_cli_garden_import_open_problem_garden_dry_run(monkeypatch, tmp_path: Path, capsys) -> None:
    from galois.platform.cli import cmd_import_open_problem_garden
    from galois.tools.open_problem_garden import OpenProblemGardenCrawlResult

    def fake_crawl_open_problem_garden(**kwargs):
        assert kwargs["category_slugs"] == ["algebra"]
        assert kwargs["limit"] == 1
        assert kwargs["pages"] == 1
        return OpenProblemGardenCrawlResult(
            problems=[
                {
                    "id": "opg-test",
                    "title": "Test problem",
                    "status": "open",
                    "difficulty": "research",
                    "domains": ["Algebra"],
                    "source": "Open Problem Garden",
                    "source_url": "http://www.openproblemgarden.org/op/test",
                    "statement": "Statement.",
                    "source_literature": ["http://www.openproblemgarden.org/op/test"],
                    "progress": ["Status: open."],
                    "community_reactions": [],
                    "graph_links": [],
                }
            ],
            skipped=[],
            errors=[],
            source_urls=["http://www.openproblemgarden.org/category/algebra"],
        )

    monkeypatch.setattr("galois.tools.open_problem_garden.crawl_open_problem_garden", fake_crawl_open_problem_garden)
    result = cmd_import_open_problem_garden(
        config_path=None,
        output_dir=tmp_path / "opg",
        cache_dir=tmp_path / "cache",
        category_slugs=["algebra"],
        limit=1,
        pages=1,
        include_spam=False,
        no_cache=False,
        delay=0.0,
        timeout=30.0,
        max_workers=4,
        dry_run=True,
        write_files=True,
        clean_output=True,
        import_db=True,
    )

    assert result == 0
    assert not (tmp_path / "opg").exists()
    payload = json.loads(capsys.readouterr().out)
    assert payload["parsed"] == 1
    assert payload["sample_ids"] == ["opg-test"]
    assert payload["written"] == []
    assert payload["imported"] == 0


def test_problem_garden_store_initializes_schema_and_submission_in_live_postgres(monkeypatch) -> None:
    database_url = "postgresql://galois:galois_dev@127.0.0.1:5432/galois"
    import psycopg

    try:
        with psycopg.connect(database_url, connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
    except psycopg.OperationalError:
        return

    from galois.platform.problem_garden import ProblemGardenStore

    with ProblemGardenStore(database_url) as store:
        store.initialize()
        problems = store.list_problems(query="Freiman", status="open", domain="finite fields", difficulty="frontier")
        assert any(problem["id"] == "pfr-finite-fields" for problem in problems)
        detail = store.get_problem("pfr-finite-fields")
        assert detail is not None
        assert detail["graph_links"]
        with store.connection.cursor() as cursor:
            cursor.execute("DELETE FROM garden_submissions WHERE id = %s", ("test-submission-live-postgres",))
        store.connection.commit()
        created = store.create_submission(
            {
                "id": "test-submission-live-postgres",
                "title": "Live PostgreSQL submission test",
                "statement": "A statement used by the test suite.",
                "source_url": "https://example.test/live-postgres-submission",
                "domain": "test",
                "source_literature": ["Test reference."],
                "progress": ["Created by pytest and cleaned up immediately."],
                "status": "pending_review",
            }
        )
        assert created == {"submission_id": "test-submission-live-postgres", "status": "pending_review"}
        imported = store.upsert_problems(
            [
                {
                    "id": "erdos-test-live-postgres",
                    "title": "Erdős test import",
                    "statement": "Imported statement.",
                    "status": "open",
                    "difficulty": "research",
                    "domains": ["number theory"],
                    "source": "teorth/erdosproblems",
                    "source_url": "https://www.erdosproblems.com/test",
                    "source_literature": ["https://www.erdosproblems.com/test"],
                    "progress": ["Status: open."],
                    "graph_links": [
                        {"from": "Problem", "relation": "imported_from", "to": "teorth/erdosproblems"},
                    ],
                }
            ]
        )
        assert imported == 1
        imported_detail = store.get_problem("erdos-test-live-postgres")
        assert imported_detail is not None
        assert imported_detail["graph_links"][0]["relation"] == "imported_from"
        store.upsert_problem(
            {
                "id": "erdos-test-live-postgres",
                "title": "Erdős test import",
                "statement": "Metadata-only entry for Erdős problem #test. Open the source page for the full problem statement: https://www.erdosproblems.com/test",
                "status": "open",
                "difficulty": "research",
                "domains": ["number theory"],
                "source": "teorth/erdosproblems",
                "source_url": "https://www.erdosproblems.com/test",
                "source_literature": ["https://www.erdosproblems.com/test"],
                "progress": ["Status: open."],
                "graph_links": [
                    {"from": "Problem", "relation": "imported_from", "to": "teorth/erdosproblems"},
                ],
            }
        )
        preserved_detail = store.get_problem("erdos-test-live-postgres")
        assert preserved_detail is not None
        assert preserved_detail["statement"] == "Imported statement."
        store.record_import_batch(
            batch_id="test-erdos-live-postgres",
            source_name="teorth/erdosproblems",
            source_url="https://example.test/problems.yaml",
            item_count=1,
            imported_count=1,
            skipped_count=0,
            fetch_pages=False,
        )
        with store.connection.cursor() as cursor:
            cursor.execute("DELETE FROM garden_problems WHERE id = %s", ("erdos-test-live-postgres",))
            cursor.execute("DELETE FROM garden_import_batches WHERE id = %s", ("test-erdos-live-postgres",))
            cursor.execute("DELETE FROM garden_submissions WHERE id = %s", ("test-submission-live-postgres",))
        store.connection.commit()


def test_matlas_search_proxy_posts_to_public_api(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    def fake_post(endpoint: str, payload: dict[str, object]) -> object:
        calls.append((endpoint, payload))
        return [
            {
                "type": "paper",
                "entity_name": "RIEMANN HYPOTHESIS CONJECTURE",
                "doi": "doi.org/10.1006/jfan.1994.1046",
                "title": "A conjecture which implies the Riemann hypothesis",
                "authors": "de Branges, Louis",
                "journal": "J. Funct. Anal.",
                "year": "1994",
                "statement": "The Riemann hypothesis is the conjecture that $\\zeta(s)$ has no zeros.",
                "candidate_id": "candidate-1",
            }
        ]

    monkeypatch.setattr(web, "_post_matlas_json", fake_post)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post("/api/matlas/search", json={"query": "Riemann hypothesis", "num_results": 10})

    assert response.status_code == 200
    assert response.json()["results"][0]["candidate_id"] == "candidate-1"
    assert calls == [("/api/search", {"query": "Riemann hypothesis", "num_results": 10})]


def test_matlas_feedback_proxy_posts_relevance_label(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    def fake_post(endpoint: str, payload: dict[str, object]) -> object:
        calls.append((endpoint, payload))
        return {"ok": True}

    monkeypatch.setattr(web, "_post_matlas_json", fake_post)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/matlas/feedback",
        json={"query": "Riemann hypothesis", "candidate_id": "candidate-1", "label": "relevant"},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert calls == [
        (
            "/api/feedback",
            {"query": "Riemann hypothesis", "candidate_id": "candidate-1", "label": "relevant"},
        )
    ]


def test_citation_lookup_api_resolves_identifier(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    class FakeCitationLookupService:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return None

        def resolve(self, identifier, sources=None):
            calls.append(("resolve", identifier, sources))
            return {"identifier": identifier, "sources": sources, "verification_level": "metadata_found"}

    monkeypatch.setattr(web, "CitationLookupService", FakeCitationLookupService)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/citations/resolve",
        json={"identifier": "10.1234/example", "sources": ["crossref"]},
    )

    assert response.status_code == 200
    assert response.json()["verification_level"] == "metadata_found"
    assert calls[1] == ("resolve", "10.1234/example", ["crossref"])


def test_citation_lookup_api_searches_sources(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    class FakeCitationLookupService:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return None

        def search(self, query, sources=None, limit=10):
            calls.append(("search", query, sources, limit))
            return {"query": query, "sources": sources, "records": [{"source": "arxiv", "status": "ok"}]}

    monkeypatch.setattr(web, "CitationLookupService", FakeCitationLookupService)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/citations/search",
        json={"query": "compactness theorem", "sources": ["arxiv"], "limit": 5},
    )

    assert response.status_code == 200
    assert response.json()["records"] == [{"source": "arxiv", "status": "ok"}]
    assert calls[1] == ("search", "compactness theorem", ["arxiv"], 5)


def test_citation_lookup_api_validates_bibtex(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    calls = []

    class FakeCitationLookupService:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return None

        def validate_bibtex(self, bibtex, sources=None):
            calls.append(("validate", bibtex, sources))
            return {"entry_count": 1, "entries": [{"key": "x", "status": "verified"}]}

    monkeypatch.setattr(web, "CitationLookupService", FakeCitationLookupService)
    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/citations/validate",
        json={"bibtex": "@article{x, title={T}, author={A}, year={2024}, doi={10.1/x}}", "sources": ["crossref"]},
    )

    assert response.status_code == 200
    assert response.json()["entries"][0]["status"] == "verified"
    assert calls[1][0] == "validate"


def test_frontend_matlas_search_renders_returned_results() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    checked: false,
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name]; }},
    closest() {{ return fakeElement(); }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{ this.focused = true; }},
  }};
  element.classList = fakeClassList();
  return element;
}}

const views = [
  fakeElement({{ view: "problem-solving" }}),
  fakeElement({{ view: "dashboard" }}),
  fakeElement({{ view: "math-learning" }}),
  fakeElement({{ view: "theorem-searching" }}),
  fakeElement({{ view: "paper-writing" }}),
];
const buttons = [
  fakeElement({{ viewTarget: "problem-solving" }}),
  fakeElement({{ viewTarget: "theorem-searching" }}),
];
const root = {{ lang: "en", dataset: {{}}, classList: fakeClassList() }};
const elementMap = new Map();
const document = {{
  documentElement: root,
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return views;
    if (selector === "[data-view-target]") return buttons;
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const storage = {{}};
const localStorage = {{
  getItem(key) {{ return storage[key] || null; }},
  setItem(key, value) {{ storage[key] = String(value); }},
  removeItem(key) {{ delete storage[key]; }},
}};
const window = {{
  location: {{ hash: "#theorem-searching" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage,
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetchCalls = [];
const fetch = async (url, options = {{}}) => {{
  fetchCalls.push([url, options]);
  if (url === "/api/matlas/search") {{
    const body = JSON.parse(options.body);
    if (body.query !== "Riemann hypothesis") throw new Error(`unexpected query: ${{body.query}}`);
    if (body.num_results !== 10) throw new Error(`unexpected count: ${{body.num_results}}`);
    return {{
      ok: true,
      json: async () => ({{
        results: [{{
          type: "paper",
          entity_name: "RIEMANN HYPOTHESIS CONJECTURE",
          doi: "doi.org/10.1006/jfan.1994.1046",
          title: "A conjecture which implies the Riemann hypothesis",
          authors: "de Branges, Louis",
          journal: "J. Funct. Anal.",
          year: "1994",
          statement: "The Riemann hypothesis is the conjecture that $\\\\zeta(s)$ has no zeros.",
          candidate_id: "candidate-1",
        }}, {{
          type: "paper",
          title: "A URL-only Matlas result",
          authors: "Example Author",
          year: "2025",
          url: "https://example.org/matlas/result",
          statement: "This result only provides a URL field.",
          candidate_id: "candidate-2",
        }}, {{
          type: "preprint",
          title: "An arXiv-only Matlas result",
          arxiv_id: "2401.01234v2",
          statement: "This result only provides an arXiv id.",
          candidate_id: "candidate-3",
        }}, {{
          type: "note",
          title: "A result without an external link",
          entity_name: "Fallback source",
          statement: "This result has no DOI, URL, or arXiv id.",
          candidate_id: "candidate-4",
        }}, {{
          type: "book",
          title: "Counting: The Art of Enumerative Combinatorics",
          authors: "George E. Martin",
          statement: "This book result only provides title and author metadata.",
          candidate_id: "candidate-5",
        }}],
      }}),
    }};
  }}
  return {{ ok: true, json: async () => ({{ runs: [] }}) }};
}};
const context = {{
  console,
  document,
  window,
  localStorage,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

(async () => {{
  vm.runInNewContext(code, context);
  elementMap.get("#matlas-query").value = "Riemann hypothesis";
  elementMap.get("#matlas-count").value = "10";
  await context.submitMatlasSearch({{ preventDefault() {{}} }});
  const resultsHtml = elementMap.get("#matlas-results").innerHTML;
  if (!resultsHtml.includes('class="matlas-card"')) throw new Error(resultsHtml);
  if (!resultsHtml.includes("A conjecture which implies the Riemann hypothesis")) throw new Error(resultsHtml);
  if (!resultsHtml.includes('<a href="https://doi.org/10.1006/jfan.1994.1046" target="_blank" rel="noreferrer">A conjecture which implies the Riemann hypothesis</a>')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('<a href="https://example.org/matlas/result" target="_blank" rel="noreferrer">A URL-only Matlas result</a>')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('<a href="https://arxiv.org/abs/2401.01234v2" target="_blank" rel="noreferrer">An arXiv-only Matlas result</a>')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('<a href="https://www.google.com/search?q=A%20result%20without%20an%20external%20link%20Fallback%20source')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('target="_blank" rel="noreferrer">A result without an external link</a>')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('<a href="https://www.google.com/search?q=Counting%3A%20The%20Art%20of%20Enumerative%20Combinatorics')) throw new Error(resultsHtml);
  if (!resultsHtml.includes('target="_blank" rel="noreferrer">Counting: The Art of Enumerative Combinatorics</a>')) throw new Error(resultsHtml);
  if (!resultsHtml.includes("RIEMANN HYPOTHESIS CONJECTURE")) throw new Error(resultsHtml);
  if (elementMap.get("#matlas-message").textContent !== "") throw new Error("search message should clear after results render");
  const searchCalls = fetchCalls.filter(([url]) => url === "/api/matlas/search");
  if (searchCalls.length !== 1) throw new Error(`expected one Matlas request, got ${{searchCalls.length}}`);
}})().catch((error) => {{
  console.error(error.stack || error.message);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_writing_output_renders_final_manuscript_and_enters_edit_mode() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  return {{
    toggle() {{}},
    contains() {{ return false; }},
    add() {{}},
    remove() {{}},
  }};
}}

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    checked: false,
    classList: fakeClassList(),
    addEventListener() {{}},
    setAttribute() {{}},
    getAttribute() {{ return ""; }},
    closest() {{ return {{ querySelectorAll() {{ return []; }}, classList: fakeClassList() }}; }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const paperOutput = fakeElement();
const paperOutputEditor = fakeElement();
paperOutputEditor.focus = function () {{ this.focused = true; }};
const elementMap = new Map([["#paper-output", paperOutput]]);
elementMap.set("#paper-output-editor", paperOutputEditor);
const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "paper-writing" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "paper-writing" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "#paper-writing" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
  JSON,
}};

vm.runInNewContext(code, context);
context.renderWritingSnapshot({{
  status: "succeeded",
  run_id: "run-1",
  pipeline: "writing-only",
  output: {{
    artifacts: {{
      manuscript_draft: {{ content: "# Draft\\nManuscript text" }},
      review_report: {{ content: "# Review\\nReview text" }},
      citation_report: {{ content: "# References\\n\\n1. Smith, A. Example paper. Journal 1 (2024). DOI: 10.1000/example\\n\\n## Citation Audit\\n- A lookup task that should not become a reference." }},
    }},
  }},
}});
if (!paperOutput.innerHTML.includes("Manuscript text")) throw new Error(paperOutput.innerHTML);
if (paperOutput.innerHTML.includes("Review text")) throw new Error(paperOutput.innerHTML);
if (paperOutput.innerHTML.includes("citation-list")) throw new Error(paperOutput.innerHTML);
context.setPaperOutputEditMode(true);
if (paperOutput.hidden !== true) throw new Error("rendered output should hide in edit mode");
if (paperOutputEditor.hidden !== false) throw new Error("output editor should show in edit mode");
if (!paperOutputEditor.value.includes("Manuscript text")) throw new Error(paperOutputEditor.value);
paperOutputEditor.value = "# Edited\\nRevised text";
context.setPaperOutputEditMode(false);
if (paperOutput.hidden !== false) throw new Error("rendered output should show after editing");
if (paperOutputEditor.hidden !== true) throw new Error("output editor should hide after editing");
if (!paperOutput.innerHTML.includes("Revised text")) throw new Error(paperOutput.innerHTML);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_matlas_enter_key_submits_search_box() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const listeners = {{}};
  const element = {{
    dataset,
    listeners,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    submitCount: 0,
    addEventListener(type, listener) {{
      listeners[type] = listener;
    }},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    closest() {{ return fakeElement(); }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{ this.submitCount += 1; }},
    scrollIntoView() {{}},
    focus() {{}},
  }};
  element.classList = fakeClassList();
  return element;
}}

const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [
      fakeElement({{ view: "problem-solving" }}),
      fakeElement({{ view: "theorem-searching" }}),
    ];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "theorem-searching" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "#theorem-searching" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const query = elementMap.get("#matlas-query");
const form = elementMap.get("#matlas-form");
query.listeners.keydown({{
  key: "Enter",
  shiftKey: false,
  metaKey: false,
  ctrlKey: false,
  preventDefault() {{
    this.defaultPrevented = true;
  }},
}});
if (form.submitCount !== 1) throw new Error(`plain Enter should submit once, got ${{form.submitCount}}`);
query.listeners.keydown({{
  key: "Enter",
  shiftKey: true,
  metaKey: false,
  ctrlKey: false,
  preventDefault() {{
    this.defaultPrevented = true;
  }},
}});
if (form.submitCount !== 1) throw new Error("Shift+Enter should keep textarea newline behavior");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_renders_multiline_display_math_with_katex_core() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains(name) {{ return false; }} }},
    addEventListener() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const document = {{
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};

const katexCalls = [];
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  katex: {{
    render(math, node, options) {{
      katexCalls.push({{ math, displayMode: options.displayMode, throwOnError: options.throwOnError }});
      node.textContent = `[rendered:${{math}}]`;
    }},
  }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const html = context.renderMarkdownLite("Before\\n\\n$$\\na^2+b^2=c^2\\n\\\\tag{{1}}\\n$$\\n\\nAfter");
if (!html.includes('class="math-source display"')) throw new Error("display math placeholder missing");
if (html.includes("$$a^2")) throw new Error("display delimiters leaked into math placeholder");

const mathNode = {{
  textContent: "\\na^2+b^2=c^2\\n\\\\tag{{1}}\\n",
  classList: {{ contains(name) {{ return name === "display"; }} }},
  replaceWith() {{}},
}};
context.renderMath({{ querySelectorAll() {{ return [mathNode]; }} }});
if (katexCalls.length !== 1) throw new Error(`expected 1 KaTeX call, got ${{katexCalls.length}}`);
if (katexCalls[0].math !== "a^2+b^2=c^2\\n\\\\tag{{1}}") throw new Error(`unexpected math: ${{katexCalls[0].math}}`);
if (katexCalls[0].displayMode !== true) throw new Error("displayMode should be true for $$ blocks");
if (katexCalls[0].throwOnError !== false) throw new Error("throwOnError should stay false");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_problem_editor_defaults_to_rendered_view_and_enters_edit_mode() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    classList: {{ toggle() {{}}, contains(name) {{ return false; }}, remove() {{}}, add() {{}} }},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name] || ""; }},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const markdown = fakeElement();
markdown.focus = function () {{ this.focused = true; }};
const preview = fakeElement({{ paperRender: "draft" }});
preview.querySelectorAll = () => [mathNode];
const mathNode = {{
  textContent: "x^2",
  classList: {{ contains(name) {{ return name === "inline"; }}, remove() {{}}, add() {{}} }},
  replaceWith() {{}},
}};
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#problem-markdown") return markdown;
    if (selector === "#problem-preview") return preview;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const katexCalls = [];
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  katex: {{
    render(math, node, options) {{
      katexCalls.push({{ math, displayMode: options.displayMode }});
      node.textContent = `[rendered:${{math}}]`;
    }},
  }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
markdown.value = "# Problem\\n\\nShow $x^2$.";
context.updateProblemPreview();
if (!preview.innerHTML.includes("<h1>Problem</h1>")) throw new Error(preview.innerHTML);
if (!preview.innerHTML.includes('class="math-source inline"')) throw new Error(preview.innerHTML);
if (katexCalls.length !== 1) throw new Error(`expected preview KaTeX call, got ${{katexCalls.length}}`);
if (katexCalls[0].math !== "x^2") throw new Error(`unexpected math: ${{katexCalls[0].math}}`);
context.setProblemEditMode(false);
if (markdown.hidden !== true) throw new Error("problem editor should be hidden in rendered mode");
if (preview.hidden !== false) throw new Error("problem render should be visible in rendered mode");
if (preview.getAttribute("tabindex") !== "0") throw new Error("problem render should be focusable");
context.setProblemEditMode(true);
if (markdown.hidden !== false) throw new Error("problem editor should show in edit mode");
if (preview.hidden !== true) throw new Error("problem render should hide in edit mode");
if (markdown.focused !== true) throw new Error("problem editor should be focused");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_paper_draft_editor_updates_markdown_preview() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
  textContent: "",
  innerHTML: "",
  className: "",
  attributes: {{}},
  classList: fakeClassList(),
  addEventListener() {{}},
  setAttribute(name, value) {{ this.attributes[name] = String(value); }},
  getAttribute(name) {{ return this.attributes[name] || ""; }},
    closest() {{ return {{ querySelectorAll() {{ return []; }}, classList: fakeClassList() }}; }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const draft = fakeElement({{ paperInput: "draft" }});
const references = fakeElement({{ paperInput: "references" }});
const preview = fakeElement({{ paperRender: "draft" }});
const referencesPreview = fakeElement({{ paperRender: "references" }});
draft.focus = function () {{ this.focused = true; }};
references.focus = function () {{ this.focused = true; }};
const mathNode = {{
  textContent: "x^2",
  classList: {{ contains(name) {{ return name === "inline"; }}, remove() {{}}, add() {{}} }},
  replaceWith() {{}},
}};
preview.querySelectorAll = () => [mathNode];
referencesPreview.querySelectorAll = () => [];

const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (selector === "#paper-draft") return draft;
    if (selector === "#paper-draft-preview") return preview;
    if (selector === "#paper-references") return references;
    if (selector === "#paper-references-preview") return referencesPreview;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "paper-writing" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "paper-writing" }})];
    if (selector === "[data-paper-input]") return [draft, references];
    if (selector === "[data-paper-render]") return [preview, referencesPreview];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const katexCalls = [];
const window = {{
  location: {{ hash: "#paper-writing" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
  katex: {{
    render(math, node, options) {{
      katexCalls.push({{ math, displayMode: options.displayMode }});
      node.textContent = `[rendered:${{math}}]`;
    }},
  }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
  JSON,
}};

vm.runInNewContext(code, context);
draft.value = "# Draft\\n\\nShow $x^2$.";
context.renderPaperDraftPreview();
if (!preview.innerHTML.includes("<h1>Draft</h1>")) throw new Error(preview.innerHTML);
if (!preview.innerHTML.includes('class="math-source inline"')) throw new Error(preview.innerHTML);
if (katexCalls.length !== 1) throw new Error(`expected draft preview KaTeX call, got ${{katexCalls.length}}`);
context.setPaperDraftEditMode(false);
if (draft.hidden !== true) throw new Error("draft editor should be hidden in rendered mode");
if (preview.hidden !== false) throw new Error("draft preview should be visible in rendered mode");
if (preview.getAttribute("tabindex") !== "0") throw new Error("draft preview should be keyboard-focusable");
context.setPaperDraftEditMode(true);
if (draft.hidden !== false) throw new Error("draft editor should be visible in edit mode");
if (preview.hidden !== true) throw new Error("draft preview should be hidden in edit mode");
if (draft.focused !== true) throw new Error("draft editor should be focused in edit mode");
references.value = "# References\\n\\n- Smith 2024";
context.renderPaperInputPreview("references");
if (!referencesPreview.innerHTML.includes("<h1>References</h1>")) throw new Error(referencesPreview.innerHTML);
context.setPaperInputEditMode("references", false);
if (references.hidden !== true) throw new Error("references editor should be hidden in rendered mode");
if (referencesPreview.hidden !== false) throw new Error("references preview should be visible in rendered mode");
context.setPaperInputEditMode("references", true);
if (references.hidden !== false) throw new Error("references editor should show in edit mode");
if (referencesPreview.hidden !== true) throw new Error("references preview should hide in edit mode");
if (references.focused !== true) throw new Error("references editor should be focused");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_problem_garden_selects_and_sends_problem_to_solver() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name]; }},
    closest() {{ return fakeElement(); }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{ this.focused = true; }},
  }};
  element.classList = fakeClassList();
  return element;
}}

const views = [
  fakeElement({{ view: "problem-solving" }}),
  fakeElement({{ view: "problem-garden" }}),
  fakeElement({{ view: "dashboard" }}),
  fakeElement({{ view: "math-learning" }}),
  fakeElement({{ view: "theorem-searching" }}),
  fakeElement({{ view: "paper-writing" }}),
];
const buttons = [
  fakeElement({{ viewTarget: "problem-solving" }}),
  fakeElement({{ viewTarget: "problem-garden" }}),
];
const problemTitle = fakeElement();
const problemMarkdown = fakeElement();
const problemPreview = fakeElement();
const gardenProblems = fakeElement();
const gardenDetail = fakeElement();
const gardenGraph = fakeElement();
const elementMap = new Map([
  ["#problem-title", problemTitle],
  ["#problem-markdown", problemMarkdown],
  ["#problem-preview", problemPreview],
  ["#garden-problems", gardenProblems],
  ["#garden-detail", gardenDetail],
  ["#garden-graph", gardenGraph],
]);
const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return views;
    if (selector === "[data-view-target]") return buttons;
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "#problem-garden" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
  JSON,
}};

vm.runInNewContext(code, context);
context.renderProblemGarden("pfr-finite-fields");
if (!gardenProblems.innerHTML.includes("Polynomial Freiman-Ruzsa conjecture")) throw new Error(gardenProblems.innerHTML);
if (!gardenProblems.innerHTML.includes("frontier")) throw new Error(gardenProblems.innerHTML);
if (!gardenDetail.innerHTML.includes("Source literature")) throw new Error(gardenDetail.innerHTML);
if (!gardenDetail.innerHTML.includes("Progress")) throw new Error(gardenDetail.innerHTML);
if (gardenDetail.innerHTML.includes("Known core ideas")) throw new Error(gardenDetail.innerHTML);
if (!gardenGraph.innerHTML.includes("uses_method")) throw new Error(gardenGraph.innerHTML);
context.useGardenProblem("pfr-finite-fields");
if (problemTitle.value !== "Polynomial Freiman-Ruzsa conjecture") throw new Error(problemTitle.value);
if (!problemMarkdown.value.includes("## Problem")) throw new Error(problemMarkdown.value);
if (!problemMarkdown.value.includes("## Source literature")) throw new Error(problemMarkdown.value);
if (!problemMarkdown.value.includes("## Progress")) throw new Error(problemMarkdown.value);
if (window.location.hash !== "#problem-solving") throw new Error(window.location.hash);
if (problemMarkdown.focused !== true) throw new Error("problem markdown should be focused");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_problem_garden_submit_markdown_fields_render_by_default() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  return {{ toggle() {{}}, contains() {{ return false; }}, add() {{}}, remove() {{}} }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    classList: fakeClassList(),
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name] || ""; }},
    closest() {{ return fakeElement(); }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{ this.focused = true; }},
  }};
  return element;
}}

const statement = fakeElement({{ gardenSubmitText: "statement" }});
const statementRender = fakeElement({{ gardenSubmitRender: "statement" }});
statementRender.querySelectorAll = () => [mathNode];
const sourceLiterature = fakeElement({{ gardenSubmitText: "source-literature" }});
const sourceLiteratureRender = fakeElement({{ gardenSubmitRender: "source-literature" }});
sourceLiteratureRender.querySelectorAll = () => [];
const mathNode = {{
  textContent: "A+A",
  classList: {{ contains(name) {{ return name === "inline"; }}, remove() {{}}, add() {{}} }},
  replaceWith() {{}},
}};
const elementMap = new Map([
  ["#garden-submit-statement", statement],
  ["#garden-submit-source-literature", sourceLiterature],
]);
const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-garden" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-garden" }})];
    if (selector === "[data-garden-submit-text]") return [statement, sourceLiterature];
    if (selector === "[data-garden-submit-render]") return [statementRender, sourceLiteratureRender];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const katexCalls = [];
const window = {{
  location: {{ hash: "#problem-garden" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
  katex: {{
    render(math) {{
      katexCalls.push(math);
    }},
  }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
  JSON,
}};

vm.runInNewContext(code, context);
statement.value = "# Statement\\nLet $A+A$ be small.";
sourceLiterature.value = "- Smith 2024";
context.setGardenSubmitFieldMode("statement", false);
if (statement.hidden !== true) throw new Error("statement textarea should hide in render mode");
if (statementRender.hidden !== false) throw new Error("statement render should show by default");
if (!statementRender.innerHTML.includes("<h1>Statement</h1>")) throw new Error(statementRender.innerHTML);
if (katexCalls[0] !== "A+A") throw new Error(`expected math render, got ${{katexCalls[0]}}`);
context.setGardenSubmitFieldMode("statement", true);
if (statement.hidden !== false) throw new Error("statement textarea should show in edit mode");
if (statementRender.hidden !== true) throw new Error("statement render should hide in edit mode");
if (statement.focused !== true) throw new Error("statement textarea should be focused");
context.renderGardenSubmitField("source-literature");
if (!sourceLiteratureRender.innerHTML.includes("<li>Smith 2024</li>")) throw new Error(sourceLiteratureRender.innerHTML);
sourceLiterature.value = "";
context.renderGardenSubmitField("source-literature");
if (sourceLiteratureRender.innerHTML !== "") throw new Error(`blank submit render should stay empty: ${{sourceLiteratureRender.innerHTML}}`);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_problem_garden_searches_and_submits_via_api() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name]; }},
    closest() {{ return fakeElement(); }},
    contains() {{ return false; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{ this.focused = true; }},
    reset() {{ this.resetCalled = true; }},
  }};
  element.classList = fakeClassList();
  return element;
}}

const views = [
  fakeElement({{ view: "problem-solving" }}),
  fakeElement({{ view: "problem-garden" }}),
];
const buttons = [fakeElement({{ viewTarget: "problem-garden" }})];
const gardenProblems = fakeElement();
const gardenDetail = fakeElement();
const gardenGraph = fakeElement();
const gardenSearchForm = fakeElement();
const gardenQuery = fakeElement();
const gardenDomain = fakeElement();
const gardenStatus = fakeElement();
const gardenDifficulty = fakeElement();
const gardenMessage = fakeElement();
const gardenSubmitForm = fakeElement();
const gardenSubmitTitle = fakeElement();
const gardenSubmitStatement = fakeElement();
const gardenSubmitSource = fakeElement();
const gardenSubmitDomain = fakeElement();
const gardenSubmitSourceLiterature = fakeElement();
const gardenSubmitProgress = fakeElement();
const gardenSubmitStatementRender = fakeElement({{ gardenSubmitRender: "statement" }});
const gardenSubmitSourceLiteratureRender = fakeElement({{ gardenSubmitRender: "source-literature" }});
const gardenSubmitProgressRender = fakeElement({{ gardenSubmitRender: "progress" }});
const elementMap = new Map([
  ["#garden-problems", gardenProblems],
  ["#garden-detail", gardenDetail],
  ["#garden-graph", gardenGraph],
  ["#garden-search-form", gardenSearchForm],
  ["#garden-query", gardenQuery],
  ["#garden-domain-filter", gardenDomain],
  ["#garden-status-filter", gardenStatus],
  ["#garden-difficulty-filter", gardenDifficulty],
  ["#garden-message", gardenMessage],
  ["#garden-submit-form", gardenSubmitForm],
  ["#garden-submit-title", gardenSubmitTitle],
  ["#garden-submit-statement", gardenSubmitStatement],
  ["#garden-submit-source", gardenSubmitSource],
  ["#garden-submit-domain", gardenSubmitDomain],
  ["#garden-submit-source-literature", gardenSubmitSourceLiterature],
  ["#garden-submit-progress", gardenSubmitProgress],
]);
const document = {{
  documentElement: {{ lang: "en", dataset: {{}}, classList: fakeClassList() }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return views;
    if (selector === "[data-view-target]") return buttons;
    if (selector === "[data-garden-submit-text]") return [
      Object.assign(gardenSubmitStatement, {{ dataset: {{ gardenSubmitText: "statement" }} }}),
      Object.assign(gardenSubmitSourceLiterature, {{ dataset: {{ gardenSubmitText: "source-literature" }} }}),
      Object.assign(gardenSubmitProgress, {{ dataset: {{ gardenSubmitText: "progress" }} }}),
    ];
    if (selector === "[data-garden-submit-render]") return [gardenSubmitStatementRender, gardenSubmitSourceLiteratureRender, gardenSubmitProgressRender];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "#problem-garden" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage: {{ getItem() {{ return null; }}, setItem() {{}}, removeItem() {{}} }},
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetchCalls = [];
const apiProblem = {{
  id: "api-pfr",
  title: "API Polynomial Freiman-Ruzsa",
  status: "open",
  difficulty: "frontier",
  domains: ["finite fields"],
  source: "API source",
  source_url: "https://example.test/source",
  statement: "API statement with $A+A$.",
  source_literature: ["API source literature"],
  progress: ["API progress"],
  graph_links: [{{ from: "Problem", relation: "stated_in", to: "API source" }}],
}};
const fetch = async (url, options = {{}}) => {{
  fetchCalls.push([String(url), options || {{}}]);
  if (String(url).startsWith("/api/problem-garden/problems?")) {{
    const value = String(url);
    if (!value.includes("q=freiman")) throw new Error(value);
    if (!value.includes("domain=Graph+Theory")) throw new Error(value);
    if (!value.includes("status=open")) throw new Error(value);
    if (!value.includes("difficulty=frontier")) throw new Error(value);
    if (!value.includes("limit=20")) throw new Error(value);
    return {{ ok: true, json: async () => ({{ problems: [apiProblem] }}) }};
  }}
  if (url === "/api/problem-garden/problems") {{
    return {{ ok: true, json: async () => ({{ problems: [apiProblem] }}) }};
  }}
  if (url === "/api/problem-garden/problems/api-pfr") {{
    return {{ ok: true, json: async () => ({{ problem: apiProblem }}) }};
  }}
  if (url === "/api/problem-garden/submissions") {{
    const body = JSON.parse(options.body);
    if (body.title !== "Submitted problem") throw new Error(options.body);
    if (body.status !== "pending_review") throw new Error(options.body);
    if (body.source_literature[0] !== "Source literature") throw new Error(options.body);
    if (body.progress[0] !== "Progress note") throw new Error(options.body);
    return {{ ok: true, json: async () => ({{ submission_id: "submission-1", status: "pending_review" }}) }};
  }}
  if (url === "/api/runs") return {{ ok: true, json: async () => ({{ runs: [] }}) }};
  return {{ ok: true, json: async () => ({{ runs: [] }}) }};
}};
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  URLSearchParams,
  Set,
  Map,
  Math,
  String,
  Number,
  JSON,
}};

(async () => {{
  vm.runInNewContext(code, context);
  gardenQuery.value = "freiman";
  gardenDomain.value = "Graph Theory";
  gardenStatus.value = "open";
  gardenDifficulty.value = "frontier";
  await context.loadProblemGarden();
  if (!gardenProblems.innerHTML.includes("API Polynomial Freiman-Ruzsa")) throw new Error(gardenProblems.innerHTML);
  if (!gardenDetail.innerHTML.includes("API source literature")) throw new Error(gardenDetail.innerHTML);
  if (!gardenGraph.innerHTML.includes("stated_in")) throw new Error(gardenGraph.innerHTML);
  const searchCalls = fetchCalls.filter(([url]) => url.startsWith("/api/problem-garden/problems?"));
  if (searchCalls.length !== 1) throw new Error(`expected one filtered search, got ${{searchCalls.length}}`);

  gardenSubmitTitle.value = "Submitted problem";
  gardenSubmitStatement.value = "Statement";
  gardenSubmitSource.value = "https://example.test/submitted";
  gardenSubmitDomain.value = "finite fields";
  gardenSubmitSourceLiterature.value = "Source literature";
  gardenSubmitProgress.value = "Progress note";
  await context.submitGardenCandidate({{ preventDefault() {{}} }});
  if (!gardenMessage.textContent.includes("pending_review")) throw new Error(gardenMessage.textContent);
  if (gardenSubmitForm.resetCalled !== true) throw new Error("submission form should reset after accepted candidate");
  if (gardenSubmitStatement.hidden !== true) throw new Error("submitted statement editor should return to render mode");
}})().catch((error) => {{
  console.error(error.stack || error.message);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_renders_markdown_headings() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const html = context.renderMarkdownLite("# Title\\n\\n## Section\\n### Adjacent\\nBody without a blank line.\\n\\n#### Detail\\n\\n##中文标题");
if (!html.includes("<h1>Title</h1>")) throw new Error(html);
if (!html.includes("<h2>Section</h2>")) throw new Error(html);
if (!html.includes("<h3>Adjacent</h3>")) throw new Error(html);
if (!html.includes("<p>Body without a blank line.</p>")) throw new Error(html);
if (!html.includes("<h4>Detail</h4>")) throw new Error(html);
if (!html.includes("<h2>中文标题</h2>")) throw new Error(html);
if (html.includes("<p>##")) throw new Error(`heading rendered as paragraph: ${{html}}`);
if (html.includes("<p>###")) throw new Error(`heading rendered as paragraph: ${{html}}`);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_uses_full_markdown_renderer_for_documents() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  marked: {{
    parse(source, options) {{
      if (!options.gfm) throw new Error("GFM should be enabled");
      let html = source;
      html = html.replace(/^> (.+)$/gm, "<blockquote><p>$1</p></blockquote>");
      html = html.replace(/^```(\\w*)\\n([\\s\\S]+?)\\n```$/gm, "<pre><code class=\\"language-$1\\">$2</code></pre>");
      html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
      html = html.replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>");
      html = html.replace(/~~([^~]+)~~/g, "<s>$1</s>");
      html = html.replace(/^\\| A \\| B \\|\\n\\|---\\|---\\|\\n\\| ([^|]+) \\| ([^|]+) \\|$/m, "<table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td>$1</td><td>$2</td></tr></tbody></table>");
      html = html.replace(/^- \\[x\\] done$/m, "<ul><li><input type=\\"checkbox\\" checked disabled> done</li></ul>");
      html = html.replace(/@@GALOIS_MATH_DISPLAY_(\\d+)@@/g, "<p>@@GALOIS_MATH_DISPLAY_$1@@</p>");
      html = html.replace(/<script>alert\\(1\\)<\\/script>/g, "<script>alert(1)</script>");
      return html;
    }},
  }},
  DOMPurify: {{
    sanitize(html) {{
      return html.replace(/<script>[\\s\\S]*?<\\/script>/g, "");
    }},
  }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const markdown = [
  "> quoted result",
  "",
  "A table:",
  "",
  "| A | B |",
  "|---|---|",
  "| **x** | `code $HOME` |",
  "",
  "- [x] done",
  "",
  "~~discarded~~ and $a+b$",
  "",
  "$$",
  "a^2+b^2=c^2",
  "$$",
  "",
  "```bash",
  "echo $HOME",
  "```",
  "",
  "<script>alert(1)</script>",
].join("\\n");
const html = context.renderMarkdownLite(markdown);
if (!html.includes("<blockquote><p>quoted result</p></blockquote>")) throw new Error(html);
if (!html.includes("<table>")) throw new Error(html);
if (!html.includes("<strong>x</strong>")) throw new Error(html);
if (!html.includes("<code>code $HOME</code>")) throw new Error(html);
if (!html.includes("checked")) throw new Error(html);
if (!html.includes("<s>discarded</s>")) throw new Error(html);
if (!html.includes('<span class="math-source inline">a+b</span>')) throw new Error(html);
if (!html.includes('<div class="math-source display">a^2+b^2=c^2</div>')) throw new Error(html);
if (html.includes("<p><div")) throw new Error(html);
if (html.includes('math-source inline">HOME')) throw new Error(html);
if (html.includes("<script>")) throw new Error(html);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_does_not_extract_math_from_code_spans_or_fences() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const html = context.renderMarkdownLite("Inline `echo $HOME` and $x+y$.\\n\\n```tex\\n$x$ should stay literal\\n```");
if (!html.includes("<code>echo $HOME</code>") && !html.includes("`echo $HOME`")) throw new Error(html);
if (!html.includes('<span class="math-source inline">x+y</span>')) throw new Error(html);
if (html.includes('math-source inline">HOME')) throw new Error(html);
if (html.includes('math-source inline">x</span> should stay literal')) throw new Error(html);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_keeps_final_blueprint_problem_and_solution_together() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }} }},
    addEventListener() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const document = {{
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
const docs = context.resolveSnapshotDocuments({{
  problem_input: {{ content: "old problem input" }},
  output: {{
    kind: "final_blueprint",
    content: "# Demo\\n\\n## Problem\\n\\nShow $x=x$.\\n\\n## Solution\\n\\nUse reflexivity.",
  }},
}});
if (docs.problemContent !== "old problem input") throw new Error("problem input should stay unchanged");
if (!docs.proofContent.includes("# Demo")) throw new Error("title should stay with proof display");
if (!docs.proofContent.includes("## Problem")) throw new Error("problem section missing");
if (!docs.proofContent.includes("## Solution")) throw new Error("solution section missing");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_only_shows_proof_sheet_after_output_exists() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }}, add() {{}}, remove() {{}} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const elementMap = new Map();
const proofSheet = fakeElement();
const output = fakeElement();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
context.renderSnapshot({{
  run_id: "queued",
  status: "queued",
  pipeline: "reasoning-verification",
  problem: {{ title: "Queued" }},
  events: [],
  output: null,
  workflows: [],
}});
if (proofSheet.hidden !== true) throw new Error("proof sheet should stay hidden without output");
if (output.innerHTML !== "") throw new Error(`output should stay empty: ${{output.innerHTML}}`);

context.renderSnapshot({{
  run_id: "done",
  status: "succeeded",
  pipeline: "reasoning-verification",
  problem: {{ title: "Done" }},
  events: [],
  output: {{ kind: "summary", content: "## Solution\\n\\nDone." }},
  workflows: [],
}});
if (proofSheet.hidden !== false) throw new Error("proof sheet should show when output exists");
if (!output.innerHTML.includes("<h2>Solution</h2>")) throw new Error(output.innerHTML);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_copies_raw_proof_markdown() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }}, add() {{}}, remove() {{}} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
    select() {{}},
    remove() {{}},
  }};
}}

const elementMap = new Map();
const proofSheet = fakeElement();
const output = fakeElement();
const copyButton = fakeElement();
const document = {{
  body: {{ appendChild() {{}} }},
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (selector === "#copy-proof-markdown") return copyButton;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
let copied = "";
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  navigator: {{ clipboard: {{ writeText(value) {{ copied = value; return Promise.resolve(); }} }} }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setTimeout(callback) {{ callback(); return 1; }},
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
(async () => {{
  context.renderSnapshot({{
    run_id: "done",
    status: "succeeded",
    pipeline: "reasoning-verification",
    problem: {{ title: "Done" }},
    events: [],
    output: {{ kind: "summary", content: "## Solution\\n\\nUse $x=x$." }},
    workflows: [],
  }});
  await context.copyProofMarkdown();
  if (copied !== "## Solution\\n\\nUse $x=x$.") throw new Error(`unexpected copied markdown: ${{copied}}`);
  if (copied.includes("<h2>")) throw new Error("copied rendered HTML instead of raw Markdown");
  if (copyButton.disabled !== false) throw new Error("copy button should be enabled after proof content exists");
}})().catch((error) => {{
  console.error(error);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_routes_use_ing_hashes() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }} }},
    addEventListener() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const views = [
  fakeElement({{ view: "problem-solving" }}),
  fakeElement({{ view: "dashboard" }}),
  fakeElement({{ view: "math-learning" }}),
  fakeElement({{ view: "theorem-searching" }}),
  fakeElement({{ view: "paper-writing" }}),
];
const buttons = [
  fakeElement({{ viewTarget: "problem-solving" }}),
  fakeElement({{ viewTarget: "theorem-searching" }}),
];
const elementMap = new Map();
const window = {{
  location: {{ hash: "#problem-solution" }},
  history: {{
    replaceState(_state, _title, hash) {{
      window.location.hash = hash;
    }},
  }},
  addEventListener() {{}},
}};
const document = {{
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return views;
    if (selector === "[data-view-target]") return buttons;
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
if (context.getViewFromHash() !== "problem-solving") throw new Error("old problem route should normalize");
context.setView("theorem-searching");
if (window.location.hash !== "#theorem-searching") throw new Error(`unexpected hash: ${{window.location.hash}}`);
context.setView("theorem-search");
if (window.location.hash !== "#theorem-searching") throw new Error("old theorem route should write ing hash");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_theorem_searching_stays_embedded_in_galois_shell() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name]; }},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
  element.classList = fakeClassList();
  return element;
}}

const views = [
  fakeElement({{ view: "problem-solving" }}),
  fakeElement({{ view: "dashboard" }}),
  fakeElement({{ view: "math-learning" }}),
  fakeElement({{ view: "theorem-searching" }}),
  fakeElement({{ view: "paper-writing" }}),
];
const buttons = [
  fakeElement({{ viewTarget: "problem-solving" }}),
  fakeElement({{ viewTarget: "theorem-searching" }}),
];
const root = {{ lang: "en", dataset: {{}}, classList: fakeClassList() }};
const elementMap = new Map();
const document = {{
  documentElement: root,
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return views;
    if (selector === "[data-view-target]") return buttons;
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "#theorem-searching" }},
  history: {{
    replaceState(_state, _title, hash) {{
      window.location.hash = hash;
    }},
  }},
  addEventListener() {{}},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
context.setView("theorem-searching");
if (root.classList.contains("matlas-route")) throw new Error("theorem search should stay embedded in the Galois shell");
if (views[3].hidden !== false) throw new Error("theorem search view should be visible");
context.setView("problem-solving");
if (root.classList.contains("matlas-route")) throw new Error("Galois shell state should not be toggled by theorem search");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_matlas_styles_follow_galois_theme_instead_of_fullscreen_white() -> None:
    css = Path("src/galois/platform/web_assets/styles.css").read_text(encoding="utf-8")

    assert ".matlas-route .side-rail" not in css
    assert ".matlas-route .top-bar" not in css
    assert "background: #ffffff;" not in css[css.index(".matlas-view") : css.index(".ledger")]
    assert "background: var(--sheet" in css[css.index(".matlas-view") : css.index(".ledger")]
    assert "background: var(--sheet-cool" in css[css.index(".matlas-view") : css.index(".ledger")]


def test_paper_writing_rendered_surfaces_fill_vertical_workspace() -> None:
    css = Path("src/galois/platform/web_assets/styles.css").read_text(encoding="utf-8")
    paper_css = css[css.index(".paper-writing-view") :]

    assert "grid-template-rows: auto minmax(18rem, 1fr) minmax(18rem, 1fr);" in paper_css
    assert ".paper-input.active:not([hidden])" in paper_css
    assert ".paper-input-render,\n.paper-output" in paper_css
    assert "max-width: none;" in paper_css
    assert "margin: 0;" in paper_css


def test_problem_garden_submit_uses_rendered_compact_markdown_fields() -> None:
    css = Path("src/galois/platform/web_assets/styles.css").read_text(encoding="utf-8")
    garden_css = css[css.index(".problem-garden-view") : css.index(".paper-writing-view")]

    assert "html {\n  background: var(--sheet);\n}" in css
    assert "align-items: stretch;" in garden_css
    assert "background: var(--sheet);" in garden_css
    assert ".garden-detail-actions {\n  display: flex;\n  justify-content: center;" in garden_css
    assert ".garden-graph-modal" in garden_css
    assert ".garden-graph-placeholder" in garden_css
    assert "min-height: calc(100vh - 8.2rem);" not in garden_css
    assert ".garden-render-surface" in garden_css
    assert "max-height: 14rem;" in garden_css
    assert "max-height: 10rem;" in garden_css
    assert "min-height: 7.5rem;" not in garden_css
    assert ".garden-edit-form" not in garden_css
    assert ".garden-submit-form label" in garden_css
    label_css = garden_css[garden_css.index(".garden-submit-form label") : garden_css.index(".garden-empty")]
    assert "text-transform: uppercase;" not in label_css


def test_frontend_uses_chinese_dark_mode_without_display_toggles() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList(owner) {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    getAttribute(name) {{ return this.attributes[name]; }},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
  element.classList = fakeClassList(element);
  return element;
}}

const translatable = [
  fakeElement({{ i18n: "nav.problemSolving" }}),
  fakeElement({{ i18n: "auth.signIn" }}),
  fakeElement({{ i18n: "placeholder.soonTitle" }}),
];
const elementMap = new Map();
const document = {{
  documentElement: {{
    lang: "en",
    dataset: {{}},
  }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    if (selector === "[data-i18n]") return translatable;
    if (selector === "[data-language-toggle]") return [];
    if (selector === "[data-theme-toggle]") return [];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const storage = {{}};
const localStorage = {{
  getItem(key) {{ return storage[key] || null; }},
  setItem(key, value) {{ storage[key] = String(value); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  localStorage,
  matchMedia() {{ return {{ matches: false }}; }},
}};
const fetch = async () => ({{ ok: true, json: async () => ({{ runs: [] }}) }});
const context = {{
  console,
  document,
  window,
  localStorage,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
if (document.documentElement.lang !== "zh-CN") throw new Error(`unexpected lang: ${{document.documentElement.lang}}`);
if (translatable[0].textContent !== "问题求解") throw new Error(`unexpected zh nav: ${{translatable[0].textContent}}`);
if (translatable[1].textContent !== "登录") throw new Error(`unexpected zh auth: ${{translatable[1].textContent}}`);
if (document.documentElement.dataset.theme !== "dark") throw new Error("dark theme was not applied");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_new_proof_clears_completed_run_state() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    attributes: {{}},
    addEventListener() {{}},
    setAttribute(name, value) {{ this.attributes[name] = String(value); }},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{ this.focused = true; }},
  }};
  element.classList = fakeClassList();
  return element;
}}

const title = fakeElement();
const markdown = fakeElement();
const preview = fakeElement();
const proofSheet = fakeElement();
const output = fakeElement();
const copyButton = fakeElement();
const submit = fakeElement();
const submitProxy = fakeElement();
const message = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#problem-title") return title;
    if (selector === "#problem-markdown") return markdown;
    if (selector === "#problem-preview") return preview;
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (selector === "#copy-proof-markdown") return copyButton;
    if (selector === "#submit-button") return submit;
    if (selector === "#submit-proxy") return submitProxy;
    if (selector === "#form-message") return message;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const storage = {{ "galois-current-run-id": "done-run" }};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState(_state, _title, hash) {{ window.location.hash = hash; }} }},
  addEventListener() {{}},
  localStorage: {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(storage, key) ? storage[key] : null; }},
    setItem(key, value) {{ storage[key] = String(value); }},
    removeItem(key) {{ delete storage[key]; }},
  }},
}};
let clearedIntervals = 0;
const fetch = async () => new Promise(() => {{}});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 42; }},
  clearInterval() {{ clearedIntervals += 1; }},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
context.startPolling("done-run");
title.value = "Old title";
markdown.value = "# Old problem";
preview.innerHTML = "<h1>Old problem</h1>";
proofSheet.hidden = false;
output.innerHTML = "<h2>Solution</h2>";
copyButton.disabled = false;
submit.disabled = true;
submitProxy.disabled = true;
message.textContent = "Queued: done-run";
context.startNewProof();

if (title.value !== "") throw new Error("title should be cleared");
if (markdown.value !== "") throw new Error("problem markdown should be cleared");
if (!preview.innerHTML.includes("预览会随输入更新。")) throw new Error(preview.innerHTML);
if (proofSheet.hidden !== true) throw new Error("proof sheet should be hidden");
if (output.innerHTML !== "") throw new Error("output should be cleared");
if (copyButton.disabled !== true) throw new Error("copy button should be disabled");
if (submit.disabled !== false || submitProxy.disabled !== false) throw new Error("submit controls should be enabled");
if (message.textContent !== "") throw new Error(`message should be blank: ${{message.textContent}}`);
if (storage["galois-current-run-id"] !== undefined) throw new Error("stored run id should be removed");
if (clearedIntervals !== 1) throw new Error(`poll interval should be cleared once, got ${{clearedIntervals}}`);
if (!title.focused) throw new Error("title input should be focused");
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_does_not_restore_completed_run_from_local_storage() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
  element.classList = fakeClassList();
  return element;
}}

const proofSheet = fakeElement();
const output = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const storage = {{}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  localStorage: {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(storage, key) ? storage[key] : null; }},
    setItem(key, value) {{ storage[key] = String(value); }},
    removeItem(key) {{ delete storage[key]; }},
  }},
}};
let intervalCount = 0;
const fetch = async (url) => {{
  if (url === "/api/runs") return new Promise(() => {{}});
  if (url === "/api/runs/done-run") {{
    return {{
      ok: true,
      json: async () => ({{
        run_id: "done-run",
        status: "succeeded",
        pipeline: "reasoning-verification",
        problem: {{ title: "Finished" }},
        events: [],
        workflows: ["reasoning", "verification"],
        output: {{ kind: "summary", content: "## Solution\\n\\nDone." }},
      }}),
    }};
  }}
  throw new Error(`unexpected fetch: ${{url}}`);
}};
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ intervalCount += 1; return intervalCount; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
storage["galois-current-run-id"] = "done-run";
proofSheet.hidden = true;
output.innerHTML = "";

(async () => {{
  await context.restoreCurrentRun();
  if (intervalCount !== 0) throw new Error(`completed run should not start polling, got ${{intervalCount}} intervals`);
  if (storage["galois-current-run-id"] !== undefined) throw new Error("completed stored run id should be removed");
  if (proofSheet.hidden !== true) throw new Error("completed proof sheet should not be restored as active state");
  if (output.innerHTML !== "") throw new Error(`old output should not be rendered: ${{output.innerHTML}}`);
}})().catch((error) => {{
  console.error(error);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_does_not_restore_run_list_without_saved_current_run() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeClassList() {{
  const values = new Set();
  return {{
    values,
    toggle(name, force) {{
      const enabled = force === undefined ? !values.has(name) : Boolean(force);
      if (enabled) values.add(name);
      else values.delete(name);
    }},
    contains(name) {{ return values.has(name); }},
    add(name) {{ values.add(name); }},
    remove(name) {{ values.delete(name); }},
  }};
}}

function fakeElement(dataset = {{}}) {{
  const element = {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
  element.classList = fakeClassList();
  return element;
}}

const proofSheet = fakeElement();
const output = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const storage = {{}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
  localStorage: {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(storage, key) ? storage[key] : null; }},
    setItem(key, value) {{ storage[key] = String(value); }},
    removeItem(key) {{ delete storage[key]; }},
  }},
}};
let intervalCount = 0;
const fetch = async () => new Promise(() => {{}});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ intervalCount += 1; return intervalCount; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
context.state = undefined;
proofSheet.hidden = true;
output.innerHTML = "";
const restorable = context.latestRestorableRun([
  {{ run_id: "old-queued", status: "queued", pipeline: "reasoning-verification" }},
  {{ run_id: "old-created", status: "created", pipeline: "reasoning-only" }},
]);
if (restorable !== null) throw new Error(`queued/created historical runs should not restore: ${{JSON.stringify(restorable)}}`);
if (intervalCount !== 0) throw new Error("latestRestorableRun should not poll by itself");

(async () => {{
  await context.restoreCurrentRun();
  if (intervalCount !== 0) throw new Error(`run list should not restore without saved id, got ${{intervalCount}} intervals`);
  if (proofSheet.hidden !== true) throw new Error("proof sheet should stay hidden");
  if (output.innerHTML !== "") throw new Error(`output should stay blank: ${{output.innerHTML}}`);
}})().catch((error) => {{
  console.error(error);
  process.exit(1);
}});
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_frontend_translates_succeeded_status() -> None:
    node = shutil.which("node")
    if node is None:
        return

    app_js = Path("src/galois/platform/web_assets/app.js").read_text(encoding="utf-8")
    harness = f"""
const vm = require("vm");
const code = {json.dumps(app_js)};

function fakeElement(dataset = {{}}) {{
  return {{
    dataset,
    hidden: false,
    disabled: false,
    value: "",
    textContent: "",
    innerHTML: "",
    className: "",
    classList: {{ toggle() {{}}, contains() {{ return false; }}, add() {{}}, remove() {{}} }},
    addEventListener() {{}},
    setAttribute() {{}},
    closest() {{ return {{ querySelectorAll() {{ return []; }} }}; }},
    querySelectorAll() {{ return []; }},
    requestSubmit() {{}},
    scrollIntoView() {{}},
    focus() {{}},
  }};
}}

const paperStatusPill = fakeElement();
const elementMap = new Map([["#paper-status-pill", paperStatusPill]]);
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    return [];
  }},
  createElement() {{ return fakeElement(); }},
}};
const window = {{
  location: {{ hash: "" }},
  history: {{ replaceState() {{}} }},
  addEventListener() {{}},
}};
const fetch = async () => new Promise(() => {{}});
const context = {{
  console,
  document,
  window,
  fetch,
  setInterval() {{ return 1; }},
  clearInterval() {{}},
  Intl,
  Date,
  Error,
  encodeURIComponent,
  Set,
  Map,
  Math,
  String,
  Number,
}};

vm.runInNewContext(code, context);
context.renderWritingSnapshot({{
  run_id: "done-run",
  status: "succeeded",
  pipeline: "reasoning-verification",
  output: {{ artifacts: {{ manuscript_draft: {{ content: "Done." }} }} }},
}});
if (paperStatusPill.textContent === "status.succeeded") throw new Error("raw status key leaked into UI");
if (paperStatusPill.textContent !== "已验证") throw new Error(`unexpected succeeded label: ${{paperStatusPill.textContent}}`);
"""
    result = subprocess.run([node, "-e", harness], check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


def test_create_run_rejects_blank_problem_markdown(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={"title": "Blank", "problem_markdown": "   ", "pipeline": "reasoning-verification"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "problem_markdown must not be blank"


def test_create_run_rejects_blank_title(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={"title": "   ", "problem_markdown": "Show that $1=1$.", "pipeline": "reasoning-verification"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "title must not be blank"


def test_latest_blueprint_prefers_highest_revision(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T100000Z_demo"
    reasoning_dir = run_dir / "reasoning"
    reasoning_dir.mkdir(parents=True)
    (reasoning_dir / "blueprint_r1.md").write_text("first", encoding="utf-8")
    (reasoning_dir / "blueprint_r3.md").write_text("third", encoding="utf-8")
    (reasoning_dir / "blueprint_r2.md").write_text("second", encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": "demo", "title": "Demo"},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["output"]["kind"] == "reasoning_blueprint"
    assert snapshot["output"]["content"] == "third"
    assert snapshot["output"]["path"].endswith("reasoning/blueprint_r3.md")


def test_final_workspace_blueprint_takes_precedence(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T101000Z_final"
    reasoning_dir = run_dir / "reasoning"
    final_dir = reasoning_dir / "workspace" / "results" / "demo"
    final_dir.mkdir(parents=True)
    (reasoning_dir / "blueprint_r1.md").write_text("intermediate blueprint", encoding="utf-8")
    (final_dir / "blueprint.md").write_text("# Demo\n\n## Problem\n\nShow it.\n\n## Solution\n\nDone.", encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": "demo", "title": "Demo"},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["output"]["kind"] == "final_blueprint"
    assert snapshot["output"]["content"].startswith("# Demo")
    assert snapshot["output"]["path"].endswith("reasoning/workspace/results/demo/blueprint.md")


def test_run_snapshot_includes_original_problem_statement(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T101500Z_problem"
    problem_dir = run_dir / "problem"
    problem_dir.mkdir(parents=True)
    (problem_dir / "statement.md").write_text("Show that\n\n$$\na^2+b^2=c^2\n$$\n", encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "problem": {"problem_id": "demo", "title": "Demo"},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["problem_input"]["kind"] == "statement"
    assert "$$\na^2+b^2=c^2\n$$" in snapshot["problem_input"]["content"]


def test_create_run_writes_problem_and_starts_background_launch(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    run_root = tmp_path / "runs"
    _write_config(config_path, run_root)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.openai.example/v1")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    launches: list[dict[str, object]] = []

    def fake_start_launch(**kwargs: object) -> None:
        launches.append(kwargs)

    monkeypatch.setattr(web, "_start_run_thread", fake_start_launch)

    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={
            "title": "Euler identity",
            "problem_markdown": "Prove $e^{i\\pi}+1=0$.",
            "pipeline": "reasoning-only",
            "model": "gpt-5.4",
        },
    )

    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "queued"
    assert payload["model"] == "gpt-5.4"
    assert payload["display_title"] == "Euler identity"
    assert not payload["run_id"].startswith("web_")
    problem_path = Path(payload["problem_path"])
    assert problem_path.exists()
    assert problem_path.name == "statement.md"
    assert problem_path.parent.name == "problem"
    run_dir = problem_path.parent.parent
    assert run_dir == run_root / payload["run_id"]
    assert (run_dir / "manifest.json").exists()
    assert (problem_path.parent / "source_statement.md").read_text(encoding="utf-8") == "Prove $e^{i\\pi}+1=0$.\n"
    assert not (run_root.parent / "web_inputs").exists()
    assert not (run_root.parent / "web_runs").exists()
    assert problem_path.read_text(encoding="utf-8") == "Prove $e^{i\\pi}+1=0$.\n"
    assert len(launches) == 1
    launch = launches[0]
    assert launch["run_id"] == payload["run_id"]
    assert launch["run_dir"] == run_dir
    assert launch["problem"].problem_id == payload["problem_id"]
    assert launch["problem"].problem_path == str(problem_path)
    assert launch["manifest"].run_id == payload["run_id"]
    assert launch["manifest"].model == "gpt-5.4"
    assert launch["manifest"].pipeline.value == "reasoning-only"

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["model"] == "gpt-5.4"
    assert manifest["problem"]["problem_path"] == "problem/statement.md"
    assert manifest["pipeline"] == "reasoning-only"

    snapshot = client.get(f"/api/runs/{payload['run_id']}").json()
    assert snapshot["problem_input"]["content"] == "Prove $e^{i\\pi}+1=0$.\n"

    runs = client.get("/api/runs").json()["runs"]
    indexed = next(run for run in runs if run["run_id"] == payload["run_id"])
    assert indexed["display_title"] == "Euler identity"
    assert indexed["problem"]["display_title"] == "Euler identity"


def test_create_run_rejects_unsupported_model(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    monkeypatch.setattr(web, "_start_run_thread", lambda **_kwargs: None)

    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={
            "title": "Bad model",
            "problem_markdown": "Show that $1=1$.",
            "pipeline": "reasoning-only",
            "model": "unknown-model",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "unsupported model"


def test_create_run_rejects_unconfigured_model_credentials(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")
    monkeypatch.delenv("GEMINI_BASE_URL", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(web, "_start_run_thread", lambda **_kwargs: None)

    client = TestClient(web.create_app(config_path=config_path))
    response = client.post(
        "/api/runs",
        json={
            "title": "Gemini",
            "problem_markdown": "Show that $1=1$.",
            "pipeline": "reasoning-only",
            "model": "gemini-pro-3.1",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "model credentials are not configured"


def test_run_snapshot_reads_events_subagents_and_summary_fallback(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260425T110000Z_summary"
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "failed",
                "pipeline": "reasoning-only",
                "problem": {"problem_id": "summary", "title": "Summary"},
                "workflows": ["reasoning"],
                "features": {"repair_loop_enabled": False},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "events.jsonl").write_text(
        json.dumps({"event_type": "run_created", "workflow": None}) + "\n"
        + json.dumps({"event_type": "run_finished", "workflow": None})
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "subagents.json").write_text(json.dumps([{"task_id": "t1", "status": "failed"}]), encoding="utf-8")
    (run_dir / "summary.md").write_text("# Run Summary\n\nFailed cleanly.", encoding="utf-8")

    snapshot = read_run_snapshot(run_root, run_dir.name)

    assert snapshot["status"] == "failed"
    assert snapshot["features"] == {"repair_loop_enabled": False}
    assert [event["event_type"] for event in snapshot["events"]] == ["run_created", "run_finished"]
    assert snapshot["subagents"] == [{"task_id": "t1", "status": "failed"}]
    assert snapshot["output"] == {
        "kind": "summary",
        "path": str(run_dir / "summary.md"),
        "content": "# Run Summary\n\nFailed cleanly.",
    }


def test_list_runs_includes_recent_real_runs(monkeypatch, tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    def fake_start_launch(**kwargs: object) -> None:
        return None

    monkeypatch.setattr(web, "_start_run_thread", fake_start_launch)
    client = TestClient(web.create_app(config_path=config_path))
    created = client.post(
        "/api/runs",
        json={
            "title": "Recent",
            "problem_markdown": "Show that $1+1=2$.",
            "pipeline": "reasoning-verification",
            "model": "gpt-5.4",
        },
    ).json()

    response = client.get("/api/runs")

    assert response.status_code == 200
    runs = response.json()["runs"]
    assert any(
        run["run_id"] == created["run_id"]
        and run["status"] == "created"
        and run["model"] == "gpt-5.4"
        and run["display_title"] == "Recent"
        for run in runs
    )


def test_list_runs_uses_readable_index_titles_and_ignores_legacy_web_run_directories(tmp_path: Path) -> None:
    from galois.platform import web

    config_path = tmp_path / "config.toml"
    project_root = tmp_path / "projects" / "default"
    run_root = project_root / "runs"
    _write_config(config_path, run_root)

    legacy_id = "web_20260426T224445_problem_8c1d96"
    legacy_dir = project_root / "web_runs" / legacy_id
    legacy_dir.mkdir(parents=True)
    (legacy_dir / "status.json").write_text(
        json.dumps(
            {
                "run_id": legacy_id,
                "status": "launched",
                "pipeline": "reasoning-verification",
                "model": "gpt-5.5",
            }
        ),
        encoding="utf-8",
    )
    real_dir = run_root / "20260426T144446Z_testtitle"
    real_dir.mkdir(parents=True)
    problem_dir = real_dir / "problem"
    problem_dir.mkdir()
    (problem_dir / "statement.md").write_text("# Friendly theorem\n\nShow it.", encoding="utf-8")
    (real_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": real_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "model": "gpt-5.5",
                "problem": {"problem_id": "problem", "title": ""},
                "workflows": ["reasoning", "verification"],
            }
        ),
        encoding="utf-8",
    )

    client = TestClient(web.create_app(config_path=config_path))
    response = client.get("/api/runs")

    assert response.status_code == 200
    runs = response.json()["runs"]
    assert [run["run_id"] for run in runs] == [real_dir.name]
    assert runs[0]["status"] == "succeeded"
    assert runs[0]["display_title"] == "Friendly theorem"
    assert runs[0]["problem"]["title"] == "Friendly theorem"


def test_run_index_keeps_database_display_title_when_resyncing(tmp_path: Path) -> None:
    from galois.platform.run_index import RunIndexStore, manifest_run_record

    database_url = "postgresql://galois:galois_dev@127.0.0.1:5432/galois"
    import psycopg

    try:
        with psycopg.connect(database_url, connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
    except psycopg.OperationalError:
        return

    run_root = tmp_path / "runs"
    run_dir = run_root / "20260428T010203Z_manual"
    problem_dir = run_dir / "problem"
    problem_dir.mkdir(parents=True)
    (problem_dir / "statement.md").write_text("# Auto title\n\nShow $x=x$.", encoding="utf-8")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "model": "gpt-5.4",
                "problem": {"problem_id": "problem", "title": ""},
            }
        ),
        encoding="utf-8",
    )

    with RunIndexStore(database_url) as store:
        store.initialize()
        with store.connection.cursor() as cursor:
            cursor.execute("DELETE FROM run_index WHERE run_id = %s", (run_dir.name,))
        store.connection.commit()
        record = manifest_run_record(run_dir)
        assert record is not None
        store.upsert_run(record)
        with store.connection.cursor() as cursor:
            cursor.execute("UPDATE run_index SET display_title = %s WHERE run_id = %s", ("Manual $x=x$ title", run_dir.name))
        store.connection.commit()
        store.upsert_run(record)
        indexed = store.list_runs(run_root=run_root, limit=1)[0]
        assert indexed["display_title"] == "Manual $x=x$ title"
        assert indexed["auto_display_title"] == "Auto title"
        with store.connection.cursor() as cursor:
            cursor.execute("DELETE FROM run_index WHERE run_id = %s", (run_dir.name,))
        store.connection.commit()


def test_cli_parser_accepts_web_command() -> None:
    from galois.platform.cli import build_parser

    args = build_parser().parse_args(["web", "--host", "0.0.0.0", "--port", "8123", "--config", "config.toml"])

    assert args.command == "web"
    assert args.host == "0.0.0.0"
    assert args.port == 8123
    assert str(args.config) == "config.toml"


def test_run_snapshot_rejects_path_traversal(tmp_path: Path) -> None:
    from galois.platform.web import read_run_snapshot

    run_root = tmp_path / "runs"
    run_root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "manifest.json").write_text(json.dumps({"run_id": "outside", "status": "succeeded"}), encoding="utf-8")

    try:
        read_run_snapshot(run_root, "../outside")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("expected traversal run id to be rejected")
