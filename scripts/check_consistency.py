#!/usr/bin/env python3
"""检查 Morphism Mapper 关键配置的一致性。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, List, Set

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_AGENTS_PATH = ROOT / "assets" / "agents" / "config" / "domain_agents.json"
MORPHISM_TAGS_PATH = ROOT / "assets" / "morphism_tags.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _missing_items(values: Iterable[str], universe: Set[str]) -> List[str]:
    return sorted({v for v in values if v not in universe})


def main() -> int:
    errors: List[str] = []

    agents = _read_json(DOMAIN_AGENTS_PATH)
    tags = _read_json(MORPHISM_TAGS_PATH)

    domains = set(agents.get("domains", {}).keys())
    mapped_domains = set(tags.get("tag_relationships", {}).get("domain_tag_mapping", {}).keys())

    missing_mapping = sorted(domains - mapped_domains)
    if missing_mapping:
        errors.append(f"domain_tag_mapping 缺失: {', '.join(missing_mapping)}")

    unknown_mapping = sorted(mapped_domains - domains)
    warnings: List[str] = []
    for domain in unknown_mapping:
        builtin = ROOT / "references" / f"{domain}_v2.md"
        custom = ROOT / "references" / "custom" / f"{domain}_v2.md"
        if builtin.exists() or custom.exists():
            warnings.append(f"domain_tag_mapping 发现仅映射领域（未注册 domain_agents）: {domain}")
        else:
            errors.append(f"domain_tag_mapping 存在未知领域且无领域文件: {domain}")

    checks = {
        "default_seed_domains": agents.get("default_seed_domains", []),
        "wildcard_candidates": agents.get("wildcard_candidates", []),
        "wildcard_rotation.pool": agents.get("wildcard_rotation", {}).get("pool", []),
    }
    for set_name, values in checks.items():
        missing = _missing_items(values, domains)
        if missing:
            errors.append(f"{set_name} 包含不存在领域: {', '.join(missing)}")

    for set_name, values in agents.get("minimal_viable_sets", {}).items():
        missing = _missing_items(values, domains)
        if missing:
            errors.append(f"minimal_viable_sets.{set_name} 包含不存在领域: {', '.join(missing)}")

    for domain, cfg in agents.get("domains", {}).items():
        file_ref = cfg.get("domain_file", "")
        if not isinstance(file_ref, str) or not file_ref.startswith("references/"):
            errors.append(f"{domain}.domain_file 格式非法: {file_ref}")
            continue
        abs_path = ROOT / file_ref
        if not abs_path.exists():
            errors.append(f"{domain}.domain_file 不存在: {file_ref}")

    if errors:
        print("[FAILED] 配置一致性检查失败:")
        for msg in errors:
            print(f"  - {msg}")
        return 1

    print("[OK] 配置一致性检查通过")
    print(f"  - domains: {len(domains)}")
    print(f"  - mapped domains: {len(mapped_domains)}")
    if warnings:
        print("  - warnings:")
        for msg in warnings:
            print(f"    * {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
