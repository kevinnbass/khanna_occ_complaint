# Verification Tiers — reviewer cookbook

This package supports **graduated verification**: a reviewer picks how much
effort they want to spend depending on how skeptical they are. Each tier
closes a different trust gap. A casual reviewer can stop at Tier 0; a
paranoid reviewer can run all of them.

**The single command** that runs every tier in sequence:

```bash
python reproduce_all.py --spot-check 5 --tier-E --tier-F --verify-timestamp
```

That's the maximalist test. The rest of this doc explains what each tier
proves so you can pick your level.

---

## Tier 0 — Manifest integrity (~1 second)

```bash
python reproduce_all.py     # runs Tier 0 + 1 + 2 by default
```

Recomputes the LF-canonical SHA256 of every file listed in
`99_SHA256SUMS.txt` (276 files) and confirms zero drift.

**Proves:** the package's bytes match what the publisher produced. Catches
tampering, incomplete clones, and bit-rot.

**Doesn't prove:** that the publisher's bytes themselves are honest.

---

## Tier 1 — Body-figure verifier (~3 seconds)

```bash
python verify_anchors_occ.py
```

For each of 68 manifest anchors (one per substantive body figure),
recomputes the figure from the bundled snapshot data and compares to the
body claim. Examples:

- OCC_M021: aggregate household trade-PnL = $61.0M mid → recomputed from
  bundled `khanna_ptr_transactions` + `khanna_ohlc` snapshots
- OCC_M070: 5 U.S.C. § 13105 STOCK Act 45-day deadline → resolved against
  bundled `statute_cites` snapshot

**Proves:** the body's figures are arithmetically derivable from the
bundled snapshots. The math is correct given the inputs.

**Doesn't prove:** that the bundled snapshots faithfully represent
primary sources (House Clerk PDFs, FEC filings, IRS 990s).

---

## Tier 2 — Substrate rebuilds (~30 seconds)

```bash
python data/ocr_products/rebuild_ptr_audit_khanna.py
python data/ocr_products/rebuild_pfd_schedule_d_khanna.py
python data/ocr_products/rebuild_trade_pnl_khanna.py
```

Re-derives the snapshot scalars themselves from the raw bundled OCR /
PDF / OHLC artifacts using stdlib Python. No network, no API keys.

**Proves:** the snapshot's load-bearing scalars (Khanna 358d worst-late,
1.74% rate, F225 $61.04M trade-PnL, etc.) are reproducible from raw
substrate via the canonical aggregation rules in the rebuild scripts.

**Doesn't prove:** that the raw substrate (bundled JSON rows) is a
faithful extraction from the primary PDFs.

---

## Tier D — Primary-source spot-check (~30 seconds per anchor)

```bash
python verify_anchors_occ.py --spot-check 5         # 5 random endpoints
python verify_anchors_occ.py --spot-check OCC_M021  # specific anchor
```

For each selected endpoint, re-fetches the primary URL fresh from
clerk.house.gov / lda.senate.gov / uscode.house.gov / etc., hashes the
returned bytes, and compares to the SHA256 stored in the snapshot's
`*.provenance.json` at publication time.

A MATCH proves the primary source today returns the SAME bytes the
publisher hashed when building the package. A DIVERGE means either the
primary source has changed since publication (benign — common for
amendment-cascade re-postings) or the publisher's snapshot was tampered
(malicious).

**Sampling logic:** if 5 random anchors all MATCH, the Bayesian
probability that the publisher tampered with even one snapshot drops
sharply. For the truly paranoid, `--spot-check 50` or
`--spot-check OCC_M021` etc. covers more ground.

**Proves:** at the inspected endpoints, the bundled snapshot bytes match
what the primary source serves today. The journalist's snapshot is
authentic at those points.

**Doesn't prove:** that other (unsampled) snapshots are equally
authentic. Use larger N to tighten the bound.

**Permanent gaps in spot-check (documented in LIMITATIONS.md):**
- yfinance OHLC: vendor-relayed; no primary URL exists
- Lake-derived chamber aggregates: SQL queries against private DB; no
  single primary URL
- ProPublica 990-PFs: Cloudflare-protected (mirror copies in the GitHub
  Release; spot-check can be done manually against the mirror)

---

## Tier E — Pipeline re-OCR (~1-2 hours, ~$5-50 in Gemini API spend)

```bash
export GEMINI_API_KEY=<your_key>
export GEMINI_PER_PAGE_HELPER_DIR=<path_to_helper_repo>
python tier_e_reocr.py
```

Re-runs the EXACT same Gemini per-page extraction pipeline that produced
the bundled structured rows:

- Same model (`gemini-3.1-flash-lite-preview`)
- Same prompt template (vendored from `rebuild_chamber_audit.py`)
- Same DPI (200) for PDF→PNG rasterization

For each Khanna PTR + PFD PDF: download from clerk.house.gov, verify
bytes match Tier-D provenance hash, re-render PNG pages, re-extract via
Gemini, compare structured rows to bundled snapshot.

**Proves:** the pipeline's OCR step is reproducible. The bundled
structured rows are what the published Gemini prompt + model produces
from the verified-authentic primary PDFs. Removes "the journalist faked
the OCR output" as a possibility.

**Doesn't prove:** that the rebuild scripts on top of the OCR rows
reproduce the body figures (that's Tier F).

**Note on independent OCR engines:** the Tesseract output bundled at
`data/ocr_products/khanna_pfd_8221318_OCR.txt` is a **separate
cross-validation artifact** — it shows that an entirely different OCR
engine (open-source Tesseract, no LLM) read the same PDF and produced
text consistent with the Gemini extraction. It's not part of the
Tier-E pipeline reproduction; it's a corroborating second opinion.

---

## Tier F — Full end-to-end re-derive (~2-4 hours, includes Tier-E spend)

```bash
python reproduce_all.py --tier-F
```

Composes Tier-E with the existing rebuild scripts:

1. Re-fetch + re-OCR all primary PDFs (Tier E)
2. Substitute the re-OCR'd structured rows for the bundled snapshots
3. Re-run the rebuild scripts (PTR audit / PFD Sch D / trade-PnL) on the
   re-OCR'd substrate
4. Compare re-derived body figures to current body claims

**Proves:** the full pipeline — primary PDF bytes → Gemini OCR →
structured rows → canonical-view dedup → aggregation → body figures —
is reproducible end-to-end from primary sources.

**Doesn't prove:** chamber-wide audits (would require Gemini-extracting
every Member's PTRs across the chamber, a $50-200 reviewer Gemini spend
opt-in via `--include-chamber-rebuild`).

**Permanent gap:** yfinance OHLC reuses bundled snapshot at Tier F
(no primary URL exists). The rebuild trade-PnL output reflects the
bundled OHLC snapshot's prices.

---

## Public timestamp — was the package backfilled? (~1 second)

```bash
python verify_timestamp.py
```

Reads `99_SHA256SUMS.txt.ots` (an OpenTimestamps proof submitted to
4 public calendar servers at publication time, anchored into Bitcoin
within ~1-2 hours after publication). Confirms:

- The proof's commitment chain attaches to the manifest's SHA256 today
- Multiple independent calendar attestations are present
- (After Bitcoin block confirmation) the manifest existed at the time
  block N was mined

**Proves:** the package's bytes existed at the time the proof was
submitted. The journalist could not have backfilled the analysis to
match later-developing events without leaving a timestamp gap.

---

## Trust math — what does each tier rule out?

| Tier | Rules out |
|---|---|
| 0 | Tampering between publisher and reviewer (mid-flight modification) |
| 1 | Body claims that don't match the data the journalist supposedly used |
| 2 | The aggregation arithmetic in the journalist's scripts being wrong |
| D | Cherry-picking or forging snapshot rows (at the inspected endpoints) |
| E | Cherry-picking or forging the OCR output (Gemini hallucination cover-up) |
| F | Any error end-to-end from primary PDF bytes through to body figure |
| OTS | Backfilling the analysis to match later events |

After all tiers pass, the journalist would have to have: tampered with
clerk.house.gov + IRS direct + uscode.house.gov + LDA Senate AND
submitted a falsified package to OTS calendars at exactly the right
moment AND reproduced the deterministic Gemini outputs at the same
model+prompt+temperature — to fake the body figures. That's a much
higher bar than "trust the journalist's PDF."

---

## What this package is NOT

This is a reproducibility kit, not a witness statement. Tier passes
prove the FIGURES are authentic and reproducible from primary sources.
The INTERPRETATION of those figures (whether they constitute STOCK Act
violation severity, conflict-of-interest disclosure failures, etc.) is
a legal/policy question for the reviewing body (OCC, FEC, DOJ, House
Ethics) — not something a Python verifier can adjudicate.

The verification stack proves what's verifiable. The legal reasoning is
in the body of the OCC complaint itself.
