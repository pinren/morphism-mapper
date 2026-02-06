#!/usr/bin/env python3
"""
Domain Selector - 智能领域选择器 (v3.0)
基于Morphism结构匹配的智能领域选择算法
"""

import json
import os
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
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
    best_matches: List[Dict[str, Any]]
    reasoning: str

class DomainSelector:
    """智能领域选择器"""
    
    def __init__(self, tags_file: Optional[str] = None):
        """
        初始化领域选择器
        
        Args:
            tags_file: morphism_tags.json文件路径，默认为脚本所在目录
        """
        if tags_file is None:
            # 默认从data目录加载
            script_dir = Path(__file__).parent.parent
            tags_file = str(script_dir / "data" / "morphism_tags.json")
        
        self.tags_data = self._load_tags(tags_file)
        self.tags = self._parse_tags()
        self.domain_tag_mapping = self.tags_data.get("tag_relationships", {}).get("domain_tag_mapping", {})
        self.scoring_rules = self.tags_data.get("scoring_rules", {})
        self.complexity_thresholds = self.tags_data.get("complexity_thresholds", {})
    
    def _load_tags(self, tags_file: str) -> Dict:
        """加载标签定义文件"""
        with open(tags_file, 'r', encoding='utf-8') as f:
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
            morphisms: 用户问题的Morphism列表
                [{"from": "A", "to": "B", "dynamics": "描述"}, ...]
        
        Returns:
            提取的标签列表
        """
        if morphisms is None:
            return []
            
        user_tags = set()
        
        for morphism in morphisms:
            dynamics = morphism.get("dynamics", "").lower()
            
            for tag_id, tag in self.tags.items():
                # 检查指标词匹配
                for indicator in tag.indicators:
                    if indicator.lower() in dynamics:
                        user_tags.add(tag_id)
                        break
        
        return list(user_tags)
    
    def calculate_domain_score(
        self, 
        domain: str, 
        user_tags: List[str],
        user_profile: Optional[str] = None
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
    
    def _apply_user_profile_bonus(self, domain: str, user_profile: str) -> float:
        """应用用户画像加权"""
        profile_rules = self.scoring_rules.get("user_profile_bonus", {})
        profile = profile_rules.get(user_profile, {})
        
        if domain in profile.get("preferred", []):
            return profile.get("bonus", 0.2)
        elif domain in profile.get("avoid", []):
            return -profile.get("bonus", 0.2)
        
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
    
    def select_domains(
        self,
        objects: Optional[List[str]],
        morphisms: Optional[List[Dict[str, str]]],
        user_profile: Optional[str] = None,
        exclude_domains: Optional[List[str]] = None,
        history_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        选择最适合的领域
        
        Args:
            objects: 用户问题的Objects列表
            morphisms: 用户问题的Morphisms列表
            user_profile: 用户画像类型
            exclude_domains: 要排除的领域列表
            history_domains: 历史使用领域列表（用于熵值衰减）
        
        Returns:
            选择结果字典
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
            
            domain_scores.append({
                "domain": domain,
                "score": score,
                "best_matches": matches,
                "reasoning": reasoning
            })
        
        # 排序并选择Top N
        domain_scores.sort(key=lambda x: x["score"], reverse=True)
        
        if complexity_level == "simple":
            selected = domain_scores[:1]
        else:
            selected = domain_scores[:5]
        
        return {
            "selected_domains": selected,
            "user_tags": user_tags,
            "complexity_level": complexity_level,
            "recommendation": f"建议使用 {selected[0]['domain']} 作为主映射域" if selected else "未找到匹配领域"
        }
    
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
    
    def interactive_mode(self):
        """交互模式"""
        print("=" * 60)
        print("Domain Selector v3.0 - 智能领域选择器")
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
        
        result = self.select_domains(objects, morphisms, user_profile)
        
        # 输出结果
        print("\n【分析结果】")
        print(f"\n提取的标签: {', '.join(result['user_tags'])}")
        print(f"问题复杂度: {result['complexity_level']}")
        print(f"\n{result['recommendation']}")
        
        print("\n【推荐领域】")
        for i, domain_info in enumerate(result['selected_domains'], 1):
            print(f"\n{i}. {domain_info['domain']}")
            print(f"   匹配分数: {domain_info['score']:.2f}")
            print(f"   推荐理由: {domain_info['reasoning']}")
            if domain_info['best_matches']:
                print(f"   匹配标签: {', '.join([m['tag'] for m in domain_info['best_matches'][:3]])}")


def main():
    """主函数"""
    import sys
    
    selector = DomainSelector()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # 交互模式
        selector.interactive_mode()
    else:
        # 显示帮助
        print("Domain Selector v3.0")
        print()
        print("用法:")
        print("  python domain_selector.py --interactive    启动交互模式")
        print()
        print("或在Python代码中使用:")
        print("  from domain_selector import DomainSelector")
        print("  selector = DomainSelector()")
        print("  result = selector.select_domains(objects, morphisms)")


if __name__ == "__main__":
    main()
