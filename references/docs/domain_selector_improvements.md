# Domain Selector 鲁棒性改进方案

## 问题描述

当前 `domain_selector.py` 容易触发缺省行为，导致总是返回相同的 5 个领域 + 庄子作为 wildcard。

**问题根源**：
1. 标签匹配依赖 `dynamics` 字段中的特定关键词
2. 当关键词不匹配时，置信度降到 45-60
3. 低置信度触发 `default_seed_domains` 回退

**当前缺省行为** (`domain_agents.json:434-439`):
```json
"default_seed_domains": [
    "thermodynamics",
    "information_theory",
    "complexity_science",
    "control_systems",
    "game_theory"
]
```

## 改进方案

### 方案 1：多层级匹配策略

**优先级**：
1. **精确关键词匹配**（当前实现）
2. **语义相似度匹配**（新增）
3. **结构相似度匹配**（新增）
4. **最小可用集**（替代 default_seed_domains）

### 方案 2：改进标签覆盖

**问题**：当前 16 个动态标签的关键词覆盖率不足

**改进**：为每个标签增加更多同义词和变体

```python
# 示例：feedback_regulation 标签
"feedback_regulation": {
    "indicators": [
        "反馈", "调节", "控制", # 现有
        "修正", "调整", "适应", "校准", "稳定", # 新增
        "反馈回路", "正反馈", "负反馈", "自我调节" # 新增
    ]
}
```

### 方案 3：动态置信度阈值

**问题**：固定的置信度阈值不适应不同类型的问题

**改进**：根据问题特征动态调整阈值

```python
def _calculate_adaptive_confidence(self, top_domains, user_tags, objects, morphisms):
    """计算自适应置信度"""

    # 基础置信度
    base_confidence = self._calculate_confidence(top_domains, user_tags)

    # 根据问题结构特征调整
    structure_bonus = 0

    # 如果 morphisms 描述详细，提高置信度
    if morphisms:
        avg_dynamics_length = sum(len(m.get('dynamics', '')) for m in morphisms) / len(morphisms)
        if avg_dynamics_length > 30:  # 详细描述
            structure_bonus += 15

    # 如果 objects 数量合理，提高置信度
    if 2 <= len(objects) <= 6:
        structure_bonus += 10

    return min(95, base_confidence + structure_bonus)
```

### 方案 4：最小可用集替代固定缺省

**问题**：5 个固定领域 + 庄子太死板

**改进**：使用"最小可用集"，根据问题类型动态选择

```python
# 最小可用集配置
MINIMAL_VIABLE_SETS = {
    "social": ["game_theory", "network_theory", "social_psychology"],
    "physical": ["thermodynamics", "control_systems", "mechanics"],
    "abstract": ["category_theory", "logic", "epistemology"],
    "practical": ["kaizen", "decision_theory", "mental_models"],
    "default": ["complexity_science", "network_theory", "game_theory"]  # 更小的缺省集
}

def select_minimal_set(problem_type_hint: str) -> List[str]:
    """根据问题类型提示选择最小可用集"""
    return MINIMAL_VIABLE_SETS.get(problem_type_hint, MINIMAL_VIABLE_SETS["default"])
```

### 方案 5：Wildcard 优化

**问题**：庄子几乎总是被选为 wildcard

**改进**：轮换使用不同的 wildcard

```python
WILDCARD_POOL = [
    "zhuangzi", "mythology", "anthropology",
    "religious_studies", "linguistics", "art_theory"
]

def select_wildcard(excluded_domains: List[str]) -> str:
    """轮换选择 wildcard，避免总是庄子"""
    available = [d for d in WILDCARD_POOL if d not in excluded_domains]
    if available:
        # 基于时间戳轮换
        index = int(time.time()) % len(available)
        return available[index]
    return "zhuangzi"  # 最终回退
```

## 实施计划

### Phase 1: 快速修复（v4.4.1）

1. ✅ 移除 SKILL.md 中固定 4 个 objects 的硬约束
2. ⏳ 增加标签同义词覆盖
3. ⏳ 使用更小的缺省集（3个领域）

### Phase 2: 深度改进（v4.5）

1. ⏳ 实现自适应置信度计算
2. ⏳ 实现 wildcard 轮换机制
3. ⏳ 增加语义相似度匹配

## 测试验证

**测试用例**：

| 问题类型 | 预期行为 | 当前行为 |
|---------|---------|---------|
| 简单问题（2-3个 objects） | 选择 2-3 个领域 | 固定 5+1 个领域 |
| 社会科学问题 | 优先选择社会科学领域 | 固定 5 个领域 |
| 抽象问题 | 优先选择哲学/逻辑领域 | 固定 5 个领域 |
| 描述详细的问题 | 提高置信度 | 置信度低 |

## 配置文件修改

### `domain_agents.json`

**删除/减少**：
```json
// 删除或注释掉
// "default_seed_domains": [...]
```

**新增**：
```json
"minimal_viable_sets": {
    "social": ["game_theory", "network_theory", "social_psychology"],
    "physical": ["thermodynamics", "control_systems", "mechanics"],
    "default": ["complexity_science", "network_theory", "game_theory"]
},
"wildcard_pool": ["zhuangzi", "mythology", "anthropology", "religious_studies", "linguistics"]
```

## 向后兼容

- 保留 `default_seed_domains` 配置项（但不使用）
- 保留现有的标签匹配逻辑
- 增加新的匹配层作为补充
