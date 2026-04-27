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
model = "gpt-5.4"
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

[platform]
resume_enabled = true
max_repair_rounds = 1
benchmark_root = "benchmarks"
project_root = "{run_root.parent}"
run_root = "{run_root.name}"
""".lstrip(),
        encoding="utf-8",
    )


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
    assert '/assets/styles.css?v=matlas-4' in response.text
    assert '/assets/app.js?v=matlas-4' in response.text


def test_index_contains_current_product_views(tmp_path: Path) -> None:
    from galois.platform.web import create_app

    config_path = tmp_path / "config.toml"
    _write_config(config_path, tmp_path / "runs")

    client = TestClient(create_app(config_path=config_path))
    response = client.get("/")

    assert response.status_code == 200
    assert 'data-view="problem-solving"' in response.text
    assert 'data-view="dashboard"' in response.text
    assert 'data-view="math-learning"' in response.text
    assert 'data-view="theorem-searching"' in response.text
    assert 'data-view="paper-writing"' in response.text
    assert 'id="ledger-runs"' in response.text
    assert 'id="problem-preview"' in response.text
    assert 'id="proof-sheet" class="output-sheet" aria-labelledby="output-title" hidden' in response.text
    assert 'id="event-list"' not in response.text
    assert "Event Trail" not in response.text
    assert "事件轨迹" not in response.text
    assert "Time Limit" not in response.text
    assert "Heuristic Model" not in response.text
    assert "Auto-Import Context" not in response.text
    assert 'id="model-select"' in response.text
    assert ">Model Selection<" in response.text
    assert '<option value="gpt-5.4" selected>GPT-5.4</option>' in response.text
    assert '<option value="gpt-5.5">GPT-5.5</option>' in response.text
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
    assert ">Preview<" in response.text
    assert "Riemann Hypothesis" in response.text
    assert "Draft Obligation" not in response.text
    assert "Problem Markdown" not in response.text
    assert "Live Preview" not in response.text
    assert "Example:" not in response.text
    assert "Lemma 4.2: Topological Equivalence" not in response.text
    assert "引理 4.2：拓扑等价" not in response.text
    assert 'class="main-grid app-view active" data-view="problem-solving"' in response.text
    assert 'data-view-target="problem-solving"' in response.text
    assert 'data-view-target="theorem-searching"' in response.text
    assert 'data-view="problem-solution"' not in response.text
    assert 'data-view="theorem-search"' not in response.text
    assert ">Problem Solving<" in response.text
    assert ">Math Learning<" in response.text
    assert ">Theorem Searching<" in response.text
    assert ">Paper Writing<" in response.text
    assert ">Dashboard<" in response.text
    assert "History" in response.text
    assert 'class="login-placeholder"' in response.text
    assert "Sign In" in response.text
    assert 'data-view-target="dashboard">History' not in response.text
    assert 'class="verify-link" data-new-proof' not in response.text
    assert 'data-language-toggle="en"' in response.text
    assert 'data-language-toggle="zh"' in response.text
    assert 'data-theme-toggle="light"' in response.text
    assert 'data-theme-toggle="dark"' in response.text
    assert "待实现" in response.text
    assert "Problem Configuration" in response.text
    assert ">Repository<" not in response.text
    assert ">Proofs<" not in response.text
    assert ">Drafts<" not in response.text


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
    assert "黎曼猜想" in response.text
    assert "示例：黎曼猜想" not in response.text
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
    assert "snapshot.output?.kind" in response.text
    assert "snapshot.problem_input?.content" in response.text
    assert "problemSource" not in response.text


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


def test_frontend_problem_editor_updates_markdown_preview() -> None:
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
    classList: {{ toggle() {{}}, contains(name) {{ return false; }}, remove() {{}}, add() {{}} }},
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
const markdown = fakeElement();
const preview = fakeElement();
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


def test_frontend_splits_final_blueprint_into_problem_and_solution() -> None:
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
if (!docs.problemContent.includes("# Demo")) throw new Error("title should stay with problem display");
if (!docs.problemContent.includes("## Problem")) throw new Error("problem section missing");
if (docs.problemContent.includes("## Solution")) throw new Error("solution leaked into problem display");
if (!docs.proofContent.startsWith("## Solution")) throw new Error("solution section should start proof display");
if (docs.proofContent.includes("old problem input")) throw new Error("fallback problem input leaked into final blueprint");
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


def test_frontend_applies_language_and_theme_modes() -> None:
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
const langButtons = [fakeElement({{ languageToggle: "en" }}), fakeElement({{ languageToggle: "zh" }})];
const themeButtons = [fakeElement({{ themeToggle: "light" }}), fakeElement({{ themeToggle: "dark" }})];
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
    if (selector === "[data-language-toggle]") return langButtons;
    if (selector === "[data-theme-toggle]") return themeButtons;
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
context.applyLocale("zh");
if (document.documentElement.lang !== "zh-CN") throw new Error(`unexpected lang: ${{document.documentElement.lang}}`);
if (translatable[0].textContent !== "问题求解") throw new Error(`unexpected zh nav: ${{translatable[0].textContent}}`);
if (translatable[1].textContent !== "登录") throw new Error(`unexpected zh auth: ${{translatable[1].textContent}}`);
if (!langButtons[1].classList.contains("active")) throw new Error("zh language button should be active");
if (langButtons[1].attributes["aria-pressed"] !== "true") throw new Error("zh language aria state missing");
if (storage["galois-language"] !== "zh") throw new Error("language preference was not saved");

context.applyTheme("dark");
if (document.documentElement.dataset.theme !== "dark") throw new Error("dark theme was not applied");
if (!themeButtons[1].classList.contains("active")) throw new Error("dark theme button should be active");
if (themeButtons[1].attributes["aria-pressed"] !== "true") throw new Error("dark theme aria state missing");
if (storage["galois-theme"] !== "dark") throw new Error("theme preference was not saved");
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
const currentTitle = fakeElement();
const statusPill = fakeElement();
const runId = fakeElement();
const runPipeline = fakeElement();
const submit = fakeElement();
const submitProxy = fakeElement();
const message = fakeElement();
const ladder = [fakeElement(), fakeElement(), fakeElement(), fakeElement(), fakeElement()];
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
    if (selector === "#current-run-title") return currentTitle;
    if (selector === "#status-pill") return statusPill;
    if (selector === "#run-id") return runId;
    if (selector === "#run-pipeline") return runPipeline;
    if (selector === "#submit-button") return submit;
    if (selector === "#submit-proxy") return submitProxy;
    if (selector === "#form-message") return message;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    if (selector === "#progress-ladder li") return ladder;
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
currentTitle.textContent = "Finished run";
statusPill.textContent = "status.succeeded";
statusPill.className = "status-pill succeeded";
runId.textContent = "done-run";
runPipeline.textContent = "reasoning-verification";
submit.disabled = true;
submitProxy.disabled = true;
message.textContent = "Queued: done-run";
ladder.forEach((item) => {{
  item.classList.add("done");
  item.classList.add("current");
}});
context.startNewProof();

if (title.value !== "") throw new Error("title should be cleared");
if (markdown.value !== "") throw new Error("problem markdown should be cleared");
if (!preview.innerHTML.includes("Preview updates as you write.")) throw new Error(preview.innerHTML);
if (proofSheet.hidden !== true) throw new Error("proof sheet should be hidden");
if (output.innerHTML !== "") throw new Error("output should be cleared");
if (copyButton.disabled !== true) throw new Error("copy button should be disabled");
if (currentTitle.textContent !== "No active run") throw new Error(`unexpected title: ${{currentTitle.textContent}}`);
if (statusPill.textContent !== "Idle") throw new Error(`unexpected status: ${{statusPill.textContent}}`);
if (statusPill.className !== "status-pill idle") throw new Error(`unexpected status class: ${{statusPill.className}}`);
if (runId.textContent !== "—") throw new Error(`unexpected run id: ${{runId.textContent}}`);
if (runPipeline.textContent !== "—") throw new Error(`unexpected pipeline: ${{runPipeline.textContent}}`);
if (submit.disabled !== false || submitProxy.disabled !== false) throw new Error("submit controls should be enabled");
if (message.textContent !== "") throw new Error(`message should be blank: ${{message.textContent}}`);
if (storage["galois-current-run-id"] !== undefined) throw new Error("stored run id should be removed");
if (clearedIntervals !== 1) throw new Error(`poll interval should be cleared once, got ${{clearedIntervals}}`);
if (ladder.some((item) => item.classList.contains("done") || item.classList.contains("current"))) {{
  throw new Error("progress ladder should be reset");
}}
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

const currentTitle = fakeElement();
const statusPill = fakeElement();
const proofSheet = fakeElement();
const output = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#current-run-title") return currentTitle;
    if (selector === "#status-pill") return statusPill;
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    if (selector === "#progress-ladder li") return [fakeElement(), fakeElement(), fakeElement(), fakeElement(), fakeElement()];
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
currentTitle.textContent = "No active run";
statusPill.textContent = "Idle";
proofSheet.hidden = true;
output.innerHTML = "";

(async () => {{
  await context.restoreCurrentRun();
  if (intervalCount !== 0) throw new Error(`completed run should not start polling, got ${{intervalCount}} intervals`);
  if (storage["galois-current-run-id"] !== undefined) throw new Error("completed stored run id should be removed");
  if (currentTitle.textContent !== "No active run") throw new Error(`completed run should not be rendered: ${{currentTitle.textContent}}`);
  if (statusPill.textContent !== "Idle") throw new Error(`status should remain idle: ${{statusPill.textContent}}`);
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

const currentTitle = fakeElement();
const statusPill = fakeElement();
const proofSheet = fakeElement();
const output = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#current-run-title") return currentTitle;
    if (selector === "#status-pill") return statusPill;
    if (selector === "#proof-sheet") return proofSheet;
    if (selector === "#output") return output;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    if (selector === "#progress-ladder li") return [fakeElement(), fakeElement(), fakeElement(), fakeElement(), fakeElement()];
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
currentTitle.textContent = "No active run";
statusPill.textContent = "Idle";
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
  if (currentTitle.textContent !== "No active run") throw new Error(`unexpected restored title: ${{currentTitle.textContent}}`);
  if (statusPill.textContent !== "Idle") throw new Error(`unexpected status: ${{statusPill.textContent}}`);
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

const statusPill = fakeElement();
const elementMap = new Map();
const document = {{
  documentElement: {{ lang: "en", dataset: {{}} }},
  querySelector(selector) {{
    if (selector === "#status-pill") return statusPill;
    if (!elementMap.has(selector)) elementMap.set(selector, fakeElement());
    return elementMap.get(selector);
  }},
  querySelectorAll(selector) {{
    if (selector === "[data-view]") return [fakeElement({{ view: "problem-solving" }})];
    if (selector === "[data-view-target]") return [fakeElement({{ viewTarget: "problem-solving" }})];
    if (selector === "#progress-ladder li") return [fakeElement(), fakeElement(), fakeElement(), fakeElement(), fakeElement()];
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
context.renderSnapshot({{
  run_id: "done-run",
  status: "succeeded",
  pipeline: "reasoning-verification",
  problem: {{ title: "Done" }},
  events: [],
  workflows: ["reasoning", "verification"],
  output: null,
}});
if (statusPill.textContent === "status.succeeded") throw new Error("raw status key leaked into UI");
if (statusPill.textContent !== "Verified") throw new Error(`unexpected succeeded label: ${{statusPill.textContent}}`);
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
        json={"title": "Recent", "problem_markdown": "Show that $1+1=2$.", "pipeline": "reasoning-verification"},
    ).json()

    response = client.get("/api/runs")

    assert response.status_code == 200
    runs = response.json()["runs"]
    assert any(
        run["run_id"] == created["run_id"] and run["status"] == "created" and run["model"] == "gpt-5.4"
        for run in runs
    )


def test_list_runs_ignores_legacy_web_run_directories(tmp_path: Path) -> None:
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
    real_dir = run_root / "20260426T144445Z_22997820"
    real_dir.mkdir(parents=True)
    (real_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": real_dir.name,
                "status": "succeeded",
                "pipeline": "reasoning-verification",
                "model": "gpt-5.5",
                "problem": {"problem_id": "finished-proof", "title": "Finished proof"},
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
