#!/usr/bin/env python3
"""自动更新 morphism_tags.json 的 domain_tag_mapping。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "assets" / "morphism_tags.json"
REFERENCES_DIR = ROOT / "references"


def resolve_domain_file(domain_name: str) -> Path:
    builtin = REFERENCES_DIR / f"{domain_name}_v2.md"
    if builtin.exists():
        return builtin
    custom = REFERENCES_DIR / "custom" / f"{domain_name}_v2.md"
    if custom.exists():
        return custom
    raise FileNotFoundError(f"领域文件不存在: {builtin} 或 {custom}")


def extract_morphisms_from_domain(domain_path: Path) -> List[Dict[str, str]]:
    """从领域文件中提取 Core Morphisms（name + dynamics）。"""
    content = domain_path.read_text(encoding="utf-8")

    sec_match = re.search(r"^## Core Morphisms.*$([\s\S]*?)(?=^##\s+|\Z)", content, re.MULTILINE)
    if not sec_match:
        return []

    section = sec_match.group(1)
    items: List[Dict[str, str]] = []

    for block in re.split(r"\n(?=-\s+\*\*)", section):
        line_match = re.search(r"-\s+\*\*(.+?)\*\*:\s*(.+)", block)
        if not line_match:
            continue

        name = line_match.group(1).strip()
        first_desc = line_match.group(2).strip()

        dyn_match = re.search(r"\*动态\*:\s*(.+)", block)
        dynamics = dyn_match.group(1).strip() if dyn_match else first_desc

        items.append({"name": name, "dynamics": dynamics})

    return items


def infer_domain_tags(
    morphisms: List[Dict[str, str]],
    tags_config: Dict[str, Dict],
    top_k: int = 3,
) -> List[str]:
    """基于标签 indicators 从 Core Morphisms 推断领域标签。"""
    scores: Dict[str, float] = {}

    for morphism in morphisms:
        text = f"{morphism.get('name', '')} {morphism.get('dynamics', '')}".lower()
        for tag_id, cfg in tags_config.items():
            indicators = cfg.get("indicators", [])
            hit = sum(1 for kw in indicators if isinstance(kw, str) and kw and kw.lower() in text)
            if hit:
                scores[tag_id] = scores.get(tag_id, 0.0) + hit

    if not scores:
        return []

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return [tag for tag, _ in ranked[:top_k]]


def update_domain_mapping(domain_name: str, top_k: int) -> bool:
    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    tags_config = db.get("tags", {})
    domain_map = db.setdefault("tag_relationships", {}).setdefault("domain_tag_mapping", {})

    domain_file = resolve_domain_file(domain_name)
    morphisms = extract_morphisms_from_domain(domain_file)

    if not morphisms:
        raise ValueError(f"未从 {domain_file} 提取到 Core Morphisms")

    inferred_tags = infer_domain_tags(morphisms, tags_config, top_k=top_k)
    if not inferred_tags:
        raise ValueError(f"未能为领域 {domain_name} 推断标签，请检查领域文件描述")

    old_tags = domain_map.get(domain_name, [])
    changed = old_tags != inferred_tags
    domain_map[domain_name] = inferred_tags

    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"✅ 已更新领域映射: {domain_name}")
    print(f"   - 领域文件: {domain_file}")
    print(f"   - 提取 Core Morphisms: {len(morphisms)}")
    print(f"   - 推断标签: {inferred_tags}")
    if old_tags:
        print(f"   - 旧标签: {old_tags}")
    print(f"   - 数据库: {DB_PATH}")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="更新 morphism_tags.json 的 domain_tag_mapping")
    parser.add_argument("domain_name", help="领域名（不含 _v2.md）")
    parser.add_argument("--top-k", type=int, default=3, help="最多写入标签数量，默认3")
    args = parser.parse_args()

    try:
        changed = update_domain_mapping(args.domain_name, top_k=args.top_k)
    except Exception as exc:
        print(f"错误: {exc}")
        return 1

    print("\n下一步:")
    print("1. 打开 assets/morphism_tags.json")
    print(f"2. 检查 tag_relationships.domain_tag_mapping.{args.domain_name}")
    print("3. 如需人工微调，可直接修改标签列表")
    return 0 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
