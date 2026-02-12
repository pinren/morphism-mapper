---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.5 Swarm Mode - 基于范畴论的跨领域并行探索系统。通过多 Agent Team 并行分析，将 Domain A 的问题结构映射到多个远域 Domain B，借助跨域共识（Limits）和互补整合（Colimits）生成非共识创新方案。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"增加易经思想领域"、"新增领域"、"添加领域"等。
---

# Category Theory Morphism Mapper v4.5 🐝

**版本**: v4.5.5 (Swarm Mode - 模拟模式必须读取领域文件)
**更新日期**: 2026-02-10
**领域数量**: 31个内置领域 + 动态新增

**核心升级**:
1. **Obstruction Theorist 升级为四维十二式智能攻击矩阵**
   - 新增本体论维度（针对"人"的系统）
   - 智能武器选择（从12个攻击点选择最致命的3个）
2. **统一持久化架构** (v4.5.1)
   - 按问题维度组织子目录：`~/.morphism_mapper/explorations/{timestamp}_{problem_slug}/`
   - 每个探索独立存储，避免文件混乱
   - 自动索引和软链接管理
3. **强制持久化与权限管理** (v4.5.2)
   - **强制执行规则**: 持久化不再是可选项，分析前必须确认写入权限
   - **按需申请权限**: 权限不足时必须停止并向用户申请
   - **权限检查清单**: 预检脚本、自定义路径、失败恢复机制
   - **禁止行为清单**: 明确标记违规操作及后果
4. **ADE 自适应扩展机制** (v4.5.3)
   - **置信度驱动**: 平均置信度<60%时自动触发扩展
   - **缺口填补策略**: 冲突解决型、盲区覆盖型、桥接型三种策略
   - **全自动扩展**: 无需用户确认，自动引入1-2个新领域
   - **硬边界限制**: 最多10领域、6轮(3次往返)强制终止
   - **专用Prompt**: 扩展阶段Agent使用特殊Prompt，强调互补性而非重复
5. **模拟模式持久化强制规范** (v4.5.4)
   - **明确模拟模式也必须自动持久化**: 无论生产还是模拟，持久化都是强制要求
   - **执行时机表**: Step 0-8每个步骤对应的保存文件清单
   - **自动执行代码模板**: Python代码示例，确保每个步骤后立即保存
   - **验证检查点**: 保存后必须验证文件完整性
6. **模拟模式必须读取领域文件** (v4.5.5) ⭐
   - **关键缺陷修复**: 之前的模拟模式分析没有读取 `references/{domain}_v2.md`
   - **强制读取流程**: 扮演 Domain Agent 前必须读取并解析领域文件
   - **V2 标准强制引用**: 分析必须包含 100基本基石、14 Core Objects、14 Core Morphisms、18 Theorems 的引用
   - **未读取则分析无效**: 如果没有引用领域文件，分析被视为不完整

---

## ⚠️ 重要说明：模拟模式 vs 生产模式

### 🔴 当前运行模式：模拟演示模式

**当你看到本消息时，说明当前处于「模拟演示模式」**：

#### 什么是模拟模式？
- ✅ **单个AI助手**扮演所有Agent角色（Team Lead、Obstruction、Synthesizer、Domain Agents）
- ✅ 所有"Agent通信"实际上是**同一会话内的上下文切换**
- ✅ 没有真正的Agent Swarm基础设施（没有独立的Agent进程、没有SendMessage系统）
- ✅ **持久化必须自动执行**（即使模拟模式，分析完成后立即保存文件）

#### 模拟模式也必须自动持久化

**核心原则**: **无论生产模式还是模拟模式，持久化都是强制要求。**

```
生产模式：                        模拟模式：
┌──────────────┐                ┌──────────────┐
│ Agent Team   │                │ 单个AI助手   │
│ 多进程并行   │                │ 单一会话     │
│ SendMessage  │                │ 角色扮演     │
│ 自动持久化   │                │ 自动持久化   │ ← 同样要求！
└──────────────┘                └──────────────┘
```

**区别仅在于触发时机**:
- **生产模式**: Agent发送`SaveFile`消息 → 系统自动保存
- **模拟模式**: 我完成每个Agent分析 → **我必须立即执行保存代码**

**在模拟模式下，我必须在以下时刻立即保存**:
- ✅ 完成 **Step 0** (创建目录结构)
- ✅ 完成 **Step 4** (Domain Agents Round 1) → 立即保存所有 `_round1.json`
- ✅ 完成 **Step 5** (Obstruction审查) → 立即保存所有 `_obstruction.json`
- ✅ 完成 **Step 6** (Domain Agents Round 2修正) → 立即保存所有 `_round2.json`
- ✅ 完成 **Step 7** (Synthesizer整合) → 立即保存 `synthesis.json`
- ✅ 完成 **Step 8** (最终报告) → 立即更新 `index.json` 和 `latest` 软链接

#### 如果我没有自动持久化怎么办？

**如果我在分析后没有立即保存文件，请提醒我**:

```
用户: "请执行持久化"
或
用户: "保存分析结果"
或
用户: "为什么持久化没有自动执行"
```

收到提醒后，我将立即：
1. 检查当前分析状态
2. 创建目录结构
3. 保存所有Agent输出
4. 更新索引
5. 验证文件完整性

### 🟢 生产模式部署（真实Agent Swarm）

要使持久化**自动执行**，需要部署到真实的Agent基础设施：

#### 方案A: 使用Claude Code的Agent Team功能
```python
# 在支持Agent Team的环境中运行
# 例如在Claude Desktop或支持TeamCreate的平台上

from claude import TeamCreate, Task, SendMessage

team = TeamCreate(team_name="morphism-analysis")
# 此时每个Agent是独立进程，SendMessage是真实的IPC通信
# 持久化由Agent基础设施自动处理
```

#### 方案B: 使用LangChain/LlamaIndex的Multi-Agent框架
```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import SystemMessage

# 为每个Agent创建独立的Executor
# 使用消息队列（如Redis）进行SendMessage通信
# 持久化由框架的事件系统触发
```

#### 方案C: 自定义Agent基础设施
见下方「生产环境部署指南」章节。

### 📋 模拟模式持久化自动执行规范

**当我处于模拟模式时，我必须在每个步骤后立即执行以下持久化操作**：

#### 执行时机与对应文件

| 步骤 | 执行时刻 | 保存文件 | 格式 |
|------|---------|---------|------|
| **Step 0** | 分析开始前 | `metadata.json` | JSON |
| **Step 4** | Domain Agents Round 1 完成后 | `{domain}_round1.json` (每个领域一个) | JSON |
| **Step 5** | Obstruction Theorist 审查后 | `{domain}_obstruction.json` (每个领域一个) | JSON |
| **Step 6** | Domain Agents Round 2 修正后 | `{domain}_round2.json` (每个领域一个) | JSON |
| **Step 7** | Synthesizer 整合后 | `synthesis.json` | JSON |
| **Step 8** | 最终报告完成后 | `index.json` + `latest` 软链接 | JSON + symlink |

#### 自动执行代码模板

**我必须在每个步骤后执行类似以下的代码**:

```python
# Step 0: 创建目录并保存 metadata
import os
from datetime import datetime

problem = "用户问题"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
problem_slug = problem[:30].replace(" ", "_").replace("/", "_")
exploration_path = os.path.expanduser(f"~/.morphism_mapper/explorations/{timestamp}_{problem_slug}")

# 创建目录
for subdir in ["domain_results", "obstruction_feedbacks", "synthesizer_inputs", "final_reports", "logs"]:
    os.makedirs(os.path.join(exploration_path, subdir), exist_ok=True)

# 保存 metadata
metadata = {
    "exploration_id": f"{timestamp}_{problem_slug}",
    "problem": problem,
    "timestamp": timestamp,
    "domains": selected_domains,
    "status": "in_progress"
}
with open(os.path.join(exploration_path, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

# Step 4: 保存 Domain Agents Round 1 结果
for domain, result in domain_results.items():
    filepath = os.path.join(exploration_path, f"domain_results/{domain}_round1.json")
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

# Step 5: 保存 Obstruction 反馈
for domain, feedback in obstruction_feedbacks.items():
    filepath = os.path.join(exploration_path, f"obstruction_feedbacks/{domain}_obstruction.json")
    with open(filepath, "w") as f:
        json.dump(feedback, f, indent=2, ensure_ascii=False)

# Step 6: 保存 Domain Agents Round 2 结果
for domain, result in domain_results_round2.items():
    filepath = os.path.join(exploration_path, f"domain_results/{domain}_round2.json")
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

# Step 7: 保存 Synthesis 报告
synthesis_path = os.path.join(exploration_path, "final_reports/synthesis.json")
with open(synthesis_path, "w") as f:
    json.dump(synthesis_result, f, indent=2, ensure_ascii=False)

# Step 8: 更新 index.json 和 latest 软链接
index_path = os.path.expanduser("~/.morphism_mapper/explorations/index.json")
# 读取现有索引，添加新探索，保存
# 更新 latest 软链接指向当前探索
```

#### 验证持久化完成的检查点

**每次保存后，我必须验证**:

```bash
# 检查文件是否存在
ls -la ~/.morphism_mapper/explorations/latest/domain_results/
ls -la ~/.morphism_mapper/explorations/latest/obstruction_feedbacks/
ls -la ~/.morphism_mapper/explorations/latest/final_reports/

# 检查 metadata
head ~/.morphism_mapper/explorations/latest/metadata.json

# 检查 index 是否更新
cat ~/.morphism_mapper/explorations/index.json
```

#### 如果我没有自动执行

**如果用户发现我没有在分析后自动保存，请立即提醒我**。

我会：
1. 道歉并承认错误
2. 立即执行所有未完成的保存操作
3. 验证文件完整性
4. 向用户报告保存结果

### 🔧 如何升级到生产模式

见下方「生产环境部署指南」章节。

---

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

## 🔍 模拟模式领域文件读取规范 (v4.5.5+)

**关键缺陷警示**: 在之前的模拟模式执行中，Domain Agents **没有读取** `references/{domain}_v2.md` 领域文件，而是直接使用通用知识生成分析，这严重违反了 V2 标准。

### 为什么必须读取领域文件？

**V2 标准的核心要求**:
- **100基本基石**: 哲学观(18) + 原则(22) + 心智模型(28) + 方法论(22) + 避坑(10)
- **14 Core Objects**: 领域核心概念
- **14 Core Morphisms**: 领域动态关系  
- **18 Theorems**: 每个含 Applicable_Structure + Mapping_Hint + Case_Study

**如果不读取领域文件**:
- ❌ 分析缺乏领域特有的深度定理
- ❌ 概念映射不准确（用通用概念替代领域专业概念）
- ❌ 无法提供 Case_Study 支持
- ❌ 违反 SKILL.md 明确规定的知识来源

### 模拟模式下的强制读取流程

**当我扮演 Domain Agent 时，我必须**：

#### Step 1: 检查领域文件是否存在

```python
import os

def check_domain_file(domain: str) -> str:
    """
    检查领域文件是否存在
    Returns: 文件路径或 None
    """
    # 标准路径
    base_path = "~/.claude/skills/morphism-mapper/references"
    
    # 尝试内置领域
    file_path = os.path.join(base_path, f"{domain}_v2.md")
    if os.path.exists(file_path):
        return file_path
    
    # 尝试自定义领域
    custom_path = os.path.join(base_path, "custom", f"{domain}_v2.md")
    if os.path.exists(custom_path):
        return custom_path
    
    return None
```

#### Step 2: 读取并解析领域文件

```python
def read_domain_knowledge(domain: str) -> dict:
    """
    读取领域文件并提取关键信息
    必须在扮演 Domain Agent 之前执行
    """
    file_path = check_domain_file(domain)
    
    if not file_path:
        # 触发补盲生成
        return generate_blind_domain(domain)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 V2 标准结构
    knowledge = {
        "domain": domain,
        "file_path": file_path,
        "philosophy": extract_section(content, "哲学观"),  # 18条
        "principles": extract_section(content, "核心原则"),  # 22条
        "mental_models": extract_section(content, "心智模型"),  # 28条
        "methodology": extract_section(content, "方法论"),  # 22条
        "pitfalls": extract_section(content, "避坑指南"),  # 10条
        "core_objects": extract_section(content, "Core Objects"),  # 14个
        "core_morphisms": extract_section(content, "Core Morphisms"),  # 14个
        "theorems": extract_theorems(content),  # 18个定理
    }
    
    return knowledge
```

#### Step 3: 在分析中强制引用

**我的分析必须包含**：

```markdown
## 领域知识基础

**来源**: `references/{domain}_v2.md`

### 使用的定理
- **Theorem X**: {theorem_name}
  - **内容**: {theorem_content}
  - **适用结构**: {applicable_structure}
  - **映射提示**: {mapping_hint}
  - **案例**: {case_study}

### 概念映射
- `问题中的概念` → **{Core Object}** (引用领域文件定义)
- `动态关系` → **{Core Morphism}** (引用领域文件定义)

### 方法论应用
- **使用的方法**: {来自22条方法论的具体条目}
- **避开的坑**: {来自10条避坑指南的具体条目}
```

### 未读取领域文件的分析无效

**如果我在分析中没有**:
- [ ] 明确声明读取了 `references/{domain}_v2.md`
- [ ] 引用了至少 **2-3 个定理** (18个定理中的)
- [ ] 使用了 **Core Objects** 和 **Core Morphisms** 进行概念映射
- [ ] 提供了 **Case_Study** 支持洞察

**则该分析应被视为不完整，需要重新执行。**

### 模拟模式执行检查清单

**每次扮演 Domain Agent 前，我必须**：

```markdown
- [ ] **读取领域文件**: `references/{domain}_v2.md`
- [ ] **提取 100 基本基石**: 哲学观、原则、心智模型、方法论、避坑
- [ ] **提取 14 Core Objects**: 建立概念映射
- [ ] **提取 14 Core Morphisms**: 建立动态关系映射
- [ ] **选择 2-3 个定理**: 基于 Applicable_Structure 和问题匹配度
- [ ] **在分析中引用**: 明确标注定理来源和 Case_Study
- [ ] **保存分析结果**: 包含领域知识引用
```

### 示例：正确的 Domain Agent 分析

```markdown
## Domain Agent: Game Theory

### 领域知识来源
**文件**: `references/game_theory_v2.md` ✅

### 使用的定理

**Theorem 7: Nash Equilibrium (纳什均衡)**
- **内容**: 在非合作博弈中，如果每个玩家都知道其他玩家的策略，且没有任何玩家可以通过单方面改变策略而获得更高收益，则该策略组合构成纳什均衡。
- **适用结构**: 多方互动、策略相互依赖、无法单方面最优
- **映射提示**: 在Domain A中寻找"互动陷入僵局"的情境——各方都在做"对自己最优"的事，但集体结果却是次优的。
- **案例**: 囚徒困境中的互相揭发；价格战中各方降价导致利润下降

**应用于本问题**: 
"越在乎越容易失去"可以建模为一个**非对称博弈**：
- 玩家A（在乎的一方）：策略空间{过度投入, 适度投入}
- 玩家B（被在乎的一方）：策略空间{投入, 疏远}

当前状态是一个**坏的纳什均衡**：
- A选择"过度投入"（试图维持关系）
- B选择"疏远"（因为感到压力）
- 双方都无法单方面改变策略而不感到更糟
- 但这并不是全局最优的均衡

### Core Objects 映射
- `在乎的人` → **Player with Strategy Space** (策略空间受限的玩家)
- `被在乎的对象` → **Player with Dominant Strategy** (拥有占优策略的玩家)
- `失去` → **Suboptimal Equilibrium** (次优均衡结果)

### Core Morphisms 映射
- `在乎→焦虑` → **Strategy Convergence** (策略收敛到单一选项)
- `焦虑→控制` → **Commitment Strategy** (承诺策略，限制自己的选择)
- `控制→逃离` → **Best Response** (对方的最佳回应是退出)

### 方法论应用
**使用的方法**: 
- 方法 #12: "收益矩阵分析"——明确列出双方的收益结构
- 方法 #15: "均衡精炼"——寻找更优的均衡点

**避开的坑**:
- 坑 #3: "假设对方理性"——实际上对方可能受情感驱动
- 坑 #7: "忽视重复博弈"——关系是长期重复博弈，不是一次性博弈

### Case_Study 引用
**来自领域文件的案例**: 
> "冷战中的核威慑博弈：双方都知道战争会导致共同毁灭（次优均衡），但都无法单方面解除武装。直到一方改变策略（Gorbachev的'新思维'），才打破均衡。"

**应用到本问题**: 
打破"越在乎越容易失去"的坏均衡，需要一方改变策略：从"过度投入"转向"适度在乎+自我价值建设"。

...
```

### 验证领域文件读取

**用户可以通过以下方式验证**：

```bash
# 检查我是否读取了领域文件
grep -n "references/.*_v2.md" ~/.morphism_mapper/explorations/latest/domain_results/*_round1.json

# 检查是否引用了定理
grep -n "Theorem" ~/.morphism_mapper/explorations/latest/domain_results/*_round1.json

# 检查是否使用了 Core Objects
grep -n "Core Object" ~/.morphism_mapper/explorations/latest/domain_results/*_round1.json
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

## 🗄️ 强制持久化流程要求 (v4.5+)

**核心原则**: 所有Agent的输出必须持久化到文件系统，确保后续轮次可以读取历史输出进行针对性修正。

### 为什么需要强制持久化

在Swarm Mode多轮迭代中，同一个Domain Agent在第二轮需要读取自己第一轮的完整输出：
- ❌ **无持久化**: 每次Task创建新Agent实例，历史输出丢失
- ✅ **有持久化**: Agent读取自己的历史文件，基于完整上下文修正

### 持久化架构 (v4.5+ 统一问题子目录)

**核心变更**: 所有探索按问题维度组织，每个问题拥有独立的子目录，避免文件混乱。

```
~/.morphism_mapper/explorations/                    # 统一根目录
├── {timestamp}_{problem_slug}/                     # 每个问题独立子目录
│   ├── metadata.json                               # 问题元数据
│   ├── domain_results/                             # Domain Agent输出
│   │   ├── {domain}_round1.json
│   │   └── {domain}_round2.json
│   ├── obstruction_feedbacks/                      # Obstruction审查反馈
│   │   └── {domain}_obstruction.json
│   ├── synthesizer_inputs/                         # Synthesizer整合输入
│   │   └── synthesis_input.json
│   ├── final_reports/                              # 最终报告
│   │   └── synthesis.json
│   └── logs/                                       # 执行日志
├── index.json                                      # 所有探索的索引
└── latest -> {timestamp}_{problem_slug}/           # 软链接到最新探索
```

### 文件路径规范

```python
import os
from datetime import datetime

# 统一根目录
BASE_PATH = os.path.expanduser("~/.morphism_mapper/explorations")

# 生成问题子目录名 (Team Lead在启动时创建)
def create_exploration_dir(problem: str) -> str:
    """
    创建问题探索子目录
    Returns: 探索目录路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    problem_slug = problem[:30].replace(" ", "_").replace("/", "_")
    exploration_id = f"{timestamp}_{problem_slug}"
    exploration_path = os.path.join(BASE_PATH, exploration_id)
    
    # 创建目录结构
    os.makedirs(exploration_path, exist_ok=True)
    for subdir in ["domain_results", "obstruction_feedbacks", "synthesizer_inputs", "final_reports", "logs"]:
        os.makedirs(os.path.join(exploration_path, subdir), exist_ok=True)
    
    # 创建元数据文件
    metadata = {
        "exploration_id": exploration_id,
        "problem": problem,
        "timestamp": timestamp,
        "status": "initiated"
    }
    with open(os.path.join(exploration_path, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    # 更新最新软链接
    latest_link = os.path.join(BASE_PATH, "latest")
    if os.path.islink(latest_link):
        os.unlink(latest_link)
    os.symlink(exploration_path, latest_link)
    
    return exploration_path

# 当前探索路径 (由Team Lead注入到所有Agent的上下文中)
EXPLORATION_PATH = os.environ.get("MORPHISM_EXPLORATION_PATH", os.path.join(BASE_PATH, "latest"))

# Domain Agent第一轮
DOMAIN_ROUND1 = f"{EXPLORATION_PATH}/domain_results/{domain}_round1.json"

# Domain Agent第二轮（修正后）
DOMAIN_ROUND2 = f"{EXPLORATION_PATH}/domain_results/{domain}_round2.json"

# Obstruction反馈
OBSTRUCTION_FEEDBACK = f"{EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json"

# Synthesizer输入
SYNTHESIS_INPUT = f"{EXPLORATION_PATH}/synthesizer_inputs/synthesis_input.json"

# 最终报告
FINAL_REPORT = f"{EXPLORATION_PATH}/final_reports/synthesis.json"
```

### Team Lead 持久化初始化职责

**Step 0: 创建探索目录** (在Step 1之前执行)

```python
# Team Lead 在启动时创建统一的问题子目录
exploration_path = create_exploration_dir(problem="人在AI时代如何快速学习成长")

# 将路径注入到所有后续Agent的环境变量
os.environ["MORPHISM_EXPLORATION_PATH"] = exploration_path

# 在启动每个Agent时，在prompt中明确告知存储路径
agent_prompt = f"""
...其他prompt内容...

## 🗄️ 强制持久化路径
当前探索目录: {exploration_path}
你必须将所有输出保存到此目录下的对应子目录中。

### 保存路径规范:
- Domain结果: {exploration_path}/domain_results/{{domain}}_round{{N}}.json
- Obstruction反馈: {exploration_path}/obstruction_feedbacks/{{domain}}_obstruction.json
- Synthesizer输入: {exploration_path}/synthesizer_inputs/synthesis_input.json
- 最终报告: {exploration_path}/final_reports/synthesis.json
- 执行日志: {exploration_path}/logs/
"""
```

---

## ⚡ 持久化强制执行与权限管理 (v4.5.2+)

**核心原则**: 持久化不再是可选项，而是强制要求。任何 Agent 在执行分析前必须确认具备写入权限，否则必须向用户申请。

### 🚨 强制执行规则

#### 规则 1: 写入权限前置检查

**在启动任何分析之前，Team Lead 必须执行以下检查**:

```python
import os

def check_persistence_prerequisites():
    """
    检查持久化前提条件
    Returns: (bool, str) - (是否通过, 错误信息)
    """
    base_path = os.path.expanduser("~/.morphism_mapper")
    
    # 1. 检查目录是否存在或可创建
    try:
        os.makedirs(base_path, exist_ok=True)
    except PermissionError:
        return False, f"❌ 无法创建目录 {base_path}：权限被拒绝"
    except Exception as e:
        return False, f"❌ 无法创建目录 {base_path}：{str(e)}"
    
    # 2. 检查写入权限
    test_file = os.path.join(base_path, ".write_test")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
    except PermissionError:
        return False, f"❌ 没有写入权限：{base_path}"
    except Exception as e:
        return False, f"❌ 写入测试失败：{str(e)}"
    
    return True, "✅ 持久化权限检查通过"

# 在 Step 0 执行
passed, message = check_persistence_prerequisites()
if not passed:
    # 必须向用户申请权限，不能继续
    request_user_permission(message)
```

#### 规则 2: 按需申请写入权限

**如果权限检查失败，必须停止分析并向用户申请权限**:

```markdown
⚠️ **权限申请通知**

Morphism Mapper 需要写入权限以保存分析结果。这是 v4.5+ 的强制要求。

**需要访问的目录**:
- `~/.morphism_mapper/explorations/` - 保存所有探索记录
- `~/.morphism_mapper/explorations/index.json` - 探索索引

**为什么需要写入权限**:
1. **多轮迭代依赖**: Round 2 需要读取 Round 1 的结果
2. **历史追踪**: 支持回顾和对比多次分析
3. **质量保证**: Obstruction Theorist 需要审查历史输出
4. **审计合规**: 所有分析过程可追溯

**可选方案**:
- **方案 A**: 授予 `~/.morphism_mapper/` 目录的写入权限（推荐）
- **方案 B**: 指定自定义路径，需提供该路径的写入权限
- **方案 C**: 使用临时模式（不推荐，功能受限，无法多轮迭代）

请授权或选择方案，分析将在获得权限后继续。
```

#### 规则 3: 权限申请后的确认流程

**用户授权后，必须重新验证**:

```python
def request_user_permission(error_message: str) -> bool:
    """
    向用户申请写入权限
    Returns: bool - 是否获得授权并验证通过
    """
    # 向用户显示权限申请通知（见上文模板）
    # 等待用户响应...
    
    # 用户授权后，再次验证
    passed, verify_message = check_persistence_prerequisites()
    
    if passed:
        print("✅ 权限已确认，继续分析流程")
        return True
    else:
        print(f"❌ 权限验证仍失败：{verify_message}")
        print("请检查文件系统权限或选择备用方案")
        return False
```

#### 规则 4: 临时模式降级（仅应急）

**如果用户拒绝授权，可以进入临时模式，但功能受限**:

```python
class PersistenceMode:
    FULL = "full"           # 完整持久化（推荐）
    TEMPORARY = "temporary" # 临时模式（功能受限）
    MEMORY_ONLY = "memory"  # 仅内存（单轮，不推荐）

def set_persistence_mode(mode: PersistenceMode):
    """
    设置持久化模式
    """
    if mode == PersistenceMode.FULL:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "full"
        os.environ["MORPHISM_EXPLORATION_PATH"] = create_exploration_dir(problem)
    elif mode == PersistenceMode.TEMPORARY:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "temporary"
        # 使用 /tmp，但用户会被警告
        temp_path = f"/tmp/morphism_mapper_{timestamp}"
        os.environ["MORPHISM_EXPLORATION_PATH"] = temp_path
        print("⚠️ 警告：使用临时模式，分析结果将在会话结束后丢失")
        print("⚠️ 限制：无法执行多轮迭代（Round 2 需要 Round 1 的历史文件）")
    elif mode == PersistenceMode.MEMORY_ONLY:
        os.environ["MORPHISM_PERSISTENCE_MODE"] = "memory"
        print("🚨 警告：使用内存模式，仅限单轮分析")
        print("🚨 Obstruction Theorist 将无法审查历史输出")

# 在权限申请失败后
if not request_user_permission(error_msg):
    print("\n选择持久化模式：")
    print("1. 临时模式（/tmp，会话结束后丢失）")
    print("2. 内存模式（仅限单轮分析）")
    print("3. 退出并手动修复权限")
    # 等待用户选择...
```

### 📋 权限检查清单

**Team Lead 必须在分析开始前确认**:

- [ ] **目录权限**: `~/.morphism_mapper/` 目录可创建/可写入
- [ ] **子目录权限**: `explorations/`、`domain_results/` 等子目录可创建
- [ ] **文件权限**: 可以创建和修改 `.json` 文件
- [ ] **索引更新**: 可以更新 `index.json` 索引文件
- [ ] **软链接**: 可以创建/更新 `latest` 软链接（非 Windows）

### 🔒 权限最佳实践

#### 1. 预检脚本

**建议用户在首次使用前运行预检**:

```bash
#!/bin/bash
# persistence_check.sh

echo "🔍 检查 Morphism Mapper 持久化权限..."

BASE_DIR="$HOME/.morphism_mapper"

# 检查目录创建
if mkdir -p "$BASE_DIR/test" 2>/dev/null; then
    echo "✅ 目录创建权限正常"
    rm -rf "$BASE_DIR/test"
else
    echo "❌ 无法创建目录 $BASE_DIR"
    echo "请检查文件系统权限："
    echo "  ls -la $HOME/ | grep morphism"
    exit 1
fi

# 检查文件写入
if echo "test" > "$BASE_DIR/write_test" 2>/dev/null; then
    echo "✅ 文件写入权限正常"
    rm "$BASE_DIR/write_test"
else
    echo "❌ 无法写入文件"
    exit 1
fi

echo "🎉 所有权限检查通过！"
```

#### 2. 自定义路径支持

**允许用户指定自定义持久化路径**:

```python
def create_exploration_dir_custom(problem: str, custom_base: str = None) -> str:
    """
    创建探索目录（支持自定义基础路径）
    """
    if custom_base:
        base_path = os.path.expanduser(custom_base)
        # 验证自定义路径的权限
        if not os.access(base_path, os.W_OK):
            raise PermissionError(f"没有写入权限：{base_path}")
    else:
        base_path = os.path.expanduser("~/.morphism_mapper/explorations")
    
    # 继续创建子目录...
```

#### 3. 失败恢复机制

**如果写入过程中失败，必须优雅降级**:

```python
def safe_write_file(filepath: str, content: str, max_retries: int = 3):
    """
    安全写入文件，失败时提供恢复选项
    """
    for attempt in range(max_retries):
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已保存: {filepath}")
            return True
            
        except PermissionError as e:
            print(f"❌ 写入失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                # 最终失败，提供备选方案
                print("\n⚠️ 无法持久化，备选方案：")
                print(f"1. 手动创建目录: mkdir -p {os.path.dirname(filepath)}")
                print(f"2. 更改路径权限: chmod 755 {os.path.dirname(filepath)}")
                print(f"3. 使用内存模式继续（功能受限）")
                return False
        except Exception as e:
            print(f"❌ 意外错误: {e}")
            return False
```

### 🚫 禁止行为

以下行为在 v4.5.2+ 中被视为严重违规：

| 违规行为 | 风险等级 | 后果 |
|---------|---------|------|
| **跳过权限检查直接分析** | 🔴 Critical | 可能导致 Round 2 无法读取 Round 1 结果 |
| **在内存中缓存而不写入** | 🔴 Critical | 进程重启后所有分析丢失 |
| **用户拒绝授权后仍强制继续** | 🟡 High | 用户体验差，分析质量无法保证 |
| **使用 `/tmp` 而不告知用户** | 🟡 High | 临时文件可能被清理，用户不知情 |
| **写入失败时静默忽略** | 🔴 Critical | 用户误以为已保存，实际未持久化 |

### ✅ 合规检查示例

**合规的执行流程**:

```python
def run_morphism_analysis(problem: str):
    """
    合规的 Morphism Mapper 执行流程
    """
    
    # 1. 权限预检
    print("🔍 Step 0: 检查持久化权限...")
    passed, message = check_persistence_prerequisites()
    
    if not passed:
        print(f"\n{message}")
        # 必须申请权限
        if not request_user_permission(message):
            print("\n❌ 无法获得持久化权限，分析终止")
            print("建议：")
            print("  1. 手动创建目录: mkdir -p ~/.morphism_mapper")
            print("  2. 检查磁盘空间: df -h")
            print("  3. 检查文件系统权限")
            return None
    
    # 2. 创建探索目录
    print("\n📁 Step 0.1: 创建探索目录...")
    exploration_path = create_exploration_dir(problem)
    print(f"   探索路径: {exploration_path}")
    
    # 3. 确认写入成功
    test_file = os.path.join(exploration_path, ".persistence_verified")
    try:
        with open(test_file, 'w') as f:
            f.write("verified")
        os.remove(test_file)
        print("   ✅ 持久化验证通过")
    except Exception as e:
        print(f"   ❌ 持久化验证失败: {e}")
        return None
    
    # 4. 继续标准分析流程...
    print("\n🚀 开始分析流程...")
    # ... TeamCreate, Agent 启动等
```

---

### 历史探索索引

所有探索自动记录在 `~/.morphism_mapper/explorations/index.json`：

```json
{
  "explorations": [
    {
      "id": "20260210_143052_人在AI时代如何快速学习成长",
      "problem": "人在AI时代如何快速学习成长",
      "timestamp": "2026-02-10T14:30:52",
      "domains": ["evolutionary_biology", "information_theory", "neuroscience"],
      "status": "completed",
      "path": "~/.morphism_mapper/explorations/20260210_143052_人在AI时代如何快速学习成长"
    }
  ],
  "total_count": 1,
  "latest": "20260210_143052_人在AI时代如何快速学习成长"
}
```
```

### 各Agent的持久化责任

#### 1. Domain Agent (ROUND 1)

**输出要求**:
```yaml
# MAPPING_RESULT_ROUND1必须包含：
domain: "domain_name"
timestamp: "ISO 8601格式"
round: 1
problem: "原始问题"
category_skeleton:
  objects: [...]
  morphisms: [...]
concept_mapping: {...}
insights: [...]
verification_proof: {...}
confidence_assessment: {...}
```

**保存指令**（Agent必须在输出末尾包含）:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json
content: <完整JSON内容>
```

**Team Lead注入的环境变量**: 每个Agent启动时，Team Lead会将 `${MORPHISM_EXPLORATION_PATH}` 注入到Agent上下文中。

#### 2. Obstruction Theorist

**输入**: 读取 `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`

**重要**: Team Lead会将当前探索路径通过环境变量 `${MORPHISM_EXPLORATION_PATH}` 注入到你的上下文中。务必使用此变量构建文件路径。

**输出要求**:
```json
{
  "obstruction_id": "{domain}_round1",
  "theorist": "obstruction-theorist",
  "agent_target": "{domain}",
  "attack_matrix": {
    "dimension_i": {...},
    "dimension_ii": {...},
    "dimension_iii": {...}
  },
  "feedback": {
    "status": "REQUIRES_REVISION | PASS",
    "critical_issues": [...],
    "revision_requirements": [...]
  },
  "diagnosis": "30字风险预警",
  "risk_tags": [...]
}
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json
```

**注意**: 使用 `${MORPHISM_EXPLORATION_PATH}` 环境变量，由Team Lead注入。

#### 3. Domain Agent (ROUND 2)

**输入**（必须读取）:
1. 自己的第一轮输出: `${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round1.json`
2. Obstruction反馈: `${MORPHISM_EXPLORATION_PATH}/obstruction_feedbacks/{domain}_obstruction.json`

**重要**: 使用 `${MORPHISM_EXPLORATION_PATH}` 环境变量构建路径，由Team Lead在启动时注入。

**修正要求**:
```yaml
# MAPPING_RESULT_ROUND2必须包含：
revision_note: "基于obstruction反馈的修正"
revision_focus: ["问题1", "问题2", "问题3"]  # 对应三大攻击点

# 必须回应的字段
obstruction_response: |
  针对性回应审查意见：
  1. 问题1：修正内容...
  2. 问题2：修正内容...
  3. 问题3：修正内容...

# 新增/修正的洞察（带边界声明）
insights:
  - theorem: "定理名称"
    insight: "修正后的洞察"
    limitation: "【新增】本映射的适用边界：..."
    correction: "【修正】根据obstruction反馈：..."
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/domain_results/{domain}_round2.json
```

**注意**: 使用 `${MORPHISM_EXPLORATION_PATH}` 环境变量。

#### 4. Synthesizer

**输入**（读取所有ROUND2结果）:
```python
import os

# 从环境变量获取当前探索路径
EXPLORATION_PATH = os.environ.get("MORPHISM_EXPLORATION_PATH")

for domain in selected_domains:
    round2_file = f"{EXPLORATION_PATH}/domain_results/{domain}_round2.json"
    # 读取并整合
```

**重要**: `${MORPHISM_EXPLORATION_PATH}` 由Team Lead注入。

**输出要求**:
```json
{
  "synthesis_metadata": {
    "domains_integrated": [...],
    "rounds": ["{domain}_round2", ...],
    "obstruction_feedback_integrated": true
  },
  "limits": [...],      // 跨域共识
  "colimits": [...],    // 互补整合
  "final_answer": "...",
  "solution_recommendations": [...],
  "uncertainty_acknowledgment": "...",
  "validation_checklist": [...]
}
```

**保存指令**:
```
===SAVE_TO_FILE===
filepath: ${MORPHISM_EXPLORATION_PATH}/final_reports/synthesis.json
```

**注意**: 使用 `${MORPHISM_EXPLORATION_PATH}` 环境变量，最终报告保存在当前探索目录中。

### 完整流程示例（带持久化）

```python
import os
from datetime import datetime

# Step 0: Team Lead 创建统一的问题子目录 (新增)
exploration_path = create_exploration_dir(problem="人在AI时代如何快速学习成长")
os.environ["MORPHISM_EXPLORATION_PATH"] = exploration_path
print(f"探索目录创建: {exploration_path}")

# Phase 1: Domain Agents ROUND 1
for domain in selected_domains:
    task = Task(
        name=f"{domain}-agent",
        prompt=f"""
        ...分析指令...
        
        ## 持久化要求
        当前探索路径: {exploration_path}
        保存位置: {exploration_path}/domain_results/{domain}_round1.json
        """,
        subagent_type="general"
    )
    # Agent输出保存到: {exploration_path}/domain_results/{domain}_round1.json

# Phase 2: Obstruction Theorist 审查
for domain in selected_domains:
    task = Task(
        name="obstruction-theorist",
        prompt=f"""
        读取 {exploration_path}/domain_results/{domain}_round1.json
        执行四维十二式攻击审查
        保存反馈到: {exploration_path}/obstruction_feedbacks/{domain}_obstruction.json
        """,
        subagent_type="general"
    )
    # 反馈保存到: {exploration_path}/obstruction_feedbacks/{domain}_obstruction.json

# Phase 3: Domain Agents ROUND 2（关键：读取历史）
for domain in selected_domains:
    task = Task(
        name=f"{domain}-agent",
        prompt=f"""
        ## 历史文件读取（必须）
        你必须先读取以下文件：
        1. {exploration_path}/domain_results/{domain}_round1.json
        2. {exploration_path}/obstruction_feedbacks/{domain}_obstruction.json
        
        基于第一轮结果 + 审查反馈，生成MAPPING_RESULT_ROUND2
        保存到: {exploration_path}/domain_results/{domain}_round2.json
        """,
        subagent_type="general"
    )
    # 修正输出保存到: {exploration_path}/domain_results/{domain}_round2.json

# Phase 4: Synthesizer 整合
task = Task(
    name="synthesizer",
    prompt=f"""
    读取目录: {exploration_path}/domain_results/*_round2.json
    执行跨域整合
    保存最终报告到: {exploration_path}/final_reports/synthesis.json
    """,
    subagent_type="general"
)
# 最终报告保存到: {exploration_path}/final_reports/synthesis.json

# Phase 5: 更新元数据
metadata_path = os.path.join(exploration_path, "metadata.json")
with open(metadata_path, "r") as f:
    metadata = json.load(f)
metadata["status"] = "completed"
metadata["domains"] = selected_domains
with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ 探索完成，所有文件保存在: {exploration_path}")
print(f"📊 查看索引: ~/.morphism_mapper/explorations/index.json")
```

### 关键检查点

**Domain Agent ROUND 2必须验证**:
- [ ] 是否成功读取了 `_round1.json`?
- [ ] 是否成功读取了 `_obstruction.json`?
- [ ] `obstruction_response` 是否逐条回应了审查意见?
- [ ] 修正内容是否针对三大攻击点?

**Obstruction Theorist必须验证**:
- [ ] 是否读取了Domain Agent的完整输出（而非仅摘要）?
- [ ] 三维攻击是否都基于Domain的具体内容?
- [ ] 30字诊断是否准确概括风险?

**Synthesizer必须验证**:
- [ ] 是否读取了所有Domain的ROUND2结果?
- [ ] Limits是否真实反映了跨域共识?
- [ ] Colimits是否正确整合了各域独特贡献?

### 向后兼容

| 版本 | 持久化方式 | 特点 |
|------|-----------|------|
| v4.4.x | `/tmp/morphism_mapper/` | 临时目录，所有探索混在一起 |
| **v4.5.0** | `/tmp/morphism_mapper/` 或 `~/.morphism_mapper/` | 统一根目录，但仍混在一起 |
| **v4.5.1+** | `~/.morphism_mapper/explorations/{problem}/` | **按问题子目录组织** (推荐) |

**生产环境要求**: 必须使用v4.5.1+统一问题子目录流程
**快速探索场景**: 可使用简化版，但需在报告中标注

---

### 持久化最佳实践

#### 1. 目录结构导航

```bash
# 查看最新探索
ls -la ~/.morphism_mapper/explorations/latest/

# 查看所有历史探索
ls -la ~/.morphism_mapper/explorations/

# 按时间排序
cd ~/.morphism_mapper/explorations && ls -lt | head -20
```

#### 2. 问题子目录命名规则

```
{timestamp}_{problem_slug}/
```

- `timestamp`: `YYYYMMDD_HHMMSS` 格式
- `problem_slug`: 问题前30个字符，空格替换为下划线
- 示例: `20260210_143052_人在AI时代如何快速学习成长`

#### 3. 元数据文件 (`metadata.json`)

每个探索自动包含元数据：

```json
{
  "exploration_id": "20260210_143052_人在AI时代如何快速学习成长",
  "problem": "人在AI时代如何快速学习成长",
  "timestamp": "2026-02-10T14:30:52",
  "domains": ["evolutionary_biology", "information_theory", "neuroscience"],
  "status": "completed",
  "rounds": 2,
  "overall_confidence": 0.72
}
```

#### 4. 清理旧探索

```python
import os
import shutil
from datetime import datetime, timedelta

# 清理30天前的探索
def cleanup_old_explorations(days=30):
    base_path = os.path.expanduser("~/.morphism_mapper/explorations")
    cutoff = datetime.now() - timedelta(days=days)
    
    for item in os.listdir(base_path):
        if item in ["index.json", "latest"]:
            continue
        item_path = os.path.join(base_path, item)
        # 解析时间戳
        try:
            item_time = datetime.strptime(item[:15], "%Y%m%d_%H%M%S")
            if item_time < cutoff:
                shutil.rmtree(item_path)
                print(f"已清理: {item}")
        except:
            pass

# 保留最近的N个探索
def keep_recent_explorations(n=10):
    base_path = os.path.expanduser("~/.morphism_mapper/explorations")
    dirs = [d for d in os.listdir(base_path) 
            if d not in ["index.json", "latest"] and os.path.isdir(os.path.join(base_path, d))]
    dirs.sort(reverse=True)  # 时间戳倒序
    
    for old_dir in dirs[n:]:
        shutil.rmtree(os.path.join(base_path, old_dir))
        print(f"已删除旧探索: {old_dir}")
```

---

## 🔄 Adaptive Domain Expansion (ADE) 机制 (v4.5.3+)

**全称**: Adaptive Domain Expansion - 置信度驱动的自适应领域扩展

**核心参数** (硬编码，不可配置):

| 参数 | 值 | 说明 |
|------|-----|------|
| **触发阈值** | 60% | 平均置信度 < 0.60 时触发扩展 |
| **最大领域数** | 10 | 无论何种情况，领域数量 ≤ 10 |
| **最大轮次** | 6轮 (3次往返) | Round 6 结束时强制终止 |
| **扩展批次** | 1-2个/次 | 每次扩展引入 1-2 个新领域 |
| **模式** | 全自动 | 无需用户确认，自动触发 |

### ADE 触发条件 (Trigger Conditions)

**在 Round 2 完成后 (或任意偶数轮完成后)，系统自动评估**:

```python
def evaluate_expansion_need(exploration_state):
    """
    ADE 触发评估函数
    在每次偶数轮完成后自动调用
    """
    
    # 终止条件检查 (优先级最高)
    if exploration_state.current_round >= 6:
        return "TERMINATE", "已达最大轮次限制 (6轮)"
    
    if len(exploration_state.domains) >= 10:
        return "TERMINATE", "已达最大领域限制 (10个)"
    
    # 置信度评估
    avg_confidence = calculate_average_confidence(exploration_state.round_results)
    
    if avg_confidence >= 0.60:
        return "TERMINATE", f"置信度达标 ({avg_confidence:.2f} ≥ 0.60)"
    
    # 触发扩展
    return "EXPAND", f"置信度不足 ({avg_confidence:.2f} < 0.60)，触发ADE"
```

### ADE 扩展策略 (Expansion Strategies)

与初始领域选择的"标签匹配"不同，ADE 使用**"缺口填补"策略**:

#### 策略 1: 冲突解决型 (Conflict Resolution)
当现有领域间存在未解决的冲突时:
- 识别冲突的核心维度
- 选择能够调和矛盾的领域
- **示例**: Evolutionary Biology (利用) vs Information Theory (学习) → 引入 Education Science

#### 策略 2: 盲区覆盖型 (Blind Spot Coverage)
当问题关键维度未被覆盖时:

```python
def identify_blind_spots(problem, current_results):
    """
    识别未被充分覆盖的问题维度
    """
    dimensions = {
        'cognitive': ['学习', '记忆', '决策'],
        'emotional': ['焦虑', '动机', '意义感'],
        'social': ['人际关系', '社会地位', '代际'],
        'economic': ['收入', '职业安全', '市场价值'],
        'technological': ['AI工具', '数字素养', '技术接受度']
    }
    # 返回覆盖度 < 50% 的维度
    # 为这些维度匹配最适合的领域
```

#### 策略 3: 桥接型 (Bridging)
当两个领域存在逻辑断层时:
- 引入能够建立连接的中介领域
- 形成更完整的理论链条

### ADE 执行流程

```
Round 2 完成
    ↓
系统自动评估触发条件
    ↓
IF 置信度 >= 60% OR 轮次 = 6 OR 领域数 = 10:
    → 进入 Synthesizer 最终整合
ELSE:
    → 执行 ADE 扩展流程
        ↓
    Step 1: 选择扩展策略 (基于缺口分析)
        ↓
    Step 2: 生成候选领域 (1-2个)
        ↓
    Step 3: 加载 ADE 专用 Prompt
        ↓
    Step 4: 启动新 Domain Agents (Round 3)
        ↓
    Step 5: 新领域必须过 Obstruction 审查
        ↓
    Step 6: 如需修正，进入 Round 4
        ↓
    回到评估点 (检查是否继续扩展)
```

### ADE 与标准流程的集成

```python
# 在 Swarm Orchestrator 中的集成点

class SwarmOrchestrator:
    
    def run_exploration(self, problem):
        # 标准启动流程
        self.initialize(problem)
        self.run_round_1()
        self.run_obstruction_round_1()
        self.run_round_2()  # 修正轮
        
        # ADE 集成点
        while True:
            decision, reason = self.ade.evaluate_expansion_need(self.state)
            
            if decision == "TERMINATE":
                self.logger.info(f"ADE终止: {reason}")
                break
            
            elif decision == "EXPAND":
                self.logger.info(f"ADE扩展: {reason}")
                expansion_plan = self.ade.generate_expansion_plan()
                self.execute_expansion(expansion_plan)
                # 新领域也必须过 obstruction 和 revision
                self.run_obstruction_for_new_domains()
                self.run_revision_for_new_domains()
                # 继续循环，检查是否需要进一步扩展
        
        # 最终整合
        self.synthesizer.generate_final_report()
```

### ADE 终止条件 (强制执行)

无论何种情况，以下任一条件触发即强制终止:

1. **轮次上限**: Round 6 结束 (已完成 3 次往返)
2. **领域上限**: 领域数量达到 10 个
3. **置信度达标**: 平均置信度 ≥ 60%
4. **边际收益不足**: 新增领域后置信度提升 < 5%
5. **系统资源限制**: API 调用成本超过阈值 (可配置)

### ADE 质量检查点

**每次扩展后必须验证**:

- [ ] 新领域是否重复已有分析?
- [ ] 新领域是否确实填补了识别出的缺口?
- [ ] 新领域结果是否通过 Obstruction 审查?
- [ ] 置信度是否有实质性提升 (≥5%)?
- [ ] 是否引入新的不可调和冲突?

### ADE Prompt 文件位置

ADE 专用 Prompt 模板位于:
```
assets/agents/prompts/ade_expansion_prompt.md
```

Team Lead 在启动扩展阶段 Domain Agent 时，必须加载此 Prompt 而非标准 Prompt。

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

当内置的31个领域无法满足分析需求时，可以通过以下方式新增领域：

**方式1**: 自然语言触发（推荐）
```
"新增心理学领域"
"添加中医领域"
"增加孙子兵法领域"
"morphism-mapper 需要艺术理论领域"
```
系统会自动识别意图并执行 `/morphism-add-domain` 命令。

**方式2**: 使用 add-domain 命令（手动）
```python
/morphism-add-domain "中医"
/morphism-add-domain "孙子兵法"
/morphism-add-domain "art_theory"
```

**方式3**: On-the-fly 补盲生成（自动）

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
| **v4.5.5** | **2026-02-10** | **模拟模式必须读取领域文件** - 修复之前未读取 references/{domain}_v2.md 的严重缺陷、强制读取流程、V2标准引用要求 |
| **v4.5.4** | **2026-02-10** | **模拟模式持久化强制规范** - 明确模拟模式(一人分饰多角)也必须自动持久化、添加执行时机表、自动执行代码模板 |
| **v4.5.3** | **2026-02-10** | **ADE 自适应扩展机制** - 置信度60%触发、最大10领域、6轮强制终止、全自动扩展、缺口填补策略 |
| **v4.5.2** | **2026-02-10** | **强制持久化与权限管理** - 写入权限前置检查、按需申请权限、临时模式降级、禁止行为清单 |
| **v4.5.1** | **2026-02-10** | **统一持久化架构** - 按问题子目录组织、自动索引、软链接管理 |
| **v4.5** | **2026-02-10** | **统一问题子目录架构** - 所有探索按问题维度组织 |
| v4.4.3 | 2026-02-09 | 动态Agent生成 + 完整定理保留 |
| v4.4 | 2026-02-09 | 合并Lead+Broadcaster职责，优化信息流 |
| v4.0 | 2026-02-07 | 纯Swarm Mode，废弃Fast Mode |

---

**核心记忆点**：3个关键Agent + SendMessage通信 + 动态Domain Agent生成
