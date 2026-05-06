#!/usr/bin/env python3
"""rebuild_pfd_schedule_d_khanna.py — cold-start re-derivation of Khanna PFD
Schedule D liabilities aggregates.

Loads the bundled structured Schedule D row substrate at
``data/occ/khanna_pfd_schedule_d_2026_05_02.json`` (one-time export from
``lake.house_pfd_schedule_d_liabilities``, filtered to Khanna SP-owned Goldman
Sachs margin facility chain, TY2016-TY2019 — see snapshot's
``substrate_authoritative_note``). Re-derives the per-tax-year aggregate
(`by_year`) and the load-bearing invariant block (`load_bearing_invariants`)
from the structured ``rows`` array, and writes a REBUILT JSON whose shape
mirrors the snapshot's aggregate fields. The companion verifier kit
(``verify_anchors_occ.py --diff-snapshots-vs-live``) runs this script under
the hood to compare REBUILT vs bundled snapshot for BIT-EXACT match.

Reviewer cookie-cutter recipe (cold-start; no lake access, no API spend, no
Gemini, stdlib-only)::

    cd OCC_FILING_PACKAGE_V2/
    python data/ocr_products/rebuild_pfd_schedule_d_khanna.py

Output goes to ``data/ocr_products/pfd_schedule_d_khanna_REBUILT.json``.

Authoritative substrate: ``lake.house_pfd_schedule_d_liabilities`` (House
Periodic Financial Disclosure Schedule D, structured per-row from House Clerk
bulk fetch + per-page Gemini extraction). Filter discipline (per s11
ADDENDUM dig-deeper landing): the ``year`` integer column is uniformly NULL
on this table; ``year_`` text column carries the actual filing year. Member
columns are ``member_first_name`` / ``member_last_name`` (NOT
``filer_first`` / ``filer_last``). Owner code 'SP' (Khanna's spouse)
isolates the load-bearing margin facility chain addressed in Counts 3 + 7
of the OCC complaint.

Architecture parity with ``rebuild_ptr_audit_khanna.py`` (s27 B-F1): both
scripts load a one-time bundled raw-substrate snapshot, apply the
canonical aggregation that the lake substrate would produce server-side,
and emit a REBUILT JSON for BIT-EXACT comparison against the snapshot's
authoritative aggregate fields.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import sys
from typing import Any


# Body's load-bearing invariants. Re-derived from `rows` per tax_year and
# compared to the snapshot's stored `load_bearing_invariants`. The
# TY2017 $1M+ Goldman SP single-line is the post-swearing-in margin-scaffold
# anchor that is mechanically incompatible with the passive-SMA / QBT / EIF
# affirmative defense under 5 U.S.C. § 13104(f)(3) — see Count 3 paragraph
# 34d + Count 6 paragraph 64b in OCC_COMPLAINT_KHANNA.md.
EXPECTED_INVARIANTS = {
    "n_rows_total": 13,
    "tax_years_present": ["2016", "2017", "2018", "2019"],
    "ty2017_has_1m_plus_line": True,
}


def derive_by_year(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group structured Schedule D rows by tax_year and aggregate.

    Returns a list of {tax_year, n_rows, sum_amount_min, sum_amount_max,
    has_1m_plus_line} records sorted ascending by tax_year. Mirrors the
    canonical aggregation the lake substrate would produce server-side.
    """
    by_year: dict[str, dict[str, Any]] = {}
    for r in rows:
        ty = r.get("tax_year")
        if ty is None:
            continue
        bucket = by_year.setdefault(
            ty,
            {
                "tax_year": ty,
                "n_rows": 0,
                "sum_amount_min": 0.0,
                "sum_amount_max": 0.0,
                "has_1m_plus_line": False,
            },
        )
        bucket["n_rows"] += 1
        amt_min = r.get("amount_min") or 0.0
        amt_max = r.get("amount_max") or 0.0
        bucket["sum_amount_min"] += float(amt_min)
        bucket["sum_amount_max"] += float(amt_max)
        # has_1m_plus_line: any line whose amount_max upper bracket reaches
        # $1,000,000 — captures the strict TY2017 "$1,000,001-$5,000,000"
        # anchor (Count 3 paragraph 34d + Count 6 paragraph 64b body
        # invariant) plus the broader "Over $1,000,000" / "$500,001-
        # $1,000,000" bracket lines that close at the $1M cap. Snapshot's
        # encoding heuristic, preserved here for BIT-EXACT match.
        if float(amt_max) >= 1_000_000.0:
            bucket["has_1m_plus_line"] = True
    return sorted(by_year.values(), key=lambda b: b["tax_year"])


def derive_invariants(rows: list[dict[str, Any]],
                      by_year: list[dict[str, Any]]) -> dict[str, Any]:
    """Re-derive load_bearing_invariants from rows + by_year aggregate."""
    tax_years_present = [b["tax_year"] for b in by_year]
    ty2017 = next((b for b in by_year if b["tax_year"] == "2017"), None)
    return {
        "n_rows_total": len(rows),
        "tax_years_present": tax_years_present,
        "ty2017_has_1m_plus_line": bool(ty2017 and ty2017["has_1m_plus_line"]),
    }


def compute_rebuild(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Run the full Schedule D aggregation pipeline against the snapshot's
    bundled structured rows.
    """
    rows = snapshot.get("rows") or []
    by_year = derive_by_year(rows)
    invariants = derive_invariants(rows, by_year)
    return {
        "rebuild_run_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "snapshot_input": snapshot.get("snapshot_target"),
        "snapshot_date": snapshot.get("snapshot_date"),
        "n_rows": len(rows),
        "by_year": by_year,
        "load_bearing_invariants": invariants,
    }


def diff_against_snapshot(
    rebuilt: dict[str, Any], snapshot: dict[str, Any]
) -> list[tuple[str, Any, Any, str]]:
    """Compare REBUILT aggregates to snapshot's stored aggregates.

    Returns list of (field, expected, actual, status). status ∈
    {OK, DRIFT_VALUE}.
    """
    diffs: list[tuple[str, Any, Any, str]] = []

    # n_rows scalar
    diffs.append((
        "n_rows", snapshot.get("n_rows"), rebuilt.get("n_rows"),
        "OK" if snapshot.get("n_rows") == rebuilt.get("n_rows") else "DRIFT_VALUE",
    ))

    # by_year list comparison (year-by-year)
    snap_by_year = {b["tax_year"]: b for b in (snapshot.get("by_year") or [])}
    rebuilt_by_year = {b["tax_year"]: b for b in (rebuilt.get("by_year") or [])}
    all_years = sorted(set(snap_by_year) | set(rebuilt_by_year))
    for y in all_years:
        s = snap_by_year.get(y, {})
        r = rebuilt_by_year.get(y, {})
        for field in ("n_rows", "sum_amount_min", "sum_amount_max",
                      "has_1m_plus_line"):
            sv = s.get(field)
            rv = r.get(field)
            if isinstance(sv, float) or isinstance(rv, float):
                ok = abs((sv or 0) - (rv or 0)) < 0.01
            else:
                ok = sv == rv
            diffs.append((
                f"by_year[TY{y}].{field}", sv, rv,
                "OK" if ok else "DRIFT_VALUE",
            ))

    # load_bearing_invariants comparison (skip rationale_* free-text fields)
    snap_inv = snapshot.get("load_bearing_invariants") or {}
    rebuilt_inv = rebuilt.get("load_bearing_invariants") or {}
    for field in ("n_rows_total", "tax_years_present",
                  "ty2017_has_1m_plus_line"):
        sv = snap_inv.get(field)
        rv = rebuilt_inv.get(field)
        diffs.append((
            f"invariants.{field}", sv, rv,
            "OK" if sv == rv else "DRIFT_VALUE",
        ))

    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    here = pathlib.Path(__file__).resolve().parent
    pkg_root = here.parent.parent  # OCC_FILING_PACKAGE_V2/
    parser.add_argument(
        "--snapshot",
        default=str(
            pkg_root / "data" / "occ"
            / "khanna_pfd_schedule_d_2026_05_02.json"),
        help="path to bundled Schedule D snapshot JSON",
    )
    parser.add_argument(
        "--output",
        default=str(here / "pfd_schedule_d_khanna_REBUILT.json"),
        help="path to write REBUILT aggregate JSON",
    )
    parser.add_argument("--quiet", action="store_true",
                        help="suppress per-field diff lines")
    args = parser.parse_args()

    snap_path = pathlib.Path(args.snapshot)
    out_path = pathlib.Path(args.output)
    if not snap_path.exists():
        print(f"ERROR: snapshot not found at {snap_path}", file=sys.stderr)
        return 2

    print(f"Loading snapshot {snap_path} ...", file=sys.stderr)
    snapshot = json.loads(snap_path.read_text(encoding="utf-8"))
    print(f"  {snapshot.get('n_rows', 0)} structured rows", file=sys.stderr)

    rebuilt = compute_rebuild(snapshot)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(
        (json.dumps(rebuilt, indent=2, default=str) + "\n").encode("utf-8")
    )

    print(f"\nREBUILT aggregate -> {out_path}")
    print(f"  n_rows                 : {rebuilt['n_rows']}")
    print(f"  tax_years_present      : "
          f"{rebuilt['load_bearing_invariants']['tax_years_present']}")
    print(f"  ty2017_has_1m_plus_line: "
          f"{rebuilt['load_bearing_invariants']['ty2017_has_1m_plus_line']}")

    diffs = diff_against_snapshot(rebuilt, snapshot)
    n_ok = sum(1 for d in diffs if d[3] == "OK")
    n_drift = sum(1 for d in diffs if d[3] == "DRIFT_VALUE")
    if not args.quiet:
        print("\nField-by-field diff vs bundled snapshot's aggregates:")
        print(f"  {'field':40s}  {'expected':>20s}  {'actual':>20s}  status")
        for field, exp, act, status in diffs:
            print(f"  {field:40s}  {str(exp):>20s}  {str(act):>20s}  "
                  f"{status}")
    print(f"\nSUMMARY: {n_ok}/{len(diffs)} fields match snapshot "
          f"({n_drift} drift)")

    # Cross-check the EXPECTED_INVARIANTS constants (defense against
    # snapshot file being modified upstream without updating this script).
    exp_n = EXPECTED_INVARIANTS["n_rows_total"]
    exp_years = EXPECTED_INVARIANTS["tax_years_present"]
    exp_1m = EXPECTED_INVARIANTS["ty2017_has_1m_plus_line"]
    actual_inv = rebuilt["load_bearing_invariants"]
    body_drift = []
    if actual_inv["n_rows_total"] != exp_n:
        body_drift.append(
            f"n_rows_total: expected {exp_n} got "
            f"{actual_inv['n_rows_total']}"
        )
    if actual_inv["tax_years_present"] != exp_years:
        body_drift.append(
            f"tax_years_present: expected {exp_years} got "
            f"{actual_inv['tax_years_present']}"
        )
    if actual_inv["ty2017_has_1m_plus_line"] != exp_1m:
        body_drift.append(
            f"ty2017_has_1m_plus_line: expected {exp_1m} got "
            f"{actual_inv['ty2017_has_1m_plus_line']}"
        )
    if body_drift:
        print("\nBODY-INVARIANT DRIFT (script-vs-rebuild) — would block "
              "filing readiness:")
        for d in body_drift:
            print(f"  - {d}")
        return 1

    return 0 if n_drift == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
