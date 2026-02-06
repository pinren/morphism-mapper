#!/usr/bin/env python3
"""
Domain Selector for Morphism-Mapper v3.0
基于Morphism结构匹配的领域选择器

Usage:
    python domain_selector.py --problem user_problem.json
    python domain_selector.py --interactive
"""

import json
import argparse
from typing import List, Dict, Tuple, Set
from pathlib import Path


class DomainSelector:
    """基于Morphism结构匹配的领域选择器"""
    
    # 标签关联关系（相关但不完全相同）
    RELATED_TAGS = {
        "feedback_regulation": ["feedforward_anticipation", "stabilization_equilibrium", "learning_adaptation"],
        "feedforward_anticipation": ["feedback_regulation", "optimization_search", "information_processing"],
        "learning_adaptation": ["evolution_development", "exploration_exploitation", "feedback_regulation"],
        "evolution_development": ["learning_adaptation", "transformation_conversion", "emergence_generation"],
        "competition_selection": ["cooperation_symbiosis", "optimization_search", "exploration_exploitation"],
        "cooperation_symbiosis": ["competition_selection", "structural_organization", "flow_exchange"],
        "information_processing": ["flow_exchange", "feedback_regulation", "feedforward_anticipation"],
        "stabilization_equilibrium": ["feedback_regulation", "oscillation_fluctuation", "structural_organization"],
        "flow_exchange": ["information_processing", "diffusion_propagation", "cooperation_symbiosis"],
        "structural_organization": ["stabilization_equilibrium", "emergence_generation", "cooperation_symbiosis"],
        "optimization_search": ["competition_selection", "learning_adaptation", "feedforward_anticipation"],
        "diffusion_propagation": ["flow_exchange", "exploration_exploitation", "emergence_generation"],
        "transformation_conversion": ["evolution_development", "emergence_generation", "exploration_exploitation"],
        "emergence_generation": ["transformation_conversion", "structural_organization", "evolution_development"],
        "exploration_exploitation": ["learning_adaptation", "competition_selection", "diffusion_propagation"],
        "oscillation_fluctuation": ["stabilization_equilibrium", "feedback_regulation", "flow_exchange"]
    }
    
    def __init__(self, db_path: str = None):
        """初始化选择器"""
        if db_path is None:
            # 默认路径：脚本所在目录的上一级/data/
            script_dir = Path(__file__).parent
            db_path_final: str = str(script_dir.parent / "data" / "morphism_tags.json")
        else:
            db_path_final = db_path
        
        with open(db_path_final, 'r', encoding='utf-8') as f:
            self.db = json.load(f)
        
        self.tag_defs = self.db['tag_definitions']
        self.domains = self.db['domains']
    
    def extract_user_morphism_tags(self, M_a: List[Dict]) -> Set[str]:
        """
        从用户问题的M_a中提取标签
        
        Args:
            M_a: List of dict with keys: 'from', 'to', 'dynamics'
                 Example: [{"from": "A", "to": "B", "dynamics": "反馈调节"}]
        
        Returns:
            Set of tag keys
        """
        user_tags = set()
        
        for m in M_a:
            dynamics = m.get('dynamics', '')
            
            # 基于关键词匹配标签
            for tag_key, tag_def in self.tag_defs.items():
                keywords = tag_def.get('keywords', [])
                if any(kw in dynamics for kw in keywords):
                    user_tags.add(tag_key)
        
        return user_tags
    
    def are_related_tags(self, tag1: str, tag2: str) -> bool:
        """判断两个标签是否相关"""
        if tag1 == tag2:
            return True
        return tag2 in self.RELATED_TAGS.get(tag1, [])
    
    def calculate_morphism_match_score(self, user_tags: Set[str], morphism_tags: List[str], verbose: bool = False) -> int:
        """
        计算用户标签与单个Morphism的匹配分数
        
        Returns:
            匹配分数 (0-100 per match)
        """
        score = 0
        match_details = []
        
        for user_tag in user_tags:
            for morph_tag in morphism_tags:
                if user_tag == morph_tag:
                    # 完全匹配
                    score += 100
                    match_details.append(f"  {user_tag} == {morph_tag}: +100")
                elif self.are_related_tags(user_tag, morph_tag):
                    # 相关匹配
                    score += 50
                    match_details.append(f"  {user_tag} ~ {morph_tag}: +50 (相关)")
        
        if verbose and match_details:
            print(f"    匹配详情:")
            for detail in match_details:
                print(f"      {detail}")
            print(f"    小计: {score}")
        
        return score
    
    def calculate_domain_match(self, user_tags: Set[str], domain_name: str, verbose: bool = False) -> Tuple[float, List[Dict]]:
        """
        计算用户标签与整个领域的匹配度
        
        Returns:
            (匹配分数 0-1, 最佳匹配的Morphism列表)
        """
        if domain_name not in self.domains:
            return 0.0, []
        
        domain_data = self.domains[domain_name]
        morphisms = domain_data.get('morphisms', [])
        
        if not morphisms:
            return 0.0, []
        
        if verbose:
            print(f"\n  领域: {domain_name}")
            print(f"  用户标签: {user_tags}")
            print(f"  总Morphism数: {len(morphisms)}")
        
        total_score = 0
        matched_morphisms = []
        
        for morphism in morphisms:
            morph_tags = morphism.get('tags', [])
            if not morph_tags:
                continue
            
            if verbose:
                print(f"\n    Morphism: {morphism['name']}")
                print(f"    动态: {morphism['dynamics']}")
                print(f"    标签: {morph_tags}")
            
            score = self.calculate_morphism_match_score(user_tags, morph_tags, verbose=verbose)
            
            if score > 0:
                total_score += score
                matched_morphisms.append({
                    'id': morphism['id'],
                    'name': morphism['name'],
                    'dynamics': morphism['dynamics'],
                    'tags': morph_tags,
                    'score': score
                })
        
        # 归一化分数 (0-1)
        max_possible_score = len(user_tags) * 100 * len(morphisms)
        normalized_score = total_score / max_possible_score if max_possible_score > 0 else 0
        
        if verbose:
            print(f"\n  领域总分: {total_score}")
            print(f"  最大可能分: {max_possible_score}")
            print(f"  归一化分数: {normalized_score:.3f}")
        
        # 排序并取Top 3匹配的Morphism
        matched_morphisms.sort(key=lambda x: x['score'], reverse=True)
        
        return min(normalized_score, 1.0), matched_morphisms[:3]
    
    def select_domains(self, O_a: List[str], M_a: List[Dict], top_n: int = 3, verbose: bool = False) -> List[Dict]:
        """
        主选择函数
        
        Args:
            O_a: Objects列表
            M_a: Morphisms列表
            top_n: 返回前N个最佳匹配领域
            verbose: 是否打印详细匹配过程
        
        Returns:
            排序后的领域选择结果
        """
        # 提取用户Morphism标签
        user_tags = self.extract_user_morphism_tags(M_a)
        
        if verbose:
            print("=" * 70)
            print("详细匹配过程")
            print("=" * 70)
            print(f"\n用户Objects: {O_a}")
            print(f"用户Morphism标签: {user_tags}")
            print(f"\n开始匹配 {len(self.domains)} 个领域...")
        
        if not user_tags:
            return []
        
        # 计算所有领域匹配度
        results = []
        for domain_name in self.domains.keys():
            score, best_matches = self.calculate_domain_match(user_tags, domain_name, verbose=verbose)
            
            if score > 0:
                results.append({
                    'domain': domain_name,
                    'score': score,
                    'best_matches': best_matches,
                    'user_tags': list(user_tags),
                    'match_count': len(best_matches)
                })
        
        # 按分数降序排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        if verbose:
            print("\n" + "=" * 70)
            print("匹配结果排序 (全部31个领域)")
            print("=" * 70)
            for i, r in enumerate(results, 1):
                match_info = f"[{r['match_count']}个Morphism匹配]" if r['match_count'] > 0 else "[无匹配]"
                print(f"{i:2d}. {r['domain']:25s} : {r['score']:6.1%} {match_info}")
        
        return results[:top_n]
    
    def format_selection_result(self, results: List[Dict]) -> str:
        """格式化选择结果为可读文本"""
        if not results:
            return "未找到匹配的领域"
        
        output = []
        output.append("=" * 60)
        output.append("基于Morphism结构匹配的领域选择结果")
        output.append("=" * 60)
        output.append("")
        
        for i, result in enumerate(results, 1):
            output.append(f"【推荐 #{i}】{result['domain']}")
            output.append(f"  匹配分数: {result['score']:.1%}")
            output.append(f"  匹配Morphism数: {result['match_count']}")
            output.append(f"  用户标签: {', '.join(result['user_tags'])}")
            output.append("")
            output.append("  最佳匹配Morphism:")
            for match in result['best_matches']:
                output.append(f"    - {match['name']} (得分: {match['score']})")
                output.append(f"      动态: {match['dynamics']}")
                output.append(f"      标签: {', '.join(match['tags'])}")
            output.append("")
            output.append("-" * 60)
            output.append("")
        
        return "\n".join(output)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='基于Morphism结构匹配的领域选择器')
    parser.add_argument('--problem', type=str, help='用户问题JSON文件路径')
    parser.add_argument('--interactive', action='store_true', help='交互模式')
    parser.add_argument('--top-n', type=int, default=5, help='返回前N个领域')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细匹配过程')
    
    args = parser.parse_args()
    
    selector = DomainSelector()
    
    if args.interactive:
        # 交互模式
        print("=" * 60)
        print("Morphism-Mapper v3.0 - 交互式领域选择")
        print("=" * 60)
        print()
        
        # 输入Objects
        print("请输入Objects（用逗号分隔）:")
        oa_input = input("> ")
        O_a = [o.strip() for o in oa_input.split(",") if o.strip()]
        
        # 输入Morphism数量
        print("\n请输入Morphism数量:")
        try:
            m_count = int(input("> "))
        except ValueError:
            m_count = 3
        
        # 输入每个Morphism
        M_a = []
        for i in range(m_count):
            print(f"\nMorphism #{i+1}:")
            print("  动态描述（如：反馈调节、竞争选择等）:")
            dynamics = input("> ")
            if dynamics:
                M_a.append({
                    'from': f'obj_{i}',
                    'to': f'obj_{i+1}',
                    'dynamics': dynamics
                })
        
        # 执行选择
        results = selector.select_domains(O_a, M_a, top_n=args.top_n, verbose=args.verbose)
        if not args.verbose:
            print(selector.format_selection_result(results))
    
    elif args.problem:
        # 文件模式
        with open(args.problem, 'r', encoding='utf-8') as f:
            problem = json.load(f)
        
        O_a = problem.get('O_a', [])
        M_a = problem.get('M_a', [])
        
        results = selector.select_domains(O_a, M_a, top_n=args.top_n, verbose=args.verbose)
        if not args.verbose:
            print(selector.format_selection_result(results))
    
    else:
        # 示例模式
        print("使用示例数据演示...")
        print()
        
        O_a = ["公司", "产品", "用户", "市场"]
        M_a = [
            {"from": "产品", "to": "用户", "dynamics": "价值传递与反馈收集"},
            {"from": "用户", "to": "产品", "dynamics": "需求反馈驱动改进"},
            {"from": "公司", "to": "市场", "dynamics": "竞争与适应"}
        ]
        
        results = selector.select_domains(O_a, M_a, top_n=args.top_n, verbose=args.verbose)
        if not args.verbose:
            print(selector.format_selection_result(results))


if __name__ == "__main__":
    main()
