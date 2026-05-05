#!/usr/bin/env python3
"""build_provenance.py — generate per-snapshot provenance manifests.

For each snapshot in `data/occ/`, emit a sibling
`<snapshot>.provenance.json` documenting:

  - The snapshot file's own SHA256 (for tamper detection at the snapshot grain)
  - The PRIMARY-SOURCE class the snapshot derives from
  - The list of primary URLs that were fetched, plus the raw-bytes SHA256 of
    each fetched body at fetch time
  - The fetch script + git commit + post-fetch transformations applied
  - Any GAP_REASON for sources that cannot be re-fetched anonymously
    (yfinance vendor-relayed, lake-derived SQL, ProPublica Cloudflare-blocked)

This script is run ONCE at release-build time. It is idempotent: re-running
will skip primary-source fetches whose hash is already populated unless
--rebuild is passed.

Output: provenance JSON files alongside the snapshots they describe.

USAGE:
    python build_provenance.py            # generate all (skip already-fetched)
    python build_provenance.py --classes statute votes lda    # subset
    python build_provenance.py --rebuild  # force re-fetch everything

The downstream `verify_anchors_occ.py --spot-check` mode reads these
provenance manifests to know which URL to re-fetch + which expected
hash to compare against.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DATA_OCC = ROOT / "data" / "occ"
CACHE_FD = ROOT / "_substrate_cache_occ" / "house_fd"

USER_AGENT = (
    "occ-khanna-complaint-provenance/1.0 "
    "(reviewer-side primary-source verification; contact: maintainer)"
)


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, encoding="utf-8"
        ).strip()
    except Exception:
        return "unknown-no-git"


def _sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _http_get_with_meta(
    url: str, *, timeout: int = 60
) -> tuple[bytes | None, dict, str | None]:
    """Fetch URL; return (body_or_None, meta_dict, error_or_None).

    meta_dict contains content_length, etag, last_modified, http_status,
    fetched_at_utc, server_header (when available).
    """
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )
    fetched_at = _dt.datetime.now(_dt.timezone.utc).isoformat()
    try:
        with urlopen(req, timeout=timeout) as r:
            body = r.read()
            headers = dict(r.headers.items())
            meta = {
                "fetched_at_utc": fetched_at,
                "http_status": r.getcode(),
                "content_length": len(body),
                "header_content_length": headers.get("Content-Length"),
                "header_content_type": headers.get("Content-Type"),
                "header_etag": headers.get("ETag"),
                "header_last_modified": headers.get("Last-Modified"),
                "header_server": headers.get("Server"),
                "header_date": headers.get("Date"),
            }
            return body, meta, None
    except HTTPError as e:
        return None, {
            "fetched_at_utc": fetched_at,
            "http_status": e.code,
            "error": f"HTTPError {e.code} {e.reason}",
        }, f"HTTPError {e.code} {e.reason}"
    except URLError as e:
        return None, {
            "fetched_at_utc": fetched_at,
            "error": f"URLError {e.reason}",
        }, f"URLError {e.reason}"
    except Exception as e:
        return None, {
            "fetched_at_utc": fetched_at,
            "error": f"{type(e).__name__} {e}",
        }, f"{type(e).__name__} {e}"


# ======================================================================
# Per-snapshot provenance generators
# ======================================================================

def _base_provenance(snapshot_path: Path, klass: str) -> dict:
    return {
        "$schema_version": "1",
        "snapshot_file": snapshot_path.name,
        "snapshot_sha256": _sha256_file(snapshot_path),
        "snapshot_size_bytes": snapshot_path.stat().st_size,
        "primary_source_class": klass,
        "fetch_script": "build_provenance.py",
        "fetch_script_git_sha": _git_sha(),
        "generated_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "primary_source_endpoints": [],
        "post_fetch_transformations": [],
        "gap_reason": None,
    }


# ----------------------------------------------------------------------
# Group 1: directly fetchable, deterministic public URLs
# ----------------------------------------------------------------------

def gen_statute_cites(skip_fetched: bool) -> dict:
    """Each statute_cites entry has source_url -> uscode.house.gov / ecfr.gov."""
    snap_path = DATA_OCC / "statute_cites_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "statute_text_uscode_ecfr")
    prov["primary_source_explanation"] = (
        "Each operative statute / regulation cite resolves against the "
        "authoritative full_text fetched from uscode.house.gov (USC) or "
        "ecfr.gov (CFR) at snapshot freeze time. The OCC body cites the "
        "section_label + full_text from this snapshot, NOT a memorized "
        "rendering. Spot-check: re-fetch each source_url, hash bytes, "
        "compare to fetched_sha256_raw_bytes here."
    )
    for entry in snap.get("entries", []):
        url = entry.get("source_url")
        if not url:
            continue
        ep = {
            "anchor_id": entry.get("marker"),
            "title": f"{entry.get('jurisdiction')} title {entry.get('title_number')} § {entry.get('section')}",
            "url": url,
        }
        # Attempt fetch
        body, meta, err = _http_get_with_meta(url, timeout=120)
        if body is not None:
            ep["fetched_sha256_raw_bytes"] = _sha256_bytes(body)
            ep["fetched_meta"] = meta
            ep["fetch_status"] = "OK"
        else:
            ep["fetch_status"] = "FAILED"
            ep["fetched_meta"] = meta
            ep["fetch_error"] = err
        prov["primary_source_endpoints"].append(ep)
        time.sleep(1.0)  # be polite to gov servers
    prov["post_fetch_transformations"] = [
        {
            "step": "html_to_text_normalize",
            "tool": "BeautifulSoup",
            "note": "uscode.house.gov returns XHTML; full_text in snapshot is the "
                    "section text extracted via DOM walk. Spot-check verifies "
                    "the raw HTML bytes; the text-normalization step is "
                    "auditable against the same source by inspecting the "
                    "snapshot's `full_text` field.",
        }
    ]
    return prov


def gen_khanna_votes(skip_fetched: bool) -> dict:
    """Each NDAA roll has clerk.house.gov XML at /evs/{year}/roll{NNN}.xml."""
    snap_path = DATA_OCC / "khanna_votes_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "house_clerk_rollcall_xml")
    prov["primary_source_explanation"] = (
        "Each NDAA roll-call vote derives from clerk.house.gov roll-call "
        "XML, deterministic by (vote_year, roll_number). The snapshot "
        "summarizes vote_position per roll; spot-check re-fetches the XML "
        "and hashes it."
    )
    rolls = snap.get("ndaa_cluster", {}).get("rolls", [])
    for r in rolls:
        roll_num = int(r["roll_number"])
        vote_year = r["vote_date"][:4]
        url = f"https://clerk.house.gov/evs/{vote_year}/roll{roll_num:03d}.xml"
        ep = {
            "title": f"Roll {roll_num:03d}/{vote_year} ({r['bill_reference']} — {r['vote_question']})",
            "url": url,
            "expected_position": r.get("vote_position"),
        }
        body, meta, err = _http_get_with_meta(url, timeout=60)
        if body is not None:
            ep["fetched_sha256_raw_bytes"] = _sha256_bytes(body)
            ep["fetched_meta"] = meta
            ep["fetch_status"] = "OK"
        else:
            ep["fetch_status"] = "FAILED"
            ep["fetched_meta"] = meta
            ep["fetch_error"] = err
        prov["primary_source_endpoints"].append(ep)
        time.sleep(0.8)
    return prov


def gen_lda_khanna(skip_fetched: bool) -> dict:
    """LDA Senate disclosure API for Khanna recipient variants."""
    snap_path = DATA_OCC / "lda_khanna_contributions_2026_05_02.json"
    prov = _base_provenance(snap_path, "lda_senate_disclosure_api")
    prov["primary_source_explanation"] = (
        "LDA Senate disclosure XML / JSON API at lda.senate.gov. Snapshot "
        "filters to filings whose contribution_items text contains 'khanna' "
        "OR 'c00503185' (Ro for Congress committee). Spot-check API "
        "endpoint may return drift due to ongoing filing accrual; "
        "snapshot is bundled-frozen at 2026-05-02."
    )
    # The LDA API endpoint pattern (one of the variants the snapshot tested)
    queries = [
        ("filings_by_contribution_payee_kw_khanna",
         "https://lda.senate.gov/api/v1/filings/?contribution_payee_keyword=khanna&page_size=100"),
        ("contributions_by_payee_kw_khanna",
         "https://lda.senate.gov/api/v1/contributions/?contribution_payee_keyword=khanna&page_size=100"),
    ]
    for label, url in queries:
        ep = {"title": label, "url": url}
        body, meta, err = _http_get_with_meta(url, timeout=120)
        if body is not None:
            ep["fetched_sha256_raw_bytes"] = _sha256_bytes(body)
            ep["fetched_meta"] = meta
            ep["fetch_status"] = "OK"
            try:
                # capture API response count (likely > snapshot due to accrual)
                obj = json.loads(body)
                ep["api_response_count"] = obj.get("count")
            except Exception:
                pass
        else:
            ep["fetch_status"] = "FAILED"
            ep["fetched_meta"] = meta
            ep["fetch_error"] = err
        prov["primary_source_endpoints"].append(ep)
        time.sleep(1.5)  # LDA API is rate-limited
    prov["expected_drift_class"] = "PASS_WITH_DEFECT_substrate_count_drift"
    prov["expected_drift_explanation"] = (
        "LDA API count likely exceeds snapshot count by 0-5% due to ongoing "
        "filing accrual since 2026-05-02 freeze. This is benign drift, NOT "
        "a tamper signal. Spot-check classifies as PASS_WITH_DEFECT when "
        "delta < 5% AND snapshot rows are a subset of live response."
    )
    return prov


# ----------------------------------------------------------------------
# Group 2: PDF-derived snapshots (PTR + PFD via clerk.house.gov)
# ----------------------------------------------------------------------

def _khanna_filings_index() -> list[dict]:
    """Load the cached FD index of all Khanna filings.

    The cached TSV header has 12 cols (with two phantom cols `Filing Year` +
    `DisclosureType` not populated in data rows). Data rows have 10 cols.
    Use position-based access: data[0]=DisclosureYear data[5]=FilingType
    data[8]=FilingDate data[9]=DocID.
    """
    p = CACHE_FD / "khanna_fd_index_all_years.tsv"
    if not p.exists():
        return []
    rows = []
    lines = p.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        return []
    for ln in lines[1:]:
        cols = ln.split("\t")
        if len(cols) < 10:
            continue
        rows.append({
            "DisclosureYear": cols[0],
            "Last": cols[2],
            "First": cols[3],
            "FilingType": cols[5],
            "StateDst": cols[6],
            "Year": cols[7],
            "FilingDate": cols[8],
            "DocID": cols[9],
        })
    return rows


def _ptr_url(filing_year: str, doc_id: str) -> str:
    return f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{filing_year}/{doc_id}.pdf"


def _pfd_url(filing_year: str, doc_id: str) -> str:
    return f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{filing_year}/{doc_id}.pdf"


def gen_khanna_ptr_transactions(skip_fetched: bool) -> dict:
    """Each Khanna PTR doc_id resolves to a clerk.house.gov PDF.

    Snapshot has 114 unique doc_ids. Provenance fetches each PDF, computes
    raw-bytes SHA256, captures HTTP metadata.
    """
    snap_path = DATA_OCC / "khanna_ptr_transactions_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "house_clerk_ptr_pdf")
    prov["primary_source_explanation"] = (
        "Each row in the snapshot is a structured transaction extracted via "
        "Gemini per-page OCR from a House Clerk PTR PDF. Provenance lists "
        "every unique doc_id with its public clerk.house.gov URL + raw-bytes "
        "SHA256 at fetch time. Spot-check re-fetches the PDF and compares "
        "bytes; Tier-E re-OCRs the PDF and compares structured rows."
    )
    # The PTR snapshot has filing_index (114 entries with doc_id +
    # filing_year + filing_date). Use that directly.
    pairs = set()
    for r in snap.get("filing_index", []):
        if not isinstance(r, dict):
            continue
        did = r.get("doc_id")
        fy = r.get("filing_year")
        if did and fy:
            pairs.add((str(fy), str(did)))
    prov["unique_doc_count"] = len(pairs)
    print(f"  PTR provenance: {len(pairs)} unique doc_ids to fetch")
    n_ok = n_fail = 0
    for fy, did in sorted(pairs):
        url = _ptr_url(fy, did)
        ep = {"doc_id": did, "filing_year": fy, "url": url}
        body, meta, err = _http_get_with_meta(url, timeout=120)
        if body is not None:
            ep["fetched_sha256_raw_bytes"] = _sha256_bytes(body)
            ep["fetched_meta"] = meta
            ep["fetch_status"] = "OK"
            n_ok += 1
        else:
            ep["fetch_status"] = "FAILED"
            ep["fetched_meta"] = meta
            ep["fetch_error"] = err
            n_fail += 1
        prov["primary_source_endpoints"].append(ep)
        # Print progress every 10 PDFs so the run is visible
        if (n_ok + n_fail) % 10 == 0:
            print(f"    {n_ok+n_fail}/{len(pairs)}: ok={n_ok} fail={n_fail}")
        time.sleep(0.4)  # be polite to clerk.house.gov
    prov["post_fetch_transformations"] = [
        {"step": "render_pdf_pages", "tool": "pymupdf", "dpi": 200},
        {
            "step": "extract_per_page",
            "tool": "gemini_per_page_extract",
            "model": "gemini-3.1-flash-lite-preview",
            "ref": "src.gemini_per_page_extract.extract_per_page (hhs_doge)",
            "note": "Per-page Gemini extraction; outputs structured tx rows. "
                    "Bundled output at _substrate_cache_occ/chamber_gemini_extract/.",
        },
        {
            "step": "canonical_view_dedup",
            "tool": "lake.house_ptr_transactions_canonical SQL",
            "ref": "scripts/k_ptr_canonical_views.py",
            "note": "tx-key (filer_identity, asset_name, tx_date, tx_type, owner) "
                    "collapses amendment-cascade re-filings into one row anchored "
                    "at earliest_filing_date. Required for STOCK Act §6 days-late "
                    "computation per stock-act-audit.md.",
        },
    ]
    print(f"  PTR provenance final: {n_ok}/{len(pairs)} fetched OK, {n_fail} failed")
    return prov


def gen_khanna_pfd_schedule_d(skip_fetched: bool) -> dict:
    """PFD Schedule D rows derive from per-year Khanna PFD PDFs."""
    snap_path = DATA_OCC / "khanna_pfd_schedule_d_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "house_clerk_pfd_pdf")
    prov["primary_source_explanation"] = (
        "PFD Schedule D liability rows derive from Khanna's per-year annual "
        "PFD PDFs (FilingType='O' in House Clerk FD index). The snapshot "
        "enumerates 13 liability rows across TY2016-TY2019. Provenance "
        "lists the PFDs sourced + clerk.house.gov URLs + raw-bytes SHA256."
    )
    # Use cached FD index to find Khanna's PFDs
    filings = _khanna_filings_index()
    pfds = [f for f in filings if f.get("FilingType") == "O"]
    print(f"  PFD provenance: {len(pfds)} PFDs in FD index")
    n_ok = n_fail = 0
    for f in pfds:
        did = f.get("DocID", "").strip()
        fy = f.get("DisclosureYear", "").strip()
        if not did or not fy:
            continue
        url = _pfd_url(fy, did)
        ep = {
            "doc_id": did,
            "filing_year": fy,
            "filing_date": f.get("FilingDate"),
            "url": url,
        }
        body, meta, err = _http_get_with_meta(url, timeout=120)
        if body is not None:
            ep["fetched_sha256_raw_bytes"] = _sha256_bytes(body)
            ep["fetched_meta"] = meta
            ep["fetch_status"] = "OK"
            n_ok += 1
        else:
            ep["fetch_status"] = "FAILED"
            ep["fetched_meta"] = meta
            ep["fetch_error"] = err
            n_fail += 1
        prov["primary_source_endpoints"].append(ep)
        time.sleep(0.4)
    prov["post_fetch_transformations"] = [
        {"step": "tesseract_ocr", "tool": "tesseract", "ref": "khanna_pfd_8221318_OCR.txt example"},
        {
            "step": "schedule_d_row_extraction",
            "tool": "manual_structured_extract",
            "note": "Schedule D rows extracted from PFD PDFs into "
                    "lake.house_pfd_schedule_d_liabilities. Snapshot is a "
                    "WHERE filer='Khanna' projection.",
        },
    ]
    print(f"  PFD provenance final: {n_ok}/{len(pfds)} fetched OK, {n_fail} failed")
    return prov


# ----------------------------------------------------------------------
# Group 3: Cloudflare-blocked (Ahuja 990-PF) — mirror to release
# ----------------------------------------------------------------------

def gen_ahuja_990pf(skip_fetched: bool) -> dict:
    """ProPublica 990-PF PDFs are Cloudflare-protected; mirror to release."""
    snap_path = DATA_OCC / "ahuja_foundation_990pf_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "irs_990pf_via_propublica_cloudflare")
    prov["primary_source_explanation"] = (
        "Ahuja Foundation IRS 990-PF filings (EIN 341685088) are filed "
        "annually with the IRS. Three primary-source paths exist: "
        "(1) ProPublica nonprofits API at projects.propublica.org "
        "(Cloudflare-protected — requires headless browser to bypass); "
        "(2) IRS direct at apps.irs.gov (browser-rendered JavaScript); "
        "(3) IRS bulk e-file index on AWS S3 (raw XML, no PDFs). "
        "MITIGATION: The 8 cited 990-PF PDFs are mirrored as separate "
        "GitHub Release assets (AHUJA_990PF_<year>.pdf). Spot-check + "
        "Tier-E pull from the release mirror, NOT ProPublica directly. "
        "Reviewer can independently cross-verify by fetching from "
        "apps.irs.gov in a browser."
    )
    prov["gap_reason"] = "primary_source_cloudflare_blocked_mirrored_to_release"
    # The snapshot's irs_990_returns list has tax_year + org_name; we'll
    # populate URL placeholders for the release-mirror assets.
    for r in snap.get("irs_990_returns", []):
        ty = r.get("tax_year")
        if not ty:
            continue
        ep = {
            "tax_year": str(ty),
            "release_mirror_asset": f"AHUJA_990PF_{ty}.pdf",
            "release_mirror_url": f"https://github.com/kevinnbass/political/releases/download/v2-occ-2026-05-04/AHUJA_990PF_{ty}.pdf",
            "primary_source_url_propublica": (
                f"https://projects.propublica.org/nonprofits/organizations/341685088"
            ),
            "primary_source_url_irs_direct": (
                "https://apps.irs.gov/app/eos/displayAll.do?dispatchMethod="
                "displayAllInfo&Id=2287614&ein=341685088"
            ),
            "fetch_status": "PENDING_RELEASE_MIRROR_UPLOAD",
        }
        prov["primary_source_endpoints"].append(ep)
    prov["post_fetch_transformations"] = [
        {
            "step": "990pf_xml_extraction",
            "tool": "irs_990_etl",
            "note": "990-PF returns ETL'd into lake.irs_990_returns + "
                    "lake.irs_990_officers + lake.irs_990_pf_noncash_donations. "
                    "Snapshot is the WHERE ein='341685088' projection.",
        },
    ]
    return prov


# ----------------------------------------------------------------------
# Group 4: Vendor-relayed (yfinance) — permanent gap
# ----------------------------------------------------------------------

def gen_khanna_ohlc(skip_fetched: bool) -> dict:
    snap_path = DATA_OCC / "khanna_ohlc_2026_05_02.json"
    prov = _base_provenance(snap_path, "vendor_relayed_no_primary_url")
    prov["primary_source_explanation"] = (
        "Daily close OHLC prices for 42 in-scope tickers + SPY benchmark, "
        "snapshotted at 2026-05-02 via yfinance into ro_khanna.daily_ohlc. "
        "yfinance aggregates Yahoo Finance feeds, which themselves source "
        "from exchange tape feeds via vendor relays. There is NO "
        "deterministic public URL that returns identical bytes across "
        "fetches: prices are split-adjusted retroactively, dividend-"
        "adjusted retroactively, and reflect Yahoo's vendor cleansing "
        "rules. This is a STRUCTURAL primary-source gap."
    )
    prov["gap_reason"] = "vendor_relayed_no_deterministic_primary_url"
    prov["mitigation"] = (
        "(1) The bundled OHLC snapshot is the authoritative source for "
        "this package and its SHA256 is committed to 99_SHA256SUMS.txt + "
        "OpenTimestamped at publication. (2) The body's SPY benchmark "
        "+ sector ETF baselines are computed against the same snapshot, "
        "so internal consistency is preserved. (3) Reviewers who want "
        "deeper verification can independently pull yfinance for the "
        "same tickers + date range and accept that absolute prices may "
        "drift due to vendor split-adjustment rebases; relative ordering "
        "+ window concentration ratios should remain stable to within "
        "~5%."
    )
    prov["primary_source_endpoints"] = []
    return prov


# ----------------------------------------------------------------------
# Group 5: Lake-derived SQL (chain-of-custody only)
# ----------------------------------------------------------------------

def _gen_lake_derived(snap_name: str, klass: str, sql_note: str,
                      script_ref: str | None = None) -> dict:
    snap_path = DATA_OCC / snap_name
    prov = _base_provenance(snap_path, klass)
    prov["primary_source_explanation"] = (
        "This snapshot is the projection of a SQL aggregate query against "
        "the lake. There is no single primary URL because the underlying "
        "rows derive from many primary documents (per-Member PTRs across "
        "the chamber, etc.) ETL'd into lake.* tables. Chain-of-custody: "
        + sql_note
    )
    prov["gap_reason"] = "lake_derived_sql_no_single_primary_url"
    prov["mitigation"] = (
        "Reviewer with lake access can re-run the producing SQL "
        "(documented in fetch_script_ref). Tier-F users without lake "
        "access can opt into the Gemini per-page chamber-wide rebuild "
        "(see rebuild_chamber_audit.py --full-chamber --cost-acknowledged; "
        "$50-200 reviewer Gemini spend). For PTR-row-level grain, the "
        "bundled khanna_ptr_transactions snapshot CAN be re-derived from "
        "primary PDFs at Tier-E with no lake access."
    )
    if script_ref:
        prov["fetch_script_ref"] = script_ref
    return prov


def gen_house_chamber_audit(skip_fetched: bool) -> dict:
    return _gen_lake_derived(
        "house_chamber_audit_2026_05_02.json",
        "lake_derived_chamber_aggregate",
        sql_note=(
            "SELECT * FROM public.house_ptr_chamber_audit_by_member "
            "(411-row Member-grain rollup of public.house_ptr_chamber_audit; "
            "rebuild via scripts/k_house_ptr_chamber_late_filing_audit.py)."
        ),
        script_ref="scripts/k_house_ptr_chamber_late_filing_audit.py",
    )


def gen_ptr_filing_audit_khanna(skip_fetched: bool) -> dict:
    return _gen_lake_derived(
        "ptr_filing_audit_khanna_2026_05_02.json",
        "lake_derived_canonical_view_aggregate",
        sql_note=(
            "Khanna-only projection of post-canonical-view-dedup chamber audit. "
            "Source: public.house_ptr_chamber_audit_by_member WHERE last='Khanna' "
            "AND state_dst='CA17'. Canonical view amendment-cascade dedup "
            "applied per stock-act-audit.md §Amendment cascade."
        ),
        script_ref="scripts/k_house_ptr_chamber_late_filing_audit.py",
    )


def gen_peer_baseline_percentiles(skip_fetched: bool) -> dict:
    return _gen_lake_derived(
        "peer_baseline_percentiles_2026_05_02.json",
        "lake_derived_peer_cohort_percentiles",
        sql_note=(
            "SELECT * FROM ro_khanna.peer_baseline_percentiles. The peer-46 "
            "cohort (10 Tier-1 HASC + 40 top-PTR-filers) is curated in "
            "ro_khanna.peer_baseline; per-metric percentiles computed via "
            "scripts/k_house_ptr_amount_weighted_audit.py + sibling scripts."
        ),
        script_ref="scripts/k_house_ptr_amount_weighted_audit.py",
    )


def gen_v3_facts_substrate_class(skip_fetched: bool) -> dict:
    return _gen_lake_derived(
        "v3_facts_substrate_class_2026_05_03.json",
        "lake_derived_v3_facts_export",
        sql_note=(
            "SELECT * FROM ro_khanna.v3_facts WHERE fact_id IN (set referenced "
            "by the 66 OCC manifest entries). Each v3_fact carries its OWN "
            "provenance (query_sql + citations + entity links + theory links) "
            "via the v3 contract documented in .claude/rules/v3-facts.md. "
            "This snapshot is a one-time dump of those facts at 2026-05-02."
        ),
        script_ref=".claude/rules/v3-facts.md (v3 contract)",
    )


def gen_trade_pnl_facts(skip_fetched: bool) -> dict:
    return _gen_lake_derived(
        "trade_pnl_facts_2026_05_02.json",
        "lake_derived_v3_facts_subset",
        sql_note=(
            "F225/F242/F820/F833 trade-PnL canonical scalars from ro_khanna.v3_facts. "
            "F225 was re-canonized 2026-05-04 to the post-cascade rebuild value "
            "($61,040,313.07) against the bundled khanna_ptr_transactions + "
            "khanna_ohlc + khanna_window_events snapshots — those three snapshots "
            "ARE the primary substrate for F225 and have their own provenance.json "
            "files. This snapshot is the canonical-scalars projection."
        ),
        script_ref="data/ocr_products/rebuild_trade_pnl_khanna.py",
    )


# ----------------------------------------------------------------------
# Group 6: Composite primary sources
# ----------------------------------------------------------------------

def gen_khanna_window_events(skip_fetched: bool) -> dict:
    """Composite of NDAA dates (constants) + 8-K events (SEC EDGAR) + USAspending contracts."""
    snap_path = DATA_OCC / "khanna_window_events_2026_05_02.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    prov = _base_provenance(snap_path, "composite_window_events")
    prov["primary_source_explanation"] = (
        "Window events are a composite of three primary-source classes: "
        "(a) NDAA enactment dates — congressional record / Public Law numbers, "
        "deterministic public list. (b) CMS rulemaking dates — Federal Register "
        "publication dates, deterministic public list. (c) Same-day 8-K events — "
        "SEC EDGAR submissions JSON API, deterministic per-CIK. (d) USAspending "
        "contract action dates — usaspending.gov bulk CSV / API, deterministic "
        "by recipient_name + action_date. Provenance documents each source "
        "class; spot-check re-fetches the constituent date sets and verifies "
        "the bundled lists are subsets."
    )
    # NDAA dates are constants — document them inline
    prov["primary_source_endpoints"].append({
        "title": "NDAA enactment dates 2017-2025",
        "url": "https://www.congress.gov/public-laws/115th-congress (FY2018 NDAA P.L. 115-91), etc.",
        "kind": "constants_list",
        "ndaa_dates_count": len(snap.get("ndaa_dates", [])),
        "ndaa_window_days": snap.get("ndaa_window_days"),
        "fetch_status": "DOCUMENTED_AS_CONSTANTS",
    })
    prov["primary_source_endpoints"].append({
        "title": "CMS rulemaking dates 2017-2024",
        "url": "https://www.federalregister.gov/agencies/centers-for-medicare-medicaid-services",
        "kind": "constants_list",
        "cms_dates_count": len(snap.get("cms_dates", [])),
        "cms_window_days": snap.get("cms_window_days"),
        "fetch_status": "DOCUMENTED_AS_CONSTANTS",
    })
    prov["primary_source_endpoints"].append({
        "title": "Same-day 8-K events (per-ticker)",
        "url": "https://data.sec.gov/submissions/CIK{cik:0>10}.json",
        "kind": "sec_edgar_submissions_api",
        "n_8k_events": snap.get("n_8k_events"),
        "fetch_status": "DETERMINISTIC_DEFERRED_TO_SPOT_CHECK",
        "note": "SEC EDGAR submissions JSON API is rate-limited at 10 req/s. "
                "Tier-D spot-check fetches per-ticker submissions JSON + "
                "filters to 8-K filings, hashes the filtered set.",
    })
    prov["primary_source_endpoints"].append({
        "title": "USAspending contract action dates (per-ticker)",
        "url": "https://api.usaspending.gov/api/v2/search/spending_by_award/",
        "kind": "usaspending_api",
        "n_contract_events": snap.get("n_contract_events"),
        "n_contract_tickers": len(snap.get("contract_tickers", [])),
        "fetch_status": "DETERMINISTIC_DEFERRED_TO_SPOT_CHECK",
    })
    return prov


# ======================================================================
# Driver
# ======================================================================

GENERATORS = {
    "statute_cites": gen_statute_cites,
    "khanna_votes": gen_khanna_votes,
    "lda_khanna_contributions": gen_lda_khanna,
    "khanna_ptr_transactions": gen_khanna_ptr_transactions,
    "khanna_pfd_schedule_d": gen_khanna_pfd_schedule_d,
    "ahuja_foundation_990pf": gen_ahuja_990pf,
    "khanna_ohlc": gen_khanna_ohlc,
    "house_chamber_audit": gen_house_chamber_audit,
    "ptr_filing_audit_khanna": gen_ptr_filing_audit_khanna,
    "peer_baseline_percentiles": gen_peer_baseline_percentiles,
    "v3_facts_substrate_class": gen_v3_facts_substrate_class,
    "trade_pnl_facts": gen_trade_pnl_facts,
    "khanna_window_events": gen_khanna_window_events,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--classes", nargs="*",
        help="Subset of snapshot stems to generate provenance for. Default: all.",
    )
    parser.add_argument(
        "--rebuild", action="store_true",
        help="Force re-fetch even if provenance.json already exists.",
    )
    args = parser.parse_args()

    targets = args.classes or list(GENERATORS.keys())
    unknown = [t for t in targets if t not in GENERATORS]
    if unknown:
        print(f"Unknown classes: {unknown}", file=sys.stderr)
        print(f"Available: {sorted(GENERATORS.keys())}", file=sys.stderr)
        return 2

    for stem in targets:
        candidates = [
            DATA_OCC / f"{stem}_2026_05_02.json",
            DATA_OCC / f"{stem}_2026_05_03.json",
        ]
        snap_path = next((c for c in candidates if c.exists()), None)
        if snap_path is None:
            print(f"  [{stem}] SNAPSHOT NOT FOUND")
            continue
        prov_path = snap_path.with_suffix(".provenance.json")
        if prov_path.exists() and not args.rebuild:
            print(f"  [{stem}] provenance.json exists; skip (use --rebuild to overwrite)")
            continue
        print(f"\n=== {stem} ===")
        prov = GENERATORS[stem](skip_fetched=False)
        prov_path.write_text(
            json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  -> {prov_path.name} ({prov_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
