#!/usr/bin/env python3
"""校验 Domain Agent 输出是否符合 domain_mapping_result.v1 schema。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "assets" / "agents" / "schemas" / "domain_mapping_result.v1.json"
REQUIRED_EVIDENCE_SECTIONS = {"Fundamentals", "Core Morphisms", "Theorems"}
REQUIRED_TOPOLOGY_FIELDS = {
    "topology_type",
    "core_action",
    "resource_flow",
    "feedback_loop",
    "time_dynamics",
    "agent_type",
}


def _validate_mapping_items(data: Dict[str, Any], key: str, required_keys: List[str], errors: List[str]) -> None:
    items = data.get(key)
    if not isinstance(items, list) or len(items) < 1:
        errors.append(f"{key} must be non-empty array")
        return
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{key}[{idx}] must be object")
            continue
        for req in required_keys:
            value = item.get(req)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{key}[{idx}].{req} must be non-empty string")


def fallback_validate(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = [
        "schema_version",
        "domain",
        "domain_file_path",
        "domain_file_hash",
        "evidence_refs",
        "objects_map",
        "morphisms_map",
        "theorems_used",
        "kernel_loss",
        "strategy_topology",
        "topology_reasoning",
        "confidence",
    ]
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")

    if data.get("schema_version") != "domain_mapping_result.v1":
        errors.append("schema_version must be domain_mapping_result.v1")

    path = str(data.get("domain_file_path", ""))
    if not re.match(r"^references/(custom/)?[a-z0-9_]+_v2\.md$", path):
        errors.append("domain_file_path format invalid")
    else:
        resolved = (ROOT / path).resolve()
        references_root = (ROOT / "references").resolve()
        if not str(resolved).startswith(str(references_root)):
            errors.append("domain_file_path must resolve under skill references/")
        elif not resolved.exists():
            errors.append("domain_file_path not found under skill references/")

    file_hash = str(data.get("domain_file_hash", ""))
    if not re.match(r"^[a-f0-9]{64}$", file_hash):
        errors.append("domain_file_hash must be sha256 hex")

    evidence_refs = data.get("evidence_refs")
    if not isinstance(evidence_refs, list) or len(evidence_refs) < 3:
        errors.append("evidence_refs must be array with at least 3 items")
    else:
        seen_sections = set()
        for idx, ref in enumerate(evidence_refs):
            if not isinstance(ref, dict):
                errors.append(f"evidence_refs[{idx}] must be object")
                continue
            section = ref.get("section")
            quote = ref.get("quote_or_summary")
            if not isinstance(section, str):
                errors.append(f"evidence_refs[{idx}].section must be string")
            else:
                seen_sections.add(section)
            if not isinstance(quote, str) or len(quote.strip()) < 8:
                errors.append(f"evidence_refs[{idx}].quote_or_summary must be at least 8 chars")

        missing_sections = REQUIRED_EVIDENCE_SECTIONS - seen_sections
        if missing_sections:
            missing = ", ".join(sorted(missing_sections))
            errors.append(f"evidence_refs missing required sections: {missing}")

    _validate_mapping_items(data, "objects_map", ["a_obj", "b_obj", "rationale"], errors)
    _validate_mapping_items(data, "morphisms_map", ["a_mor", "b_mor", "dynamics"], errors)

    theorems = data.get("theorems_used")
    if not isinstance(theorems, list) or len(theorems) < 2:
        errors.append("theorems_used must contain at least 2 items")
    else:
        for idx, theorem in enumerate(theorems):
            if not isinstance(theorem, dict):
                errors.append(f"theorems_used[{idx}] must be object")
                continue
            for req in ["id", "name", "mapping_hint_application"]:
                value = theorem.get(req)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"theorems_used[{idx}].{req} must be non-empty string")

    kernel_loss = data.get("kernel_loss", {})
    if not isinstance(kernel_loss, dict):
        errors.append("kernel_loss must be object")
    else:
        if not isinstance(kernel_loss.get("lost_nuances"), list) or len(kernel_loss.get("lost_nuances", [])) < 1:
            errors.append("kernel_loss.lost_nuances must be non-empty array")
        score = kernel_loss.get("preservation_score")
        if not isinstance(score, (int, float)) or score < 0 or score > 1:
            errors.append("kernel_loss.preservation_score must be number in [0,1]")

    strategy_topology = data.get("strategy_topology")
    if not isinstance(strategy_topology, dict):
        errors.append("strategy_topology must be object")
    else:
        missing_topology = REQUIRED_TOPOLOGY_FIELDS - set(strategy_topology.keys())
        if missing_topology:
            missing = ", ".join(sorted(missing_topology))
            errors.append(f"strategy_topology missing required fields: {missing}")

    topology_reasoning = data.get("topology_reasoning")
    if not isinstance(topology_reasoning, str) or len(topology_reasoning.strip()) < 8:
        errors.append("topology_reasoning must be non-empty string (>=8 chars)")

    confidence = data.get("confidence")
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        errors.append("confidence must be number in [0,1]")

    return errors


def validate_with_jsonschema(data: Dict[str, Any]) -> List[str]:
    try:
        import jsonschema  # type: ignore
    except Exception:
        return fallback_validate(data)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = [err.message for err in validator.iter_errors(data)]
    # 保留 jsonschema 的严格约束，同时补充可读性更强的语义错误信息。
    merged = schema_errors + fallback_validate(data)
    deduped: List[str] = []
    seen = set()
    for msg in merged:
        if msg not in seen:
            seen.add(msg)
            deduped.append(msg)
    return deduped


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: scripts/validate_mapping_json.py <json-file> [json-file ...]")
        return 2

    rc = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[ERROR] {p}: cannot read JSON - {exc}")
            rc = 1
            continue

        errors = validate_with_jsonschema(data)
        if errors:
            print(f"[FAILED] {p}")
            for e in errors:
                print(f"  - {e}")
            rc = 1
        else:
            print(f"[OK] {p}")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
