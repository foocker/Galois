# Galois

Galois 是一个 Codex-first 的数学 agent 单仓工作区，当前主路径聚焦两件事：

- 自然语言数学推理 `reasoning`
- 自然语言证明校验 `verification`

仓库的目标不是把上游项目原样拼接，而是把仍然有价值的 prompt、skill、workflow 资产收进单仓，再在 `src/galois/platform/` 里建立稳定、可测、可 benchmark 的控制面。

主设计文件：

- [docs/GALOIS_SYSTEM_DESIGN.md](/home/gg/Galois/docs/GALOIS_SYSTEM_DESIGN.md)

## Current Status

当前状态：控制面已支持 `reasoning-only` 和 `reasoning-verification` 两条主链路。

已经具备：

- repo-level `uv` 环境与 [pyproject.toml](/home/gg/Galois/pyproject.toml)
- 默认配置文件 [configs/defaults.toml](/home/gg/Galois/configs/defaults.toml)
- Python 包入口 `galois-run`
- `show-config`：打印解析后的默认配置
- `plan-run`：创建 run manifest，并打印 launch plan
- `launch-run`：创建 run 目录、写事件日志、启动 workflow、归档 stdout / stderr
- `inspect-run`：查看 run manifest、events、subagent 状态
- `SubagentManager`：任务注册、后台线程、子进程、状态、取消、snapshot 能力
- `src/galois/reasoning` 内化 runner：直接实现 reasoning prompt / resume / session / repair 启动逻辑
- `src/galois/verification` 内化 service：直接实现 verification API，vendored API 只保留兼容入口
- reasoning blueprint 归档到 run 目录
- reasoning blueprint 到 verification API 的文件契约接线
- verification raw response 归一化为 Galois-owned artifact
- verification decision：`accepted` / `repair_needed` / `verification_malformed` / `verification_api_failed`
- `repair_needed` 时写 reasoning repair input contract
- repo-local smoke suite 规划入口：`galois-run suite list|plan|init-smoke`

尚未完成：

- subagent PTY attach / interactive TUI
- 更高级的多 subagent 调度策略
- 更完整的 benchmark harness

## Layout

```text
three_horse/     source asset root for reasoning and verification
projects/        runtime state root for runs, services, artifacts, and reports
benchmarks/      benchmark problems and experiment manifests
configs/         system and experiment configuration
docs/            architecture and design notes
src/galois/      long-lived Python package code
references/      read-only upstream reference snapshots
```

Core Python control-plane code lives in:

- [src/galois/contracts.py](/home/gg/Galois/src/galois/contracts.py)
- [src/galois/platform/config.py](/home/gg/Galois/src/galois/platform/config.py)
- [src/galois/platform/paths.py](/home/gg/Galois/src/galois/platform/paths.py)
- [src/galois/platform/contracts.py](/home/gg/Galois/src/galois/platform/contracts.py)
- [src/galois/platform/launcher.py](/home/gg/Galois/src/galois/platform/launcher.py)
- [src/galois/platform/run_registry.py](/home/gg/Galois/src/galois/platform/run_registry.py)
- [src/galois/platform/subagents.py](/home/gg/Galois/src/galois/platform/subagents.py)
- [src/galois/platform/workflows.py](/home/gg/Galois/src/galois/platform/workflows.py)
- [src/galois/platform/cli.py](/home/gg/Galois/src/galois/platform/cli.py)
- [src/galois/reasoning/runner.py](/home/gg/Galois/src/galois/reasoning/runner.py)
- [src/galois/verification/service.py](/home/gg/Galois/src/galois/verification/service.py)

## Environment

仓库使用 `uv` 作为默认环境与依赖管理器：

```bash
cd /home/gg/Galois
uv sync
uv sync --dev
```

主仓库依赖真源是 [pyproject.toml](/home/gg/Galois/pyproject.toml)。`three_horse/reasoning/` 和 `three_horse/verification/` 下保留的 requirements 仅作为上游参考，不应再为主仓库维护额外长期虚拟环境。

Codex 默认继承当前进程环境，例如：

```bash
export OPENAI_BASE_URL=...
export OPENAI_API_KEY=...
```

## Control Plane

查看解析后的配置：

```bash
cd /home/gg/Galois
uv run galois-run show-config
```

当前配置输出会包含：

```text
backend=codex
model=gpt-5.4
model_reasoning_effort=xhigh
reasoning_dir=three_horse/reasoning
reasoning_enabled=True
verification_dir=three_horse/verification
verification_enabled=True
max_repair_rounds=1
project_root=projects/default
run_root=runs
run_root_path=/home/gg/Galois/projects/default/runs
```

创建 run manifest 并打印 launch plan：

```bash
cd /home/gg/Galois
uv run galois-run plan-run \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --title "Example Problem"
```

`plan-run` 只做 planning，不启动 reasoning 或 verification。

创建 run 并启动配置好的 workflow：

```bash
cd /home/gg/Galois
uv run galois-run launch-run \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --title "Example Problem"
```

只跑自然语言推理：

```bash
cd /home/gg/Galois
uv run galois-run launch-run \
  --pipeline reasoning-only \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md
```

跑自然语言推理加自然语言校验：

```bash
cd /home/gg/Galois
uv run galois-run launch-run \
  --pipeline reasoning-verification \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md
```

`--verification-nlp` 仍作为 `--verification` 的兼容别名保留。外层 repair loop 属于运行策略，不是独立 pipeline；可用 `--no-repair-loop` 关闭。

本地 smoke suite：

```bash
uv run galois-run suite list
uv run galois-run suite plan --pipeline reasoning-verification
uv run galois-run suite plan --pipeline reasoning-only --limit 1
```

控制面 smoke 测试可使用：

```bash
cd /home/gg/Galois
uv run galois-run launch-run \
  --config tests/fixtures/no_workflows.toml \
  --problem-id empty-smoke \
  --problem-path three_horse/reasoning/data/example.md \
  --title "Empty Smoke"
```

查看 run：

```bash
cd /home/gg/Galois
uv run galois-run inspect-run projects/default/runs/<run_id>
```

## Manual Entrypoints

调试单个上游导入组件时，仍可使用手动入口。

Reasoning：

```bash
cd /home/gg/Galois
uv run bash three_horse/reasoning/tests/run_example.sh
uv run bash three_horse/reasoning/tests/run_example_resume.sh
uv run python -m galois.reasoning.runner --repo-root /home/gg/Galois
```

Verification API：

```bash
cd /home/gg/Galois
uv run uvicorn galois.verification.service:app --host 0.0.0.0 --port 8091
uv run python three_horse/verification/api/server.py
uv run python three_horse/verification/mcp/server.py
```

## Asset Boundaries

主开发路径：

- `src/galois/`
- `configs/`
- `docs/`

只在集成或清理上游资产时修改：

- `three_horse/reasoning/`
- `three_horse/verification/`

不要把新核心逻辑继续放进：

- `references/`
- 工作区外部的上游仓库

## Near-Term Target

近期重点是把 `reasoning-only` 与 `reasoning-verification` 两条链路继续做稳，包括：

- 更可靠的 run artifact 归档
- 更清晰的 repair-loop 记录
- 更可复现的 benchmark suite 规划与执行
