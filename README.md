# OCC Complaint Package — IN RE: Rep. Rohit "Ro" Khanna (CA-17)

Body snapshot date: **2026-05-02**.

This directory contains a complaint to the **Office of Congressional Conduct ("OCC"; formerly the Office of Congressional Ethics ("OCE"))** alleging six distinct courses of conduct by Representative Rohit "Ro" Khanna (CA-17, sworn in January 3, 2017; fifth-term Member of the 119th Congress) under the **Ethics in Government Act (5 U.S.C. Ch. 131)**, the **STOCK Act of 2012** (5 U.S.C. § 13105(l) periodic-transaction reporting; 15 U.S.C. § 78u-1(g) MNPI extension), the **Federal Election Campaign Act** (52 U.S.C. § 30116; 11 C.F.R. § 109.21 coordination), the **Lobbying Disclosure Act** (2 U.S.C. §§ 1604, 1606), **18 U.S.C. § 207** (post-employment restrictions), **House Rule XXIII** (Code of Official Conduct), and related provisions. Parallel referrals to the **Federal Election Commission**, the **House Committee on Ethics**, and the **Department of Justice** address the matters within their respective jurisdictions on the same factual record and are transmitted to those venues separately.

The complaint is presented along with full reproducibility infrastructure: an 80-marker provenance manifest, a 651-line methodology cover document, a 24-anchor reviewer-side reproducibility kit, six frozen substrate snapshots covering every class-1 substrate referenced by a load-bearing body claim, and an LF-canonical SHA-256 integrity manifest.

---

## What's in this directory

| File | Purpose |
|---|---|
| **`OCC_COMPLAINT_KHANNA.md`** | Operative complaint body (630 lines / 6 Counts / 14 numbered Anticipated Responses + 5 preemptive rebuttals). Cover page, Caption and Standing, Factual Allegations, Counts 1–6, Damages and Disgorgement, Civil Penalties Sought, Anticipated Responses, Exhibit List, Verification, Methodology footer, and the auto-generated §A Provenance Appendix (lines 569–670). This is what gets transmitted to the Office of Congressional Conduct. |
| **`OCC_EXHIBIT_LIST.md`** | Authoritative catalog of the 28 lettered exhibits (A, B, C, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Z, AA, BB, CC, DD, EE, FF, GG, II, JJ) plus the chamber-MNPI-scan workpaper. Each row maps to a file path, primary-fact predicate keywords, and the Counts the exhibit supports. Exhibit files themselves live one directory up at the dossier root (`../EXHIBIT_*.md`, `../EXHIBIT_*.csv`, `../EXHIBIT_L_PFD_*.png`, `../EXHIBIT_L_PFD_OCR.txt`). |
| **`PRE_FLIGHT_REPORT.md`** | Phase-0 inventory + drift-scan report. Voice-rule + citation-currency + vacated-severity invariants documented with grep evidence. |
| **`REPRODUCIBILITY_METHODOLOGY_OCC.md`** | 651-line methodology cover document. § 1 substrate-translation table (26 distinct substrates mapped to public-source equivalents); § 2 column cross-walk; § 3 dedup methodology rules (3.1 PTR amendment-cascade canonical view, 3.2 pre-tenure LATERAL filter, 3.3 tightened mixed-date parse-error sentinel, 3.4 notification-date NULL fallback, 3.5 two-universe peer baseline, 3.6 composite severity score, 3.7 ticker-NULL fallback, 3.8 FEC Schedule E `(committee_id, candidate_id, tran_id)`-canonical aggregation, 3.9 LDA registrant-OR-client universe, 3.10 cross-cycle name-variant donor aggregation, 3.11 empty-string-to-numeric casting, 3.12 date-format heterogeneity, 3.13 SQL-dialect equivalence, 3.14 snapshot-freshness statement, 3.15 Class-2 OCR work-product reproducibility chain, 3.16 automated fetch recipe; § 3a chamber-baseline disclosure venue-specific paragraph template); § 4 expected-result anchor table (30+ load-bearing scalars); § 5 reproducibility-precision lessons; § 6 worked end-to-end HUMANA 358-day example; § 7 reviewer aids (30-entry glossary + 12-exhibit reproducibility map + 11-pattern common-divergence diagnostic). Reviewers should read this alongside the body. |
| **`verify_anchors_occ.py`** | Reviewer-side reproducibility kit (Python 3.8+, single dependency: `requests` for `--live` mode; ~1,186 lines). 24 anchor checks across 12 verifier kinds against the bundled frozen snapshots; emits a side-by-side comparison report at `verify_anchors_occ_report.md`. |
| **`verify_anchors_occ_report.md`** | Auto-regenerated reviewer-kit output. Last invocation: **33 anchors / 31 OK / 0 DIVERGE / 0 ERROR / 2 MANUAL** (the 2 MANUAL rows are the FEC committee-registration and Schedule E aggregate that require `--live` API access). |
| **`_provenance_index_occ.json`** | 80-entry machine-readable provenance manifest. Each marker `OCC_M001`–`OCC_M080` maps to: claim text, body section, substrate, predicate-grep over the fact store, fact_ids, verification_ids, element_id, theory_id, what-it-means / what-it-shows, first-seen section. The §A Provenance Appendix in the body is regenerated from this file. 76 markers carry resolved fact_ids; 63 carry resolved verification_ids; 4 are computed-substrate-class entries whose verifier kind is wired in `verify_anchors_occ.py` (statute-cite / methodology-text / manifest-self-reference / chamber-audit / peer-baseline / ptr-audit / vote / IRS-990) rather than against a single v3_fact. |
| **`99_SHA256SUMS_OCC.txt`** | LF-canonical SHA-256 integrity manifest covering every text file (markdown / Python / JSON) in this directory plus exhibit data and frozen snapshots. Verifies against any tampering of body, methodology, kit, exhibits, or snapshots. Regenerated by `scripts/manifest_canonical_sha.py --root <this_dir> --manifest-name 99_SHA256SUMS_OCC.txt --write` in the source repo. CRLF→LF normalization applied to text/markdown/csv before hashing so manifest hashes are reproducible across Windows working trees with `core.autocrlf=true` and Linux/macOS / canonical-repo filesystems. |
| **`data/occ/`** | Date-stamped frozen substrate snapshots (all 2026-05-02): `statute_cites_2026_05_02.json` (operative-cite resolutions from `public.v_statute_current`), `ptr_filing_audit_khanna_2026_05_02.json` (Khanna's `public.house_ptr_chamber_audit_by_member` row + per-tx HUMANA 358-day worst-late detail), `house_chamber_audit_2026_05_02.json` (chamber-wide rate + severity percentiles + Khanna severity rank), `peer_baseline_percentiles_2026_05_02.json` (5 canonical peer-46 metrics), `khanna_votes_2026_05_02.json` (NDAA cluster 13 rolls / 12 NAY), `ahuja_foundation_990pf_2026_05_02.json` (EIN 34-1685088 8-tax-year returns + Ritu Ahuja Khanna trustee roster + NVDA TY2024 contributors detail 10,076 shares / $1,667,345 FMV + EoY FMV TY2024 $45,102,055 across 30 holdings). The reviewer kit reads from these. |
| **`exhibits_ahuja/`** | Class-1 supporting CSVs for the Ahuja Foundation Count 6 / Exhibit H / Exhibit O analysis: `E_corpus_by_year.csv`, `F_nvidia_transfers.csv`, `G_sector_concentration.csv`, `H_grantmaking_top_recipients.csv`. Each is reproducible from `lake.irs_990_*` + `ro_khanna.ahuja_foundation_holdings`; methodology in `exhibits_ahuja/README.md`. |

---

## Reproducibility — pick your verification depth

This package supports **graduated verification**. A casual reviewer can
confirm the package's integrity in seconds; a paranoid reviewer can
re-derive every body figure end-to-end from primary sources. Each tier
closes a different trust gap. See `VERIFICATION_TIERS.md` for the full
cookbook + `LIMITATIONS.md` for the documented permanent gaps.

### Easiest path (first-time reviewers): guided launcher

```bash
python welcome.py
```

Walks through what's in the package, what each tier proves, and asks
which depth you want to run. Defaults are sensible — pressing Enter
through the prompts runs Tiers 0+1+2 (~30s, fully offline) and offers
opt-ins for Tier-D primary-source spot-check + OpenTimestamps proof.
For Tier-E (re-OCR yourself with Gemini), the launcher detects
`GEMINI_API_KEY` from env or prompts you to paste one — most reviewers
skip this since the bundled OCR is the publisher's authoritative
output and Tiers 0+1+2+D already cover the body figures + primary-
source bytes.

### Scripted / CI path

```bash
python reproduce_all.py                                    # Tiers 0+1+2 (~30s, offline)
python reproduce_all.py --spot-check 5 --verify-timestamp  # + Tier-D + OTS
python reproduce_all.py --tier-E                           # + re-OCR (needs Gemini key, ~1-2 hr)
python reproduce_all.py --tier-F                           # + full re-derive (~2-4 hr)
python reproduce_all.py --verbose                          # dump full subprocess output
```

For CI, run `python reproduce_all.py` with no prompts. Set
`GEMINI_API_KEY` + `GEMINI_PER_PAGE_HELPER_DIR` for Tier-E/F to
actually re-OCR; otherwise those tiers report `SKIPPED`.

### What's bundled in the cold-clone tarball

- 114 per-PTR Gemini OCR JSONs at `data/ocr_products/khanna_ptrs/`
- 1 PFD Tesseract OCR text + 5 page renders for the 116-page TY2024 PFD
- 13 snapshot JSONs + 13 sibling provenance.json files at `data/occ/`
- 33 supporting exhibits at `exhibits/` (each shipped as both a markdown narrative and a rendered PDF, plus 7 supporting CSV / PNG / TXT files — 73 files total)
- LF-canonical SHA256 manifest + OpenTimestamps proof
- All verifier + rebuild + tier-D/E/F + comprehensive-test scripts
- Cold-clone tarball total: ~78 MB

### What the bundled OCR contains

114 per-PTR Gemini OCR JSONs at `data/ocr_products/khanna_ptrs/<doc_id>/<doc_id>_OCR.json`
(the publisher's most-recent extraction) + 1 PFD Tesseract OCR text at
`data/ocr_products/khanna_pfd_8221318_OCR.txt` (cross-validation against
Gemini for the 116-page TY2024 PFD). Tier-E re-runs the EXACT same
Gemini per-page pipeline against PDFs you fetch yourself, proving the
bundled OCR isn't fabricated. The bundled OCR alone is sufficient for
Tiers 0+1+2; Tier-E is opt-in for paranoid mode.

### Per-tier menu

| Tier | Cost | Verifies | Command |
|---|---|---|---|
| 0 | <1s | manifest integrity (298 SHA256s) | `python reproduce_all.py` |
| 1 | ~3s | 68 body figures derive from snapshots | `python verify_anchors_occ.py` |
| 2 | ~30s | snapshot scalars derive from raw OCR/PDF | `python data/ocr_products/rebuild_*.py` |
| **D** | ~30s/anchor | snapshots match primary-source bytes | `python verify_anchors_occ.py --spot-check 5` |
| **E** | ~1-2 hr + ~$5-50 | bundled OCR reproduces from re-OCR'ing primary PDFs | `python tier_e_reocr.py` |
| **F** | ~2-4 hr + Gemini spend | full re-derive from primary PDFs to body figures | `python reproduce_all.py --tier-F` |
| **OTS** | <1s | package was not backfilled (calendar+Bitcoin proof) | `python verify_timestamp.py` |

### Tier prerequisites

- Tiers 0 + 1 + 2 + OTS: stdlib Python 3.8+ + `pip install opentimestamps-client` (for OTS)
- Tier D (spot-check): network access to clerk.house.gov / lda.senate.gov / uscode.house.gov
- Tier E (re-OCR): `pip install pymupdf google-generativeai` + `GEMINI_API_KEY` env + `GEMINI_PER_PAGE_HELPER_DIR` (path to a checkout exposing `src.gemini_per_page_extract`)
- Tier F: same as E

### Legacy verification path (still supported)

```bash
# 1. Requirements: Python 3.8+. Install one third-party package:
pip install requests

# 2. Run the kit. Default: read frozen snapshots in data/occ/.
python verify_anchors_occ.py

# Expected output: 31 OK / 0 DIVERGE / 0 ERROR / 0 FAIL on the resolvable rows;
# remaining rows MANUAL pending substrate-snapshot expansion.

# 3. Live cross-check (re-fetch from the FEC OpenFEC API + report drift):
export DATA_GOV_API_KEY=<your_api.data.gov_key>      # signup https://api.data.gov/signup/
python verify_anchors_occ.py --live --api-key $DATA_GOV_API_KEY

# Expected output: 33 OK / 0 DIVERGE (modulo amendment drift on
# continuing-cycle filings).

# 4. Verify SHA-256 manifest integrity:
sha256sum -c 99_SHA256SUMS_OCC.txt                   # Linux / macOS
Get-FileHash -Algorithm SHA256 *                     # PowerShell (manual cross-check)

# 5. (Optional) Snapshot-vs-primary currency check — for each frozen
#    snapshot in data/occ/, re-derive against current primary substrate
#    and report per-snapshot drift class. Closes the snapshot-vs-primary
#    trust gap ("snapshots are 2026-05-02; how do I know they still match
#    primary?"). Three snapshots are fully primary-diffable from a cold-
#    start environment (statute USC sections, Khanna roll-call votes,
#    Ahuja Foundation 990-PF metadata); six others honestly disclose their
#    blocker (lake access / fact-store access / LDA API key) along with
#    the substrate authority and re-derivation recipe.
python verify_anchors_occ.py --diff-snapshots-vs-live
# OR run only the diff (skip the regular anchor checks):
python verify_anchors_occ.py --diff-snapshots-vs-live --diff-only

# Expected output (cold-start, no lake / no API keys):
#   35 per-row diffs across 9 snapshots —
#   CLEAN: 27 / DRIFT_BENIGN: 0 / DRIFT_VALUE: 0 / BLOCKED: 8 / ERROR: 0
# (Reviewer who first runs `python fetch_substrate_occ.py --classes lda` to
#  populate the LDA REST API cache will see 31 CLEAN / 2 PASS_WITH_DEFECT /
#  4 BLOCKED — the LDA row flips to PWD/api_substrate_subset_of_lake_bulk
#  per s23 B-D4 wiring; ptr_filing_audit_khanna additionally flips
#  BLOCKED → 2 × CLEAN via s27 B-F1 wiring; pfd_schedule_d flips
#  BLOCKED → 2 × CLEAN via s29 B-F2 wiring; trade_pnl_facts flips
#  BLOCKED → 1 × CLEAN + 1 × PASS_WITH_DEFECT/post_cascade_substrate_drift
#  via s30 B-F3 wiring — all without any extra fetch.)
# CLEAN means frozen scalar reproduces against live primary today.
# BLOCKED rows carry the substrate authority + re-derivation recipe in
# their Notes column for reviewers with lake / API access.
# Diff report written to verify_anchors_occ_diff_report.md (NOT bundled
# in 99_SHA256SUMS_OCC.txt; the diff report is regenerated on demand).
#
# NEW 2026-05-03 (s27 B-F1): the Khanna PTR audit aggregates
# (n_tx_total=35,954 / n_tx_late=624 / worst=358d) are now reviewer-
# rebuildable from the bundled raw substrate without lake access:
#   python data/ocr_products/rebuild_ptr_audit_khanna.py
# (~30s; stdlib only; no API spend; no DB driver). Loads
# data/occ/khanna_ptr_transactions_2026_05_02.json (one-time export of
# lake.house_ptr_transactions 36,277 raw rows for Khanna) → applies
# canonical-view tx-key dedup + audit_flag exclusions + days_late
# computation per .claude/rules/stock-act-audit.md → BIT-EXACT match on
# all 10 aggregate fields + HUMANA worst-tx detail.
#
# NEW 2026-05-03 (s30 B-F3): the Khanna household trade-PnL canonical
# scalars (F225 mid $61.04M household terminal P&L; F820 14-ticker
# pharma alpha; F833 broader pharma alpha) are now reviewer-rebuildable
# from three bundled snapshots (PTR rows + OHLC daily-close + window-
# attribution event sets) without yfinance install or lake access:
#   python data/ocr_products/rebuild_trade_pnl_khanna.py
# (~10-30s; stdlib only). Loads khanna_ptr_transactions + khanna_ohlc +
# khanna_window_events snapshots → applies ticker_map ILIKE
# classification + per-tx forward P&L using OHLC + ±14d window flags +
# per-sector aggregation. Output diffs against trade_pnl_facts snapshot
# load_bearing_invariants within ±5% PASS_WITH_DEFECT band on F225 mid
# (current rebuild lands at $61.04M, 4.2% under, attributable to post-
# AF#67 amendment-cascade dedup discipline + USAspending substrate-grow
# per stock-act-audit.md §Amendment cascade).
```

The kit performs three classes of check across 12 verifier kinds:

1. **Statute-cite resolves** (10 anchors / `statute_cite_resolve` kind): loads the `statute_cites_2026_05_02.json` snapshot of `public.v_statute_current`, resolves each operative complaint cite (5 U.S.C. § 13105(l), 5 U.S.C. § 13106, 5 U.S.C. § 13104(d)(1)(A), 15 U.S.C. § 78u-1(g), 11 C.F.R. § 109.21, 52 U.S.C. § 30116(a)(7)(B)(i), 2 U.S.C. § 1604, 2 U.S.C. § 1606, 18 U.S.C. § 207, House Rule XXIII), confirms the bundled `full_text` contains every required token. Per `.claude/rules/citation-currency.md`, comparison is against `full_text`, **not** against `section_label` (the latter carries a known P0.5.A-era ingest off-by-one for 5 U.S.C. Ch. 131 EIGA-descendant sections).
2. **Filesystem-anchored claims** (2 anchors / `manifest_self_reference` + `methodology_text` kinds): confirms `OCC_EXHIBIT_LIST.md` exists at the claimed path and contains the required exhibit-letter tokens; confirms `OCC_COMPLAINT_KHANNA.md §METHODOLOGY` exists and enumerates the substrates / dedup rules / chamber-baseline disclosure template.
3. **Substrate-snapshot resolves** (12 anchors / `ptr_audit_aggregate` + `ptr_audit_worst_humana` + `chamber_audit_p50` + `peer_baseline_metric_resolve` + `vote_resolve` + `irs_990_resolve` kinds): loads each substrate snapshot, applies the canonical-view dedup + percentile + per-tx-worst + roll-call multiplexing logic per **REPRODUCIBILITY_METHODOLOGY_OCC.md § 3.1 / § 3.5 / § 3.6**, compares to body anchors. Live mode (planned extension) re-fetches the 2 currently-MANUAL FEC anchors from OpenFEC and reports drift.

The frozen-snapshot path produces EXACTLY the body's authored figures regardless of post-snapshot lake or OpenFEC drift. The `--live` path is the reviewer's independent verification against current FEC public data.

### Why frozen snapshots, not raw lake access?

The complaint's substrate is the campaign's PostgreSQL "lake" plus the case-schema methodology artifacts (`ro_khanna.ptr_filing_audit`, `ro_khanna.peer_baseline_percentiles`, `ro_khanna.ahuja_foundation_holdings`, `public.house_ptr_chamber_audit_by_member`). Reviewers do not have direct access to the lake. The frozen snapshots capture every load-bearing scalar that the body operatively cites, in JSON, alongside the SQL recipe that produced each snapshot — so a reviewer with House Clerk PDF access, FEC bulk / OpenFEC API access, IRS 990-PF e-file-corpus access, and the methodology cover doc can re-derive the same scalars without lake access. Cold-start re-derivability is the design constraint.

Count 4 (insider-pattern trading convergence) is anchored on the same SEC Form 8-K and Form 3/4/5 substrates that Counts 1 and 3 use; reviewers reproducing it run the same anchor-check rows.

---

## Body anchors (33 reviewer-checkable scalars)

| Marker | § | Claim | Expected scalar | Verification path |
|---|---|---|---|---|
| `OCC_M070` | Counts 1, 6 | 5 U.S.C. § 13105(l) STOCK Act §6 PTR 45-day deadline (operative) | full_text contains "13105", "Filing of reports", "(l)", "45 days" | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M071` | Counts 1, 6 / Damages | 5 U.S.C. § 13106 EIGA civil-penalty framework (operative) | resolved federal_usc title=5 sec=13106 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M072` | Counts 1–3 (MNPI) | 15 U.S.C. § 78u-1(g) STOCK Act §§3-4 MNPI extension to Members | resolved federal_usc title=15 sec=78u-1 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M073` | Count 6 | 5 U.S.C. § 13104(d)(1)(A) spouse-asset disclosure scope | resolved federal_usc title=5 sec=13104 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M074` | Count 4 | 11 C.F.R. § 109.21 coordinated-communications 3-prong test | resolved federal_cfr title=11 sec=109.21 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M075` | Count 4 | 52 U.S.C. § 30116(a)(7)(B)(i) FECA contribution limits + coordination | resolved federal_usc title=52 sec=30116 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M076a` | Count 5 | 2 U.S.C. § 1604 LDA quarterly LD-2 + semiannual LD-203 reports | resolved federal_usc title=2 sec=1604 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M076c` | Count 5 | 2 U.S.C. § 1606 LDA civil + criminal penalties ($200K cap / 5-yr) | resolved federal_usc title=2 sec=1606 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M077` | Count 5 | 18 U.S.C. § 207 post-employment restrictions | resolved federal_usc title=18 sec=207 | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M078` | Counts 1, 2, 4, 5 | House Rule XXIII Code of Official Conduct | resolved house_rules sec=XXIII | `data/occ/statute_cites_2026_05_02.json` |
| `OCC_M079` | Exhibit list | OCC_EXHIBIT_LIST.md catalogs the lettered exhibit set | file present, all required tokens present | filesystem |
| `OCC_M080` | §METHODOLOGY footer | OCC_COMPLAINT_KHANNA.md §METHODOLOGY enumerates substrates + dedup rules + chamber-baseline disclosure template | file present, all required tokens present | filesystem |
| `OCC_M007` | Count 1 | Khanna late-filing count 624 of 35,954 (1.74%) across 22 distinct PFD docs | late 624/35954 = 1.74% / 22 of 114 PTRs | `data/occ/ptr_filing_audit_khanna_2026_05_02.json` |
| `OCC_M008` | Count 1 | Worst single-tx delay 358 days (HUMANA INC. CMN, DC owner, tx 2023-10-02 → filed 2024-11-08) | exact match | `data/occ/ptr_filing_audit_khanna_2026_05_02.json` |
| `OCC_M010` | Count 1 chamber baseline | Chamber rate baseline P50 10.06% across 210 Members (n_tx_total ≥ 20); Khanna severity rank 108/210 | n=210 P50_rate=10.055% P50_worst=344.0d; severity rank 108/210 | `data/occ/house_chamber_audit_2026_05_02.json` |
| `OCC_M012` | Count 1 peer baseline | Peer-46 rate baseline P50 5.96%; Khanna 1.74% rank 35/46 P25 (exculpatory on rate) | exact match | `data/occ/peer_baseline_percentiles_2026_05_02.json` |
| `OCC_M020` | Count 2 (NDAA NAY-cluster) | Khanna voted NAY on 12 of 13 NDAA passage / conference / override rolls 2017-2024 | NDAA cluster: 12 NAY of 13 rolls (92.3% NAY rate) | `data/occ/khanna_votes_2026_05_02.json` |
| `OCC_M027` | Count 6 (Nvidia × Select-Cmte) | Ahuja Foundation TY2024 NVIDIA non-cash donations: 10,076 total shares ($1,667,345 FMV) | 10,076 shares / $1,667,345 FMV across 2 contributor rows | `data/occ/ahuja_foundation_990pf_2026_05_02.json` |
| `OCC_M054` | Count 6 (spouse-asset disclosure scope) | Ritu Ahuja Khanna named TRUSTEE of Ahuja Foundation (EIN 34-1685088) every tax year 2018-2024 | TRUSTEE rows: 8 tax years (2018-2024) | `data/occ/ahuja_foundation_990pf_2026_05_02.json` |
| `OCC_M055` | Count 6 (Foundation EoY FMV anchor) | Ahuja Foundation TY2024 End-of-Year Fair Market Value $45,102,055 across 30 distinct holdings | $45,102,055.00 across 30 holdings | `data/occ/ahuja_foundation_990pf_2026_05_02.json` |
| `OCC_M021` | Count 2 (defense alpha) | Defense-prime sector midpoint terminal P&L $9.9M vs SPY $4.6M; alpha $5.4M (344 tx) | F225 / F242 carry the canonical scalars (substrate-class anchor) | `data/occ/trade_pnl_facts_2026_05_02.json` |
| `OCC_M026` | Count 3 (pharma alpha) | Pharma 12-ticker strict universe $215K alpha vs sector match (XLV/IBB/VHT); 20-ticker broader universe $1.84M | F820 / F833 BIT-EXACT | `data/occ/trade_pnl_facts_2026_05_02.json` |
| `OCC_M028` | Count 3 / Count 6 (Goldman margin scaffold) | Goldman Sachs margin facility TY2017-TY2019; TY2017 single liability $1M+ load-bearing | 13 Khanna SP-owned Goldman rows TY2016-TY2019 reproduce | `data/occ/khanna_pfd_schedule_d_2026_05_02.json` |
| `OCC_M041` | DOJ §3 (LD-203 aggregate) | LD-203 aggregate 2011-10 → 2025-12: $299,198 / 147 line items / 53 unique LDA registrants | 53-registrant invariant BIT-EXACT (line/amount drift = `substrate_count_drift` PASS_WITH_DEFECT acknowledged) | `data/occ/lda_khanna_contributions_2026_05_02.json` |
| `OCC_M058` | Count 6 (margin ladder TY2017-TY2020) | Household margin-loan ladder Goldman + Ritu Ahuja 1994 Trust TY2017-TY2020 (forecloses § 13104(f)(3) passive-SMA defense) | TY2017 $1M+ + TY2018 $265K-$550K + TY2019 + TY2020 ladder reproduce | `data/occ/khanna_pfd_schedule_d_2026_05_02.json` |
| `OCC_M061` | §IV (Damages Table) | Aggregate household terminal P&L midpoint $61.0M / SPY baseline $32.9M / alpha-over-SPY $28.2M | F225 numeric_value=61040313.07 BIT-EXACT (substrate-class anchor: F225 carries the constituents inside its preserved provenance) | `data/occ/trade_pnl_facts_2026_05_02.json` |
| `OCC_M062` | §IV ¶67 (window-attributable) | 41.3% of midpoint terminal P&L ($25.2M) generated by trades within ±14d of NDAA / CMS / 8-K / USAspending events | constituent scalar inside F225 umbrella (substrate-class anchor) | `data/occ/trade_pnl_facts_2026_05_02.json` |
| `OCC_M063` | §IV ¶68 (T+30 short-window) | 57.7% of T+30 mark-to-market P&L attributable to event-window trades = 3.4× per-trade ratio | constituent scalar inside F225 umbrella (substrate-class anchor) | `data/occ/trade_pnl_facts_2026_05_02.json` |
| `OCC_M064` | §IV ¶69 (sector decomposition) | Big Tech $27.6M / Defense Prime $5.4M / Defense Tech $0.7M / Pharma -$2.2M / HC Devices -$2.9M / HC Services -$0.3M (per-sector alphas sum to $28.16M ≡ headline alpha) | constituent scalar inside F225 umbrella (substrate-class anchor) | `data/occ/trade_pnl_facts_2026_05_02.json` |

The 80-marker manifest in `_provenance_index_occ.json` covers every load-bearing scalar in the body. The 33 anchors above are the prosecutorially-load-bearing ones reviewers should reproduce first; the remaining 47 markers are coverage breadth and trace to the same fact-store substrate via the manifest's `predicate_grep` + `substrate` + `sql_text` fields.

### Substrate classes (where each anchor is reproducible from)

This complaint's 80 markers split across three substrate classes:

| Class | Approx. count | Where to reproduce | Independent fetch |
|---|---|---|---|
| **Class 1: public bulk / public API** | ~72 of 80 | House Clerk Periodic-Transaction-Report + Annual-PFD bulk index + per-Member PDFs (`disclosures-clerk.house.gov`); FEC bulk + OpenFEC API; IRS 990 / 990-PF e-file XML (`s3://irs-form-990/`); House Clerk roll-call XML; Senate LDA quarterly LD-2 + LD-203; California Cal-Access bulk; U.S.C. + C.F.R. text (uscode.house.gov + ecfr.gov); House Rules + Ethics-Committee guidance text (rules.house.gov + ethics.house.gov + conduct.house.gov) | **deferred — `fetch_substrate_occ.py` planned (B-S10)**; in the interim, the methodology cover doc § 1 + § 3.16 enumerates each substrate's authoritative URL + SQL recipe so reviewers can pull manually |
| **Class 2: public PDF + private OCR extraction** | ~7 of 80 | Source PDFs at `disclosures-clerk.house.gov` (Khanna household PFDs + PTRs); OUR Tesseract-/Gemini-extracted parsed JSON for the 5-page TY2024 PFD bundled at `../EXHIBIT_L_PFD_P0[1-5].png` + `../EXHIBIT_L_PFD_OCR.txt`. Independent re-OCR is a reviewer-side cross-check. | **`data/ocr_products/` bundle deferred (B-S9)**; the source PDFs are publicly fetchable from House Clerk and the OCR text is staged at `../EXHIBIT_L_PFD_OCR.txt` so a reviewer can run their own pipeline against the same source material |
| **Class 3: paper-filed PDF + private hand-keyed extraction** | 0 of 80 | (n/a — none of the cited filers paper-filed during the cited periods) | (n/a) |

A reviewer reproducing this complaint's figures spends ~99% of their effort on class-1 substrates that are entirely public. The class-2 OCR work product is the SMA / QBT / EIF rebuttal at Counts 1 / 3 / 7 (the absence of any separately-managed-account, qualified-blind-trust, or exempt-investment-fund disclosure on Khanna's TY2024 Annual PFD); the source PDFs are publicly fetchable from House Clerk and a reviewer who wants to independently re-OCR runs their preferred pipeline against them.

---

## Theory and counts (high-level)

The complaint pleads **six distinct courses of conduct**, each anchored on the post-cascade canonical fact set (8/8 invariant: F215 / F227 / F486 / F610 / F612 / F628 / F742 / F865 + retained predecessors F226 / F743) and each independently READY_TO_PLEAD per the `mcp__facts__v3_theory_readiness(case='ro_khanna')` gate:

| Count | Theory | Operative statutes | Supporting exhibits |
|---|---|---|---|
| **1** | STOCK Act § 6 documentary non-compliance and §§ 3–4 MNPI-adjacent pattern evidence | 5 U.S.C. §§ 13105(l), 13106; 15 U.S.C. § 78u-1(g) | A, B, C, M, X, Z, F, FF |
| **2** | NDAA front-running (HASC jurisdictional nexus + ±14-day enactment-window defense-prime trades + public-NAY / private-BUY divergence) | 5 U.S.C. §§ 13105, 13106; 15 U.S.C. § 78u-1(g); 18 U.S.C. § 208 | E, N, U, A |
| **3** | Household financial-interest conflicts and regulatory-axis convergence (CMS pharma rulemaking; Palantir × HASC; Nvidia × Select-Committee; Goldman margin triangle) | 5 U.S.C. § 13104(a); 18 U.S.C. § 208; 15 U.S.C. § 78u-1(g) | F, N, O, CC, X, L, II, JJ, A |
| **4** | Insider-pattern trading convergence with authoritative issuer-event and insider-trade disclosures (same-day SEC Form 8-K intersection; aligned-direction Form 3/4/5 officer-trade intersection) | 15 U.S.C. §§ 78u-1(g), 78ff, 78j(b); House Rule XXIII cl. 1 | M, Z, F, X, FF |
| **5** | LDA § 203 reportable contributions, FARA / LDA dual-registration disclosure, and direct industry lobbying on respondent-sponsored bills | 2 U.S.C. §§ 1604, 1605; 22 U.S.C. § 611 et seq. | AA, S, C, GG |
| **6** | Revolving-door donor network, post-employment lobbying nexus, and LD-203 compliance failures | 2 U.S.C. § 1604(d); 18 U.S.C. § 207 | I, T, C |
| **7** | Spouse-asset disclosure scope (Ahuja Charitable Foundation EIN 34-1685088); Dover, Delaware rental-property asymmetric disclosure; household margin-loan + written-options scaffold foreclosing passive-SMA / QBT / EIF defense | 5 U.S.C. §§ 13104(a), (d)(1)(A), (f)(3), 13106; 18 U.S.C. § 1346 (contingent) | H, Q, O, EE, CC, L, K, II, JJ |

The complaint additionally publishes **fourteen numbered Anticipated Responses** plus **five preemptive rebuttals** (Responses #2 below-median rate framing, #2b defense-prime sector-share, #12 donor-capture, #12a MUR 7062 distinguishability, #13 progressive credentials), addressing every defense class represented in `ro_khanna.v3_defense_arguments WHERE severity >= 7 AND status='open'`. Eleven of fourteen Responses are mitigated; one is open at moderate severity (Response #5 dual FARA / LDA registration); two are acknowledged-and-preempted. Zero fatal defenses remain. Per `.claude/rules/occ-complaint.md` §Anticipated Responses structure, class-coverage is the binding floor; sev-7 nuanced variants are held in red-team reserve.

The aggregate estimated economic gain to respondent's household from the conduct is bounded between approximately **$15.3 million (low) and $112.1 million (high)**, with a midpoint estimate of approximately **$63.7 million** and alpha over the S&P 500 benchmark of approximately **$28.2 million**. Disgorgement target: **$25.2M–$28.2M, Treasury-allocable.**

---

## Chamber-baseline disclosure (full candor)

Per `.claude/rules/peer-baseline.md` and `.claude/rules/occ-complaint.md` §Chamber-baseline disclosure (mandatory), every comparative-statistic Count discloses respondent's position on **both** chamber-wide and peer-cohort baselines in the same paragraph:

- **Khanna's late-filing rate (1.74%)** sits **below** the House chamber median (10.06%) AND **below** the active-trader peer-46 cohort median (5.96%). Both universes agree: the rate dimension is exculpatory.
- **Khanna's worst single-transaction delay (358 days)** sits essentially **at** chamber median (severity rank 108 of 210, P49.5) and **below** active-trader-cohort median (rank 32 of 46, P32.6). Both universes agree: the per-transaction-severity dimension is at-or-below median.
- **Khanna's aggregate dollar-weighted composite exposure (~$41.3 million)** sits at **chamber rank 15 of 210 (P93)** AND **active-trader cohort rank 5 of 43 (P91)**. Both universes agree: the composite dimension is the operative Count 1 axis.
- **Khanna's defense-prime trade share (1.24%)** sits at **peer-cohort median**. The complaint does not allege defense-sector over-concentration. Count 2's probative value lies in **timing** (NDAA enactment windows), **direction** (pre-passage accumulation against public NAY votes), and **HASC jurisdictional nexus**.

This pattern defeats any opposing-counsel attempt to pick the larger denominator and accuse selective sampling. The two-universe rule is canonical per `.claude/rules/peer-baseline.md`.

---

## Methodological correction trail (single candor paragraph)

Per `.claude/rules/occ-complaint.md` §When a v3_audit_finding affects a pleaded fact: earlier drafts of the complaint cited a **3,635-day** worst single-transaction delay figure and a successor **2,158-day** intermediate-corrected figure. Both were vacated. The 3,635-day figure was a Gemini year-digit parse-error artifact; remediation produced the 2,158-day figure; independent Tesseract OCR re-extraction + canonical-view amendment-cascade dedup then VACATED the severity-outlier framing entirely and anchored Count 1 on dollar-weighted composite exposure (the current $41.3M / chamber P93 / peer P91 framing). The two-correction trail is disclosed here for procedural candor, pre-empts "complainant's prior inconsistent position" attacks, and is documented in the methodology cover doc § 3.3 with the tightened mixed-date parse-error sentinel that prevents recurrence.

---

## What this complaint is NOT

- This is **not a final adjudication**. The Office of Congressional Conduct's mandate is preliminary review and (in second-phase review) referral to the House Committee on Ethics. The relief sought is OCC investigation + Committee on Ethics referral + parallel agency referrals, not a finding by OCC of any final violation.
- This is **not a criminal indictment**. The DOJ referral seeks the Public Integrity Section's review for the matters within its jurisdiction (18 U.S.C. § 207 post-employment review of five named ex-federal-employee donors; 18 U.S.C. § 1001 false-statement review of LD-203 certifications; 18 U.S.C. § 1346 honest-services consideration contingent on a Committee on Ethics scope finding on the Foundation question). DOJ retains exclusive prosecutorial discretion.
- This is **not a final transmission**. The packet is in pre-transmission form. The transmission posture remains **"draft until physically transmitted to the Office of Congressional Conduct, the Federal Election Commission, the House Committee on Ethics, and the Department of Justice"** — the document-level preamble's posture statement is load-bearing; nothing about this README being published, this packet being pushed to a private remote, or this packet being subtree-split into a standalone repo changes that posture.
- This is **not an attack on respondent's progressive policy posture**. The complaint expressly acknowledges respondent's no-PAC pledge, the No PAC Caucus, the No PAC Act, and respondent's own Member-stock-trading-ban legislation. The complaint is directed at the **disconnect between** respondent's public-facing posture and respondent's household-facing trading conduct, not at respondent's policy positions.

---

## Reviewer-kit ship-ready posture (current status)

- **Manifest**: 80/80 entries with substrate + sql_text + predicate_grep + element_id + theory_id + what_means / what_shows / first_seen_section. 76 with resolved fact_ids; 63 with resolved verification_ids; 4 computed-substrate-class for non-v3 verifier kinds.
- **Methodology cover**: 651 lines / 7 sections / 14 dedup-rule sub-sections + 30+ load-bearing scalar anchor table + worked end-to-end HUMANA 358-day example + 30-entry glossary + 12-exhibit reproducibility map + 11-pattern common-divergence diagnostic + chamber-baseline disclosure venue-specific template.
- **Reviewer kit**: 33 anchors / 15 verifier kinds. Frozen-mode: **31 OK / 0 DIVERGE / 0 ERROR / 0 FAIL / 2 MANUAL** (the 2 MANUAL are FEC `--live`-only). Drift gate: substrate=0 appendix=0 facts=0 across all 80 manifest entries.
- **Frozen substrate snapshots**: 9/9 covered substrates (statute / PTR audit / chamber audit / peer baseline / votes / IRS 990 / LDA contributions / PFD Schedule D liabilities / trade-PnL canonical scalars) date-stamped 2026-05-02; SHA-checksummed in `99_SHA256SUMS_OCC.txt`.
- **Class-2 OCR products bundle**: `data/ocr_products/` ships `MANIFEST.md` + `fetch_source_pdfs.py` + the cited Khanna TY2024 PFD (doc_id 8221318) Tesseract OCR text + 5 page renders + Schedule A cross-tax-year asset CSV + 114-PTR corpus index — sufficient for a reviewer to re-OCR every PDF-class substrate independently.
- **Public-substrate fetch recipe**: `fetch_substrate_occ.py` (~415 lines / 6 fetch classes: statute / house roll-calls / House Clerk PTR-PFD index / IRS 990-PF / OpenFEC REST / Senate LDA bulk) — re-fetches every class-1 substrate from primary sources for a cold-start reviewer.
- **Voice + citation-currency + vacated-severity invariants**: drift = 0 across body + parallel referrals + exhibit list + pre-flight report + methodology cover. Bare `OCE` matches occur only in permitted historical-narrative parentheticals at first mention; obsolete-form `5 U.S.C. App. § 10[N]` operative cites = 0; vacated 3,635 / 2,158 / "extreme outlier" framing = 0 in operative sections (single candor paragraph at § VI Response #2 is the methodology-cover analog endorsed by `.claude/rules/occ-complaint.md`).
- **Theory readiness**: 7/7 invariant per `mcp__facts__v3_theory_readiness(case='ro_khanna')`. Canonical 8/8 hashes invariant (F215 / F227 / F486 / F610 / F612 / F628 / F742 / F865 + retained predecessors F226 / F743).

**Open ship gates** (tracked at `prompts/K_ro_khanna_occ_complaint/TRACKER.md` SCORECARD):

- Phase B subtree split + standalone repo `kevinnbass/occ-khanna-complaint` (private) + tag `v1.0.0-pre-transmission`
- Phase C cold-start verification: fresh clone, `pip install requests`, `verify_anchors_occ.py` returns 31 OK / 2 MANUAL / 0 DIVERGE in frozen mode AND 33 OK / 0 DIVERGE in `--live` mode (the 2 MANUAL stubs are the FEC committee-resolve / Schedule-E-aggregate kinds, which become OK with internet access)

---

## License + redistribution

This complaint is a public-record submission to the Office of Congressional Conduct (with parallel referrals to the Federal Election Commission, the House Committee on Ethics, and the Department of Justice). Reviewers may freely redistribute, reformat, and re-host. The author requests that downstream reproducers preserve the **provenance manifest** (`_provenance_index_occ.json`) and **SHA-256 integrity manifest** (`99_SHA256SUMS_OCC.txt`) intact when forwarding the packet, so that reviewers downstream of the redistribution can verify that the reproduced figures resolve against the same fact-store entries the original reviewer saw.

---

## Contact

Substantive questions about the complaint, the underlying fact-store, the reproducibility kit, or the provenance manifest may be directed to the Complainant via the contact information in **`OCC_COMPLAINT_KHANNA.md` § Verification**.
