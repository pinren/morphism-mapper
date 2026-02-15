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
| `RUNNING` | 蜂群已运行 | `SendMessage`；增量 `Task(..., team_name=...)` | 创建无 `team_name` 的独立 Task |
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
- 仅在 `RUNNING` 的增量扩展场景，才允许 `Task(..., team_name=...)` 添加新成员。

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

# MEMBERS_READY -> RUNNING
AgentTeam(team_name=team_name, members=launch_roster, shared_context=shared_context)

# RUNNING (incremental only)
Task(name="new-domain-agent", prompt=prompt, team_name=team_name)
```

## 6. 错误分支

- 无法解析 `Already leading team` 的 team 名称：中止并请求用户确认，不允许猜测。
- `AgentTeam` 原子启动失败：记录失败成员并整体重试，不允许回退为首批 `Task` 逐个启动。
- 增量 Task 未传 `team_name`：视为严重协议违规。
