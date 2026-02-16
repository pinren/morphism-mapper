# Bootstrap Contract (Single Source of Truth)

本文件定义 Morphism Mapper 的最小可执行启动协议。  
若与其他文档冲突，以本文件为准。

## 1) 状态机

`INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> CORE_READY -> RUNNING -> (可选) FALLBACK`

## 2) 每个状态只做一类事

| 状态 | 允许动作 | 禁止动作 |
|---|---|---|
| `INIT` | `TeamCreate(team_name=...)` | 直接分析、直接拉成员 |
| `TEAM_PROBED` | 解析 TeamCreate 返回，进入 A/B/C 分支 | 跳过分支判定 |
| `TEAM_READY` | 构建首批 roster（core + selected domains） | Lead 逐个启动成员 |
| `MEMBERS_READY` | 一次团队级首批启动（团队级语义，不依赖固定工具名） | 拆成多批首发 |
| `CORE_READY` | 向 core 发 ping，收双 ACK | 未收双 ACK 就启动 domain 工作 |
| `RUNNING` | `SendMessage` 协作；团队级增量加人 | Lead 自己分析或代替 core |
| `FALLBACK` | 走 `simulation_mode_guide.md` | 继续 Team 流程 |

## 3) TeamCreate 三分支

1. Case A: 成功  
   - 进入 `TEAM_READY`
   - 使用返回的 `team_name`
2. Case B: `Already leading team XXX`  
   - 进入 `TEAM_READY`
   - 复用 `XXX`
3. Case C: `Feature not available`（或等效 Team 不可用）  
   - 进入 `FALLBACK`

补充约束：

- `TeamCreate` 是唯一必需的显式入口调用。
- 禁止根据“工具列表里是否出现 AgentTeam/SendMessage”来判定可用性。
- 只看 `TeamCreate` 返回与后续启动证据。

## 4) 团队级启动定义（关键）

团队级启动的判据是“语义与证据”，不是函数名：

- 首批一次覆盖 `core + selected domains`
- 有可审计 `LAUNCH_EVIDENCE`
- 有 core 双 ACK

实现上可表现为：

- 显式团队 API（若平台暴露）
- 平台 in-process 自然语言 team invocation

以下都不算团队级启动：

- Lead 逐个 `Task(...)` 拉成员
- `Task(..., team_name, subagent_type)` 伪装团队启动
- 先 core 后 domain 的分批首发
- “domain analysis agents”这类聚合任务替代真实队伍拉起

## 5) Core 就绪门禁

首批启动后，Lead 必须先收齐：

- `OBSTRUCTION_CORE_READY_ACK`
- `SYNTHESIZER_CORE_READY_ACK`

收齐前禁止：

- 启动任何 domain 分析流程
- 声称 “Agent Swarm 已启动”

## 6) Delegation Mode（简化后硬约束）

- Lead 只做编排、状态推进、催办、仲裁
- Lead 不得写 domain 分析正文
- Lead 不得代替 `synthesizer` 产出最终整合
- 若出现“流程太重，直接分析”，视为协议违规并回滚到最近合法状态

## 7) 最小 LAUNCH_EVIDENCE

进入 `RUNNING` 前，Lead 必须能给出：

```json
{
  "launch_mode": "team_launch",
  "launch_method": "team_api|platform_nl_team_invocation",
  "team_name": "xxx",
  "selected_domains": ["..."],
  "active_core_members": ["obstruction-theorist", "synthesizer"],
  "core_ready_ack": {
    "OBSTRUCTION_CORE_READY_ACK": true,
    "SYNTHESIZER_CORE_READY_ACK": true
  }
}
```

## 8) Obstruction -> Synthesizer 时序

1. Domain Round 1 先提交给 obstruction + synthesizer（双投递，双 ACK）
2. Obstruction 必须至少完成一轮审查并回 `OBSTRUCTION_ROUND1_COMPLETE`
3. 若存在 `REVISE/REJECT`，先修正再复审
4. 仅当 `OBSTRUCTION_GATE_CLEARED` 后，Lead 才能发 `FINAL_SYNTHESIS_REQUEST`

Domain 文件读取约束（适用于 Swarm/Fallback）：

- 先读 skill 内 `references/` 绝对路径
- 仅绝对路径不可读时再回退 `references/...` 相对路径
- 禁止先在当前项目工作目录搜索同名 `references/`

## 9) 失败分支（保留最小集合）

- `PROTOCOL_BREACH_INITIAL_TASK_LAUNCH`: 首批被 Lead 逐个 Task 启动
- `PROTOCOL_BREACH_INVALID_FALLBACK_REASON`: Team 可用却非法降级
- `PROTOCOL_BREACH_CORE_NOT_READY`: 未收齐 core 双 ACK
- `PROTOCOL_BREACH_DOMAIN_BEFORE_CORE_READY`: core 未就绪先跑 domain
- `PROTOCOL_BREACH_LEAD_SOLO_ANALYSIS`: Lead 自行分析或代替 core
- `PROTOCOL_BREACH_PARTIAL_ATOMIC_LAUNCH`: 首批 roster 未一次完整拉起
- `PROTOCOL_BLOCKED_TEAM_LAUNCH_UNAVAILABLE`: 团队级启动能力确实不可用

## 10) 一页执行清单

1. `TeamCreate`
2. 解析 A/B/C
3. 组装首批 roster（core + all selected domains）
4. 一次团队级首批启动
5. Core ping + 双 ACK
6. 进入 `RUNNING`
7. Domain 双投递 + 双 ACK
8. Obstruction 一轮审查
9. Gate cleared 后请求 final synthesis
