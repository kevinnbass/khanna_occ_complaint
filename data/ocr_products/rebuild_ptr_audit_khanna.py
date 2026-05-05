#!/usr/bin/env python3
"""rebuild_ptr_audit_khanna.py — cold-start re-derivation of Khanna PTR audit aggregates.

Loads the bundled raw structured PTR row substrate at
``data/occ/khanna_ptr_transactions_2026_05_02.json`` (one-time export from
``lake.house_ptr_transactions`` — see snapshot file's ``source_query``), applies
the canonical-view tx-key amendment-cascade dedup, applies the audit_flag
exclusions (no_tx_date / tx_after_filing / pre_stock_act / pre_tenure /
parse_error_suspect), computes days_late per row using the
``LEAST(notification_date + 30d, transaction_date + 45d)`` deadline formula,
and aggregates into a JSON output matching
``data/occ/ptr_filing_audit_khanna_2026_05_02.json``'s scalar fields.

Reviewer cookie-cutter recipe (cold-start; no lake access, no API spend, no
Gemini, stdlib-only)::

    cd OCC_FILING_PACKAGE_V2/
    python data/ocr_products/rebuild_ptr_audit_khanna.py

Output goes to ``data/ocr_products/ptr_filing_audit_khanna_REBUILT.json``.
The companion verifier kit (``verify_anchors_occ.py --diff-snapshots-vs-live``)
runs this script under the hood to compare REBUILT vs bundled snapshot.

Authoritative substrate: ``lake.house_ptr_transactions`` (raw structured rows
from Gemini per-page extraction; 1:1 with PDF tx rows; pre-canonical-view
dedup). The dedup + days_late + audit_flag rules are documented in
``.claude/rules/stock-act-audit.md`` and mirrored inline below for cookie-cutter
self-containment.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import statistics
import sys
from typing import Any

# Khanna swearing-in (per stock-act-audit.md §Pre-tenure filter); STOCK Act §6
# binds from this date forward. Bundled in the snapshot as ``served_from_iso``;
# this constant is a fallback for when the snapshot lacks the field.
KHANNA_SERVED_FROM = _dt.date(2017, 1, 3)
PRE_TENURE_GRACE_DAYS = 30  # tx_date < (served_from - 30) are pre_tenure

# STOCK Act effective date (P.L. 112-105 enacted 2012-04-04; §6 PTR provision
# operational from 2012-08-15 per House Ethics implementing guidance).
STOCK_ACT_EFFECTIVE = _dt.date(2012, 8, 15)

# Days-late deadline formula constants (stock-act-audit.md §Deadline formula).
NOTIF_DEADLINE_DAYS = 30
TX_DEADLINE_DAYS = 45

# Tightened parse_error_suspect heuristic threshold (stock-act-audit.md
# §Parse-error sentinel — tightened heuristic). A doc with a small (<20)
# pre-modern cluster embedded inside a mostly-modern filing is flagged; pure
# pre-modern batched-late amendments are NOT flagged.
PARSE_ERROR_YEAR_GAP = 3
PARSE_ERROR_MAX_OLD_TX = 20

# OCC body's load-bearing post-canonical-view aggregates (snapshot's
# expected_aggregates). The rebuild output is compared against these for the
# differ's CLEAN/DRIFT verdict.
EXPECTED_AGGREGATES = {
    "n_tx_total": 35954,
    "n_tx_late": 624,
    "n_docs_total": 114,
    "n_docs_with_late": 22,
    "pct_late": 1.74,
    "worst_days_late": 358,
    "n_tx_over_90d_late": 68,
    "n_tx_over_180d_late": 63,
    "n_tx_over_1yr_late": 0,
    "median_days_late_when_late": 9.0,
}


def _parse_iso(s: str | None) -> _dt.date | None:
    if not s:
        return None
    return _dt.date.fromisoformat(s)


def load_snapshot(path: pathlib.Path) -> dict[str, Any]:
    """Load the bundled raw-substrate snapshot."""
    with path.open("rb") as f:
        return json.loads(f.read().decode("utf-8"))


def canonical_dedup(transactions: list[dict[str, Any]],
                    filing_index: dict[str, _dt.date]) -> list[dict[str, Any]]:
    """Apply canonical-view tx-key dedup (lake.house_ptr_transactions_canonical).

    tx-key = (filer_key, asset_name, transaction_date, transaction_type, owner_key)
    where filer_key = "last|first|state_district" and owner_key = COALESCE(owner, '').

    For each tx-key partition the canonical row carries:
      - earliest_filing_date (drives days_late)
      - earliest_doc_id
      - amount fields from the LATEST filing (filer's corrected value)
      - notification_date from the EARLIEST notification_date

    Returns the deduped list; n_filings + all_doc_ids preserved as cascade
    provenance.
    """
    # Group by tx-key
    groups: dict[tuple, list[dict[str, Any]]] = {}
    for tx in transactions:
        filer_key = "{}|{}|{}".format(
            tx.get("member_last_name") or "",
            tx.get("member_first_name") or "",
            tx.get("state_district") or "",
        )
        owner_key = tx.get("owner") or ""
        key = (filer_key, tx.get("asset_name"), tx.get("transaction_date"),
               tx.get("transaction_type"), owner_key)
        groups.setdefault(key, []).append(tx)

    out: list[dict[str, Any]] = []
    for key, rows in groups.items():
        # Annotate with filing_date for sorting
        for r in rows:
            r["_filing_date"] = filing_index.get(r["doc_id"])
        # earliest filing_date for days_late computation
        rows_with_fd = [r for r in rows if r["_filing_date"] is not None]
        if not rows_with_fd:
            continue
        earliest = min(rows_with_fd, key=lambda r: (r["_filing_date"], r["doc_id"]))
        latest = max(rows_with_fd, key=lambda r: (r["_filing_date"], r["doc_id"]))
        # earliest notification_date among the partition (NULL-tolerant)
        notif_dates = [r.get("notification_date") for r in rows_with_fd
                       if r.get("notification_date")]
        canonical_notif = min(notif_dates) if notif_dates else None

        canonical = dict(earliest)  # base on earliest filing
        # Override amount fields with latest filer-corrected values
        canonical["amount_min"] = latest.get("amount_min")
        canonical["amount_max"] = latest.get("amount_max")
        canonical["amount_range_text"] = latest.get("amount_range_text")
        canonical["asset_ticker"] = latest.get("asset_ticker")
        canonical["notification_date"] = canonical_notif
        canonical["earliest_doc_id"] = earliest["doc_id"]
        canonical["earliest_filing_date"] = earliest["_filing_date"].isoformat()
        canonical["n_filings"] = len(rows_with_fd)
        canonical["all_doc_ids"] = sorted({r["doc_id"] for r in rows_with_fd})
        canonical["is_amended"] = len(rows_with_fd) > 1
        out.append(canonical)
    return out


def assign_audit_flag(tx: dict[str, Any], served_from: _dt.date,
                      doc_modern_lt3yr: dict[str, int],
                      doc_modern_ge3yr: dict[str, int]) -> str:
    """Per .claude/rules/stock-act-audit.md §Exclusion flags + tightened
    parse_error_suspect heuristic.
    """
    tx_date = _parse_iso(tx.get("transaction_date"))
    filing_date = _parse_iso(tx.get("earliest_filing_date"))
    if tx_date is None:
        return "no_tx_date"
    if filing_date is not None and tx_date > filing_date:
        return "tx_after_filing"
    if tx_date < STOCK_ACT_EFFECTIVE:
        return "pre_stock_act"
    if tx_date < served_from - _dt.timedelta(days=PRE_TENURE_GRACE_DAYS):
        return "pre_tenure"
    # Tightened parse_error_suspect: year_gap >= 3 AND host_doc has other tx
    # within (filing_year - 3, filing_year]. Pure pre-modern batches do NOT
    # qualify.
    if filing_date is not None:
        year_gap = filing_date.year - tx_date.year
        doc_id = tx["earliest_doc_id"]
        if (year_gap >= PARSE_ERROR_YEAR_GAP
                and doc_modern_lt3yr.get(doc_id, 0) > 0
                and 0 < doc_modern_ge3yr.get(doc_id, 0) < PARSE_ERROR_MAX_OLD_TX):
            return "parse_error_suspect"
    return "auditable"


def compute_days_late(tx: dict[str, Any]) -> int:
    """LEAST(notif + 30d, tx + 45d) deadline; days_late = filing - deadline."""
    tx_date = _parse_iso(tx.get("transaction_date"))
    filing_date = _parse_iso(tx.get("earliest_filing_date"))
    notif_date = _parse_iso(tx.get("notification_date"))
    if tx_date is None or filing_date is None:
        return 0
    deadline_tx = tx_date + _dt.timedelta(days=TX_DEADLINE_DAYS)
    if notif_date is not None:
        deadline_notif = notif_date + _dt.timedelta(days=NOTIF_DEADLINE_DAYS)
        deadline = min(deadline_tx, deadline_notif)
    else:
        deadline = deadline_tx
    return max(0, (filing_date - deadline).days)


def compute_audit(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Run the full audit pipeline against the snapshot's bundled raw rows."""
    filing_index = {r["doc_id"]: _dt.date.fromisoformat(r["filing_date"])
                    for r in snapshot["filing_index"]}
    transactions = snapshot["transactions"]

    # Stage 1: canonical-view dedup
    canonical = canonical_dedup(transactions, filing_index)

    # Stage 2: per-doc modern/old tx counts for parse_error_suspect heuristic
    # (calculated on canonical rows — tightened-rule says "host doc")
    doc_modern_lt3yr: dict[str, int] = {}
    doc_modern_ge3yr: dict[str, int] = {}
    for tx in canonical:
        tx_date = _parse_iso(tx.get("transaction_date"))
        filing_date = _parse_iso(tx.get("earliest_filing_date"))
        if tx_date is None or filing_date is None:
            continue
        gap = filing_date.year - tx_date.year
        doc_id = tx["earliest_doc_id"]
        if gap >= PARSE_ERROR_YEAR_GAP:
            doc_modern_ge3yr[doc_id] = doc_modern_ge3yr.get(doc_id, 0) + 1
        else:
            doc_modern_lt3yr[doc_id] = doc_modern_lt3yr.get(doc_id, 0) + 1

    # Stage 3: assign audit_flag + compute days_late
    served_from = _dt.date.fromisoformat(
        snapshot.get("served_from_iso", KHANNA_SERVED_FROM.isoformat()))
    auditable = []
    flag_counts: dict[str, int] = {}
    for tx in canonical:
        flag = assign_audit_flag(tx, served_from, doc_modern_lt3yr,
                                 doc_modern_ge3yr)
        tx["audit_flag"] = flag
        tx["days_late"] = compute_days_late(tx) if flag == "auditable" else 0
        flag_counts[flag] = flag_counts.get(flag, 0) + 1
        if flag == "auditable":
            auditable.append(tx)

    # Stage 4: aggregate
    n_tx_total = len(auditable)
    late = [t for t in auditable if t["days_late"] > 0]
    n_tx_late = len(late)
    days_late_when_late = sorted(t["days_late"] for t in late)

    docs_with_late = {t["earliest_doc_id"] for t in late}

    n_docs_total = len({t["earliest_doc_id"] for t in auditable})
    n_docs_with_late = len(docs_with_late)
    pct_late = round((n_tx_late / n_tx_total) * 100, 2) if n_tx_total else 0.0
    worst_days_late = max((t["days_late"] for t in auditable), default=0)
    n_over_90 = sum(1 for d in days_late_when_late if d > 90)
    n_over_180 = sum(1 for d in days_late_when_late if d > 180)
    n_over_365 = sum(1 for d in days_late_when_late if d > 365)
    median_late = (statistics.median(days_late_when_late)
                   if days_late_when_late else 0)

    # Worst single tx (the HUMANA anchor)
    worst_tx = max(auditable, key=lambda t: t["days_late"]) if auditable else None
    worst_tx_summary = None
    if worst_tx is not None and worst_tx["days_late"] > 0:
        worst_tx_summary = {
            "asset_name": worst_tx.get("asset_name"),
            "owner": worst_tx.get("owner"),
            "transaction_date": worst_tx.get("transaction_date"),
            "filing_date": worst_tx.get("earliest_filing_date"),
            "days_late": worst_tx["days_late"],
            "transaction_type": worst_tx.get("transaction_type"),
            "amount_range": worst_tx.get("amount_range_text"),
        }

    return {
        "rebuild_run_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "snapshot_input": snapshot.get("snapshot_target"),
        "snapshot_date": snapshot.get("snapshot_date"),
        "served_from_iso": served_from.isoformat(),
        "n_transactions_raw_input": len(transactions),
        "n_canonical_post_dedup": len(canonical),
        "audit_flag_distribution": flag_counts,
        "khanna_aggregate": {
            "member_last_name": "Khanna",
            "member_first_name": "Rohit",
            "sample_state_district": "CA17",
            "n_tx_total": n_tx_total,
            "n_tx_late": n_tx_late,
            "n_docs_total": n_docs_total,
            "n_docs_with_late": n_docs_with_late,
            "pct_late": pct_late,
            "worst_days_late": worst_days_late,
            "n_tx_over_90d_late": n_over_90,
            "n_tx_over_180d_late": n_over_180,
            "n_tx_over_1yr_late": n_over_365,
            "median_days_late_when_late": float(median_late),
        },
        "worst_late_humana": worst_tx_summary,
    }


def diff_against_expected(rebuilt: dict[str, Any]) -> list[tuple[str, Any, Any, str]]:
    """Compare REBUILT aggregates to snapshot's expected_aggregates.

    Returns list of (field, expected, actual, status). status ∈
    {OK, DRIFT_VALUE}.
    """
    diffs = []
    actual = rebuilt["khanna_aggregate"]
    for field, exp_value in EXPECTED_AGGREGATES.items():
        act_value = actual.get(field)
        # Numeric tolerance — bit-exact for ints, 0.01 for percent
        if isinstance(exp_value, float):
            ok = abs((act_value or 0) - exp_value) < 0.01
        else:
            ok = act_value == exp_value
        diffs.append((field, exp_value, act_value, "OK" if ok else "DRIFT_VALUE"))
    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    here = pathlib.Path(__file__).resolve().parent
    pkg_root = here.parent.parent  # OCC_FILING_PACKAGE_V2/
    parser.add_argument("--snapshot",
                        default=str(pkg_root / "data" / "occ"
                                    / "khanna_ptr_transactions_2026_05_02.json"),
                        help="path to bundled raw-substrate snapshot JSON")
    parser.add_argument("--output",
                        default=str(here / "ptr_filing_audit_khanna_REBUILT.json"),
                        help="path to write REBUILT audit JSON")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress per-field diff lines")
    args = parser.parse_args()

    snap_path = pathlib.Path(args.snapshot)
    out_path = pathlib.Path(args.output)
    if not snap_path.exists():
        print(f"ERROR: snapshot not found at {snap_path}", file=sys.stderr)
        return 2

    print(f"Loading snapshot {snap_path} ...", file=sys.stderr)
    snapshot = load_snapshot(snap_path)
    print(f"  {snapshot['n_transactions_raw']:,} raw tx + "
          f"{snapshot['n_filings']} filings", file=sys.stderr)

    rebuilt = compute_audit(snapshot)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes((json.dumps(rebuilt, indent=2, default=str)
                          + "\n").encode("utf-8"))

    print(f"\nREBUILT audit -> {out_path}")
    print(f"  audit_flag distribution: {rebuilt['audit_flag_distribution']}")
    print(f"  n_canonical_post_dedup : {rebuilt['n_canonical_post_dedup']:,}")

    diffs = diff_against_expected(rebuilt)
    n_ok = sum(1 for d in diffs if d[3] == "OK")
    n_drift = sum(1 for d in diffs if d[3] == "DRIFT_VALUE")
    if not args.quiet:
        print(f"\nField-by-field diff vs bundled snapshot's expected_aggregates:")
        print(f"  {'field':30s}  {'expected':>12s}  {'actual':>12s}  status")
        for field, exp, act, status in diffs:
            print(f"  {field:30s}  {str(exp):>12s}  {str(act):>12s}  {status}")
    print(f"\nSUMMARY: {n_ok}/{len(diffs)} fields match expected ({n_drift} drift)")

    if rebuilt["worst_late_humana"]:
        print(f"\nWorst-late single tx (rebuilt):")
        for k, v in rebuilt["worst_late_humana"].items():
            print(f"  {k}: {v}")

    return 0 if n_drift == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
