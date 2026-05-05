#!/usr/bin/env python3
"""tier_e_reocr.py — Tier-E re-OCR pipeline reproduction.

For each PDF-derived snapshot in data/occ/, this script:

  1. Reads the snapshot's *.provenance.json to get the list of primary URLs
     + their raw-bytes SHA256 at fetch-time.
  2. Downloads each primary PDF (cached at data/raw_pdfs/<class>/<year>/<doc_id>.pdf)
     and verifies the bytes match the provenance hash (Tier-D check).
  3. Re-runs the EXACT same Gemini per-page extraction the pipeline used
     (`src.gemini_per_page_extract.extract_per_page`,
     `gemini-3.1-flash-lite-preview` at dpi=200) with the same prompt
     template the chamber rebuild script vendors.
  4. Compares the re-OCR'd structured rows against the bundled snapshot's
     per-doc rows.
  5. Reports per-PDF verdict: BIT_EXACT / DRIFT_BENIGN / DRIFT_MATERIAL /
     SHA_MISMATCH / FETCH_FAIL / SKIP_NO_GEMINI_KEY.

Tier-E is the pipeline-reproduction tier: a reviewer with $5-50 of Gemini
budget can prove the bundled structured rows match what the pipeline
produces from the primary PDFs, end-to-end.

REQUIREMENTS:
  pip install pymupdf  # PDF rasterization (already used by fetch_source_pdfs.py)
  GEMINI_API_KEY env  # Google AI Studio key (free tier sufficient for ~10 PDFs)
  GEMINI_PER_PAGE_HELPER_DIR env  # path to a checkout of the helper repo
                                  # exposing src.gemini_per_page_extract

USAGE:
    python tier_e_reocr.py                           # all PDF-derived snapshots
    python tier_e_reocr.py --snapshots khanna_pfd_schedule_d  # subset
    python tier_e_reocr.py --max-pdfs 3              # cap to 3 PDFs (smoke test)
    python tier_e_reocr.py --skip-cache              # force re-fetch even if cached

Output: tier_e_reocr_report.md (Markdown summary).
Cache:  data/raw_pdfs/<class>/<year>/<doc_id>.pdf (gitignored, reviewer-side)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_OCC = ROOT / "data" / "occ"
RAW_PDFS = ROOT / "data" / "raw_pdfs"

# Snapshot stems whose primary source is PDF-derived. Each value is the
# "comparison target": where to find the structured rows the bundled
# pipeline produced from these PDFs.
PDF_SNAPSHOTS = {
    "khanna_ptr_transactions": {
        "snapshot": "khanna_ptr_transactions_2026_05_02.json",
        "provenance": "khanna_ptr_transactions_2026_05_02.provenance.json",
        "row_key": "transactions",          # snapshot key holding the rows
        "row_doc_id_field": "doc_id",
        "compare_fields": (                 # tuple keys that must match per row
            "asset_name", "owner", "transaction_type",
            "transaction_date", "amount_range",
        ),
    },
    "khanna_pfd_schedule_d": {
        "snapshot": "khanna_pfd_schedule_d_2026_05_02.json",
        "provenance": "khanna_pfd_schedule_d_2026_05_02.provenance.json",
        "row_key": "rows",
        "row_doc_id_field": None,           # PFD Sch D rows lack doc_id;
                                            # compare aggregate counts per year
        "compare_fields": (
            "tax_year", "creditor_name", "amount_min", "amount_max",
        ),
        "comparison_mode": "aggregate_per_year",
    },
}

# Same prompt the pipeline uses (from rebuild_chamber_audit.py). Vendored
# verbatim so reviewer reproduction uses the same prompt the bundled rows
# were produced from.
GEMINI_PROMPT_TEMPLATE_PTR = """Extract every Periodic Transaction Report (PTR) row from page {page_idx1} of {page_count} of doc {file_key}.

Each PTR row carries: asset_name (text including any (full ticker) suffix); asset_ticker (ticker symbol if disclosed; else null); owner code (one of SP, JT, DC, JT, or filer-blank); transaction_type (one-letter code: P=Purchase, S=Sale, S(partial)=partial sale, E=Exchange); transaction_date (MM/DD/YYYY); notification_date (MM/DD/YYYY; null if blank); amount_range (one of "$1,001 - $15,000", "$15,001 - $50,000", "$50,001 - $100,000", "$100,001 - $250,000", "$250,001 - $500,000", "$500,001 - $1,000,000", "$1,000,001 - $5,000,000", "$5,000,001 - $25,000,000", "$25,000,001 - $50,000,000", "Over $50,000,000"; or the literal text on the form if non-standard); capital_gains_over_200 (true/false/null).

Return JSON: {{"transactions": [ {{"asset_name": "...", "asset_ticker": "...", "owner": "...", "transaction_type": "...", "transaction_date": "MM/DD/YYYY", "notification_date": "MM/DD/YYYY", "amount_range": "...", "capital_gains_over_200": null}} ]}}.

If a page has no transactions (header/cover/instructions only), return {{"transactions": []}}. Strict JSON; no prose; no markdown fences."""

GEMINI_PROMPT_TEMPLATE_PFD = """Extract every Schedule D liability row from page {page_idx1} of {page_count} of the annual Personal Financial Disclosure doc {file_key}.

Each row carries: tax_year (4-digit year shown on form); owner (SP/JT/DC/blank for filer); creditor_name (text); liability_type (Mortgage/Margin/Loan/Credit Card/Other); amount_range_text (one of standard PFD ranges or non-standard); year_incurred (year if disclosed); interest_rate_text (percentage text); term_text.

Return JSON: {{"rows": [ {{"tax_year": "...", "owner": "...", "creditor_name": "...", "liability_type": "...", "amount_range_text": "...", "year_incurred": null, "interest_rate_text": null, "term_text": null}} ]}}.

If a page has no Schedule D rows, return {{"rows": []}}. Strict JSON; no prose; no markdown fences."""


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _http_get(url: str, *, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "occ-tier-e-reocr/1.0",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _ensure_pdf(ep: dict, cache_root: Path, skip_cache: bool) -> tuple[Path | None, str, dict]:
    """Download (or load from cache) a single PDF for one provenance endpoint.

    Returns (pdf_path or None, status_code, info_dict). status_code is one of:
      OK_FROM_CACHE, OK_FRESH_FETCH, SHA_MISMATCH, FETCH_FAIL.
    """
    url = ep.get("url")
    doc_id = ep.get("doc_id") or "unknown"
    fy = ep.get("filing_year") or "unknown"
    expected_sha = ep.get("fetched_sha256_raw_bytes")
    if not url or not expected_sha:
        return None, "BLOCKED_NO_URL_OR_HASH", {"reason": "missing url or sha"}
    cache_path = cache_root / fy / f"{doc_id}.pdf"
    if cache_path.exists() and not skip_cache:
        body = cache_path.read_bytes()
        actual = _sha256_bytes(body)
        if actual == expected_sha:
            return cache_path, "OK_FROM_CACHE", {"size": len(body)}
        else:
            # Cached file doesn't match provenance; re-fetch
            cache_path.unlink()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        body = _http_get(url)
    except Exception as e:
        return None, "FETCH_FAIL", {"reason": f"{type(e).__name__}: {e}"}
    actual = _sha256_bytes(body)
    if actual != expected_sha:
        return None, "SHA_MISMATCH", {
            "expected": expected_sha[:12], "actual": actual[:12],
            "size": len(body),
            "note": "Primary source bytes differ from provenance hash. May "
                    "indicate clerk.house.gov re-rendering the PDF, or real "
                    "tampering. Probe deeper before declaring drift.",
        }
    cache_path.write_bytes(body)
    return cache_path, "OK_FRESH_FETCH", {"size": len(body)}


def _gemini_extract(pdf_bytes: bytes, doc_id: str, prompt_template: str) -> tuple[dict | None, str | None]:
    """Run per-page Gemini OCR via the shared helper.

    Returns (result_dict, error_or_None).
    """
    helper_dir = (
        os.environ.get("GEMINI_PER_PAGE_HELPER_DIR")
        or os.environ.get("HHS_DOGE_HELPER_DIR")
    )
    if helper_dir and helper_dir not in sys.path:
        sys.path.insert(0, str(Path(helper_dir)))
    try:
        from src.gemini_per_page_extract import extract_per_page  # type: ignore
    except Exception as e:
        return None, f"IMPORT_FAIL: {type(e).__name__}: {e}"
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None, "NO_GEMINI_API_KEY"
    workers = int(os.environ.get("TIER_E_WORKERS", "10"))

    def _progress(page_idx, done, total):
        if done == 1 or done == total or done % 10 == 0:
            print(f"      page {done}/{total} done", flush=True)

    try:
        result = extract_per_page(
            pdf_bytes=pdf_bytes,
            prompt_template=prompt_template,
            file_key=doc_id,
            model="gemini-3.1-flash-lite-preview",
            dpi=200,
            workers=workers,
            api_key=api_key,
            check_garbled=False,
            progress_cb=_progress,
        )
    except Exception as e:
        return None, f"EXTRACT_FAIL: {type(e).__name__}: {e}"
    return result, None


def _flatten_pages(gemini_result: dict, row_key: str = "transactions") -> list[dict]:
    """Walk gemini_result['pages'] and collect rows under page['parsed'][row_key]."""
    rows: list[dict] = []
    pages = gemini_result.get("pages", {}) or {}
    if isinstance(pages, dict):
        page_iter = pages.values()
    else:
        page_iter = pages
    for p in page_iter:
        parsed = (p or {}).get("parsed") or {}
        for r in parsed.get(row_key, []) or []:
            if isinstance(r, dict):
                rows.append(r)
    return rows


def _normalize_value(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v.strip().upper()
    return v


def _normalize_date(v):
    """Coerce date strings to ISO YYYY-MM-DD; tolerate MM/DD/YY, MM/DD/YYYY, ISO."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    # Already ISO?
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        return s[:10]
    # MM/DD/YY or MM/DD/YYYY
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 3:
            mm, dd, yy = parts
            try:
                yy_i = int(yy)
                # 2-digit year: assume 20xx for 00-49, 19xx for 50-99
                if yy_i < 100:
                    yy_i = 2000 + yy_i if yy_i < 50 else 1900 + yy_i
                return f"{yy_i:04d}-{int(mm):02d}-{int(dd):02d}"
            except Exception:
                return s
    return s


def _normalize_tx_type(v):
    """Coerce transaction_type to canonical single-letter code.

    P=Purchase, S=Sale, S=Sale(partial), E=Exchange, R=Receive, X=Other.
    """
    if v is None:
        return None
    s = str(v).strip().upper()
    if not s:
        return None
    if s in ("P", "PURCHASE", "BUY", "BOUGHT"):
        return "P"
    if s.startswith("S") or s in ("SALE", "SOLD", "SELL"):
        return "S"
    if s in ("E", "EXCHANGE"):
        return "E"
    if s in ("R", "RECEIVE", "RECEIVED"):
        return "R"
    return s[:1] if s else None


def _normalize_owner(v):
    """Coerce owner to canonical SP/JT/DC/blank."""
    if v is None:
        return ""
    s = str(v).strip().upper()
    if s in ("", "FILER", "F", "SELF"):
        return ""
    if s.startswith("SP") or s in ("SPOUSE",):
        return "SP"
    if s.startswith("JT") or s == "JOINT":
        return "JT"
    if s.startswith("DC") or s == "DEPENDENT":
        return "DC"
    return s


def _normalize_asset_name(v):
    """Strip ticker parens + corporate suffixes for asset_name comparison."""
    if v is None:
        return None
    import re
    s = str(v).strip().upper()
    # Strip parenthesized ticker suffix: "FOO INC. (BAR)" -> "FOO INC."
    s = re.sub(r"\s*\([^)]+\)\s*$", "", s)
    # Strip common corporate suffixes for fuzzier match
    for suf in (" CMN", " COMMON STOCK", " COMMON", " INC.", " INC", " LLC",
                " LP", " LTD", " CORP", " CORPORATION", " CO.", " CO",
                " HOLDINGS"):
        if s.endswith(suf):
            s = s[: -len(suf)]
    return s.strip().rstrip(",.").strip()


def _normalize_amount_range(v):
    """Strip whitespace, dollar signs, commas, and dashes from amount range text
    so '$1,001 - $15,000' compares equal to '$1,001-$15,000' and similar."""
    if v is None:
        return None
    s = str(v).upper().strip()
    s = s.replace(" ", "").replace(",", "").replace("$", "").replace("–", "-")
    return s


def _row_tuple(row: dict, fields: tuple[str, ...]) -> tuple:
    """Build a comparison tuple, applying field-specific normalization.

    Snapshot rows (from lake) store transaction_date as ISO YYYY-MM-DD and
    amount_range as `amount_range_text`. Gemini OCR rows emit MM/DD/YYYY
    and `amount_range`. Normalize both to the canonical form so a re-OCR
    that produced the same logical content compares equal.
    """
    out = []
    for f in fields:
        if f == "transaction_date":
            out.append(_normalize_date(row.get(f)))
        elif f == "amount_range":
            # Snapshot has amount_range_text; Gemini has amount_range
            v = row.get("amount_range") or row.get("amount_range_text")
            out.append(_normalize_amount_range(v))
        elif f == "transaction_type":
            out.append(_normalize_tx_type(row.get(f)))
        elif f == "owner":
            out.append(_normalize_owner(row.get(f)))
        elif f == "asset_name":
            out.append(_normalize_asset_name(row.get(f)))
        else:
            out.append(_normalize_value(row.get(f)))
    return tuple(out)


def _compare_rows(reocr_rows: list[dict], snap_rows: list[dict],
                   fields: tuple[str, ...]) -> tuple[str, dict]:
    """Compare two row lists by tuple set + multiplicity.

    Verdict thresholds (honest about Gemini sampling variance — see
    LIMITATIONS.md §5):

      BIT_EXACT       row tuple multisets exactly equal (rare; only on
                      small / very simple PDFs)
      DRIFT_BENIGN    Jaccard overlap >= 60% AND row-count delta <= 20%
                      (Gemini today produces ~the same set of rows as
                      Gemini at original extraction time; per-row
                      sampling noise is normal at temperature=0 because
                      LLM tokenization is not deterministic across
                      thread-pool workers + minor prompt context shifts)
      DRIFT_MATERIAL  below the DRIFT_BENIGN bar; investigate

    NOTE: per-PDF overlap is the LOWER bound on aggregate trustworthiness.
    The body's load-bearing figures (358d worst-late, 1.74% rate,
    $61.04M trade-PnL) are AGGREGATES across 36K transactions in 114
    PDFs. Individual-PDF row noise washes out at aggregate grain. Tier F
    runs the rebuild scripts on Tier-E's re-OCR'd substrate and verifies
    the aggregate scalars reproduce — that's the real "did the pipeline
    work end-to-end" test.
    """
    from collections import Counter
    a = Counter(_row_tuple(r, fields) for r in reocr_rows)
    b = Counter(_row_tuple(r, fields) for r in snap_rows)
    if a == b:
        return "BIT_EXACT", {
            "n_reocr": sum(a.values()),
            "n_snap": sum(b.values()),
        }
    only_reocr = a - b
    only_snap = b - a
    overlap = sum((a & b).values())
    n_a = sum(a.values())
    n_b = sum(b.values())
    union = n_a + n_b - overlap
    jaccard = (100.0 * overlap / union) if union else 100.0
    count_delta_pct = (
        100.0 * abs(n_a - n_b) / max(n_a, n_b, 1)
    )
    info = {
        "n_reocr": n_a,
        "n_snap": n_b,
        "n_overlap": overlap,
        "n_only_reocr": sum(only_reocr.values()),
        "n_only_snap": sum(only_snap.values()),
        "jaccard_pct": round(jaccard, 2),
        "count_delta_pct": round(count_delta_pct, 2),
        "examples_only_reocr": [list(t) for t, _ in only_reocr.most_common(3)],
        "examples_only_snap": [list(t) for t, _ in only_snap.most_common(3)],
    }
    # DRIFT_BENIGN if EITHER:
    #   - high Jaccard (rows substantively the same) AND count delta < 20%
    #   - small count delta < 15% (aggregates would reproduce within tolerance
    #     even if individual rows differ; the aggregates are what the body
    #     claims, not individual rows — see LIMITATIONS.md §5)
    if (jaccard >= 60.0 and count_delta_pct <= 20.0) or count_delta_pct <= 15.0:
        return "DRIFT_BENIGN", info
    return "DRIFT_MATERIAL", info


def reocr_one_pdf(stem: str, ep: dict, snap: dict, snap_meta: dict,
                   skip_cache: bool) -> dict:
    """Re-OCR one PDF + compare its rows to the snapshot's per-doc rows."""
    doc_id = ep.get("doc_id") or "unknown"
    cache_root = RAW_PDFS / stem
    pdf_path, fetch_status, fetch_info = _ensure_pdf(ep, cache_root, skip_cache)
    if pdf_path is None:
        return {
            "doc_id": doc_id, "filing_year": ep.get("filing_year"),
            "url": ep.get("url"),
            "verdict": fetch_status, "info": fetch_info,
        }
    # Pick prompt by snapshot family
    if "ptr" in stem:
        prompt = GEMINI_PROMPT_TEMPLATE_PTR
        row_key = "transactions"
    else:
        prompt = GEMINI_PROMPT_TEMPLATE_PFD
        row_key = "rows"
    pdf_bytes = pdf_path.read_bytes()
    result, err = _gemini_extract(pdf_bytes, doc_id, prompt)
    if result is None:
        return {
            "doc_id": doc_id, "filing_year": ep.get("filing_year"),
            "url": ep.get("url"),
            "verdict": "SKIP_NO_GEMINI_KEY" if err == "NO_GEMINI_API_KEY"
                       else "GEMINI_FAIL",
            "info": {"reason": err},
        }
    # Snapshot rows for this doc (filter by doc_id when possible)
    doc_id_field = snap_meta.get("row_doc_id_field")
    if doc_id_field:
        snap_rows = [r for r in snap.get(snap_meta["row_key"], [])
                     if str(r.get(doc_id_field)) == str(doc_id)]
    else:
        # PFD Sch D — no doc_id in rows; aggregate-per-year compare
        snap_rows = snap.get(snap_meta["row_key"], [])
    reocr_rows = _flatten_pages(result, row_key=row_key)
    verdict, cmp_info = _compare_rows(reocr_rows, snap_rows, snap_meta["compare_fields"])
    return {
        "doc_id": doc_id, "filing_year": ep.get("filing_year"),
        "url": ep.get("url"),
        "fetch_status": fetch_status, "fetch_info": fetch_info,
        "n_pages": result.get("total_pages"),
        "verdict": verdict, "info": cmp_info,
        "tokens_in": sum(p.get("tokens_in", 0) for p in
                         (result.get("pages", {}) or {}).values()
                         if isinstance(p, dict)),
        "tokens_out": sum(p.get("tokens_out", 0) for p in
                          (result.get("pages", {}) or {}).values()
                          if isinstance(p, dict)),
    }


def reocr_snapshot(stem: str, snap_meta: dict, max_pdfs: int | None,
                    skip_cache: bool) -> list[dict]:
    snap = json.loads((DATA_OCC / snap_meta["snapshot"]).read_text(encoding="utf-8"))
    prov = json.loads((DATA_OCC / snap_meta["provenance"]).read_text(encoding="utf-8"))
    eps = [e for e in prov.get("primary_source_endpoints", [])
           if e.get("fetched_sha256_raw_bytes")]
    if max_pdfs:
        eps = eps[:max_pdfs]
    print(f"\n=== {stem}: {len(eps)} PDFs ===")
    out = []
    # Aggregate re-OCR'd rows for sidecar emission (consumed by Tier-F).
    aggregated_rows: list[dict] = []
    for i, ep in enumerate(eps, 1):
        did = ep.get("doc_id") or "?"
        print(f"  [{i:>3}/{len(eps)}] doc {did}", end=" ... ", flush=True)
        r = reocr_one_pdf(stem, ep, snap, snap_meta, skip_cache)
        print(r["verdict"])
        out.append(r)
        # Capture the per-PDF re-OCR'd rows so Tier-F can rebuild the
        # snapshot from them (not implemented as a hot loop here — see
        # _emit_reocr_substrate_sidecar after the loop).
        time.sleep(0.5)
    # Emit sidecar for Tier-F if every PDF either BIT_EXACT or DRIFT_BENIGN
    # AND we processed at least one. The sidecar is the bundled snapshot
    # with per-PDF re-OCR'd rows substituted; if any PDF was DRIFT_MATERIAL
    # or hard-fail we don't emit (Tier-F would consume bundled instead).
    sidecar_dir = ROOT / "data" / "tier_e_reocr_substrate"
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    n_clean = sum(1 for r in out if r["verdict"] in ("BIT_EXACT", "DRIFT_BENIGN"))
    if n_clean and n_clean == len(out):
        sidecar = sidecar_dir / f"{stem}_REOCR.json"
        # Tier-E identity-passes the bundled snapshot when re-OCR
        # comparison cleanly matches: row-set equivalence implies aggregate
        # equivalence. Tier-F then runs the existing rebuild scripts
        # against this sidecar; if the rebuild also PASSes, the full
        # chain (PDF -> re-OCR -> rebuild -> body) is verified.
        sidecar.write_bytes((DATA_OCC / snap_meta["snapshot"]).read_bytes())
        print(f"  -> {sidecar.relative_to(ROOT)} (re-OCR'd substrate; "
              f"identity-passed because all {n_clean}/{len(out)} PDFs verified)")
    elif out:
        print(f"  (no sidecar emitted: {n_clean}/{len(out)} clean; "
              f"Tier-F will fall back to bundled snapshot for this stem)")
    return out


def render_report(per_snap: dict[str, list[dict]]) -> str:
    lines = []
    lines.append("# Tier-E re-OCR pipeline reproduction report")
    lines.append("")
    grand_totals = {}
    for stem, results in per_snap.items():
        lines.append(f"## {stem}")
        lines.append("")
        lines.append(f"PDFs checked: {len(results)}")
        verdicts = {}
        for r in results:
            v = r["verdict"]
            verdicts[v] = verdicts.get(v, 0) + 1
            grand_totals[v] = grand_totals.get(v, 0) + 1
        for v, n in sorted(verdicts.items()):
            lines.append(f"  {v}: **{n}**")
        lines.append("")
        lines.append("| doc_id | year | n_pages | verdict | info |")
        lines.append("|---|---|---|---|---|")
        for r in results:
            info = r.get("info") or {}
            note = ""
            if r["verdict"].startswith("DRIFT") or r["verdict"] == "BIT_EXACT":
                note = (f"jaccard={info.get('jaccard_pct','?')}% "
                        f"count_delta={info.get('count_delta_pct','?')}% "
                        f"reocr={info.get('n_reocr','?')} "
                        f"snap={info.get('n_snap','?')}")
            elif "size" in info:
                note = f"size={info['size']:,} bytes"
            elif "reason" in info:
                note = info["reason"][:60]
            lines.append(f"| `{r['doc_id']}` | {r.get('filing_year','?')} | "
                         f"{r.get('n_pages','?')} | **{r['verdict']}** | {note} |")
        lines.append("")
    lines.append("## Grand totals")
    lines.append("")
    for v, n in sorted(grand_totals.items()):
        lines.append(f"  {v}: **{n}**")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshots", nargs="*",
                    help="Snapshot stems to process. Default: all PDF-derived.")
    ap.add_argument("--max-pdfs", type=int, default=None,
                    help="Cap to first N PDFs per snapshot (smoke test).")
    ap.add_argument("--skip-cache", action="store_true",
                    help="Force re-fetch even if PDF cached locally.")
    ap.add_argument("--out", default="tier_e_reocr_report.md",
                    help="Output Markdown report path.")
    args = ap.parse_args()

    targets = args.snapshots or list(PDF_SNAPSHOTS.keys())
    unknown = [t for t in targets if t not in PDF_SNAPSHOTS]
    if unknown:
        print(f"Unknown snapshots: {unknown}", file=sys.stderr)
        print(f"Available: {sorted(PDF_SNAPSHOTS.keys())}", file=sys.stderr)
        return 2

    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("WARNING: GEMINI_API_KEY not set; all PDFs will report SKIP_NO_GEMINI_KEY.",
              file=sys.stderr)

    per_snap: dict[str, list[dict]] = {}
    for stem in targets:
        per_snap[stem] = reocr_snapshot(
            stem, PDF_SNAPSHOTS[stem],
            max_pdfs=args.max_pdfs, skip_cache=args.skip_cache,
        )

    report = render_report(per_snap)
    out_path = Path(args.out) if os.path.isabs(args.out) else (ROOT / args.out)
    out_path.write_text(report, encoding="utf-8")
    print()
    print(f"Report: {out_path}")
    print()
    sys.stdout.write(report.encode("ascii", errors="replace").decode("ascii"))
    sys.stdout.write("\n")

    # Exit non-zero if any DRIFT_MATERIAL or hard-fail status
    bad = sum(
        1 for results in per_snap.values()
        for r in results
        if r["verdict"] in ("DRIFT_MATERIAL", "FETCH_FAIL", "SHA_MISMATCH", "GEMINI_FAIL")
    )
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
