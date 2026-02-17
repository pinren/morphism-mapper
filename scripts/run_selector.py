#!/usr/bin/env python3
"""
Debug 模式领域选择 - 婆媳问题
"""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from domain_selector import DomainSelector

# 婆媳问题的范畴骨架
category_skeleton = {
    "objects": [
        {"name": "婆婆", "attributes": "母系权威持有者, 传统家庭价值观守护者"},
        {"name": "媳妇", "attributes": "新加入成员, 现代独立意识携带者"},
        {"name": "儿子/丈夫", "attributes": "双重角色, 中介与缓冲者"},
        {"name": "家庭权力结构", "attributes": "资源分配与决策权的隐性/显性规则"}
    ],
    "morphisms": [
        {
            "from": "婆婆",
            "to": "媳妇",
            "dynamics": "权威试探(边界测试、规则灌输、地位确认)"
        },
        {
            "from": "媳妇",
            "to": "婆婆",
            "dynamics": "独立宣言(自主空间争取、代际价值观冲突)"
        },
        {
            "from": "儿子/丈夫",
            "to": "婆婆",
            "dynamics": "角色撕裂(忠诚分裂、调解压力)"
        },
        {
            "from": "儿子/丈夫",
            "to": "媳妇",
            "dynamics": "角色撕裂(平衡压力、站队风险)"
        },
        {
            "from": "家庭权力结构",
            "to": "婆婆",
            "dynamics": "资源竞争(关注度、话语权分配)"
        },
        {
            "from": "家庭权力结构",
            "to": "媳妇",
            "dynamics": "资源竞争(经济权、决策权争夺)"
        }
    ],
    "核心问题": "婆媳矛盾怎么破？",
    "tags": ["competition_conflict", "constraint_limitation", "resource_allocation", "communication_signaling"]
}

# 用户画像
user_profile = {
    "identity": "面临婆媳关系的家庭成员",
    "resources": ["家庭关系", "情感资本", "时间精力"],
    "constraints": ["传统伦理约束", "代际价值观差异", "三角关系复杂性"]
}

# 初始化选择器
selector = DomainSelector()

# 执行选择
result = selector.select_domains(
    objects=[o["name"] for o in category_skeleton["objects"]],
    morphisms=category_skeleton["morphisms"],
    user_profile=user_profile
)

print("\n" + "="*60)
print("【Debug 模式】领域选择结果")
print("="*60)

# Debug 模式：取 Top 2
top_domains = result["top_domains"][:2]

for i, domain in enumerate(top_domains, 1):
    matched_tags = [m.get("tag", "") for m in domain.get("best_matches", []) if m.get("tag")]
    print(f"\n【领域 {i}】")
    print(f"选择的领域: {domain['domain']}")
    print(f"整体置信度: {result.get('confidence', 0):.2f}")
    print(f"匹配标签: {', '.join(matched_tags) if matched_tags else '无'}")
    print(f"推荐理由: {domain.get('reasoning', '无')}")

# 输出用于启动 Agent 的信息
print("\n" + "="*60)
print("【Agent 启动配置】")
print("="*60)
for domain in top_domains:
    print(f"\ndomain_name: {domain['domain']}")
    print(f"agent_name: {domain['domain'].lower().replace(' ', '_')}-agent")
