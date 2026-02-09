#!/usr/bin/env python3
"""
Category Extraction Module v1.0
精细范畴提取模块 - 支持 Team Lead 在 Phase 0 中提取更精确的 morphism 结构
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TemporalType(Enum):
    """时间维度"""
    INSTANTANEOUS = "瞬时"  # 立即发生
    DELAYED = "延迟"        # 有延迟
    CONTINUOUS = "持续"     # 持续过程
    CUMULATIVE = "累积"     # 累积效应


class DirectionType(Enum):
    """方向性"""
    UNIDIRECTIONAL = "单向"     # A → B
    BIDIRECTIONAL = "双向"      # A ↔ B
    CYCLIC = "循环"            # A → B → A


class IntensityLevel(Enum):
    """强度级别"""
    WEAK = "弱"
    MODERATE = "中"
    STRONG = "强"
    EXPONENTIAL = "指数级"


class FeedbackType(Enum):
    """反馈类型"""
    NONE = "无反馈"
    POSITIVE = "正反馈"        # 增强效应
    NEGATIVE = "负反馈"        # 衰减效应
    COMPOUND = "复合反馈"      # 复杂反馈


class ReversibilityType(Enum):
    """可逆性"""
    REVERSIBLE = "可逆"
    IRREVERSIBLE = "不可逆"
    CONDITIONALLY_REVERSIBLE = "条件可逆"


@dataclass
class Morphism:
    """
    精细化 Morphism 定义

    示例：
    ```python
    Morphism(
        source="老板",
        target="员工",
        relation_type="利润分配",
        dynamics="50%利润分红给员工",
        temporal_type=TemporalType.CUMULATIVE,
        direction_type=DirectionType.UNIDIRECTIONAL,
        intensity_level=IntensityLevel.STRONG,
        feedback_type=FeedbackType.POSITIVE,
        reversibility_type=ReversibilityType.IRREVERSIBLE,
        conditions=["企业盈利"],
        effects=["员工激励增加", "留存率提升"],
        side_effects=["老板短期收入减少"]
    )
    ```
    """
    # 基础信息
    source: str                      # 源实体
    target: str                      # 目标实体
    relation_type: str               # 关系类型
    dynamics: str                    # 动态描述

    # 精细维度
    temporal_type: TemporalType      # 时间维度
    direction_type: DirectionType    # 方向性
    intensity_level: IntensityLevel  # 强度
    feedback_type: FeedbackType      # 反馈类型
    reversibility_type: ReversibilityType  # 可逆性

    # 约束与效果
    conditions: List[str] = field(default_factory=list)     # 触发条件
    effects: List[str] = field(default_factory=list)        # 主要效果
    side_effects: List[str] = field(default_factory=list)   # 副作用

    # 量化指标（可选）
    magnitude: Optional[float] = None    # 强度数值
    time_lag: Optional[float] = None     # 延迟时间

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "source": self.source,
            "target": self.target,
            "relation_type": self.relation_type,
            "dynamics": self.dynamics,
            "temporal_type": self.temporal_type.value,
            "direction_type": self.direction_type.value,
            "intensity_level": self.intensity_level.value,
            "feedback_type": self.feedback_type.value,
            "reversibility_type": self.reversibility_type.value,
            "conditions": self.conditions,
            "effects": self.effects,
            "side_effects": self.side_effects,
            "magnitude": self.magnitude,
            "time_lag": self.time_lag
        }

    def to_simple_string(self) -> str:
        """转换为简化的字符串格式（用于 domain_selector）"""
        return f"{self.source} → {self.target}: {self.dynamics}"


@dataclass
class CategorySkeleton:
    """
    范畴骨架 - 精细版

    包含 Objects、Morphisms 和结构标签的完整定义
    """
    objects: List[Dict[str, Any]]     # 实体列表
    morphisms: List[Morphism]          # 关系列表（精细版）
    structural_tags: List[str]         # 结构标签
    user_profile: Optional[Dict] = None  # 用户画像

    def to_simple_format(self) -> Dict[str, Any]:
        """转换为简单格式（用于 domain_selector）"""
        return {
            "objects": [obj.get("name", obj) for obj in self.objects],
            "morphisms": [m.to_simple_string() for m in self.morphisms],
            "tags": self.structural_tags
        }


class CategoryExtractor:
    """
    范畴提取器 - 帮助 Team Lead 执行 Phase 0 精细提取
    """

    # 16个动态标签定义
    STRUCTURAL_TAGS = [
        "feedback_regulation",     # 反馈调节
        "flow_exchange",           # 流动交换
        "competition_conflict",    # 竞争对抗
        "cooperation_synergy",     # 合作协同
        "adaptation_learning",     # 适应学习
        "optimization_efficiency", # 优化效率
        "uncertainty_risk",        # 不确定风险
        "emergence_pattern",       # 涌现模式
        "equilibrium_stability",   # 平衡稳定
        "transformation_change",   # 转化变化
        "information_encoding",    # 信息编码
        "resource_allocation",     # 资源分配
        "constraint_limitation",   # 约束限制
        "decomposition_composition",  # 分解组合
        "selection_elimination",   # 选择淘汰
        "communication_signaling"  # 通信信号
    ]

    @classmethod
    def extract_from_case(cls, user_problem: str) -> CategorySkeleton:
        """
        从用户问题中提取精细范畴骨架

        Args:
            user_problem: 用户问题的自然语言描述

        Returns:
            CategorySkeleton 精细版范畴骨架
        """
        # 这里是一个示例实现
        # 实际使用时需要结合 LLM 进行智能提取

        morphisms = []

        # 示例：郑州老板案例
        if "利润" in user_problem and "员工" in user_problem:
            morphisms.append(Morphism(
                source="老板",
                target="员工",
                relation_type="利润分配",
                dynamics="50%利润分红给员工",
                temporal_type=TemporalType.CUMULATIVE,
                direction_type=DirectionType.UNIDIRECTIONAL,
                intensity_level=IntensityLevel.STRONG,
                feedback_type=FeedbackType.POSITIVE,
                reversibility_type=ReversibilityType.IRREVERSIBLE,
                conditions=["企业盈利"],
                effects=["员工激励增加", "归属感提升", "服务质量改善"],
                side_effects=["老板短期收入减少", "现金流压力"],
                magnitude=0.5
            ))

        if "不打卡" in user_problem or "考勤" in user_problem:
            morphisms.append(Morphism(
                source="老板",
                target="员工",
                relation_type="信任授予",
                dynamics="不打卡考勤，给予员工自主权",
                temporal_type=TemporalType.CONTINUOUS,
                direction_type=DirectionType.BIDIRECTIONAL,
                intensity_level=IntensityLevel.MODERATE,
                feedback_type=FeedbackType.POSITIVE,
                reversibility_type=ReversibilityType.CONDITIONALLY_REVERSIBLE,
                conditions=["员工表现良好"],
                effects=["自主权提升", "心理安全感增加"],
                side_effects=["管理难度增加"]
            ))

        if "负债" in user_problem and "翻盘" in user_problem:
            morphisms.append(Morphism(
                source="负债状态",
                target="盈利状态",
                relation_type="逆境转化",
                dynamics="通过管理模式创新实现逆风翻盘",
                temporal_type=TemporalType.DELAYED,
                direction_type=DirectionType.UNIDIRECTIONAL,
                intensity_level=IntensityLevel.EXPONENTIAL,
                feedback_type=FeedbackType.COMPOUND,
                reversibility_type=ReversibilityType.IRREVERSIBLE,
                conditions=["员工响应积极", "市场接受度提升"],
                effects=["企业摆脱负债", "实现盈利增长"],
                side_effects=["管理模式被模仿"],
                time_lag=6.0  # 假设6个月
            ))

        if "客户" in user_problem or "服务质量" in user_problem:
            morphisms.append(Morphism(
                source="员工",
                target="客户",
                relation_type="价值传递",
                dynamics="员工满意度提升转化为服务质量提升",
                temporal_type=TemporalType.CONTINUOUS,
                direction_type=DirectionType.UNIDIRECTIONAL,
                intensity_level=IntensityLevel.MODERATE,
                feedback_type=FeedbackType.POSITIVE,
                reversibility_type=ReversibilityType.CONDITIONALLY_REVERSIBLE,
                conditions=["员工保持积极状态"],
                effects=["客户满意度提升", "客户忠诚度增加"],
                side_effects=[]
            ))

        return CategorySkeleton(
            objects=[
                {"name": "老板", "type": "决策者", "attributes": {"风险承受": "高"}},
                {"name": "员工", "type": "执行者", "attributes": {"激励敏感": "高"}},
                {"name": "企业", "type": "组织系统", "attributes": {"状态": "转型中"}},
                {"name": "客户", "type": "价值接收者", "attributes": {}}
            ],
            morphisms=morphisms,
            structural_tags=[
                "cooperation_synergy",   # 合作协同
                "incentive_design",      # 激励设计（隐含）
                "trust_game",            # 信任博弈（隐含）
                "feedback_regulation",   # 反馈调节
                "emergence_pattern"      # 涌现模式
            ]
        )

    @classmethod
    def infer_structural_tags(cls, morphisms: List[Morphism]) -> List[str]:
        """
        从 morphisms 推断结构标签

        Args:
            morphisms: Morphism 列表

        Returns:
            推断的结构标签列表
        """
        tags = set()

        for m in morphisms:
            # 根据反馈类型推断标签
            if m.feedback_type == FeedbackType.POSITIVE:
                tags.add("emergence_pattern")
            elif m.feedback_type == FeedbackType.NEGATIVE:
                tags.add("equilibrium_stability")

            # 根据方向性推断标签
            if m.direction_type == DirectionType.BIDIRECTIONAL:
                tags.add("cooperation_synergy")
            elif m.direction_type == DirectionType.CYCLIC:
                tags.add("feedback_regulation")

            # 根据关系类型推断标签
            if "利润" in m.relation_type or "资源" in m.relation_type:
                tags.add("resource_allocation")
            if "信任" in m.relation_type:
                tags.add("cooperation_synergy")
            if "信息" in m.relation_type or "信号" in m.relation_type:
                tags.add("communication_signaling")

        return list(tags)


def demo_extraction():
    """演示精细范畴提取"""
    print("=" * 60)
    print("Category Extraction Demo - 郑州老板案例")
    print("=" * 60)

    skeleton = CategoryExtractor.extract_from_case(
        "郑州一老板效仿胖东来，利润一半给员工、不打卡考勤，负债百万逆风翻盘"
    )

    print("\n【Objects (实体)】")
    for obj in skeleton.objects:
        print(f"  - {obj['name']} ({obj['type']})")

    print("\n【Morphisms (关系) - 精细版】")
    for i, m in enumerate(skeleton.morphisms, 1):
        print(f"\n  {i}. {m.source} → {m.target}")
        print(f"     类型: {m.relation_type}")
        print(f"     描述: {m.dynamics}")
        print(f"     时间: {m.temporal_type.value} | 方向: {m.direction_type.value}")
        print(f"     强度: {m.intensity_level.value} | 反馈: {m.feedback_type.value}")
        print(f"     可逆: {m.reversibility_type.value}")
        if m.conditions:
            print(f"     条件: {', '.join(m.conditions)}")
        if m.effects:
            print(f"     效果: {', '.join(m.effects)}")
        if m.side_effects:
            print(f"     副作用: {', '.join(m.side_effects)}")

    print(f"\n【结构标签】")
    print(f"  {', '.join(skeleton.structural_tags)}")

    print("\n【简单格式 (用于 domain_selector)】")
    simple = skeleton.to_simple_format()
    print(f"  Objects: {simple['objects']}")
    print(f"  Morphisms: {simple['morphisms']}")
    print(f"  Tags: {simple['tags']}")


if __name__ == "__main__":
    demo_extraction()
