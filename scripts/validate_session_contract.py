#!/usr/bin/env python3
"""Validate visualization artifact contract for a Morphism Mapper session."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = [
    "session_manifest.json",
    "mailbox_events.ndjson",
    "metadata.json",
    "category_skeleton.json",
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


def validate_domain_artifacts(root: Path) -> list[str]:
    out: list[str] = []
    manifest = _load_manifest(root)
    if not manifest:
        return out

    active_domains = manifest.get("active_domains")
    if not isinstance(active_domains, list) or not active_domains:
        out.append(_err("session_manifest.active_domains missing or empty"))
        return out

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


def _iter_event_lines(p: Path) -> Iterable[tuple[int, str]]:
    with p.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            yield i, s


def validate_events(root: Path) -> list[str]:
    out: list[str] = []
    p = root / "mailbox_events.ndjson"
    if not p.exists():
        return out

    has_signal = False
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
        if obj.get("signal"):
            has_signal = True

    if not has_signal:
        out.append(_err("mailbox_events.ndjson has no signal records"))
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
