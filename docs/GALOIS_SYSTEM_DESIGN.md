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

- 用户通过 `sh run.sh` 或 `sh run.sh web` 启动。
- 前端提交 Markdown/LaTeX 数学问题。
- FastAPI 后端写入 `projects/default/web_inputs/`。
- 后端以子进程复用现有 `launch-run` 控制链路，而不是引入新的持久队列或数据库。
- Web wrapper 状态写入 `projects/default/web_runs/`，真实 run 仍写入 `projects/default/runs/`。
- 查询接口会把 `web_*` wrapper id 映射回真实 run id，并展示 manifest、events、subagents、summary、blueprint 等 artifacts。

用户文档只暴露 `run.sh` 入口；底层 `galois-run web` 保留为脚本调用和自动化测试入口。

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

- `show-config`
- `plan-run`
- `launch-run`
- `inspect-run`
- `web`
- `suite list`
- `suite plan`
- `suite init-smoke`

当前 `plan-run` 只做 planning，不做 execution。  
`launch-run` 负责创建 run、写事件、启动 workflow、管理 verification service、归档结果。`web` 由 `run.sh` 包装，提供本地研究工作台。

## 12. benchmark 设计

### 12.1 当前 benchmark 层级

当前主路径至少区分：

- `reasoning-only`
- `reasoning-verification`

### 12.2 当前 benchmark 入口

已落地：

- `benchmarks/manifests/reasoning_data_smoke.toml`
- `uv run galois-run suite list`
- `uv run galois-run suite plan --pipeline reasoning-verification`

默认 smoke suite 复用 `three_horse/reasoning/data`。

### 12.3 benchmark 记录要求

每次实验至少记录：

- problem set
- backend / model / effort
- pipeline
- repair loop 配置
- success / partial / fail
- failure category

## 13. 实施阶段

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

- 更稳定的问题集入口
- 结果聚合
- 更清晰的 ablation 支持

## 13. 当前开发约定

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
