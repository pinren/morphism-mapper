# Morphism Mapper

> 基于范畴论的跨领域结构映射 Skill（Swarm Experimental）

[![Version](https://img.shields.io/badge/version-v4.7.0-green.svg)](https://github.com/pinren/morphism-mapper/releases)
[![Domains](https://img.shields.io/badge/domains-35%2B-orange.svg)](#领域覆盖)

## TL;DR

Morphism Mapper 现在是一个可执行的跨域推理协议，不再只是“类比提示词”：

- 启动协议单一真相：`references/docs/bootstrap_contract.md`
- Team 启动路径固定：`TeamCreate` 探测 + `AgentTeam` 首批原子启动
- Domain Agent 输出固定：`domain_mapping_result.v1` 严格 JSON
- 可审计数据流：强制 `domain_file_path` + `domain_file_hash` + `evidence_refs`
- 可计算整合：Synthesizer 基于结构化字段做交换图校验（Commutativity）

版本唯一来源：`assets/version.json`

## 适用场景

- 复杂问题需要多领域并行拆解
- 需要明确“共识结论 vs 条件分歧”，而不是平均化折中
- 希望输出可被程序校验、可追溯、可复盘

典型触发语句：

- “看不穿这个商业模式”
- “环境变了，策略怎么转型”
- “这个方案如何落地，风险在哪里”
- “做一次多领域交叉验证”

## 核心能力（v4.7）

### 1) Bootstrap Contract（启动协议统一）

状态机固定为：

`INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> RUNNING -> (可选) FALLBACK`

关键规则：

- `INIT` 只允许 `TeamCreate(team_name=...)`
- 首批成员必须通过 `AgentTeam(...)` 一次性启动
- `RUNNING` 才允许增量 `Task(..., description=..., team_name=...)`
- `Already leading team XXX` 视为可用并复用 team
- 只有 `Feature not available` 才允许降级 FALLBACK

参考：`references/docs/bootstrap_contract.md`

### 2) 严格 JSON 输出协议

Domain Agent 唯一有效输出是：

- Schema: `assets/agents/schemas/domain_mapping_result.v1.json`
- 必填字段包括：
  - `objects_map`, `morphisms_map`, `theorems_used`
  - `kernel_loss`, `strategy_topology`, `confidence`
  - `domain_file_path`, `domain_file_hash`, `evidence_refs`

### 3) 领域文件审计链路

每个 Domain Agent 必须：

1. 读取 `references/{domain}_v2.md`（或 `references/custom/...`）
2. 输出该文件的 `sha256` 到 `domain_file_hash`
3. 提供 `evidence_refs` 证明映射依据来自领域文件（必须覆盖 `Fundamentals/Core Morphisms/Theorems`）

### 4) 交换图校验与非交换分歧处理

Synthesizer 只消费结构化 JSON，计算：

- `FULLY_COMMUTATIVE` / `LOCALLY_COMMUTATIVE` / `NON_COMMUTATIVE`
- 非交换时不和稀泥，输出 bifurcation 场景并触发 obstruction alert

## 架构概览

- `team-lead`：流程驱动、状态推进、会议召集
- `obstruction-theorist`：Schema Gate + 五维十四式审查
- `synthesizer`：交换图校验、Limit/Colimit 提炼
- `domain-agents (N)`：单域映射，严格 JSON 交付

通信规则：仅 `SendMessage`。

## 环境要求

### Claude Code

- Claude Code 2.1.34+
- 启用 Agent Teams

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

### OpenCode

- 支持同一 skill 目录结构
- 安装后重启 OpenCode

## 安装

### Claude Code

```bash
cd ~/.claude/skills
git clone -b swarm-experimental https://github.com/pinren/morphism-mapper.git
```

### OpenCode

```bash
cd ~/.config/opencode/skills
git clone https://github.com/pinren/morphism-mapper.git
```

## 使用方式

直接描述问题即可触发。

示例：

- “我们业务增长停滞，但组织越来越重，怎么破局？”
- “从多领域分析这个转型策略，给我可执行方案和风险边界。”

你也可以在对话里明确要求：

- “用 swarm 模式”
- “要交换图校验和分歧场景”
- “输出可审计 JSON 结果”

## 领域覆盖

- 内置领域：35（`references/*_v2.md`）
- 自定义领域：放在 `references/custom/*_v2.md`
- 当前仓库可用领域总数（含 custom）可通过校验脚本自动统计

## 新增领域

### 路径 A：手工新增

1. 在 `references/custom/` 新建 `<domain>_v2.md`
2. 遵循 V2 结构：`Fundamentals / Core Objects / Core Morphisms / Theorems`
3. 重新运行领域校验脚本

### 路径 B：运行时补盲（auto_create）

`DynamicAgentGenerator` 支持在领域缺失时返回生成指令，供 Team Lead 补盲后继续流程。

核心实现：`scripts/dynamic_agent_generator.py`

## 质量门禁与测试

### 1) 领域文件健康检查

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_domains.py
```

检查项包括：

- 必要章节存在
- 基本条目数量下限
- `extract_knowledge` 可解析

### 2) Parser 单元测试

```bash
cd ~/.claude/skills/morphism-mapper
python3 -m unittest scripts.tests.test_domain_parser
```

### 3) 映射结果 Schema 校验

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_mapping_json.py /path/to/mapping.json
```

## 端到端实战示例

下面用一个真实流程演示从输入到最终结果的最短路径。

### Step 1: 用户输入

在 Claude/OpenCode 中直接输入：

```text
请用 swarm 模式分析：我们业务增长停滞，但组织越来越重，给出可执行转型策略、风险边界和分歧场景。
```

### Step 2: Team Lead 启动分支（Bootstrap Contract）

预期状态推进：

```text
INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> RUNNING
```

关键检查：

1. 必须先执行 `TeamCreate(team_name=...)`
2. `Already leading team XXX` 视为可用并复用 `XXX`
3. 首批成员必须用一次 `AgentTeam(...)` 原子启动
4. 首批 `launch_roster` 必须同时包含 `obstruction-theorist` 与 `synthesizer`
5. Team Lead 不得代替 `synthesizer` 做最终整合
6. 若 Synthesizer 延迟/未响应，Lead 只能催促与升级，不得直接输出最终报告

### Step 3: Domain Agent 产出严格 JSON

每个 Domain Agent 都应发送 `MAPPING_RESULT_JSON`（或 `MAPPING_RESULT_ROUND1`）并包含完整 schema 字段。示例：

```json
{
  "schema_version": "domain_mapping_result.v1",
  "domain": "game_theory",
  "domain_file_path": "references/game_theory_v2.md",
  "domain_file_hash": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "evidence_refs": [
    {"section": "Fundamentals", "quote_or_summary": "博弈主体在约束中追求收益最大化。"},
    {"section": "Core Morphisms", "quote_or_summary": "策略变化是对对手动作的条件响应。"},
    {"section": "Theorems", "quote_or_summary": "纳什均衡定义稳定策略组合。"}
  ],
  "objects_map": [
    {"a_obj": "业务单元", "b_obj": "博弈主体", "rationale": "都在竞争与合作约束中做策略选择。"}
  ],
  "morphisms_map": [
    {"a_mor": "组织调整", "b_mor": "策略偏移", "dynamics": "结构变化改变收益矩阵与行动空间。"}
  ],
  "theorems_used": [
    {"id": "T1", "name": "纳什均衡", "mapping_hint_application": "识别稳定但低效均衡点并设计破局动作。"},
    {"id": "T2", "name": "重复博弈", "mapping_hint_application": "用长期激励约束短期机会主义行为。"}
  ],
  "kernel_loss": {
    "lost_nuances": [
      {"element": "情绪因素", "description": "经典理性模型无法完整表达组织情绪扩散。", "severity": "MEDIUM"}
    ],
    "preservation_score": 0.73
  },
  "strategy_topology": {
    "topology_type": "distributed_mesh",
    "core_action": "remove_bottleneck",
    "resource_flow": "recirculate",
    "feedback_loop": "negative_feedback",
    "time_dynamics": "continuous",
    "agent_type": "active_strategic"
  },
  "topology_reasoning": "通过去中心化协作和闭环反馈降低组织内耗并恢复流动性。",
  "confidence": 0.81
}
```

### Step 4: 本地门禁校验（建议）

把任一 Domain 输出保存为 JSON 文件后执行：

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_mapping_json.py /path/to/domain_result.json
```

期望结果是 `[OK] ...`。若缺 `domain_file_hash` 或 `kernel_loss`，应返回 `[FAILED]` 并列出缺失字段。

### Step 5: Obstruction 与 Synthesizer 收敛

1. Obstruction 先做 `Schema Gate`，再做风险分层审查（LOW/MEDIUM/HIGH）  
2. 至少等待 Obstruction Round 1 对全部 active domains 完成反馈后，才允许进入最终整合  
3. 若 Obstruction 要求二轮修正，先完成修正+复审，再触发最终整合  
4. Synthesizer 仅消费 JSON，计算交换图一致性并产出：
   - `commutative_diagram_report`
   - `limit`（跨域不变量）
   - `colimit`（分场景互补策略）

### Step 6: 最终交付

最终应包含三部分：

1. 共识策略（Limit）
2. 分歧场景与条件策略（Colimit + bifurcation）
3. 风险容器与落地边界（来自 Obstruction + kernel_loss 汇总）

职责边界：最终整合结论必须由 `synthesizer` 产出，Lead 只做流程协调与发布。

## 关键文件索引

### 协议与版本

- `assets/version.json`
- `references/docs/bootstrap_contract.md`
- `assets/agents/schemas/domain_mapping_result.v1.json`

### 核心 prompts

- `assets/agents/system_prompts/leader.md`
- `assets/agents/system_prompts/obstruction.md`
- `assets/agents/system_prompts/synthesizer.md`
- `assets/agents/system_prompts/domain_template.md`

### 核心脚本

- `scripts/domain_selector.py`
- `scripts/dynamic_agent_generator.py`
- `scripts/validate_domains.py`
- `scripts/validate_mapping_json.py`

### 参考文档

- `SKILL.md`
- `references/docs/DOMAIN_AGENT_GUIDE.md`
- `references/docs/simulation_mode_guide.md`

## 常见问题

### Q1: 什么时候会进入 FALLBACK？

仅当 `TeamCreate` 返回 Team 能力不可用（例如 `Feature not available`）。

### Q2: `Already leading team XXX` 算失败吗？

不算。应复用 `XXX` 并继续 Agent Swarm。

### Q3: 可以只发摘要给 Synthesizer 吗？

不可以。v4.7 统一为结构化 JSON 主体，缺字段即拒收。

### Q4: 为什么必须带 `domain_file_hash`？

为了证明结果确实来自指定领域文件，防止“未读文件的泛化输出”。

## 版本说明

当前：`v4.7.0`（2026-02-15）

本版重点：

- 协议统一（Bootstrap Contract）
- 输出统一（domain_mapping_result.v1）
- 审计统一（domain_file_hash + evidence_refs）

更多细节见：`SKILL.md` 的版本历史。
