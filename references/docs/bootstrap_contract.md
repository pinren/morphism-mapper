# Bootstrap Contract (Single Source of Truth)

> 本文件是 Morphism Mapper 启动协议唯一真相。  
> 若 `SKILL.md`、`leader.md`、其他文档与本文件冲突，以本文件为准。

## 1. 状态机

`INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> RUNNING -> (可选) FALLBACK`

## 2. 状态定义与允许 API

| 状态 | 含义 | 允许 API | 禁止行为 |
|---|---|---|---|
| `INIT` | 尚未探测 Team 能力 | `TeamCreate(team_name=...)` | 直接 `Task` 拉核心成员；直接降级 |
| `TEAM_PROBED` | 已拿到 TeamCreate 返回 | 解析返回并做分支判定 | 跳过分支判定 |
| `TEAM_READY` | Team 能力可用，且 team_name 已确定 | 构建首批成员名册 | 用 `Task` 逐个拉首批成员 |
| `MEMBERS_READY` | 首批成员（Core + 首轮 Domain）名册已构建 | `AgentTeam(team_name, members, shared_context)` | 分批启动首批成员 |
| `RUNNING` | 蜂群已运行 | `SendMessage`；增量 `Task(..., description=..., team_name=...)` | 创建无 `description` 或无 `team_name` 的 Task |
| `FALLBACK` | Team 能力不可用 | 单 AI 顺序执行（参见 `simulation_mode_guide.md`） | 调用 `TeamCreate`/`AgentTeam`/Team `Task` |

## 3. TeamCreate 分支判定（必须）

1. **Case A: TeamCreate 成功**  
   进入 `TEAM_READY`，使用返回的 `team_name`。

2. **Case B: 返回 `Already leading team XXX`**  
   进入 `TEAM_READY`，复用 `XXX` 作为 `team_name`。这不是失败。

3. **Case C: 返回 `Feature not available` 或等效不可用错误**  
   进入 `FALLBACK`，禁止继续 Team API。

## 4. 首批启动规则

- 首批成员（`obstruction-theorist`、`synthesizer`、首轮 Domain Agents）必须一次性由 `AgentTeam` 原子启动。
- 仅在 `RUNNING` 的增量扩展场景，才允许 `Task(..., description=..., team_name=...)` 添加新成员。

### 4.1 核心成员硬约束（不可跳过）

- `launch_roster` 必须同时包含 `obstruction-theorist` 与 `synthesizer`。
- 若任一核心成员缺失，禁止进入 `RUNNING`。
- 禁止 Team Lead 自行执行跨域整合；整合职责只属于 `synthesizer`。

## 5. 最小执行模板

```python
# INIT
probe = TeamCreate(team_name="morphism-{timestamp}")

# TEAM_PROBED -> TEAM_READY
if probe.ok:
    team_name = probe.team_name
elif "Already leading team" in probe.error:
    team_name = extract_team_name(probe.error)
elif "Feature not available" in probe.error:
    goto_fallback()
else:
    raise RuntimeError("Unrecognized TeamCreate result")

# TEAM_READY -> MEMBERS_READY
launch_roster = [obstruction_member, synthesizer_member] + domain_members

if not has_member(launch_roster, "obstruction-theorist") or not has_member(launch_roster, "synthesizer"):
    raise RuntimeError("Core roster incomplete: obstruction-theorist + synthesizer are required")

# MEMBERS_READY -> RUNNING
AgentTeam(team_name=team_name, members=launch_roster, shared_context=shared_context)

# RUNNING (incremental only)
Task(
    name="new-domain-agent",
    description="Incremental domain analysis task",
    prompt=prompt,
    team_name=team_name
)
```

## 6. 错误分支

- 无法解析 `Already leading team` 的 team 名称：中止并请求用户确认，不允许猜测。
- `AgentTeam` 原子启动失败：记录失败成员并整体重试，不允许回退为首批 `Task` 逐个启动。
- 增量 Task 未传 `description` 或 `team_name`：视为严重协议违规。
- Synthesizer 未按时返回：只允许 `SendMessage` 催促与升级，不允许 Team Lead 直接产出最终整合报告。

## 7. Obstruction -> Synthesizer 时序门禁（必须）

- Domain Round 1 JSON 产出后，必须先进入 Obstruction Round 1。
- `obstruction_round1_coverage = reviewed_domains / active_domains`。
- 当 `obstruction_round1_coverage < 100%` 时，禁止触发 `FINAL_SYNTHESIS_REQUEST`。
- 若任一域被判定 `REVISE/REJECT`，必须先完成修正轮并复审，再考虑最终整合。
- 仅当 active domains 全部通过 Obstruction（`PASS`）或被显式剔除并记录原因，才允许 `OBSTRUCTION_GATE_CLEARED`。

## 8. 堵点提效策略（标准流程）

- Obstruction 先执行 Stage A 批量 Schema Gate，快速筛出 `SCHEMA_BLOCKER`。
- 再执行 Stage B 风险分层：`LOW/MEDIUM/HIGH`，按风险决定审查深度。
- Synthesizer 可在 `OBSTRUCTION_ROUND1_COMPLETE` 后做 `PRELIMINARY_SYNTHESIS` 草稿计算。
- 最终结论（Limit/Colimit + verdict）必须等 `OBSTRUCTION_GATE_CLEARED` 后输出。

## 9. Synthesizer 阻塞恢复（必须）

- Lead 发送 `FINAL_SYNTHESIS_REQUEST` 后，若未收到 `SYNTHESIS_RESULT_JSON`：
  - `T+2min` 发送第一次提醒
  - `T+5min` 发送第二次提醒并声明阻塞
  - `T+10min` 触发 `DECISION_MEETING_REQUEST`
- 恢复前，系统状态保持为 `RUNNING`，并标记 `SYNTHESIS_BLOCKED`。
- 任何情况下都不得由 Lead 代替 Synthesizer 或 Obstruction 输出最终结论。

## 10. 投递 ACK 握手（必须）

- Domain 每次发送映射结果都必须带 `message_id`，并同时发给 Obstruction 与 Synthesizer。
- Obstruction 收到后必须回：
  - 给 Domain：`OBSTRUCTION_ACK_RECEIVED`
  - 给 Lead：`OBSTRUCTION_DELIVERY_ACK`
- Synthesizer 收到后必须回：
  - 给 Domain：`SYNTHESIZER_ACK_RECEIVED`
  - 给 Lead：`SYNTHESIZER_DELIVERY_ACK`
- Lead 必须维护每个域的 ACK 矩阵；若 90s 未齐全，触发重发与催促。
- 未完成 ACK 握手的域不得计入“已送达/可审查”。
