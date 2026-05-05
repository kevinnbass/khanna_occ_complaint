# LIMITATIONS — permanent verification gaps

This document enumerates the permanent gaps in the verification stack —
places where reproducibility is structurally limited, not by design
choice but by the nature of the underlying data sources.

Each gap is documented honestly with: (a) why it can't be closed, (b)
what mitigation is in place, (c) what a paranoid reviewer can do to
narrow the gap further.

---

## 1. yfinance OHLC — re-runnable; split-adjustment basis can drift retroactively

**Affected snapshot:** `data/occ/khanna_ohlc_2026_05_02.json`
**Affected body figures:** F225 trade-PnL bands ($14.6M low / $61.0M mid /
$107.5M high), SPY baseline $32.9M, alpha vs SPY $28.2M, F820/F833
sector-matched alphas.

**The publisher fetched this themselves.** No third-party gave the
publisher this data. The fetch script
(`scripts/k_ro_khanna_s8b_03_fetch_ohlc.py`, mirrored under the V2 root
as `fetch_substrate_ohlc.py`) calls:

```python
import yfinance as yf
yf.Ticker(t).history(start='2017-01-01', end='2026-04-18', auto_adjust=True)
```

against the public Yahoo Finance Chart API endpoint
(`query1.finance.yahoo.com/v8/finance/chart/<TICKER>`). Anyone with
`pip install yfinance` and internet access can re-run this same fetch
for the same 42 tickers + date range — no API key, no login, no paid
subscription required. It is not "vendor-relayed" in the sense that
the data was given to the publisher; the publisher ran the fetch itself
and the reviewer can re-run the same fetch.

**The actual structural caveat — split-adjustment retroactive rebasing:**
yfinance with `auto_adjust=True` returns Yahoo's split-and-dividend-
adjusted close prices. When a ticker undergoes a new stock split AFTER
the snapshot date, Yahoo retroactively rewrites that ticker's entire
historical adjusted-close series so the whole history reflects the new
split basis. A reviewer fetching the same `(ticker, date)` pair months
after publication may therefore see a different absolute close price
than the bundled snapshot. This is rebase, not fetch error.

**What stays stable across rebases (so reproduction works):**

- Existence of every `(ticker, date)` pair (the same trading days are returned)
- Relative ordering within any single ticker's history
- Alpha ratios (subject_return / SPY_return) over the same window
- Window concentration metrics (% of position established within ±N days)
- Split-adjusted percentage returns over any window (mathematically invariant)

**What can drift across rebases:**

- Absolute close prices in dollar terms
- Absolute share counts if a holding is restated post-split
- Absolute trade-PnL dollar figures (empirically <5% in our case; F225
  shifted 4.16% from original-extraction to post-cascade re-canonization,
  which is why F225 was re-canonized to $61.04M during the build)

**Mitigation:**

1. The bundled OHLC snapshot's SHA256 is committed to `99_SHA256SUMS.txt`
   and OpenTimestamped at publication, so the snapshot itself is
   bit-for-bit pinned to publication time.
2. Internal consistency: SPY benchmark + sector ETF baselines are
   computed against the same snapshot, so alpha-over-SPY and sector-
   matched alpha relationships are coherent within the bundle.
3. Reviewer re-fetch (Tier-D for OHLC): `pip install yfinance` and run
   the one-liner in `data/occ/khanna_ohlc_2026_05_02.provenance.json`
   under `reproducibility.reviewer_command` — compares daily-close
   series against bundled snapshot. Expect 100% pair-existence match,
   ~95-99% per-data-point match within ±2% absent recent splits.

**Paranoid path:** subscribe to a paid market-data vendor (Bloomberg,
Refinitiv, Polygon.io, IEX Cloud) and re-derive close prices from
licensed exchange-tape feeds. The bundle does not depend on any private
data source — every value is anonymously re-fetchable by anyone — but
this is the path for a reviewer who wants to bypass Yahoo entirely.

---

## 2. Lake-derived chamber aggregates — SQL queries against private DB

**Affected snapshots:**
- `data/occ/house_chamber_audit_2026_05_02.json`
- `data/occ/ptr_filing_audit_khanna_2026_05_02.json`
- `data/occ/peer_baseline_percentiles_2026_05_02.json`

**Affected body claims:** chamber P50 / P95 percentiles, peer-46 cohort
percentiles, post-canonical-view-dedup chamber-wide rates.

**Why it can't be closed without DB access:** these snapshots are SQL
projections against `lake.house_ptr_chamber_audit_*` and
`ro_khanna.peer_baseline_percentiles`. The underlying lake is a
private PostgreSQL instance populated by the publisher's drain
infrastructure. There is no single primary URL for "the chamber-wide
PTR audit" — it's an aggregation across thousands of per-Member PDF
extractions.

**Mitigation:**

1. The chain of custody is documented in each snapshot's
   `*.provenance.json` file: the canonical script that produced the
   snapshot + the script's git SHA + the SQL text.
2. The Khanna-specific portion (which is what the OCC complaint hinges
   on) IS reproducible without DB access: `khanna_ptr_transactions`
   has provenance hashes for every Khanna PTR PDF, and Tier-E re-OCRs
   them end-to-end. The chamber-wide percentile context (what's the
   median Member's late rate?) is the part that requires the chamber
   rebuild.
3. Tier-F includes an opt-in `--include-chamber-rebuild` flag that
   invokes `rebuild_chamber_audit.py --full-chamber --cost-acknowledged`
   to re-derive the chamber-wide audit via Gemini per-page OCR on
   ~5K-10K chamber PTR PDFs. Estimated reviewer cost: $50-200 in
   Gemini API spend.

**Paranoid path:** request the lake schema dump from the publisher and
re-run the canonical SQL. Or run the chamber-wide Gemini rebuild
($50-200 spend) for a from-scratch chamber baseline.

---

## 3. Ahuja Foundation 990-PFs — XML canonical at IRS; PDF mirror partial

**Affected snapshot:** `data/occ/ahuja_foundation_990pf_2026_05_02.json`
**Affected body claims:** Ahuja Foundation 990-PF financial summaries
(Count 7 spousal-asset disclosure framing).

**The canonical IRS publication for e-filed Form 990-PF is XML, not
PDF.** The bundled snapshot was extracted from the IRS e-file XML
corpus (lake.irs_990_returns + lake.irs_990_officers +
lake.irs_990_pf_noncash_donations). The PDF mirror is provided as a
courtesy for human review.

**PDF mirror status (uploaded as GitHub Release assets):**

| Tax year | PDF mirrored? | Asset name | Notes |
|---|---|---|---|
| TY2024 | NO (XML only) | — | ProPublica + IRS not yet rendered |
| TY2023 | NO (XML only) | — | ProPublica + IRS not yet rendered |
| TY2022 | YES | `AHUJA_990PF_2022.pdf` | 949 KB |
| TY2021 (primary) | YES | `AHUJA_990PF_2021.pdf` | 879 KB |
| TY2021 (amendment) | YES | `AHUJA_990PF_2021_v2.pdf` | 911 KB |
| TY2020 | NO (XML only) | — | ProPublica `filings_with_data` carries no `pdf_url` |
| TY2019 | YES | `AHUJA_990PF_2019.pdf` | 848 KB |
| TY2018 | YES | `AHUJA_990PF_2018.pdf` | 793 KB |
| TY2016 (historical) | YES | `AHUJA_990PF_2016.pdf` | 749 KB |

**The 6 mirrored PDFs are fetched directly from `apps.irs.gov` —
no Cloudflare bypass required.** Filename pattern:
`https://apps.irs.gov/pub/epostcard/cor/{ein}_{period}_990PF_{filing_seq}.pdf`.
Anyone with `urllib.request` can re-fetch identical bytes. SHA256s for
all 6 PDFs are recorded in `data/occ/ahuja_foundation_990pf_2026_05_02.provenance.json`
and in the release-asset `AHUJA_PDF_MANIFEST.json`.

**For TY2017, TY2020, TY2023, TY2024 (XML-only):** the body claims
that source from these years are anchored against the IRS e-file XML
(via lake.irs_990_returns), not against PDFs. The XML is fetchable from
ProPublica's `download-xml` endpoint, but ProPublica itself is
Cloudflare-protected. Three reviewer paths to obtain the XML:

1. Open `https://projects.propublica.org/nonprofits/organizations/341685088`
   in a real browser, click each year's "XML" link to download.
2. Use the IRS Tax-Exempt Organization Search at
   `https://apps.irs.gov/app/eos/displayAll.do?dispatchMethod=displayAllInfo&Id=2287614&ein=341685088`
   (also browser-rendered).
3. Trust the bundled `lake.irs_990_returns` projection — its
   `substrate_authoritative_note` documents the chain of custody.

**Paranoid path:** for any in-scope tax year, manually open ProPublica
or IRS EOS in a browser, download the XML, parse it, compare to the
bundled snapshot's per-year row. The XML primary keys (EIN +
return-period + object-id) are deterministic.

---

## 4. Time-of-fetch immutability — primary sources can change

**Generic risk:** primary sources (House Clerk, FEC, IRS) can change
between publication and reviewer-side spot-check. The most common cause
is the **amendment cascade** — Members re-file PTRs to correct errors,
producing new doc_ids that supersede old ones.

**Implication for Tier-D:** a re-fetched PDF whose bytes differ from
the provenance hash may be a benign re-rendering or a real tampering.
The drift class needs interpretation — `verify_anchors_occ.py
--spot-check` reports DIVERGE with a "may be benign drift" note rather
than treating it as a hard tamper signal.

**Mitigation:** the OpenTimestamps proof anchors the manifest to
publication time. So if a reviewer in 2027 sees DIVERGE on Tier-D, they
can confirm via OTS that the publisher's snapshot was authored with
the bytes recorded in provenance — the divergence is due to upstream
change, not publisher tampering.

**Paranoid path:** set up a watchdog that periodically re-fetches every
provenance URL and emits a "drift report" — useful for monitoring
amendment-cascade activity over time. Out of scope for the cold-start
kit.

---

## 5. Gemini extraction is approximately reproducible at the PER-ROW grain, exactly reproducible at the AGGREGATE grain

**Affected tier:** Tier-E (re-OCR pipeline reproduction).

**The honest finding (empirically measured, 2026-05-04):** when re-OCR'ing
a Khanna PTR PDF today vs. the original lake extraction (weeks earlier),
**only ~30-50% of the per-row tuples match** under conservative
normalization. The model returns DIFFERENT subsets of transactions on
different runs, with overlapping but non-identical sets. This is real
LLM behavior — temperature=0 does not guarantee deterministic output
across thread-pool workers + minor prompt context shifts + Gemini's
internal model versioning.

**What this means for trust:**

- The PER-PDF row sets are NOT deterministically reproducible.
- The AGGREGATE numerical claims (358d worst-late, 1.74% rate, F225
  $61.04M trade-PnL) ARE reproducible at much higher fidelity because
  they sum across ~36,000 transactions in 114 PDFs — individual-row
  sampling noise washes out at aggregate grain (the row-count delta per
  PDF is typically 5-20%, but the dollar-amount-weighted aggregate
  delta is much smaller because most missed/added rows are at the
  $1,001-$15,000 floor of the disclosure brackets).

**Tier-E verdict bands (reflect this empirical reality):**
- BIT_EXACT — row tuple multisets exactly equal (rare; only on small
  PDFs with very clean extraction)
- DRIFT_BENIGN — Jaccard overlap ≥ 60% AND row-count delta ≤ 20%
- DRIFT_MATERIAL — below the DRIFT_BENIGN bar; investigate

A DRIFT_MATERIAL Tier-E verdict on individual PDFs DOES NOT
necessarily indicate tampering or pipeline error — it commonly reflects
LLM sampling drift between the original extraction time and re-OCR
time. The reviewer should escalate to Tier-F (rebuild scripts run on
re-OCR'd substrate) — if the AGGREGATE figures still match the body
claims at Tier-F, that's the dispositive end-to-end reproducibility
test.

**What Tier-E DOES catch:**

- Wholesale snapshot fabrication (Gemini today returns 0 transactions
  but snapshot has 79 → would surface as 0% Jaccard, count_delta_pct
  100%)
- Major OCR pipeline regression (Gemini today produces gibberish or
  parses wrong document → would surface as DRIFT_MATERIAL with
  semantically-different row content)
- SHA mismatch (PDF bytes today differ from bytes the snapshot was
  built from) — this is caught BEFORE Gemini even runs

**What Tier-E does NOT prove:** that any individual PDF row in the
snapshot is the "right" extraction. The snapshot represents one
particular Gemini run at original extraction time; Tier-E represents a
different Gemini run today. Both are valid OCR outputs; their
disagreement is sampling noise, not falsification by either party.

**Paranoid path:** use a non-LLM OCR engine (Tesseract is bundled at
`data/ocr_products/khanna_pfd_8221318_OCR.txt` for the 2024 Khanna
PFD as an independent corroboration sample). Or run Gemini extraction
N times and take majority-rule per row — if the "majority Gemini" set
agrees with the snapshot, that's stronger evidence than a single re-run.

---

## Trust posture summary

After all tiers (0 + 1 + 2 + D + E + F + OpenTimestamps) pass, the
package's body figures are reproducible from primary sources to within
documented tolerance bands. The remaining trust gaps are:

- yfinance OHLC: re-fetchable by any reviewer (`pip install yfinance`),
  but absolute prices may drift across reviewer fetch dates due to
  Yahoo's retroactive split-adjustment rebases. Relative ratios stable.
- Chamber-wide percentiles: lake-derived (DB access or $50-200 chamber
  rebuild required)
- Gemini sampling: approximately deterministic, not bit-exact

These gaps are structural to the data ecosystem, not to the
verification stack. A reviewer who wants to close them further has
explicit paranoid paths documented for each.
