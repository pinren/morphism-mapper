# DOMAIN_AGENT_GUIDE (v4.7)

## 协议优先级

1. `assets/agents/schemas/domain_mapping_result.v1.json`
2. `references/docs/bootstrap_contract.md`
3. 本指南

## 角色目标

Domain Agent 的唯一交付物是 `domain_mapping_result.v1` JSON。

## 必做步骤

1. 读取领域文件：`references/{domain}_v2.md` 或 `references/custom/{domain}_v2.md`
2. 生成 `domain_file_hash`（sha256）
3. 在 `evidence_refs` 中明确引用文件证据
4. 完整输出 schema 必填字段
5. 将同一 JSON 主体发送给 `obstruction-theorist` 与 `synthesizer`
6. 等待双 ACK：`OBSTRUCTION_ACK_RECEIVED` + `SYNTHESIZER_ACK_RECEIVED`

## 必填字段

- `schema_version`
- `domain`
- `domain_file_path`
- `domain_file_hash`
- `evidence_refs`
- `objects_map`
- `morphisms_map`
- `theorems_used`
- `kernel_loss`
- `strategy_topology`
- `topology_reasoning`
- `confidence`

## 严格门禁

### 无效条件（任一触发即无效）

- 未读取领域文件
- 缺失 `domain_file_hash`
- `kernel_loss.lost_nuances` 为空
- 仅输出 markdown 表格，未输出 JSON 主体
- 只给单个 recipient 发送结果
- 90s 内未收到 ACK 且未重发/上报

### 通过条件

- JSON 可被 `validate_mapping_json.py` 校验通过
- `evidence_refs` 至少覆盖 Fundamentals + Core Morphisms + Theorems
- `theorems_used` 至少 2 条，且有 mapping hint 应用

## 推荐发送格式

```text
MAPPING_RESULT_JSON
message_id={domain}-{timestamp}-roundN
{json_payload}
```

## 审查后修正

收到 `OBSTRUCTION_FEEDBACK` 后，必须重发完整 JSON 主体，不允许只发送增量 diff。
若 90s 内未收到任一 ACK，必须重发一次并向 Team Lead 上报 `DELIVERY_ACK_TIMEOUT`。
