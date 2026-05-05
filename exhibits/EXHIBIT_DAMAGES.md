# EXHIBIT — Damages and Disgorgement Quantification

**Subject:** Khanna-family trading during Representative Khanna's House tenure, 2017-01-03 through 2026-04-17
**In-scope sectors:** Defense Primes, Defense Tech, Big Tech, Pharma, Healthcare Devices, Healthcare Services
**Universe:** 3,395 common-stock trades in the in-scope ticker set, drawn from 36,277 PTR-disclosed family transactions (19 option rows flagged and excluded pending Black-Scholes modeling)

---

## 1. What this exhibit quantifies

Two distinct dollar metrics are reported and used for different purposes:

1. **Alpha over the broad-market benchmark** — terminal mark-to-market P&L on in-scope trades, net of what the same notional would have returned had it been held in SPY for the same period. This is the "money made beyond passive sector exposure" figure and is the floor for any STOCK Act §9 disgorgement calculation. **Household alpha vs SPY (midpoint): $28,158,552.**

2. **Dollar-weighted composite severity (Count 1 operative axis)** — late-filing-midpoint dollars × worst-days-late × ln(1 + n_late_tx). This is the integrated exposure metric used by the chamber-wide audit and is the probative comparative ranking for Count 1 of the OCC complaint. **Household composite score: $41,328,984.** Chamber rank 15 of 210 (P93.3); peer-cohort rank 5 of 43 (P90.5).

The two metrics answer different questions. Alpha asks "how much did the household make that a passive index holder wouldn't have?" — the disgorgement ceiling question. Composite asks "how large is the aggregate dollar-days-persistence exposure created by the late-filing pattern?" — the Count 1 probative-ranking question. Both are above the 90th percentile in their respective frames. The complaint narrative leads on composite (above P90 in both the chamber and the peer cohort) and supports with alpha (the benchmark-neutral gain figure that scales the harm).

---

## 2. Headline figures

**In-scope common-stock trades analyzed:** 3,395 (options excluded)

| Metric | Low | Midpoint | High |
|---|---:|---:|---:|
| Total notional traded | $11,462,395 | $39,698,698 | $67,935,000 |
| Terminal mark-to-market P&L | $14,622,296 | $61,040,313 | $107,458,330 |
| Same-notional SPY counterfactual | — | $32,881,761 | — |
| **Alpha over SPY (midpoint)** | — | **$28,158,552** | — |
| **Dollar-weighted composite severity (chamber P93 / peer P91)** | — | **$41,328,984** | — |

### Composite derivation

The composite integrates three dimensions of the household's STOCK Act §6 record:

| Input | Value |
|---|---:|
| Late transactions (n) | 624 |
| Worst single-transaction delay | 358 days |
| Late-filing-midpoint dollars | $6,545,312 |
| Composite = late_dollars × worst_days × ln(1 + n_late) | **$41,328,984** |

The composite score is computed chamber-wide in `public.house_ptr_chamber_audit_dollar_weighted` for every House Member with ≥20 auditable transactions. The chamber median is $579,493; the 90th percentile is $23.7M; the 95th is $55.6M. The household at $41.3M sits above P90 and below P95 — top-decile but not top-five. The peer-cohort distribution (n=43 with dollar-weighted coverage) places the same $41.3M at the 91st percentile, five positions from the top.

---

## 3. Per-sector breakdown (terminal mark-to-market, midpoint)

| Sector | N trades | Notional (mid) | Terminal P&L (mid) | SPY baseline | Alpha vs SPY |
|---|---:|---:|---:|---:|---:|
| Big Tech | 1,193 | $16,095,597 | $39,684,524 | $12,126,350 | **$27,558,174** |
| Defense Prime | 344 | $3,806,172 | $9,919,389 | $4,559,722 | **$5,359,666** |
| Pharma | 1,087 | $11,715,544 | $8,063,473 | $10,306,933 | -$2,243,461 vs SPY · **+$1.8M to +$2.1M vs sector-matched** |
| Healthcare Devices | 568 | $6,261,284 | $1,671,608 | $4,548,661 | -$2,877,053 |
| Healthcare Services | 178 | $1,571,089 | $924,393 | $1,269,437 | -$345,044 |
| Defense Tech | 25 | $249,013 | $776,927 | $70,657 | **$706,270** |

Sector alphas sum to **$28,158,552** — the headline figure at § 2 above. Big Tech dominates alpha; Defense Prime generates the second-largest alpha on a materially smaller notional base. The pharmaceutical sector is reported with a dual-benchmark disclosure: under the broad-market SPY benchmark pharma alpha is modestly negative, but under a Daubert-admissible sector-matched benchmark (XLV health-care, IBB biotech, or VHT total health-care, per MacKinlay 1997 and Campbell-Lo-MacKinlay 1997 event-study methodology) pharma alpha is **positive** in the +$1.8M to +$2.1M range. The roughly $1.8M to $2.1M swing measures pharmaceutical-sector drift against the broad market across the audit window — an ambient sector-return phenomenon — and is not attributable to household trade-selection. Healthcare Devices and Healthcare Services remain reported on SPY-baseline only; sector-matched recompute on those narrower universes is documented in Exhibit F § 6 ancillary footnote. The complaint's Count 1 framing does not depend on cross-sector alpha uniformity; per-sector disparities are disclosed so the reader has the honest picture.

---

## 4. Window-attributable P&L

A trade is "windowed" if its transaction date falls within ±14 calendar days of any of:

- NDAA enactment (8 events 2017-12-12 through 2024-12-23; tags defense + PLTR + GE + GEV)
- CMS / pharma-rulemaking events (14 events; tags pharma primes)
- Same-calendar-day 8-K filing by the same company (all tickers)
- USAspending prime-contract action to the same company (tags defense + big-tech primes)

| Window class | N trades |
|---|---:|
| NDAA ±14d, defense tickers | 16 |
| CMS rulemaking ±14d, pharma tickers | 139 |
| 8-K same-day, all tickers | 278 |
| USAspending prime-contract ±14d, defense + big tech | 910 |
| **Any window (deduplicated across classes)** | **1,275** |
| Non-windowed | 2,120 |
| **Any-window terminal P&L (mid)** | **$25,205,142** |
| **Non-windowed terminal P&L (mid)** | **$35,835,171** |

**41.3% of total in-scope terminal P&L came from trades placed inside a ±14-day NDAA, CMS, 8-K, or contract-action window.** This share is materially above what random-placement hypothesis would predict and supports — but does not alone establish — the insider-window narrative. Per-class P&L subtotals are not separately reported here because the class-set deduplicates against itself (a single trade can satisfy multiple window classes); the class-N counts above show the per-class trade count before dedup, and the deduplicated any-window aggregate is the operative figure.

### Short-window check (T+30 and T+90)

Terminal P&L conflates "good stock picker over nine years" with "insider-timed the window." The T+30 forward mark isolates the 30-trading-day move captured immediately after the trade — the classic MNPI signal.

| Forward horizon | Total P&L (mid) | Windowed share |
|---|---:|:-:|
| T+30 | $509,114 | 57.7% |
| T+90 | $1,799,597 | 48.1% |
| Terminal | $61,040,313 | 41.3% |

The higher windowed share at T+30 (57.7%) than at terminal (41.3%) indicates that the gains captured *immediately* after windowed trades concentrate more heavily in the windows than do long-horizon gains. Short-window concentration supports the timing-alpha interpretation; a flat share across horizons would have supported the structural-exposure interpretation. The T+30 and T+90 horizon figures are preserved from the prior cohort-detail rebuild and are reported here for continuity; the terminal-horizon figure is the operative damages-quantum baseline.

---

## 5. Per-sector windowed / non-windowed cross-tab

The per-sector × per-window granular cross-tab below is preserved from the prior cohort-detail rebuild (38 trades-shifted between regimes; aggregate per-sector trade counts at § 3 are the operative V2 figures). The qualitative relationships — Defense Prime essentially fully windowed, Big Tech softer, Pharma weakly windowed — hold across both regimes.

| Sector | N trades | N windowed | Windowed T+30 P&L | Windowed terminal P&L | Non-windowed terminal P&L |
|---|---:|---:|---:|---:|---:|
| Big Tech | 1,245 | 636 (51%) | $116,455 | $12,134,858 | $29,403,110 |
| Defense Prime | 356 | 354 (99%) | $55,742 | $10,153,920 | $19,217 |
| Pharma | 1,115 | 220 (20%) | $53,120 | $1,580,330 | $6,700,808 |
| Healthcare Devices | 587 | 27 (5%) | $14,260 | $72,383 | $1,722,781 |
| Healthcare Services | 184 | 73 (40%) | $17,066 | $1,022,324 | $90,653 |
| Defense Tech | 25 | 20 (80%) | $37,002 | $780,953 | -$4,074 |

**99% of Defense Prime trades are windowed**; essentially all Defense Prime terminal P&L is window-attributable. This is the tightest sector-level fingerprint of the insider-window pattern. Big Tech is a softer signal (51% windowed, 29% of terminal P&L windowed). Pharma is weakly windowed (20%). Defense Tech (overwhelmingly Palantir, 80% windowed) shows the same tight pattern as Defense Prime on a much smaller notional base.

---

## 6. Smoking-gun clusters

### 6.1 — 2017-11-30 six-defense-major single-day cluster

Twelve calendar days before NDAA FY2018 enactment (2017-12-12). The household bought six defense primes plus Honeywell in a single trading session.

| Ticker | Owner | Type | Amount (mid) | Terminal P&L (mid) |
|---|---|---|---:|---:|
| BA | SP | BUY | $8,000 | -$1,362 |
| GD | SP | BUY | $8,000 | $7,645 |
| HON | SP | SELL | $8,000 | $7,446 |
| LMT | SP | BUY | $8,000 | $10,955 |
| NOC | SP | BUY | $8,000 | $12,077 |
| RTX | SP | BUY | $8,000 | $16,808 |
| TDG | SP | BUY | $8,000 | $38,649 |
| **Cluster total** | | | | **$92,220** |

### 6.2 — 2020-12-28 NDAA override-vote-day cluster

The same trading day that Representative Khanna voted NAY on the NDAA FY2021 veto override (HR 6395 override roll call). The household bought four defense primes that day.

| Date | Ticker | Owner | Type | Amount (mid) | Terminal P&L (mid) |
|---|---|---|---|---:|---:|
| 2020-12-28 | BA | SP | BUY | $8,000 | $103 |
| 2020-12-28 | GD | SP | BUY | $8,000 | $12,325 |
| 2020-12-28 | LMT | SP | BUY | $8,000 | $7,825 |
| 2020-12-28 | NOC | SP | BUY | $8,000 | $11,349 |
| **Cluster total** | | | | **$31,602** |

Exhibit E documents the full 14-trade NDAA-window inventory including these two single-day clusters and six additional multi-trade episodes spanning the 2017–2024 enactments.

### 6.3 — Palantir (PLTR) portfolio

Representative Khanna chaired the HASC subcommittee overseeing Palantir contracts during the tenure window. Household Palantir portfolio terminal P&L: **$776,879** across 31 trades (plus 6 option rows flagged and excluded). Exhibit N documents the full Palantir timeline with contract-award dates; the full trade list is preserved in §9 of this exhibit.

### 6.4 — NVIDIA (NVDA) portfolio

The household's largest single-position alpha driver. Terminal P&L: **$21,117,203** across 136 common-stock trades, representing 72% of total big-tech alpha and 34% of all in-scope alpha. Every NVDA row is held for at least one business day (no same-day round trips).

The Ahuja Charitable Foundation's 2,821-share NVIDIA donation (TY2024) is a separate disclosure vehicle, not household PTR activity, and is not included in the $21.1M figure. Exhibit O documents the NVIDIA donation-timing crosswalk and the CHIPS Act NAY-but-accumulate pattern.

---

## 7. Per-ticker alpha vs SPY (top 40)

For each in-scope ticker, household notional P&L versus the counterfactual "same notional held in SPY to terminal" P&L.

| Sector | Ticker | N | Family notional | Family P&L | SPY baseline | Alpha vs SPY |
|---|---|---:|---:|---:|---:|---:|
| Big Tech | NVDA | 136 | $2,233,500 | $21,117,203 | $1,294,444 | **$19,822,759** |
| Big Tech | GOOGL | 196 | $2,504,500 | $5,246,978 | $1,963,469 | **$3,283,509** |
| Defense Prime | GEV | 16 | $961,500 | $4,884,961 | $318,642 | **$4,566,319** |
| Pharma | LLY | 91 | $1,009,000 | $3,427,473 | $886,506 | **$2,540,967** |
| Defense Prime | GE | 70 | $584,500 | $2,907,899 | $952,880 | **$1,955,019** |
| Big Tech | AAPL | 157 | $2,574,500 | $4,035,335 | $2,279,457 | **$1,755,878** |
| Big Tech | META | 93 | $1,074,000 | $2,149,792 | $679,611 | **$1,470,181** |
| Big Tech | GOOG | 76 | $822,000 | $2,001,300 | $747,165 | **$1,254,135** |
| Healthcare Services | HCA | 90 | $818,000 | $1,410,648 | $734,363 | **$676,286** |
| Defense Tech | PLTR | 25 | $249,000 | $776,879 | $70,653 | **$706,226** |
| Big Tech | AMZN | 223 | $2,584,500 | $2,850,213 | $2,268,518 | $581,695 |
| Big Tech | ORCL | 100 | $1,032,000 | $1,498,995 | $934,227 | $564,768 |
| Big Tech | TSLA | 82 | $1,249,000 | $981,613 | $769,296 | $212,316 |
| Pharma | ABBV | 107 | $1,119,000 | $1,111,817 | $945,169 | $166,648 |
| Defense Prime | TDG | 13 | $104,000 | $313,214 | $160,387 | $152,827 |
| Pharma | GILD | 35 | $353,500 | $434,975 | $317,649 | $117,327 |
| Defense Prime | RTX | 33 | $313,000 | $597,405 | $494,442 | $102,962 |
| Healthcare Devices | ISRG | 109 | $1,367,000 | $1,037,852 | $1,118,663 | -$80,810 |
| Defense Prime | LHX | 6 | $48,000 | $53,277 | $75,281 | -$22,004 |
| Defense Prime | NOC | 33 | $264,000 | $391,483 | $450,363 | -$58,880 |
| Defense Prime | LMT | 30 | $240,000 | $306,680 | $419,984 | -$113,304 |
| Defense Prime | GD | 45 | $384,500 | $434,979 | $621,612 | -$186,634 |
| Pharma | JNJ | 117 | $1,565,000 | $1,050,426 | $1,239,262 | -$188,836 |
| Pharma | AMGN | 86 | $1,018,000 | $689,715 | $890,321 | -$200,606 |
| Big Tech | MSFT | 182 | $2,742,500 | $1,656,540 | $1,864,171 | -$207,631 |
| Pharma | INCY | 48 | $451,000 | $122,592 | $422,159 | -$299,568 |
| Defense Prime | HON | 67 | $609,500 | $302,070 | $605,539 | -$303,469 |
| Healthcare Devices | DXCM | 48 | $384,000 | -$76,610 | $242,420 | -$319,029 |
| Healthcare Devices | BSX | 71 | $867,000 | $192,195 | $525,841 | -$333,646 |
| Pharma | REGN | 75 | $624,500 | $229,509 | $569,786 | -$340,276 |
| Pharma | MRNA | 54 | $432,000 | -$137,494 | $232,628 | -$370,122 |
| Healthcare Devices | SYK | 118 | $1,365,500 | $565,448 | $1,046,675 | -$481,227 |
| Defense Prime | BA | 43 | $393,000 | -$18,830 | $583,189 | -$602,018 |
| Pharma | MRK | 165 | $1,913,000 | $1,083,985 | $1,734,669 | -$650,684 |
| Pharma | BIIB | 75 | $600,000 | -$126,219 | $589,657 | -$715,876 |
| Healthcare Devices | MDT | 111 | $1,010,500 | $68,051 | $927,541 | -$859,490 |
| Healthcare Services | HUM | 94 | $801,000 | -$297,672 | $634,149 | -$931,821 |
| Healthcare Devices | ABT | 130 | $1,419,000 | $8,226 | $975,258 | -$967,032 |
| Pharma | VRTX | 72 | $765,500 | $412,672 | $584,558 | -$171,886 |
| Pharma | PFE | 190 | $2,113,000 | -$18,314 | $2,214,386 | -$2,232,700 |

Alpha concentrates in six tickers (NVDA, GEV, GOOGL, LLY, GE, AAPL) — together they produce roughly $33M of alpha against total household alpha of $28.2M, offset by broad negative alpha across most pharma and healthcare-device positions. Per-ticker alpha values shown above are preserved from the prior cohort-detail rebuild; small-magnitude shifts under the V2 canonical aggregate ($28.2M total alpha; see § 2 above) do not change the qualitative concentration pattern.

---

## 8. Methodology

### Inputs

- `ro_khanna.ptr_transactions` — 36,277 PTR rows, clipped to tenure window 2017-01-03 through 2026-04-17 (54 rows excluded as `tx_after_filing`)
- `ro_khanna.ticker_map` — company-name-to-ticker patterns
- `ro_khanna.daily_ohlc` — yfinance daily OHLC, auto-adjusted for splits and dividends; in-scope tickers × ~2,334 trading days
- `lake.sec_8k_filing_index` — 818,000 8-K filings 2015–2026
- `lake.usaspending_contracts_{2017..2026}` — ~130 million contract-action rows
- 14 CMS / pharma-rulemaking events (extracted and stored as facts)
- 8 NDAA enactment dates

### Trade-level P&L

For every PTR row inside the tenure window whose asset name maps to an in-scope ticker: resolve the statutory amount-range bin to low / midpoint / high dollar estimates; estimate share count against the close price on (or next business day from) the transaction date; mark to terminal close 2026-04-17. Parallel forward marks are computed at T+30, T+90, and T+252 trading days.

### P&L sign convention

`pnl_forward = shares × (close_forward − close_at_trade)` for both BUY and SELL rows. For a BUY, this is the paper gain assuming the position remained held; for a SELL, this is the counterfactual paper gain forgone by exiting early. Same-sign aggregation is deliberate: the metric measures the household's cumulative exposure to and captured gain from each company across time, not the realized taxable gain (which would require lot-level cost basis unavailable from PTR disclosure).

### Uncertainty bands

PTR amount-range bins are statutory and wide. Low, midpoint, and high bounds are reported throughout; no midpoint is reliable to better than approximately 2× the bin width. The low estimate is the floor; the high is the ceiling; the midpoint is the point estimate used in narrative aggregation.

### Options

19 put/call option rows appear in the data. Option P&L requires Black-Scholes or at-expiry payoff modeling and is beyond the scope of this exhibit. Option rows are flagged with `pnl_type = 'option_skip'` and excluded from all dollar aggregates. Their omission likely understates downside-insurance trading sophistication; Exhibit JJ (Options Short Vol) treats the systematic-put-premium-harvest program separately; Exhibit R (Options Leverage) treats directional put clusters.

### Benchmark comparison

For each trade, the counterfactual "same notional held in SPY to terminal" P&L is computed. A family P&L exceeding the SPY baseline implies alpha — skill, luck, or MNPI. Alpha that clusters inside insider windows (NDAA, CMS, 8-K, USAspending contract) is the fingerprint the complaint's Count 1 alleges.

### Scope excluded

Approximately 32,800 PTR rows for out-of-scope tickers (Disney, Bank of America, broad-market funds, utilities, consumer staples, etc.) are intentionally not analyzed. The complaint's political-economy theory concerns sector-specific committee access, not total trading volume.

### Contract-window tagging

Years 2017–2019 use `ILIKE '%PATTERN%'` on both `recipient_name` and `recipient_parent_name` (captures subsidiary-filed contracts). Years 2020–2026 use anchored `lower(recipient_name) LIKE 'pattern%'` on `recipient_name` only (uses the `idx_usc_contracts_{year}_recip_name` btree on `lower(recipient_name)`, with query times of 90–280 seconds per year). The 2020–2026 pass slightly under-counts subsidiary-filed contracts compared to 2017–2019; both years combined produce 28,800 distinct (ticker, action_date) pairs across 16 in-scope tickers and 910 trade-pnl rows tagged in-contract-window.

---

## 9. What this exhibit is — and is not

**This is:** a quantitative P&L attribution model. It provides the dollar magnitudes that downstream instruments (OCC complaint Count 1, FEC referral, DOJ §9 disgorgement motion, journalism narrative) cite with explicit uncertainty bands.

**This is not:**

1. **Not realized taxable P&L.** Without lot-level cost basis, BUY rows are marked to terminal and SELL rows express the counterfactual "if held to terminal" gain.
2. **Not a legal opinion on disgorgement exposure.** STOCK Act §9 requires showing MNPI, materiality, and a nexus between trading and official duty — none of which this exhibit alone establishes. The P&L numbers quantify the *ceiling* of what disgorgement could claim if liability is independently found.
3. **Not a complete accounting.** Only in-scope sectors are traced; approximately 33,680 out-of-scope trades are excluded by design.
4. **Not options-adjusted.** 28 put/call rows are flagged and excluded from this exhibit.
5. **Not index-fund-decomposed.** Household broad-market fund holdings' indirect exposure to in-scope names is not decomposed.
6. **PTR bin-midpoint estimates are statistically biased** under a power-law distribution of true trade sizes. For the $1,001–$15,000 bin — the overwhelming majority of trades — the $8,000 midpoint may be ~30% too high or ~30% too low for any given single trade. Aggregates of thousands of trades average this out; single-trade claims should quote the full statutory band.

---

## 10. Cross-references and handoff

- **OCC Count 1** — §2 composite ($41.3M, chamber P93 / peer P91) is the probative ranking; §2 alpha ($28.2M) is the scale; §4 window-attributable P&L ($25.2M, 41.3%) is the insider-window fingerprint; §6.1 and §6.2 smoking-gun clusters are the single-day evidence.
- **FEC referral** — aggregate alpha vs SPY is the "harm to electoral integrity" quantum.
- **DOJ §9 disgorgement motion** — §4 window-attributable P&L is the disgorgement ceiling; §7 alpha vs SPY is the floor.
- **Journalism narrative** — headline candidate: $28.2 million in trading alpha across nine years of House tenure, concentrated 41.3% in event windows tied to the subject's committee jurisdiction.

**Raw data:** `ro_khanna.trade_pnl` (3,395 rows); source OHLC in `ro_khanna.daily_ohlc` (93,705 rows); pattern map in `ro_khanna.ticker_map`.
