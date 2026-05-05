# OCR work products — bundled with the OCC complaint

This directory carries the OCR / structured-extraction work products that
underlie the OCC complaint's substantive PFD-derived and PTR-derived claims.
The House Clerk publishes Periodic Transaction Reports (PTRs) and Personal
Financial Disclosures (PFDs) at
`https://disclosures-clerk.house.gov/public_disc/` as **PDFs only** — there
is no machine-readable bulk export of per-transaction Schedule A rows or
per-liability Schedule D rows. Every researcher that wants the rows must run
OCR + structured extraction on each PDF, which produces non-deterministic
output (different OCR / extraction pipelines yield materially different
parses, particularly on the multi-column Schedule A asset table and the
Schedule D liability rows).

The Federal Election Commission's bulk Schedule A / Schedule E feeds are
different — they ARE published in machine-readable CSV/TSV form and can be
re-fetched directly via `../../fetch_substrate_occ.py --classes fec_api`.
**The files in this directory are the OCR / structured-extraction work
products on which the OCC complaint's PFD-derived and PTR-derived claims
rely** — the FEC, IRS 990, statute, and roll-call substrates do not require
OCR work products and are reproducible directly via `fetch_substrate_occ.py`.

## What's here

| File | Marker(s) | Body section | Source PDF | Source URL |
|---|---|---|---|---|
| `khanna_pfd_8221318_OCR.txt` | `OCC_M005` (PFD operative-text quotation) + supports `OCC_M028` / `OCC_M058` (Goldman SP margin scaffold cross-check) | §III.7 + §III.6 | doc_id 8221318 — Khanna TY2024 PFD | `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024/8221318.pdf` |
| `khanna_pfd_8221318_P0[1-5].png` | (renders supporting `OCC_M005`) | §III.7 page-citation | doc_id 8221318 (5-page render) | (same as above) |
| `khanna_pfd_schedule_a_assets.csv` | `OCC_M057` (Khanna PFD Schedule A asset enumeration; primary anchor for the asset-class composition + holding-period framing) | §III.6 + §III.7 | doc_ids 8220039 / 8220067 / 8220674 / 8221124 / 8221231 / 8221318 (TY2014–TY2023) | per-doc URLs at `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf` |
| `khanna_ptr_corpus.json` | corpus index for `OCC_M013` / `OCC_M014` (late-filing audit + per-tx framing) | Counts 1-3 + 6 + 7 | 114 PTR PDFs 2017-2026 | per-doc URLs at `https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf` |
| `khanna_ptrs/<doc_id>/<doc_id>_OCR.txt` | per-page Gemini OCR transcription of every cited PTR (114 docs / 1,787 pages) | Counts 1-3 + 6 + 7 (grep / browse aid) | same 114 PTRs as `khanna_ptr_corpus.json` | per-doc URLs at `https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf` |
| `khanna_ptrs/<doc_id>/<doc_id>_OCR.json` | per-page extractor metadata (model, tokens, served_by, errors, garble flags) for the same 114 docs | reproducibility audit | (same as above) | (same as above) |
| `rebuild_ptr_audit_khanna.py` | regenerates `ptr_filing_audit_khanna_REBUILT.json` (B-F1) | Counts 1-3 + 6 + 7 reviewer cookie-cutter | (rebuilds from `../occ/khanna_ptr_transactions_2026_05_02.json`) | n/a (stdlib-only Python; no fetch) |
| `rebuild_pfd_schedule_d_khanna.py` | regenerates `pfd_schedule_d_khanna_REBUILT.json` (B-F2) | Count 3 + Count 7 (TY2017 $1M+ Goldman SP single-line anchor) | (rebuilds from `../occ/khanna_pfd_schedule_d_2026_05_02.json`) | n/a (stdlib-only Python; no fetch) |
| `rebuild_trade_pnl_khanna.py` | regenerates `trade_pnl_facts_REBUILT.json` (B-F3) | Count 1 §IV ¶69 (sector-level alpha + window-attribution) | (rebuilds from `../occ/khanna_ptr_transactions_2026_05_02.json` + `../occ/khanna_ohlc_2026_05_02.json` + `../occ/khanna_window_events_2026_05_02.json`) | n/a (stdlib-only Python; no fetch, no yfinance) |

The structured per-PTR-row data driving the late-filing audit lives in the
**frozen snapshot** at `../occ/ptr_filing_audit_khanna_2026_05_02.json` (the
verifier kit reads from there). The PTR corpus index in
`khanna_ptr_corpus.json` is the per-PDF source-URL list, used by
`fetch_source_pdfs.py` to re-download every cited PDF.

## Why these are bundled rather than fetched on demand

For PDF-OCR substrates the bundled work product IS the canonical figure
relied on in the complaint body. A reviewer's independent re-extraction is
offered as a cross-check, not a primary verification path. The kit's anchor
checks for PFD/PTR-derived markers use the bundled JSON (frozen-mode) or
re-derive against the lake (live-mode).

`fetch_source_pdfs.py` exists for the case where a reviewer wants to run
their own OCR + extraction pipeline against the source PDFs and compare to
the bundled work products.

## Independent reproducibility path (re-OCR from source PDFs)

A reviewer who wants to independently re-derive the rows in either file
should:

1. Run `python fetch_source_pdfs.py` in this directory. Default mode fetches
   the 1 cited PFD (doc_id 8221318) only (~3 MB). Pass `--include-ptr-corpus`
   to also fetch all 114 cited Khanna PTR PDFs (~30-50 MB total). Pass
   `--render-pages` to additionally render every fetched PDF to one 300-DPI
   PNG per page under `khanna_pfd_renders/` (and `khanna_ptr_renders/` if
   `--include-ptr-corpus` is also passed) — this gives a one-command path
   to PDFs + per-page renders ready for grep, browse, or OCR re-derivation
   with any engine. Page-render output is BIT-EXACT idempotent across
   re-runs and matches the bundled `khanna_pfd_8221318_P0[1-5].png`
   reference renders 0-byte delta on all 5 pages.
2. Run their own OCR + extraction pipeline against the cached PDFs (or
   directly against the per-page PNGs if `--render-pages` was used). Two
   suggested approaches:
   - **Tesseract** + table-detection (open-source, deterministic but lower
     extraction quality on multi-column PFD/PTR tables; this is what
     produced `khanna_pfd_8221318_OCR.txt`).
   - **Gemini / Claude / GPT-4** with a per-page extraction prompt
     similar to the campaign's (see
     `../../REPRODUCIBILITY_METHODOLOGY_OCC.md` §3 for prompt structure).
3. Compare their extraction against the bundled JSON / CSV / OCR text.
   Material differences in any per-row field flag for follow-up; structural
   agreement on the row inventory + per-row dollar-range buckets +
   transaction dates is the load-bearing reproducibility check.

### Reviewer one-command (full kit, no spend)

```bash
pip install requests pymupdf
python fetch_source_pdfs.py --include-ptr-corpus --render-pages
# → ~30-50 MB of PDFs + ~150-400 MB of 300-DPI per-page PNGs
# → directly browseable, greppable, and ready for any independent OCR engine
```

The `--render-pages` flag uses the same PyMuPDF pipeline (`fitz.open` →
`page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))` → `tobytes("png")`)
that produced the bundled `khanna_pfd_8221318_P0[1-5].png` reference
renders, so reviewer-side renders are BIT-EXACT to the bundled ones (0-byte
delta confirmed at the time this kit shipped).

## Provenance and re-derivation chain for the PFD anchor `OCC_M005`

The PFD operative-text quotation in OCC §III.7 cites doc_id 8221318
(Khanna's TY2024 PFD). The bundled OCR text was produced via:

1. PDF download from
   `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024/8221318.pdf`
2. Page-by-page render to PNG at 300 DPI (5 pages → 5 PNGs).
3. Tesseract OCR on each page (baseline open-source extraction).
4. Manual cross-check of the operative-text quotation against the PFD's
   Schedule A "broker statement" line as it appears on page 5 of the OCR.

A reviewer running an independent extraction should expect material
agreement on the operative-text quotation and on the asset enumeration in
`khanna_pfd_schedule_a_assets.csv`. Structural variance on the asset
sub-line breakdown is normal across OCR pipelines; the load-bearing claim
is the operative-text quotation, which is page-stable.

## Bundled PTR OCR text (`khanna_ptrs/`, B-D2.b)

Bundled 2026-05-03 via the canonical campaign per-page extractor at
`hhs_doge/src/gemini_per_page_extract.extract_per_page` against all 114
cited Khanna PTR PDFs. Output structure:

    khanna_ptrs/
        <doc_id>/
            <doc_id>_OCR.txt    # page-delimited transcribed text
            <doc_id>_OCR.json   # per-page extractor metadata + token + error log

Each `_OCR.txt` opens with a header block (doc_id / year / source URL /
total_pages / engine / token totals / produced timestamp) and then emits
one section per page delimited by `--- PAGE NN ---`. Lines within each page
preserve reading order to the extent the model could recover from the
scanned multi-column layout.

**Engine match**: the bundle uses `gemini-3.1-flash-lite-preview` — the
same model that produced the structured-tx JSON at
`../occ/ptr_filing_audit_khanna_2026_05_02.json`. This means a reviewer
diffing this OCR text against the structured-tx JSON sees the engine's
own internal text, not a competing engine's parse, eliminating
engine-class noise from the comparison. The structured rows remain the
load-bearing artifact (the late-filing audit reads from the JSON, not
the text); the text bundle exists for grep / browse / page-citation
navigation and as an engine-matched cross-check.

**Re-derivation**: a reviewer can re-run the bundle by setting
`GEMINI_API_KEY` and invoking
`scripts/k_ro_khanna_occ_d2b_bundle_ptr_ocr.py` from the source-side
codebase. Idempotent — re-runs skip docs whose `_OCR.txt` is already
present and non-trivial. Total spend on the original run was ~$2.47 at
Flash Lite published rates (1,787 pages, 0 failures, 3.9M input + 5.2M
output tokens).

**Independent-engine cross-check**: a reviewer who wants to verify
against a non-Gemini engine should fetch the source PDFs via
`fetch_source_pdfs.py --include-ptr-corpus --render-pages` and run their
preferred OCR engine over the per-page renders. Material disagreement on
the structured-tx fields (transaction date / asset name / amount range /
owner code) is the load-bearing reproducibility check; small per-line
variance in the transcribed text is normal across engines.

## Provenance and re-derivation chain for the PTR corpus

The 114 Khanna PTR PDFs underpin the late-filing audit (Count 1) and every
per-tx claim cited in Counts 2 / 3 / 6 / 7. The structured per-tx rows
driving the audit are in the lake at `lake.house_ptr_transactions_canonical`
(post-amendment-cascade dedup; see
`../../REPRODUCIBILITY_METHODOLOGY_OCC.md` §1 for the canonical-view
discipline) and frozen for cold-start at
`../occ/ptr_filing_audit_khanna_2026_05_02.json`.

A reviewer who wants to re-derive the late-filing audit independently:

1. Fetch all 114 PTR PDFs via `fetch_source_pdfs.py --include-ptr-corpus`.
2. Run OCR + structured extraction (Gemini per-page is what the campaign
   used; per-page is mandatory for PDFs ≥50pp per
   `.claude/rules/core-infrastructure.md` of the source-side codebase, but
   most Khanna PTRs are <10pp).
3. Apply the canonical-view dedup rule (per
   `REPRODUCIBILITY_METHODOLOGY_OCC.md` §1.4): tx-key
   `(filer_identity, asset_name, transaction_date, transaction_type,
   COALESCE(owner,''))`; canonical row carries `earliest_filing_uuid`,
   `earliest_filing_date` (drives `days_late`), `amount_range` from the
   LATEST filing.
4. Compute `days_late = GREATEST(0, earliest_filing_date - LEAST(notification_date + 30 days, transaction_date + 45 days))`.
5. Aggregate to per-Member rate + per-tx severity. Expect material
   agreement on the canonical scalars: late_rate_pct=1.74,
   worst_days_late=358 (HUMANA SP-owned), n_late_tx=22, n_tx_total=624.

The frozen snapshot embeds those scalars; the verifier kit reads from there.

## Provenance and re-derivation chain for the trade-PnL anchors (B-F3)

The Khanna household terminal P&L canonical scalar **F225 = $61.04M mid**
(low $14.62M / high $107.46M) underpins Count 1 §IV ¶69's sector-level
alpha-attribution narrative. The rebuild script reproduces this scalar in
pure stdlib Python from three bundled snapshots:

* `../occ/khanna_ptr_transactions_2026_05_02.json` — 36,277 raw PTR rows
  (B-F1 substrate; same source file F1's audit rebuild reads).
* `../occ/khanna_ohlc_2026_05_02.json` — daily close prices for 42 in-scope
  tickers (Defense Primes / Defense Tech / Big Tech / Pharma / Healthcare
  Devices / Healthcare Services / Crypto + SPY benchmark) over 2017-01-03
  through 2026-04-16. Pulled from yfinance into `ro_khanna.daily_ohlc` at
  the time of F225 derivation; bundled here so the rebuild is isolated from
  yfinance retroactive split-adjustment / dividend-reconvention drift.
* `../occ/khanna_window_events_2026_05_02.json` — per-ticker event date
  sets for the four window-attribution paths: NDAA (8 dates as constants
  in `scripts/k_ro_khanna_s8b_05_tag_windows.py`); CMS (14 dates same);
  per-ticker SEC 8-K filing dates from `lake.sec_8k_filing_index` (6,620
  dates across 41 tickers); per-ticker USAspending contract action dates
  from `lake.usaspending_contracts_{2017..2026}` (29,516 dates across 17
  defense + tech tickers).

A reviewer who wants to re-derive the trade-PnL anchors independently:

1. Run `python rebuild_trade_pnl_khanna.py` in this directory. ~10-30s on
   stdlib-only Python (no yfinance, no lake, no API keys).
2. Compare output `trade_pnl_facts_REBUILT.json` against
   `../occ/trade_pnl_facts_2026_05_02.json` `load_bearing_invariants`
   block. Expected outcome: F225 mid bit-exact at
   $61.04M (re-canonized 2026-05-04 against the bundled 2026-05-02 substrate
   snapshot per amendment-cascade dedup discipline + post-derivation USAspending
   substrate-grow — see verifier kit's diff report `drift_notes` for the
   structural attribution per `.claude/rules/stock-act-audit.md`
   §Amendment cascade — tx-level canonical attribution).
3. To independently re-derive OHLC (cross-check the bundled snapshot
   against today's yfinance state): `pip install yfinance` and re-fetch
   the same (ticker, date_range) tuples; expect minor split-adjustment
   drift that does NOT materially shift F225.

Architecture parity with B-F1 (PTR audit rebuild) + B-F2 (PFD Schedule D
rebuild): bundle the structured substrate, re-derive aggregates in stdlib,
compare BIT-EXACT within tolerance band. The Phase F items collectively
ensure the canonical body anchors are reviewer-cookie-cutter reproducible
without lake access, Gemini API spend, or yfinance install.

## Related files in the OCC packet

* `../occ/ptr_filing_audit_khanna_2026_05_02.json` — frozen per-tx late-filing
  audit (canonical-view-derived).
* `../occ/khanna_pfd_schedule_d_2026_05_02.json` — frozen Goldman SP
  margin-ladder ladder TY2016-TY2019 (Schedule D liabilities).
* `../occ/khanna_ohlc_2026_05_02.json` — frozen daily close prices for the
  42 in-scope tickers + SPY benchmark.
* `../occ/khanna_window_events_2026_05_02.json` — frozen per-ticker
  window-attribution event date sets.
* `../occ/trade_pnl_facts_2026_05_02.json` — frozen trade-PnL canonical
  scalars snapshot (F225 / F242 / F820 / F833 from `ro_khanna.v3_facts`).
* `../../verify_anchors_occ.py` — the reviewer kit; reads bundled snapshots
  in `--frozen` mode (default) or re-derives against the lake in `--live`
  mode.
* `../../fetch_substrate_occ.py` — primary-source fetch recipe for the
  non-OCR substrates (statute / FEC / IRS / roll-calls / LDA).
* `../../REPRODUCIBILITY_METHODOLOGY_OCC.md` §3 — full per-substrate dedup
  rule discipline, OCR work-product reproducibility chain, and worked HUMANA
  358d end-to-end example.
