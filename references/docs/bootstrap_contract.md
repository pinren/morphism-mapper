# Bootstrap Contract (Single Source of Truth)

本文件定义 Morphism Mapper 的最小启动协议。  
目标：去掉 ACK 机制，改为 `SendMessage + mailbox` 驱动。

## 1) 状态机

`INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> CORE_READY -> RUNNING -> (可选) FALLBACK`

## 2) 状态职责

| 状态 | 允许动作 | 禁止动作 |
|---|---|---|
| `INIT` | `TeamCreate(team_name=...)` | 直接分析、直接拉成员 |
| `TEAM_PROBED` | 解析 TeamCreate 返回 | 跳过分支 |
| `TEAM_READY` | 先跑 `scripts/domain_selector.py`（或等价调用）并产出 `DOMAIN_SELECTION_EVIDENCE`，再构建首批 roster | 手工拍脑袋选域；Lead 逐个手动拉首批成员 |
| `MEMBERS_READY` | 一次团队级首批启动 | 拆分首发 |
| `CORE_READY` | 向 core 发送启动指令并等待 mailbox 就绪信号 | core 未就绪就发 domain 分析指令 |
| `RUNNING` | 仅 `SendMessage` + mailbox 轮询推进 | Lead 代替 core 干活 |
| `FALLBACK` | 走 `simulation_mode_guide.md` | 继续 Team 流程 |

## 3) TeamCreate 分支

1. 成功 -> `TEAM_READY`
2. `Already leading team XXX` -> `TEAM_READY`（复用 `XXX`）
3. `Feature not available` -> `FALLBACK`

补充：

- `TeamCreate` 是唯一必需显式入口。
- 禁止基于“工具名是否出现”做可用性推断。

## 4) 团队级启动语义

团队级首批启动以行为证据判定，不依赖固定工具名：

- 首批一次覆盖 `core + selected_domains`
- 有 `LAUNCH_EVIDENCE`
- core 成员都在 mailbox 发出就绪业务信号

不合规示例：

- Lead 逐个 `Task(...)` 拉首批
- `Task(..., team_name, subagent_type)` 伪装团队启动
- 先 core 后 domain 分批首发

## 4.5) 领域选择门禁（必须）

在 `TEAM_READY` 阶段，Lead 必须先执行领域选择器并输出证据，再允许进入 `MEMBERS_READY`。

最小证据：

```json
{
  "signal": "DOMAIN_SELECTION_EVIDENCE",
  "selector_method": "scripts/domain_selector.py|helpers.call_domain_selector",
  "selector_ok": true,
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

## 5) Core 就绪（无 ACK）

去掉 `*_ACK`。改为 mailbox 业务信号：

- `obstruction-theorist` 发 `OBSTRUCTION_PIPELINE_READY`
- `synthesizer` 发 `SYNTHESIS_PIPELINE_READY`

两条信号齐全后才允许进入 `RUNNING`。

## 6) Domain 交付（无 ACK）

每个 domain 仍需双投递：

1. `MAPPING_RESULT_ROUND1` -> obstruction
2. `MAPPING_RESULT_JSON` -> synthesizer

不再要求 ACK。Lead 用 mailbox 观察下游业务结果推进：

- obstruction 对该域产出 `OBSTRUCTION_FEEDBACK`
- synthesizer 将该域纳入 `PRELIMINARY_SYNTHESIS` 或发 `SCHEMA_REJECTED`

## 7) Obstruction -> Synthesizer 时序

1. Domain round1 双投递
2. obstruction 完成首轮并发 `OBSTRUCTION_ROUND1_COMPLETE`
3. 有 `REVISE/REJECT` 先修正再复审
4. `OBSTRUCTION_GATE_CLEARED` 后，Lead 才能发 `FINAL_SYNTHESIS_REQUEST`

## 8) 最小 LAUNCH_EVIDENCE

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

## 9) 违规码（最小集）

- `PROTOCOL_BREACH_INITIAL_TASK_LAUNCH`
- `PROTOCOL_BREACH_INVALID_FALLBACK_REASON`
- `PROTOCOL_BREACH_PARTIAL_ATOMIC_LAUNCH`
- `PROTOCOL_BREACH_CORE_NOT_READY`
- `PROTOCOL_BREACH_DOMAIN_BEFORE_CORE_READY`
- `PROTOCOL_BREACH_LEAD_SOLO_ANALYSIS`
- `PROTOCOL_BLOCKED_TEAM_LAUNCH_UNAVAILABLE`
- `PROTOCOL_BREACH_SELECTOR_SKIPPED`

## 10) 一页执行清单

1. TeamCreate
2. 运行 domain selector 并产出 `DOMAIN_SELECTION_EVIDENCE`
3. 构建首批 roster
4. 团队级首批启动
5. core 发 pipeline ready 信号
6. 广播 `CATEGORY_SKELETON`
7. domain 双投递
8. obstruction round1 / gate
9. final synthesis
