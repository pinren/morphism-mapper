#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/pinren/projects/V/AgentTeam/.claude/skills/morphism-mapper/scripts')

from domain_selector import DomainSelector

# 用户问题：中美贸易战中场休息，但感觉这事没完，尤其是当特朗普过了2026中期选举后，接下来会如何演变

category_skeleton = {
    "objects": [
        "中国 (主体A)",
        "美国 (主体B)",
        "特朗普 (关键决策者)",
        "2026中期选举 (时间触发器)",
        "贸易战 (博弈场域)",
        "关税政策 (核心工具)",
        "全球产业链 (博弈标的)"
    ],
    "morphisms": [
        {"from": "选举结果", "to": "政策转向", "dynamics": "时间延迟效应"},
        {"from": "中期选举", "to": "权力结构变化", "dynamics": "国会控制权争夺"},
        {"from": "关税战", "to": "经济博弈", "dynamics": "成本转嫁与反馈调节"},
        {"from": "特朗普决策", "to": "全球供应链扰动", "dynamics": "不确定性与预测应对"},
        {"from": "政治周期", "to": "贸易策略调整", "dynamics": "时间窗口与演化发展"},
        {"from": "选民压力", "to": "政策承诺兑现", "dynamics": "政治约束与博弈竞争"}
    ],
    "核心问题": "特朗普通过2026中期选举后，中美贸易战将如何演变？"
}

# 运行领域选择
selector = DomainSelector()
result = selector.select_domains(
    objects=category_skeleton["objects"],
    morphisms=category_skeleton["morphisms"]
)

print("=== 领域选择结果 ===")
print(f"\n匹配到的 Morphism Tags: {result.get('user_tags', [])}")
print(f"\nTop 5 推荐领域:")
for i, domain in enumerate(result['top_domains'][:5], 1):
    rationale = domain.get('rationale', '无')
    print(f"  {i}. {domain['domain']} (分数: {domain['score']:.3f}) - {rationale}")

# 运行 Tier Balance 选择
tier_result = selector.tier_balance_selection(result['top_domains'])
print(f"\n=== Tier Balance 选择 ===")
print(f"选中领域: {tier_result.selected_domains}")
print(f"Wildcard领域: {tier_result.wildcard_domain}")
print(f"层级分布: {tier_result.tier_distribution}")

# 输出用于 Domain Agent 生成
print("\n=== 用于生成 Domain Agents ===")
all_domains = tier_result.selected_domains.copy()
if tier_result.wildcard_domain:
    all_domains.append(tier_result.wildcard_domain)
print(f"最终领域列表: {all_domains}")
