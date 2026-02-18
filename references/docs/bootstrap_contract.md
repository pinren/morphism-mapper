# Bootstrap Contract (Single Source of Truth)

本文件定义 Morphism Mapper 的最小启动协议。  
目标：去掉 ACK 机制，改为 `SendMessage + mailbox` 驱动。

可视化契约（硬要求）：

- 必须遵循 `references/docs/visualization_contract.md`
- 新 session 必须产出 `session_manifest.json` + `mailbox_events.ndjson`
- 禁止把 `logs/message_events.jsonl` 当主事件流
- 同一 run 只能使用一个 `${MORPHISM_EXPLORATION_PATH}`，目录名必须等于 `session_id`

## 1) 状态机

`INIT -> PERSISTENCE_READY -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> CORE_READY -> RUNNING -> (可选) FALLBACK`

## 2) 状态职责

| 状态 | 允许动作 | 禁止动作 |
|---|---|---|
| `INIT` | 执行持久化前置检查 | 直接分析、直接拉成员 |
| `PERSISTENCE_READY` | `TeamCreate(team_name=...)` | 使用项目目录或 `/tmp` 作为主持久化目录 |
| `TEAM_PROBED` | 解析 TeamCreate 返回 | 跳过分支 |
| `TEAM_READY` | 优先执行 `scripts/prepare_domain_selection.py` 提取并落盘 `CATEGORY_SKELETON`（含 `CATEGORY_SKELETON_EXTRACTED`），再产出 `DOMAIN_SELECTION_EVIDENCE`，再构建首批 roster | 手工拍脑袋选域；跳过 skeleton 提取；手写超长 skeleton 直接 write；Lead 逐个手动拉首批成员 |
| `MEMBERS_READY` | 一次团队级首批启动 | 拆分首发 |
| `CORE_READY` | 向 core 发送启动指令并等待 mailbox 就绪信号 | core 未就绪就发 domain 分析指令 |
| `RUNNING` | 仅 `SendMessage` + mailbox 轮询推进 | Lead 代替 core 干活 |
| `FALLBACK` | 走 `simulation_mode_guide.md` | 继续 Team 流程 |

## 3) 持久化前置门禁（必须）

在调用 `TeamCreate` 前，Lead 必须先完成持久化初始化并记录：

```json
{
  "signal": "PERSISTENCE_READY",
  "persistence_mode": "production",
  "exploration_path": "/home/<user>/.morphism_mapper/explorations/<session_id>",
  "writable": true
}
```

硬约束：

- `exploration_path` 必须在 `~/.morphism_mapper/explorations/` 下
- `<session_id>` 格式必须是 `YYYYMMDDTHHMMSSZ_xxxxxx_slug`
- `MORPHISM_RUN_ID` 格式必须是 `YYYYMMDDTHHMMSSZ_xxxxxx`
- 同一 `MORPHISM_RUN_ID` 必须映射到唯一 `exploration_path`
- 禁止使用项目目录（cwd/workspace）和 `/tmp`
- 任一关键目录创建失败时必须阻塞流程，标记 `PROTOCOL_BLOCKED_PERSISTENCE_UNAVAILABLE`
- 主写入失败时必须执行 failover 持久化（`artifacts/failover`），仅当主+failover 都失败才阻塞

## 4) TeamCreate 分支

1. 成功 -> `TEAM_READY`
2. `Already leading team XXX` -> `TEAM_READY`（复用 `XXX`）
3. `Feature not available` -> `FALLBACK`

补充：

- `TeamCreate` 是唯一必需显式入口。
- 禁止基于“工具名是否出现”做可用性推断。

## 5) 团队级启动语义

团队级首批启动以行为证据判定，不依赖固定工具名：

- 首批一次覆盖 `core + selected_domains`
- 有 `LAUNCH_EVIDENCE`
- core 成员都在 mailbox 发出就绪业务信号

不合规示例：

- Lead 逐个 `Task(...)` 拉首批
- `Task(..., team_name, subagent_type)` 伪装团队启动
- 先 core 后 domain 分批首发
- Lead 在主 context 连续读取多个 `references/*_v2.md` 并直接写 `domain_results/*.json`

## 5.5) Skeleton + 领域选择门禁（必须）

在 `TEAM_READY` 阶段，Lead 必须先提取 `CATEGORY_SKELETON`，再执行领域选择器并输出证据，再允许进入 `MEMBERS_READY`。

强制建议：

- 默认必须调用 `scripts/prepare_domain_selection.py --topic "<problem>"`。
- 禁止把超长/多层嵌套 skeleton 直接写入 `write` 参数。

最小 skeleton 提取证据：

```json
{
  "signal": "CATEGORY_SKELETON_EXTRACTED",
  "extraction_method": "scripts/prepare_domain_selection.py|equivalent",
  "category_skeleton_ref": "category_skeleton.json",
  "category_skeleton_sha256": "<sha256>",
  "objects_count": 1,
  "morphisms_count": 1
}
```

最小证据：

```json
{
  "signal": "DOMAIN_SELECTION_EVIDENCE",
  "selector_method": "scripts/domain_selector.py|helpers.call_domain_selector",
  "category_skeleton_ref": "category_skeleton.json",
  "selector_input_ref": "artifacts/domain_selection/selector_input.json",
  "selector_output_ref": "artifacts/domain_selection/selector_output.json",
  "domain_catalog_ref": "artifacts/domain_selection/domain_catalog_snapshot.json",
  "domain_catalog_sha256": "<sha256>",
  "domain_knowledge_ref": "artifacts/domain_selection/domain_knowledge_snapshot.json",
  "domain_knowledge_sha256": "<sha256>",
  "selected_domains_source": "selector_output.top_domains + knowledge_viability_gate",
  "selector_ok": true,
  "blind_spot_generation_required": false,
  "blind_spot_domains": [],
  "blind_spot_trigger_signals": [],
  "blind_spot_domain_sources": {},
  "blind_spot_evidence_ref": null,
  "selected_domains": ["..."],
  "selector_rationale": "..."
}
```

仅当 selector 执行失败时允许降级为手工选域，但必须带原始错误：

```json
{
  "signal": "DOMAIN_SELECTION_EVIDENCE",
  "selector_ok": false,
  "selector_error": "<stderr/raw error>",
  "manual_selection_reason": "...",
  "selected_domains": ["..."]
}
```

无证据直接选域，标记 `PROTOCOL_BREACH_SELECTOR_SKIPPED`。
若 `selector_ok=true` 但缺失 `selector_input_ref/selector_output_ref/domain_catalog_ref/domain_knowledge_ref`，或 `selected_domains` 不在 selector 输出中，或所选域无对应 `references/*_v2.md`，视为违规。
若触发补盲扩域（`blind_spot_generation_required=true`），必须满足：
- `blind_spot_domains == (active_domains - selected_domains)`
- `blind_spot_trigger_signals` 非空（来自低置信/输入不完整信号）
- `blind_spot_domain_sources[domain] in {builtin, add-domain}`
- `add-domain` 对应知识文件位于 `references/custom/{domain}_v2.md`
在 `DOMAIN_SELECTION_EVIDENCE` 生成前，输出“已准备领域团队 N 个/领域清单表格”同样视为违规（预选域泄漏）。

## 6) Core 就绪（无 ACK）

去掉 `*_ACK`。改为 mailbox 业务信号：

- `obstruction-theorist` 发 `OBSTRUCTION_PIPELINE_READY`
- `synthesizer` 发 `SYNTHESIS_PIPELINE_READY`

两条信号齐全后才允许进入 `RUNNING`。

## 7) Domain 交付（无 ACK）

每个 domain 仍需双投递：

1. `MAPPING_RESULT_ROUND1` -> obstruction
2. `MAPPING_RESULT_JSON` -> synthesizer

不再要求 ACK。Lead 用 mailbox 观察下游业务结果推进：

- obstruction 对该域产出 `OBSTRUCTION_FEEDBACK`
- synthesizer 将该域纳入 `PRELIMINARY_SYNTHESIS` 或发 `SCHEMA_REJECTED`
- 若 synthesizer 读取到截断/分页结果，必须发 `INPUT_INCOMPLETE`，并阻塞综合输出
- 分页读取必须读到 EOF 并成功解析完整 JSON；补齐后必须发 `INPUT_COMPLETE`（含 `content_sha256`）

## 8) Obstruction -> Synthesizer 时序

1. Domain round1 双投递
2. obstruction 完成首轮并发 `OBSTRUCTION_ROUND1_COMPLETE`
3. 有 `REVISE/REJECT` 先修正再复审
4. `OBSTRUCTION_GATE_CLEARED` 后，Lead 才能发 `FINAL_SYNTHESIS_REQUEST`
5. 禁止预创建 obstruction 占位文件；每域 obstruction 落盘必须发生在对应 domain round 结果之后
6. 若任一域存在未被 `INPUT_COMPLETE` 解除的 `INPUT_INCOMPLETE`，禁止触发 `FINAL_SYNTHESIS_REQUEST`

Lead 放行前必须做报告验收：

- `OBSTRUCTION_ROUND1_COMPLETE.coverage.reviewed_domains == active_domains`
- `domain_verdicts` 覆盖全部 active domains
- `unresolved_domains` 为空（或明确进入修正轮）
- `OBSTRUCTION_GATE_CLEARED.conditions_for_final_synthesis` 非空
- `clear_summary` 必含 `pass_domains/revised_domains/excluded_domains/residual_risks`

任一不满足：禁止 final synthesis，标记 `PROTOCOL_BREACH_WEAK_OBSTRUCTION_REPORT`。

## 9) 最小 LAUNCH_EVIDENCE

```json
{
  "launch_mode": "team_launch",
  "launch_method": "team_api|platform_nl_team_invocation",
  "team_name": "xxx",
  "selected_domains": ["..."],
  "active_core_members": ["obstruction-theorist", "synthesizer"],
  "core_ready_signals": [
    "OBSTRUCTION_PIPELINE_READY",
    "SYNTHESIS_PIPELINE_READY"
  ]
}
```

## 10) 违规码（最小集）

- `PROTOCOL_BREACH_INITIAL_TASK_LAUNCH`
- `PROTOCOL_BREACH_INVALID_FALLBACK_REASON`
- `PROTOCOL_BREACH_PARTIAL_ATOMIC_LAUNCH`
- `PROTOCOL_BREACH_CORE_NOT_READY`
- `PROTOCOL_BREACH_DOMAIN_BEFORE_CORE_READY`
- `PROTOCOL_BREACH_LEAD_SOLO_ANALYSIS`
- `PROTOCOL_BREACH_LEAD_DOMAIN_FILE_WRITE`
- `PROTOCOL_BLOCKED_TEAM_LAUNCH_UNAVAILABLE`
- `PROTOCOL_BREACH_SELECTOR_SKIPPED`
- `PROTOCOL_BREACH_WEAK_OBSTRUCTION_REPORT`
- `PROTOCOL_BREACH_PERSISTENCE_NOT_READY`
- `PROTOCOL_BREACH_ILLEGAL_PERSISTENCE_PATH`
- `PROTOCOL_BREACH_PERSISTENCE_FAILOVER_SKIPPED`
- `PROTOCOL_BLOCKED_PERSISTENCE_UNAVAILABLE`

## 11) 一页执行清单

1. 产出 `PERSISTENCE_READY`
2. TeamCreate
3. 提取 `CATEGORY_SKELETON` 并产出 `CATEGORY_SKELETON_EXTRACTED`
4. 运行 domain selector 并产出 `DOMAIN_SELECTION_EVIDENCE`
5. 构建首批 roster
6. 团队级首批启动
7. core 发 pipeline ready 信号
8. 广播 `CATEGORY_SKELETON`
9. domain 双投递
10. obstruction round1 / gate
11. final synthesis

## 12) 强制门禁命令（必须）

在流程中必须执行以下阻断校验：

1. 每个 domain round 落盘后立刻执行：
   - `python3 scripts/strict_gate.py --phase domain ${MORPHISM_EXPLORATION_PATH} --domain <domain>`
2. Final 输出前执行：
   - `python3 scripts/strict_gate.py --phase final ${MORPHISM_EXPLORATION_PATH}`

任一命令返回非 0，必须阻塞流程，不得宣布完成。
