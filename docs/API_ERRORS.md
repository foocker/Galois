# API Error Contract

API 错误只保留前端真正需要处理的几类。前端判断 `error.code`，不要判断英文
`message`。

## Shape

```json
{
  "error": {
    "code": "not_found",
    "message": "Project not found.",
    "retryable": false
  }
}
```

## Run Failure

已经被 API 接收的 run 可能在执行中失败。这时创建请求仍然是成功的，后续查询
run 状态时会看到 `failed`：

```json
{
  "project_id": "...",
  "run_id": "...",
  "status": "failed",
  "capability": "math_research",
  "continued_from": null,
  "error": {
    "code": "runtime_failed",
    "message": "The run failed during execution.",
    "retryable": true
  },
  "artifacts": {
    "solution": null,
    "verified_solution": null
  }
}
```

## Error Codes

| Code | When | Frontend behavior |
| --- | --- | --- |
| `not_found` | Project 或 run 不存在，或当前用户无权访问。 | 回到列表页或提示任务不可用。 |
| `insufficient_credits` | 用户积分不足，不能开启新 run。 | 引导充值、升级或联系管理员。 |
| `busy` | 用户并发数已满，或系统队列暂时接不下新任务。 | 告诉用户稍后重试，也可以保留当前输入。 |
| `runtime_failed` | run 已创建，但 agent 执行失败。这个错误在 run 状态里，不是创建接口的 HTTP 错误。 | 在 run 页面提示失败，允许用户追加 prompt 后继续。 |
| `internal_error` | 服务端未知错误。 | 显示通用错误，不暴露日志、本机路径或内部实现。 |

当前 runtime 服务实际会返回 `not_found`、`runtime_failed`、`internal_error`。
`insufficient_credits` 和 `busy` 通常由产品后端或网关在接入用户、积分、限流后返回。

网络断开、请求超时、浏览器 fetch 失败不一定有 API payload。前端按“网络错误，
请重试”处理即可。
