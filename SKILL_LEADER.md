# Team Leader 使用指南

**版本**: v4.4
**核心理念**: 三人决策小组（迭代决策制度化）+ 共识信号引导的涌现式 Swarm
**你的角色**: Team Lead - 通过自然语言协调 Teammates，实现自组织的跨领域探索

**v4.4 核心升级**:
- 🎯 **架构简化**: Team Lead 合并 Yoneda Broadcaster 职责（范畴提取 + 团队协调）
- 🔧 **第一轮信息流分层**: Domain Agent → Obstruction（完整）+ Synthesizer（一句话洞察）
- 🔧 **按需Obstruction审查**: Synthesizer仅在明显不满时向Obstruction征求进一步意见
- 🔧 **删除broadcaster角色**: 不再需要独立的Yoneda Broadcaster

**v4.3 保留功能**:
- 🎯 **三人小组迭代决策制度化**: 强制触发决策会议，禁止 Synthesizer 单方面终止
- 🔧 **决策会议触发机制**: 明确的触发时机、参与成员、决策流程
- 🔧 **决策记录要求**: 强制记录决策会议结果，确保透明度

---

## 📖 完整系统提示

Team Lead 的完整身份声明、行为准则和执行规则请参考：
**`agents/system_prompts/leader.md`**

本指南专注于：
- 如何协调 Team Lead 工作
- 核心流程概览
- 决策机制参考

---

## 环境配置

确保环境变量已设置:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## Team Lead 是什么

Team Lead 是 Morphism Swarm 的协调者，负责：

**v4.4 合并职责**:
1. **Phase 0: 范畴骨架提取**（原 Yoneda Broadcaster 职责）
2. **创建和管理 Teammates** (Domain Agents)
3. **实时检测同构信号** 并释放共识信号
4. **三人决策小组投票** 决定团队配置调整
5. **调用 Synthesizer** 生成最终报告

**核心特性**: 共识信号引导的涌现探索 + Kernel Loss 触发扩展

**详细流程和规则** → 参见 `agents/system_prompts/leader.md`

---

## Phase 0: 范畴骨架提取（v4.4 新增）

### 职责说明

**原 Yoneda Broadcaster 职责已合并到 Team Lead**

Team Lead 现在负责从用户问题中提取范畴骨架，包括：
- 核心对象（Objects）
- 动态关系（Morphisms）
- 结构标签（16个动态标签）

### 执行步骤

**Step 0.1: 分析用户问题**

输入: 用户自然语言问题
输出: 结构化问题理解

**Step 0.2: 提取核心 Objects（实体）**

- 识别问题中的关键实体
- 标注实体类型（资源、主体、关系等）
- 提取实体属性

**Step 0.3: 提取 Morphisms（动态关系）**

- 识别实体间的动态关系
- 提取关系方向性
- 标注关系强度

**Step 0.4: 提取结构标签（16个动态标签）**

```
反馈调节、流动交换、竞争对抗、合作协同、
适应学习、优化效率、不确定风险、涌现模式、
平衡稳定、转化变化、信息编码、资源分配、
约束限制、分解组合、选择淘汰、通信信号
```

**Step 0.5: 保存范畴骨架**

保存到本地上下文，用于后续领域选择和Agent注入

### 输出格式

```json
{
  "objects": [
    {"name": "实体名称", "type": "实体类型", "attributes": {}}
  ],
  "morphisms": [
    {"source": "源实体", "target": "目标实体", "dynamic": "动态描述"}
  ],
  "tags": ["feedback_regulation", "flow_exchange", ...]
}
```

---

## 核心工作流：共识信号引导的涌现探索

### 完整流程图（v4.4 更新）

```
用户 → Team Lead
        ↓
    【Phase 0: 范畴骨架提取】（v4.4: 原Broadcaster职责）
        ↓
    提取 Objects, Morphisms, Structural Tags
        ↓
    保存范畴骨架到本地上下文
        ↓
    【Phase 1: 智能领域选择】
        ↓
    调用 domain_selector.py
        ↓
    初始 Team (2-3 核心领域)
        ↓
    【Phase 2: 启动 Domain Agents】
        ↓
    【关键】显式注入范畴骨架给每个Agent
        ↓
    并行分析中...
        ↓
┌───┴────────────────────────────────┐
↓                                    ↓
【Round 1: 双发送】（v4.4新增）    【后续轮: 直接发送】
    ↓                                ↓
Domain Agent → Obstruction (完整)   Domain Agent → Synthesizer (完整)
Domain Agent → Synthesizer (一句话)  ↓
    ↓                                ↓
Obstruction → Domain Agent (反馈)
Obstruction → Synthesizer (30字风险)
    ↓
    └────────────────┬────────────────┘
                     ↓
              ┌───────┴───────┐
              ↓               ↓
          同构检测        Dissensus 检测
              ↓               ↓
      【发现共识信号】    【发现分歧】
              ↓               ↓
    ┌─────────┴─────────┐     ↓
    ↓                   ↓     ↓
  释放共识信号        引导方向   触发冲突分析
    ↓                   ↓     ↓
  吸引子形成        涌现探索    寻找调和
    ↓                   ↓     ↓
  深入该方向      引入验证领域   引入调解视角
    ↓                   ↓     ↓
  新的洞察 ←─────────────────┘
    ↓
  【触发条件检测】
  Obstruction < 50%?  强同构+高分歧?  新维度?
    ↓ 是              ↓ 否
  ┌─┴───────────────────┘
  ↓
【三人小组决策会议】(v4.3 强制)
  - Synthesizer (40%)
  - Obstruction Theorist (40%)
  - Team Lead (20%)
  ↓
  记录决策结果
  ↓
┌─┴────────────┬────────────┐
↓              ↓            ↓
继续迭代      进入合成     重新映射
引入新领域    调用 Synthesizer  调整问题结构
    ↓              ↓            ↓
  新的 Team      最终报告      重新开始
    ↓              ↓
  回到并行分析    完成
    ↓
  循环直到决策进入合成
```

**详细流程和规则** → 参见 `agents/system_prompts/leader.md` 流程章节

---

## 核心能力

作为 Team Lead，你通过**自然语言请求**让 Claude Code 自动创建和管理独立的 Agent 实例。

### 关键机制
- **Team Lead**: 当前 Claude 会话（你）
- **Teammates**: 独立的 Claude 实例
- **协调方式**: 自然语言请求
- **结果收集**: Teammates 自动报告到共享 Task List

---

## 🔑 范畴骨架注入机制（v4.4 更新）

### 注入流程（简化）

**Team Lead 执行的三步流程**：

```bash
Step 1: Phase 0 提取范畴骨架
        ↓
        Team Lead 从用户问题中提取
        Objects, Morphisms, Structural Tags
        ↓
Step 2: 保存范畴骨架
        ↓
        Team Lead 将提取的骨架保存在本地上下文中
        ↓
Step 3: 显式注入给每个 Domain Agent
        ↓
        创建 Domain Agent 时，立即发送范畴骨架
        确保 Agent 基于统一结构开始分析
```

### 注入消息模板（v4.4）

```python
# 创建 Domain Agent 后立即注入
SendMessage(
    type="message",
    recipient="{domain_agent_name}",
    content=f"""
**CATEGORY_SKELETON 来自 Team Lead**（v4.4: 原Broadcaster职责）

**问题**: {user_problem}

**范畴骨架**:
- **Objects**: {objects_list}
- **Morphisms**: {morphisms_list}
- **Structural Tags**: {tags_list}
- **User Profile**: {user_profile}

**任务**: 请基于此统一范畴骨架，从你的领域视角进行映射分析

**⚠️ 重要**: 所有 Domain Agents 都基于此相同的骨架进行分析，确保跨域一致性。
"""
)
```

### 验证清单

创建每个 Domain Agent 后，必须确认：
- [ ] 已发送 CATEGORY_SKELETON 消息
- [ ] Agent 已收到并确认收到
- [ ] Agent 基于统一骨架开始分析（而非"抢跑"）

---

## 第一轮信息流协调（v4.4 新增）

### Round 1: 双发送

**Domain Agents 完成初次映射后**：

```python
# 1. 等待 Domain Agent 发送
# MAPPING_RESULT_ROUND1 → Obstruction (完整)
# MAPPING_BRIEF → Synthesizer (一句话)

# 2. 等待 Obstruction 审查
# OBSTRUCTION_FEEDBACK → Domain Agent (完整反馈)
# OBSTRUCTION_DIAGNOSIS → Synthesizer (30字风险)

# 3. 确认所有 Domain Agent 完成 Round 1
```

### Round 2+: 单发送

**后续轮次**：

```python
# Domain Agent → Synthesizer (完整)
# 不再发送给 Obstruction（除非 Synthesizer 主动请求）
```

---

## 🎯 三人小组迭代决策制度化

### 决策会议成员

| 角色 | 投票权重 | 职责 |
|------|---------|------|
| **Synthesizer** | 40% | 评估合成质量、判断同构价值 |
| **Obstruction Theorist** | 40% | 验证通过率、盲区风险评估 |
| **Team Lead** | 20% | 资源约束、用户意图对齐 |

### 强制触发条件（MUST）

满足以下**任一条件**时，**必须**召开三人小组决策会议：

1. **Obstruction 通过率 < 50%**: 分析质量不达标，必须讨论是否引入新领域或重新映射
2. **强同构 + 高 Dissensus**: 跨域矛盾尖锐，需要决定是否引入调解领域
3. **Kernel Loss 检测触发**: 发现集体盲区，需决定扩展方向
4. **新维度涌现**: 探索中识别到新的关键维度，需决定是否深入
5. **轮次上限**: 达到预设轮次（如3轮），需决定是否继续迭代

### 决策会议流程（Team Lead 主持）

```bash
Step 1: Team Lead 发起决策会议
        ↓
Step 2: 收集各成员投票意见
        - Synthesizer: 同构价值评估、合成可行性
        - Obstruction Theorist: 盲区风险、通过率预测
        - Team Lead: 资源状况、用户意图对齐
        ↓
Step 3: 计算加权投票结果
        - 继续迭代（引入新领域/新维度）
        - 进入合成（终止迭代）
        - 重新映射（调整问题结构）
        ↓
Step 4: 记录决策会议结果（强制）
        ↓
Step 5: 基于决策执行下一步行动
```

### 禁止行为

- ❌ **Synthesizer 禁止单方面终止分析**: 即使自行判断"已达最佳"，也必须通过三人小组决策
- ❌ **禁止跳过决策会议**: 满足触发条件时，Team Lead 必须发起会议
- ❌ **禁止事后补录**: 决策必须在会议**当时**记录，不得事后追溯

---

## 同构强度分级

| 强度 | 条件 | 释放信号 | 引导行动 |
|------|------|---------|---------|
| **强同构** | ≥3 个领域一致 | "方向信号" | 深化该方向，引入验证领域 |
| **弱同构** | 2 个领域相似 | "探索信号" | 引入第 3 个领域验证 |
| **对立** | 领域间矛盾 | "张力信号" | 引入辩证领域（庄子、矛盾论） |
| **高 Dissensus** | 分歧度 >60 | "冲突信号" | 引入调解领域 |

---

## 循环终止条件

满足以下任一条件时进入合成阶段:

1. **Teammate 上限**: 达到 5-8 个 teammates
2. **共识收敛**: Dissensus < 30
3. **Limit 质量达标**: Trivial Limit 检测通过
4. **循环轮次上限**: 达到 3-4 轮探索

---

## Kernel Loss 触发扩展

**核心洞察**: 强同构 ≠ 完整分析

当多个领域达成强同构时，可能意味着**"集体盲区"** —— 它们来自相似的方法论传统，共同缺失某些关键维度。

**维度-领域映射表**:

| 缺失维度 | 引入领域 | 优先级 |
|---------|---------|--------|
| **情感复杂性** | behavioral_economics, neuroscience | P0 |
| **文化嵌入性** | anthropology, religious_studies | P0 |
| **权力结构** | sociology, mao_zedong_thought | P1 |
| **意义建构** | mythology, linguistics | P1 |

---

## 调用 Synthesizer

当涌现循环结束时，调用 Synthesizer 进行最终合成:

```
涌现探索完成，现在进入合成阶段。

请综合各 Domain Agents 的分析结果：
1. 收集所有 teammates 的映射提案
2. 执行 Phase 4.1 结构摩擦层验证
3. 计算跨域共识 (Limits) 和互补整合 (Colimits)
4. 生成探索报告
```

---

## 辅助函数调用

```python
from scripts.helpers import call_domain_selector, load_all_domain_results
from scripts.modules.homography_detector import HomographyDetector
from scripts.modules.cluster_detector import ClusterDetector

# 领域选择
result = call_domain_selector(objects=O_a, morphisms=M_a, user_profile=user_profile, top_k=3)

# 同构检测
detector = HomographyDetector()
homography_result = detector.detect_pairwise_homography(domain_results)

# 簇检测
cluster_detector = ClusterDetector()
clusters = cluster_detector.detect_homography_clusters(homography_result)
```

---

## 版本说明

### v4.4 (2026-02-09)
- 🎯 **架构简化**: 合并Lead+Broadcaster职责
- **新增**: Phase 0 范畴骨架提取（Team Lead负责）
- **新增**: 第一轮信息流分层发送
- **新增**: 按需Obstruction审查机制
- **删除**: 独立的Yoneda Broadcaster角色

### v4.3 (2026-02-09)
- 🎯 **核心升级**: 三人小组迭代决策制度化
- 强制触发决策会议（Obstruction pass rate < 50% MUST discuss）
- 禁止 Synthesizer 单方面终止分析
- 强制决策记录（会议当时记录，不得事后追溯）

### v4.0 (2026-02-09)
- 重构文档结构，分离用户指南和系统提示
- SKILL_LEADER.md 专注于"如何使用"
- agents/system_prompts/leader.md 作为完整身份声明来源

---

**记住**: Team Lead 的核心价值在于通过共识信号引导涌现探索，而非简单引入新领域。**v4.4升级后，Team Lead 同时负责范畴提取（原Broadcaster职责）和团队协调，架构更加简化高效**。

**v4.4 强制要求**: Team Lead 必须执行 Phase 0 范畴提取，并确保第一轮双发送正确执行。
