# plan-run 只做规划，不启动 workflow
# uv run galois-run plan-run \
#   --problem-id example \
#   --problem-path three_horse/reasoning/data/example.md \
#   --pipeline reasoning-verification


# 1. 只跑自然语言证明生成
# uv run galois-run launch-run \
#   --problem-id example \
#   --problem-path three_horse/reasoning/data/example2.md \
#   --pipeline reasoning-only


# 2. 轻量 smoke：证明生成 -> 自然语言验证
# uv run galois-run launch-run \
#   --problem-id Alan-Cahn-Navier-Stokes \
#   --problem-path "benchmarks/problems/Alan-Cahn-Navier-Stokes Equations.md" \
#   --pipeline reasoning-verification

# 研究级 benchmark 单独手动跑，不建议作为默认脚本：
# uv run galois-run launch-run \
#   --problem-id "Existence of the Batchelor Scale" \
#   --problem-path "benchmarks/problems/Existence of the Batchelor Scale.md" \
#   --pipeline reasoning-verification


uv run galois-run launch-run \
  --problem-id cap-set-problem\
  --problem-path "benchmarks/problems/finite_fields/cap set problem.md" \
  --pipeline reasoning-only
