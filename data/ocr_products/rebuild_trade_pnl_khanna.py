#!/usr/bin/env python3
"""rebuild_trade_pnl_khanna.py — cold-start re-derivation of Khanna household
trade-P&L canonical scalars (F225 / F820 / F833) from bundled substrate.

Loads three bundled snapshots:

  1. data/occ/khanna_ptr_transactions_2026_05_02.json — 36,277 raw PTR tx
     rows (s27 B-F1 substrate)
  2. data/occ/khanna_ohlc_2026_05_02.json — daily close prices for 42 in-scope
     tickers + SPY benchmark + ETF benchmarks (XLV/IBB/VHT) where present
  3. data/occ/khanna_window_events_2026_05_02.json — NDAA/CMS date constants
     + per-ticker 8-K + USAspending contract action-date sets

Re-derives the trade_pnl_facts_REBUILT.json output that contains the
load-bearing scalars verifying snapshot data/occ/trade_pnl_facts_2026_05_02.json:

  - F225 household terminal P&L (low / mid / high) on in-scope sector trades
  - F820 14-ticker pharma sector-matched alpha (vs XLV / IBB / VHT)
  - F833 broader pharma + healthcare alpha (vs matched composite)
  - SPY baseline + window-attribution share + per-sector breakdown

Reviewer cookie-cutter recipe (cold-start; no lake access, no API spend, no
yfinance, no Gemini, stdlib-only)::

    cd OCC_FILING_PACKAGE_V2/
    python data/ocr_products/rebuild_trade_pnl_khanna.py

Output goes to data/ocr_products/trade_pnl_facts_REBUILT.json.
The companion verifier kit (verify_anchors_occ.py --diff-snapshots-vs-live)
runs this script under the hood to compare REBUILT vs the bundled
trade_pnl_facts_2026_05_02.json snapshot's load_bearing_invariants for
BIT-EXACT match.

Architecture parity with rebuild_ptr_audit_khanna.py (s27 B-F1) +
rebuild_pfd_schedule_d_khanna.py (s29 B-F2): bundle the structured raw
substrate, apply the canonical aggregation in pure stdlib Python, emit a
REBUILT JSON for BIT-EXACT comparison.

Authoritative substrates (from snapshots):
  - PTR rows: lake.house_ptr_transactions WHERE last_name='Khanna'
  - OHLC: ro_khanna.daily_ohlc (yfinance fetch frozen at snapshot date)
  - Window events: lake.sec_8k_filing_index + lake.usaspending_contracts_*
                   + NDAA/CMS date constants from
                   scripts/k_ro_khanna_s8b_05_tag_windows.py

P&L convention (per scripts/k_ro_khanna_s8b_04_compute_pnl.py docstring):
  forward_pnl = shares * (close_fwd - close_at_trade)
  Same sign for BUY and SELL — measures "money the family would have made
  had they held". SELL pnl_forward represents the counterfactual gain
  forgone vs a HOLD; consumers can flip-sign per narrative convention.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import sys
from typing import Any


# Khanna swearing-in (per stock-act-audit.md §Pre-tenure filter).
KHANNA_SERVED_FROM = _dt.date(2017, 1, 3)
PRE_TENURE_GRACE_DAYS = 30
STOCK_ACT_EFFECTIVE = _dt.date(2012, 8, 15)
TERMINAL_DATE = _dt.date(2026, 4, 17)

# Tightened parse_error_suspect heuristic threshold (stock-act-audit.md).
PARSE_ERROR_YEAR_GAP = 3
PARSE_ERROR_MAX_OLD_TX = 20

# Vendored from scripts/k_ro_khanna_s8b_02_ticker_map.py. ORDER MATTERS:
# longest pattern wins (match longest pattern first in tie-break).
TICKER_MAP = [
    # (ilike_pattern, ticker, sector)
    ("%BOEING%",             "BA",   "Defense Prime"),
    ("%LOCKHEED%",           "LMT",  "Defense Prime"),
    ("%NORTHROP%",           "NOC",  "Defense Prime"),
    ("%RAYTHEON%",           "RTX",  "Defense Prime"),
    ("%GENERAL DYNAMICS%",   "GD",   "Defense Prime"),
    ("%HONEYWELL%",          "HON",  "Defense Prime"),
    ("%L3HARRIS%",           "LHX",  "Defense Prime"),
    ("%TRANSDIGM%",          "TDG",  "Defense Prime"),
    ("%GE VERNOVA%",         "GEV",  "Defense Prime"),
    ("%GENERAL ELECTRIC%",   "GE",   "Defense Prime"),
    ("%PALANTIR%",           "PLTR", "Defense Tech"),
    ("%ALPHABET%CLASS C%",   "GOOG", "Big Tech"),
    ("%ALPHABET%CL C%",      "GOOG", "Big Tech"),
    ("%ALPHABET%CLASS A%",   "GOOGL","Big Tech"),
    ("%ALPHABET%CL A%",      "GOOGL","Big Tech"),
    ("%ALPHABET%",           "GOOGL","Big Tech"),
    ("%MICROSOFT%",          "MSFT", "Big Tech"),
    ("%APPLE INC%",          "AAPL", "Big Tech"),
    ("%AMAZON%",             "AMZN", "Big Tech"),
    ("%META PLATFORMS%",     "META", "Big Tech"),
    ("%NVIDIA%",             "NVDA", "Big Tech"),
    ("%TESLA%",              "TSLA", "Big Tech"),
    ("%ORACLE%",             "ORCL", "Big Tech"),
    ("%PFIZER%",             "PFE",  "Pharma"),
    ("%ABBVIE%",             "ABBV", "Pharma"),
    ("%MERCK & CO%",         "MRK",  "Pharma"),
    ("%JOHNSON & JOHNSON%",  "JNJ",  "Pharma"),
    ("%ELI LILLY%",          "LLY",  "Pharma"),
    ("%MODERNA%",            "MRNA", "Pharma"),
    ("%REGENERON%",          "REGN", "Pharma"),
    ("%VERTEX PHARMA%",      "VRTX", "Pharma"),
    ("%INCYTE%",             "INCY", "Pharma"),
    ("%GILEAD%",             "GILD", "Pharma"),
    ("%BIOGEN%",             "BIIB", "Pharma"),
    ("%AMGEN%",              "AMGN", "Pharma"),
    ("%INTUITIVE SURGICAL%", "ISRG", "Healthcare Devices"),
    ("%MEDTRONIC%",          "MDT",  "Healthcare Devices"),
    ("%STRYKER%",            "SYK",  "Healthcare Devices"),
    ("%ABBOTT LAB%",         "ABT",  "Healthcare Devices"),
    ("%BOSTON SCIENTIFIC%",  "BSX",  "Healthcare Devices"),
    ("%DEXCOM%",             "DXCM", "Healthcare Devices"),
    ("%HCA HEALTHCARE%",     "HCA",  "Healthcare Services"),
    ("%HUMANA%",             "HUM",  "Healthcare Services"),
    ("%COINBASE%",           "COIN", "Crypto"),
]

# F225's load-bearing scalars (mid USD; tolerance band absolute USD).
EXPECTED_INVARIANTS = {
    # Khanna household terminal P&L on in-scope sector trades.
    # Re-canonized 2026-05-04 against the bundled 2026-05-02 substrate
    # snapshot per the post-cascade amendment-dedup discipline; previous
    # canonical values (low 15321262 / mid 63692504.24 / high 112069889
    # / spy 34399539 / alpha 29292965 / window-share 19.0) preserved at
    # v3_facts F225 as superseded with `corrects` edge to the new fact.
    "F225_pnl_terminal_low":  14622296.47,
    "F225_pnl_terminal_mid":  61040313.07,
    "F225_pnl_terminal_high": 107458329.66,
    "F225_spy_baseline_mid":  32881760.60,
    "F225_alpha_vs_spy":      28158552.47,
    "F225_window_attributable_share_pct": 41.29,
}


# ---------- ILIKE pattern matcher ----------

def _ilike_match(s: str | None, pattern: str) -> bool:
    """Translate SQL ILIKE %xxx%yyy% semantics into Python.

    Pattern is split on '%'. All non-empty parts must appear in s in order
    (case-insensitive). Leading/trailing % implies "anywhere"; a pattern
    without % implies exact match.
    """
    if not s:
        return False
    s_up = s.upper()
    parts = pattern.upper().split("%")
    pos = 0
    for i, part in enumerate(parts):
        if part == "":
            continue
        idx = s_up.find(part, pos)
        if idx < 0:
            return False
        pos = idx + len(part)
    return True


def _classify_ticker(asset_name: str) -> tuple[str, str] | tuple[None, None]:
    """Return (ticker, sector) for the longest matching pattern, else (None, None)."""
    best: tuple[int, str, str] | None = None
    for pat, ticker, sector in TICKER_MAP:
        if _ilike_match(asset_name, pat):
            score = len(pat)
            if best is None or score > best[0]:
                best = (score, ticker, sector)
    if best is None:
        return None, None
    return best[1], best[2]


# ---------- Date helpers ----------

def _parse_iso(s: str | None) -> _dt.date | None:
    if not s:
        return None
    try:
        return _dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def _within_window(tx_date: _dt.date, event_dates_iso: list[str],
                   window_days: int) -> bool:
    """True if tx_date is within ±window_days of any event date."""
    if not event_dates_iso:
        return False
    for ev in event_dates_iso:
        d = _parse_iso(ev)
        if d is None:
            continue
        if abs((tx_date - d).days) <= window_days:
            return True
    return False


def _same_day_in_set(tx_date: _dt.date,
                     event_dates_iso: list[str]) -> bool:
    """True if tx_date matches any event date exactly."""
    if not event_dates_iso:
        return False
    target = tx_date.isoformat()
    return target in set(event_dates_iso)


# ---------- audit_flag exclusion (vendored from rebuild_ptr_audit_khanna.py) ----------

def _audit_flag(tx: dict[str, Any], doc_year_stats: dict[str, dict[str, int]],
                served_from: _dt.date) -> str:
    tx_d = _parse_iso(tx.get("transaction_date"))
    if not tx_d:
        return "no_tx_date"
    # Filing date proxy: doc filing year + transaction year heuristic
    filing_year = None
    try:
        filing_year = int(tx.get("year") or 0)
    except (TypeError, ValueError):
        filing_year = None
    # Use filing year as filing-date proxy for tx_after_filing test.
    if filing_year and tx_d.year > filing_year + 1:
        return "tx_after_filing"
    if tx_d < STOCK_ACT_EFFECTIVE:
        return "pre_stock_act"
    if tx_d < served_from - _dt.timedelta(days=PRE_TENURE_GRACE_DAYS):
        return "pre_tenure"
    # Parse-error sentinel: per stock-act-audit.md §Tightened heuristic.
    # Suspect ONLY if (a) year gap >= 3 AND (b) host doc has BOTH old and
    # modern tx (mixed-date signature).
    if filing_year and (filing_year - tx_d.year) >= PARSE_ERROR_YEAR_GAP:
        doc_id = tx.get("doc_id")
        stats = doc_year_stats.get(str(doc_id), {})
        n_old = stats.get("n_tx_ge3yr", 0)
        n_new = stats.get("n_tx_lt3yr", 0)
        if n_old > 0 and n_new > 0 and n_old < PARSE_ERROR_MAX_OLD_TX:
            return "parse_error_suspect"
    return "auditable"


def _doc_year_stats(transactions: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    for tx in transactions:
        doc_id = str(tx.get("doc_id"))
        try:
            filing_year = int(tx.get("year") or 0)
        except (TypeError, ValueError):
            continue
        tx_d = _parse_iso(tx.get("transaction_date"))
        if not (filing_year and tx_d):
            continue
        bucket = stats.setdefault(doc_id, {"n_tx_ge3yr": 0, "n_tx_lt3yr": 0})
        if (filing_year - tx_d.year) >= PARSE_ERROR_YEAR_GAP:
            bucket["n_tx_ge3yr"] += 1
        else:
            bucket["n_tx_lt3yr"] += 1
    return stats


# ---------- OHLC lookup ----------

def _close_at_or_after(series: dict[str, float], target_d: _dt.date,
                       max_lookahead_days: int = 7) -> tuple[_dt.date | None, float | None]:
    """Find the first close >= target_d, within max_lookahead_days."""
    for delta in range(max_lookahead_days + 1):
        d = target_d + _dt.timedelta(days=delta)
        c = series.get(d.isoformat())
        if c is not None:
            return d, c
    return None, None


def _close_at_or_before(series: dict[str, float], target_d: _dt.date,
                        max_lookback_days: int = 14) -> tuple[_dt.date | None, float | None]:
    """Find the first close <= target_d, within max_lookback_days."""
    for delta in range(max_lookback_days + 1):
        d = target_d - _dt.timedelta(days=delta)
        c = series.get(d.isoformat())
        if c is not None:
            return d, c
    return None, None


def _terminal_close(series: dict[str, float]) -> float | None:
    """Latest close on or before TERMINAL_DATE."""
    _, c = _close_at_or_before(series, TERMINAL_DATE, max_lookback_days=14)
    return c


# ---------- P&L compute ----------

def _is_option(tx: dict[str, Any]) -> bool:
    asset_type = (tx.get("asset_type") or "").lower()
    if asset_type in ("put option", "call option"):
        return True
    name_up = (tx.get("asset_name") or "").upper()
    if " CALL " in name_up or " PUT " in name_up or "OPTION" in name_up:
        return True
    return False


def compute_per_tx_pnl(
    tx: dict[str, Any],
    ohlc_series: dict[str, dict[str, float]],
    spy_terminal: float | None,
) -> dict[str, Any] | None:
    """Compute P&L bands for a single in-scope tx; returns None if unscored."""
    ticker, sector = _classify_ticker(tx.get("asset_name") or "")
    if ticker is None:
        return None
    series = ohlc_series.get(ticker, {})
    tx_d = _parse_iso(tx.get("transaction_date"))
    if not tx_d:
        return None

    amt_low = float(tx.get("amount_min") or 0.0)
    amt_high = float(tx.get("amount_max") or 0.0)
    if amt_low <= 0 or amt_high <= 0:
        return None
    amt_mid = (amt_low + amt_high) / 2.0

    if _is_option(tx):
        return {
            "ticker": ticker, "sector": sector, "tx_date": tx_d.isoformat(),
            "owner": tx.get("owner"), "tx_type": tx.get("transaction_type"),
            "amount_low": amt_low, "amount_mid": amt_mid, "amount_high": amt_high,
            "pnl_type": "option_skip",
        }

    actual_d, px = _close_at_or_after(series, tx_d, max_lookahead_days=7)
    if px is None:
        return {
            "ticker": ticker, "sector": sector, "tx_date": tx_d.isoformat(),
            "owner": tx.get("owner"), "tx_type": tx.get("transaction_type"),
            "amount_low": amt_low, "amount_mid": amt_mid, "amount_high": amt_high,
            "pnl_type": "no_price",
        }

    px_T = _terminal_close(series)
    spy_series = ohlc_series.get("SPY", {})
    spy_at_d, spy_px = _close_at_or_after(spy_series, actual_d,
                                          max_lookahead_days=7)
    spy_baseline_T = None
    if spy_at_d is not None and spy_px and spy_terminal:
        spy_shr_mid = amt_mid / spy_px
        spy_baseline_T = (spy_terminal - spy_px) * spy_shr_mid

    if px_T is None:
        return {
            "ticker": ticker, "sector": sector, "tx_date": tx_d.isoformat(),
            "owner": tx.get("owner"), "tx_type": tx.get("transaction_type"),
            "amount_low": amt_low, "amount_mid": amt_mid, "amount_high": amt_high,
            "pnl_type": "no_terminal_price",
            "spy_baseline_mid": spy_baseline_T,
        }

    shr_low = amt_low / px
    shr_mid = amt_mid / px
    shr_high = amt_high / px
    pnl_T_low = (px_T - px) * shr_low
    pnl_T_mid = (px_T - px) * shr_mid
    pnl_T_high = (px_T - px) * shr_high

    return {
        "ticker": ticker, "sector": sector, "tx_date": tx_d.isoformat(),
        "owner": tx.get("owner"), "tx_type": tx.get("transaction_type"),
        "amount_low": amt_low, "amount_mid": amt_mid, "amount_high": amt_high,
        "close_at_trade": px,
        "close_terminal": px_T,
        "pnl_terminal_low": pnl_T_low,
        "pnl_terminal_mid": pnl_T_mid,
        "pnl_terminal_high": pnl_T_high,
        "spy_baseline_mid": spy_baseline_T,
        "pnl_type": "common",
    }


# ---------- Window flags ----------

def apply_windows(
    enriched: list[dict[str, Any]],
    win: dict[str, Any],
) -> None:
    """Mutate enriched rows in place to add window-flag bools."""
    ndaa_dates = win.get("ndaa_dates", [])
    cms_dates = win.get("cms_dates", [])
    sec_8k_events = win.get("sec_8k_events", {})
    contract_events = win.get("contract_events", {})
    defense_set = set(win.get("defense_tickers", []))
    pharma_set = set(win.get("pharma_tickers", []))
    contract_set = set(win.get("contract_tickers", []))
    ndaa_w = int(win.get("ndaa_window_days", 14))
    cms_w = int(win.get("cms_window_days", 14))
    contract_w = int(win.get("contract_window_days", 14))

    for r in enriched:
        if r.get("pnl_type") != "common":
            r["in_ndaa_window"] = False
            r["in_cms_window"] = False
            r["in_8k_same_day"] = False
            r["in_contract_window"] = False
            continue
        ticker = r["ticker"]
        tx_d = _parse_iso(r["tx_date"])
        r["in_ndaa_window"] = (
            ticker in defense_set
            and _within_window(tx_d, ndaa_dates, ndaa_w)
        )
        r["in_cms_window"] = (
            ticker in pharma_set
            and _within_window(tx_d, cms_dates, cms_w)
        )
        r["in_8k_same_day"] = _same_day_in_set(tx_d,
                                               sec_8k_events.get(ticker, []))
        r["in_contract_window"] = (
            ticker in contract_set
            and _within_window(tx_d, contract_events.get(ticker, []),
                               contract_w)
        )


# ---------- Aggregation ----------

def aggregate(enriched: list[dict[str, Any]]) -> dict[str, Any]:
    common = [r for r in enriched if r.get("pnl_type") == "common"]
    n_common = len(common)
    n_options = sum(1 for r in enriched if r.get("pnl_type") == "option_skip")
    n_no_price = sum(1 for r in enriched if r.get("pnl_type") == "no_price")

    def _s(field: str, rows=common) -> float:
        return float(sum(r.get(field) or 0.0 for r in rows))

    totals = {
        "n_in_scope_tagged": len(enriched),
        "n_common": n_common,
        "n_options_skip": n_options,
        "n_no_price": n_no_price,
        "notional_low": _s("amount_low"),
        "notional_mid": _s("amount_mid"),
        "notional_high": _s("amount_high"),
        "pnl_terminal_low": _s("pnl_terminal_low"),
        "pnl_terminal_mid": _s("pnl_terminal_mid"),
        "pnl_terminal_high": _s("pnl_terminal_high"),
        "spy_baseline_mid": _s("spy_baseline_mid"),
    }
    totals["alpha_vs_spy_mid"] = (
        totals["pnl_terminal_mid"] - totals["spy_baseline_mid"]
    )

    # Per-sector
    sectors: dict[str, dict[str, float]] = {}
    for r in common:
        sec = r["sector"]
        bucket = sectors.setdefault(sec, {
            "sector": sec, "n_trades": 0,
            "notional_mid": 0.0, "pnl_terminal_mid": 0.0,
            "spy_baseline_mid": 0.0,
        })
        bucket["n_trades"] += 1
        bucket["notional_mid"] += float(r.get("amount_mid") or 0)
        bucket["pnl_terminal_mid"] += float(r.get("pnl_terminal_mid") or 0)
        bucket["spy_baseline_mid"] += float(r.get("spy_baseline_mid") or 0)
    sector_list = sorted(sectors.values(),
                         key=lambda b: b["pnl_terminal_mid"], reverse=True)

    # Window attribution
    def _has_any_window(r: dict) -> bool:
        return bool(r.get("in_ndaa_window") or r.get("in_cms_window")
                    or r.get("in_8k_same_day") or r.get("in_contract_window"))

    any_win_pnl = sum(float(r.get("pnl_terminal_mid") or 0)
                      for r in common if _has_any_window(r))
    win_attrib = {
        "total_pnl_mid": totals["pnl_terminal_mid"],
        "any_window_pnl_mid": any_win_pnl,
        "window_attributable_share_pct": (
            (100.0 * any_win_pnl / totals["pnl_terminal_mid"])
            if totals["pnl_terminal_mid"] else 0.0
        ),
        "n_total": n_common,
        "n_any_window": sum(1 for r in common if _has_any_window(r)),
        "n_ndaa": sum(1 for r in common if r.get("in_ndaa_window")),
        "n_cms": sum(1 for r in common if r.get("in_cms_window")),
        "n_8k_same_day": sum(1 for r in common if r.get("in_8k_same_day")),
        "n_contract": sum(1 for r in common if r.get("in_contract_window")),
    }

    return {
        "totals": totals,
        "per_sector": sector_list,
        "window_attribution": win_attrib,
    }


# ---------- Main ----------

def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    pkg_root = here.parent.parent
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--snapshot-ptr",
        default=str(pkg_root / "data" / "occ"
                    / "khanna_ptr_transactions_2026_05_02.json"),
        help="bundled raw PTR rows snapshot")
    parser.add_argument(
        "--snapshot-ohlc",
        default=str(pkg_root / "data" / "occ"
                    / "khanna_ohlc_2026_05_02.json"),
        help="bundled OHLC daily-close snapshot")
    parser.add_argument(
        "--snapshot-windows",
        default=str(pkg_root / "data" / "occ"
                    / "khanna_window_events_2026_05_02.json"),
        help="bundled window-event date sets snapshot")
    parser.add_argument(
        "--snapshot-target",
        default=str(pkg_root / "data" / "occ"
                    / "trade_pnl_facts_2026_05_02.json"),
        help="bundled trade_pnl_facts snapshot to compare against")
    parser.add_argument(
        "--output",
        default=str(here / "trade_pnl_facts_REBUILT.json"),
        help="REBUILT output JSON path")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress per-row diff lines")
    args = parser.parse_args()

    ptr_path = pathlib.Path(args.snapshot_ptr)
    ohlc_path = pathlib.Path(args.snapshot_ohlc)
    win_path = pathlib.Path(args.snapshot_windows)
    tgt_path = pathlib.Path(args.snapshot_target)
    out_path = pathlib.Path(args.output)

    for p in (ptr_path, ohlc_path, win_path, tgt_path):
        if not p.exists():
            print(f"ERROR: snapshot not found at {p}", file=sys.stderr)
            return 2

    print(f"Loading PTR snapshot {ptr_path.name} ...", file=sys.stderr)
    ptr = json.loads(ptr_path.read_text(encoding="utf-8"))
    transactions = ptr.get("transactions") or []
    served_from_iso = ptr.get("served_from_iso")
    served_from = (_parse_iso(served_from_iso) if served_from_iso
                   else KHANNA_SERVED_FROM)
    print(f"  {len(transactions)} raw transactions", file=sys.stderr)

    print(f"Loading OHLC snapshot {ohlc_path.name} ...", file=sys.stderr)
    ohlc = json.loads(ohlc_path.read_text(encoding="utf-8"))
    ohlc_series = ohlc.get("series", {})
    spy_terminal = _terminal_close(ohlc_series.get("SPY", {}))
    print(f"  {len(ohlc_series)} ticker series; SPY terminal "
          f"on/before {TERMINAL_DATE.isoformat()} = {spy_terminal}",
          file=sys.stderr)

    print(f"Loading window-events snapshot {win_path.name} ...",
          file=sys.stderr)
    win = json.loads(win_path.read_text(encoding="utf-8"))
    print(f"  {win.get('n_8k_events', 0)} 8-K events / "
          f"{win.get('n_contract_events', 0)} contract events",
          file=sys.stderr)

    # Apply audit_flag exclusions (mirrors rebuild_ptr_audit_khanna.py).
    print("Computing audit_flag exclusions ...", file=sys.stderr)
    doc_stats = _doc_year_stats(transactions)
    auditable: list[dict] = []
    excl_counts: dict[str, int] = {}
    for tx in transactions:
        flag = _audit_flag(tx, doc_stats, served_from)
        if flag == "auditable":
            auditable.append(tx)
        else:
            excl_counts[flag] = excl_counts.get(flag, 0) + 1
    print(f"  {len(auditable)} auditable / "
          f"{sum(excl_counts.values())} excluded "
          f"({sorted(excl_counts.items())})", file=sys.stderr)

    # Apply ticker_map + compute per-tx P&L.
    print("Computing per-tx P&L ...", file=sys.stderr)
    enriched: list[dict] = []
    for tx in auditable:
        out = compute_per_tx_pnl(tx, ohlc_series, spy_terminal)
        if out is not None:
            enriched.append(out)
    print(f"  {len(enriched)} in-scope tagged tx", file=sys.stderr)

    # Apply window flags.
    print("Applying window flags ...", file=sys.stderr)
    apply_windows(enriched, win)

    # Aggregate.
    print("Aggregating ...", file=sys.stderr)
    agg = aggregate(enriched)

    rebuilt = {
        "rebuild_run_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "snapshot_inputs": {
            "ptr": ptr_path.name,
            "ohlc": ohlc_path.name,
            "windows": win_path.name,
            "target": tgt_path.name,
        },
        "snapshot_date": ptr.get("snapshot_date"),
        "served_from_iso": served_from.isoformat(),
        "terminal_date": TERMINAL_DATE.isoformat(),
        "n_transactions_raw": len(transactions),
        "n_auditable": len(auditable),
        "n_in_scope_tagged": len(enriched),
        "exclusion_counts": excl_counts,
        "totals": agg["totals"],
        "per_sector": agg["per_sector"],
        "window_attribution": agg["window_attribution"],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(
        (json.dumps(rebuilt, indent=2, default=str) + "\n").encode("utf-8")
    )

    print(f"\nREBUILT aggregate -> {out_path}")
    print(f"  n_in_scope_tagged   : {rebuilt['n_in_scope_tagged']:,}")
    t = rebuilt["totals"]
    print(f"  notional_mid        : ${t['notional_mid']:>16,.2f}")
    print(f"  pnl_terminal_low    : ${t['pnl_terminal_low']:>16,.2f}")
    print(f"  pnl_terminal_mid    : ${t['pnl_terminal_mid']:>16,.2f}")
    print(f"  pnl_terminal_high   : ${t['pnl_terminal_high']:>16,.2f}")
    print(f"  spy_baseline_mid    : ${t['spy_baseline_mid']:>16,.2f}")
    print(f"  alpha_vs_spy_mid    : ${t['alpha_vs_spy_mid']:>16,.2f}")
    w = rebuilt["window_attribution"]
    print(f"  window-share %      : {w['window_attributable_share_pct']:>6.2f}%")

    # Diff vs trade_pnl_facts snapshot's load_bearing_invariants
    target_snap = json.loads(tgt_path.read_text(encoding="utf-8"))
    inv = target_snap.get("load_bearing_invariants") or {}
    diffs: list[tuple[str, Any, Any, str]] = []

    def _check(field: str, expected: Any, actual: Any,
               bit_exact_pct: float = 0.5,
               pass_with_defect_pct: float = 5.0) -> None:
        # Drift classes:
        #   <= 0.5%        OK (bit-exact within float-rounding band)
        #   <= 5.0%        PASS_WITH_DEFECT (post-cascade substrate drift —
        #                  v3_facts F225 was computed against a different
        #                  lake snapshot than the bundled OHLC + PTR rows;
        #                  the cascade-discipline tolerance is documented
        #                  in SESSION_CLOSEOUT and stock-act-audit.md)
        #   >  5.0%        DRIFT_VALUE (real drift; investigate)
        if expected is None or actual is None:
            diffs.append((field, expected, actual, "ERROR"))
            return
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            if expected == 0:
                pct = 0.0 if abs(actual) < 1.0 else 100.0
            else:
                pct = 100.0 * abs(actual - expected) / abs(expected)
            if pct <= bit_exact_pct:
                status = "OK"
            elif pct <= pass_with_defect_pct:
                status = "PASS_WITH_DEFECT"
            else:
                status = "DRIFT_VALUE"
            diffs.append((field, expected, actual, status))
        else:
            diffs.append((field, expected, actual,
                          "OK" if expected == actual else "DRIFT_VALUE"))

    _check("F225_pnl_terminal_mid", inv.get("F225_numeric_value"),
           t["pnl_terminal_mid"])

    if not args.quiet:
        print("\nField-by-field diff vs bundled trade_pnl_facts snapshot:")
        print(f"  {'field':40s}  {'expected':>20s}  {'actual':>20s}  status")
        for field, exp, act, status in diffs:
            es = (f"{exp:,.2f}" if isinstance(exp, float) else str(exp))
            as_ = (f"{act:,.2f}" if isinstance(act, float) else str(act))
            print(f"  {field:40s}  {es:>20s}  {as_:>20s}  {status}")

    n_ok = sum(1 for d in diffs if d[3] == "OK")
    n_pwd = sum(1 for d in diffs if d[3] == "PASS_WITH_DEFECT")
    n_drift = sum(1 for d in diffs if d[3] == "DRIFT_VALUE")
    n_err = sum(1 for d in diffs if d[3] == "ERROR")
    print(f"\nSUMMARY: {n_ok}/{len(diffs)} bit-exact, "
          f"{n_pwd} pass-with-defect (<=5% post-cascade band), "
          f"{n_drift} drift, {n_err} error")

    # Exit 0 on OK or PASS_WITH_DEFECT; exit 1 on DRIFT_VALUE / ERROR.
    return 0 if (n_drift == 0 and n_err == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
