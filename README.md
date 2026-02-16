# Morphism Mapper

> 基于范畴论的跨领域推理 Skill（Swarm Experimental）

[![Version](https://img.shields.io/badge/version-v4.7.0-green.svg)](https://github.com/pinren/morphism-mapper/releases)
[![Schema](https://img.shields.io/badge/schema-domain_mapping_result.v1-blue.svg)](./assets/agents/schemas/domain_mapping_result.v1.json)

## 这次重构做了什么

目标只有一个：**把提示系统简化成一套最小可执行协议**。

- 删除重复规则与多处“同义不同文案”
- 启动逻辑只认一个文件：`references/docs/bootstrap_contract.md`
- Lead prompt 改为短版：只保留状态机、门禁、ACK
- Domain/Obstruction/Synthesizer prompts 改为短版
- `SKILL.md` 从超长手册收敛为可执行清单

## 核心机制（简化后）

1. Team 探测：`TeamCreate`
2. 首批启动：一次团队级启动（语义判定，不依赖固定工具名）
3. Core 就绪：必须收齐双 ACK
4. Domain 输出：严格 JSON schema
5. Obstruction 先审：通过后才能 final synthesis
6. Synthesizer 负责最终整合，Lead 不代劳

## 状态机

`INIT -> TEAM_PROBED -> TEAM_READY -> MEMBERS_READY -> CORE_READY -> RUNNING -> (可选) FALLBACK`

详见：`references/docs/bootstrap_contract.md`

## 团队级启动说明

“团队级启动”看行为证据，不看是否出现 `AgentTeam` 这个工具名。
在 in-process 模式下，平台可能以托管任务形式展示启动过程。

以下都不算：

- Lead 逐个 `Task(...)` 拉人
- `Task(..., team_name, subagent_type)` 伪装团队启动
- 先 core 再 domain 的分批首发

## 目录结构（关键）

```text
morphism-mapper/
├── SKILL.md
├── assets/
│   ├── version.json
│   └── agents/
│       ├── schemas/domain_mapping_result.v1.json
│       └── system_prompts/
│           ├── leader.md
│           ├── domain_template.md
│           ├── obstruction.md
│           └── synthesizer.md
├── references/
│   ├── docs/bootstrap_contract.md
│   ├── docs/simulation_mode_guide.md
│   ├── *_v2.md
│   └── custom/*_v2.md
└── scripts/
    ├── dynamic_agent_generator.py
    ├── validate_domains.py
    └── validate_mapping_json.py
```

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

## 使用

直接提问复杂问题即可，例如：

- “请用多领域分析我们的增长停滞问题，给出策略和风险边界。”
- “不要单学科答案，要能指出一致结论和冲突结论。”

## Domain 输出契约（必须）

schema: `assets/agents/schemas/domain_mapping_result.v1.json`

关键必填字段：

- 读取顺序：先 skill 内 `references/` 绝对路径，再回退相对 `references/...`（禁止先查项目 cwd）
- `schema_version`
- `domain_file_path`
- `domain_file_hash`
- `evidence_refs`（覆盖 `Fundamentals/Core Morphisms/Theorems`）
- `objects_map`
- `morphisms_map`
- `theorems_used`
- `kernel_loss`（对象，不可标量）
- `strategy_topology`

## 质量门禁脚本

### 校验领域文件

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_domains.py
```

### 校验 domain JSON

```bash
cd ~/.claude/skills/morphism-mapper
./scripts/validate_mapping_json.py /path/to/domain_result.json
```

## FAQ（精简）

### Q1: TeamCreate 成功后还能降级 Fallback 吗？

不能。只有 Team 能力不可用（例如 `Feature not available`）才允许。

### Q2: UI 出现 `Task agents launched` 算违规吗？

不一定。以协议证据判定：是否一次性覆盖首批 roster、是否有 `LAUNCH_EVIDENCE`、是否有 core 双 ACK。

### Q3: obstruction clear 只回一个 “clear” 可以吗？

不可以。必须带 `clear_summary`（通过域、修正域、残余风险、最终条件）。

### Q4: Lead 可不可以赶时间直接整合？

不可以。Lead 只能编排，final synthesis 只能由 synthesizer 产出。

### Q5: `Task(..., team_name, subagent_type)` 能否当团队启动？

不能。这仍是单成员启动。

### Q6: 看不到 `AgentTeam` 工具名，是不是就不能走 Swarm？

不是。不要按工具名推断。以 `TeamCreate` 返回、首批团队级启动证据、core 双 ACK 判定。

## 版本

- 单一版本源：`assets/version.json`
