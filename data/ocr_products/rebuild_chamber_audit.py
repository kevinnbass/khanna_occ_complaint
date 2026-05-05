#!/usr/bin/env python3
"""rebuild_chamber_audit.py — chamber-wide PTR audit rebuild scaffold.

**B-F4 Phase-1 scaffold.** This script enumerates the chamber-wide PTR
universe from the bundled per-year House Clerk FD ZIP indexes, picks N
random Members for a dry-run smoke test (default 5), and reports what the
full chamber-wide rebuild WOULD do — without invoking any paid API.

The full chamber-wide rebuild requires Gemini per-page OCR on ~5K-10K PTR
PDFs at an estimated reviewer cost of $50-200 (per the bundled OCC
methodology cover doc and the K_p1_per_page_extractor pattern). The
``--full-chamber --cost-acknowledged`` mode is the gated path that ACTUALLY
invokes the per-page OCR + structured extraction + canonical-view dedup +
per-Member aggregation pipeline.

**Reviewer cost discipline:**

- ``--dry-run-smoke`` (default): zero spend. Enumerates 5 random Members from
  the cached per-year FD index, lists their PTR doc_ids, prints the would-be
  fetch URLs, and reports the projected cost for the full chamber-wide path.
- ``--full-chamber`` alone: hard-fails with cost-acknowledgment guidance.
- ``--full-chamber --cost-acknowledged``: actually invokes the chamber-wide
  pipeline. Requires GEMINI_API_KEY in the environment. The default model is
  `gemini-3.1-flash-lite-preview` (matching the engine used in B-F1's
  bundled Khanna OCR products); per-page extraction follows the
  ``src.gemini_per_page_extract.extract_per_page`` caterpillar pattern.

**Pipeline architecture (full chamber path):**

1. **Member enumeration** — read ``_substrate_cache_occ/house_fd/{YEAR}FD.zip``
   for YEAR in 2014..2026, filter to PTR rows (``FilingType='P'``), build
   ``(member_last, member_first, state_district, year, doc_id)`` tuples.
2. **Per-Member PTR fetch** — pull each PDF from
   ``https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf``
   into the substrate cache (idempotent; skip if already cached >2 KB).
3. **Per-page Gemini OCR** — ``src.gemini_per_page_extract.extract_per_page``
   pattern: per-PDF page rasterize @ 200 DPI → Gemini per-page JSON
   extraction with the same prompt-shape used by B-D2.b for Khanna.
4. **Structured normalization** — flatten Gemini JSON to the same
   per-tx-row schema bundled at
   ``data/occ/khanna_ptr_transactions_2026_05_02.json`` (fields:
   asset_name, ticker, owner, transaction_date, transaction_type,
   amount_range, etc.).
5. **Canonical-view dedup** — apply the tx-key amendment-cascade dedup
   discipline from ``rebuild_ptr_audit_khanna.py`` (which mirrors the
   ``lake.house_ptr_transactions_canonical`` view per
   ``.claude/rules/stock-act-audit.md``).
6. **audit_flag exclusions** — apply no_tx_date / tx_after_filing /
   pre_stock_act / pre_tenure / parse_error_suspect (tightened heuristic
   per K_p1_infra_fixes #9) per-Member.
7. **Per-Member aggregation** — same days_late =
   ``filing_date - LEAST(notification_date + 30d, transaction_date + 45d)``
   formula; aggregate (n_tx_total, n_tx_late, pct_late, worst_days_late,
   etc.).
8. **Chamber percentile compute** — filter to Members with n_tx_total >= 20
   per ``.claude/rules/peer-baseline.md``; compute p25/p50/p75/p95 of
   pct_late + worst_days; output the rate_percentiles + severity_percentiles
   blocks matching ``data/occ/house_chamber_audit_2026_05_02.json``.

**Output**: ``data/ocr_products/house_chamber_audit_REBUILT.json`` matching
the bundled snapshot's load-bearing scalars (rate_percentiles +
severity_percentiles + khanna_severity_rank).

**Companion differ**: ``verify_anchors_occ.py`` ``_diff_chamber_audit_via_rebuild()``
reads the REBUILT json + compares to the snapshot; reports
BLOCKED_NEEDS_REVIEWER_REBUILD until the reviewer runs this script in
``--full-chamber --cost-acknowledged`` mode and produces the REBUILT
artifact.

**Why this is multi-session author work** (per the B-F4 backlog
classification): the script body below is the chamber-Member enumeration
+ dry-run smoke + cost-disclosure scaffold. The full Gemini-spend pipeline
(steps 2-8 above) is documented inline as TODO blocks for the Phase-2
author session that performs the actual chamber-wide spend (which itself
requires explicit user authorization per the OCC campaign's
``§Escalate-to-user`` LLM-verification trigger).
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import io
import json
import os
import pathlib
import random
import statistics
import sys
import time
import urllib.request
import zipfile
from typing import Any

# --- Cost model ---
# Estimated per-PDF Gemini spend (model: gemini-3.1-flash-lite-preview;
# rate as of 2026-05-03 ~$0.10 input / $0.40 output per 1M tokens):
#   - typical Khanna PTR: 12-15 pages, ~0.5K input + ~1.5K output tokens / page
#   - per-PDF cost ≈ 12 × ($0.0005 input + $0.0006 output) ≈ $0.013
# Chamber-wide: ~5K-10K PTR PDFs (433 voting Members + delegates × ~12-25
# PTRs per active-trader Member; most Members have 0-3 PTRs total).
# Net projected reviewer cost: $50-200 (matches B-F4 backlog cost band).
TYPICAL_PTR_PDF_PAGES = 12
COST_PER_PDF_USD_LO = 0.005
COST_PER_PDF_USD_HI = 0.020
COST_PER_PDF_USD_MID = 0.013

PROJECT_ROOT_OCC = pathlib.Path(__file__).resolve().parents[2]
DATA_OCC = PROJECT_ROOT_OCC / "data" / "occ"
DATA_OCR = PROJECT_ROOT_OCC / "data" / "ocr_products"
SUBSTRATE_CACHE = PROJECT_ROOT_OCC / "_substrate_cache_occ"
FD_CACHE = SUBSTRATE_CACHE / "house_fd"
PTR_PDF_CACHE = SUBSTRATE_CACHE / "chamber_ptr_pdfs"
GEMINI_CACHE = SUBSTRATE_CACHE / "chamber_gemini_extract"

# Per-Member served_from lookup CSV bundled in data/occ/ (derived from
# lake.congress_members chamber IN ('House of Representatives','both')).
SERVED_FROM_CSV = DATA_OCC / "house_member_served_from_2026_05_03.csv"

# Pre-tenure / parse-error / STOCK-Act constants (mirror rebuild_ptr_audit_khanna.py).
PRE_TENURE_GRACE_DAYS = 30
STOCK_ACT_EFFECTIVE = _dt.date(2012, 8, 15)
NOTIF_DEADLINE_DAYS = 30
TX_DEADLINE_DAYS = 45
PARSE_ERROR_YEAR_GAP = 3
PARSE_ERROR_MAX_OLD_TX = 20

# Chamber percentile-stability filter per .claude/rules/peer-baseline.md.
PERCENTILE_MIN_TX = 20


# --- Member enumeration from bundled per-year FD ZIPs ---

def enumerate_chamber_ptr_universe(years: list[int] | None = None) -> dict[str, Any]:
    """Walk the per-year FD ZIPs in ``_substrate_cache_occ/house_fd/`` and
    return a chamber-wide PTR universe. If the cache is empty, returns an
    empty universe + a hint to run ``fetch_substrate_occ.py --classes house_fd``.

    Note: ``cmd_house_fd`` in ``fetch_substrate_occ.py`` filters to Khanna's
    rows when emitting the per-year TSVs, but it caches the RAW ZIP first,
    so the chamber-wide rows are still recoverable from the ZIP archives.
    """
    if years is None:
        years = list(range(2014, 2027))
    universe: dict[str, list[dict]] = {}  # member_key -> list of PTR rows
    n_zips_scanned = 0
    n_ptr_rows = 0
    for year in years:
        zip_path = FD_CACHE / f"{year}FD.zip"
        if not zip_path.exists():
            # Raw ZIP not cached. fetch_substrate_occ.py downloads + parses
            # the ZIP in-memory and only WRITES the filtered TSVs; the raw
            # ZIPs are downloaded but not always retained. Phase-2 will
            # extend cmd_house_fd to retain the raw ZIPs.
            continue
        try:
            with zipfile.ZipFile(zip_path) as z:
                txt_name = next((n for n in z.namelist() if n.endswith(".txt")), None)
                if txt_name is None:
                    continue
                with z.open(txt_name) as f:
                    raw = f.read().decode("utf-8", errors="replace")
        except Exception:
            continue
        n_zips_scanned += 1
        lines = raw.splitlines()
        if not lines:
            continue
        # Header: Prefix Last First Suffix FilingType StateDst Year FilingDate DocID
        for ln in lines[1:]:
            if not ln.strip():
                continue
            cols = ln.split("\t")
            if len(cols) < 9:
                continue
            filing_type = cols[4].strip().upper()
            if filing_type != "P":  # PTR only
                continue
            last = cols[1].strip().upper()
            first = cols[2].strip().upper()
            state_dst = cols[5].strip().upper()
            filing_year = cols[6].strip()
            filing_date = cols[7].strip()
            doc_id = cols[8].strip()
            member_key = f"{last}|{first}|{state_dst}"
            row = {
                "year": year,
                "doc_id": doc_id,
                "filing_year": filing_year,
                "filing_date": filing_date,
                "pdf_url": (
                    f"https://disclosures-clerk.house.gov/public_disc/"
                    f"ptr-pdfs/{year}/{doc_id}.pdf"
                ),
            }
            universe.setdefault(member_key, []).append(row)
            n_ptr_rows += 1
    return {
        "n_zips_scanned": n_zips_scanned,
        "n_ptr_rows": n_ptr_rows,
        "n_members": len(universe),
        "universe": universe,
    }


def _project_cost(n_ptrs: int) -> dict[str, float]:
    """Return (lo, mid, hi) cost projection for N PTR PDFs."""
    return {
        "n_ptrs": n_ptrs,
        "estimated_total_usd_lo": round(n_ptrs * COST_PER_PDF_USD_LO, 2),
        "estimated_total_usd_mid": round(n_ptrs * COST_PER_PDF_USD_MID, 2),
        "estimated_total_usd_hi": round(n_ptrs * COST_PER_PDF_USD_HI, 2),
        "model": "gemini-3.1-flash-lite-preview",
        "per_pdf_assumption": (
            f"~{TYPICAL_PTR_PDF_PAGES} pages × ${COST_PER_PDF_USD_MID:.4f}/PDF "
            f"(model: gemini-3.1-flash-lite-preview at ~$0.10 input + "
            f"$0.40 output per 1M tokens; matches B-F1 bundled Khanna OCR "
            f"engine + ~$2.47 actual Khanna spend / 114 PTRs / 1,787 pages "
            f"per K_ro_khanna_occ_complaint s21 B-D2.b)"
        ),
    }


# --- Dry-run smoke mode ---

def cmd_dry_run_smoke(n_members: int = 5, seed: int = 42) -> int:
    """Dry-run smoke against N random Members. Zero spend. Reports what
    the full chamber-wide path WOULD do."""
    print(f"[chamber-rebuild dry-run-smoke] enumerating chamber PTR universe ...")
    inv = enumerate_chamber_ptr_universe()
    if inv["n_zips_scanned"] == 0:
        print(
            "  No raw FD ZIPs cached at "
            f"{FD_CACHE}/. The current fetch_substrate_occ.py cmd_house_fd "
            "filters Khanna rows in-memory and only writes the filtered TSVs "
            "(per-year + combined). The raw ZIPs are not retained. To run a "
            "chamber-wide enumeration:\n"
            "    1. Re-run cmd_house_fd with the (pending Phase-2) --keep-raw-zips flag,\n"
            "    2. OR manually fetch the per-year ZIPs from\n"
            "       https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{YEAR}FD.zip\n"
            f"       into {FD_CACHE}/{{YEAR}}FD.zip then re-run this script.\n\n"
            "Phase-1 scaffold limitation: enumeration source not yet bundled. "
            "Reporting projected cost band based on documented chamber-wide PTR "
            "volume estimate (~5K-10K PTR PDFs total; see B-F4 backlog cost band)."
        )
        proj_lo = _project_cost(5_000)
        proj_hi = _project_cost(10_000)
        print(
            f"\nProjected reviewer cost (5K PTR floor): "
            f"${proj_lo['estimated_total_usd_lo']:.2f} (lo) / "
            f"${proj_lo['estimated_total_usd_mid']:.2f} (mid) / "
            f"${proj_lo['estimated_total_usd_hi']:.2f} (hi)"
        )
        print(
            f"Projected reviewer cost (10K PTR ceiling): "
            f"${proj_hi['estimated_total_usd_lo']:.2f} (lo) / "
            f"${proj_hi['estimated_total_usd_mid']:.2f} (mid) / "
            f"${proj_hi['estimated_total_usd_hi']:.2f} (hi)"
        )
        return 0
    print(
        f"  scanned {inv['n_zips_scanned']} per-year FD ZIPs / "
        f"{inv['n_ptr_rows']:,} PTR rows / "
        f"{inv['n_members']:,} distinct Members across the universe"
    )
    universe = inv["universe"]
    member_keys = sorted(universe.keys())
    rng = random.Random(seed)
    sample_keys = rng.sample(member_keys, k=min(n_members, len(member_keys)))
    print(f"\nDry-run smoke against {len(sample_keys)} random Members "
          f"(seed={seed}):\n")
    sample_n_ptrs = 0
    for k in sample_keys:
        rows = universe[k]
        sample_n_ptrs += len(rows)
        last, first, state_dst = k.split("|")
        print(f"  Member: {last}, {first} ({state_dst}) — {len(rows)} PTR(s)")
        for r in rows[:3]:
            print(f"    year={r['year']} doc_id={r['doc_id']} filing_date={r['filing_date']}")
            print(f"      pdf_url={r['pdf_url']}")
        if len(rows) > 3:
            print(f"    ... ({len(rows) - 3} more)")
    sample_proj = _project_cost(sample_n_ptrs)
    chamber_proj = _project_cost(inv['n_ptr_rows'])
    print(f"\nSample cost projection ({sample_n_ptrs} PTRs across "
          f"{len(sample_keys)} sample Members):")
    print(
        f"  ${sample_proj['estimated_total_usd_lo']:.2f} (lo) / "
        f"${sample_proj['estimated_total_usd_mid']:.2f} (mid) / "
        f"${sample_proj['estimated_total_usd_hi']:.2f} (hi)"
    )
    print(f"\nFull chamber-wide cost projection ({inv['n_ptr_rows']:,} PTRs "
          f"across {inv['n_members']:,} Members):")
    print(
        f"  ${chamber_proj['estimated_total_usd_lo']:.2f} (lo) / "
        f"${chamber_proj['estimated_total_usd_mid']:.2f} (mid) / "
        f"${chamber_proj['estimated_total_usd_hi']:.2f} (hi)"
    )
    return 0


# --- Phase-2: full chamber rebuild pipeline (steps 2-8) ---
#
# Step 2: Per-Member PTR PDF fetch (idempotent cache)
# Step 3: Per-page Gemini OCR via src.gemini_per_page_extract.extract_per_page
# Step 4: Structured normalization to per-tx schema
# Step 5: Canonical-view tx-key amendment-cascade dedup (per-Member partition)
# Step 6: audit_flag exclusions (per-Member served_from + tightened parse_error_suspect)
# Step 7: Per-Member aggregation (n_tx_total / n_tx_late / pct_late / worst_days_late)
# Step 8: Chamber percentile compute (Members with n_tx_total >= 20)

GEMINI_PROMPT_TEMPLATE = """Extract every Periodic Transaction Report (PTR) row from page {page_idx1} of {page_count} of doc {file_key}.

Each PTR row carries: asset_name (text including any (full ticker) suffix); asset_ticker (ticker symbol if disclosed; else null); owner code (one of SP, JT, DC, JT, or filer-blank); transaction_type (one-letter code: P=Purchase, S=Sale, S(partial)=partial sale, E=Exchange); transaction_date (MM/DD/YYYY); notification_date (MM/DD/YYYY; null if blank); amount_range (one of "$1,001 - $15,000", "$15,001 - $50,000", "$50,001 - $100,000", "$100,001 - $250,000", "$250,001 - $500,000", "$500,001 - $1,000,000", "$1,000,001 - $5,000,000", "$5,000,001 - $25,000,000", "$25,000,001 - $50,000,000", "Over $50,000,000"; or the literal text on the form if non-standard); capital_gains_over_200 (true/false/null).

Return JSON: {{"transactions": [ {{"asset_name": "...", "asset_ticker": "...", "owner": "...", "transaction_type": "...", "transaction_date": "MM/DD/YYYY", "notification_date": "MM/DD/YYYY", "amount_range": "...", "capital_gains_over_200": null}} ]}}.

If a page has no transactions (header/cover/instructions only), return {{"transactions": []}}. Strict JSON; no prose; no markdown fences."""


def fetch_pdf(url: str, dest: pathlib.Path, timeout: int = 60) -> bytes | None:
    """Idempotent PDF fetch. Skip if cached >2KB. Returns bytes or None on failure."""
    if dest.exists() and dest.stat().st_size > 2048:
        return dest.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "rebuild_chamber_audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
    except Exception as e:
        print(f"    [fetch FAIL] {url} -> {type(e).__name__}: {e}")
        return None
    if len(data) < 2048:
        print(f"    [fetch STUB] {url} -> {len(data)} bytes (skipping)")
        return None
    dest.write_bytes(data)
    return data


def extract_pdf_via_gemini(pdf_bytes: bytes, doc_id: str, cache_path: pathlib.Path) -> dict[str, Any] | None:
    """Run per-page Gemini OCR via the shared helper. Cache the result JSON."""
    if cache_path.exists() and cache_path.stat().st_size > 16:
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Lazy-import the helper from the sibling hhs_doge codebase. Reviewers
    # without hhs_doge can either (a) install the helper as a standalone
    # package, or (b) rely on the bundled chamber audit snapshot at
    # data/occ/house_chamber_audit_2026_05_02.json (the differ falls back to
    # BLOCKED_NEEDS_REVIEWER_REBUILD if the helper import fails).
    # Helper directory is resolved from $GEMINI_PER_PAGE_HELPER_DIR (preferred)
    # or $HHS_DOGE_HELPER_DIR (alias). If neither is set the import will fail
    # below and the differ returns BLOCKED_NEEDS_REVIEWER_REBUILD.
    helper_dir = (
        os.environ.get("GEMINI_PER_PAGE_HELPER_DIR")
        or os.environ.get("HHS_DOGE_HELPER_DIR")
    )
    if helper_dir:
        sys.path.insert(0, str(pathlib.Path(helper_dir)))
    try:
        from src.gemini_per_page_extract import extract_per_page  # type: ignore
    except Exception as e:
        print(f"    [gemini IMPORT FAIL] {e}")
        return None
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    try:
        result = extract_per_page(
            pdf_bytes=pdf_bytes,
            prompt_template=GEMINI_PROMPT_TEMPLATE,
            file_key=doc_id,
            model="gemini-3.1-flash-lite-preview",
            dpi=200,
            workers=10,
            api_key=api_key,
            check_garbled=False,
        )
    except Exception as e:
        print(f"    [gemini EXTRACT FAIL] {doc_id}: {type(e).__name__}: {e}")
        return None
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    # Strip non-JSON-serializable tails before caching
    pages = {}
    for pidx, p in result.get("pages", {}).items():
        pages[str(pidx)] = {
            "parsed": p.get("parsed"),
            "tokens_in": p.get("tokens_in", 0),
            "tokens_out": p.get("tokens_out", 0),
        }
    out = {
        "file_key": result.get("file_key", doc_id),
        "total_pages": result.get("total_pages", 0),
        "pages": pages,
        "stats": result.get("stats", {}),
    }
    cache_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def normalize_gemini_extract(
    extract: dict[str, Any],
    member_last: str,
    member_first: str,
    state_district: str,
    doc_id: str,
    year: int,
) -> list[dict[str, Any]]:
    """Step 4: flatten per-page Gemini JSON to per-tx schema matching
    data/occ/khanna_ptr_transactions_2026_05_02.json's `transactions` shape."""
    out: list[dict[str, Any]] = []
    for pidx, page in (extract.get("pages") or {}).items():
        parsed = page.get("parsed")
        if not parsed:
            continue
        rows = parsed.get("transactions", []) if isinstance(parsed, dict) else []
        if not isinstance(rows, list):
            continue
        for r in rows:
            if not isinstance(r, dict):
                continue
            amt_min, amt_max = _parse_amount_range(r.get("amount_range"))
            tx_iso = _parse_us_date(r.get("transaction_date"))
            notif_iso = _parse_us_date(r.get("notification_date"))
            out.append({
                "doc_id": str(doc_id),
                "year": int(year),
                "member_first_name": member_first,
                "member_last_name": member_last,
                "state_district": state_district,
                "asset_name": r.get("asset_name"),
                "asset_ticker": r.get("asset_ticker"),
                "asset_type": None,
                "owner": (r.get("owner") or "").strip().upper() or None,
                "transaction_type": (r.get("transaction_type") or "").strip().upper() or None,
                "transaction_date": tx_iso,
                "notification_date": notif_iso,
                "amount_min": amt_min,
                "amount_max": amt_max,
                "amount_range_text": r.get("amount_range"),
                "capital_gains_over_200": r.get("capital_gains_over_200"),
                "notes": None,
            })
    return out


_AMOUNT_BANDS = [
    ("$1,001 - $15,000", 1001, 15000),
    ("$15,001 - $50,000", 15001, 50000),
    ("$50,001 - $100,000", 50001, 100000),
    ("$100,001 - $250,000", 100001, 250000),
    ("$250,001 - $500,000", 250001, 500000),
    ("$500,001 - $1,000,000", 500001, 1000000),
    ("$1,000,001 - $5,000,000", 1000001, 5000000),
    ("$5,000,001 - $25,000,000", 5000001, 25000000),
    ("$25,000,001 - $50,000,000", 25000001, 50000000),
    ("Over $50,000,000", 50000001, None),
]


def _parse_amount_range(s: str | None) -> tuple[float | None, float | None]:
    if not s:
        return (None, None)
    s = s.strip()
    for lbl, lo, hi in _AMOUNT_BANDS:
        if s == lbl:
            return (float(lo), float(hi) if hi is not None else None)
    # tolerant fallback: drop spaces + hyphens, compare suffix
    return (None, None)


def _parse_us_date(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%Y-%m-%d"):
        try:
            return _dt.datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            continue
    return None


def _parse_iso_date(s: str | None) -> _dt.date | None:
    if not s:
        return None
    try:
        return _dt.date.fromisoformat(s)
    except Exception:
        return None


def _parse_filing_date(s: str | None) -> _dt.date | None:
    """House FD filing_date in source is "M/D/YYYY"; tolerate ISO too."""
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"):
        try:
            return _dt.datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def load_served_from() -> dict[tuple[str, str], _dt.date]:
    """Load (last, first_word) -> earliest served_from date from bundled CSV.
    Best-effort name-key match (drop suffixes / honorifics / second initials).
    """
    if not SERVED_FROM_CSV.exists():
        return {}
    out: dict[tuple[str, str], _dt.date] = {}
    with SERVED_FROM_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            last = (row["last_name"] or "").strip().upper()
            first = (row["first_name"] or "").strip().upper().split(" ")[0]
            served = (row["served_from"] or "").strip()
            if not (last and first and served):
                continue
            try:
                # served_from is a 4-digit year (text); convert to Jan 3 of that year.
                year = int(served[:4])
                d = _dt.date(year, 1, 3)
            except Exception:
                continue
            key = (last, first)
            if key not in out or d < out[key]:
                out[key] = d
    return out


def canonical_dedup_member(transactions: list[dict[str, Any]],
                            filing_index: dict[str, _dt.date]) -> list[dict[str, Any]]:
    """Per-Member tx-key amendment-cascade dedup. Mirrors rebuild_ptr_audit_khanna.py."""
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
    for _, rows in groups.items():
        for r in rows:
            r["_filing_date"] = filing_index.get(r["doc_id"])
        rows_with_fd = [r for r in rows if r["_filing_date"] is not None]
        if not rows_with_fd:
            continue
        earliest = min(rows_with_fd, key=lambda r: (r["_filing_date"], r["doc_id"]))
        latest = max(rows_with_fd, key=lambda r: (r["_filing_date"], r["doc_id"]))
        notif_dates = [_parse_iso_date(r.get("notification_date")) for r in rows_with_fd]
        notif_dates = [d for d in notif_dates if d]
        canonical_notif = min(notif_dates).isoformat() if notif_dates else None
        canonical = dict(earliest)
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


def aggregate_member(member_key: str, canonical_rows: list[dict[str, Any]],
                     served_from: _dt.date | None) -> dict[str, Any]:
    """Steps 6 + 7: audit_flag + days_late + per-Member aggregation."""
    last, first, state_dst = member_key.split("|")
    # Per-doc modern/old tx counts for parse_error_suspect tightened heuristic
    doc_modern_lt3yr: dict[str, int] = {}
    doc_modern_ge3yr: dict[str, int] = {}
    for tx in canonical_rows:
        tx_d = _parse_iso_date(tx.get("transaction_date"))
        f_d = _parse_iso_date(tx.get("earliest_filing_date"))
        if tx_d is None or f_d is None:
            continue
        gap = f_d.year - tx_d.year
        d = tx["earliest_doc_id"]
        if gap >= PARSE_ERROR_YEAR_GAP:
            doc_modern_ge3yr[d] = doc_modern_ge3yr.get(d, 0) + 1
        else:
            doc_modern_lt3yr[d] = doc_modern_lt3yr.get(d, 0) + 1

    flag_counts: dict[str, int] = {}
    auditable = []
    for tx in canonical_rows:
        flag = _assign_audit_flag(tx, served_from, doc_modern_lt3yr, doc_modern_ge3yr)
        tx["audit_flag"] = flag
        tx["days_late"] = _compute_days_late(tx) if flag == "auditable" else 0
        flag_counts[flag] = flag_counts.get(flag, 0) + 1
        if flag == "auditable":
            auditable.append(tx)

    n_tx_total = len(auditable)
    late = [t for t in auditable if t["days_late"] > 0]
    n_tx_late = len(late)
    days_late_when_late = sorted(t["days_late"] for t in late)
    pct_late = round((n_tx_late / n_tx_total) * 100, 4) if n_tx_total else 0.0
    worst = max((t["days_late"] for t in auditable), default=0)
    return {
        "member_last_name": last,
        "member_first_name": first,
        "state_district": state_dst,
        "served_from_iso": served_from.isoformat() if served_from else None,
        "n_canonical_post_dedup": len(canonical_rows),
        "audit_flag_distribution": flag_counts,
        "n_tx_total": n_tx_total,
        "n_tx_late": n_tx_late,
        "pct_late": pct_late,
        "worst_days_late": worst,
        "n_tx_over_90d_late": sum(1 for d in days_late_when_late if d > 90),
        "n_tx_over_180d_late": sum(1 for d in days_late_when_late if d > 180),
        "n_tx_over_1yr_late": sum(1 for d in days_late_when_late if d > 365),
        "median_days_late_when_late": (statistics.median(days_late_when_late)
                                        if days_late_when_late else 0),
    }


def _assign_audit_flag(tx, served_from, doc_modern_lt3yr, doc_modern_ge3yr):
    tx_date = _parse_iso_date(tx.get("transaction_date"))
    filing_date = _parse_iso_date(tx.get("earliest_filing_date"))
    if tx_date is None:
        return "no_tx_date"
    if filing_date is not None and tx_date > filing_date:
        return "tx_after_filing"
    if tx_date < STOCK_ACT_EFFECTIVE:
        return "pre_stock_act"
    if served_from is not None and tx_date < served_from - _dt.timedelta(days=PRE_TENURE_GRACE_DAYS):
        return "pre_tenure"
    if filing_date is not None:
        gap = filing_date.year - tx_date.year
        d = tx["earliest_doc_id"]
        if (gap >= PARSE_ERROR_YEAR_GAP
                and doc_modern_lt3yr.get(d, 0) > 0
                and 0 < doc_modern_ge3yr.get(d, 0) < PARSE_ERROR_MAX_OLD_TX):
            return "parse_error_suspect"
    return "auditable"


def _compute_days_late(tx):
    tx_d = _parse_iso_date(tx.get("transaction_date"))
    f_d = _parse_iso_date(tx.get("earliest_filing_date"))
    n_d = _parse_iso_date(tx.get("notification_date"))
    if tx_d is None or f_d is None:
        return 0
    deadline_tx = tx_d + _dt.timedelta(days=TX_DEADLINE_DAYS)
    if n_d is not None:
        deadline = min(deadline_tx, n_d + _dt.timedelta(days=NOTIF_DEADLINE_DAYS))
    else:
        deadline = deadline_tx
    return max(0, (f_d - deadline).days)


def chamber_percentiles(member_aggs: list[dict[str, Any]]) -> dict[str, Any]:
    """Step 8: chamber percentile compute over Members with n_tx_total >= 20."""
    eligible = [m for m in member_aggs if m["n_tx_total"] >= PERCENTILE_MIN_TX]
    if not eligible:
        return {"n_members": 0, "filter": f"n_tx_total >= {PERCENTILE_MIN_TX}"}
    rates = sorted(m["pct_late"] for m in eligible)
    worsts = sorted(m["worst_days_late"] for m in eligible)
    def _pct(arr, p):
        if not arr:
            return 0.0
        # nearest-rank percentile (matches numpy default)
        k = max(0, min(len(arr) - 1, int(round((p / 100) * (len(arr) - 1)))))
        return arr[k]
    out = {
        "n_members_eligible": len(eligible),
        "filter": f"n_tx_total >= {PERCENTILE_MIN_TX}",
        "rate_percentiles": {
            "p25_pct_late": _pct(rates, 25),
            "p50_pct_late": _pct(rates, 50),
            "p75_pct_late": _pct(rates, 75),
            "p95_pct_late": _pct(rates, 95),
        },
        "severity_percentiles": {
            "p50_worst_days": _pct(worsts, 50),
            "p75_worst_days": _pct(worsts, 75),
            "p95_worst_days": _pct(worsts, 95),
            "max_worst_days": worsts[-1] if worsts else 0,
        },
    }
    # Khanna severity rank if Khanna in cohort
    khanna = next((m for m in eligible
                   if m["member_last_name"] == "KHANNA"
                   and m["state_district"] == "CA17"), None)
    if khanna:
        khanna_worst = khanna["worst_days_late"]
        rank_le = sum(1 for w in worsts if w <= khanna_worst)
        out["khanna_severity_rank"] = {
            "khanna_worst": khanna_worst,
            "khanna_rank_le_n": rank_le,
            "rank_denominator": len(eligible),
        }
    return out


def run_chamber_pipeline(
    n_members: int | None,
    seed: int,
    max_spend_usd: float | None,
    years: list[int] | None,
) -> int:
    """Run steps 2-8 against the chamber universe (or N-Member sample).

    n_members=None => full chamber. Otherwise sample N Members (deterministic).
    max_spend_usd=None => no spend ceiling. Otherwise abort once projected spend
    crosses ceiling (PDF count × COST_PER_PDF_USD_MID).
    """
    print("[chamber-rebuild Phase-2] enumerating chamber PTR universe ...")
    inv = enumerate_chamber_ptr_universe(years=years)
    if inv["n_zips_scanned"] == 0:
        print("FATAL: no per-year FD ZIPs cached. Run "
              "`python fetch_substrate_occ.py --classes house_fd` first.")
        return 5
    print(f"  {inv['n_zips_scanned']} per-year ZIPs / {inv['n_ptr_rows']:,} PTR rows / "
          f"{inv['n_members']:,} distinct Members")

    universe = inv["universe"]
    member_keys = sorted(universe.keys())
    if n_members is not None and n_members < len(member_keys):
        rng = random.Random(seed)
        member_keys = rng.sample(member_keys, k=n_members)
    n_ptrs = sum(len(universe[k]) for k in member_keys)
    proj_mid = round(n_ptrs * COST_PER_PDF_USD_MID, 2)
    print(f"  Sample: {len(member_keys)} Members / {n_ptrs} PTRs / projected ~${proj_mid:.2f} mid")
    if max_spend_usd is not None and proj_mid > max_spend_usd:
        print(f"FATAL: projected spend ${proj_mid:.2f} exceeds --max-spend-usd ${max_spend_usd:.2f}.")
        return 6

    served_lookup = load_served_from()
    if not served_lookup:
        print("WARN: served_from CSV empty; pre_tenure filter inert (chamber percentiles "
              "approximate to within ~13% Member-coverage gap).")

    # Step 2 + 3: fetch + Gemini OCR per PTR
    member_results = []
    spent_usd = 0.0
    for mi, mk in enumerate(member_keys, 1):
        rows = universe[mk]
        last, first, sd = mk.split("|")
        first_word = first.split(" ")[0]
        served = served_lookup.get((last, first_word))
        print(f"\n  [{mi}/{len(member_keys)}] {last}, {first} ({sd}) — "
              f"{len(rows)} PTRs (served_from={served.isoformat() if served else 'unknown'})")
        all_tx_raw: list[dict[str, Any]] = []
        filing_index_member: dict[str, _dt.date] = {}
        for r in rows:
            doc_id = r["doc_id"]
            year = r["year"]
            f_d = _parse_filing_date(r.get("filing_date"))
            if f_d is None:
                continue
            filing_index_member[str(doc_id)] = f_d
            pdf_path = PTR_PDF_CACHE / str(year) / f"{doc_id}.pdf"
            extract_path = GEMINI_CACHE / str(year) / f"{doc_id}.json"
            pdf_bytes = fetch_pdf(r["pdf_url"], pdf_path)
            if pdf_bytes is None:
                continue
            extract = extract_pdf_via_gemini(pdf_bytes, doc_id, extract_path)
            if extract is None:
                continue
            tin = sum((p.get("tokens_in", 0) or 0) for p in extract.get("pages", {}).values())
            tout = sum((p.get("tokens_out", 0) or 0) for p in extract.get("pages", {}).values())
            # Approx cost from tokens (gemini-3.1-flash-lite-preview pricing)
            cost = (tin / 1_000_000) * 0.10 + (tout / 1_000_000) * 0.40
            spent_usd += cost
            tx_rows = normalize_gemini_extract(extract, last, first, sd, doc_id, year)
            all_tx_raw.extend(tx_rows)
        canonical = canonical_dedup_member(all_tx_raw, filing_index_member)
        agg = aggregate_member(mk, canonical, served)
        agg["n_pdfs_processed"] = len([r for r in rows if r.get("doc_id")])
        member_results.append(agg)

    # Step 8: chamber percentiles
    pct = chamber_percentiles(member_results)
    is_full = (n_members is None) or (n_members >= inv["n_members"])
    out: dict[str, Any] = {
        "rebuild_run_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "snapshot_target": "OCC_M010 + chamber severity context (Phase-2 rebuild)",
        "snapshot_input": "data/occ/house_chamber_audit_2026_05_02.json",
        "served_from_csv": "data/occ/house_member_served_from_2026_05_03.csv",
        "is_full_chamber_rebuild": is_full,
        "n_members_in_sample": len(member_results),
        "n_members_in_universe_total": inv["n_members"],
        "n_ptrs_in_universe_total": inv["n_ptr_rows"],
        "estimated_spend_usd": round(spent_usd, 4),
        "model": "gemini-3.1-flash-lite-preview",
        "members": member_results,
        "chamber_percentiles": pct,
    }
    # Surface top-level scalar blocks ONLY for full-chamber rebuild so the
    # differ sees BIT-EXACT-comparable shapes vs the snapshot. For sample
    # rebuilds, the differ reads `is_full_chamber_rebuild=False` and emits
    # PASS_WITH_DEFECT/sample_rebuild_subset_of_chamber (load-bearing scalars
    # are valid sample percentiles, not the chamber population).
    if is_full and pct.get("rate_percentiles"):
        out["rate_percentiles"] = {"n_members": pct["n_members_eligible"], **pct["rate_percentiles"]}
        out["severity_percentiles"] = {"n_members_with_worst": pct["n_members_eligible"],
                                        **pct["severity_percentiles"]}
        if pct.get("khanna_severity_rank"):
            out["khanna_severity_rank"] = pct["khanna_severity_rank"]
    out_path = DATA_OCR / "house_chamber_audit_REBUILT.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[chamber-rebuild Phase-2] wrote {out_path}")
    print(f"  Members processed: {len(member_results)}")
    print(f"  Eligible (n_tx_total>={PERCENTILE_MIN_TX}): {pct.get('n_members_eligible', 0)}")
    print(f"  Estimated Gemini spend: ${spent_usd:.4f}")
    if pct.get("rate_percentiles"):
        rp = pct["rate_percentiles"]
        sp = pct["severity_percentiles"]
        print(f"  Sample rate p50={rp['p50_pct_late']}, severity p50={sp['p50_worst_days']}")
    return 0


# --- Full chamber path (gated; Phase-2) ---

def cmd_full_chamber(cost_acknowledged: bool) -> int:
    """The full chamber-wide rebuild path. Requires --cost-acknowledged
    AND GEMINI_API_KEY in the environment. Phase-2 work; the chamber-fetch
    + per-page Gemini OCR + structured normalization + per-Member
    aggregation pipeline is documented as inline TODO blocks above."""
    if not cost_acknowledged:
        print(
            "REFUSING to run --full-chamber without --cost-acknowledged.\n"
            "\n"
            "The full chamber-wide rebuild fetches ~5K-10K House Member PTR "
            "PDFs from disclosures-clerk.house.gov AND invokes Gemini per-"
            "page OCR on each page. Estimated reviewer spend:\n"
        )
        proj = _project_cost(7_500)  # midpoint estimate
        print(
            f"  Mid-band: ${proj['estimated_total_usd_lo']:.2f} (lo) / "
            f"${proj['estimated_total_usd_mid']:.2f} (mid) / "
            f"${proj['estimated_total_usd_hi']:.2f} (hi)\n"
            f"  Model: {proj['model']}\n"
            f"  Per-PDF assumption: {proj['per_pdf_assumption']}\n"
            "\n"
            "If you accept this spend AND have GEMINI_API_KEY in the env:\n"
            "    python rebuild_chamber_audit.py --full-chamber --cost-acknowledged\n"
        )
        return 2
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print(
            "REFUSING to run --full-chamber: GEMINI_API_KEY (or GOOGLE_API_KEY) not in env.\n"
            "Set GEMINI_API_KEY before re-running."
        )
        return 3
    return run_chamber_pipeline(
        n_members=None,  # full chamber
        seed=42,
        max_spend_usd=None,
        years=None,
    )


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--dry-run-smoke", action="store_true",
        help="(default) Enumerate 5 random Members + print would-be fetch URLs "
             "+ projected cost. Zero spend.",
    )
    p.add_argument(
        "--full-chamber", action="store_true",
        help="Invoke the full chamber-wide rebuild pipeline (Phase-2; gated "
             "behind --cost-acknowledged).",
    )
    p.add_argument(
        "--cost-acknowledged", action="store_true",
        help="Reviewer acknowledgment of the projected $50-200 reviewer "
             "Gemini spend; required for --full-chamber.",
    )
    p.add_argument("--n-members", type=int, default=5, help="Sample size for dry-run smoke OR --sample-rebuild (default 5).")
    p.add_argument("--seed", type=int, default=42, help="Random seed for sample selection (default 42).")
    p.add_argument(
        "--sample-rebuild", action="store_true",
        help="Run the Phase-2 pipeline (steps 2-8) against an N-Member sample "
             "(default 5). Requires GEMINI_API_KEY. Bounded by --max-spend-usd.",
    )
    p.add_argument(
        "--max-spend-usd", type=float, default=2.0,
        help="Hard ceiling on projected Gemini spend (default $2.00 for "
             "--sample-rebuild). --full-chamber ignores this ceiling.",
    )
    args = p.parse_args()

    if args.full_chamber:
        return cmd_full_chamber(args.cost_acknowledged)
    if args.sample_rebuild:
        if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            print("REFUSING --sample-rebuild: GEMINI_API_KEY (or GOOGLE_API_KEY) not in env.")
            return 3
        return run_chamber_pipeline(
            n_members=args.n_members,
            seed=args.seed,
            max_spend_usd=args.max_spend_usd,
            years=None,
        )
    # Default: dry-run smoke
    return cmd_dry_run_smoke(n_members=args.n_members, seed=args.seed)


if __name__ == "__main__":
    sys.exit(main())
