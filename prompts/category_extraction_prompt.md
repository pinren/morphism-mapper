# Phase 0: 范畴骨架提取提示词

**版本**: v1.0
**用途**: Team Lead 在 Phase 0 中使用此提示词提取精细范畴骨架

---

## 提示词模板

```
你是 Category Extraction Specialist，负责从用户问题中提取精细的范畴骨架。

**你的任务**：
从用户问题中提取 Objects（实体）和 Morphisms（动态关系），并为每个 Morphism 标注 8 个精细维度。

**输出格式**（JSON）：
```json
{
  "objects": [
    {"name": "实体名", "type": "类型", "attributes": {"属性": "值"}}
  ],
  "morphisms": [
    {
      "from": "源实体",
      "to": "目标实体",
      "relation_type": "关系类型",
      "dynamics": "动态描述",
      "temporal_type": "瞬时|延迟|持续|累积",
      "direction_type": "单向|双向|循环",
      "intensity_level": "弱|中|强|指数级",
      "feedback_type": "无|正反馈|负反馈|复合反馈",
      "reversibility_type": "可逆|不可逆|条件可逆",
      "conditions": ["触发条件"],
      "effects": ["主要效果"],
      "side_effects": ["副作用"]
    }
  ],
  "structural_tags": ["从以下标签中选择3-5个最相关的：feedback_regulation, flow_exchange, competition_conflict, cooperation_synergy, adaptation_learning, optimization_efficiency, uncertainty_risk, emergence_pattern, equilibrium_stability, transformation_change, information_encoding, resource_allocation, constraint_limitation, decomposition_composition, selection_elimination, communication_signaling"]
}
```

**8 个精细维度判断标准**：

1. **temporal_type (时间维度)**：
   - 瞬时：立即发生，如"命令下达"
   - 延迟：有滞后效应，如"培训→能力提升"
   - 持续：持续不断，如"信任关系"
   - 累积：越来越强，如"利润分红"

2. **direction_type (方向性)**：
   - 单向：A → B，如"利润分配"
   - 双向：A ↔ B，如"信任关系"
   - 循环：A → B → A，如"反馈回路"

3. **intensity_level (强度)**：
   - 弱：轻微影响
   - 中：明显影响
   - 强：重大影响，改变结构
   - 指数级：临界点、蝴蝶效应

4. **feedback_type (反馈类型)**：
   - 无反馈：一次性事件
   - 正反馈：越...越...，如"口碑→更多客户"
   - 负反馈：趋向平衡，如"温控"
   - 复合反馈：多重反馈交织

5. **reversibility_type (可逆性)**：
   - 可逆：可以撤销
   - 不可逆：无法回头，如"信任破裂"
   - 条件可逆：有条件可撤销

6. **conditions (触发条件)**：
   - 什么情况下这个关系会发生？
   - 需要满足什么前提？

7. **effects (主要效果)**：
   - 这个关系会带来什么直接结果？

8. **side_effects (副作用)**：
   - 伴随的负面影响是什么？

**用户问题**：
{USER_PROBLEM}

**请按上述格式输出 JSON**。
```

---

## 示例输入输出

### 输入
```
郑州一老板效仿胖东来，利润一半给员工、不打卡考勤，负债百万逆风翻盘，怎么做到的？
```

### 输出
```json
{
  "objects": [
    {"name": "老板", "type": "决策者", "attributes": {"风险承受": "高"}},
    {"name": "员工", "type": "执行者", "attributes": {"激励敏感": "高"}},
    {"name": "企业", "type": "组织系统", "attributes": {"状态": "转型中"}},
    {"name": "客户", "type": "价值接收者", "attributes": {}}
  ],
  "morphisms": [
    {
      "from": "老板",
      "to": "员工",
      "relation_type": "利润分配",
      "dynamics": "50%利润分红给员工",
      "temporal_type": "累积",
      "direction_type": "单向",
      "intensity_level": "强",
      "feedback_type": "正反馈",
      "reversibility_type": "不可逆",
      "conditions": ["企业盈利"],
      "effects": ["员工激励增加", "归属感提升", "服务质量改善"],
      "side_effects": ["老板短期收入减少", "现金流压力"]
    },
    {
      "from": "老板",
      "to": "员工",
      "relation_type": "信任授予",
      "dynamics": "不打卡考勤，给予员工自主权",
      "temporal_type": "持续",
      "direction_type": "双向",
      "intensity_level": "中",
      "feedback_type": "正反馈",
      "reversibility_type": "条件可逆",
      "conditions": ["员工表现良好"],
      "effects": ["自主权提升", "心理安全感增加"],
      "side_effects": ["管理难度增加"]
    },
    {
      "from": "负债状态",
      "to": "盈利状态",
      "relation_type": "逆境转化",
      "dynamics": "通过管理模式创新实现逆风翻盘",
      "temporal_type": "延迟",
      "direction_type": "单向",
      "intensity_level": "指数级",
      "feedback_type": "复合反馈",
      "reversibility_type": "不可逆",
      "conditions": ["员工响应积极", "市场接受度提升"],
      "effects": ["企业摆脱负债", "实现盈利增长"],
      "side_effects": ["管理模式被模仿"]
    }
  ],
  "structural_tags": [
    "cooperation_synergy",
    "resource_allocation",
    "feedback_regulation",
    "emergence_pattern"
  ]
}
```

---

## Team Lead 使用流程

```
Step 1: 复制提示词模板
Step 2: 替换 {USER_PROBLEM} 为用户问题
Step 3: 发送给 LLM，获取 JSON 输出
Step 4: 验证 JSON 格式正确性
Step 5: 将 morphisms 列表传递给 domain_selector.py
```

---

## 快速参考卡

### 时间维度判断
| 关键词 | 类型 |
|--------|------|
| 立即、瞬间、下达 | 瞬时 |
| 滞后、之后、逐步 | 延迟 |
| 持续、不断、长期 | 持续 |
| 累积、越来越多、复利 | 累积 |

### 方向性判断
| 关键词 | 类型 |
|--------|------|
| 分配、给予、发送 | 单向 |
| 互动、交流、合作 | 双向 |
| 反馈、循环、迭代 | 循环 |

### 强度判断
| 关键词 | 类型 |
|--------|------|
| 轻微、小幅 | 弱 |
| 明显、有效 | 中 |
| 重大、根本性、改变 | 强 |
| 临界、爆发、指数 | 指数级 |

### 反馈判断
| 关键词 | 类型 |
|--------|------|
| 越来越、滚雪球 | 正反馈 |
| 趋向、稳定、调节 | 负反馈 |
| 复杂、交织、多重 | 复合 |

---

**记住**：精细提取不是增加复杂度，而是让后续的领域选择更准确。投入时间在 Phase 0，会节省后续迭代时间。
