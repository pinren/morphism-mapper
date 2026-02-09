# Synthesizer 使用指南

**版本**: v4.4
**核心理念**: 通过 Phase 4.1 结构摩擦层，确保只有经过严格验证的映射才能进入合成
**你的角色**: 使用 Synthesizer 将 Domain Agents 的结果合成为 Limit 和 Colimit

**v4.4 核心升级**:
- 🎯 **第一轮信息接收变更**: 只接收一句话洞察（MAPPING_BRIEF），不接收完整结果
- 🔧 **按需Obstruction调用**: 仅在对某Domain"明显不满"时征求Obstruction意见
- 🔧 **参与三人小组决策**: 禁止单方面终止分析

---

## 📖 完整系统提示

Synthesizer 的完整身份声明、行为准则和执行规则请参考：
**`agents/system_prompts/synthesizer.md`**

本指南专注于：
- 如何调用 Synthesizer
- 核心流程概览
- 输出格式参考

---

## 环境配置

确保环境变量已设置:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## Synthesizer 是什么

Synthesizer 是 Morphism Swarm 的综合者，负责：
1. **提取跨域共识** (Limit): 所有同构簇都认同的核心洞察
2. **生成互补整合方案** (Colimit): 各领域独特贡献的组合

**核心特性**: Phase 4.1 结构摩擦层（四道防线）
- Blind Signature Collection（结构指纹聚类）
- Kernel Loss Protocol（强制声明映射损耗）
- Obstruction Theorist Review（职业反对派审查）
- Round-Trip Check（语义漂移检测，按需）

**v4.4 新增特性**:
- 第一轮轻量级接收（MAPPING_BRIEF一句话洞察）
- 按需Obstruction深度诊断（避免过度审查）

**详细流程和规则** → 参见 `agents/system_prompts/synthesizer.md`

---

## 第一轮信息流处理（v4.4 新增）

### 接收 MAPPING_BRIEF

**Domain Agent 第一轮发送**：

```json
{
  "type": "MAPPING_BRIEF",
  "from": "thermodynamics-agent",
  "content": {
    "domain": "thermodynamics",
    "core_insight": "熵增定律揭示婆媳关系必然走向无序"
  }
}
```

**处理动作**:
- 记录到 `round1_briefs[domain]`
- 提取核心洞察关键词
- 初步判断该域的价值方向

### 接收 OBSTRUCTION_DIAGNOSIS

**Obstruction 第一轮审查后**：

```json
{
  "type": "OBSTRUCTION_DIAGNOSIS",
  "from": "obstruction-theorist",
  "content": {
    "domain": "thermodynamics",
    "diagnosis": "热力学隐喻风险：家庭非封闭系统",
    "risk_level": "HIGH"
  }
}
```

**处理动作**:
- 记录到 `obstruction_diagnoses[domain]`
- 结合 MAPPING_BRIEF 评估该域可靠性
- 标记高风险域用于后续深度审查

---

## 按需 Obstruction 调用（v4.4 新增）

### 触发条件

仅在对某Domain结论"明显不满"时向Obstruction征求进一步意见：

**条件1**: 置信度 < 30%
**条件2**: 与其他域严重冲突
**条件3**: 核心洞察模糊或不完整
**条件4**: Obstruction首轮标记为HIGH_RISK

### 发送按需审查请求

```python
SendMessage(
    type="message",
    recipient="obstruction-theorist",
    content=f"""
## ADHOC_REVIEW_REQUEST

**目标Domain**: {domain}

**不满意原因**: {reason}

**该Domain的映射结果**:
{mapping_result_json}

---
**Synthesizer 请求按需审查**
"""
)
```

### 接收按需诊断

```json
{
  "type": "ADHOC_DIAGNOSIS",
  "from": "obstruction-theorist",
  "content": {
    "domain": "thermodynamics",
    "specific_issue": "响应具体问题",
    "deep_analysis": {...},
    "recommendation": "建议保留/替换/修正"
  }
}
```

**处理动作**:
- 根据 recommendation 更新该域权重
- 如建议替换，标记该域为待替换
- 继续执行 Limits/Colimits 计算

---

## 核心输出格式

Synthesizer 生成包含以下内容的探索报告：

1. **探索概览**: 用户问题、参与 Agents、探索时长
2. **第一轮信息汇总**: Briefs + Obstruction诊断（v4.4新增）
3. **Phase 4.1 验证结果**: 四道防线的执行结果
4. **同构簇发现**: 识别的同构簇及其共享结构
5. **Trivial Limit 检测**: 通用形容词检测、结构性描述验证
6. **【极限提取】- 跨域元逻辑**: Limit 输出
7. **【余极限整合】- 互补方案**: Colimit 输出
8. **质量评估**: 整体质量评级（MINIMAL/ACCEPTABLE/EXCELLENT）

**完整输出格式参考** → 参见 `agents/system_prompts/synthesizer.md` 输出格式章节

---

## 三人小组决策会议

### 触发条件

第一轮映射完成后，Team Lead 自动召集决策会议。

### 参会成员

- **Team Lead** (主席)
- **Obstruction Theorist**
- **Synthesizer** (你)

### 会议流程

**Step 1: 评估当前状态**

你报告：
```markdown
## Synthesizer 状态报告

### 收集的 Briefs
- thermodynamics: "熵增定律揭示..."
- game_theory: "零和博弈假设失效..."
- control_systems: "正反馈回路导致..."

### Obstruction 诊断
- thermodynamics: 🔴 HIGH - "家庭非封闭系统"
- game_theory: 🟡 MEDIUM - "忽视情感非理性"
- control_systems: 🟢 LOW - "无明显风险"

### 初步评估
- 高价值域: control_systems
- 需修正域: thermodynamics
- 可替换域: game_theory
```

**Step 2: 讨论 Obstruction 发现的问题**

**Step 3: 决策**

投票选项：
- A: 启动第二轮迭代（要求 Domain Agent 修正）
- B: 替换高风险域（引入新领域）
- C: 接受当前结果（进入最终综合）

**⚠️ 重要约束**

**你无权单方面决定终止分析！**
必须通过三人小组投票决定。

---

## 调用 Synthesizer

### 自然语言激活

```
涌现探索完成，现在进入合成阶段。

请综合各 Domain Agents 的分析结果：
1. 收集所有 teammates 的映射提案
2. 执行 Phase 4.1 结构摩擦层验证
3. 计算跨域共识 (Limits) 和互补整合 (Colimits)
4. 生成探索报告
```

### Python 辅助函数

```python
from scripts.helpers import load_all_domain_results

# 加载所有 Domain Agent 结果
results = load_all_domain_results(["thermodynamics", "control_systems"])

# 调用同构检测
import sys
sys.path.insert(0, "scripts/modules")
from homography_detector import HomographyDetector
from cluster_detector import ClusterDetector

detector = HomographyDetector()
homography_result = detector.detect_pairwise_homography(results)

cluster_detector = ClusterDetector()
clusters = cluster_detector.detect_homography_clusters(homography_result)
```

---

## 质量标准

### 好的 Synthesis
- Limit 有洞察性（不只是陈述事实）
- Limit 包含结构性描述
- Limit 不依赖通用形容词
- Colimit 可执行（不是空泛建议）
- 逻辑自洽（Limit 和 Colimit 不矛盾）
- 尊重用户约束（符合用户画像）
- **v4.4**: 正确使用按需Obstruction调用

### 差的 Synthesis
- Limit 太泛（"需要创新"这种空话）
- Limit 使用通用形容词逃避具体分析
- Trivial Limit 检测未通过
- Colimit 只是罗列（没有整合逻辑）
- 忽略用户资源（建议无法执行）
- 强行整合（忽略领域间的冲突）
- **v4.4**: 过度调用Obstruction（降低效率）
- **v4.4**: 从不调用Obstruction（错失高风险域）

---

## 错误处理

| 场景 | 处理 |
|------|------|
| 无同构簇 | 执行 Koan Break |
| 单个 Agent 成功 | 报告该领域洞察，标记"需验证" |
| Agents 结论冲突 | 启动 conflict_analyzer |
| Trivial Limit | 重新挖掘或启动 conflict_analyzer |
| 高 Dissensus (>60) | 强制启动 conflict_analyzer |
| 超时 | 基于已收集结果生成部分报告 |
| **v4.4: 对某Domain明显不满** | 按需调用Obstruction深度诊断 |

---

## 版本说明

### v4.4 (2026-02-09)
- 🎯 **第一轮信息接收变更**: 只接收一句话洞察（MAPPING_BRIEF）
- 🎯 **按需Obstruction调用**: 仅在明显不满时征求Obstruction意见
- 🎯 **三人小组决策参与**: 禁止单方面终止分析
- 删除独立Yoneda Broadcaster引用

### v4.0 (2026-02-09)
- 重构文档结构，分离用户指南和系统提示
- SKILL_SYNTHESIZER.md 专注于"如何使用"
- agents/system_prompts/synthesizer.md 作为完整身份声明来源

### v3.0 (2026-02-08)
- 引入 Phase 4.1 结构摩擦层（四道防线）
- Trivial Limit 检测机制
- Dissensus Metric 计算与处理
- 同构簇检测

### v2.0 (2026-02-07)
- 引入 Synthesizer 概念
- Limit/Colimit 计算框架
- 跨域共识提取

---

**记住**: Synthesizer 的核心价值在于通过 Phase 4.1 的四道防线，确保只有经过严格验证的映射才能进入合成。**v4.4升级后，通过第一轮轻量接收+按需Obstruction调用，可以更高效地完成跨域整合**。从"寻求共识"转向"压力测试"，只有经历了 Obstruction Theorist 攻击、通过 Round-Trip 检验、诚实交代 Kernel Loss 的映射，才是真正鲁棒的自然变换。

**v4.4 强制要求**: 参与三人小组决策会议，禁止单方面终止分析。
