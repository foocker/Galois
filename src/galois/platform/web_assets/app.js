const state = {
  currentRunId: null,
  pollHandle: null,
  runs: [],
  proofMarkdown: '',
};

const elements = {
  form: document.querySelector('#run-form'),
  title: document.querySelector('#problem-title'),
  markdown: document.querySelector('#problem-markdown'),
  pipeline: document.querySelector('#pipeline'),
  model: document.querySelector('#model-select'),
  pipelineChoices: [...document.querySelectorAll('input[name="pipeline-choice"]')],
  views: [...document.querySelectorAll('[data-view]')],
  viewButtons: [...document.querySelectorAll('[data-view-target]')],
  languageButtons: [...document.querySelectorAll('[data-language-toggle]')],
  themeButtons: [...document.querySelectorAll('[data-theme-toggle]')],
  submit: document.querySelector('#submit-button'),
  submitProxy: document.querySelector('#submit-proxy'),
  newProof: document.querySelector('#new-proof-shortcut'),
  newProofButtons: [...document.querySelectorAll('[data-new-proof]')],
  example: document.querySelector('#example-button'),
  message: document.querySelector('#form-message'),
  recent: document.querySelector('#recent-runs'),
  ledgerRuns: document.querySelector('#ledger-runs'),
  refresh: document.querySelector('#refresh-runs'),
  currentTitle: document.querySelector('#current-run-title'),
  statusPill: document.querySelector('#status-pill'),
  runId: document.querySelector('#run-id'),
  runPipeline: document.querySelector('#run-pipeline'),
  problemPreview: document.querySelector('#problem-preview'),
  proofSheet: document.querySelector('#proof-sheet'),
  copyProofMarkdown: document.querySelector('#copy-proof-markdown'),
  output: document.querySelector('#output'),
  ladder: [...document.querySelectorAll('#progress-ladder li')],
};

const defaultView = 'problem-solving';
const viewAliases = new Map([
  ['problem-solution', 'problem-solving'],
  ['theorem-search', 'theorem-searching'],
]);
const viewNames = new Set(['problem-solving', 'dashboard', 'math-learning', 'theorem-searching', 'paper-writing']);
const languageStorageKey = 'galois-language';
const themeStorageKey = 'galois-theme';
const currentRunStorageKey = 'galois-current-run-id';
const supportedLocales = new Set(['en', 'zh']);
const supportedThemes = new Set(['light', 'dark']);
const rootElement = document.documentElement || { lang: 'en', dataset: {} };

const translations = {
  en: {
    'actions.commenceRun': 'Commence Run',
    'actions.copyFailed': 'Copy failed. Select the proof document and copy manually.',
    'actions.copyProofMarkdown': 'Copy Markdown',
    'actions.copiedProofMarkdown': 'Copied Markdown',
    'actions.loadExample': 'Load example',
    'actions.newProof': 'New Proof',
    'actions.refresh': 'Refresh',
    'actions.startRun': 'Start research run',
    'auth.signIn': 'Sign In',
    'brand.subtitle': 'Mathematics<br />Learning &amp;<br /><span>Research</span>',
    'config.description': 'Choose the model and verification pipeline for the current proof obligation.',
    'config.modelSelection': 'Model Selection',
    'config.pipelineSelection': 'Pipeline Selection',
    'config.title': 'Problem Configuration',
    'empty.noRunsLoaded': 'No runs loaded yet.',
    'empty.noVerifiedRuns': 'No verified runs found.',
    'empty.noVerifiedRunsLoaded': 'No verified runs loaded yet.',
    'empty.previewPending': 'Preview updates as you write.',
    'history.date': 'Date',
    'history.end': 'End of Ledger',
    'history.ledgerKicker': 'Ledger Vol. XIV',
    'history.pipelineStatus': 'Pipeline Status',
    'history.problemTitle': 'Problem Title',
    'history.recentRuns': 'Recent Runs',
    'history.title': 'History',
    'message.exampleLoaded': 'Example problem loaded. Edit it or start a run.',
    'message.problemRequired': 'Paste a Markdown problem before starting a run.',
    'message.submitting': 'Submitting problem to Galois...',
    'nav.dashboard': 'Dashboard',
    'nav.mathLearning': 'Math Learning',
    'nav.paperWriting': 'Paper Writing',
    'nav.problemSolving': 'Problem Solving',
    'nav.theoremSearching': 'Theorem Searching',
    'output.proofDocument': 'Proof Document',
    'pipeline.fastDraft': 'Fast Draft',
    'pipeline.formalCheck': 'Formal Check',
    'pipeline.reasoningOnly': 'Reasoning-Only',
    'pipeline.reasoningOnlyDesc': 'Generates mathematical reasoning without strict downstream verification.',
    'pipeline.reasoningVerification': 'Reasoning & Verification',
    'pipeline.reasoningVerificationDesc': 'Constructs a proof attempt, then runs the verification service.',
    'placeholder.mathLearning': 'Concept explanation, guided study paths, and example-driven learning will live here.',
    'placeholder.paperWriting': 'Drafting, polishing, and mathematical exposition tools will live here.',
    'placeholder.soonTitle': 'Not implemented',
    'placeholder.theoremSearching': 'The theorem and related-paper search workspace will live here.',
    'problem.draftObligation': 'Title',
    'problem.latexSupport': 'Markdown / LaTeX support active',
    'problem.livePreview': 'Preview',
    'problem.markdownLabel': 'Problem',
    'problem.markdownPlaceholder': 'Paste a theorem, exercise, proof attempt, or research question here...',
    'problem.titlePlaceholder': 'Riemann Hypothesis',
    'status.complete': 'Complete',
    'status.empty': 'Empty',
    'status.failed': 'Failed',
    'status.idle': 'Idle',
    'status.on': 'On',
    'status.pipeline': 'Pipeline',
    'status.queued': 'Queued',
    'status.reasoning': 'Reasoning',
    'status.reasoningOnly': 'Reasoning-Only',
    'status.repairLoop': 'Repair Loop',
    'status.runId': 'Run Id',
    'status.running': 'Running',
    'status.succeeded': 'Verified',
    'status.unknown': 'Unknown',
    'status.verification': 'Verification',
    'status.verificationStatus': 'Verification Status',
    'status.verified': 'Verified',
    'status.noActiveRun': 'No active run',
    'theme.day': 'Day',
    'theme.night': 'Night',
  },
  zh: {
    'actions.commenceRun': '开始运行',
    'actions.copyFailed': '复制失败。请选中证明文档后手动复制。',
    'actions.copyProofMarkdown': '复制 Markdown',
    'actions.copiedProofMarkdown': '已复制 Markdown',
    'actions.loadExample': '加载示例',
    'actions.newProof': '新证明',
    'actions.refresh': '刷新',
    'actions.startRun': '开始研究运行',
    'auth.signIn': '登录',
    'brand.subtitle': '数学学习与研究',
    'config.description': '为当前证明任务选择模型和验证流程。',
    'config.modelSelection': '模型选择',
    'config.pipelineSelection': '流程选择',
    'config.title': '问题配置',
    'empty.noRunsLoaded': '尚未加载运行记录。',
    'empty.noVerifiedRuns': '暂无已验证运行。',
    'empty.noVerifiedRunsLoaded': '尚未加载已验证运行。',
    'empty.previewPending': '预览会随输入更新。',
    'history.date': '日期',
    'history.end': '记录结束',
    'history.ledgerKicker': '记录卷 XIV',
    'history.pipelineStatus': '流程状态',
    'history.problemTitle': '问题标题',
    'history.recentRuns': '最近运行',
    'history.title': '历史',
    'message.problemRequired': '请先粘贴 Markdown 问题再启动运行。',
    'message.submitting': '正在提交问题到 Galois...',
    'nav.dashboard': '仪表盘',
    'nav.mathLearning': '数学学习',
    'nav.paperWriting': '论文写作',
    'nav.problemSolving': '问题求解',
    'nav.theoremSearching': '定理搜索',
    'output.proofDocument': '证明文档',
    'pipeline.fastDraft': '快速草稿',
    'pipeline.formalCheck': '形式检查',
    'pipeline.reasoningOnly': '仅推理',
    'pipeline.reasoningOnlyDesc': '生成数学推理，不执行严格的下游验证。',
    'pipeline.reasoningVerification': '推理与验证',
    'pipeline.reasoningVerificationDesc': '先构造证明尝试，再运行验证服务。',
    'placeholder.mathLearning': '概念解释、学习路径和示例驱动学习将在这里实现。',
    'placeholder.paperWriting': '论文起草、润色和数学表达工具将在这里实现。',
    'placeholder.soonTitle': '待实现',
    'placeholder.theoremSearching': '定理与相关论文搜索工作区将在这里实现。',
    'problem.draftObligation': '标题',
    'problem.latexSupport': 'Markdown / LaTeX 支持已启用',
    'problem.livePreview': '预览',
    'problem.markdownLabel': '问题',
    'problem.markdownPlaceholder': '在这里粘贴定理、习题、证明尝试或研究问题...',
    'problem.titlePlaceholder': '黎曼猜想',
    'status.complete': '完成',
    'status.empty': '空',
    'status.failed': '失败',
    'status.idle': '空闲',
    'status.on': '开启',
    'status.pipeline': '流程',
    'status.queued': '排队中',
    'status.reasoning': '推理中',
    'status.reasoningOnly': '仅推理',
    'status.repairLoop': '修复循环',
    'status.runId': '运行 ID',
    'status.running': '运行中',
    'status.succeeded': '已验证',
    'status.unknown': '未知',
    'status.verification': '验证中',
    'status.verificationStatus': '验证状态',
    'status.verified': '已验证',
    'status.noActiveRun': '暂无活动运行',
    'theme.day': '白天',
    'theme.night': '黑夜',
  },
};

let currentLocale = 'en';

const exampleProblem = `# Compactness problem

Let $X$ be a compact topological space and let $f:X \to \mathbb{R}$ be continuous.

Prove that $f$ is bounded and attains its maximum and minimum on $X$.

Please give a proof-oriented explanation and identify the key theorem used.`;

function translate(key) {
  return translations[currentLocale]?.[key] || translations.en[key] || key;
}

function storageGet(key) {
  try {
    return window.localStorage?.getItem(key);
  } catch (_error) {
    return null;
  }
}

function storageSet(key, value) {
  try {
    window.localStorage?.setItem(key, value);
  } catch (_error) {
    // Ignore storage failures in restricted browser contexts.
  }
}

function storageRemove(key) {
  try {
    window.localStorage?.removeItem(key);
  } catch (_error) {
    // Ignore storage failures in restricted browser contexts.
  }
}

function preferredTheme() {
  const saved = storageGet(themeStorageKey);
  if (supportedThemes.has(saved)) return saved;
  if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) return 'dark';
  return 'light';
}

function applyLocale(locale) {
  currentLocale = supportedLocales.has(locale) ? locale : 'en';
  rootElement.lang = currentLocale === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-i18n]').forEach((node) => {
    node.textContent = translate(node.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-html]').forEach((node) => {
    node.innerHTML = translate(node.dataset.i18nHtml);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => {
    node.placeholder = translate(node.dataset.i18nPlaceholder);
  });
  elements.languageButtons.forEach((button) => {
    const active = button.dataset.languageToggle === currentLocale;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  storageSet(languageStorageKey, currentLocale);
}

function applyTheme(theme) {
  const nextTheme = supportedThemes.has(theme) ? theme : 'light';
  rootElement.dataset.theme = nextTheme;
  elements.themeButtons.forEach((button) => {
    const active = button.dataset.themeToggle === nextTheme;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  storageSet(themeStorageKey, nextTheme);
}

function setMessage(text, tone = 'neutral') {
  elements.message.textContent = text;
  elements.message.dataset.tone = tone;
}

function setSubmitDisabled(disabled) {
  elements.submit.disabled = disabled;
  elements.submitProxy.disabled = disabled;
}

function getViewFromHash() {
  const viewName = window.location.hash.replace(/^#/, '');
  const normalizedView = viewAliases.get(viewName) || viewName;
  return viewNames.has(normalizedView) ? normalizedView : null;
}

function setView(viewName, options = {}) {
  const normalizedView = viewAliases.get(viewName) || viewName;
  const nextView = viewNames.has(normalizedView) ? normalizedView : defaultView;
  elements.views.forEach((view) => {
    const active = view.dataset.view === nextView;
    view.hidden = !active;
    view.classList.toggle('active', active);
  });
  elements.viewButtons.forEach((item) => {
    const target = item.dataset.viewTarget;
    item.classList.toggle('active', target === nextView);
  });
  if (options.updateHash !== false && window.location.hash !== `#${nextView}`) {
    window.history.replaceState(null, '', `#${nextView}`);
  }
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function mathPlaceholder(index, display) {
  return `@@GALOIS_MATH_${display ? 'DISPLAY' : 'INLINE'}_${index}@@`;
}

function codePlaceholder(index) {
  return `@@GALOIS_CODE_${index}@@`;
}

function protectMarkdownCode(source) {
  const segments = [];
  let protectedSource = source.replace(/(^|\n)([ \t]*(`{3,}|~{3,})[^\n]*(?:\n[\s\S]*?\n[ \t]*\3[ \t]*)?)(?=\n|$)/g, (match, prefix, code) => {
    const index = segments.push(code) - 1;
    return `${prefix}${codePlaceholder(index)}`;
  });
  protectedSource = protectedSource.replace(/(`+)([\s\S]*?)\1/g, (match) => {
    const index = segments.push(match) - 1;
    return codePlaceholder(index);
  });
  return { source: protectedSource, segments };
}

function restoreCodePlaceholders(source, segments) {
  return source.replace(/@@GALOIS_CODE_(\d+)@@/g, (_match, indexValue) => segments[Number(indexValue)] || '');
}

function extractMathSegments(markdown) {
  const segments = [];
  const protectedCode = protectMarkdownCode(markdown || '');
  let source = protectedCode.source;
  source = source.replace(/\$\$([\s\S]+?)\$\$/g, (_match, math) => {
    const index = segments.push({ display: true, math: math.trim() }) - 1;
    return `\n\n${mathPlaceholder(index, true)}\n\n`;
  });
  source = source.replace(/\$([^$\n]+?)\$/g, (_match, math) => {
    const index = segments.push({ display: false, math: math.trim() }) - 1;
    return mathPlaceholder(index, false);
  });
  source = restoreCodePlaceholders(source, protectedCode.segments);
  return { source, segments };
}

function renderMathPlaceholders(html, segments) {
  const normalizedHtml = html.replace(/<p>\s*(@@GALOIS_MATH_DISPLAY_\d+@@)\s*<\/p>/g, '$1');
  return normalizedHtml.replace(/@@GALOIS_MATH_(DISPLAY|INLINE)_(\d+)@@/g, (_match, mode, indexValue) => {
    const segment = segments[Number(indexValue)];
    if (!segment) return '';
    const math = escapeHtml(segment.math);
    if (mode === 'DISPLAY') return `<div class="math-source display">${math}</div>`;
    return `<span class="math-source inline">${math}</span>`;
  });
}

function renderMarkdownWithLibrary(source) {
  if (!window.marked?.parse || !window.DOMPurify?.sanitize) return null;
  try {
    const rawHtml = window.marked.parse(source, {
      async: false,
      breaks: false,
      gfm: true,
    });
    return window.DOMPurify.sanitize(rawHtml, {
      ADD_ATTR: ['checked', 'target', 'rel'],
    });
  } catch (_error) {
    return null;
  }
}

function renderMarkdownFallback(source) {
  const escaped = escapeHtml(source);
  const output = [];
  let paragraphLines = [];
  let listItems = [];
  let codeLines = [];
  let inCodeBlock = false;

  const flushParagraph = () => {
    if (!paragraphLines.length) return;
    output.push(`<p>${paragraphLines.join('<br />')}</p>`);
    paragraphLines = [];
  };

  const flushList = () => {
    if (!listItems.length) return;
    output.push(`<ul>${listItems.map((item) => `<li>${item}</li>`).join('')}</ul>`);
    listItems = [];
  };

  const flushCode = () => {
    output.push(`<pre>${codeLines.join('\n')}</pre>`);
    codeLines = [];
  };

  escaped.split('\n').forEach((line) => {
    const trimmed = line.trim();

    if (inCodeBlock) {
      if (/^```/.test(trimmed)) {
        flushCode();
        inCodeBlock = false;
        return;
      }
      codeLines.push(line);
      return;
    }

    if (/^```/.test(trimmed)) {
      flushParagraph();
      flushList();
      inCodeBlock = true;
      codeLines = [];
      return;
    }

    if (!trimmed) {
      flushParagraph();
      flushList();
      return;
    }

    if (/^@@GALOIS_MATH_DISPLAY_\d+@@$/.test(trimmed)) {
      flushParagraph();
      flushList();
      output.push(trimmed);
      return;
    }

    const headingMatch = line.match(/^(#{1,6})\s*(.+)$/);
    if (headingMatch) {
      flushParagraph();
      flushList();
      const level = headingMatch[1].length;
      output.push(`<h${level}>${headingMatch[2].trim()}</h${level}>`);
      return;
    }

    const listMatch = line.match(/^-\s+(.+)$/);
    if (listMatch) {
      flushParagraph();
      listItems.push(listMatch[1]);
      return;
    }

    flushList();
    paragraphLines.push(line);
  });

  if (inCodeBlock) flushCode();
  flushParagraph();
  flushList();

  return output.join('');
}

function renderMarkdownDocument(markdown) {
  const { source, segments } = extractMathSegments(markdown || '');
  const html = renderMarkdownWithLibrary(source) ?? renderMarkdownFallback(source);
  return renderMathPlaceholders(html, segments);
}

function renderMarkdownLite(markdown) {
  return renderMarkdownDocument(markdown);
}

function renderMathFallback(container) {
  container.querySelectorAll('.math-source').forEach((node) => {
    const display = node.classList.contains('display');
    const math = document.createElement(display ? 'div' : 'span');
    math.className = `math-fallback ${display ? 'display' : 'inline'}`;
    math.textContent = (node.textContent || '').trim();
    node.replaceWith(math);
  });
}

function renderMath(container) {
  const mathNodes = [...container.querySelectorAll('.math-source')];
  if (!mathNodes.length) return;

  if (window.katex && typeof window.katex.render === 'function') {
    mathNodes.forEach((node) => {
      const display = node.classList.contains('display');
      const math = (node.textContent || '').trim();
      try {
        window.katex.render(math, node, {
          displayMode: display,
          throwOnError: false,
          strict: false,
        });
        node.classList.remove?.('math-source');
        node.classList.add?.('math-rendered');
      } catch (_error) {
        node.textContent = math;
        renderMathFallback({ querySelectorAll: () => [node] });
      }
    });
    return;
  }

  if (typeof window.renderMathInElement !== 'function') {
    renderMathFallback(container);
    return;
  }
  mathNodes.forEach((node) => {
    const display = node.classList.contains('display');
    const math = (node.textContent || '').trim();
    node.textContent = display ? `$$${math}$$` : `$${math}$`;
  });
  window.renderMathInElement(container, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '$', right: '$', display: false },
    ],
    throwOnError: false,
  });
}

function updateProblemPreview() {
  const content = elements.markdown.value;
  if (!content.trim()) {
    elements.problemPreview.innerHTML = `<p class="empty-state">${escapeHtml(translate('empty.previewPending'))}</p>`;
    return;
  }
  elements.problemPreview.innerHTML = renderMarkdownLite(content);
  renderMath(elements.problemPreview);
}

function statusLabel(run) {
  const status = run.status || 'unknown';
  const pipeline = run.pipeline || '';
  if (status === 'succeeded' && pipeline === 'reasoning-verification') return translate('status.verified');
  if (status === 'succeeded') return translate('status.complete');
  if (status === 'failed') return translate('status.failed');
  if (status === 'running' || status === 'launched') return translate('status.running');
  if (status === 'queued') return translate('status.queued');
  if (pipeline === 'reasoning-only') return translate('status.reasoningOnly');
  return status;
}

function translatedStatus(status) {
  const key = `status.${status || 'unknown'}`;
  return translations[currentLocale]?.[key] || translations.en[key] || translate('status.unknown');
}

function snapshotStatusLabel(snapshot) {
  if (snapshot.status === 'succeeded' && (snapshot.pipeline || snapshot.launch?.pipeline) === 'reasoning-verification') {
    return translate('status.verified');
  }
  if (snapshot.status === 'succeeded') return translate('status.complete');
  return translatedStatus(snapshot.status);
}

function statusClass(run) {
  const status = run.status || 'unknown';
  const pipeline = run.pipeline || '';
  if (status === 'succeeded' && (pipeline === 'reasoning-verification' || !pipeline)) return 'verified';
  if (status === 'failed') return 'failed';
  return 'draft';
}

function isActiveRun(run) {
  return ['created', 'queued', 'running', 'launched'].includes(run.status || '');
}

function isVerifiedRun(run) {
  return run.status === 'succeeded' && run.pipeline === 'reasoning-verification';
}

function verifiedRuns(runs) {
  const seen = new Set();
  return runs.filter(isVerifiedRun).filter((run) => {
    const key = run.problem?.problem_id || run.problem?.title || run.run_id;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function formatRunDate(runId) {
  const match = String(runId || '').match(/(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})/);
  if (!match) return 'Current Session';
  const [, year, month, day, hour, minute, second] = match;
  const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second)));
  return new Intl.DateTimeFormat(undefined, { month: 'short', day: '2-digit', year: 'numeric' }).format(date);
}

function splitFinalBlueprint(content) {
  const text = content || '';
  const problemMatch = text.match(/^##\s+Problem\s*$/im);
  const solutionMatch = text.match(/^##\s+Solution\s*$/im);
  if (!problemMatch || !solutionMatch || solutionMatch.index <= problemMatch.index) {
    return { problemContent: text, proofContent: text };
  }

  const titleContent = text.slice(0, problemMatch.index).trim();
  const problemContent = text.slice(problemMatch.index, solutionMatch.index).trim();
  const proofContent = text.slice(solutionMatch.index).trim();
  return {
    problemContent: [titleContent, problemContent].filter(Boolean).join('\n\n'),
    proofContent,
  };
}

function resolveSnapshotDocuments(snapshot) {
  if (snapshot.output?.kind === 'final_blueprint' && snapshot.output?.content) {
    return splitFinalBlueprint(snapshot.output.content);
  }
  return {
    problemContent: snapshot.problem_input?.content || null,
    proofContent: snapshot.output?.content || null,
  };
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
  const documents = resolveSnapshotDocuments(snapshot);
  elements.currentTitle.textContent = snapshot.problem?.title || snapshot.problem?.problem_id || 'Research run';
  elements.statusPill.textContent = snapshotStatusLabel(snapshot);
  elements.statusPill.className = `status-pill ${status}`;
  elements.runId.textContent = snapshot.run_id || '—';
  elements.runPipeline.textContent = snapshot.pipeline || snapshot.launch?.pipeline || '—';

  if (documents.proofContent) {
    state.proofMarkdown = documents.proofContent;
    elements.proofSheet.hidden = false;
    elements.copyProofMarkdown.disabled = false;
    elements.copyProofMarkdown.textContent = translate('actions.copyProofMarkdown');
    elements.output.innerHTML = renderMarkdownLite(documents.proofContent);
    renderMath(elements.output);
  } else {
    state.proofMarkdown = '';
    elements.proofSheet.hidden = true;
    elements.copyProofMarkdown.disabled = true;
    elements.copyProofMarkdown.textContent = translate('actions.copyProofMarkdown');
    elements.output.innerHTML = '';
  }

  renderLadder(snapshot);
}

function clearCurrentRunStorage(runId = null) {
  if (runId && storageGet(currentRunStorageKey) !== runId) return;
  storageRemove(currentRunStorageKey);
}

function resetRunStatus() {
  elements.currentTitle.textContent = translate('status.noActiveRun');
  elements.statusPill.textContent = translate('status.idle');
  elements.statusPill.className = 'status-pill idle';
  elements.runId.textContent = '—';
  elements.runPipeline.textContent = '—';
  elements.ladder.forEach((item) => {
    item.classList.remove('done');
    item.classList.remove('current');
  });
}

function clearProofOutput() {
  state.proofMarkdown = '';
  elements.proofSheet.hidden = true;
  elements.copyProofMarkdown.disabled = true;
  elements.copyProofMarkdown.textContent = translate('actions.copyProofMarkdown');
  elements.output.innerHTML = '';
}

function stopPolling() {
  if (state.pollHandle) {
    clearInterval(state.pollHandle);
    state.pollHandle = null;
  }
}

function startNewProof() {
  stopPolling();
  state.currentRunId = null;
  clearCurrentRunStorage();
  elements.title.value = '';
  elements.markdown.value = '';
  updateProblemPreview();
  clearProofOutput();
  resetRunStatus();
  setSubmitDisabled(false);
  setMessage('');
  setView(defaultView);
  elements.title.focus();
  elements.title.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function copyProofMarkdown() {
  if (!state.proofMarkdown.trim()) return;
  try {
    const clipboard = window.navigator?.clipboard;
    if (clipboard?.writeText) {
      await clipboard.writeText(state.proofMarkdown);
    } else {
      const scratch = document.createElement('textarea');
      scratch.value = state.proofMarkdown;
      scratch.setAttribute('readonly', '');
      scratch.className = 'copy-scratch';
      document.body.appendChild(scratch);
      scratch.select();
      document.execCommand('copy');
      scratch.remove();
    }
    elements.copyProofMarkdown.textContent = translate('actions.copiedProofMarkdown');
    setTimeout(() => {
      elements.copyProofMarkdown.textContent = translate('actions.copyProofMarkdown');
    }, 1600);
  } catch (_error) {
    setMessage(translate('actions.copyFailed'), 'error');
  }
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
    stopPolling();
    if (state.currentRunId === runId) {
      state.currentRunId = null;
      clearCurrentRunStorage(runId);
    }
    setSubmitDisabled(false);
    await loadRecentRuns();
  }
}

function startPolling(runId, viewName = defaultView) {
  state.currentRunId = runId;
  storageSet(currentRunStorageKey, runId);
  setView(viewName);
  if (state.pollHandle) clearInterval(state.pollHandle);
  pollRun(runId).catch((error) => setMessage(error.message, 'error'));
  state.pollHandle = setInterval(() => {
    pollRun(runId).catch((error) => setMessage(error.message, 'error'));
  }, 2500);
}

async function loadRecentRuns() {
  const payload = await fetchJson('/api/runs');
  state.runs = payload.runs || [];
  const verified = verifiedRuns(state.runs);
  renderLedgerRuns(verified);
  if (!verified.length) {
    elements.recent.innerHTML = `<p class="muted">${escapeHtml(translate('empty.noVerifiedRuns'))}</p>`;
    return state.runs;
  }
  elements.recent.innerHTML = verified.map((run) => {
    const title = run.problem?.title || run.problem?.problem_id || run.run_id;
    return `<div class="run-item"><button type="button" data-run-id="${escapeHtml(run.run_id)}"><strong>${escapeHtml(title)}</strong><small>${escapeHtml(translate('status.verified'))}</small></button></div>`;
  }).join('');
  return state.runs;
}

function latestRestorableRun(runs) {
  return runs.find((run) => run.status === 'running' || run.status === 'launched')
    || null;
}

async function restoreCurrentRun() {
  const savedRunId = storageGet(currentRunStorageKey);
  if (savedRunId) {
    try {
      const snapshot = await fetchJson(`/api/runs/${encodeURIComponent(savedRunId)}`);
      if (isActiveRun(snapshot)) {
        startPolling(savedRunId);
      } else {
        clearCurrentRunStorage(savedRunId);
      }
    } catch (error) {
      clearCurrentRunStorage(savedRunId);
      setMessage(error.message, 'error');
    }
    return;
  }
}

function renderLedgerRuns(runs) {
  if (!runs.length) {
    elements.ledgerRuns.innerHTML = `<div class="ledger-row ledger-empty">
      <time>—</time>
      <strong>${escapeHtml(translate('empty.noVerifiedRuns'))}</strong>
      <em class="status-tag draft">${escapeHtml(translate('status.empty'))}</em>
    </div>`;
    return;
  }
  elements.ledgerRuns.innerHTML = runs.slice(0, 8).map((run) => {
    const title = run.problem?.title || run.problem?.problem_id || run.run_id;
    return `<button class="ledger-row ledger-button" type="button" data-run-id="${escapeHtml(run.run_id)}">
      <time>${escapeHtml(formatRunDate(run.run_id))}</time>
      <strong>${escapeHtml(title)}</strong>
      <em class="status-tag ${escapeHtml(statusClass(run))}">${escapeHtml(statusLabel(run))}</em>
    </button>`;
  }).join('');
}

async function submitRun(event) {
  event.preventDefault();
  const problemMarkdown = elements.markdown.value;
  if (!problemMarkdown.trim()) {
    setMessage(translate('message.problemRequired'), 'error');
    return;
  }

  setSubmitDisabled(true);
  setMessage(translate('message.submitting'));
  try {
    const created = await fetchJson('/api/runs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: elements.title.value.trim() || null,
        problem_markdown: problemMarkdown,
        pipeline: elements.pipeline.value,
        model: elements.model.value,
      }),
    });
    setMessage(`${translate('status.queued')}: ${created.run_id}`);
    renderSnapshot({
      run_id: created.run_id,
      status: 'queued',
      pipeline: created.pipeline,
      model: created.model,
      problem: { title: elements.title.value.trim(), problem_id: created.problem_id },
      events: [],
      output: null,
      workflows: [],
    });
    startPolling(created.run_id);
    await loadRecentRuns();
  } catch (error) {
    setSubmitDisabled(false);
    setMessage(error.message, 'error');
  }
}

function wireEvents() {
  elements.viewButtons.forEach((item) => {
    item.addEventListener('click', () => {
      if (!item.dataset.viewTarget) return;
      setView(item.dataset.viewTarget);
    });
  });
  elements.languageButtons.forEach((button) => {
    button.addEventListener('click', () => {
      applyLocale(button.dataset.languageToggle);
      loadRecentRuns().catch((error) => setMessage(error.message, 'error'));
    });
  });
  elements.themeButtons.forEach((button) => {
    button.addEventListener('click', () => applyTheme(button.dataset.themeToggle));
  });
  elements.form.addEventListener('submit', submitRun);
  elements.markdown.addEventListener('input', updateProblemPreview);
  elements.copyProofMarkdown.addEventListener('click', () => {
    copyProofMarkdown().catch(() => setMessage(translate('actions.copyFailed'), 'error'));
  });
  elements.submitProxy.addEventListener('click', () => elements.form.requestSubmit());
  elements.newProof.addEventListener('click', () => {
    startNewProof();
  });
  elements.newProofButtons.forEach((button) => {
    button.addEventListener('click', () => {
      startNewProof();
    });
  });
  elements.example.addEventListener('click', () => {
    elements.title.value = 'Compactness and extrema';
    elements.markdown.value = exampleProblem;
    updateProblemPreview();
    setMessage(translate('message.exampleLoaded'));
  });
  elements.pipelineChoices.forEach((choice) => {
    choice.addEventListener('change', () => {
      elements.pipeline.value = choice.value;
      choice.closest('.pipeline-field').querySelectorAll('.pipeline-option').forEach((option) => {
        option.classList.toggle('selected', option.contains(choice));
      });
    });
  });
  elements.pipeline.addEventListener('change', () => {
    elements.pipelineChoices.forEach((choice) => {
      choice.checked = choice.value === elements.pipeline.value;
      choice.closest('.pipeline-option').classList.toggle('selected', choice.checked);
    });
  });
  elements.refresh.addEventListener('click', () => loadRecentRuns().catch((error) => setMessage(error.message, 'error')));
  elements.recent.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-run-id]');
    if (!button) return;
    startPolling(button.dataset.runId);
  });
  elements.ledgerRuns.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-run-id]');
    if (!button) return;
    startPolling(button.dataset.runId, defaultView);
  });
  window.addEventListener('hashchange', () => setView(getViewFromHash() || defaultView, { updateHash: false }));
}

wireEvents();
applyTheme(preferredTheme());
applyLocale(supportedLocales.has(storageGet(languageStorageKey)) ? storageGet(languageStorageKey) : 'en');
setView(getViewFromHash() || defaultView, { updateHash: false });
updateProblemPreview();
loadRecentRuns()
  .then(() => restoreCurrentRun())
  .catch((error) => setMessage(error.message, 'error'));
