# Agent Runtime

这是一个面向前端或其他后端的数学研究 agent 运行服务。公共接口只暴露项目、运行、事件和产物，不暴露底层 agent 名称、内部文件结构或本机路径。

## 快速开始

```bash
uv sync
uv run agent-runtime serve --host 127.0.0.1 --port 8765
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
tests/                    接口与运行时测试
references/Lumen/         底层 agent 资产；不是公共 API
```

运行数据默认写入 `.research-runtime/`，也可以通过 `agent-runtime serve --runtime-root <dir>` 指定。
