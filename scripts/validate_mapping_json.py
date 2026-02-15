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
    if not re.match(r"^references/(custom/)?[a-z0-9_]+_v2\\.md$", path):
        errors.append("domain_file_path format invalid")

    file_hash = str(data.get("domain_file_hash", ""))
    if not re.match(r"^[a-f0-9]{64}$", file_hash):
        errors.append("domain_file_hash must be sha256 hex")

    if not isinstance(data.get("objects_map"), list) or len(data.get("objects_map", [])) < 1:
        errors.append("objects_map must be non-empty array")
    if not isinstance(data.get("morphisms_map"), list) or len(data.get("morphisms_map", [])) < 1:
        errors.append("morphisms_map must be non-empty array")
    if not isinstance(data.get("theorems_used"), list) or len(data.get("theorems_used", [])) < 2:
        errors.append("theorems_used must contain at least 2 items")

    kernel_loss = data.get("kernel_loss", {})
    if not isinstance(kernel_loss, dict):
        errors.append("kernel_loss must be object")
    else:
        if not isinstance(kernel_loss.get("lost_nuances"), list) or len(kernel_loss.get("lost_nuances", [])) < 1:
            errors.append("kernel_loss.lost_nuances must be non-empty array")
        score = kernel_loss.get("preservation_score")
        if not isinstance(score, (int, float)) or score < 0 or score > 1:
            errors.append("kernel_loss.preservation_score must be number in [0,1]")

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
    return [err.message for err in validator.iter_errors(data)]


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
