#!/usr/bin/env python3
"""Strict gate wrapper for Morphism Mapper artifacts.

Usage:
  python3 scripts/strict_gate.py --phase domain <session_path> [--domain xxx ...]
  python3 scripts/strict_gate.py --phase session <session_path>
  python3 scripts/strict_gate.py --phase final <session_path>
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DOMAIN_ROUND_RE = re.compile(r"^(?P<domain>[a-z0-9_]+)_round(?P<round>\d+)\.json$")
DOMAIN_LEGACY_RE = re.compile(r"^(?P<domain>[a-z0-9_]+)\.json$")


def _run(cmd: List[str]) -> int:
    proc = subprocess.run(cmd)
    return proc.returncode


def _discover_domain_candidates(
    session_path: Path,
    domains: Optional[List[str]] = None,
) -> Tuple[List[Path], List[str]]:
    domain_dir = session_path / "domain_results"
    errors: List[str] = []
    if not domain_dir.exists() or not domain_dir.is_dir():
        return [], [f"[ERROR] missing directory: {domain_dir}"]

    by_domain: Dict[str, Dict[str, Path]] = {}
    for path in sorted(domain_dir.glob("*.json")):
        name = path.name
        m_round = DOMAIN_ROUND_RE.match(name)
        if m_round:
            domain = m_round.group("domain")
            by_domain.setdefault(domain, {})
            by_domain[domain][f"round{m_round.group('round')}"] = path
            continue
        m_legacy = DOMAIN_LEGACY_RE.match(name)
        if m_legacy:
            domain = m_legacy.group("domain")
            by_domain.setdefault(domain, {})
            by_domain[domain]["legacy"] = path

    selected_domains = domains or sorted(by_domain.keys())
    selected_files: List[Path] = []
    for domain in selected_domains:
        candidates = by_domain.get(domain)
        if not candidates:
            errors.append(f"[ERROR] missing domain result for: {domain}")
            continue
        rounds = [
            (int(key.removeprefix("round")), path)
            for key, path in candidates.items()
            if key.startswith("round")
        ]
        if rounds:
            _, path = max(rounds, key=lambda x: x[0])
            selected_files.append(path)
        elif "legacy" in candidates:
            selected_files.append(candidates["legacy"])
        else:
            errors.append(f"[ERROR] no usable domain file for: {domain}")
    return selected_files, errors


def _validate_domain_filenames(files: List[Path], allow_legacy: bool) -> List[str]:
    errors: List[str] = []
    for path in files:
        if DOMAIN_ROUND_RE.match(path.name):
            continue
        if allow_legacy and DOMAIN_LEGACY_RE.match(path.name):
            continue
        errors.append(
            f"[ERROR] invalid domain filename (must be *_roundN.json): {path.name}"
        )
    return errors


def _validate_domain_schema(files: List[Path], root: Path) -> int:
    if not files:
        print("[ERROR] no domain files selected for schema validation")
        return 1
    script = root / "scripts" / "validate_mapping_json.py"
    cmd = [sys.executable, str(script)] + [str(p) for p in files]
    print(f"[GATE] domain schema check: {' '.join(cmd)}", flush=True)
    return _run(cmd)


def _validate_session_contract(session_path: Path, root: Path) -> int:
    script = root / "scripts" / "validate_session_contract.py"
    cmd = [sys.executable, str(script), str(session_path)]
    print(f"[GATE] session contract check: {' '.join(cmd)}", flush=True)
    return _run(cmd)


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    ap = argparse.ArgumentParser(
        description="Strict gate wrapper for domain schema and session contract checks."
    )
    ap.add_argument(
        "--phase",
        choices=["domain", "session", "final"],
        default="final",
        help="domain: only domain schema; session: only contract; final: both",
    )
    ap.add_argument(
        "session_path",
        nargs="?",
        default=os.environ.get("MORPHISM_EXPLORATION_PATH"),
        help="Session directory path. Defaults to $MORPHISM_EXPLORATION_PATH.",
    )
    ap.add_argument(
        "--domain",
        action="append",
        dest="domains",
        help="Validate specific domain(s). Repeatable.",
    )
    ap.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Validate specific domain result file(s). Repeatable.",
    )
    ap.add_argument(
        "--allow-legacy-name",
        action="store_true",
        help="Allow legacy domain_results/<domain>.json file names in domain phase.",
    )
    args = ap.parse_args()

    if not args.session_path:
        print("[ERROR] missing session_path and MORPHISM_EXPLORATION_PATH is unset")
        return 2

    session_path = Path(args.session_path).expanduser().resolve()
    if not session_path.exists() or not session_path.is_dir():
        print(f"[ERROR] invalid session_path: {session_path}")
        return 2

    overall_rc = 0

    if args.phase in ("domain", "final"):
        if args.files:
            domain_files = [Path(p).expanduser().resolve() for p in args.files]
            discovery_errors: List[str] = []
        else:
            domain_files, discovery_errors = _discover_domain_candidates(session_path, args.domains)

        for err in discovery_errors:
            print(err)
        if discovery_errors:
            return 1

        filename_errors = _validate_domain_filenames(domain_files, args.allow_legacy_name)
        for err in filename_errors:
            print(err)
        if filename_errors:
            overall_rc = 1

        rc = _validate_domain_schema(domain_files, root)
        if rc != 0:
            overall_rc = rc
            if args.phase == "domain":
                return rc

    if args.phase in ("session", "final"):
        rc = _validate_session_contract(session_path, root)
        if rc != 0:
            overall_rc = rc

    if overall_rc == 0:
        print(f"[GATE] PASSED phase={args.phase} session={session_path}")
    else:
        print(f"[GATE] FAILED phase={args.phase} session={session_path}")
    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main())
