# Galois

Galois 是一个 Codex-first 的数学 agent 单仓工作区，当前聚焦：

- 自然语言数学推理 `reasoning`
- 自然语言证明校验 `verification`
- 面向数学研究的 Web workbench

## 快速开始

本地开发入口直接使用项目 CLI：

```bash
uv run galois web
```

默认会启动研究工作台 Web UI。打开终端输出中的本地地址后，可以输入 Markdown/LaTeX 数学问题，等待 Galois 创建真实 run，并查看 reasoning / verification 状态与结果产物。

常用入口：

```bash
uv run galois web
uv run galois suite list
uv run galois inspect <run_id_or_path>

uv run galois plan \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --pipeline reasoning-verification

uv run galois launch \
  --problem-id example \
  --problem-path three_horse/reasoning/data/example.md \
  --pipeline reasoning-only

uv run galois launch \
  --problem-id polynomial-Freiman-Ruzsa-conjecture \
  --problem-path "benchmarks/problems/finite_fields/polynomial Freiman-Ruzsa conjecture.md" \
  --pipeline reasoning-only
```

Web 端口通过 CLI 参数设置：

```bash
uv run galois web --host 127.0.0.1 --port 8000
```

真实 reasoning / verification 需要当前 shell 中已经配置好模型环境变量，例如 `OPENAI_BASE_URL` 与 `OPENAI_API_KEY`。

## 本地 PostgreSQL

Problem Garden 使用本地 PostgreSQL 作为正式数据源。WSL / Ubuntu 24.04 可直接安装系统包：

```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo service postgresql start
pg_isready
psql --version
```

初始化 Galois 开发库：

```bash
sudo -u postgres psql
```

在 `psql` 中执行：

```sql
CREATE USER galois WITH PASSWORD 'galois_dev';
CREATE DATABASE galois OWNER galois;
GRANT ALL PRIVILEGES ON DATABASE galois TO galois;
\q
```

验证连接：

```bash
psql "postgresql://galois:galois_dev@127.0.0.1:5432/galois" -c "select version();"
```

默认配置见 `configs/defaults.toml` 的 `[database]`。如需覆盖连接串，设置：

```bash
export DATABASE_URL="postgresql://galois:galois_dev@127.0.0.1:5432/galois"
```

启动 Web 后，`/api/problem-garden/problems` 会自动建表并写入默认 seed 问题；候选问题提交会进入 `garden_submissions` 的 `pending_review` 队列。

## 当前能力

- `galois launch`：创建 run 目录、写事件日志、启动 workflow、归档 stdout / stderr。
- `reasoning-only`：只跑自然语言数学推理并归档 `blueprint`。
- `reasoning-verification`：启动 reasoning，并在需要时启动 verification API 做自然语言校验。
- Web workbench：提交 Markdown 问题、轮询 run 状态、展示事件轨迹和最终 artifact。
- benchmark example suite：保留本地 suite 规划与列表入口。

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
