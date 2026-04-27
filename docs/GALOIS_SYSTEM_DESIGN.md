# Galois 系统设计

状态：Current  
默认模型：`codex / gpt-5.4 / xhigh`  
环境管理：`uv`

## 1. 目标

Galois 当前是一个围绕数学问题求解的单仓控制面，聚焦两条能力链路：

- `reasoning`：生成自然语言证明草图与修复版本
- `verification`：对证明草图做自然语言严格校验，并返回 verdict 与 repair hints

它的目标不是保留历史阶段的所有能力分支，而是把当前仍在使用的上游资产收束到一个可运行、可审计、可 benchmark 的系统里。

## 2. 非目标

当前阶段不做这些事：

- 不保留已删除能力的兼容控制面
- 不把 `references/` 继续当作主实现层
- 不优先做复杂 TUI 或多层 agent 树
- 不追求在第一阶段统一所有 prompt 细节

## 3. 设计原则

### 3.1 单仓工作，分层实现

所有长期保留的控制逻辑都进入 `src/galois/`。  
上游项目只保留为资产来源或参考快照。

### 3.2 控制逻辑用 Python

以下逻辑由 Python control plane 负责：

- 配置加载
- 路径解析
- run manifest
- workflow launch planning
- service 生命周期
- artifact 归档
- benchmark suite 规划

### 3.3 数学资产与控制面分离

`three_horse/reasoning/` 和 `three_horse/verification/` 保留 prompt、skill、MCP、schema、脚本等运行资产；  
`src/galois/` 负责长期保留的工程外壳与运行控制。

### 3.4 benchmark first

核心控制面必须服务于后续 benchmark。  
如果某个流程难以规划、记录、比较，它就不应进入主控制面。

## 4. 当前仓库布局

```text
Galois/
  .codex/
  benchmarks/
  configs/
  docs/
  projects/
  references/
  src/galois/
  tests/
  three_horse/
```

### 4.1 主代码区

`src/galois/` 当前核心模块：

- `platform/config.py`
- `platform/paths.py`
- `platform/contracts.py`
- `platform/run_registry.py`
- `platform/workflows.py`
- `platform/launcher.py`
- `platform/cli.py`
- `platform/web.py`
- `platform/web_assets/`
- `platform/benchmark.py`
- `platform/artifacts.py`
- `reasoning/runner.py`
- `verification/service.py`

### 4.2 资产区

运行资产保留在：

- `three_horse/reasoning/`
- `three_horse/verification/`

资产目录用于保存上游继承而来的 prompt、skill、MCP、脚本和样例，不作为主实现目录。

### 4.3 参考区

`references/` 是只读对照层。  
需要继续保留的逻辑，应迁入 `src/galois/` 或 `three_horse/`，而不是继续在 `references/` 上开发。

## 5. 系统分层

### 5.1 `platform`

职责：

- 加载全局配置
- 解析 repo 路径
- 生成 run manifest
- 构造 workflow launch plan
- 管理 service workflow 与 oneshot workflow
- 记录 run event
- 收集 reasoning / verification artifacts
- 提供 benchmark suite 入口
- 提供 Web workbench API 与静态前端入口

不负责：

- 直接生成数学证明内容
- 直接判定证明正确性

### 5.2 `reasoning`

职责：

- 从问题陈述生成自然语言证明草图
- 在需要时基于 repair input 继续修复
- 管理 run-local `results/`、`memory/`、`downloads/`

不负责：

- 直接提供系统级调度
- 直接做 proof verification

### 5.3 `verification`

职责：

- 接收 statement 与 blueprint
- 以自然语言 proof verifier 进行严格检查
- 产出 verdict、summary、gaps、repair hints
- 为 platform 提供结构化响应

不负责：

- 直接改写 reasoning 输出
- 直接调度其他 workflow

## 6. 核心工件

当前主链路围绕这些稳定工件运作：

### 6.1 `problem`

输入问题及其元信息。

建议字段：

- `problem_id`
- `title`
- `statement`
- `source_path`
- `tags`

### 6.2 `blueprint`

reasoning 的核心输出。

建议字段：

- `problem_id`
- `revision`
- `content`
- `notes`

### 6.3 `verification_report`

verification 的核心输出。

建议字段：

- `problem_id`
- `revision`
- `verdict`
- `summary`
- `critical_errors`
- `gaps`
- `repair_hints`

### 6.4 `run_manifest`

platform 的主控制记录。

建议字段：

- `run_id`
- `problem`
- `backend`
- `model`
- `model_reasoning_effort`
- `status`
- `pipeline`
- `features`
- `workflows`

### 6.5 `run_event`

所有关键步骤的统一日志事件。

建议字段：

- `timestamp`
- `run_id`
- `workflow`
- `event_type`
- `payload`

## 7. 运行目录

建议结构：

```text
projects/default/runs/<run_id>/
  manifest.json
  events.jsonl
  subagents.json
  problem/
    statement.md
    source_statement.md
    meta.json
  reasoning/
    blueprint_r1.md
    blueprint_r1.json
    repair_input_r1.json
    logs/
    workspace/
  verification/
    verification_request_r1.json
    verification_r1.json
    verification_r1.normalized.json
    verification_decision_r1.json
    logs/
    workspace/
```

规则：

- 每次 run 必须独立目录
- 不覆盖旧 run
- 运行产物写入 `projects/default/`，不写回资产目录

## 8. 默认运行模型

当前固定配置：

- backend：`codex`
- model：`gpt-5.4`
- reasoning effort：`xhigh`
- personality：`pragmatic`

配置来源：

- `configs/defaults.toml`

## 9. 环境与依赖管理

主仓库只使用 `uv`：

```bash
uv sync
uv sync --dev
```

原则：

- 根 `pyproject.toml` 是唯一依赖真源
- `three_horse/` 下的 requirements 文件仅作上游参考
- 不在主仓库维护多个长期独立虚拟环境

## 10. Web workbench

Web workbench 是当前本地研究入口：

- 用户通过 `uv run galois web` 启动。
- 前端提交 Markdown/LaTeX 数学问题。
- FastAPI 后端写入 `projects/default/web_inputs/`。
- 后端以子进程复用现有 `launch` 控制链路，而不是引入新的持久队列或数据库。
- Web wrapper 状态写入 `projects/default/web_runs/`，真实 run 仍写入 `projects/default/runs/`。
- 查询接口会把 `web_*` wrapper id 映射回真实 run id，并展示 manifest、events、subagents、summary、blueprint 等 artifacts。

用户文档直接暴露 `uv run galois ...`，不再维护额外 shell wrapper。

## 11. workflow 设计

### 10.1 支持的 pipeline

当前只支持两种顶层 pipeline：

- `reasoning-only`
- `reasoning-verification`

`reasoning-only` 用于只生成自然语言证明草图。  
`reasoning-verification` 用于生成草图后，由 platform 托管 verification service 做结构化校验。

### 10.2 repair loop

外层 repair loop 是运行策略，不是独立 pipeline。

默认流程：

1. 读取 `problem`
2. reasoning 生成 `blueprint_r1`
3. verification 检查 `blueprint_r1`
4. 若 verdict 为 `repair_needed`，platform 写 `repair_input_r1.json`
5. reasoning 基于 repair input 继续
6. 直到 accepted、失败或达到 repair round 上限

### 10.3 当前 CLI 能力

已落地命令：

- `config`
- `plan`
- `launch`
- `inspect`
- `web`
- `suite list`
- `suite plan`
- `suite init-examples`

当前 `plan` 只做 planning，不做 execution。
`launch` 负责创建 run、写事件、启动 workflow、管理 verification service、归档结果。`web` 提供本地研究工作台。

## 12. benchmark 设计

### 12.1 当前 benchmark 层级

当前主路径至少区分：

- `reasoning-only`
- `reasoning-verification`

### 12.2 当前 benchmark 入口

已落地：

- `benchmarks/manifests/reasoning_data_examples.toml`
- `uv run galois suite list`
- `uv run galois suite plan --pipeline reasoning-verification`

默认 example suite 复用 `three_horse/reasoning/data`。

### 12.3 benchmark 记录要求

每次实验至少记录：

- problem set
- backend / model / effort
- pipeline
- repair loop 配置
- success / partial / fail
- failure category

## 13. Problem Garden 未来功能

Problem Garden（问题花园）是一个独立功能，不是当前 `Problem Solving` 输入框的装饰区，也不是 run history。它的 Web 入口放在首页顶部导航的中间栏，顺序位于 `Problem Solving` 之后、`Math Learning` 之前。它面向“有研究价值的待解决问题”的发现、收录、追踪和图谱化展示。

### 13.1 功能定位

目标：

- 从互联网、论文、预印本、会议资料、数学社区页面等来源中收录有价值的待解决问题。
- 为每个问题维护结构化状态、来源、相关文献、尝试路径和研究进展。
- 在 Web 中展示问题列表、单问题详情，以及问题与文献、领域、方法之间的链接图结构。
- 当被收录的问题在后续文献中被解决时，标记为已解决，并记录解决论文地址与核心解法线索。

非目标：

- 第一版不自动声称某个开放问题已经被解决。
- 不把未验证的网络文本当作事实；来源、状态和解决情况必须带出处。
- 不替代 benchmark suite。Problem Garden 可为 benchmark 提供候选问题，但它本身是研究问题知识库。

### 13.2 问题结构草案

单个问题至少需要这些字段：

- `title`：问题题目。
- `statement`：较完整的问题表述，支持 Markdown / LaTeX。
- `status`：`open`、`partially_solved`、`solved`、`retracted`、`unclear`。
- `difficulty_level`：粗粒度难度等级，例如 `introductory`、`graduate`、`research`、`frontier`。
- `domains`：问题领域，例如 number theory、algebraic geometry、combinatorics、PDE。
- `source`：原始来源文献、网页、帖子或书籍位置，必须含 URL / DOI / arXiv ID / bibliographic note。
- `source_reliability`：来源可信度与人工审核状态。
- `attempted_literature`：已有尝试文献与失败/部分结果摘要。
- `related_literature`：相关背景论文、survey、工具论文。
- `known_core_ideas`：已知核心思路、等价转化、常用方法。
- `progress_notes`：进展摘要，按时间或来源组织。
- `possible_ideas`：待验证想法，必须标记为 conjectural / speculative。
- `solved_by`：若已解决，记录解决论文、作者、日期、链接与解法摘要。
- `graph_links`：问题到问题、文献、领域、方法、作者或数据源的边。
- `ingestion_metadata`：采集时间、采集器、原始文本片段、去重键、审核人。

### 13.3 链接图结构

Problem Garden 应把问题作为图谱节点，而不是普通表格：

- Problem 节点：开放问题或已解决问题。
- Paper 节点：来源文献、尝试文献、相关文献、解决文献。
- Domain 节点：数学领域或子领域。
- Method 节点：可能的工具、技术路线、核心思路。
- Source 节点：arXiv、Crossref、OpenAlex、网页、社区来源等采集入口。

典型边：

- `stated_in`
- `attempted_by`
- `related_to`
- `uses_method`
- `belongs_to_domain`
- `solved_by`
- `generalizes`
- `special_case_of`
- `inspired_by`

### 13.4 采集与审核链路

未来实现应分成采集、归一化、审核和展示四层：

1. crawler / fetcher：从允许的数据源抓取候选问题与文献元数据。
2. extractor：从文本中抽取问题表述、状态、领域、引用和候选链接。
3. resolver：用 arXiv、Crossref、OpenAlex 等源解析文献身份并去重。
4. reviewer：人工或 agent 审核字段可信度，标记不确定信息。
5. garden store：保存结构化问题、文献节点和图边。
6. Web UI：提供列表、筛选、单问题详情、图谱视图和“送入 Problem Solving”入口。

### 13.5 Web 入口草案

Problem Garden 应作为独立页面进入顶部导航，并在首页模块顺序中位于 `Problem Solving` 与 `Math Learning` 之间。

列表页显示：

- 问题题目
- 简短表述
- 状态
- 难度等级
- 领域
- 来源
- 最近进展
- 相关文献数量

详情页显示：

- 完整问题表述
- 来源与可信度
- 尝试文献、来源文献、相关文献、解决文献
- 已知核心思路、进展、可能想法
- 链接图结构
- 操作：复制为当前问题、启动 reasoning run、加入 benchmark candidate

### 13.6 已落地的 PostgreSQL 数据层

第一版 Problem Garden 已经接入本地 PostgreSQL，不再只依赖前端静态数组。默认连接串由 `configs/defaults.toml` 的 `[database]` 提供：

- `url_env = "DATABASE_URL"`：优先读环境变量。
- `url = "postgresql://galois:galois_dev@127.0.0.1:5432/galois"`：本地开发默认值。

当前表结构：

- `garden_problems`：问题主表。保存 `id`、`title`、`statement`、`status`、`difficulty`、`domains`、`source`、`source_url`、`context`，以及 `source_literature`、`attempted_literature`、`related_literature`、`known_core_ideas`、`progress`、`possible_ideas` 等 JSONB 字段。
- `garden_edges`：链接图边表。保存 `problem_id`、`from_label`、`relation`、`to_label`，用于表示问题到文献、领域、方法、来源的关系。
- `garden_submissions`：候选提交审核队列表。保存用户提交的 `title`、`statement`、`source_url`、`domain`、`context`、`references_text`，默认状态为 `pending_review`。

当前 Web API：

- `GET /api/problem-garden/problems`：列出问题，支持 `q`、`status`、`domain`、`difficulty` 过滤。
- `GET /api/problem-garden/problems/{problem_id}`：读取单个问题详情和 `graph_links`。
- `POST /api/problem-garden/submissions`：提交候选问题进入审核队列，不直接进入公开 Garden。

Web 端已接入：

- 顶部导航独立入口，位置在 `Problem Solving` 与 `Math Learning` 之间。
- 左侧检索与筛选：关键词、状态、领域、难度。
- 中间详情：问题表述、来源文献、尝试文献、相关文献、核心思路、进展、可能想法。
- 右侧链接图和候选问题提交表单。
- 数据库不可用时显示本地 seed 问题作为开发降级，但正式链路以 PostgreSQL 为准。

### 13.7 分阶段 TODO

- P0：继续固化 `ProblemGardenProblem`、`ProblemGardenPaper`、`ProblemGardenEdge` 的 JSON schema 和导入/导出格式。
- P1：手动录入 5-10 个高质量样例问题，先验证字段是否够用。
- P2：完善 Problem Garden 独立 Web 页面：更多筛选、审核队列视图、送入 Problem Solving。
- P3：接入 arXiv / Crossref / OpenAlex 文献解析与去重。
- P4：实现候选问题采集器，但所有 open / solved 状态必须进入审核队列。
- P5：实现图谱视图，展示问题、文献、领域、方法之间的链接结构。
- P6：将可信问题导出为 benchmark candidate suite。

## 14. 实施阶段

### Phase 1：control plane bootstrap

目标：

- 配置加载
- 路径模型
- run manifest
- workflow planning

### Phase 2：workflow launch

目标：

- 启动 reasoning workflow
- 启动 verification service
- 归档 stdout / stderr 与 artifacts

### Phase 3：artifact collection and replay

目标：

- 统一 summary 与 artifact 归档
- 稳定 resume / replay / inspect 能力

### Phase 4：benchmark harness

目标：

- 更稳定的 benchmark problem set 入口
- 结果聚合
- 更清晰的 ablation 支持
- Problem Garden 中通过审核的问题可作为后续 benchmark candidate，但不与 benchmark harness 混为一层。

### Phase 5：Problem Garden

目标：

- 建立问题花园数据模型
- 支持人工录入与审核
- 支持文献身份解析、来源追踪和状态标注
- 支持列表、详情和链接图展示
- 支持将可信问题送入 Problem Solving 或 benchmark candidate

## 15. 当前开发约定

主开发目录：

- `src/galois/`
- `configs/`
- `docs/`
- `tests/`

必要时修改：

- `three_horse/reasoning/`
- `three_horse/verification/`

不要在这些位置继续发展核心逻辑：

- `references/`
- 已删除能力相关的旧目录或旧流程说明
