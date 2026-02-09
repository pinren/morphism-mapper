---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.4 Swarm Mode - 基于范畴论的跨领域并行探索系统。通过多 Agent Team 并行分析，将 Domain A 的问题结构映射到多个远域 Domain B，借助跨域共识（Limits）和互补整合（Colimits）生成非共识创新方案。**⚠️ 蜂群模式是本技能的正确打开姿势**，避免使用并行 Task Pool 模式。支持领域知识管理（新增自定义领域）。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"增加易经思想领域"等。v4.4 核心升级：合并Lead+Broadcaster职责，优化第一轮信息流分层发送。
---

# Category Theory Morphism Mapper v4.4 🐝

基于范畴论的函子映射逻辑，通过**蜂群模式**将 Domain A 的问题结构并行映射到多个远域 Domain B，借助跨域共识生成创新方案。

**版本**: v4.4.1 (Swarm Mode - 合并Lead+Broadcaster，优化信息流 + 范畴骨架注入标准)
**更新日期**: 2026-02-09
**领域数量**: 31个内置领域

**v4.4 核心升级**:
- 🎯 **架构简化**: Team Lead 合并 Yoneda Broadcaster 职责（范畴提取 + 团队协调）
- 🔧 **第一轮信息流分层**: Domain Agent → Obstruction（完整）+ Synthesizer（一句话洞察）
- 🔧 **Obstruction诊断简报**: 30字风险预警发送给Synthesizer
- 🔧 **按需审查机制**: Synthesizer仅在明显不满时向Obstruction征求进一步意见
- 🔧 **删除broadcaster角色**: 不再需要独立的Yoneda Broadcaster
**领域版本**: V2（100基本基石 + 14 Objects + 14 Morphisms + 18 Theorems）
**核心架构**: Agent Team 协作模式（Team Lead + Domain Agents + Obstruction Theorist + Synthesizer）

## 核心原理

1. **Object Preservation**: 识别 Domain A 核心实体
2. **Morphism Preservation**: 识别实体间动态关系
3. **Composition Consistency**: 映射结果可拉回并保持逻辑闭环
4. **Swarm Intelligence**: 多 Agent 并行探索，跨域共识验证

## ⚠️ 重要：蜂群模式是正确打开姿势

**🚨 常见错误警告**：

```
❌ 错误做法 1: 先单独运行 Yoneda Broadcaster，再创建团队
→ 这样 Yoneda Broadcaster 不是 teammate，无法使用 SendMessage

❌ 错误做法 2: 创建团队后只启动 Domain Agents
→ 缺少 Obstruction Theorist 和 Synthesizer，无法完成流程

❌ 错误做法 3: 顺序启动核心成员
→ 应该同时启动，让它们并行工作

❌ 错误做法 4: 决策会议时创建新的 Task(name="team-lead")
→ 这会创建第二个 team-lead，导致重复
→ ✅ 正确做法：已存在的 Team Lead 通过 SendMessage 通信触发会议
```

**✅ 正确做法**：

```
✅ Step 1: TeamCreate() → 自动创建 team-lead（leadAgentId）
✅ Step 2: 只需启动 obstruction-theorist + synthesizer
✅ Step 3: Team Lead 提取范畴骨架并调用 domain_selector.py
✅ Step 4: Team Lead 启动 Domain Agents
✅ Step 5: Team Lead 自动触发决策会议
```

**🔴 关键记忆点**:
```
TeamCreate(team_name="xxx")
    ↓
自动创建: team-lead@xxx (作为 leadAgentId)
    ↓
❌ 错误: Task(name="team-lead") → 创建 team-lead-2（重复！）
✅ 正确: 只创建 obstruction-theorist + synthesizer
```

---

## 蜂群模式 vs 并行 Task Pool 模式

**Morphism Mapper v4.0 采用蜂群模式，而非并行 Task Pool 模式**：

```
✅ 正确方式：Agent Team 协作
- 使用 TeamCreate 创建团队
- 使用 Task 工具启动 teammates（带 team_name 参数）
- Teammates 通过 SendMessage 相互通信
- Synthesizer 进行跨域整合

❌ 错误方式：并行 Task Pool
- 使用 Task 工具启动多个独立 general-purpose agents
- 没有团队协作机制
- 无法实现真正的跨域共识计算
```

## 🚨 CRITICAL: v4.4 重大升级 - 架构简化与信息流优化

### 问题背景

在 v4.3 执行中，发现架构冗余问题：
- **问题**: Yoneda Broadcaster 和 Team Lead 职责有重叠，都是负责第一阶段的信息提取和协调
- **冗余**: 第一轮 Domain Agent 完成后需要向两个人发送完整报告（Obstruction + Synthesizer），信息流不够分层
- **后果**: 信息传递效率低，Synthesizer 需要处理大量冗余信息

### v4.4 简化解决方案

**核心原则**: Team Lead 合并 Yoneda Broadcaster 职责，信息流分层优化

**强制要求**:
1. **Team Lead 职责合并**: Team Lead 负责范畴提取 + 团队协调，不再需要独立的 Yoneda Broadcaster
2. **第一轮信息流分层**: Domain Agent → Obstruction（完整报告）+ Synthesizer（一句话洞察）
3. **Obstruction诊断简报**: Obstruction 发送30字风险预警给 Synthesizer
4. **按需审查机制**: Synthesizer 仅在明显不满时向 Obstruction 征求进一步意见

---

## 🚨 CRITICAL: 智能领域选择是核心机制

**⚠️ domain_selector.py 是 Morphism Mapper v4.1 的核心组件，不能跳过！**

### 工作原理

```
用户问题 (Domain A)
    ↓
Team Lead 提取结构骨架（合并了原 Yoneda Broadcaster 职责）
    ↓
domain_selector.py 分析结构特征
    ↓
匹配 16 个动态标签 + 31 个领域
    ↓
按 Tier Balance 筛选 Top 3-5
    ↓
动态生成 Domain Agent teammates
    ↓
【关键】Team Lead 显式注入范畴骨架给每个 Agent
```

### 结构特征 → 标签映射

domain_selector.py 通过分析 Domain A 的 Morphisms 动态描述，自动提取 16 个核心动态标签：

| 标签 | 匹配关键词 | 相关领域 |
|------|----------|---------|
| `feedback_regulation` | 反馈、调节、控制 | control_systems, thermodynamics |
| `flow_exchange` | 流动、交换、传播 | network_theory, information_theory |
| `competition_conflict` | 竞争、对抗、博弈 | game_theory, military_strategy |
| `cooperation_synergy` | 合作、协同、共生 | ecology, social_capital |
| `adaptation_learning` | 适应、学习、进化 | evolutionary_biology, complexity_science |
| `optimization_efficiency` | 优化、效率、最大化 | operations_research, behavioral_economics |
| `uncertainty_risk` | 不确定、风险、波动 | quantum_mechanics, antifragility |
| `emergence_pattern` | 涌现、模式、自组织 | complexity_science, network_theory |
| `equilibrium_stability` | 平衡、稳定、稳态 | thermodynamics, control_systems |
| `transformation_change` | 转化、变化、相变 | thermodynamics, zhuangzi |
| `information_encoding` | 信息、编码、符号 | information_theory, linguistics |
| `resource_allocation` | 资源、分配、配置 | game_theory, incentive_design |
| `constraint_limitation` | 约束、限制、边界 | operations_research, control_systems |
| `decomposition_composition` | 分解、组合、模块 | distributed_systems, network_theory |
| `selection_elimination` | 选择、淘汰、筛选 | evolutionary_biology, innovation_theory |
| `communication_signaling` | 通信、信号、传递 | information_theory, linguistics |

### Tier Balance 算法

筛选 Top 3-5 领域时强制执行层级平衡：

```
Tier 1 (公理化): 1-2 个
    └── 热力学、量子力学、控制理论等底层原理
    └── 提供坚实的理论基础

Tier 2 (应用): 2-3 个
    └── 博弈论、网络理论、复杂系统等应用框架
    └── 提供可操作的分析工具

Tier 3/4 (实践/阐释): 0-1 个
    └── 军事战略、庄子哲学等实践智慧
    └── 提供行动指导和哲学视角

Wildcard: 1 个随机领域
    └── 从非种子领域随机选择
    └── 确保非共识创新
```

### 代码调用示例

```python
# 必须调用 domain_selector.py
from scripts.domain_selector import DomainSelector

selector = DomainSelector()
result = selector.select_domains(
    objects=category_skeleton["objects"],
    morphisms=category_skeleton["morphisms"],
    user_profile=infer_user_profile(user_problem)
)

# 获取 Top 3-5 推荐
selected_domains = result["top_domains"][:3]

# 动态生成 Domain Agents
for domain_info in selected_domains:
    Task(
        subagent_type="general-purpose",
        team_name=f"morphism-swarm-{task_id}",
        name=f"{domain_info['domain']}-agent"
    )
```

### 禁止行为

```
❌ 硬编码 5 个领域（如 thermodynamics, game_theory, control_systems, complexity_science, network_theory）
❌ 跳过 domain_selector.py 直接选择领域
❌ 忽略 Tier Balance 算法
❌ 不使用 Wildcard Agent

✅ 必须基于问题结构特征动态选择
✅ 必须遵守 Tier Balance 层级平衡
✅ 必须包含 1 个 Wildcard Agent
```

### 验证检查点

执行完 domain_selector.py 后，检查：
- [ ] 用户标签是否正确提取？
- [ ] Top 3-5 领域是否包含不同 Tier？
- [ ] 是否有 1 个 Wildcard Agent？
- [ ] 置信度是否 > 70%？（低于阈值应触发 Swarm Mode）

## 使用方式

**直接描述问题**，系统自动启动 Swarm Mode：

```
用户: "婆媳矛盾怎么破"
→ 自动启动 Agent Team
→ 多领域并行分析
→ 三人小组决策是否迭代
→ 生成 Limit + Colimit 洞察
```

---

## 🐝 蜂群模式架构 (v4.4 - 合并Lead+Broadcaster，优化信息流)

**⚠️ 正确启动顺序（必须严格遵守）**：

```
Step 1: TeamCreate()
    ↓ 自动创建 team-lead (leadAgentId: team-lead@{team_name})
Step 2: 同时启动两个核心成员
    ├── Task("obstruction-theorist", team_name=...)
    └── Task("synthesizer", team_name=...)
    ↓
Step 3: Team Lead 提取范畴骨架并调用 domain_selector.py
    ↓
Step 4: Team Lead 启动 Domain Agents
    ↓
Step 5: Domain Agents 并行分析，发送分层报告
    ↓
Step 6: Team Lead 触发决策会议
    ↓
Step 7: 根据决策执行（迭代 or 终止）
```

**🔴 核心成员（有且只有一个）**:
| 角色 | 创建方式 | 创建时机 | 工作阶段 |
|------|---------|---------|---------|
| **Team Lead** | TeamCreate 自动 | Step 1 | 全流程协调 + 范畴提取 |
| **Obstruction Theorist** | Task(name="obstruction-theorist") | Step 2 | Phase 1-3: 实时审查 |
| **Synthesizer** | Task(name="synthesizer") | Step 2 | Phase 1-4: 整合 + 决策 |

```
┌─────────────────────────────────────────────────────────────┐
│       Morphism Mapper v4.4 Swarm Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 0: Team Lead (合并 Yoneda Broadcaster 职责)            │
│  └── 提取范畴骨架 (Objects + Morphisms + Tags)             │
│              ↓ 调用 domain_selector.py                       │
│  Phase 1: 智能领域选择 ⭐ (domain_selector.py)                │
│  └── 基于Morphism结构匹配选择 Top 3-5 领域                  │
│              ↓ 动态选择 Domain Agents                        │
│  Phase 2-3: Domain Agents + Obstruction Theorist (并行)     │
│  ├── Domain Agents (动态选择的领域并行分析)                  │
│  │   (根据问题特征自动匹配，而非固定5个)                     │
│  └── Obstruction Theorist (实时审查)                         │
│              ↓ 分层发送分析结果                              │
│  Phase 4: Synthesizer + 三人决策小组                         │
│  ├── Synthesizer 整合洞察                                   │
│  ├── 按需向 Obstruction 征求意见                             │
│  ├── 三人小组决策会议                                        │
│  └── 生成最终报告                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 三人决策小组职责

| 成员 | 主要职责 | 决策权重 | v4.4 升级 |
|------|---------|---------|----------|
| **Synthesizer** | 跨域整合、Limits/Colimits 计算、同构检测 | 40% | **按需审查机制** |
| **Obstruction Theorist** | 映射质量把关、结构性问题识别、风险预警 | 40% | 分层报告（完整+诊断） |
| **Team Lead** | 流程协调、资源分配、范畴提取、最终决策、用户沟通 | 20% | **合并范畴提取职责** |

**⚠️ v4.4 关键变更**:
- Team Lead 合并 Yoneda Broadcaster 职责，不再需要独立 broadcaster
- Domain Agent 第一轮报告分层：完整给 Obstruction，一句话洞察给 Synthesizer
- Obstruction 发送30字诊断简报给 Synthesizer
- Synthesizer 仅在明显不满时向 Obstruction 征求完整意见

---

## 🎯 三人小组迭代决策流程（v4.4 优化版）

### 🚨 强制触发机制

**触发时机**（满足任一即触发）：
1. ⏰ **时间触发**: 首轮分析完成（收到所有 MAPPING_RESULT）
2. 🚨 **阈值触发**: Obstruction 通过率 < 50%
3. 🔍 **信号触发**: 检测到强同构、高分歧、涌现新维度

**禁止行为**:
- ❌ Synthesizer 单方面决定终止分析
- ❌ Synthesizer 单方面决定不启动迭代
- ❌ 跳过决策会议直接生成报告

### 决策会议流程

```
┌─────────────────────────────────────────────────────────────┐
│              三人小组决策会议（强制触发）                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【Step 1】Synthesizer 发言                                  │
│  ├── 报告 Limits/Colimits 初步结果                          │
│  ├── 报告同构簇分析                                         │
│  ├── 报告 Dissensus 检测结果                                 │
│  └── 提议：需要迭代 or 终止？                                │
│                                                             │
│  【Step 2】Obstruction Theorist 发言                         │
│  ├── 报告 Obstruction 通过率                                 │
│  ├── 指出系统性问题或风险                                     │
│  ├── ⚠️ 通过率 < 50% 时：必须说明缺失的维度                   │
│  └── 建议引入的新领域                                         │
│                                                             │
│  【Step 3】Team Lead 发言                                   │
│  ├── 评估资源消耗和时间预算                                  │
│  ├── 考虑用户需求优先级                                       │
│  ├── 提出迭代建议或终止建议                                   │
│  └── ⚠️ 如需终止，必须说明理由                                  │
│                                                             │
│  【Step 4】投票决策                                          │
│  ├── 引入新领域? → 需要 2/3 多数同意                          │
│  ├── 深化现有 Agent? → 需要 2/3 多数同意                       │
│  ├── 终止分析? → 需要 2/3 多数同意                            │
│  └── 重大决策 → 需要一致同意                                  │
│                                                             │
│  【Step 5】记录决策结果                                      │
│  ├── 决策内容：迭代/终止                                     │
│  ├── 投票情况：谁支持谁反对                                   │
│  ├── 理由说明：为什么做出这个决策                             │
│  └── 后续行动：具体执行步骤                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 决策矩阵

| 决策维度 | Synthesizer 权重 | Obstruction 权重 | Team Lead 权重 | 通过阈值 |
|---------|-----------------|-------------------|---------------|---------|
| 同构强度是否足够? | 40% | 30% | 30% | 简单多数 (2/3) |
| **Obstruction 通过率是否可接受?** | **30%** | **40%** | **30%** | **<50% 必须讨论迭代** |
| 是否有新维度值得探索? | 40% | 20% | 40% | 简单多数 |
| 资源/时间是否允许? | 20% | 10% | 70% | 简单多数 |
| **终止分析?** | **20%** | **10%** | **70%** | **禁止单方面决定** |

---

## 🚨 v4.4 迭代触发条件（优化版）

### 触发条件 1: Obstruction 反馈 → 系统性问题 ⚠️ 强制触发

**判断标准**:
```python
if obstruction_pass_rate < 0.5:
    # ⚠️ 强制触发三人小组决策会议
    # Obstruction Theorist 必须说明具体缺失的维度
    missing_dimensions = obstruction_theorist.identify_gaps()

    # 讨论内容：
    # 1. 哪些维度被现有领域遗漏？
    # 2. 引入什么新领域可以补充？
    # 3. 是否启动 Round 2？
```

**强制要求**:
- Obstruction 通过率 < 50% **必须讨论**是否启动迭代
- Obstruction Theorist **必须建议**可能缺失的维度
- 讨论结果 **必须记录**

**示例决策**:
```
Obstruction: "所有科学框架都遗漏了政策维度"
建议: "引入 political_theory, public_policy"
Synthesizer: "同意，现有框架无法覆盖制度约束"
Team Lead: "同意，启动 Round 2"
→ 决策通过：引入 2 个政策分析领域
```

### 触发条件 2: 同构信号 → 需要验证

**判断标准**:
```python
if strong_homography_detected (≥3域使用相似结构):
    # 引入验证领域进行三角验证
elif weak_homography_detected (2域有相似视角):
    # 引入第3领域验证或证伪
```

**三人小组决策**:
- Synthesizer: 报告同构模式和强度
- Obstruction Theorist: 评估同构是否真实或表面相似
- Team Lead: 决定引入验证领域

### 触发条件 3: 高分歧 → 需要调解

**判断标准**:
```python
if dissensus_metric > 60:
    # 分歧过高，引入调解领域
```

**三人小组决策**:
- Synthesizer: 报告分歧的具体内容和原因
- Obstruction Theorist: 评估分歧是否是根本性的
- Team Lead: 决定引入调解领域或终止分析

### 触发条件 4: 涌现洞察 → 新维度

**判断标准**:
```python
if new_dimension_emerged:
    # 首轮分析揭示了之前未考虑的重要维度
```

**三人小组决策**:
- Synthesizer: 描述新发现的重要维度
- Obstruction Theorist: 评估该维度是否被现有领域覆盖
- Team Lead: 决定是否引入新领域探索

---

## 迭代终止条件

**满足以下任一条件即可终止迭代**:
1. **收敛**: Obstruction 通过率 ≥ 0.7 且 Dissensus ≤ 40
2. **上限**: 达到最大领域数 (8-10 个)
3. **饱和**: 新增领域不再产生新洞察（由三人小组判断）
4. **时间**: 用户主动终止或超过时间预算（由 Team Lead 评估）
5. **⚠️ v4.4 优化**: **三人小组一致同意终止**（需记录理由）

**⚠️ 终止决策记录要求**:
- 谁支持终止？
- 反对者如果有异议，是否被解决？
- 终止的具体理由是什么？
- 是否有未充分探索的维度？

---

## 三人决策小组决策记录格式（v4.4 优化版）

### 决策记录模板

```markdown
## 三人小组决策会议记录 - Round N

**时间**: {timestamp}
**参与成员**: Synthesizer, Obstruction Theorist, Team Lead
**触发原因**: {obstruction_pass_rate < 0.5 / strong_homography / high_dissensus / new_dimension}

---

### Synthesizer 发言

**Limits/Colimits 初步结果**:
{summary}

**同构簇分析**:
{clusters}

**Dissensus 检测**:
{dissensus}

**建议**: {需要迭代 / 终止}

---

### Obstruction Theorist 发言

**Obstruction 通过率**: {pass_rate}%

**系统性问题**:
{systemic_issues}

**缺失维度**:
{missing_dimensions}

**建议引入的新领域**:
{suggested_domains}

---

### Team Lead 发言

**资源消耗**: {resource_usage}

**时间预算**: {time_budget}

**建议**: {继续迭代 / 终止分析}

---

### 投票决策

| 决策项 | Synthesizer | Obstruction | Team Lead | 结果 |
|-------|------------|------------|-----------|------|
| 启动新一轮迭代? | ✅/❌ | ✅/❌ | ✅/❌ | {通过/否决} |
| 引入的新领域 | {list} | {list} | {list} | {approved/rejected} |

---

### 最终决策

**决策**: {启动 Round 2 / 终止分析}

**理由**:
{reasoning}

**后续行动**:
{next_steps}

---

**记录人**: Team Lead
**确认人**: Synthesizer, Obstruction Theorist
```

---

## 完整执行流程代码模板（v4.4）

```python
# ============================================================================
# STEP 1: 创建团队
# ============================================================================

task_id = "analysis-{timestamp}"

TeamCreate(
    team_name=f"morphism-swarm-{task_id}",
    description="Morphism蜂群分析",
    agent_type="general-purpose"
)

# ============================================================================
# STEP 2: ⭐ 启动核心成员（Obstruction + Synthesizer）
# ============================================================================

# ⚠️🔴 关键：TeamCreate 已自动创建 team-lead，不需要再创建！
# ❌ 错误：Task(name="team-lead") 会创建 team-lead-2 导致重复
# ✅ 正确：只创建 obstruction-theorist、synthesizer

# 2.1 启动 Obstruction Theorist（实时审查）
Task(
    description="Obstruction Theorist - 映射质量审查",
    prompt=f"""
    你是 Obstruction Theorist，职业反对派，负责审查所有映射结果。

    **核心职责**:
    1. 等待 Domain Agents 发送 MAPPING_RESULT
    2. 对每个映射执行三道攻击测试
    3. 向 Synthesizer 发送 OBSTRUCTION_REPORT

    **⚠️ 重要**: 轻易不通过，怀疑一切。
    """,
    subagent_type="general-purpose",
    team_name=f"morphism-swarm-{task_id}",
    name="obstruction-theorist"
)

# 2.2 启动 Synthesizer（跨域整合）
Task(
    description="Synthesizer - 跨域整合与 Limits/Colimits 计算",
    prompt=f"""
    你是 Synthesizer，负责跨域整合和共识计算。

    **核心职责**:
    1. 接收 Domain Agents 的一句话洞察
    2. 计算 Limits（跨域共识）
    3. 计算 Colimits（互补整合）
    4. 检测同构簇
    5. 参与 Three-Person Decision Meeting
    6. 按需向 Obstruction 征求完整意见

    **⚠️ 重要**: 你无权单方面决定终止分析，必须通过三人小组决策。
    """,
    subagent_type="general-purpose",
    team_name=f"morphism-swarm-{task_id}",
    name="synthesizer"
)

# ============================================================================
# 🎯 Team Lead 说明
# ============================================================================
# Team Lead 由 TeamCreate 自动创建，agentId 格式为: team-lead@{team_name}
# v4.4 中，Team Lead 合并了 Yoneda Broadcaster 的职责
# 它会自动接收团队成员的 SendMessage 通信
# 无需再用 Task 工具创建！

# ============================================================================
# STEP 3: Team Lead 提取范畴骨架
# ============================================================================

# Team Lead 自动从用户问题中提取范畴骨架
# 这是 v4.4 的新增职责（原 Yoneda Broadcaster 的工作）

# ============================================================================
# STEP 4: 智能领域选择（由 Team Lead 触发）
# ============================================================================

# Team Lead 完成范畴提取后，调用 domain_selector.py
# 使用 Bash 工具执行 Python 脚本

# ============================================================================
# STEP 5: 启动 Domain Agents（由 Team Lead 触发）
# ============================================================================

# Team Lead 根据 domain_selector.py 的结果，动态启动 Domain Agents

# ============================================================================
# STEP 6: Domain Agents 并行分析
# ============================================================================

# 每个 Domain Agent 完成后，发送分层报告:
# - 完整报告 → Obstruction Theorist
# - 一句话洞察 → Synthesizer

# ============================================================================
# STEP 7: ⭐ 强制触发三人小组决策会议
# ============================================================================

# ⚠️ 关键：决策会议由已存在的 Team Lead 通过 SendMessage 触发
# ❌ 不要创建新的 Task，否则会导致重复创建 team-lead

# Team Lead 在等待所有 Domain Agent 完成后：
# 1. 使用 SendMessage 向 Synthesizer 询问 Limits/Colimits 结果
# 2. 使用 SendMessage 向 Obstruction Theorist 询问审查结果
# 3. 组织决策会议讨论
# 4. 记录决策结果
# 5. 根据决策启动后续行动

# 正确的做法是通过 SendMessage 通信：
# SendMessage(type="message", recipient="synthesizer", content="请报告 Limits/Colimits 分析结果")
# SendMessage(type="message", recipient="obstruction-theorist", content="请报告 Obstruction 审查结果")

# ============================================================================
# STEP 8: 根据决策结果执行（v4.4 优化）
# ============================================================================

# 如果决策是启动新一轮迭代
if decision == "iterate":
    # 方式 A: 深化现有 Agent
    for agent in valuable_agents:
        Task(..., name=f"{agent}-round2")

    # 方式 B: 引入新领域 Agent
    for domain in new_domains:
        Task(..., name=f"{domain}-agent")

    # 等待新一轮结果完成
    # 再次触发决策会议
    # 循环直到满足终止条件

# 如果决策是终止分析
elif decision == "terminate":
    # Synthesizer 生成最终报告
    # 基于三人小组的决策结果
    Task(
        description="生成最终报告",
        prompt=f"""
        你是 Synthesizer，请基于三人小组的决策结果生成最终报告。

        **决策记录**: {decision_record}

        **⚠️ 重要**: 你的报告必须基于三人小组的决策，而非单方面判断。

        **报告要求**:
        - 说明决策过程和理由
        - 整合所有轮次的分析结果
        - 说明为何最终选择终止/继续
        """,
        subagent_type="general-purpose",
        team_name=f"morphism-swarm-{task_id}",
        name="synthesizer-final"
    )
```

---

## 核心差异：v4.4 vs v4.3

| 方面 | v4.3 | v4.4 |
|-----|------|------|
| 核心成员数 | 4个（Team Lead + Yoneda Broadcaster + Obstruction + Synthesizer） | **3个**（Team Lead 合并 Broadcaster + Obstruction + Synthesizer） |
| Team Lead 职责 | 团队协调 | **团队协调 + 范畴提取** |
| 第一轮信息流 | Domain Agent → Obstruction（完整）+ Synthesizer（完整） | **Domain Agent → Obstruction（完整）+ Synthesizer（一句话洞察）** |
| Obstruction 报告 | 仅完整报告 | **完整报告 + 30字诊断简报** |
| Synthesizer 审查 | 自动接收完整报告 | **按需征求完整意见** |

---

## 核心差异：v4.4 纯 Swarm vs 旧版本

| 方面 | 旧版本 | v4.4 纯 Swarm |
|------|--------|--------------|
| 模式 | Fast Mode + Swarm Mode | **仅 Swarm Mode** |
| 启动方式 | 快捷命令 + 对话选择 | **直接描述问题** |
| 领域选择 | 用户手动选择 1-5 | **自动智能选择** (domain_selector.py) |
| 领域来源 | 固定列表 | **31个领域动态匹配** |
| 范畴提取 | Yoneda Broadcaster 独立角色 | **Team Lead 合并职责** |
| 信息流 | 统一发送完整报告 | **分层发送（完整+洞察）** |
| 扩展机制 | 一次性全部 | **三人决策小组信号引导 + 强制决策会议** |
| 迭代决策 | Synthesizer 可单方面决定 | **强制决策会议，禁止单方面终止** |
| 决策记录 | 无 | **必须记录决策过程** |

---

## 指南文档

| 文档 | 用途 | 目标 |
|------|------|------|
| `SKILL_LEADER.md` | Team Lead 决策会议指南 ⭐ v4.4 更新 | Team Lead |
| `SKILL_SYNTHESIZER.md` | Synthesizer 合成与 Phase 4.1 指南 | Synthesizer |
| `SKILL_OBSTRUCTION.md` | Obstruction Theorist 审查指南 | Obstruction Theorist |
| `docs/DOMAIN_AGENT_GUIDE.md` | Domain Agent 角色指南 | Teammates |

---

## 质量保证

### Trivial Limit 检测

拒绝使用通用形容词的"假共识":
- ❌ "需要平衡"
- ❌ "应该重视"
- ❌ "要有长远眼光"

### Kernel Loss 强制要求

所有 Domain Agent 输出必须包含 `kernel_loss` 字段：
```json
{
  "kernel_loss": {
    "lost_nuances": [
      {
        "element": "丢失的元素",
        "description": "详细说明",
        "severity": "HIGH | MEDIUM | LOW"
      }
    ],
    "preservation_score": 0.75
  }
}
```

**如果 kernel_loss 为空或 "None"** → 结果直接丢弃

### 🔴 Obstruction Theorist 审查（Phase 4.1 第三道防线）

**参考文件**: `agents/personas/obstruction_theorist.md`

**三道攻击测试**:

1. **动力学反转测试**: 线性 vs 指数? 可逆 vs 不可逆?
2. **约束丢失测试**: 资源约束? 伦理约束?
3. **副作用盲区测试**: 情感维度? 政治后果?

**处理逻辑**:
```python
if obstruction_result == "OBSTRUCTION_FOUND":
    # 映射被阻断，不进入 Limit/Colimit 计算
    mapping["is_verified"] = False
elif obstruction_result == "PASS":
    # 通过但置信度打折
    mapping["is_verified"] = True
    mapping["confidence"] *= 0.8
```

**PASS 率警示**:
- 如果 Obstruction Theorist 的 PASS 率超过 30%，说明审查不够严格
- 职业反对派的设计初衷是"怀疑一切，轻易不通过"

---

## 版本历史

| 版本 | 日期 | 核心更新 |
|-----|------|---------|
| **v4.4.1** | 2026-02-09 | 🔧 **范畴骨架注入标准**: 新增统一模板确保所有 Agent 获得一致的范畴骨架 |
| **v4.4** | 2026-02-09 | 🎯 **架构简化**: 合并Lead+Broadcaster职责，优化第一轮信息流分层发送 |
| **v4.3.1** | 2026-02-09 | 🔧 **修复范畴骨架注入机制**：Broadcaster → Team Lead → Domain Agents（显式注入，防止抢跑） |
| **v4.3** | 2026-02-09 | 🎯 **三人小组迭代决策制度化**：强制触发决策会议、禁止单方面终止、决策记录要求 |
| **v4.2** | 2026-02-09 | Obstruction Theorist 职责明晰化：三道攻击测试标准化、主动催促机制、范畴骨架审查 |
| **v4.1** | 2026-02-08 | 三人决策小组（Synthesizer + Obstruction Theorist + Team Lead）持续通信与投票机制 |
| **v4.0** | 2026-02-07 | 纯 Swarm Mode，废弃 Fast Mode，引入 Phase 4.1 结构摩擦层 |
| **v3.0** | 2026-02-06 | 单域映射模式，引入 Yoneda Broadcaster 和 Kernel Loss Protocol |
| **v2.0** | 2026-02-05 | 基础映射框架，支持 31 个领域 |

### v4.4 核心升级详情

**1. 架构简化：合并 Lead + Broadcaster**
- **删除独立角色**: 不再需要独立的 Yoneda Broadcaster
- **职责合并**: Team Lead 负责范畴提取 + 团队协调
- **减少通信**: 减少一个角色的通信开销

**2. 第一轮信息流分层优化**
- **完整报告**: Domain Agent → Obstruction（完整分析）
- **一句话洞察**: Domain Agent → Synthesizer（30字核心洞察）
- **诊断简报**: Obstruction → Synthesizer（30字风险预警）

**3. 按需审查机制**
- **自动触发**: Synthesizer 在明显不满时向 Obstruction 征求完整意见
- **减少冗余**: 避免不必要的完整报告传输
- **提高效率**: 信息流更加分层和精准

**4. 代码模板更新**
- 移除 Yoneda Broadcaster 启动代码
- 更新 Team Lead 职责描述
- 更新信息流发送逻辑

**5. 新增：范畴骨架注入标准模板** ⭐ v4.4.1
- 确保 Team Lead 向所有 Domain Agent（包括迭代新增）注入**统一格式**的范畴骨架
- 防止信息差导致分析深度不一致

---

## 🚨 CRITICAL: 范畴骨架注入标准模板 (v4.4.1)

**问题**: 迭代时新增 Agent 可能获得的信息不一致

**解决方案**: Team Lead 必须向**每个** Domain Agent 注入完整的范畴骨架

### 标准模板格式

```python
# ============================================================================
# 范畴骨架注入模板（所有 Domain Agent 必须使用）
# ============================================================================

CATEGORY_SKELETON = {
    "objects": [
        {"name": "实体1", "attributes": "属性描述"},
        {"name": "实体2", "attributes": "属性描述"},
        {"name": "实体3", "attributes": "属性描述"},
        {"name": "实体4", "attributes": "属性描述"}
    ],
    "morphisms": [
        {
            "from": "实体1",
            "to": "实体2",
            "dynamics": "详细的动态描述（如：信息选择、过滤、包装机制）"
        },
        {
            "from": "实体2",
            "to": "实体3",
            "dynamics": "详细的动态描述（如：认知塑造、信念更新机制）"
        },
        {
            "from": "实体3",
            "to": "实体1",
            "dynamics": "详细的动态描述（如：反馈调节、修正机制）"
        },
        {
            "from": "外部冲击",
            "to": "实体2",
            "dynamics": "详细的动态描述（如：现实检验、相变触发）"
        }
    ],
    "核心问题": "用户困惑的精确表述"
}
```

### Domain Agent Prompt 注入示例

```python
Task(
    description="{Domain} Agent 分析",
    prompt=f"""
    你是 {Domain} Domain Agent，基于 {Domain} 原理分析问题。

    **范畴骨架**（统一标准格式）:
    - Objects: {', '.join([f"{o['name']}({o['attributes']})" for o in CATEGORY_SKELETON['objects']])}
    - Morphisms:
        {chr(10).join([f"{m['from']} → {m['to']}: {m['dynamics']}" for m in CATEGORY_SKELETON['morphisms']])}

    **核心问题**: {CATEGORY_SKELETON['核心问题']}

    **输出要求**:
    - 完整 MAPPING_RESULT → obstruction-theorist
    - 一句话洞察（30字内） → synthesizer

    请开始分析。
    """,
    subagent_type="general-purpose",
    team_name=f"morphism-swarm-{task_id}",
    name="{domain_lower}-agent"
)
```

### 强制检查点

每次启动 Domain Agent 后，Team Lead 必须确认：
- [ ] Objects 是否包含 4 个核心实体？
- [ ] Morphisms 是否包含 `from`, `to`, `dynamics` 三个字段？
- [ ] `dynamics` 描述是否足够详细（非简略）？
- [ ] 所有 Agent 获得的格式是否一致？

**❌ 禁止**:
```python
# 禁止使用简化版本
prompt=f"""
范畴骨架:
- Objects: 媒体, 受众, 美国
- Morphisms: 宣传, 认知, 崩塌
"""  # ✗ 信息不足

# ✅ 必须使用详细版本
prompt=f"""
范畴骨架:
- Objects: 媒体主体(信息编码器), 受众群体(解码器+信念更新者), 目标对象(被建构的理想美国), 现实对照(爱泼斯坦案等事实冲击)
- Morphisms:
  - 媒体主体 → 目标对象: 宣传建构(信息选择、过滤、美化编码)
  - 目标对象 → 受众群体: 认知塑造(信念植入、形成刻板印象)
  - 现实对照 → 受众群体: 认知冲击(贝叶斯更新、失调崩塌)
  - 受众群体 → 媒体主体: 信任崩塌(互信息→0、不再信任)
"""  # ✓ 信息完整
```

---

**初版创建**: 2026-02-08
**最新版本**: v4.4.1 (范畴骨架注入标准)
**核心理念**: 从"五角色协作"转向"三角色高效协作 + 分层信息流 + 统一范畴注入"
