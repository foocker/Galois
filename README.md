# Galois

Galois 是一个 Codex-first 的数学 agent 单仓工作区，当前聚焦：

- 自然语言数学推理 `reasoning`
- 自然语言证明校验 `verification`
- 面向数学研究的 Web workbench

## 快速开始

本地开发入口直接使用项目 CLI：

```bash
uv run galois-run web
```

默认会启动研究工作台 Web UI。打开终端输出中的本地地址后，可以输入 Markdown/LaTeX 数学问题，等待 Galois 创建真实 run，并查看 reasoning / verification 状态与结果产物。

常用入口：

```bash
uv run galois-run web
uv run galois-run suite list
uv run galois-run inspect-run <run_id_or_path>

uv run galois-run plan-run \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --pipeline reasoning-verification

uv run galois-run launch-run \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --pipeline reasoning-only

uv run galois-run launch-run \
  --problem-id polynomial-Freiman-Ruzsa-conjecture \
  --problem-path "benchmarks/problems/finite_fields/polynomial Freiman-Ruzsa conjecture.md" \
  --pipeline reasoning-only
```

Web 端口通过 CLI 参数设置：

```bash
uv run galois-run web --host 127.0.0.1 --port 8000
```

真实 reasoning / verification 需要当前 shell 中已经配置好模型环境变量，例如 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY`。

## 当前能力

- `galois-run launch-run`：创建 run 目录、写事件日志、启动 workflow、归档 stdout / stderr。
- `reasoning-only`：只跑自然语言数学推理并归档 `blueprint`。
- `reasoning-verification`：启动 reasoning，并在需要时启动 verification API 做自然语言校验。
- Web workbench：提交 Markdown 问题、轮询 run 状态、展示事件轨迹和最终 artifact。
- benchmark smoke suite：保留本地 suite 规划与列表入口。

## 项目结构

```text
three_horse/     reasoning 和 verification 的运行资产
projects/        run、service、artifact、report 等运行状态
benchmarks/      benchmark problems 与实验 manifest
configs/         系统与实验配置
docs/            架构、设计与计划文档
src/galois/      长期维护的 Python package 代码
references/      只读上游参考快照
```

核心设计文档见 `docs/GALOIS_SYSTEM_DESIGN.md`。

## 开发边界

主开发路径：

- `src/galois/`
- `configs/`
- `docs/`
- `tests/`

资产目录：

- `three_horse/reasoning/`
- `three_horse/verification/`

不要把新核心逻辑继续放进 `references/`。
