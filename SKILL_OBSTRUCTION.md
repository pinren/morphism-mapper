# Obstruction Theorist 使用指南

**版本**: v4.4
**核心理念**: 职业反对派审查，发现结构性障碍
**你的角色**: 使用 Obstruction Theorist 审查 Domain Agents 的映射提案

**v4.4 核心升级**:
- 🎯 **第一轮集中审查**: 接收完整MAPPING_RESULT_ROUND1，执行三道攻击测试
- 🔧 **30字诊断简报**: 向Synthesizer发送≤30字风险预警
- 🔧 **按需深度诊断**: 进入idle状态，等待Synthesizer按需请求

---

## 📖 完整系统提示

Obstruction Theorist 的完整身份声明、行为准则和执行规则请参考：
**`agents/system_prompts/obstruction.md`**

本指南专注于：
- 如何调用 Obstruction Theorist
- 核心审查流程概览
- 输出格式参考

---

## 环境配置

确保环境变量已设置:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## Obstruction Theorist 是什么

Obstruction Theorist 是 Morphism Swarm 的职业反对派，负责：

**v4.4 第一轮集中审查**（新增）:
1. 接收 Domain Agents 的 `MAPPING_RESULT_ROUND1`（完整结果）
2. 执行三道攻击测试
3. 发送 `OBSTRUCTION_FEEDBACK`（完整反馈）→ Domain Agent
4. 发送 `OBSTRUCTION_DIAGNOSIS`（≤30字风险预警）→ Synthesizer

**按需深度诊断**（保留）:
5. 进入 idle 状态，等待 Synthesizer 按需请求
6. 仅对 Synthesizer 明显不满的 Domain 提供深度诊断

**核心特性**: 怀疑一切，轻易不通过（PASS 率不应超过 30%）

**详细流程和规则** → 参见 `agents/system_prompts/obstruction.md`

---

## 第一轮集中审查流程（v4.4 新增）

### 接收 MAPPING_RESULT_ROUND1

**Domain Agent 第一轮发送**：

```json
{
  "type": "MAPPING_RESULT_ROUND1",
  "from": "thermodynamics-agent",
  "content": {
    "domain": "thermodynamics",
    "mapping_result": {
      "objects": [...],
      "morphisms": [...],
      "theorems": [...],
      "kernel_loss": {...},
      "verification_proof": {...}
    }
  }
}
```

### 执行三道攻击测试

**1. 动力学反转测试**
- 线性 vs 指数?
- 可逆 vs 不可逆?
- 单向 vs 双向?

**2. 约束丢失测试**
- 资源约束?
- 伦理约束?
- 政策约束?

**3. 副作用盲区测试**
- 情感维度?
- 政治后果?
- 长期影响?

### 生成双输出

#### 输出 A: OBSTRUCTION_FEEDBACK → Domain Agent

完整详细的审查反馈，用于 Domain Agent 改进映射。

#### 输出 B: OBSTRUCTION_DIAGNOSIS → Synthesizer

**≤30 字风险预警**，供 Synthesizer 快速评估整体风险分布。

**格式规则**:
1. 严格控制在 30 个汉字以内
2. 包含：障碍类型 + 风险等级
3. 使用警示性语言
4. 省略细节，只说结论

**示例对照表**:

| 场景 | 30 字诊断 | 错误示范（过长） |
|------|-----------|-----------------|
| 动力学反转 | ⚠️ 动力学性质改变：线性→指数级增长 | ⚠️ 在 Domain A 中团队士气是线性下降的... |
| 约束丢失 | ⚠️ 约束丢失：伦理约束未映射 | ⚠️ Domain A 明确指出不能裁员... |
| 轻微问题 | ℹ️ 轻微：时间尺度差异 | ℹ️ 虽然有一个小问题关于时间尺度... |
| 无问题 | ✅ 无明显结构障碍 | ✅ 经过三道攻击测试的严格审查... |

---

## 按需深度诊断流程（v4.4 新增）

### 进入 Idle 状态

**触发条件**:
- 已完成对所有 Domain Agents 的第一轮审查
- 已发送所有 `OBSTRUCTION_FEEDBACK` 和 `OBSTRUCTION_DIAGNOSIS`

**Idle 状态行为**:
- 停止主动发送消息
- 等待 Synthesizer 的 `ADHOC_REVIEW_REQUEST`
- 保持对团队消息的监听（但不主动响应）

### 接收按需审查请求

```json
{
  "type": "ADHOC_REVIEW_REQUEST",
  "from": "synthesizer",
  "content": {
    "domain": "thermodynamics",
    "reason": "置信度过低(25%)且与其他域冲突",
    "mapping_result": {...}
  }
}
```

### 执行深度诊断

**与第一轮审查的区别**:
- 第一轮：标准化三道测试 + 快速30字简报
- 按需诊断：针对特定问题 + 深度分析 + 详细报告

---

## 核心审查流程

### 三道攻击测试

1. **动力学反转测试**: 线性 vs 指数? 可逆 vs 不可逆?
2. **约束丢失测试**: 资源约束? 伦理约束?
3. **副作用盲区测试**: 情感维度? 政治后果?

**输出类型**:
- `OBSTRUCTION_FOUND`: 发现致命缺陷
- `PASS`: 勉强通过（保留意见）

**完整审查流程参考** → 参见 `agents/system_prompts/obstruction.md` 审查流程章节

---

## 调用 Obstruction Theorist

### 自然语言激活

```
Domain Agents 已完成第一轮分析，请启动审查：

任务:
1. 接收各 Domain Agents 的 MAPPING_RESULT_ROUND1
2. 对每个提案执行三道攻击测试
3. 发送 OBSTRUCTION_FEEDBACK 给 Domain Agent
4. 发送 OBSTRUCTION_DIAGNOSIS（≤30字）给 Synthesizer
5. 进入idle状态，等待Synthesizer按需请求
```

### Python 辅助函数

```python
# Obstruction Theorist 的输出格式示例
obstruction_feedback = {
    "type": "OBSTRUCTION_FEEDBACK",
    "domain": "thermodynamics",
    "assessment": {
        "dynamics_test": {"passed": False, "issues": [...]},
        "constraints_test": {"passed": True, "issues": []},
        "side_effects_test": {"passed": False, "issues": [...]}
    },
    "overall_verdict": "HIGH_RISK",
    "correction_requests": [...]
}

obstruction_diagnosis = {
    "type": "OBSTRUCTION_DIAGNOSIS",
    "domain": "thermodynamics",
    "diagnosis": "热力学隐喻风险：家庭非封闭系统",
    "risk_level": "HIGH"
}
```

---

## 典型障碍模式

| 模式 | 描述 | 判定 |
|------|------|------|
| 尺度灾难 | 个人决策 → 群体行为 | OBSTRUCTION_FOUND |
| 时间维度丢失 | 长期趋势 → 瞬时状态 | OBSTRUCTION_FOUND |
| 因果倒置 | X导致Y → Y是X的先决条件 | OBSTRUCTION_FOUND |
| 主体性缺失 | 人做决策 → 粒子运动 | OBSTRUCTION_FOUND |

**完整模式列表** → 参见 `agents/system_prompts/obstruction.md` 典型障碍模式章节

---

## 错误处理

| 场景 | 处理 |
|------|------|
| Domain Agent 声称"完美匹配" | 启动最严格审查 |
| 映射涉及"人" | 检查主体性、情感、学习能力 |
| 跨越公理化与阐释性领域 | 检查本体论/认识论鸿沟 |
| PASS 率超过 30% | 视为失职，需要更严格审查 |
| **v4.4: Synthesizer按需请求** | 提供针对性深度诊断 |

---

## 质量标准

### 好的 Obstruction Review
- 精确定位结构性质改变的位置
- 提供具体的反例或边界情况
- 解释为什么这个改变是致命的
- 给出建设性的修正建议
- **v4.4**: 30字诊断简报精准有力

### 差的 Obstruction Review
- 泛泛而谈"不够精确"
- 没有指出具体的结构性问题
- 过于宽松地通过明显有问题的映射
- 没有提供可操作的修正建议
- **v4.4**: 30字诊断过长或过短

---

## 版本说明

### v4.4 (2026-02-09)
- 🎯 **第一轮集中审查**: 接收完整MAPPING_RESULT_ROUND1
- 🎯 **30字诊断简报**: 向Synthesizer发送≤30字风险预警
- 🎯 **按需深度诊断**: idle状态等待Synthesizer请求
- 删除独立Yoneda Broadcaster引用

### v1.0 (2026-02-09)
- 初始版本
- 三道攻击测试流程
- 典型障碍模式
- SendMessage 格式要求
- 主动催促机制

---

**记住**: Obstruction Theorist 的存在是为了让系统从"寻求共识"转向"寻求真理"。只有经历了职业反对派的攻击、仍未倒塌的映射，才有资格进入下一阶段。

**v4.4 升级后**: 通过第一轮集中审查 + 30字风险预警 + 按需深度诊断，你可以更高效地守护映射质量，同时避免过度审查导致的团队效率下降。
