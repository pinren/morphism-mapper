---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.4 Swarm Mode - 基于范畴论的跨领域并行探索系统。通过多 Agent Team 并行分析，将 Domain A 的问题结构映射到多个远域 Domain B，借助跨域共识（Limits）和互补整合（Colimits）生成非共识创新方案。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"增加易经思想领域"等。
---

# Category Theory Morphism Mapper v4.4 🐝

**版本**: v4.4.3 (Swarm Mode)
**更新日期**: 2026-02-09
**领域数量**: 31个内置领域 + 动态新增

**核心架构**: 3个关键 Agent + 动态 Domain Agents
**通信铁律**: 只能使用 SendMessage，其他方式会导致 Team 异常
**关键脚本**: `scripts/domain_selector.py` + `scripts/dynamic_agent_generator.py`
**配置路径**: `assets/agents/config/`

---

## 核心架构 (3+N 模型，N 按需生成)

```
┌─────────────────────────────────────────────────────────────┐
│              Morphism Mapper v4.4 核心架构                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔴 核心成员（3个）                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Team Lead  │  │  Obstruction │  │  Synthesizer │      │
│  │   (自动创建)  │  │   Theorist   │  │              │      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤      │
│  │• 范畴提取     │  │• 三道攻击测试 │  │• Limits计算  │      │
│  │• 领域选择     │  │• 质量审查     │  │• Colimits整合│      │
│  │• Agent生成    │  │• 风险预警     │  │• 跨域共识     │      │
│  │• 决策协调     │  │• 通过率统计   │  │• 最终报告     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ↓                                │
│                  ┌─────────────────┐                       │
│                  │  SendMessage    │                       │
│                  │   (唯一通信)     │                       │
│                  └────────┬────────┘                       │
│                           ↓                                 │
│  🟡 动态成员（1-N个）                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Domain A1  │  │   Domain A2  │  │   Domain A3  │      │
│  │   (动态生成)  │  │   (动态生成)  │  │   (动态生成)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agent 职责

| Agent | 创建方式 | 核心职责 | 通信对象 |
|-------|---------|---------|---------|
| **Team Lead** | `TeamCreate` 自动创建 | 范畴提取、领域选择、Agent生成、决策协调 | 所有成员 |
| **Obstruction Theorist** | `Task(name="obstruction-theorist")` | 三道攻击测试、质量审查、风险预警 | Synthesizer, Team Lead |
| **Synthesizer** | `Task(name="synthesizer")` | Limits/Colimits计算、跨域整合、最终报告 | 所有成员 |
| **Domain Agent** | `Task(name="{domain}-agent")` | 领域分析、映射执行 | Obstruction, Synthesizer |

---

## 🚨 通信铁律：只能使用 SendMessage

**唯一正确的通信方式**：
```python
SendMessage(
    type="message",
    recipient="agent-name",  # 目标Agent名称
    content="消息内容",
    summary="消息摘要"
)
```

**为什么其他方式会失败**：
- ❌ Task prompt 中嵌入信息 → 信息不一致、无法更新
- ❌ 全局变量 → Agent Team 无共享内存
- ❌ 文件读写 → 延迟、竞争条件
- ❌ print/output → 其他 Agent 无法接收

**通信流程**：
```
Domain Agent 完成分析
    ↓
SendMessage → Obstruction Theorist (完整报告)
SendMessage → Synthesizer (一句话洞察)
    ↓
Obstruction Theorist 审查后
    ↓
SendMessage → Synthesizer (30字诊断简报)
    ↓
三人小组决策会议 (SendMessage 循环)
    ↓
Team Lead 发送最终报告
```

---

## 动态 Agent 生成机制

### 核心脚本

```python
from scripts.dynamic_agent_generator import DynamicAgentGenerator

# 初始化
generator = DynamicAgentGenerator()

# 批量生成（推荐）
prompts = generator.generate_batch(
    domains=['game_theory', 'evolutionary_biology'],
    category_skeleton={
        "objects": [...],
        "morphisms": [...],
        "核心问题": "..."
    }
)

# 启动 Domain Agents
for domain, prompt in prompts.items():
    Task(
        name=f"{domain}-agent",
        prompt=prompt,  # 已包含完整领域知识 + 范畴骨架
        ...
    )
```

### 知识来源

1. **内置领域**: `references/{domain}_v2.md` (31个)
2. **自定义领域**: `references/custom/{domain}_v2.md`
3. **动态创建**: 如果不存在，自动生成 V2 标准格式

### V2 标准结构

每个领域文件包含：
- **100基本基石**: 哲学观(18) + 原则(22) + 心智模型(28) + 方法论(22) + 避坑(10)
- **14 Core Objects**: 领域核心概念
- **14 Core Morphisms**: 领域动态关系
- **18 Theorems**: 每个含 Applicable_Structure + Mapping_Hint + Case_Study

---

## 执行流程

```
Step 1: TeamCreate(team_name="xxx")
    ↓ 自动创建 team-lead
Step 2: 启动核心成员
    ├── Task("obstruction-theorist")
    └── Task("synthesizer")
    ↓
Step 3: Team Lead 提取 Category Skeleton
    ├── Objects: 问题中的实体
    └── Morphisms: 实体间动态关系
    ↓
Step 4: 领域选择 (domain_selector.py)
    ├── 分析 Morphisms 提取标签
    ├── 匹配 16 个动态标签
    └── Tier Balance 选择 Top 3-5
    ↓
Step 5: Team Lead 动态生成 Domain Agents

    ```python
    from scripts.dynamic_agent_generator import DynamicAgentGenerator
    from scripts.domain_selector import DomainSelector

    # 5.1 领域选择
    selector = DomainSelector()
    result = selector.select_domains(objects, morphisms)
    selected_domains = [d['domain'] for d in result['top_domains'][:3]]

    # 5.2 初始化生成器（启用补盲模式）
    generator = DynamicAgentGenerator()

    # 5.3 批量生成 Prompts（关键：auto_create=True 启用补盲）
    prompts = generator.generate_batch(
        domains=selected_domains,
        category_skeleton=category_skeleton,
        auto_create=True,  # ✅ 启用自动补盲
        domain_sources={
            'domain_name': '领域描述（用于补盲生成）'
        }
    )

    # 5.4 处理每个领域
    for domain, prompt_or_instruction in prompts.items():

        # 情况A: 正常返回（字符串）
        if isinstance(prompt_or_instruction, str):
            Task(
                name=f"{domain}-agent",
                prompt=prompt_or_instruction,
                subagent_type="general-purpose",
                team_name=team_name
            )

        # 情况B: 需要补盲生成（字典）
        elif isinstance(prompt_or_instruction, dict):
            if prompt_or_instruction['action'] == 'CREATE_DOMAIN':
                # Team Lead 调用 LLM 生成领域知识
                generation_prompt = prompt_or_instruction['generation_prompt']

                # 调用 LLM（当前上下文）
                content = generate_content(generation_prompt)  # Team Lead 执行

                # 保存领域文件
                file_path = generator.create_domain_from_content(domain, content)

                # 重新生成完整 Prompt
                full_prompt = generator.generate_full_prompt(domain, category_skeleton)

                # 启动 Domain Agent
                Task(
                    name=f"{domain}-agent",
                    prompt=full_prompt,
                    subagent_type="general-purpose",
                    team_name=team_name
                )
    ```

    **Team Lead 决策逻辑**：
    - 检查返回类型：`str` = 正常，`dict` = 需要补盲
    - 如果是补盲：必须先生成领域文件，再启动 Agent
    - 补盲是阻塞步骤，完成后才能继续
    ↓
Step 6: Domain Agents 并行分析
    ├── 领域知识映射
    ├── SendMessage → Obstruction (完整)
    └── SendMessage → Synthesizer (洞察)
    ↓
Step 7: 三人小组决策会议
    ├── Synthesizer: 报告 Limits/Colimits
    ├── Obstruction: 报告通过率/风险
    └── Team Lead: 决策迭代 or 终止
    ↓
Step 8: 生成报告 & 知识库更新
    ├── 保存到 knowledge/exploration_history/
    └── 更新 knowledge/homography_graph.json
```

---

## 关键约束

### 1. Agent 启动约束
```python
# ✅ 正确
TeamCreate(team_name="xxx")  # 自动创建 team-lead
Task(name="obstruction-theorist", team_name="xxx")
Task(name="synthesizer", team_name="xxx")

# ❌ 错误：重复创建 team-lead
Task(name="team-lead", team_name="xxx")
```

### 2. 通信约束
```python
# ✅ 正确：使用 SendMessage
SendMessage(
    type="message",
    recipient="synthesizer",
    content="分析结果..."
)

# ❌ 错误：直接输出
print("分析结果...")  # 其他Agent收不到
```

### 3. 领域选择约束
```python
# ✅ 正确：使用 domain_selector.py
from scripts.domain_selector import DomainSelector
selector = DomainSelector()
result = selector.select_domains(objects, morphisms)

# ❌ 错误：硬编码
selected = ['game_theory', 'thermodynamics']  # 跳过智能选择
```

### 4. 决策约束
```python
# ✅ 正确：三人小组决策
# - Synthesizer 提议
# - Obstruction 审查
# - Team Lead 决策
# - 2/3 多数通过

# ❌ 错误：单方面决策
# - Synthesizer 单方面终止
# - Team Lead 跳过会议直接写报告
```

---

## 快速开始

### 启动分析
```python
# 用户问题触发
/morphism-mapper "美国抓捕马杜罗对国际局势的影响"

# 系统自动：
# 1. TeamCreate
# 2. 启动 Obstruction + Synthesizer
# 3. 提取 Category Skeleton
# 4. domain_selector 选择领域
# 5. DynamicAgentGenerator 生成 Prompts
# 6. 启动 Domain Agents
# 7. 等待 SendMessage 通信
# 8. 触发三人决策会议
# 9. 生成报告
```

### 调试模式
```python
# 只启动1个Domain Agent，便于跟踪消息流
selected_domains = result['top_domains'][:1]
```

### 新增领域

**方式1**: 使用 add-domain 命令（手动）
```python
/morphism-add-domain "中医"
```

**方式2**: On-the-fly 补盲生成（自动）

当 `domain_selector.py` 选中了一个不存在的领域时，`DynamicAgentGenerator` 会自动触发补盲机制：

```python
from scripts.dynamic_agent_generator import DynamicAgentGenerator

generator = DynamicAgentGenerator()

# 启用 auto_create 模式
prompts = generator.generate_batch(
    domains=['quantum_field_theory'],  # 假设这个领域不存在
    category_skeleton=skeleton,
    auto_create=True,  # 启用自动创建
    domain_sources={'quantum_field_theory': '量子场论，物理学的基本框架'}
)

# 检查返回结果
for domain, result in prompts.items():
    if isinstance(result, dict) and result.get('action') == 'CREATE_DOMAIN':
        # 需要补盲生成
        generation_prompt = result['generation_prompt']

        # Team Lead 使用 generation_prompt 调用 LLM
        # content = call_llm(generation_prompt)

        # 保存生成的领域文件
        file_path = generator.create_domain_from_content(domain, content)

        # 重新生成 Domain Agent Prompt
        full_prompt = generator.generate_full_prompt(domain, skeleton)
```

**补盲流程**：
```
domain_selector 选中领域 X
    ↓
DynamicAgentGenerator 检查文件不存在
    ↓
生成 V2 标准格式的 generation_prompt
    ↓
返回给 Team Lead
    ↓
Team Lead 调用 LLM 生成完整内容
    ↓
create_domain_from_content 保存到 references/custom/
    ↓
重新生成 Domain Agent Prompt
    ↓
正常启动 Domain Agent
```

**关键特性**：
- ✅ 自动检测缺失领域
- ✅ 生成符合 V2 标准的提示词
- ✅ Team Lead 调用 LLM 生成内容
- ✅ 自动保存到 references/custom/
- ✅ 无缝继续执行流程

---

## 文件结构

```
morphism-mapper/
├── SKILL.md                          # 本文件
├── references/                       # 领域知识库
│   ├── game_theory_v2.md
│   ├── thermodynamics_v2.md
│   └── custom/                       # 自定义领域
├── scripts/
│   ├── domain_selector.py            # 智能领域选择
│   ├── dynamic_agent_generator.py    # 动态Agent生成
│   └── commands/
│       └── add-domain.md             # 新增领域命令
└── knowledge/                        # 输出目录
    ├── exploration_history/          # 分析报告
    └── homography_graph.json         # 统计信息
```

---

## 版本历史

| 版本 | 日期 | 核心更新 |
|-----|------|---------|
| v4.4.3 | 2026-02-09 | 动态Agent生成 + 完整定理保留 |
| v4.4 | 2026-02-09 | 合并Lead+Broadcaster职责，优化信息流 |
| v4.0 | 2026-02-07 | 纯Swarm Mode，废弃Fast Mode |

---

**核心记忆点**：3个关键Agent + SendMessage通信 + 动态Domain Agent生成
