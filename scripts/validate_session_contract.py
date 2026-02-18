#!/usr/bin/env python3
"""Validate visualization artifact contract for a Morphism Mapper session."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


REQUIRED_FILES = [
    "session_manifest.json",
    "mailbox_events.ndjson",
    "metadata.json",
    "category_skeleton.json",
    "category_extraction_evidence.json",
    "domain_selection_evidence.json",
    "launch_evidence.json",
    "final_reports/synthesis.json",
    "obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json",
    "obstruction_feedbacks/OBSTRUCTION_GATE_CLEARED.json",
]

REQUIRED_EVENT_KEYS = {
    "timestamp",
    "signal",
    "actor",
    "target",
    "domain",
    "payload_ref",
    "summary",
}

ALLOWED_RUN_MODE = {"swarm", "fallback", "hybrid"}
ALLOWED_STATUS = {"RUNNING", "COMPLETED", "BLOCKED", "FAILED"}
SESSION_ID_RE = re.compile(r"^(?P<run_id>\d{8}T\d{6}Z_[0-9a-f]{6})_(?P<slug>[A-Za-z0-9_-]+)$")
DOMAIN_ROUND_RE = re.compile(r"^(?P<domain>[a-z0-9_]+)_round(?P<round>\d+)\.json$")


def _err(msg: str) -> str:
    return f"[ERROR] {msg}"


def _warn(msg: str) -> str:
    return f"[WARN] {msg}"


def _ok(msg: str) -> str:
    return f"[OK] {msg}"


def validate_required_files(root: Path) -> list[str]:
    out: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            out.append(_err(f"missing required file: {rel}"))
    if (root / "logs" / "message_events.jsonl").exists():
        out.append(_err("legacy primary event stream detected: logs/message_events.jsonl"))
    return out


def validate_manifest(root: Path) -> list[str]:
    out: list[str] = []
    p = root / "session_manifest.json"
    if not p.exists():
        return out
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [_err(f"session_manifest.json invalid JSON: {e}")]

    if data.get("schema_version") != "session_manifest.v1":
        out.append(_err("session_manifest.schema_version must be session_manifest.v1"))
    if data.get("artifact_version") != "1.1":
        out.append(_err("session_manifest.artifact_version must be 1.1"))
    if data.get("run_mode") not in ALLOWED_RUN_MODE:
        out.append(_err("session_manifest.run_mode must be swarm|fallback|hybrid"))
    if data.get("status") not in ALLOWED_STATUS:
        out.append(_err("session_manifest.status invalid"))
    if not data.get("session_id"):
        out.append(_err("session_manifest.session_id missing"))
    if not data.get("topic"):
        out.append(_err("session_manifest.topic missing"))

    session_id = data.get("session_id")
    if isinstance(session_id, str):
        m = SESSION_ID_RE.match(session_id)
        if not m:
            out.append(
                _err(
                    "session_manifest.session_id format invalid, expected "
                    "YYYYMMDDTHHMMSSZ_xxxxxx_slug"
                )
            )
        if session_id != root.name:
            out.append(_err("session_manifest.session_id must equal exploration directory name"))
        if m:
            run_id = m.group("run_id")
            siblings = [
                p.name
                for p in root.parent.iterdir()
                if p.is_dir() and p.name.startswith(run_id + "_") and p.name != root.name
            ]
            if siblings:
                out.append(
                    _err(
                        f"multiple directories share same run_id={run_id}: "
                        + ", ".join(sorted(siblings + [root.name]))
                    )
                )

    metadata_path = root / "metadata.json"
    if metadata_path.exists():
        try:
            meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            exploration_path = meta.get("exploration_path")
            if isinstance(exploration_path, str):
                resolved = Path(exploration_path).expanduser().resolve()
                if resolved != root:
                    out.append(
                        _err("metadata.exploration_path does not match actual exploration directory")
                    )
        except Exception as e:  # noqa: BLE001
            out.append(_warn(f"metadata.json parse failed: {e}"))
    return out


def _load_manifest(root: Path) -> dict | None:
    p = root / "session_manifest.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(data, dict):
        return None
    return data


def _resolve_ref(root: Path, ref: str) -> Path | None:
    candidate = (root / ref).resolve()
    root_resolved = root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        return None
    return candidate


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_domain_artifacts(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    if not manifest:
        return out

    active_domains = manifest.get("active_domains")
    if not isinstance(active_domains, list) or not active_domains:
        out.append(_err("session_manifest.active_domains missing or empty"))
        return out

    active_domain_set = {d for d in active_domains if isinstance(d, str) and d}

    for d in active_domains:
        if not isinstance(d, str) or not d:
            out.append(_err("session_manifest.active_domains contains invalid domain value"))
            continue
        round1 = root / "domain_results" / f"{d}_round1.json"
        obs = root / "obstruction_feedbacks" / f"{d}_obstruction.json"
        if not round1.exists():
            out.append(_err(f"missing required domain result: domain_results/{d}_round1.json"))
        if not obs.exists():
            out.append(_err(f"missing required obstruction result: obstruction_feedbacks/{d}_obstruction.json"))
        if round1.exists() and obs.exists():
            try:
                if obs.stat().st_mtime < round1.stat().st_mtime:
                    out.append(
                        _err(
                            f"obstruction artifact appears earlier than domain result for {d} "
                            "(expected domain_results first, then obstruction_feedbacks)"
                        )
                    )
            except OSError as e:
                out.append(_warn(f"mtime check failed for {d}: {e}"))

    domain_dir = root / "domain_results"
    if domain_dir.exists():
        for path in sorted(domain_dir.glob("*.json")):
            m = DOMAIN_ROUND_RE.match(path.name)
            if not m:
                continue
            domain = m.group("domain")
            if domain not in active_domain_set:
                out.append(
                    _err(
                        f"domain_results contains artifact for non-active domain: {path.name} "
                        "(possible implicit blind-spot expansion)"
                    )
                )

    return out


def validate_launch_evidence(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    p = root / "launch_evidence.json"
    if not p.exists():
        return out
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [_err(f"launch_evidence.json invalid JSON: {e}")]

    if not isinstance(data, dict):
        return [_err("launch_evidence.json must be object")]

    required = ["launch_mode", "selected_domains", "active_core_members"]
    for k in required:
        if k not in data:
            out.append(_err(f"launch_evidence missing field: {k}"))

    run_mode = manifest.get("run_mode") if isinstance(manifest, dict) else None
    if run_mode == "swarm":
        for k in ["team_name", "core_ready_signals"]:
            if k not in data:
                out.append(_err(f"launch_evidence missing swarm field: {k}"))
    if run_mode == "fallback":
        for k in ["fallback_reason", "team_unavailable"]:
            if k not in data:
                out.append(_err(f"launch_evidence missing fallback field: {k}"))

    return out


def validate_category_and_selection(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    manifest_selected_domains: set[str] = set()
    manifest_active_domains: set[str] = set()
    if isinstance(manifest, dict):
        raw_selected = manifest.get("selected_domains")
        raw_active = manifest.get("active_domains")
        if isinstance(raw_selected, list):
            manifest_selected_domains = {d for d in raw_selected if isinstance(d, str) and d}
        if isinstance(raw_active, list):
            manifest_active_domains = {d for d in raw_active if isinstance(d, str) and d}
        if manifest_selected_domains and manifest_active_domains:
            missing = sorted(manifest_selected_domains - manifest_active_domains)
            if missing:
                out.append(
                    _err(
                        "session_manifest.selected_domains must be subset of active_domains: "
                        + ",".join(missing)
                    )
                )

    skill_root = Path(__file__).resolve().parents[1]
    domain_catalog_cfg = skill_root / "assets" / "agents" / "config" / "domain_agents.json"
    allowed_domains: set[str] = set()
    if domain_catalog_cfg.exists():
        try:
            cfg = json.loads(domain_catalog_cfg.read_text(encoding="utf-8"))
            domains_obj = cfg.get("domains")
            if isinstance(domains_obj, dict):
                allowed_domains = {str(k) for k in domains_obj.keys()}
        except Exception as e:  # noqa: BLE001
            out.append(_warn(f"domain catalog parse failed: {e}"))

    def resolve_domain_knowledge(domain: str) -> Path | None:
        refs = skill_root / "references"
        base_path = refs / f"{domain}_v2.md"
        custom_path = refs / "custom" / f"{domain}_v2.md"
        if base_path.exists():
            return base_path.resolve()
        if custom_path.exists():
            return custom_path.resolve()
        return None

    def has_domain_knowledge(domain: str) -> bool:
        return resolve_domain_knowledge(domain) is not None

    skeleton_path = root / "category_skeleton.json"
    extraction_path = root / "category_extraction_evidence.json"
    selection_path = root / "domain_selection_evidence.json"

    if skeleton_path.exists():
        try:
            skeleton = json.loads(skeleton_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            out.append(_err(f"category_skeleton.json invalid JSON: {e}"))
            skeleton = None
        if isinstance(skeleton, dict):
            payload = json.dumps(skeleton, ensure_ascii=False, separators=(",", ":"))
            if len(payload) > 6000:
                out.append(_err("category_skeleton payload too large (>6000 chars), must be compact"))

            disallowed_keys = {"category_objects", "category_morphisms", "objects_map", "morphisms_map"}
            hit_keys = sorted(k for k in disallowed_keys if k in skeleton)
            if hit_keys:
                out.append(
                    _err(
                        "category_skeleton uses unsupported root keys: "
                        + ",".join(hit_keys)
                        + " (use objects/morphisms/tags/核心问题 only)"
                    )
                )

            objects = skeleton.get("objects")
            morphisms = skeleton.get("morphisms")
            if not isinstance(objects, list) or not objects:
                out.append(_err("category_skeleton.objects missing or empty"))
            if not isinstance(morphisms, list) or not morphisms:
                out.append(_err("category_skeleton.morphisms missing or empty"))
            if isinstance(objects, list) and len(objects) > 12:
                out.append(_err("category_skeleton.objects too many (>12), must be trimmed"))
            if isinstance(morphisms, list) and len(morphisms) > 16:
                out.append(_err("category_skeleton.morphisms too many (>16), must be trimmed"))

            if isinstance(objects, list):
                for idx, obj in enumerate(objects):
                    if isinstance(obj, str):
                        if not obj.strip():
                            out.append(_err(f"category_skeleton.objects[{idx}] empty string"))
                    elif isinstance(obj, dict):
                        name = obj.get("name")
                        if not isinstance(name, str) or not name.strip():
                            out.append(_err(f"category_skeleton.objects[{idx}].name missing"))
                        if "attributes" in obj:
                            out.append(
                                _err(
                                    f"category_skeleton.objects[{idx}] must not include nested attributes "
                                    "(keep skeleton flat)"
                                )
                            )
                    else:
                        out.append(_err(f"category_skeleton.objects[{idx}] invalid type"))

            if isinstance(morphisms, list):
                for idx, mor in enumerate(morphisms):
                    if not isinstance(mor, dict):
                        out.append(_err(f"category_skeleton.morphisms[{idx}] invalid type"))
                        continue
                    required = ["from", "to", "dynamics"]
                    for k in required:
                        v = mor.get(k)
                        if not isinstance(v, str) or not v.strip():
                            out.append(_err(f"category_skeleton.morphisms[{idx}].{k} missing"))
                    if any(k in mor for k in ("attributes", "metadata", "details")):
                        out.append(
                            _err(
                                f"category_skeleton.morphisms[{idx}] must stay flat "
                                "(no attributes/metadata/details)"
                            )
                        )

    if extraction_path.exists():
        try:
            extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            out.append(_err(f"category_extraction_evidence.json invalid JSON: {e}"))
            extraction = None
        if isinstance(extraction, dict):
            ref = extraction.get("category_skeleton_ref")
            if not isinstance(ref, str) or not ref:
                out.append(_err("category_extraction_evidence.category_skeleton_ref missing"))
            else:
                ref_path = (root / ref).resolve()
                if ref_path != skeleton_path.resolve():
                    out.append(_err("category_extraction_evidence.category_skeleton_ref must point to category_skeleton.json"))
            method = extraction.get("extraction_method")
            if not isinstance(method, str) or not method:
                out.append(_err("category_extraction_evidence.extraction_method missing"))

    if selection_path.exists():
        try:
            selection = json.loads(selection_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            out.append(_err(f"domain_selection_evidence.json invalid JSON: {e}"))
            selection = None
        if isinstance(selection, dict):
            selected_domains = selection.get("selected_domains")
            if not isinstance(selected_domains, list) or not selected_domains:
                out.append(_err("domain_selection_evidence.selected_domains missing or empty"))
            ref = selection.get("category_skeleton_ref")
            if not isinstance(ref, str) or not ref:
                out.append(_err("domain_selection_evidence.category_skeleton_ref missing"))
            else:
                ref_path = (root / ref).resolve()
                if ref_path != skeleton_path.resolve():
                    out.append(_err("domain_selection_evidence.category_skeleton_ref must point to category_skeleton.json"))
            selector_ok = selection.get("selector_ok")
            if not isinstance(selector_ok, bool):
                out.append(_err("domain_selection_evidence.selector_ok must be boolean"))
                selector_ok = None

            blind_spot_required = selection.get("blind_spot_generation_required")
            blind_spot_domains = selection.get("blind_spot_domains")
            blind_spot_trigger_signals = selection.get("blind_spot_trigger_signals")
            blind_spot_domain_sources = selection.get("blind_spot_domain_sources")
            blind_spot_evidence_ref = selection.get("blind_spot_evidence_ref")
            blind_spot_reason = selection.get("blind_spot_reason")
            if blind_spot_required is None:
                out.append(_err("domain_selection_evidence.blind_spot_generation_required missing"))
            elif not isinstance(blind_spot_required, bool):
                out.append(_err("domain_selection_evidence.blind_spot_generation_required must be boolean"))
            if blind_spot_domains is None:
                out.append(_err("domain_selection_evidence.blind_spot_domains missing"))
            elif not isinstance(blind_spot_domains, list):
                out.append(_err("domain_selection_evidence.blind_spot_domains must be array"))
            if blind_spot_trigger_signals is None:
                out.append(_err("domain_selection_evidence.blind_spot_trigger_signals missing"))
            elif not isinstance(blind_spot_trigger_signals, list):
                out.append(_err("domain_selection_evidence.blind_spot_trigger_signals must be array"))
            if blind_spot_domain_sources is None:
                out.append(_err("domain_selection_evidence.blind_spot_domain_sources missing"))
            elif not isinstance(blind_spot_domain_sources, dict):
                out.append(_err("domain_selection_evidence.blind_spot_domain_sources must be object"))
            if blind_spot_required is False and isinstance(blind_spot_domains, list) and blind_spot_domains:
                out.append(
                    _err(
                        "domain_selection_evidence.blind_spot_domains must be empty when "
                        "blind_spot_generation_required=false"
                    )
                )
            if (
                blind_spot_required is False
                and isinstance(blind_spot_trigger_signals, list)
                and blind_spot_trigger_signals
            ):
                out.append(
                    _err(
                        "domain_selection_evidence.blind_spot_trigger_signals must be empty when "
                        "blind_spot_generation_required=false"
                    )
                )
            if (
                blind_spot_required is False
                and isinstance(blind_spot_domain_sources, dict)
                and blind_spot_domain_sources
            ):
                out.append(
                    _err(
                        "domain_selection_evidence.blind_spot_domain_sources must be empty when "
                        "blind_spot_generation_required=false"
                    )
                )
            if blind_spot_required is False and blind_spot_evidence_ref not in (None, ""):
                out.append(
                    _err(
                        "domain_selection_evidence.blind_spot_evidence_ref must be null/empty when "
                        "blind_spot_generation_required=false"
                    )
                )
            if blind_spot_required is True:
                if not isinstance(blind_spot_domains, list) or not blind_spot_domains:
                    out.append(
                        _err(
                            "domain_selection_evidence.blind_spot_domains must be non-empty "
                            "when blind_spot_generation_required=true"
                        )
                    )
                if not isinstance(blind_spot_trigger_signals, list) or not blind_spot_trigger_signals:
                    out.append(
                        _err(
                            "domain_selection_evidence.blind_spot_trigger_signals must be non-empty "
                            "when blind_spot_generation_required=true"
                        )
                    )
                else:
                    allowed_triggers = {
                        "LOW_CONFIDENCE_LEAD",
                        "LOW_CONFIDENCE_OBSTRUCTION",
                        "LOW_CONFIDENCE_SYNTHESIZER",
                        "INPUT_INCOMPLETE",
                        "OBSTRUCTION_RECHECK_REQUEST",
                    }
                    invalid = [
                        sig
                        for sig in blind_spot_trigger_signals
                        if not isinstance(sig, str) or sig not in allowed_triggers
                    ]
                    if invalid:
                        out.append(
                            _err(
                                "domain_selection_evidence.blind_spot_trigger_signals has invalid values: "
                                + ",".join(str(v) for v in invalid)
                            )
                        )
                if not isinstance(blind_spot_domain_sources, dict) or not blind_spot_domain_sources:
                    out.append(
                        _err(
                            "domain_selection_evidence.blind_spot_domain_sources must be non-empty object "
                            "when blind_spot_generation_required=true"
                        )
                    )
                if not isinstance(blind_spot_evidence_ref, str) or not blind_spot_evidence_ref:
                    out.append(
                        _err(
                            "domain_selection_evidence.blind_spot_evidence_ref must be non-empty when "
                            "blind_spot_generation_required=true"
                        )
                    )
                else:
                    eref = (root / blind_spot_evidence_ref).resolve()
                    if not eref.exists():
                        out.append(
                            _err(
                                "domain_selection_evidence.blind_spot_evidence_ref target not found"
                            )
                        )
                if not isinstance(blind_spot_reason, str) or not blind_spot_reason.strip():
                    out.append(
                        _err(
                            "domain_selection_evidence.blind_spot_reason must be non-empty when "
                            "blind_spot_generation_required=true"
                        )
                    )

            if selector_ok is False:
                selector_error = selection.get("selector_error")
                manual_reason = selection.get("manual_selection_reason")
                if not isinstance(selector_error, str) or not selector_error.strip():
                    out.append(_err("domain_selection_evidence.selector_error required when selector_ok=false"))
                if not isinstance(manual_reason, str) or not manual_reason.strip():
                    out.append(_err("domain_selection_evidence.manual_selection_reason required when selector_ok=false"))

            selector_method = selection.get("selector_method")
            if selector_ok is True:
                if not isinstance(selector_method, str) or "domain_selector.py" not in selector_method:
                    out.append(_err("domain_selection_evidence.selector_method must include domain_selector.py when selector_ok=true"))

            input_ref = selection.get("selector_input_ref")
            output_ref = selection.get("selector_output_ref")
            catalog_ref = selection.get("domain_catalog_ref")
            catalog_sha = selection.get("domain_catalog_sha256")
            knowledge_ref = selection.get("domain_knowledge_ref")
            knowledge_sha = selection.get("domain_knowledge_sha256")

            selector_output_domains: list[str] = []
            knowledge_available_domains: set[str] = set()
            if selector_ok is True:
                if not isinstance(input_ref, str) or not input_ref:
                    out.append(_err("domain_selection_evidence.selector_input_ref missing"))
                else:
                    input_path = (root / input_ref).resolve()
                    if not input_path.exists():
                        out.append(_err("domain_selection_evidence.selector_input_ref target not found"))

                if not isinstance(output_ref, str) or not output_ref:
                    out.append(_err("domain_selection_evidence.selector_output_ref missing"))
                else:
                    output_path = (root / output_ref).resolve()
                    if not output_path.exists():
                        out.append(_err("domain_selection_evidence.selector_output_ref target not found"))
                    else:
                        try:
                            output_data = json.loads(output_path.read_text(encoding="utf-8"))
                            result_obj = output_data.get("result") if isinstance(output_data, dict) else None
                            top_domains = result_obj.get("top_domains") if isinstance(result_obj, dict) else None
                            if not isinstance(top_domains, list) or not top_domains:
                                out.append(_err("selector_output.result.top_domains missing or empty"))
                            else:
                                selector_output_domains = [
                                    item.get("domain")
                                    for item in top_domains
                                    if isinstance(item, dict) and isinstance(item.get("domain"), str)
                                ]
                        except Exception as e:  # noqa: BLE001
                            out.append(_err(f"selector_output_ref invalid JSON: {e}"))

            catalog_domains: set[str] = set()
            if not isinstance(catalog_ref, str) or not catalog_ref:
                out.append(_err("domain_selection_evidence.domain_catalog_ref missing"))
            else:
                cpath = (root / catalog_ref).resolve()
                if not cpath.exists():
                    out.append(_err("domain_selection_evidence.domain_catalog_ref target not found"))
                else:
                    try:
                        catalog_data = json.loads(cpath.read_text(encoding="utf-8"))
                        domains = catalog_data.get("domains") if isinstance(catalog_data, dict) else None
                        if not isinstance(domains, list) or not domains:
                            out.append(_err("domain_catalog_ref domains missing or empty"))
                        else:
                            catalog_domains = {str(d) for d in domains}
                        if not isinstance(catalog_sha, str) or not catalog_sha:
                            out.append(_err("domain_selection_evidence.domain_catalog_sha256 missing"))
                        else:
                            actual_sha = hashlib.sha256(
                                json.dumps(catalog_data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                            ).hexdigest()
                            if actual_sha != catalog_sha:
                                out.append(_err("domain_selection_evidence.domain_catalog_sha256 mismatch"))
                    except Exception as e:  # noqa: BLE001
                        out.append(_err(f"domain_catalog_ref invalid JSON: {e}"))

            if selector_ok is True:
                if not isinstance(knowledge_ref, str) or not knowledge_ref:
                    out.append(_err("domain_selection_evidence.domain_knowledge_ref missing"))
                else:
                    kpath = (root / knowledge_ref).resolve()
                    if not kpath.exists():
                        out.append(_err("domain_selection_evidence.domain_knowledge_ref target not found"))
                    else:
                        try:
                            knowledge_data = json.loads(kpath.read_text(encoding="utf-8"))
                            available = (
                                knowledge_data.get("available_domains")
                                if isinstance(knowledge_data, dict)
                                else None
                            )
                            if not isinstance(available, list) or not available:
                                out.append(_err("domain_knowledge_ref available_domains missing or empty"))
                            else:
                                knowledge_available_domains = {str(d) for d in available}
                            if not isinstance(knowledge_sha, str) or not knowledge_sha:
                                out.append(_err("domain_selection_evidence.domain_knowledge_sha256 missing"))
                            else:
                                actual_sha = hashlib.sha256(
                                    json.dumps(knowledge_data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                                ).hexdigest()
                                if actual_sha != knowledge_sha:
                                    out.append(_err("domain_selection_evidence.domain_knowledge_sha256 mismatch"))
                        except Exception as e:  # noqa: BLE001
                            out.append(_err(f"domain_knowledge_ref invalid JSON: {e}"))

            if isinstance(selected_domains, list) and selected_domains:
                selected_domain_list = [d for d in selected_domains if isinstance(d, str) and d]
                selected_domain_set = set(selected_domain_list)
                if manifest_selected_domains and selected_domain_set != manifest_selected_domains:
                    out.append(
                        _err(
                            "domain_selection_evidence.selected_domains must match session_manifest.selected_domains"
                        )
                    )
                if manifest_active_domains:
                    expansion_domains = manifest_active_domains - selected_domain_set
                    if blind_spot_required is False and expansion_domains:
                        out.append(
                            _err(
                                "active_domains includes extra domains but blind_spot_generation_required=false: "
                                + ",".join(sorted(expansion_domains))
                            )
                        )
                    if blind_spot_required is True:
                        blind_set = (
                            {d for d in blind_spot_domains if isinstance(d, str) and d}
                            if isinstance(blind_spot_domains, list)
                            else set()
                        )
                        if blind_set != expansion_domains:
                            out.append(
                                _err(
                                    "blind_spot_domains must exactly equal "
                                    "(active_domains - selected_domains)"
                                )
                            )
                        overlap = blind_set & selected_domain_set
                        if overlap:
                            out.append(
                                _err(
                                    "blind_spot_domains must not overlap selected_domains: "
                                    + ",".join(sorted(overlap))
                                )
                            )
                        if isinstance(blind_spot_domain_sources, dict):
                            for domain in sorted(blind_set):
                                source = blind_spot_domain_sources.get(domain)
                                if source not in {"builtin", "add-domain"}:
                                    out.append(
                                        _err(
                                            f"blind spot domain source invalid for {domain}: {source}"
                                        )
                                    )
                                    continue
                                knowledge_path = resolve_domain_knowledge(domain)
                                if knowledge_path is None:
                                    out.append(
                                        _err(
                                            f"blind spot domain missing knowledge file in references: {domain}"
                                        )
                                    )
                                    continue
                                if source == "add-domain":
                                    custom_root = (skill_root / "references" / "custom").resolve()
                                    try:
                                        knowledge_path.relative_to(custom_root)
                                    except ValueError:
                                        out.append(
                                            _err(
                                                f"blind spot add-domain must resolve under references/custom: {domain}"
                                            )
                                        )

                if selector_ok is True and not selector_output_domains:
                    out.append(_err("selector_ok=true but selector_output domains missing"))
                if selector_output_domains:
                    selector_output_set = set(selector_output_domains)
                    for d in selected_domain_list:
                        if d not in selector_output_set:
                            out.append(_err(f"selected domain not present in selector output: {d}"))
                if catalog_domains:
                    for d in selected_domain_list:
                        if d not in catalog_domains:
                            out.append(_err(f"selected domain not present in domain catalog snapshot: {d}"))
                if knowledge_available_domains:
                    for d in selected_domain_list:
                        if d not in knowledge_available_domains:
                            out.append(_err(f"selected domain missing domain knowledge file: {d}"))
                if allowed_domains:
                    for d in selected_domain_list:
                        if d not in allowed_domains:
                            out.append(_err(f"selected domain not present in domain_agents.json: {d}"))
                for d in selected_domain_list:
                    if not has_domain_knowledge(d):
                        out.append(_err(f"selected domain has no knowledge file in references: {d}"))

    return out


def validate_synthesis_artifact(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    active_domains = (
        [d for d in manifest.get("active_domains", []) if isinstance(d, str) and d]
        if isinstance(manifest, dict)
        else []
    )

    synthesis_path = root / "final_reports" / "synthesis.json"
    if not synthesis_path.exists():
        return out

    try:
        synthesis = json.loads(synthesis_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [_err(f"final_reports/synthesis.json invalid JSON: {e}")]
    if not isinstance(synthesis, dict):
        return [_err("final_reports/synthesis.json must be object")]

    coverage = synthesis.get("input_coverage")
    if not isinstance(coverage, dict):
        return [_err("final_reports/synthesis.json missing required object: input_coverage")]

    cov_active = coverage.get("active_domains")
    cov_completed = coverage.get("completed_domains")
    cov_incomplete = coverage.get("incomplete_domains")
    cov_sources = coverage.get("sources")
    if not isinstance(cov_active, list):
        out.append(_err("synthesis.input_coverage.active_domains must be array"))
        cov_active = []
    if not isinstance(cov_completed, list):
        out.append(_err("synthesis.input_coverage.completed_domains must be array"))
        cov_completed = []
    if not isinstance(cov_incomplete, list):
        out.append(_err("synthesis.input_coverage.incomplete_domains must be array"))
        cov_incomplete = []
    if not isinstance(cov_sources, list):
        out.append(_err("synthesis.input_coverage.sources must be array"))
        cov_sources = []

    active_set = {d for d in active_domains if isinstance(d, str) and d}
    cov_active_set = {d for d in cov_active if isinstance(d, str) and d}
    completed_set = {d for d in cov_completed if isinstance(d, str) and d}
    incomplete_set = {d for d in cov_incomplete if isinstance(d, str) and d}

    if active_set and cov_active_set != active_set:
        out.append(_err("synthesis.input_coverage.active_domains must match session_manifest.active_domains"))
    if completed_set & incomplete_set:
        overlap = ",".join(sorted(completed_set & incomplete_set))
        out.append(_err(f"synthesis coverage conflict: domain appears in both completed/incomplete: {overlap}"))
    if cov_active_set and (completed_set | incomplete_set) != cov_active_set:
        out.append(_err("synthesis coverage mismatch: completed_domains + incomplete_domains must equal active_domains"))
    if incomplete_set:
        out.append(_err("final synthesis is not allowed when input_coverage.incomplete_domains is non-empty"))

    sources_by_domain: dict[str, dict[str, Any]] = {}
    for idx, source in enumerate(cov_sources):
        if not isinstance(source, dict):
            out.append(_err(f"synthesis.input_coverage.sources[{idx}] must be object"))
            continue
        domain = source.get("domain")
        payload_ref = source.get("payload_ref")
        read_complete = source.get("read_complete")
        content_sha256 = source.get("content_sha256")
        read_method = source.get("read_method")
        if not isinstance(domain, str) or not domain:
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].domain missing"))
            continue
        if domain in sources_by_domain:
            out.append(_err(f"synthesis.input_coverage.sources duplicate domain entry: {domain}"))
            continue
        sources_by_domain[domain] = source
        if not isinstance(payload_ref, str) or not payload_ref:
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].payload_ref missing for domain={domain}"))
            continue
        if not isinstance(read_complete, bool):
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].read_complete must be boolean for domain={domain}"))
        if not isinstance(content_sha256, str) or not re.match(r"^[a-f0-9]{64}$", content_sha256):
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].content_sha256 must be 64-hex for domain={domain}"))
        if read_method not in {"full_read", "paged_to_eof"}:
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].read_method invalid for domain={domain}"))

        ref_path = _resolve_ref(root, payload_ref)
        if ref_path is None:
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].payload_ref escapes session root: {payload_ref}"))
            continue
        if not ref_path.exists():
            out.append(_err(f"synthesis.input_coverage.sources[{idx}].payload_ref target not found: {payload_ref}"))
            continue
        if isinstance(read_complete, bool) and read_complete:
            if isinstance(content_sha256, str) and re.match(r"^[a-f0-9]{64}$", content_sha256):
                actual_sha = _sha256_file(ref_path)
                if actual_sha != content_sha256:
                    out.append(_err(f"synthesis source hash mismatch for domain={domain} payload_ref={payload_ref}"))

    for domain in cov_active_set:
        source = sources_by_domain.get(domain)
        if source is None:
            out.append(_err(f"synthesis.input_coverage.sources missing domain={domain}"))
            continue
        read_complete = source.get("read_complete")
        if domain in completed_set and read_complete is not True:
            out.append(_err(f"synthesis source read_complete must be true for completed domain={domain}"))
        if domain in incomplete_set and read_complete is not False:
            out.append(_err(f"synthesis source read_complete must be false for incomplete domain={domain}"))

    return out


def _iter_event_lines(p: Path) -> Iterable[tuple[int, str]]:
    with p.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            yield i, s


def validate_revision_round_policy(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    if not manifest:
        return out

    active_domains = manifest.get("active_domains")
    if not isinstance(active_domains, list):
        return out
    active_domain_set = {d for d in active_domains if isinstance(d, str) and d}

    domain_dir = root / "domain_results"
    round2_domains: dict[str, Path] = {}
    if domain_dir.exists():
        for path in sorted(domain_dir.glob("*.json")):
            m = DOMAIN_ROUND_RE.match(path.name)
            if not m:
                continue
            round_n = int(m.group("round"))
            if round_n >= 2:
                round2_domains[m.group("domain")] = path

    if not round2_domains:
        return out

    mailbox = root / "mailbox_events.ndjson"
    input_incomplete_domains: set[str] = set()
    mapping_round2_domains: set[str] = set()
    if mailbox.exists():
        for idx, line in _iter_event_lines(mailbox):
            try:
                event = json.loads(line)
            except Exception as e:  # noqa: BLE001
                out.append(_err(f"mailbox_events.ndjson line {idx} invalid JSON: {e}"))
                continue
            signal = str(event.get("signal") or "")
            domain = event.get("domain")
            if not isinstance(domain, str) or not domain:
                continue
            if signal == "INPUT_INCOMPLETE":
                input_incomplete_domains.add(domain)
            if signal == "MAPPING_RESULT_ROUND2":
                mapping_round2_domains.add(domain)

    revise_domains: set[str] = set()
    summary_path = root / "obstruction_feedbacks" / "OBSTRUCTION_ROUND1_SUMMARY.json"
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            verdicts = summary.get("domain_verdicts")
            if isinstance(verdicts, dict):
                for domain, verdict in verdicts.items():
                    if isinstance(domain, str) and str(verdict).upper() in {"REVISE", "REJECT"}:
                        revise_domains.add(domain)
            unresolved = summary.get("unresolved_domains")
            if isinstance(unresolved, list):
                for domain in unresolved:
                    if isinstance(domain, str) and domain:
                        revise_domains.add(domain)
        except Exception as e:  # noqa: BLE001
            out.append(_err(f"obstruction_feedbacks/OBSTRUCTION_ROUND1_SUMMARY.json invalid JSON: {e}"))

    trigger_domains = revise_domains | input_incomplete_domains
    for domain, path in sorted(round2_domains.items()):
        if active_domain_set and domain not in active_domain_set:
            out.append(
                _err(
                    f"unexpected round2 artifact for non-active domain: {path.name}"
                )
            )
        if domain not in trigger_domains:
            out.append(
                _err(
                    f"unexpected round2 artifact without trigger evidence: {path.name} "
                    "(need REVISE/REJECT/unresolved or INPUT_INCOMPLETE for this domain)"
                )
            )
        if domain not in mapping_round2_domains:
            out.append(
                _err(
                    f"round2 artifact exists but mailbox lacks MAPPING_RESULT_ROUND2 signal: {path.name}"
                )
            )

    return out


def validate_events(root: Path) -> list[str]:
    out: list[str] = []
    p = root / "mailbox_events.ndjson"
    if not p.exists():
        return out

    has_signal = False
    signal_first_line: dict[str, int] = {}
    events: list[tuple[int, dict]] = []
    for idx, line in _iter_event_lines(p):
        try:
            obj = json.loads(line)
        except Exception as e:  # noqa: BLE001
            out.append(_err(f"mailbox_events.ndjson line {idx} invalid JSON: {e}"))
            continue
        missing = [k for k in REQUIRED_EVENT_KEYS if k not in obj]
        if missing:
            out.append(_err(f"mailbox_events.ndjson line {idx} missing keys: {','.join(missing)}"))
        if "event" in obj and "signal" not in obj:
            out.append(_err(f"mailbox_events.ndjson line {idx} uses legacy event/message fields"))
        signal = obj.get("signal")
        if signal:
            has_signal = True
            if signal not in signal_first_line:
                signal_first_line[str(signal)] = idx
        events.append((idx, obj))

    if not has_signal:
        out.append(_err("mailbox_events.ndjson has no signal records"))

    required_signals = ["CATEGORY_SKELETON_EXTRACTED", "DOMAIN_SELECTION_EVIDENCE"]
    for sig in required_signals:
        if sig not in signal_first_line:
            out.append(_err(f"mailbox_events.ndjson missing required signal: {sig}"))

    if (
        "CATEGORY_SKELETON_EXTRACTED" in signal_first_line
        and "DOMAIN_SELECTION_EVIDENCE" in signal_first_line
        and signal_first_line["CATEGORY_SKELETON_EXTRACTED"] > signal_first_line["DOMAIN_SELECTION_EVIDENCE"]
    ):
        out.append(_err("signal ordering invalid: DOMAIN_SELECTION_EVIDENCE appears before CATEGORY_SKELETON_EXTRACTED"))

    manifest = _load_manifest(root)
    active_domains = (
        manifest.get("active_domains")
        if isinstance(manifest, dict) and isinstance(manifest.get("active_domains"), list)
        else []
    )

    mapping_line_by_domain: dict[str, int] = {}
    obstruction_line_by_domain: dict[str, int] = {}
    round1_complete_lines: list[int] = []
    gate_cleared_lines: list[int] = []
    input_incomplete_by_domain: dict[str, int] = {}
    input_complete_by_domain: dict[str, int] = {}
    final_request_lines: list[int] = []
    synthesis_output_lines: list[int] = []

    for idx, obj in events:
        signal = str(obj.get("signal") or "")
        domain = obj.get("domain")
        if signal.startswith("MAPPING_RESULT_ROUND") and isinstance(domain, str) and domain:
            mapping_line_by_domain.setdefault(domain, idx)
        if signal == "OBSTRUCTION_FEEDBACK" and isinstance(domain, str) and domain:
            obstruction_line_by_domain.setdefault(domain, idx)
        if signal == "OBSTRUCTION_ROUND1_COMPLETE":
            round1_complete_lines.append(idx)
        if signal == "OBSTRUCTION_GATE_CLEARED":
            gate_cleared_lines.append(idx)
        if signal == "INPUT_INCOMPLETE" and isinstance(domain, str) and domain:
            input_incomplete_by_domain.setdefault(domain, idx)
        if signal == "INPUT_COMPLETE" and isinstance(domain, str) and domain:
            input_complete_by_domain[domain] = idx
        if signal == "FINAL_SYNTHESIS_REQUEST":
            final_request_lines.append(idx)
        if signal in {"SYNTHESIS_RESULT_JSON", "SYNTHESIS_COMPLETE"}:
            synthesis_output_lines.append(idx)

    for domain, ob_line in obstruction_line_by_domain.items():
        map_line = mapping_line_by_domain.get(domain)
        if map_line is None:
            out.append(
                _err(
                    f"ordering invalid for domain={domain}: OBSTRUCTION_FEEDBACK appears before any MAPPING_RESULT_ROUND*"
                )
            )
        elif ob_line < map_line:
            out.append(
                _err(
                    f"ordering invalid for domain={domain}: OBSTRUCTION_FEEDBACK appears before MAPPING_RESULT_ROUND*"
                )
            )

    if round1_complete_lines:
        round1_line = round1_complete_lines[0]
        for domain in active_domains:
            if isinstance(domain, str) and domain and domain not in mapping_line_by_domain:
                out.append(
                    _err(
                        f"ordering invalid: OBSTRUCTION_ROUND1_COMPLETE exists but no MAPPING_RESULT_ROUND* event for domain={domain}"
                    )
                )
            elif isinstance(domain, str) and domain:
                if mapping_line_by_domain[domain] > round1_line:
                    out.append(
                        _err(
                            f"ordering invalid: domain={domain} mapping event appears after OBSTRUCTION_ROUND1_COMPLETE"
                        )
                    )
            if isinstance(domain, str) and domain and domain not in obstruction_line_by_domain:
                out.append(
                    _err(
                        f"ordering invalid: OBSTRUCTION_ROUND1_COMPLETE exists but no OBSTRUCTION_FEEDBACK event for domain={domain}"
                    )
                )
            elif isinstance(domain, str) and domain:
                if obstruction_line_by_domain[domain] > round1_line:
                    out.append(
                        _err(
                            f"ordering invalid: domain={domain} OBSTRUCTION_FEEDBACK appears after OBSTRUCTION_ROUND1_COMPLETE"
                        )
                    )

    if gate_cleared_lines and round1_complete_lines:
        if gate_cleared_lines[0] < round1_complete_lines[0]:
            out.append(
                _err("ordering invalid: OBSTRUCTION_GATE_CLEARED appears before OBSTRUCTION_ROUND1_COMPLETE")
            )

    unresolved_input_domains: list[str] = []
    unresolved_first_line: int | None = None
    for domain, incomplete_line in input_incomplete_by_domain.items():
        complete_line = input_complete_by_domain.get(domain)
        if complete_line is None or complete_line < incomplete_line:
            unresolved_input_domains.append(domain)
            if unresolved_first_line is None or incomplete_line < unresolved_first_line:
                unresolved_first_line = incomplete_line

    if unresolved_input_domains and unresolved_first_line is not None:
        unresolved_label = ",".join(sorted(unresolved_input_domains))
        if any(line > unresolved_first_line for line in final_request_lines):
            out.append(
                _err(
                    "ordering invalid: FINAL_SYNTHESIS_REQUEST emitted while unresolved INPUT_INCOMPLETE exists "
                    f"(domains={unresolved_label})"
                )
            )
        if any(line > unresolved_first_line for line in synthesis_output_lines):
            out.append(
                _err(
                    "ordering invalid: synthesis output emitted while unresolved INPUT_INCOMPLETE exists "
                    f"(domains={unresolved_label})"
                )
            )

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("session_path", help="Path to session exploration directory")
    args = ap.parse_args()
    root = Path(args.session_path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(_err(f"invalid session path: {root}"))
        return 2

    results: list[str] = []
    results.extend(validate_required_files(root))
    results.extend(validate_manifest(root))
    results.extend(validate_domain_artifacts(root))
    results.extend(validate_launch_evidence(root))
    results.extend(validate_category_and_selection(root))
    results.extend(validate_revision_round_policy(root))
    results.extend(validate_synthesis_artifact(root))
    results.extend(validate_events(root))

    errors = [x for x in results if x.startswith("[ERROR]")]
    if not results:
        print(_ok("session contract passed"))
        return 0

    for line in results:
        print(line)
    if errors:
        return 1
    print(_warn("session contract passed with warnings"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
