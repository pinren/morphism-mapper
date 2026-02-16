---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.7 Swarm Mode。用于复杂问题的跨领域并行推理：TeamCreate 探测、团队级启动语义（不依赖固定工具名）、Domain 严格 JSON 输出、Obstruction 审查、Synthesizer 交换图整合。适用于“多领域交叉验证/策略转型/复杂系统诊断”等问题。
---

# Morphism Mapper v4.7（简化版）

本版本目标：**降低提示词复杂度，保留硬约束**。  
只保留一套协议与最小门禁，不再堆叠重复规则。

## 0. 先读哪几个文件

1. 启动协议（唯一真相）  
   `references/docs/bootstrap_contract.md`
2. Team Lead prompt  
   `assets/agents/system_prompts/leader.md`
3. Domain/Synthesizer/Obstruction prompts  
   `assets/agents/system_prompts/domain_template.md`  
   `assets/agents/system_prompts/synthesizer.md`  
   `assets/agents/system_prompts/obstruction.md`
4. 输出 schema  
   `assets/agents/schemas/domain_mapping_result.v1.json`

## 1. 最小执行流程（必须）

1. `TeamCreate(team_name=...)`
2. 分支判定：
   - 成功 -> `TEAM_READY`
   - `Already leading team XXX` -> 复用 `XXX`
   - `Feature not available` -> `FALLBACK`
3. 选领域并构建首批 roster：`core + all selected domains`
4. 一次团队级首批启动（团队级语义，不要求出现特定工具名）
5. Core 双 ACK：
   - `OBSTRUCTION_CORE_READY_ACK`
   - `SYNTHESIZER_CORE_READY_ACK`
6. 注入 `CATEGORY_SKELETON`
7. Domain agents 输出严格 JSON，双投递并收双 ACK
8. Obstruction Round1 完成并给 gate 结论
9. `OBSTRUCTION_GATE_CLEARED` 后触发 final synthesis
10. Synthesizer 交付最终整合

## 2. 六个不可破坏规则

1. TeamCreate 成功后，禁止非法降级 FALLBACK。
2. 首批必须是团队级原子启动，不能逐个 Task 拉人。
3. `Task(..., team_name, subagent_type)` 仍是单成员，不等于团队级启动。
4. Core 双 ACK 前禁止启动 domain 分析流程。
5. Lead 只编排，不能代替 synthesizer/obstruction 干活。
6. 禁止用“工具列表里看不到 AgentTeam”作为降级或改道依据。

## 3. 输出协议（Domain）

Domain Agent 只允许输出 `domain_mapping_result.v1` JSON，且至少满足：

- `schema_version`
- `domain_file_path`
- `domain_file_hash`
- `evidence_refs`（覆盖 `Fundamentals/Core Morphisms/Theorems`）
- `objects_map`
- `morphisms_map`
- `theorems_used`
- `kernel_loss`（对象，非标量）
- `strategy_topology`

缺任一项，视为无效结果。

## 4. 角色分工（最小定义）

- `team-lead`：流程推进、状态管理、催办与仲裁
- `domain-agent-*`：单域映射 JSON
- `obstruction-theorist`：schema gate + 风险审查 + clear 条件
- `synthesizer`：交换图校验 + final synthesis

## 5. ACK 握手（必须）

### 5.1 Core ACK

- Obstruction 和 Synthesizer 各回一条 `*_CORE_READY_ACK`

### 5.2 Delivery ACK

每个 domain JSON 都需要：

- `OBSTRUCTION_ACK_RECEIVED`
- `SYNTHESIZER_ACK_RECEIVED`

超时要重发一次并向 Lead 报告 `DELIVERY_ACK_TIMEOUT`。

### 5.3 Gate ACK

- Obstruction 必须发 `OBSTRUCTION_ROUND1_COMPLETE`
- clear 时必须附 `clear_summary`，不能只说 “clear”

## 6. 团队级启动语义说明

Morphism Mapper 以“行为证据”判定团队级启动，不以工具名判定：

- 平台可用 `TeamCreate` 并返回可用状态
- 首批一次性覆盖 `core + selected domains`
- 产生可追踪的 `LAUNCH_EVIDENCE`
- 收齐 core 双 ACK

可选实现形态包括：

- 显式团队 API（如存在）
- 平台 in-process 的自然语言 team 启动

判断是否合规，不看 UI 文案（如 `Task agents launched`），只看证据链。

## 7. Fallback（仅在 Team 不可用时）

仅当 TeamCreate 返回 Team 能力不可用（如 `Feature not available`）时进入。  
进入后遵循：

`references/docs/simulation_mode_guide.md`

注意：Fallback 是兜底，不是便捷模式。

## 8. 常用脚本

### 8.1 领域文件校验

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_domains.py
```

### 8.2 Domain JSON 校验

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_mapping_json.py /path/to/domain_result.json
```

### 8.3 动态生成 Domain Prompt

```python
from scripts.dynamic_agent_generator import DynamicAgentGenerator

g = DynamicAgentGenerator()
prompt = g.generate_base_prompt("game_theory")
```

## 9. 新增领域（精简）

1. 新建文件：`references/custom/<domain>_v2.md`
2. 必须包含四段：
   - `Fundamentals`
   - `Core Objects`
   - `Core Morphisms`
   - `Theorems`
3. 跑 `validate_domains.py`

## 10. 协议违规码（保留最小集）

- `PROTOCOL_BREACH_INITIAL_TASK_LAUNCH`
- `PROTOCOL_BREACH_INVALID_FALLBACK_REASON`
- `PROTOCOL_BREACH_PARTIAL_ATOMIC_LAUNCH`
- `PROTOCOL_BREACH_CORE_NOT_READY`
- `PROTOCOL_BREACH_DOMAIN_BEFORE_CORE_READY`
- `PROTOCOL_BREACH_LEAD_SOLO_ANALYSIS`
- `PROTOCOL_BLOCKED_TEAM_LAUNCH_UNAVAILABLE`

## 11. 实操模板（Lead 的最短话术）

```text
Step 0: TeamCreate 探测
Step 1: 构建 selected_domains
Step 2: 一次团队级首批启动（core + all selected domains）
Step 3: 收 core 双 ACK
Step 4: 广播 CATEGORY_SKELETON
Step 5: 等待 domain 双投递 + 双 ACK
Step 6: 等 obstruction round1 + gate clear
Step 7: 请求 synthesizer final synthesis
Step 8: 汇总交付
```

## 12. 版本来源

- 单一版本源：`assets/version.json`
- 其他文档不再各自维护独立版本号语义
