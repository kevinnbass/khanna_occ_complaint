#!/usr/bin/env python3
"""rebuild_peer_baseline.py — peer-46 baseline rebuild (B-F5).

Depends on the F4 chamber-wide rebuild output at
``data/ocr_products/house_chamber_audit_REBUILT.json``. Filters chamber
per-Member aggregates to the bundled peer-46 roster
(``data/occ/peer46_roster_2026_05_03.csv``) and computes the late-rate +
worst-days percentile blocks matching
``data/occ/peer_baseline_percentiles_2026_05_02.json`` shape.

This script is intentionally narrow — it only re-derives the late-rate
+ worst-late-days metrics that B-F4's chamber rebuild produces. Other
peer-baseline metrics in the bundled snapshot (defense_prime_pct,
ndaa_window_pct_of_defense, sp_dc_trade_pct, etc.) require additional
substrate (defense-prime ticker classifier, NDAA enactment-window
constants, owner-code distribution) that lives in the broader
``ro_khanna.peer_baseline`` derivation pipeline. Those metrics remain
verifier-MANUAL or PWD/substrate_class_anchor in the existing Phase A
verifier wiring; B-F5 closes the late-rate + worst-late-days legs only.

Reviewer cookie-cutter recipe (cold-start; no lake access; depends on
F4 having already produced the chamber REBUILT output)::

    cd OCC_FILING_PACKAGE_V2/
    python data/ocr_products/rebuild_chamber_audit.py --full-chamber --cost-acknowledged
    python data/ocr_products/rebuild_peer_baseline.py

Output: ``data/ocr_products/peer_baseline_percentiles_REBUILT.json``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import pathlib
import sys
from typing import Any

PROJECT_ROOT_OCC = pathlib.Path(__file__).resolve().parents[2]
DATA_OCC = PROJECT_ROOT_OCC / "data" / "occ"
DATA_OCR = PROJECT_ROOT_OCC / "data" / "ocr_products"

CHAMBER_REBUILT = DATA_OCR / "house_chamber_audit_REBUILT.json"
PEER46_ROSTER = DATA_OCC / "peer46_roster_2026_05_03.csv"
SNAPSHOT = DATA_OCC / "peer_baseline_percentiles_2026_05_02.json"
OUT_PATH = DATA_OCR / "peer_baseline_percentiles_REBUILT.json"

KHANNA_NAME_TOKEN = "KHANNA"
KHANNA_STATE_DST = "CA17"


def _pct(arr: list[float], p: float) -> float:
    if not arr:
        return 0.0
    arr = sorted(arr)
    k = max(0, min(len(arr) - 1, int(round((p / 100) * (len(arr) - 1)))))
    return arr[k]


def load_peer46_roster() -> list[dict[str, str]]:
    with PEER46_ROSTER.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_member_in_chamber(rebuilt_members: list[dict[str, Any]],
                            peer: dict[str, str]) -> dict[str, Any] | None:
    """Best-effort match of peer roster row to chamber rebuild member.
    Match key: state_district + last_name (case-insensitive).
    """
    sd = (peer.get("state_district") or "").strip().upper()
    name_full = (peer.get("name") or "").strip()
    name_tokens = name_full.upper().split()
    last = name_tokens[-1] if name_tokens else ""
    for m in rebuilt_members:
        m_sd = (m.get("state_district") or "").strip().upper()
        m_last = (m.get("member_last_name") or "").strip().upper()
        if m_sd == sd and m_last == last:
            return m
    # Fallback: state_district only (handles name spelling variants)
    matches = [m for m in rebuilt_members
               if (m.get("state_district") or "").strip().upper() == sd]
    if len(matches) == 1:
        return matches[0]
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    if not CHAMBER_REBUILT.exists():
        print(f"FATAL: {CHAMBER_REBUILT} not found.\n"
              f"Run B-F4 first: `python data/ocr_products/rebuild_chamber_audit.py "
              f"--full-chamber --cost-acknowledged` (OR `--sample-rebuild` for "
              f"the author-side validation path).")
        return 1

    chamber = json.loads(CHAMBER_REBUILT.read_text(encoding="utf-8"))
    members = chamber.get("members", [])
    if not members:
        print("FATAL: chamber REBUILT has no members[] block.")
        return 2

    roster = load_peer46_roster()
    is_full = bool(chamber.get("is_full_chamber_rebuild"))
    n_members_in_sample = chamber.get("n_members_in_sample", len(members))

    matched_peers: list[dict[str, Any]] = []
    unmatched: list[dict[str, str]] = []
    for peer in roster:
        m = find_member_in_chamber(members, peer)
        if m is None:
            unmatched.append(peer)
            continue
        matched_peers.append({
            "peer_name": peer.get("name"),
            "peer_state_district": peer.get("state_district"),
            "peer_bioguide_id": peer.get("bioguide_id"),
            "is_subject": peer.get("is_subject", "").upper() == "TRUE",
            "n_tx_total": m.get("n_tx_total"),
            "n_tx_late": m.get("n_tx_late"),
            "pct_late": m.get("pct_late"),
            "worst_days_late": m.get("worst_days_late"),
        })

    if not args.quiet:
        print(f"[peer-baseline rebuild] chamber rebuild members={len(members)} "
              f"(is_full_chamber_rebuild={is_full})")
        print(f"  peer-46 roster: {len(roster)} peers")
        print(f"  matched in chamber rebuild: {len(matched_peers)}")
        print(f"  unmatched: {len(unmatched)}")

    # Khanna anchor (subject row)
    khanna = next((m for m in members
                   if (m.get("member_last_name") or "").upper() == KHANNA_NAME_TOKEN
                   and (m.get("state_district") or "").upper() == KHANNA_STATE_DST), None)

    rates = [p["pct_late"] for p in matched_peers if p["pct_late"] is not None]
    worsts = [p["worst_days_late"] for p in matched_peers if p["worst_days_late"] is not None]

    metrics = []
    if rates:
        rate_metric = {
            "metric_name": "late_rate_pct",
            "n_peers": len(rates),
            "p25": _pct(rates, 25),
            "p50": _pct(rates, 50),
            "p75": _pct(rates, 75),
            "p95": _pct(rates, 95),
        }
        if khanna is not None:
            kv = khanna.get("pct_late")
            rate_metric["khanna_value"] = kv
            sorted_rates = sorted(rates)
            rank = sum(1 for r in sorted_rates if r <= kv) if kv is not None else None
            rate_metric["khanna_rank_le_n"] = rank
            rate_metric["khanna_percentile"] = (round(rank / len(sorted_rates) * 100, 2)
                                                 if rank else None)
        metrics.append(rate_metric)

    if worsts:
        sev_metric = {
            "metric_name": "worst_late_days",
            "n_peers": len(worsts),
            "p25": _pct(worsts, 25),
            "p50": _pct(worsts, 50),
            "p75": _pct(worsts, 75),
            "p95": _pct(worsts, 95),
        }
        if khanna is not None:
            kv = khanna.get("worst_days_late")
            sev_metric["khanna_value"] = kv
            sorted_worsts = sorted(worsts)
            rank = sum(1 for w in sorted_worsts if w <= kv) if kv is not None else None
            sev_metric["khanna_rank_le_n"] = rank
            sev_metric["khanna_percentile"] = (round(rank / len(sorted_worsts) * 100, 2)
                                                if rank else None)
        metrics.append(sev_metric)

    out: dict[str, Any] = {
        "rebuild_run_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "snapshot_target": "OCC_M012 peer-46 baseline (late-rate + worst-late-days legs)",
        "snapshot_input": "data/occ/peer_baseline_percentiles_2026_05_02.json",
        "chamber_rebuild_input": str(CHAMBER_REBUILT.relative_to(PROJECT_ROOT_OCC)),
        "peer46_roster": str(PEER46_ROSTER.relative_to(PROJECT_ROOT_OCC)),
        "is_full_chamber_rebuild_upstream": is_full,
        "n_members_in_chamber_rebuild": len(members),
        "n_peers_in_roster": len(roster),
        "n_peers_matched": len(matched_peers),
        "n_peers_unmatched": len(unmatched),
        "unmatched_sample": unmatched[:5],
        "metrics": metrics,
        "narrow_scope_disclosure": (
            "Only late-rate + worst-late-days legs of OCC_M012's peer baseline "
            "are re-derivable from the F4 chamber rebuild. defense_prime_pct, "
            "ndaa_window_pct_of_defense, sp_dc_trade_pct, top_employer_donor_pct, "
            "protect_progress_ie_amount remain anchored on the broader "
            "ro_khanna.peer_baseline derivation pipeline (verifier kinds: "
            "peer_baseline_metric_resolve via v3_facts_substrate_class)."
        ),
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    if not args.quiet:
        print(f"\n[peer-baseline rebuild] wrote {OUT_PATH}")
        for m in metrics:
            print(f"  {m['metric_name']}: n={m['n_peers']} "
                  f"p50={m['p50']} khanna={m.get('khanna_value','?')} "
                  f"rank={m.get('khanna_rank_le_n','?')}/{m['n_peers']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
