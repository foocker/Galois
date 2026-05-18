# Agent Runtime

这是一个面向前端或其他后端的数学研究 agent 运行服务。公共接口只暴露项目、运行、事件和产物，不暴露底层 agent 名称、内部文件结构或本机路径。

## 快速开始

```bash
uv sync
uv run agent-runtime serve --host 127.0.0.1 --port 8765 --max-concurrency 2
```

创建首轮研究：

```bash
uv run agent-runtime create \
  --problem-file problem.md \
  --title "Compactness problem" \
  --instruction strategy.md \
  --reference notes.md \
  --json
```

继续已有项目：

```bash
uv run agent-runtime continue <project_id> \
  --prompt "The first proof missed a boundary case. Continue from the prior work." \
  --json
```

查询状态和结果：

```bash
uv run agent-runtime status <run_id> --json
uv run agent-runtime artifacts <run_id> --json
uv run agent-runtime events <run_id> --json
```

## HTTP 接口

服务默认地址：`http://127.0.0.1:8765`

- `GET /v1/health`
- `GET /v1/config`
- `GET /v1/projects`
- `GET /v1/projects/{project_id}`
- `GET /v1/projects/{project_id}/runs`
- `POST /v1/projects`
- `POST /v1/projects/{project_id}/runs`
- `GET /v1/runs/{run_id}`
- `GET /v1/runs/{run_id}/artifacts`
- `GET /v1/runs/{run_id}/events`

详细请求和响应见 `docs/AGENT_RUNTIME_API.md`。

## 目录

```text
src/agent_runtime/        CLI 和 HTTP service
docs/AGENT_RUNTIME_API.md API 合约
docs/FRONTEND_INTEGRATION.md 前端交互实现说明
tests/                    接口与运行时测试
references/Lumen/         底层 agent 资产；不是公共 API
```

运行数据默认写入 `.research-runtime/`，也可以通过 `agent-runtime serve --runtime-root <dir>` 指定。HTTP 创建和续跑请求会先进入本机队列，`--max-concurrency` 或 `AGENT_RUNTIME_MAX_CONCURRENCY` 控制同时运行的 agent 数；同一个 project 的 run 会串行执行，避免并发写同一份 `memory/` 和 `results/`。

每个 project 只创建一个薄 workspace：静态 agent 资产通过符号链接复用，`data/`、`input/`、`memory/`、`results/`、`downloads/`、`scripts/` 在 project 内持续写入和复用；每个 run 保留本轮 `input/`、`logs/`、`events` 和 artifact 快照，并在 run 目录下提供 `memory/`、`results/`、`downloads/`、`scripts/` 的符号链接入口，方便人工检查但不复制数据。
