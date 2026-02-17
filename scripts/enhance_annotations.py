#!/usr/bin/env python3
"""批量增强 domain_tag_mapping（当前 schema 兼容版）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "assets" / "morphism_tags.json"
AGENTS_PATH = ROOT / "assets" / "agents" / "config" / "domain_agents.json"

# 扩展关键词映射（标签 -> 关键词）
TAG_KEYWORDS = {
    "feedback_regulation": ["反馈", "调节", "纠正", "控制", "修正", "调整", "稳态", "平衡"],
    "feedforward_anticipation": ["前馈", "预见", "预测", "提前", "前瞻", "预警"],
    "learning_adaptation": ["学习", "适应", "习得", "改进", "经验", "可塑性"],
    "evolution_development": ["演化", "发展", "演替", "进化", "变革", "转型"],
    "competition_selection": ["竞争", "选择", "淘汰", "斗争", "对抗", "博弈"],
    "cooperation_symbiosis": ["合作", "共生", "互惠", "协同", "互利", "联盟"],
    "information_processing": ["信息", "信号", "编码", "解码", "处理", "认知", "感知"],
    "stabilization_equilibrium": ["稳定", "均衡", "平衡", "收敛", "恢复", "守恒"],
    "flow_exchange": ["流动", "交换", "传递", "循环", "转移", "输送"],
    "structural_organization": ["组织", "结构", "构建", "形成", "整合", "秩序"],
    "optimization_search": ["优化", "搜索", "求解", "寻找", "最大化", "最优"],
    "diffusion_propagation": ["扩散", "传播", "传染", "级联", "蔓延", "推广"],
    "transformation_conversion": ["转化", "转变", "转换", "变化", "转型", "重构"],
    "emergence_generation": ["涌现", "生成", "产生", "创造", "形成", "创新"],
    "exploration_exploitation": ["探索", "利用", "尝试", "试验", "发现", "试错"],
    "oscillation_fluctuation": ["振荡", "波动", "周期", "涨落", "起伏", "震荡"],
}


def resolve_domain_file(domain: str) -> Path | None:
    builtin = ROOT / "references" / f"{domain}_v2.md"
    if builtin.exists():
        return builtin
    custom = ROOT / "references" / "custom" / f"{domain}_v2.md"
    if custom.exists():
        return custom
    return None


def extract_text_for_tagging(content: str) -> str:
    """提取 Core Morphisms 区块文本用于标签推断。"""
    marker = "## Core Morphisms"
    start = content.find(marker)
    if start < 0:
        return content

    rest = content[start:]
    next_idx = rest.find("\n## ", 1)
    section = rest if next_idx < 0 else rest[:next_idx]
    return section


def infer_tags(text: str, allowed_tags: set[str], top_k: int = 3) -> List[str]:
    text_lower = text.lower()
    scores: Dict[str, int] = {}

    for tag, keywords in TAG_KEYWORDS.items():
        if tag not in allowed_tags:
            continue
        score = 0
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1
        if score > 0:
            scores[tag] = score

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return [tag for tag, _ in ranked[:top_k]]


def enhance_database() -> int:
    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    agents = json.loads(AGENTS_PATH.read_text(encoding="utf-8"))

    allowed_tags = set(db.get("tags", {}).keys())
    domain_map = db.setdefault("tag_relationships", {}).setdefault("domain_tag_mapping", {})
    agent_domains = list(agents.get("domains", {}).keys())

    total = 0
    updated = 0
    skipped = 0

    for domain in agent_domains:
        total += 1
        domain_file = resolve_domain_file(domain)
        if not domain_file:
            skipped += 1
            continue

        content = domain_file.read_text(encoding="utf-8")
        text = extract_text_for_tagging(content)
        new_tags = infer_tags(text, allowed_tags, top_k=3)

        if not new_tags:
            # 无法推断时保留现有映射
            skipped += 1
            continue

        if domain_map.get(domain) != new_tags:
            domain_map[domain] = new_tags
            updated += 1

    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("✅ 增强完成")
    print(f"   总领域: {total}")
    print(f"   更新领域: {updated}")
    print(f"   跳过领域: {skipped}")
    print(f"   数据库: {DB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(enhance_database())
