#!/usr/bin/env python3
"""领域知识库健康检查。"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"

sys.path.insert(0, str((ROOT / "scripts").resolve()))
from dynamic_agent_generator import DynamicAgentGenerator  # noqa: E402

REQUIRED_HEADINGS = [
    r"^## Fundamentals",
    r"^## Core Objects",
    r"^## Core Morphisms",
    r"^## Theorems",
]


def section_item_count(section: str) -> int:
    return len(re.findall(r"^\s*-\s+\*\*", section, re.MULTILINE))


def theorem_count(theorems_section: str) -> int:
    return len(re.findall(r"^###\s+\d+\.\s+", theorems_section, re.MULTILINE))


def validate_file(generator: DynamicAgentGenerator, file_path: Path) -> List[str]:
    errors: List[str] = []
    content = file_path.read_text(encoding="utf-8")

    for heading in REQUIRED_HEADINGS:
        if not re.search(heading, content, re.MULTILINE):
            errors.append(f"missing heading: {heading}")

    if "### 导语" not in content:
        errors.append("missing intro heading: ### 导语")

    domain = file_path.stem.replace("_v2", "")
    try:
        knowledge = generator.extract_knowledge(content, domain)
    except Exception as exc:  # pragma: no cover - direct CLI signal
        errors.append(f"extract_knowledge failed: {exc}")
        return errors

    object_items = section_item_count(knowledge.core_objects)
    morphism_items = section_item_count(knowledge.core_morphisms)
    theorem_items = theorem_count(knowledge.theorems)
    mapping_hint_items = len(re.findall(r"Mapping_Hint", knowledge.theorems))

    if object_items < 10:
        errors.append(f"core_objects entries too few: {object_items} < 10")
    if morphism_items < 10:
        errors.append(f"core_morphisms entries too few: {morphism_items} < 10")
    if theorem_items < 10:
        errors.append(f"theorem entries too few: {theorem_items} < 10")
    if mapping_hint_items < 8:
        errors.append(f"Mapping_Hint entries too few: {mapping_hint_items} < 8")

    return errors


def list_domain_files() -> Tuple[List[Path], List[Path]]:
    builtin = sorted(REFERENCES.glob("*_v2.md"))
    custom = sorted((REFERENCES / "custom").glob("*_v2.md"))
    return builtin, custom


def main() -> int:
    generator = DynamicAgentGenerator(str(REFERENCES))
    builtin, custom = list_domain_files()
    files = builtin + custom

    print(f"Built-in domains: {len(builtin)}")
    print(f"Custom domains: {len(custom)}")

    failures = []
    for file_path in files:
        errors = validate_file(generator, file_path)
        if errors:
            failures.append((file_path, errors))

    if failures:
        print("\n[FAILED] domain validation errors detected:")
        for file_path, errors in failures:
            print(f"- {file_path}")
            for err in errors:
                print(f"  - {err}")
        return 1

    print("\n[OK] all domain files passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
