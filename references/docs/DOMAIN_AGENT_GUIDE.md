# DOMAIN_AGENT_GUIDE (v4.7, no-ack)

## 协议优先级

1. `assets/agents/schemas/domain_mapping_result.v1.json`
2. `references/docs/bootstrap_contract.md`
3. 本指南

## 必做步骤

1. 优先读取 skill 内 `references/` 绝对路径文件
2. 仅绝对路径不可读时回退 `references/...` 相对路径
3. 生成 `domain_file_hash`（sha256）
4. 输出完整 `domain_mapping_result.v1` JSON
5. 双投递：
   - `MAPPING_RESULT_ROUND1` -> obstruction
   - `MAPPING_RESULT_JSON` -> synthesizer
6. 通过 mailbox 等待后续业务消息（审查反馈/修正请求）

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

## 无效条件

- 未读取领域文件
- 缺失 `domain_file_hash`
- `kernel_loss` 不是对象
- 未输出合法 JSON 主体
- 只发送给单个 recipient

## 修正规则

收到 `OBSTRUCTION_FEEDBACK` 或 `SCHEMA_REJECTED` 后，必须重发完整 JSON 主体，不发送 diff 片段。
