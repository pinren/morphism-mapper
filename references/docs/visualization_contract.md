# Visualization Contract (Strict JSON, v1)

本文件定义 Morphism Mapper 输出给前端可视化的**唯一标准契约**。  
目标：新 session 必须可直接被可视化读取，不依赖 legacy 适配。

## 0. 目录命名与 run 唯一性（硬要求）

- 单次 run 只能绑定一个持久化目录，不允许同一 run 多目录并行写入。
- 目录名必须等于 `session_id`，格式：
  - `YYYYMMDDTHHMMSSZ_xxxxxx_slug`
  - 其中 `xxxxxx` 为 6 位十六进制随机段。
- `session_manifest.session_id` 必须与目录 basename 完全一致。
- 若发现同一 `run_id`（`YYYYMMDDTHHMMSSZ_xxxxxx`）对应多个目录，视为协议违规。
  - 违规码：`PROTOCOL_BREACH_RUN_DIRECTORY_SPLIT`

## 1. 必需文件（硬要求）

Swarm 与 Fallback **必须生成同一套文件路径**；不得因模式不同而删减文件。

以下文件缺任意一项，都应视为 `PROTOCOL_BREACH_VISUALIZATION_ARTIFACT_MISSING`：

- `${MORPHISM_EXPLORATION_PATH}/session_manifest.json`
- `${MORPHISM_EXPLORATION_PATH}/mailbox_events.ndjson`
- `${MORPHISM_EXPLORATION_PATH}/metadata.json`
- `${MORPHISM_EXPLORATION_PATH}/category_skeleton.json`
- `${MORPHISM_EXPLORATION_PATH}/domain_selection_evidence.json`
- `${MORPHISM_EXPLORATION_PATH}/launch_evidence.json`（fallback 也必须写）
- `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`（必要时 round2+）
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json`
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/OBSTRUCTION_GATE_CLEARED.json`
- `${MORPHISM_EXPLORATION_PATH}/final_reports/synthesis.json`

## 2. 禁止项（legacy 不再允许）

- 禁止把 `logs/message_events.jsonl` 作为主事件源。
- 禁止仅输出 `mailbox/*.json` 零散事件而缺失聚合事件流。
- 禁止缺失 `session_manifest.json`。

可选调试文件（不影响契约）：

- `logs/lead_events.jsonl`
- `logs/obstruction_events.jsonl`
- `logs/synthesis_events.jsonl`
- `artifacts/failover/*.envelope.json`

## 3. session_manifest.json 最小结构

参考 schema：`assets/agents/schemas/session_manifest.v1.json`

```json
{
  "schema_version": "session_manifest.v1",
  "session_id": "string",
  "run_mode": "swarm|fallback|hybrid",
  "topic": "string",
  "timestamp_start": "ISO-8601",
  "timestamp_end": "ISO-8601|null",
  "selected_domains": ["string"],
  "active_domains": ["string"],
  "wildcard_domain": "string|null",
  "status": "RUNNING|COMPLETED|BLOCKED|FAILED",
  "artifact_version": "1.1"
}
```

模式约束：

- `run_mode=swarm`：`launch_evidence.json` 必须含 `team_name/core_ready_signals`
- `run_mode=fallback`：`launch_evidence.json` 必须含 `fallback_reason/team_unavailable`
- 不允许“fallback 缺文件、swarm 才有文件”的分叉输出

## 4. mailbox_events.ndjson 行结构

参考 schema：`assets/agents/schemas/mailbox_event.v1.json`

每行必须是单个合法 JSON 对象：

```json
{
  "timestamp": "ISO-8601",
  "signal": "string",
  "actor": "lead|domain|obstruction|synthesizer|system",
  "target": "string|null",
  "domain": "string|null",
  "payload_ref": "relative/path/or/null",
  "summary": "string"
}
```

要求：

- 必须有 `timestamp` 和 `signal`。
- 不允许仅使用 `event/message` 旧字段。
- 若原始事件来自其他格式，必须在落盘前归一为本结构。

## 4.1 Domain/Obstruction 同构完整性

以 `session_manifest.active_domains` 为准，逐域必须存在：

- `domain_results/{domain}_round1.json`
- `obstruction_feedbacks/{domain}_obstruction.json`

并且必须存在：

- `obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json`
- `obstruction_feedbacks/OBSTRUCTION_GATE_CLEARED.json`

## 5. 失败处理

- 主写入失败时必须走 failover。
- 若主写入 + failover 都失败，必须阻塞流程并输出：
  - `PROTOCOL_BLOCKED_PERSISTENCE_UNAVAILABLE`
  - `PROTOCOL_BREACH_VISUALIZATION_ARTIFACT_MISSING`

## 6. 交付前校验（必须）

执行：

```bash
python3 scripts/validate_session_contract.py "${MORPHISM_EXPLORATION_PATH}"
```

要求：

- 退出码必须为 `0`
- 出现任意 `[ERROR]` 视为未达标，不得宣布会话完成
