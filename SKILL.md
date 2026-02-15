---
name: morphism-mapper
description: Category Theory Morphism Mapper v4.7 Swarm Mode - 基于范畴论的跨领域并行探索系统。通过 TeamCreate 探测 + AgentTeam 原子启动 + 严格 JSON Schema 输出，构建可审计、可计算的跨域推理流程。触发关键词包括"看不穿商业模式"、"环境变了需要转型"、"方案如何落地"、"多领域交叉验证"、"新增领域"、"添加领域"等。
---

# Category Theory Morphism Mapper v4.7.0 🐝

**版本**: v4.7.0 (Swarm Mode - 协议统一与可审计数据流)
**更新日期**: 2026-02-15
**版本源**: `assets/version.json`
**领域数量**: 35个内置领域 + 动态新增

**核心升级**:
1. **Obstruction Theorist 升级为五维十四式智能攻击矩阵**
   - 五个维度：动力学、约束条件、认识论、本体论、函子性
   - 3+2 模式：3个智能选择 + 2个强制范畴论检查
   - 智能武器选择（根据问题特征从14个攻击点中选择最致命的3个）
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
5. **持久化强制规范** (v4.5.4)
   - 无论生产还是 Fallback，持久化都是强制要求
   - Step 0-8 每个步骤对应保存文件清单
6. **领域文件强制读取** (v4.5.5)
   - Domain Agent 必须读取 `references/{domain}_v2.md`
   - 分析必须引用 V2 标准内容 (Core Objects, Core Morphisms, Theorems)
8. **自然变换与交换图校验** (v4.6.0) ⭐⭐
   - **Synthesizer 升级**: 从"总结拼凑"升级为"拓扑一致性校验"
   - **结构化输出**: Domain Agent 输出 `strategy_topology` JSON
   - **交换性验证**: 自动检测不同领域策略是否同构
   - **分歧报警**: 非交换时触发 Obstruction Alert，不和稀泥


---

## 🚨 运行时模式侦测 — 必须首先执行 (v4.7)

> **本文档默认为 Agent Swarm 生产模式编写。** 仅当环境不支持时才降级。
> **启动协议唯一真相**: `references/docs/bootstrap_contract.md`

### Step 0: 运行时环境检测（启动后立即执行）

**在执行任何分析之前，必须先确认运行模式：**

```
检测流程:
1. 尝试执行 TeamCreate(team_name="morphism-{timestamp}") 创建一个 Team
2. 判断返回结果:

   Case A: TeamCreate 成功 ✅
   → 进入 Agent Swarm 模式（下文所有流程适用）
   → team_name 已知，后续创建 Agents 时使用此 team_name
   
   Case B: 报错 "Already leading team XXX" ⚠️
   → **这不是 Fallback 场景！Team 功能可用！**
   → 获取现有 Team 的 team_name（从错误信息中提取 "XXX"）
   → 使用现有 team_name 继续 Agent Swarm 模式
   → **禁止降级到 Simulation 或创建独立 Task agents**
   
   Case C: 报错 "Feature not available" 或其他不可用错误 ❌
   → 确认 Team 功能不可用
   → 降级到 Fallback 模式
   → 读取 references/docs/simulation_mode_guide.md 获取完整 Fallback 流程
   → 按该文件中的「单 AI 顺序执行」步骤操作
```

**⚠️ 关键规则**:
- **永远先尝试生产模式**，不要预判环境不可用
- **"Already leading team" 不等于失败**，这说明 Team 功能正常工作！
- **只有功能确实不可用时**才降级到 Simulation
- **用户明确要求生产模式时**，必须使用 Agent Swarm，不得自行降级
- **降级后的完整 Fallback 流程不在本文档中**，请参阅 [Simulation Mode Guide](references/docs/simulation_mode_guide.md)

---

## 🟢 Agent Swarm 模式 — Lead Agent 主动驱动工作流

> ⚠️ **核心原则**: Lead Agent 是流程**驱动者**，不是被动等待者。接收用户问题后必须**一口气推进到“由 Synthesizer 产出的最终报告”**。

### Lead Agent 职责清单

| Step | Lead Agent 动作 | 产出 | 通信方式 |
|------|-----------------|------|---------|
| 0 | 环境检测 + 创建探索目录 + 初始化持久化 | `metadata.json` | — |
| 1 | **主动提取范畴骨架** (Objects, Morphisms, Tags) | Category Skeleton JSON | — |
| 2 | 调用 `domain_selector.py` 选择领域 + Tier Balance | 领域列表 | — |
| 3 | 构建首批名册（`obstruction-theorist` + `synthesizer` + 首轮 Domain Agents） | `launch_roster` | — |
| 4 | **AgentTeam 原子化启动首批成员** | Team 会话 | `AgentTeam()` |
| 5 | 监听 Domain Agent JSON 完成 → **推动** Obstruction 审查 | 审查触发 | `SendMessage` |
| 6 | 收集 Obstruction Round 1 反馈（覆盖率=100%）→ **推动** Domain Agent Round 2 | 迭代指令 | `SendMessage` |
| 7 | Obstruction Gate 清空后再**召集三人决策会议** (Synthesizer + Obstruction + Lead) | 会议记录 | `SendMessage` 循环 |
| 8 | 仅在 `OBSTRUCTION_GATE_CLEARED` 后指示 Synthesizer 生成最终报告，更新索引 | 最终报告 | `SendMessage` |

### ❌ Lead Agent 禁止行为
- 未经 TeamCreate() 测试就直接采用 Fallback 模式
- 完成骨架提取后停下来等待用户指令
- 领域选择后不启动 Domain Agents
- Domain Agents 完成后不触发 Obstruction 审查
- Obstruction Round 1 未完成就请求 Synthesizer 产出最终结论
- 被动等待而不主动催促超时的 Agent
- **一个人分饰多角完成全部分析**（这是 Fallback 行为，生产模式禁止）
- **创建 Task() 时缺失 `description` 或 `team_name` 参数**（会触发 InputValidationError 或创建独立 Agent）
- **Synthesizer 未输出时由 Lead 直接写最终报告**（严重协议违规）

### ✅ 关键提醒：所有 Task() 调用必须传入 `description` + `team_name`

```python
# ❌ 错误示范1 - 缺 description，会触发 InputValidationError
Task(name="obstruction-theorist", prompt="...", team_name="morphism-team")

# ❌ 错误示范2 - 缺 team_name，会创建独立 Agent，不属于 Team
Task(name="obstruction-theorist", description="Round 1 schema review", prompt="...")

# ✅ 正确示范 - 在 RUNNING 阶段增量创建 Team 成员
Task(
    name="new-domain-agent",
    description="Analyze selected domain with strict JSON schema",
    prompt="...",
    team_name="morphism-team"
)
```

---

**核心架构**: 3个关键 Agent + 动态 Domain Agents

| Agent | Prompt 路径 | 说明 |
|-------|------------|------|
| **Team Lead** | `assets/agents/system_prompts/leader.md` | 流程协调、范畴提取 |
| **Obstruction** | `assets/agents/system_prompts/obstruction.md` | 攻击测试、质量审查 |
| **Synthesizer** | `assets/agents/system_prompts/synthesizer.md` | 跨域整合、交换图校验 |
**通信铁律**: 只能使用 SendMessage，其他方式会导致 Team 异常
**关键脚本**: `scripts/domain_selector.py` + `scripts/dynamic_agent_generator.py`
**配置路径**: `assets/agents/config/`

---

## 核心架构 (3+N 模型，N 按需生成)

```
┌─────────────────────────────────────────────────────────────┐
│              Morphism Mapper v4.7 核心架构                   │
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
| **Obstruction Theorist** | 首批由 `AgentTeam` 原子启动；仅增量扩展时允许 `Task(..., description=..., team_name=...)` | 三道攻击测试、质量审查、风险预警 | Synthesizer, Team Lead |
| **Synthesizer** | 首批由 `AgentTeam` 原子启动；仅增量扩展时允许 `Task(..., description=..., team_name=...)` | Limits/Colimits计算、跨域整合、最终报告 | 所有成员 |
| **Domain Agent** | 首批由 `AgentTeam` 原子启动；仅增量扩展时允许 `Task(..., description=..., team_name=...)` | 领域分析、映射执行 | Obstruction, Synthesizer |

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
SendMessage → Obstruction Theorist (MAPPING_RESULT_ROUND1 + JSON主体)
SendMessage → Synthesizer (MAPPING_RESULT_JSON + JSON主体)
    ↓
Obstruction Theorist 审查后
    ↓
SendMessage → Synthesizer (30字诊断简报)
    ↓
三人小组决策会议 (SendMessage 循环)
    ↓
Synthesizer 生成最终整合报告，Team Lead 仅转发与持久化
```

---

## 🔍 领域文件读取规范 (v4.7+)

> 无论哪种运行模式，Domain Agent 都必须基于领域知识库进行分析。

**关键要求**:
- **必须读取**: `references/{domain}_v2.md`
- **必须输出**: `domain_file_path` + `domain_file_hash` + `evidence_refs`
- **必须覆盖**: `evidence_refs` 至少包含 `Fundamentals/Core Morphisms/Theorems`
- **必须符合**: `assets/agents/schemas/domain_mapping_result.v1.json`
- **违规后果**: 缺失 `domain_file_hash`、`kernel_loss` 或关键 `evidence_refs` section 的结果将被视为无效

---

## Phase 3: 蜂群组装与启动 (Swarm Assembly)

### 核心脚本: 统一名册构建 (Singleton Aware)

```python
from scripts.dynamic_agent_generator import DynamicAgentGenerator

# 1. 准备核心成员 (仅首次创建)
core_members = []
active_agents = get_active_members()

if "obstruction-theorist" not in active_agents:
    core_members.append({"name": "obstruction-theorist", "prompt": load("obstruction.md")})
if "synthesizer" not in active_agents:
    core_members.append({"name": "synthesizer", "prompt": load("synthesizer.md")})

# 2. 准备动态领域专家 (增量创建)
new_domain_members = []
generator = DynamicAgentGenerator()

for domain in selected_domains:
    if f"{domain}-agent" in active_agents:
        continue  # ✅ 跳过已存在的 Agent
        
    prompt = generator.generate_prompt(domain, category_skeleton)
    new_domain_members.append({"name": f"{domain}-agent", "prompt": prompt})

# 3. 合并新名册
launch_roster = core_members + new_domain_members

# 4. 蜂群原子化启动 (Atomic Swarm Launch)
# 仅启动新成员
if launch_roster:
    AgentTeam(
        team_name="morphism-analysis",
        members=launch_roster,
        shared_context={
            "category_skeleton": category_skeleton,
            "user_profile": user_profile,
            "role": "Morphism Swarm"
        }
    )
```

### 知识来源

1. **内置领域**: `references/{domain}_v2.md` (35个)
2. **自定义领域**: `references/custom/{domain}_v2.md`
3. **动态创建**: 如果不存在，自动生成 V2 标准格式

---

## 执行流程

```
Step 1: TeamCreate(team_name="morphism-team")  # 创建 Team Context
    ↓
Step 2: Team Lead 执行分析 (Analysis Phase)
    ├── 2.1 提取 Category Skeleton (Objects, Morphisms)
    └── 2.2 选择 Domains (Tier Balance Selection)
    ↓
Step 3: 蜂群组装与启动 (Swarm Assembly)
    ├── 构建完整名册: [Obstruction, Synthesizer] + [Domain A, Domain B...]
    └── 蜂群原子化启动: AgentTeam(members, shared_context)
    ↓
Step 4: 蜂群监控 (Monitoring Phase)
    └── 监听分析流与同构信号
    ↓
Step 5: 映射执行与协调
    ├── Domain Agents 分析并发送结果
    ├── Obstruction 执行 Round 1 审查（先过门禁）
    ├── 必要时触发 Domain Round 2 + Obstruction 复审
    └── Obstruction Gate 清空后，Synthesizer 执行最终交换图校验
```

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
                description=f"Round 1 domain mapping for {domain}",
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
                    description=f"Round 1 domain mapping for {domain}",
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
│   ├── commutative_checks/                         # 🆕 交换图校验结果
│   │   └── diagram_report.json
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
    for subdir in ["domain_results", "obstruction_feedbacks", "synthesizer_inputs", "commutative_checks", "final_reports", "logs"]:
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

# 🆕 交换图校验报告
COMMUTATIVE_REPORT = f"{EXPLORATION_PATH}/commutative_checks/diagram_report.json"

# 最终报告
FINAL_REPORT = f"{EXPLORATION_PATH}/final_reports/synthesis.json"
```

### Team Lead 持久化初始化职责

**Step 0: 创建探索目录** (在Step 1之前执行)

```python
# Team Lead 在启动时创建统一的问题子目录
exploration_path = create_exploration_dir(problem=user_problem)  # user_problem 来自用户输入

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
- 交换图报告: {exploration_path}/commutative_checks/diagram_report.json
- 最终报告: {exploration_path}/final_reports/synthesis.json
- 执行日志: {exploration_path}/logs/
"""
```

---

## 🚨 强制持久化与权限管理 (v4.5.2+)

> **详细指南**: 请参阅 [Persistence Guide](references/docs/persistence_guide.md) 获取完整的权限管理、失败恢复机制、合规检查清单及各 Agent 的详细持久化责任规范。

**核心规则**:
1. **写入权限前置检查**: 分析前必须确认权限，否则无法启动。
2. **按需申请**: 权限不足时自动引导用户授权。
3. **禁止行为**: 严禁跳过检查、内存缓存、静默失败等行为。

**文件架构**:
- 探索记录: `~/.morphism_mapper/explorations/{timestamp}_{problem_slug}/`
- 索引文件: `~/.morphism_mapper/explorations/index.json`
- 最新链接: `~/.morphism_mapper/explorations/latest`

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
    → 仅当 Obstruction Gate 已清空时进入 Synthesizer 最终整合
    → 否则先完成 Obstruction 审查闭环
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
TeamCreate(team_name="xxx")
AgentTeam(
    team_name="xxx",
    members=[obstruction_member, synthesizer_member, domain_members...],
    shared_context={...}
)

# ❌ 错误：重复创建 team-lead
Task(name="team-lead", description="duplicate lead launch", team_name="xxx")
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
# 1. TeamCreate 探测（含 Already leading team 分支）
# 2. 提取 Category Skeleton
# 3. domain_selector 选择领域
# 4. DynamicAgentGenerator 生成 Prompts（注入 domain_file_path/hash）
# 5. AgentTeam 原子启动首批成员（Core + Domain）
# 6. Domain Agents 发送严格 JSON 映射结果
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

当内置的35个领域无法满足分析需求时，可以通过以下方式新增领域：

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

### 进阶范畴论模块 (Advanced Modules)

当标准流程 (Limits/Colimits) 无法满足特定分析需求时，可使用以下指令召唤高阶范畴论模块：

**1. Adjoint Balancer (伴随平衡器)**
- **命令**: `/morphism-balance`
- **用途**: 在"理想脑洞" (Left Adjoint) 与"现实约束" (Right Adjoint) 之间寻找最优平衡点 (Unit)。
- **场景**: 方案太虚无法落地，或方案太实缺乏创新。

**2. Kan Extension (坎扩展全息缩放器)**
- **命令**: `/morphism-scale`
- **用途**: 将局部验证成功的模式扩展到全局 (Left Kan 激进扩展 / Right Kan 保守扩展)。
- **场景**: "这个模式在A地成功了，如何复制到B地？"

**3. Yoneda Probe (米田引理探针)**
- **命令**: `/morphism-yoneda`
- **用途**: 当对象信息不透明时，通过其与周围环境的交互关系 (Hom-sets) 反推其本质。
- **场景**: 分析竞品、黑盒系统或信息缺失的对象。

**4. Koan Break (禅宗公案中断器)**
- **命令**: `/morphism-koan`
- **用途**: 当问题存在逻辑悖论或范畴错误时，提供重构提问而非直接解答。
- **场景**: "如何让圆变成方？"、陷入逻辑死循环。

**5. Natural Transformation (自然变换引擎)**
- **命令**: `/morphism-pivot` (Mode C: 策略演化)
- **命令**: `/morphism-view` (Mode A: 视角对齐)
- **命令**: `/morphism-zoom` (Mode B: 颗粒度缩放)
- **用途**: 处理多视角对齐、战略执行断层或环境变化时的策略平滑迁移。
- **场景**: "技术和业务打架"、"战略无法落地"、"市场环境变了"。

**6. Limits & Colimits (极限与余极限 - 手动模式)**
- **命令**: `/morphism-limit` (提取共同核心)
- **命令**: `/morphism-colimit` (整合互补洞察)
- **用途**: 手动触发标准流程的特定计算步骤。

**7. Monad Risk Container (风险容器)**
- **命令**: `/morphism-risk`
- **用途**: 对方案进行法律、成本、信任维度的风险校验。
- **场景**: 也就是 `/morphism-monad`。

---

## 文件结构

```
morphism-mapper/
├── SKILL.md                          # 本文件
├── references/                       # 领域知识库
│   ├── docs/                         # 文档目录
│   │   ├── persistence_guide.md      # 持久化指南
│   │   └── simulation_mode_guide.md  # 模拟模式指南
│   ├── game_theory_v2.md
│   ├── thermodynamics_v2.md
│   └── custom/                       # 自定义领域
├── scripts/
│   ├── domain_selector.py            # 智能领域选择
│   ├── dynamic_agent_generator.py    # 动态Agent生成
│   └── commands/
│       └── add-domain.md             # 新增领域命令

```

---

## 版本历史

| 版本 | 日期 | 核心更新 |
|-----|------|---------|
| **v4.7.0** | **2026-02-15** | **协议统一与可审计输出** - 新增 Bootstrap Contract 单一真相；Domain Agent 强制输出 `domain_mapping_result.v1` JSON（含 `domain_file_hash`/`evidence_refs`）；Synthesizer/Obstruction 仅消费结构化数据 |
| **v4.6.0** | **2026-02-14** | **自然变换与交换图校验** - Domain Agent 输出结构化拓扑，Synthesizer 执行交换性验证，非交换触发报警；从"散沙"升级为"混凝土" |
| **v4.5.7** | **2026-02-12** | **生产模式优先** - SKILL.md 默认为 Agent Swarm 编写，运行时 Task() 测试侦测，仅失败时降级到 Fallback；移除文档中的模拟模式偏向 |
| **v4.5.6** | **2026-02-12** | **运行模式自动侦测** - 自动识别 Agent Swarm 环境，智能降级到模拟模式 |
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
