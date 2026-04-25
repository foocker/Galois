const state = {
  currentRunId: null,
  pollHandle: null,
};

const elements = {
  form: document.querySelector('#run-form'),
  title: document.querySelector('#problem-title'),
  markdown: document.querySelector('#problem-markdown'),
  pipeline: document.querySelector('#pipeline'),
  submit: document.querySelector('#submit-button'),
  example: document.querySelector('#example-button'),
  message: document.querySelector('#form-message'),
  recent: document.querySelector('#recent-runs'),
  refresh: document.querySelector('#refresh-runs'),
  currentTitle: document.querySelector('#current-run-title'),
  statusPill: document.querySelector('#status-pill'),
  runId: document.querySelector('#run-id'),
  runPipeline: document.querySelector('#run-pipeline'),
  artifactPath: document.querySelector('#artifact-path'),
  output: document.querySelector('#output'),
  events: document.querySelector('#event-list'),
  ladder: [...document.querySelectorAll('#progress-ladder li')],
};

const exampleProblem = `# Compactness problem

Let $X$ be a compact topological space and let $f:X \to \mathbb{R}$ be continuous.

Prove that $f$ is bounded and attains its maximum and minimum on $X$.

Please give a proof-oriented explanation and identify the key theorem used.`;

function setMessage(text, tone = 'neutral') {
  elements.message.textContent = text;
  elements.message.dataset.tone = tone;
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderMarkdownLite(markdown) {
  const escaped = escapeHtml(markdown || '');
  const blocks = escaped.split(/\n{2,}/).map((block) => {
    if (block.startsWith('```')) {
      return `<pre>${block.replace(/^```\w*\n?/, '').replace(/```$/, '')}</pre>`;
    }
    if (block.startsWith('# ')) return `<h3>${block.slice(2)}</h3>`;
    if (block.startsWith('## ')) return `<h4>${block.slice(3)}</h4>`;
    if (block.startsWith('- ')) {
      const items = block.split('\n').map((line) => `<li>${line.replace(/^-\s*/, '')}</li>`).join('');
      return `<ul>${items}</ul>`;
    }
    return `<p>${block.replaceAll('\n', '<br />')}</p>`;
  });
  return blocks.join('');
}

function deriveSteps(snapshot) {
  const status = snapshot.status || 'queued';
  const workflows = new Set(snapshot.workflows || []);
  const events = snapshot.events || [];
  const eventNames = new Set(events.map((event) => event.event_type));
  const steps = new Set(['queued']);

  if (status === 'running' || status === 'launched' || status === 'succeeded' || status === 'failed') steps.add('reasoning');
  if (workflows.has('verification') || eventNames.has('artifact_collected')) steps.add('verification');
  if (eventNames.has('repair_input_written') || eventNames.has('repair_contract_published')) steps.add('repair');
  if (status === 'succeeded' || status === 'failed') steps.add('complete');

  return steps;
}

function renderLadder(snapshot) {
  const steps = deriveSteps(snapshot);
  const order = ['queued', 'reasoning', 'verification', 'repair', 'complete'];
  const activeIndex = Math.max(...[...steps].map((step) => order.indexOf(step)));
  elements.ladder.forEach((item, index) => {
    item.classList.toggle('done', index < activeIndex || snapshot.status === 'succeeded');
    item.classList.toggle('current', index === activeIndex && !['succeeded', 'failed'].includes(snapshot.status));
  });
}

function renderSnapshot(snapshot) {
  const status = snapshot.status || 'unknown';
  elements.currentTitle.textContent = snapshot.problem?.title || snapshot.problem?.problem_id || 'Research run';
  elements.statusPill.textContent = status;
  elements.statusPill.className = `status-pill ${status}`;
  elements.runId.textContent = snapshot.web_run_id || snapshot.run_id || '—';
  elements.runPipeline.textContent = snapshot.pipeline || snapshot.launch?.pipeline || '—';
  elements.artifactPath.textContent = snapshot.output?.path || snapshot.launch?.stdout_path || '—';

  if (snapshot.output?.content) {
    elements.output.innerHTML = renderMarkdownLite(snapshot.output.content);
  } else if (status === 'failed') {
    elements.output.innerHTML = `<p class="empty-state">The run failed before a blueprint was collected. Check the event trail and launch logs.</p>`;
  } else {
    elements.output.innerHTML = `<p class="empty-state">Galois is preparing the research artifact. This panel updates when a blueprint or summary is available.</p>`;
  }

  const events = snapshot.events || [];
  if (events.length === 0) {
    elements.events.innerHTML = '<li class="muted">No control-plane events yet.</li>';
  } else {
    elements.events.innerHTML = events.slice(-12).reverse().map((event) => {
      const workflow = event.workflow ? ` · ${event.workflow}` : '';
      return `<li><strong>${escapeHtml(event.event_type || 'event')}</strong>${escapeHtml(workflow)}<br /><small>${escapeHtml(event.timestamp || '')}</small></li>`;
    }).join('');
  }

  renderLadder(snapshot);
}

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || `Request failed: ${response.status}`);
  return payload;
}

async function pollRun(runId) {
  const snapshot = await fetchJson(`/api/runs/${encodeURIComponent(runId)}`);
  renderSnapshot(snapshot);
  if (['succeeded', 'failed'].includes(snapshot.status)) {
    clearInterval(state.pollHandle);
    state.pollHandle = null;
    elements.submit.disabled = false;
    await loadRecentRuns();
  }
}

function startPolling(runId) {
  state.currentRunId = runId;
  if (state.pollHandle) clearInterval(state.pollHandle);
  pollRun(runId).catch((error) => setMessage(error.message, 'error'));
  state.pollHandle = setInterval(() => {
    pollRun(runId).catch((error) => setMessage(error.message, 'error'));
  }, 2500);
}

async function loadRecentRuns() {
  const payload = await fetchJson('/api/runs');
  if (!payload.runs?.length) {
    elements.recent.innerHTML = '<p class="muted">No previous runs found.</p>';
    return;
  }
  elements.recent.innerHTML = payload.runs.map((run) => {
    const title = run.problem?.title || run.problem?.problem_id || run.run_id;
    return `<div class="run-item"><button type="button" data-run-id="${escapeHtml(run.run_id)}"><strong>${escapeHtml(title)}</strong><small>${escapeHtml(run.status || 'unknown')} · ${escapeHtml(run.pipeline || 'pipeline')}</small></button></div>`;
  }).join('');
}

async function submitRun(event) {
  event.preventDefault();
  const problemMarkdown = elements.markdown.value;
  if (!problemMarkdown.trim()) {
    setMessage('Paste a Markdown problem before starting a run.', 'error');
    return;
  }

  elements.submit.disabled = true;
  setMessage('Submitting problem to Galois…');
  try {
    const created = await fetchJson('/api/runs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: elements.title.value.trim() || null,
        problem_markdown: problemMarkdown,
        pipeline: elements.pipeline.value,
      }),
    });
    setMessage(`Run queued: ${created.run_id}`);
    renderSnapshot({
      run_id: created.run_id,
      status: 'queued',
      pipeline: created.pipeline,
      problem: { title: elements.title.value.trim(), problem_id: created.problem_id },
      events: [],
      output: null,
      workflows: [],
    });
    startPolling(created.run_id);
    await loadRecentRuns();
  } catch (error) {
    elements.submit.disabled = false;
    setMessage(error.message, 'error');
  }
}

function wireEvents() {
  elements.form.addEventListener('submit', submitRun);
  elements.example.addEventListener('click', () => {
    elements.title.value = 'Compactness and extrema';
    elements.markdown.value = exampleProblem;
    setMessage('Example problem loaded. Edit it or start a run.');
  });
  elements.refresh.addEventListener('click', () => loadRecentRuns().catch((error) => setMessage(error.message, 'error')));
  elements.recent.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-run-id]');
    if (!button) return;
    startPolling(button.dataset.runId);
  });
}

wireEvents();
loadRecentRuns().catch((error) => setMessage(error.message, 'error'));
