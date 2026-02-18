#!/usr/bin/env python3
"""Extract CATEGORY_SKELETON then run domain selection with persisted evidence.

This script guarantees the visible sequence:
1) CATEGORY_SKELETON_EXTRACTED
2) DOMAIN_SELECTION_EVIDENCE
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from domain_selector import DomainSelector
from helpers import ensure_exploration_path
from modules.category_extraction import CategoryExtractor


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_json(data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _resolve_domain_knowledge_file(domain: str) -> Optional[Path]:
    base = _skill_root() / "references"
    candidates = [
        base / f"{domain}_v2.md",
        base / "custom" / f"{domain}_v2.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def _normalize_skeleton(raw: Dict[str, Any], topic: str) -> Dict[str, Any]:
    objects_raw = raw.get("objects") or []
    morphisms_raw = raw.get("morphisms") or []

    objects: List[Dict[str, Any]] = []
    for item in objects_raw:
        if isinstance(item, str):
            name = item.strip()
            if name:
                objects.append({"name": name})
        elif isinstance(item, dict):
            name = str(item.get("name", "")).strip()
            if name:
                norm = dict(item)
                norm["name"] = name
                objects.append(norm)

    morphisms: List[Dict[str, Any]] = []
    for item in morphisms_raw:
        if not isinstance(item, dict):
            continue
        source = item.get("from") or item.get("source") or item.get("src")
        target = item.get("to") or item.get("target") or item.get("dst")
        dynamics = item.get("dynamics") or item.get("description") or item.get("relation") or ""
        source = str(source).strip() if source is not None else ""
        target = str(target).strip() if target is not None else ""
        dynamics = str(dynamics).strip()
        if source and target and dynamics:
            morphisms.append(
                {
                    "from": source,
                    "to": target,
                    "dynamics": dynamics,
                }
            )

    tags = raw.get("tags")
    if not isinstance(tags, list):
        tags = []

    normalized = {
        "objects": objects,
        "morphisms": morphisms,
        "tags": tags,
        "核心问题": raw.get("核心问题") or topic,
    }
    object_names = [obj.get("name") for obj in normalized["objects"] if isinstance(obj, dict)]
    is_generic_default = set(object_names) == {"老板", "员工", "企业", "客户"}

    topic_hint_objects = None
    if "中美日" in topic or "三角博弈" in topic:
        topic_hint_objects = ["中国", "美国", "日本", "东亚秩序"]
    elif "婆媳" in topic:
        topic_hint_objects = ["婆婆", "媳妇", "儿子/丈夫", "家庭权力结构"]

    if not normalized["objects"] or (is_generic_default and topic_hint_objects):
        if topic_hint_objects:
            normalized["objects"] = [{"name": n} for n in topic_hint_objects]
        else:
            normalized["objects"] = [
                {"name": "核心行为体"},
                {"name": "关系对象"},
                {"name": "约束环境"},
            ]

    if not normalized["morphisms"] or (is_generic_default and topic_hint_objects):
        names = [obj["name"] for obj in normalized["objects"] if isinstance(obj, dict) and obj.get("name")]
        if len(names) < 3:
            names = ["核心行为体", "关系对象", "约束环境"]
        normalized["morphisms"] = [
            {
                "from": names[0],
                "to": names[1],
                "dynamics": f"围绕{topic}形成持续互动与反馈",
            },
            {
                "from": names[2],
                "to": names[0],
                "dynamics": f"{topic}中约束条件影响行为体策略选择",
            },
        ]
    return normalized


def _append_event(path: Path, signal: str, payload_ref: str, summary: str) -> None:
    line = {
        "timestamp": _utc_now(),
        "signal": signal,
        "actor": "lead",
        "target": None,
        "domain": None,
        "payload_ref": payload_ref,
        "summary": summary,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False, separators=(",", ":")) + "\n")


def _read_user_profile(path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if path is None:
        return None
    raw = _load_json(path)
    if not isinstance(raw, dict):
        raise ValueError("user_profile JSON must be an object")
    return raw


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract skeleton then run domain selection.")
    ap.add_argument("--topic", required=True, help="Problem/topic text")
    ap.add_argument("--session-path", help="Exploration session path")
    ap.add_argument("--skeleton-json", help="Optional existing skeleton JSON path")
    ap.add_argument("--user-profile-json", help="Optional user profile JSON path")
    ap.add_argument("--top-n", type=int, default=6, help="Number of selected domains")
    args = ap.parse_args()

    if args.session_path:
        session_path = Path(args.session_path).expanduser().resolve()
        session_path.mkdir(parents=True, exist_ok=True)
    else:
        session_path = ensure_exploration_path(args.topic)

    skeleton_path = session_path / "category_skeleton.json"
    extraction_path = session_path / "category_extraction_evidence.json"
    selection_path = session_path / "domain_selection_evidence.json"
    mailbox_path = session_path / "mailbox_events.ndjson"
    selector_artifacts_dir = session_path / "artifacts" / "domain_selection"
    selector_artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.skeleton_json:
        raw = _load_json(Path(args.skeleton_json).expanduser().resolve())
        extraction_method = "manual_json"
    else:
        extracted = CategoryExtractor.extract_from_case(args.topic)
        raw = extracted.to_simple_format()
        extraction_method = "modules.category_extraction.CategoryExtractor.extract_from_case"

    if not isinstance(raw, dict):
        raise ValueError("skeleton data must be a JSON object")
    skeleton = _normalize_skeleton(raw, args.topic)
    skeleton_json = json.dumps(skeleton, ensure_ascii=False, indent=2)
    skeleton_path.write_text(skeleton_json, encoding="utf-8")
    skeleton_sha = hashlib.sha256(
        json.dumps(skeleton, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    extraction_evidence = {
        "signal": "CATEGORY_SKELETON_EXTRACTED",
        "timestamp": _utc_now(),
        "topic": args.topic,
        "extraction_method": extraction_method,
        "category_skeleton_ref": "category_skeleton.json",
        "category_skeleton_sha256": skeleton_sha,
        "objects_count": len(skeleton["objects"]),
        "morphisms_count": len(skeleton["morphisms"]),
    }
    extraction_path.write_text(
        json.dumps(extraction_evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _append_event(
        mailbox_path,
        "CATEGORY_SKELETON_EXTRACTED",
        "category_skeleton.json",
        f"objects={len(skeleton['objects'])}, morphisms={len(skeleton['morphisms'])}",
    )

    selector = DomainSelector()
    allowed_domains = sorted(selector.domain_info.keys())
    allowed_domain_set = set(allowed_domains)
    domain_catalog = {
        "timestamp": _utc_now(),
        "source": "assets/agents/config/domain_agents.json",
        "domains": allowed_domains,
    }
    domain_catalog_sha = _sha256_json(domain_catalog)
    domain_catalog_path = selector_artifacts_dir / "domain_catalog_snapshot.json"
    domain_catalog_path.write_text(
        json.dumps(domain_catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    user_profile = _read_user_profile(
        Path(args.user_profile_json).expanduser().resolve() if args.user_profile_json else None
    )
    selector_input = {
        "timestamp": _utc_now(),
        "topic": args.topic,
        "objects": [obj["name"] for obj in skeleton["objects"]],
        "morphisms": skeleton["morphisms"],
        "user_profile": user_profile,
        "top_n": args.top_n,
    }
    selector_input_path = selector_artifacts_dir / "selector_input.json"
    selector_input_path.write_text(
        json.dumps(selector_input, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    selector_top_n = max(args.top_n * 3, args.top_n)
    result = selector.select_domains(
        objects=selector_input["objects"],
        morphisms=skeleton["morphisms"],
        user_profile=user_profile,
        top_n=selector_top_n,
    )
    selector_output = {
        "timestamp": _utc_now(),
        "topic": args.topic,
        "result": result,
    }
    selector_output_path = selector_artifacts_dir / "selector_output.json"
    selector_output_path.write_text(
        json.dumps(selector_output, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    top_domains = result.get("top_domains", [])

    knowledge_index: Dict[str, str] = {}
    unavailable_domains: List[str] = []
    for domain in allowed_domains:
        path = _resolve_domain_knowledge_file(domain)
        if path is None:
            unavailable_domains.append(domain)
        else:
            try:
                rel = path.relative_to(_skill_root()).as_posix()
            except ValueError:
                rel = str(path)
            knowledge_index[domain] = rel

    viable_domain_set = set(knowledge_index.keys())
    ranked_domains = [
        item.get("domain")
        for item in top_domains
        if isinstance(item, dict) and item.get("domain") in allowed_domain_set
    ]
    raw_selected_domains = ranked_domains[: args.top_n]
    dropped_unavailable_domains = [d for d in raw_selected_domains if d not in viable_domain_set]

    selected_domains: List[str] = []
    for d in ranked_domains:
        if d in viable_domain_set and d not in selected_domains:
            selected_domains.append(d)
        if len(selected_domains) >= args.top_n:
            break

    if len(selected_domains) < args.top_n:
        for d in selector.default_seed_domains:
            if d in viable_domain_set and d not in selected_domains:
                selected_domains.append(d)
            if len(selected_domains) >= args.top_n:
                break

    if len(selected_domains) < args.top_n:
        for d in sorted(viable_domain_set):
            if d not in selected_domains:
                selected_domains.append(d)
            if len(selected_domains) >= args.top_n:
                break

    selection_adjustment_applied = raw_selected_domains != selected_domains[: len(raw_selected_domains)] or bool(dropped_unavailable_domains)
    selector_ok = len(selected_domains) > 0
    selector_error = ""
    if not selector_ok:
        selector_error = "No viable domains with existing references/*_v2.md were found"

    domain_knowledge_catalog = {
        "timestamp": _utc_now(),
        "source": "references/*_v2.md + references/custom/*_v2.md",
        "available_domains": sorted(viable_domain_set),
        "unavailable_domains": unavailable_domains,
        "domain_file_map": knowledge_index,
    }
    domain_knowledge_sha = _sha256_json(domain_knowledge_catalog)
    domain_knowledge_path = selector_artifacts_dir / "domain_knowledge_snapshot.json"
    domain_knowledge_path.write_text(
        json.dumps(domain_knowledge_catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    selection_evidence = {
        "signal": "DOMAIN_SELECTION_EVIDENCE",
        "selection_timestamp": _utc_now(),
        "topic": args.topic,
        "selector_method": "scripts/prepare_domain_selection.py -> scripts/domain_selector.py",
        "selector_ok": selector_ok,
        "category_skeleton_ref": "category_skeleton.json",
        "category_skeleton_sha256": skeleton_sha,
        "selector_input_ref": "artifacts/domain_selection/selector_input.json",
        "selector_output_ref": "artifacts/domain_selection/selector_output.json",
        "domain_catalog_ref": "artifacts/domain_selection/domain_catalog_snapshot.json",
        "domain_catalog_sha256": domain_catalog_sha,
        "domain_knowledge_ref": "artifacts/domain_selection/domain_knowledge_snapshot.json",
        "domain_knowledge_sha256": domain_knowledge_sha,
        "selected_domains_source": "selector_output.top_domains + knowledge_viability_gate",
        "selector_requested_top_n": args.top_n,
        "selector_raw_top_domains": raw_selected_domains,
        "dropped_unavailable_domains": dropped_unavailable_domains,
        "blind_spot_generation_required": False,
        "blind_spot_domains": [],
        "blind_spot_trigger_signals": [],
        "blind_spot_domain_sources": {},
        "blind_spot_evidence_ref": None,
        "blind_spot_reason": "",
        "selection_adjustment_applied": selection_adjustment_applied,
        "selected_domains": selected_domains,
        "top_domains": top_domains,
        "selector_error": selector_error if not selector_ok else "",
        "selector_rationale": result.get("selection_reasoning") or result.get("reasoning") or "",
    }
    selection_path.write_text(
        json.dumps(selection_evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _append_event(
        mailbox_path,
        "DOMAIN_SELECTION_EVIDENCE",
        "domain_selection_evidence.json",
        f"selected_domains={len(selected_domains)}",
    )

    print(
        json.dumps(
            {
                "session_path": str(session_path),
                "category_skeleton_ref": str(skeleton_path),
                "domain_selection_ref": str(selection_path),
                "selected_domains": selected_domains,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
