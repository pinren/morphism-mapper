#!/usr/bin/env python3
"""
Domain Selector - 智能领域选择器 (v4.0)
基于Morphism结构匹配的智能领域选择算法
支持 v4.0 Tier Balance 和 complexity_tier
"""

import json
import os
import random
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class MorphismTag:
    """Morphism标签定义"""
    name: str
    description: str
    indicators: List[str]
    related_tags: List[str]
    opposite_tags: List[str]
    example_domains: List[str]
    weight: float = 1.0

@dataclass
class DomainMatch:
    """领域匹配结果"""
    domain: str
    score: float
    complexity_tier: str
    tier_strength: float
    best_matches: List[Dict[str, Any]]
    reasoning: str

@dataclass
class TierBalanceResult:
    """Tier Balance 选择结果"""
    selected_domains: List[str]
    wildcard_domain: Optional[str]
    tier_distribution: Dict[str, List[str]]
    reasoning: str

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，便于序列化和外部调用"""
        return {
            'selected_domains': self.selected_domains,
            'wildcard_domain': self.wildcard_domain,
            'tier_distribution': self.tier_distribution,
            'reasoning': self.reasoning,
        }

class DomainSelector:
    """智能领域选择器 v4.0"""

    def __init__(
        self,
        tags_file: Optional[str] = None,
        agents_file: Optional[str] = None
    ):
        """
        初始化领域选择器

        Args:
            tags_file: morphism_tags.json文件路径，默认为assets目录
            agents_file: domain_agents.json文件路径，默认为agents/config目录
        """
        script_dir = Path(__file__).parent.parent

        # 加载 morphism_tags.json
        if tags_file is None:
            tags_file = str(script_dir / "assets" / "morphism_tags.json")
        self.tags_data = self._load_tags(tags_file)
        self.tags = self._parse_tags()
        self.domain_tag_mapping = self.tags_data.get("tag_relationships", {}).get("domain_tag_mapping", {})
        self.scoring_rules = self.tags_data.get("scoring_rules", {})
        self.complexity_thresholds = self.tags_data.get("complexity_thresholds", {})

        # 加载 domain_agents.json (v4.0)
        if agents_file is None:
            agents_file = str(script_dir / "agents" / "config" / "domain_agents.json")
        self.agents_data = self._load_agents(agents_file)
        self.domain_info = self.agents_data.get("domains", {})
        self.complexity_tiers = self.agents_data.get("complexity_tiers", {})
        self.wildcard_candidates = self.agents_data.get("wildcard_candidates", [])
        self.default_seed_domains = self.agents_data.get("default_seed_domains", [])

        # v4.4.1 新增：最小可用集和 wildcard 轮换
        self.minimal_viable_sets = self.agents_data.get("minimal_viable_sets", {})
        self.wildcard_rotation_config = self.agents_data.get("wildcard_rotation", {})

    def _load_tags(self, tags_file: str) -> Dict:
        """加载标签定义文件"""
        with open(tags_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_agents(self, agents_file: str) -> Dict:
        """加载领域代理配置文件"""
        with open(agents_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _parse_tags(self) -> Dict[str, MorphismTag]:
        """解析标签定义"""
        tags = {}
        for tag_id, tag_data in self.tags_data.get("tags", {}).items():
            tags[tag_id] = MorphismTag(
                name=tag_data["name"],
                description=tag_data["description"],
                indicators=tag_data["indicators"],
                related_tags=tag_data["related_tags"],
                opposite_tags=tag_data["opposite_tags"],
                example_domains=tag_data["example_domains"],
                weight=tag_data.get("weight", 1.0)
            )
        return tags

    def extract_user_tags(self, morphisms: Optional[List[Dict[str, str]]]) -> List[str]:
        """
        从用户Morphism中提取标签

        Args:
            morphisms: 用户问题的Morphism列表（标准字典格式）
                [{"from": "A", "to": "B", "dynamics": "描述"}, ...]
                兼容字段名: from/source/src, to/target/dst, dynamics/description/relation/type

        Returns:
            提取的标签列表
        """
        if morphisms is None:
            return []

        user_tags = set()

        # 字段名映射表（兼容多种命名风格）
        source_fields = ["from", "source", "src", "start", "源", "起点", "起始"]
        target_fields = ["to", "target", "dst", "end", "dest", "目标", "终点", "结束"]
        dynamics_fields = ["dynamics", "description", "desc", "relation", "type", "relationship",
                          "动态", "描述", "关系", "类型"]

        for i, morphism in enumerate(morphisms):
            if not isinstance(morphism, dict):
                continue

            # 提取描述字段（多字段兼容）
            dynamics = ""
            for field in dynamics_fields:
                if field in morphism and morphism[field]:
                    dynamics = str(morphism[field])
                    break

            # 如果没有找到描述字段，尝试从源/目标字段组合
            if not dynamics:
                source_val = ""
                target_val = ""

                for field in source_fields:
                    if field in morphism and morphism[field]:
                        source_val = str(morphism[field])
                        break

                for field in target_fields:
                    if field in morphism and morphism[field]:
                        target_val = str(morphism[field])
                        break

                if source_val and target_val:
                    dynamics = f"{source_val} → {target_val}"

            # 如果仍然没有dynamics，记录警告（仅在verbose模式）
            if not dynamics:
                continue

            dynamics_lower = dynamics.lower()

            for tag_id, tag in self.tags.items():
                # 检查指标词匹配
                for indicator in tag.indicators:
                    if indicator.lower() in dynamics_lower:
                        user_tags.add(tag_id)
                        break

        return list(user_tags)

    def calculate_domain_score(
        self,
        domain: str,
        user_tags: List[str],
        user_profile: Optional[Union[str, Dict]] = None
    ) -> Tuple[float, List[Dict], str]:
        """
        计算领域匹配分数

        Args:
            domain: 领域名称
            user_tags: 用户标签列表
            user_profile: 用户画像类型

        Returns:
            (分数, 最佳匹配列表, 推理说明)
        """
        domain_tags = self.domain_tag_mapping.get(domain, [])
        if not domain_tags:
            return 0.0, [], f"领域 {domain} 无标签定义"

        total_score = 0
        best_matches = []

        # 计算标签匹配分数
        for domain_tag in domain_tags:
            if domain_tag in user_tags:
                # 完全匹配
                score = self.scoring_rules.get("exact_match", 100)
                total_score += score
                best_matches.append({
                    "tag": domain_tag,
                    "score": score,
                    "type": "exact"
                })
            else:
                # 检查相关标签
                tag_obj = self.tags.get(domain_tag)
                if tag_obj:
                    for related in tag_obj.related_tags:
                        if related in user_tags:
                            score = self.scoring_rules.get("related_match", 50)
                            total_score += score
                            best_matches.append({
                                "tag": domain_tag,
                                "related_to": related,
                                "score": score,
                                "type": "related"
                            })
                            break

                    # 检查对立标签（惩罚）
                    for opposite in tag_obj.opposite_tags:
                        if opposite in user_tags:
                            score = self.scoring_rules.get("opposite_match", -20)
                            total_score += score
                            break

        # 归一化分数
        max_possible = len(domain_tags) * self.scoring_rules.get("exact_match", 100)
        normalized_score = total_score / max_possible if max_possible > 0 else 0

        # 用户画像加权
        if user_profile:
            profile_bonus = self._apply_user_profile_bonus(domain, user_profile)
            normalized_score *= (1 + profile_bonus)

        # 生成推理说明
        reasoning = self._generate_reasoning(domain, best_matches, user_tags)

        return normalized_score, best_matches, reasoning

    def _apply_user_profile_bonus(self, domain: str, user_profile: Union[str, Dict]) -> float:
        """应用用户画像加权

        支持两种格式:
        1. 字符串格式: 预定义的 profile key (如 "investor", "tech_executive")
        2. 字典格式: 详细的用户画像，如 {"concern_type": "...", "risk_tolerance": "..."}

        Args:
            domain: 领域名称
            user_profile: 用户画像，字符串或字典

        Returns:
            加权分数，范围通常在 -0.2 到 0.2 之间
        """
        profile_rules = self.scoring_rules.get("user_profile_bonus", {})

        # 处理字符串格式（预定义 profile）
        if isinstance(user_profile, str):
            profile = profile_rules.get(user_profile, {})
            if domain in profile.get("preferred", []):
                return profile.get("bonus", 0.2)
            elif domain in profile.get("avoid", []):
                return -profile.get("bonus", 0.2)
            return 0.0

        # 处理字典格式（详细画像）
        if isinstance(user_profile, dict):
            bonus = 0.0

            # 基于 concern_type 进行领域偏好匹配
            concern_type = user_profile.get("concern_type", "")
            concern_lower = concern_type.lower() if concern_type else ""

            # 经济/财务相关 → 博弈论、行为经济学、复杂科学
            if any(kw in concern_lower for kw in ["经济", "财务", "投资", "market", "finance"]):
                if domain in ["game_theory", "behavioral_economics", "complexity_science"]:
                    bonus += 0.15

            # 社会影响相关 → 社会资本、人类学、网络理论
            if any(kw in concern_lower for kw in ["社会", "影响", "social", "impact"]):
                if domain in ["social_capital", "anthropology", "network_theory"]:
                    bonus += 0.15

            # 战略/政策相关 → 博弈论、军事战略、激励设计
            if any(kw in concern_lower for kw in ["战略", "政策", "strategy", "policy"]):
                if domain in ["game_theory", "military_strategy", "incentive_design"]:
                    bonus += 0.15

            # 基于 risk_tolerance 调整
            risk_tolerance = user_profile.get("risk_tolerance", "")
            if risk_tolerance and domain in ["antifragility", "complexity_science", "evolutionary_biology"]:
                bonus += 0.1

            # 基于 constraint_emphasis 调整
            constraints = user_profile.get("constraint_emphasis", [])
            if isinstance(constraints, list):
                constraint_str = ",".join(constraints).lower()
                if "技术" in constraint_str or "technical" in constraint_str:
                    if domain in ["control_systems", "distributed_systems", "information_theory"]:
                        bonus += 0.1
                if "资源" in constraint_str or "resource" in constraint_str:
                    if domain in ["thermodynamics", "ecology", "operations_research"]:
                        bonus += 0.1
                if "伦理" in constraint_str or "ethical" in constraint_str:
                    if domain in ["anthropology", "religious_studies", "zhuangzi"]:
                        bonus += 0.1

            # 上限控制
            return min(bonus, 0.3)

        return 0.0

    def _generate_reasoning(
        self,
        domain: str,
        best_matches: List[Dict],
        user_tags: List[str]
    ) -> str:
        """生成推理说明"""
        if not best_matches:
            return f"领域 {domain} 与用户标签匹配度较低"

        exact_matches = [m for m in best_matches if m["type"] == "exact"]
        if exact_matches:
            tags_str = ", ".join([m["tag"] for m in exact_matches[:3]])
            return f"用户问题的{tags_str}等动态特征与{domain}高度匹配"
        else:
            return f"用户问题与{domain}存在相关特征匹配"

    def get_domain_complexity_tier(self, domain: str) -> Tuple[str, float]:
        """
        获取领域的复杂度层级

        Args:
            domain: 领域名称

        Returns:
            (complexity_tier, tier_strength)
        """
        domain_data = self.domain_info.get(domain, {})
        return (
            domain_data.get("complexity_tier", "tier_2_application"),
            domain_data.get("tier_strength", 0.5)
        )

    def select_domains(
        self,
        objects: Optional[List[str]],
        morphisms: Optional[List[Dict[str, str]]],
        user_profile: Optional[Union[str, Dict]] = None,
        exclude_domains: Optional[List[str]] = None,
        history_domains: Optional[List[str]] = None,
        top_n: int = 5
    ) -> Dict[str, Any]:
        """
        选择最适合的领域 (Fast Mode)

        Args:
            objects: 用户问题的Objects列表
            morphisms: 用户问题的Morphisms列表
            user_profile: 用户画像类型
            exclude_domains: 要排除的领域列表
            history_domains: 历史使用领域列表（用于熵值衰减）
            top_n: 返回Top N领域，默认5

        Returns:
            选择结果字典，包含 complexity_tier 信息
        """
        # 处理None值
        objects = objects or []
        morphisms = morphisms or []

        # 提取用户标签
        user_tags = self.extract_user_tags(morphisms)

        # 计算复杂度
        complexity_level = self._determine_complexity(objects, morphisms)

        # 计算所有领域分数
        domain_scores = []
        for domain in self.domain_tag_mapping.keys():
            # 排除指定领域
            if exclude_domains and domain in exclude_domains:
                continue

            score, matches, reasoning = self.calculate_domain_score(
                domain, user_tags, user_profile
            )

            # 应用熵值衰减
            if history_domains:
                score = self._apply_entropy_decay(domain, score, history_domains)

            # 获取 complexity_tier
            complexity_tier, tier_strength = self.get_domain_complexity_tier(domain)

            domain_scores.append({
                "domain": domain,
                "score": score,
                "complexity_tier": complexity_tier,
                "tier_strength": tier_strength,
                "best_matches": matches,
                "reasoning": reasoning
            })

        # 排序并选择Top N
        domain_scores.sort(key=lambda x: x["score"], reverse=True)
        top_n_domains = domain_scores[:top_n]

        # 计算整体置信度
        confidence = self._calculate_confidence(top_n_domains, user_tags)

        return {
            "all_domains": domain_scores,     # 所有领域评分
            "top_domains": top_n_domains,     # Top N领域
            "user_tags": user_tags,
            "complexity_level": complexity_level,
            "confidence": confidence,
            "mode": "fast"
        }

    def tier_balance_selection(
        self,
        fast_candidates: List[Dict[str, Any]],
        selected_count: int = 5
    ) -> TierBalanceResult:
        """
        Tier Balance 种子选择 (Swarm Mode)

        Args:
            fast_candidates: Fast Mode候选领域列表
            selected_count: 目标选择数量，默认5

        Returns:
            TierBalanceResult 包含选定领域和wildcard
        """
        # v4.4.1: 如果候选为空或不足，使用最小可用集作为回退
        if not fast_candidates or len(fast_candidates) < 2:
            minimal_set = self._get_minimal_viable_set("default")
            # 转换为 fast_candidates 格式
            fast_candidates = []
            for domain_name in minimal_set:
                complexity_tier, tier_strength = self.get_domain_complexity_tier(domain_name)
                fast_candidates.append({
                    "domain": domain_name,
                    "score": 0.5,  # 默认分数
                    "complexity_tier": complexity_tier,
                    "tier_strength": tier_strength,
                    "best_matches": [],
                    "reasoning": "来自最小可用集"
                })

        # 按tier分组
        tier_groups: Dict[str, List[Dict]] = {
            "tier_1_axiomatic": [],
            "tier_2_application": [],
            "tier_3_practical": [],
            "tier_4_interpretive": []
        }

        for domain_info in fast_candidates:
            tier = domain_info.get("complexity_tier", "tier_2_application")
            tier_groups[tier].append(domain_info)

        # 平衡选择算法
        selected = []

        # Tier 1: 1-2个（确保有底层理论支撑）
        tier_1_count = 1 if selected_count <= 4 else 2
        if tier_groups["tier_1_axiomatic"]:
            selected.extend(tier_groups["tier_1_axiomatic"][:tier_1_count])

        # Tier 2: 2-3个（确保有应用方法论）
        tier_2_count = 2 if selected_count <= 4 else 3
        if tier_groups["tier_2_application"]:
            remaining_slots = selected_count - len(selected)
            tier_2_actual = min(tier_2_count, remaining_slots, len(tier_groups["tier_2_application"]))
            selected.extend(tier_groups["tier_2_application"][:tier_2_actual])

        # Tier 3/4: 0-1个（可选实践或阐释视角）
        if len(selected) < selected_count:
            remaining = selected_count - len(selected)
            if tier_groups["tier_3_practical"] and remaining > 0:
                selected.extend(tier_groups["tier_3_practical"][:1])
                remaining -= 1
            if tier_groups["tier_4_interpretive"] and remaining > 0:
                selected.extend(tier_groups["tier_4_interpretive"][:1])

        # 如果仍未满，从其他tier补充
        if len(selected) < selected_count:
            all_remaining = [d for t_group in tier_groups.values() for d in t_group if d not in selected]
            selected.extend(all_remaining[:selected_count - len(selected)])

        # 🔴 强制 Wildcard Agent（v4.4.1: 支持轮换）
        wildcard = self._select_wildcard_with_rotation(selected)

        # 构建tier分布映射
        tier_distribution = {}
        for domain_info in selected:
            tier = domain_info["complexity_tier"]
            if tier not in tier_distribution:
                tier_distribution[tier] = []
            tier_distribution[tier].append(domain_info["domain"])

        result = TierBalanceResult(
            selected_domains=[d["domain"] for d in selected],
            wildcard_domain=wildcard,
            tier_distribution=tier_distribution,
            reasoning=f"从{len(fast_candidates)}个候选中按Tier Balance选择{len(selected)}个领域"
        )

        return result

    def _calculate_confidence(
        self,
        top_domains: List[Dict],
        user_tags: List[str]
    ) -> float:
        """计算Fast Mode置信度"""
        if not top_domains:
            return 0.0

        # 有明确标签匹配
        if user_tags and top_domains[0]["score"] > 0.5:
            return min(95, 50 + top_domains[0]["score"] * 40)

        # 无标签匹配但领域覆盖好
        if len(top_domains) >= 3:
            return 60

        return 45

    def _determine_complexity(
        self,
        objects: List[str],
        morphisms: List[Dict]
    ) -> str:
        """判定问题复杂度"""
        simple_threshold = self.complexity_thresholds.get("simple", {})
        max_objects = simple_threshold.get("max_objects", 5)
        max_morphisms = simple_threshold.get("max_morphisms", 7)

        if len(objects) <= max_objects and len(morphisms) <= max_morphisms:
            return "simple"
        return "complex"

    def _apply_entropy_decay(
        self,
        domain: str,
        score: float,
        history: List[str]
    ) -> float:
        """应用熵值衰减"""
        entropy_rules = self.scoring_rules.get("entropy_decay", {})
        window_size = entropy_rules.get("window_size", 10)
        threshold = entropy_rules.get("threshold", 3)
        penalty = entropy_rules.get("penalty", 0.5)

        # 统计最近window_size次中该领域使用次数
        recent_history = history[-window_size:] if len(history) > window_size else history
        usage_count = recent_history.count(domain)

        if usage_count > threshold:
            return score * penalty

        return score

    def _get_minimal_viable_set(self, set_type: str = "default") -> List[str]:
        """
        获取最小可用集（v4.4.1 新增）

        Args:
            set_type: 集合类型（social/physical/abstract/practical/default）

        Returns:
            领域名称列表
        """
        if not self.minimal_viable_sets:
            # 回退到更小的缺省集
            return ["complexity_science", "network_theory", "game_theory"]

        return self.minimal_viable_sets.get(set_type, self.minimal_viable_sets.get("default", []))

    def _select_wildcard_with_rotation(self, selected: List[Dict[str, Any]]) -> Optional[str]:
        """
        使用轮换机制选择 wildcard（v4.4.1 新增）

        Args:
            selected: 已选定的领域列表

        Returns:
            wildcard 领域名称
        """
        import time

        selected_domains = [d["domain"] for d in selected]

        # 检查是否启用轮换
        if self.wildcard_rotation_config.get("enabled", False):
            pool = self.wildcard_rotation_config.get("pool", [])
            if pool:
                # 基于时间戳轮换
                index = int(time.time()) % len(pool)
                wildcard = pool[index]
                # 确保 wildcard 不在已选列表中
                if wildcard not in selected_domains:
                    return wildcard
                # 否则尝试下一个
                for i in range(len(pool)):
                    index = (index + 1) % len(pool)
                    wildcard = pool[index]
                    if wildcard not in selected_domains:
                        return wildcard

        # 回退到原始逻辑
        if self.wildcard_candidates:
            available_wildcards = [w for w in self.wildcard_candidates if w not in selected_domains]
            if available_wildcards:
                return random.choice(available_wildcards)

        return None

    def interactive_mode(self):
        """
        交互模式（调试用途）
        ⚠️ 注意：Swarm 模式下自动调用 select_domains() + tier_balance_selection()，无需交互
        """
        print("=" * 60)
        print("Domain Selector v4.0 - 智能领域选择器（全自动模式）")
        print("=" * 60)
        print()

        # 输入Objects
        print("请输入Objects（用逗号分隔，如：公司,产品,用户）：")
        objects_input = input().strip()
        objects = [o.strip() for o in objects_input.split(",") if o.strip()]

        # 输入Morphisms
        print("\n请输入Morphisms（格式：from->to:描述，每行一个，输入空行结束）：")
        morphisms = []
        while True:
            line = input().strip()
            if not line:
                break
            if "->" in line and ":" in line:
                parts = line.split(":", 1)
                relation = parts[0].strip()
                dynamics = parts[1].strip()
                if "->" in relation:
                    from_obj, to_obj = relation.split("->", 1)
                    morphisms.append({
                        "from": from_obj.strip(),
                        "to": to_obj.strip(),
                        "dynamics": dynamics
                    })

        # 选择用户画像
        print("\n请选择用户画像（直接回车跳过）：")
        profiles = ["tech_executive", "entrepreneur", "indie_developer",
                   "product_manager", "investor", "student_researcher"]
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile}")
        profile_input = input().strip()
        user_profile = None
        if profile_input.isdigit() and 1 <= int(profile_input) <= len(profiles):
            user_profile = profiles[int(profile_input) - 1]

        # 执行选择
        print("\n" + "=" * 60)
        print("正在分析...")
        print("=" * 60)

        # Step 1: Fast Mode 预筛选
        result = self.select_domains(objects, morphisms, user_profile)

        # 输出分析结果
        print("\n【Fast Mode 分析结果】")
        print(f"\n提取的标签: {', '.join(result['user_tags']) if result['user_tags'] else '(无)'}")
        print(f"问题复杂度: {result['complexity_level']}")
        print(f"置信度: {result['confidence']:.0f}%")

        # 显示Top 5领域
        top_domains = result['top_domains']
        print(f"\n【Top 5 候选领域】")
        for i, domain_info in enumerate(top_domains, 1):
            print(f"\n{i}. {domain_info['domain']}")
            print(f"   匹配分数: {domain_info['score']:.2f}")
            print(f"   复杂度层级: {domain_info['complexity_tier']}")
            if domain_info['best_matches']:
                tags_str = ', '.join([m['tag'] for m in domain_info['best_matches'][:3]])
                print(f"   匹配标签: {tags_str}")

        # Step 2: 全自动 Tier Balance 选择（Swarm 模式标准流程）
        print("\n" + "=" * 60)
        print("【Swarm Mode】执行 Tier Balance 全自动选择...")
        print("=" * 60)

        tier_result = self.tier_balance_selection(result['top_domains'])

        print(f"\n✓ 选定领域: {tier_result.selected_domains}")
        print(f"✓ Wildcard: {tier_result.wildcard_domain}")
        print(f"✓ Tier 分布: {tier_result.tier_distribution}")

        final_list = tier_result.selected_domains.copy()
        if tier_result.wildcard_domain:
            final_list.append(tier_result.wildcard_domain)

        print(f"\n【最终种子列表 (Swarm Mode)】: {final_list}")
        print("\n⚠️ 提示: Swarm 模式下 Team Lead 自动调用，无需人工选择")
        print("=" * 60)


def main():
    """主函数"""
    import sys
    import json

    selector = DomainSelector()

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # 交互模式
        selector.interactive_mode()
    elif len(sys.argv) > 1 and sys.argv[1] == "--tier-balance":
        # Tier Balance 演示模式
        print("=" * 60)
        print("Tier Balance Selection Demo (v4.0)")
        print("=" * 60)

        # 模拟 Fast Mode 结果
        demo_result = selector.select_domains(
            objects=["产品", "用户", "增长"],
            morphisms=[
                {"from": "产品", "to": "用户", "dynamics": "价值传递"},
                {"from": "用户", "to": "产品", "dynamics": "反馈驱动"}
            ]
        )

        print("\n【Fast Mode 候选】")
        for i, d in enumerate(demo_result['top_domains'][:6], 1):
            print(f"{i}. {d['domain']} (Tier: {d['complexity_tier']}, Score: {d['score']:.2f})")

        # 执行 Tier Balance
        tier_result = selector.tier_balance_selection(demo_result['top_domains'][:6])

        print("\n【Tier Balance 选择结果】")
        print(f"选定领域: {tier_result.selected_domains}")
        print(f"Wildcard: {tier_result.wildcard_domain}")
        print(f"Tier 分布: {tier_result.tier_distribution}")
        print(f"推理: {tier_result.reasoning}")

        final_list = tier_result.selected_domains.copy()
        if tier_result.wildcard_domain:
            final_list.append(tier_result.wildcard_domain)
        print(f"\n最终种子列表 (含Wildcard): {final_list}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--output-json":
        # JSON输出模式（便于脚本调用）
        demo_result = selector.select_domains(
            objects=["产品", "用户", "增长"],
            morphisms=[
                {"from": "产品", "to": "用户", "dynamics": "价值传递"},
                {"from": "用户", "to": "产品", "dynamics": "反馈驱动"}
            ]
        )

        tier_result = selector.tier_balance_selection(demo_result['top_domains'][:6])

        output = {
            'selected_domains': tier_result.selected_domains,
            'wildcard_domain': tier_result.wildcard_domain,
            'tier_distribution': tier_result.tier_distribution,
            'reasoning': tier_result.reasoning,
            'user_tags': demo_result.get('user_tags', []),
            'confidence': demo_result.get('confidence', 0.0)
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    else:
        # 显示帮助
        print("Domain Selector v4.0")
        print()
        print("用法:")
        print("  python domain_selector.py --interactive    启动交互模式")
        print("  python domain_selector.py --tier-balance   Tier Balance 演示")
        print("  python domain_selector.py --output-json    JSON输出（脚本调用）")
        print()
        print("或在Python代码中使用:")
        print("  from domain_selector import DomainSelector")
        print("  selector = DomainSelector()")
        print("  result = selector.select_domains(objects, morphisms)")
        print("  tier_result = selector.tier_balance_selection(result['top_domains'])")
        print()
        print("返回值说明:")
        print("  tier_result.selected_domains  - List[str] 选中的领域列表")
        print("  tier_result.wildcard_domain   - Optional[str] 随机领域")
        print("  tier_result.tier_distribution - Dict[str, List[str]] 各层级分布")
        print("  tier_result.reasoning         - str 选择理由")
        print()
        print("或使用 to_dict() 方法转换为字典:")
        print("  tier_result.to_dict()  - Dict[str, Any]")


if __name__ == "__main__":
    main()
