# EXHIBIT M — Same-Day 8-K Trading Pattern, Chamber-Wide

**Subject:** Rep. Ro Khanna (D-CA-17), household transactions executed on the same calendar day that the issuer filed an SEC Form 8-K
**Counts supported:** Count 1 (STOCK Act §§3–4 MNPI), Count 3 (financial-interest conflicts at asset-jurisdiction overlap)
**Sources:** `lake.sec_8k_filing_index`, `lake.house_ptr_transactions`, `ro_khanna.cik_ticker_map` (40 of 44 in-scope tickers bridged); figures replayed against the live substrate snapshot of 2026-04-25 per the §6 documented `asset_name ILIKE` fuzzy bridge.

---

## 1. Why this exhibit exists

The SEC Form 8-K is the current-report filing a public company must file between its quarterly and annual reports whenever a material event occurs — earnings releases, executive changes, M&A announcements, material contract awards, regulatory actions, restructurings. Item codes such as 1.01 (entry into material definitive agreement), 2.01 (acquisition or disposition), 2.02 (results of operations), 5.02 (director or officer departure), 7.01 (Reg FD disclosure), and 8.01 (other events) frequently move the issuer's stock price.

A household trade dated on the same calendar day as the issuer's own 8-K filing is a recognized signature of information-advantaged trading. It does not by itself prove that the household acted on material non-public information. It does establish that one of two things is true: either the household received the 8-K's information before the filing crossed the SEC wire, or the household is repeatedly co-incident with material disclosures at a frequency that does not align with passive index rebalancing, broker-discretion-only management, or random timing.

This exhibit quantifies the Khanna household's same-day-8-K intersection, places the household against all 357 House Members with PTR filings in the period, and reports the sector decomposition and the single-day clusters that anchor Count 1's per-trade pattern evidence.

---

## 2. Headline result — chamber rank #1 by absolute count

Across the House chamber universe with PTR disclosures in the 2017–2026 window, the subset with statistical stability (≥20 transactions in the 40 mapped in-scope tickers) contains 96 Members. Within that 96-Member chamber universe (figures as of the 2026-04-25 substrate snapshot):

| Member | District | Transactions in mapped tickers | Same-day-8-K matches | Rate |
|---|---|---:|---:|---:|
| **Khanna, Rohit** | **CA-17** | **3,429** | **186** | **5.42%** |
| McCaul, Michael | TX-10 | 621 | 43 | 6.92% |
| Gottheimer, Josh | NJ-05 | 696 | 33 | 4.74% |
| Roe, David | TN-01 | 447 | 16 | 3.58% |
| Cisneros, Gilbert | CA-31 | 202 | 11 | 5.45% |
| Langevin, James | RI-02 | 52 | 10 | 19.23% |
| MacArthur, Thomas | NJ-03 | 109 | 10 | 9.17% |
| Manning, Kathy | NC-06 | 166 | 10 | 6.02% |
| Renacci, James | OH-16 | 284 | 10 | 3.52% |
| Cisneros, Gilbert | CA-39 | 79 | 9 | 11.39% |

**186 same-day-8-K matches is the chamber maximum** across the 96 qualifying Members. The closest peer (Michael McCaul, TX-10) has 43 such matches — fewer than a quarter. The third-ranked Member (Josh Gottheimer, NJ-05) has 33, fewer than a fifth. The Khanna household's absolute count is **4.3× the second-place Member and 5.6× the third-place Member**.

### Rate-dimension candor (two-universe disclosure)

Distribution of the same-day-8-K rate across the 96-Member chamber universe (≥20 ticker-bridged transactions):

| Statistic | Value |
|---|---:|
| Mean | 4.71% |
| Median | 4.50% |
| P75 | 6.93% |
| P95 | 11.43% |
| Maximum | 19.23% (small-denominator Member, n=52) |
| **Khanna** | **5.42% — chamber rank 36 of 96, P62** |

Distribution of the same-day-8-K rate across the 46-Member active-trader peer cohort (39 peers with the same-day-8-K dimension populated for percentile stability):

| Statistic | Value |
|---|---:|
| P25 | 2.90% |
| P50 | 3.83% |
| P75 | 4.77% |
| P90 | 5.19% |
| P95 | 9.52% |
| **Khanna** | **5.06% — cohort P89, above P75 but below the top decile** |

On the rate dimension, both universes converge: the household's rate sits above each universe's median and above the active-trader cohort's 75th percentile, but below the chamber 75th percentile and below the cohort top decile. The rate posture is above-median in both universes; it is not extreme on either. The case this exhibit supports is therefore not rate-uniqueness. It is the conjunction of (a) **absolute count** — 186 distinct same-day-8-K trades, the chamber maximum across the 96-Member ticker-bridged universe; (b) **ticker-specificity** — the household's same-day intersections concentrate on issuers in sectors under the subject's House Armed Services, House Oversight, and House Science-Space-Technology committee jurisdictions, rather than dispersing randomly across the Russell 1000; and (c) **composite-pattern generality** — the same-day-8-K finding is structurally parallel to the NDAA-enactment-window pattern (Exhibit E), the FDA advisory-committee-window pattern (Exhibit X), the CMS-rulemaking-window pattern (Exhibit F), and the aligned-direction Form 3/4/5 same-day pattern (Exhibit Z). The rate disclosure is included here in the same posture as Count 1's chamber-baseline paragraph: the two-universe rate context is disclosed so that opposing counsel cannot frame the absolute-count finding as cherry-picked.

---

## 3. Sector decomposition

The 186 distinct household trades that have at least one same-day-8-K coincidence fall across five sectors. Some trades match multiple 8-Ks filed by the same issuer on the same calendar day (for example, a same-day earnings release plus a same-day Reg FD disclosure plus a same-day officer-departure notice); those collapse to 205 distinct trade-by-8-K pairs against 186 distinct trades (figures as of the 2026-04-25 substrate snapshot).

| Sector | Distinct trades with same-day 8-K | Trade × 8-K pairs |
|---|---:|---:|
| Big Tech | 64 | 76 |
| Pharma | 55 | 58 |
| Defense Prime | 27 | 29 |
| Healthcare Devices | 27 | 28 |
| Healthcare Services | 13 | 14 |
| **Total (deduped)** | **186** | **205** |

The Big Tech sector accounts for the largest share of the same-day-8-K intersection (approximately 34% of the total), with Pharma a close second (approximately 30%). Defense Prime contributes approximately 14.5%; together the two healthcare sectors contribute approximately 21.5%. The composite picture is a household same-day-8-K footprint that spans every sector under the subject's House Armed Services, House Oversight, and House Science-Space-Technology committee jurisdictions, with no single sector accounting for a majority. The Defense-Prime concentration documented in Exhibit E (NDAA enactment windows) is a separate per-issuer-event pattern: the NDAA-window pattern anchors on ±14 days around eight legislative enactment dates, while the same-day-8-K pattern anchors on per-issuer corporate-disclosure events (earnings, contract wins, regulatory actions) that may or may not fall inside an NDAA window. The two patterns reinforce each other — several of the 14 NDAA-window trades documented in Exhibit E also intersect same-day 8-Ks from the issuer in question — but each stands independently as a distinct per-trade evidentiary pattern.

### Year-by-year

| Year | Big Tech | Pharma | Defense Prime | Healthcare Devices | Healthcare Services | Total |
|---|---:|---:|---:|---:|---:|---:|
| 2017 | 3 | 4 | 1 | 3 | 1 | 12 |
| 2018 | 6 | 9 | 8 | 2 | — | 25 |
| 2019 | 1 | 4 | 5 | 2 | 1 | 13 |
| 2020 | 8 | 7 | 4 | 1 | 2 | 22 |
| 2021 | 1 | 7 | 6 | 3 | — | 17 |
| 2022 | 10 | 4 | 1 | 3 | 3 | 21 |
| 2023 | 8 | 8 | — | 2 | 1 | 19 |
| 2024 | 9 | 2 | 1 | 2 | 2 | 16 |
| 2025 | 11 | 8 | — | 2 | 3 | 24 |
| 2026 YTD | 7 | 2 | 1 | 7 | — | 17 |

The pattern is sustained across the full tenure. Annual totals range from 12 (2017) to 25 (2018). The pattern does not concentrate in a single year or a single administration; Big Tech is the leading sector in 2022, 2023, 2024, 2025, and 2026 YTD, while Defense Prime led in 2018–2019 and Pharma is consistently the second or third contributor across most years.

---

## 4. Selected Big-Tech matches

The Big-Tech sub-pattern is the second-largest sector contribution and the most recent-in-time. Sample household trades executed on the same calendar day that the issuer filed an 8-K:

| Date | Ticker | Owner | Side | Amount | Issuer |
|---|---|---|---|---|---|
| 2026-01-29 | AAPL | SP | BUY | $15,001–$50,000 | Apple Inc. |
| 2026-01-23 | NVDA | DC | BUY | $1,001–$15,000 | NVIDIA CORP |
| 2025-12-05 | AAPL | DC | SELL | $1,001–$15,000 | Apple Inc. |
| 2025-11-20 | AMZN | SP + DC | both SELL | $1,001–$15,000 each | AMAZON COM INC |
| 2025-09-05 | GOOG | DC | BUY | $15,001–$50,000 | Alphabet Inc. |
| 2025-07-01 | MSFT | SP | BUY | $1,001–$15,000 | MICROSOFT CORP |
| 2025-01-22 | MSFT | DC | SELL | $50,001–$100,000 | MICROSOFT CORP |
| 2024-08-06 | GOOGL | SP + DC, mixed BUY/SELL | three trades | $1,001–$15,000 each | Alphabet Inc. |
| 2024-06-07 | NVDA and GOOGL | DC | both SELL | $1,001–$15,000 each | NVIDIA CORP + Alphabet Inc. |

The 2024-08-06 Alphabet triplet — three distinct household trades on a single calendar day, in opposite directions, coincident with an Alphabet 8-K — is among the more compact Big-Tech intra-day sub-patterns in the record. The 2024-06-07 cross-issuer pair — two distinct 8-Ks from two distinct issuers on the same day, with one household account trading in both — is the next in compactness.

---

## 5. Top single-day clusters, all sectors

| Date | Distinct trades with same-day 8-K | Trade × 8-K pairs |
|---|---:|---:|
| 2018-10-25 | **6** | 7 |
| 2024-08-06 | 3 | 6 |
| 2019-04-29 | 3 | 5 |
| 2025-01-22 | 3 | 4 |
| 2017-05-02 | 3 | 3 |
| 2018-05-08 | 3 | 3 |
| 2021-04-20 | 3 | 3 |
| 2021-08-17 | 3 | 3 |
| 2021-11-02 | 3 | 3 |
| 2022-01-11 | 3 | 3 |
| 2023-08-03 | 3 | 3 |
| 2026-01-29 | 3 | 3 |

The 2018-10-25 cluster — 6 distinct same-day-8-K trades in a single trading session, against 7 trade-by-8-K pairs — is the largest intra-day intersection in the 2017–2026 record. The 2024-08-06 cluster of 3 distinct trades against 6 pairs is the most pair-dense daily cluster: a single trading day on which household activity in three positions intersected six separate 8-K filings filed by issuers in the household universe. A defensible reading of the 2018-10-25 entry is that the household cycled through six mapped-ticker positions on a single rebalancing day and six issuers happened to file 8-Ks on the same calendar day. An adversarial reading is that the household traded into and out of six covered positions on a day concentrated with material corporate disclosures across the family's universe. The exhibit reports the number without committing to either reading; the probative value is in the aggregate count, not any single day's interpretation.

---

## 6. Methodology and limits

### Match logic

1. **CIK-to-ticker bridge.** For each of the 44 in-scope tickers, identify the SEC CIK whose company name fuzzy-matches the same `asset_name` ILIKE pattern used in the household PTR catalog and which has the largest 8-K filing volume in `lake.sec_8k_filing_index` (rank 1 by 8-K count, to deduplicate defunct subsidiaries, ADR shells, and similarly-named companies). 40 of 44 tickers map cleanly (91%); the four unmapped tickers fall through because the SEC registrant name uses a holding-company shell that does not pattern-match the operating-subsidiary brand.
2. **Same-day join.** For each household PTR transaction with a mapped ticker, find every 8-K filing where the issuer CIK matches the ticker's CIK and the 8-K `date_filed` matches the PTR `transaction_date`. Distinct-trade counts are taken at the `transaction_id` grain (or, equivalently, the `lake.house_ptr_transactions_canonical` tx-key `(filer, asset_name, transaction_date, transaction_type, owner)`); pair counts retain one row per (trade × 8-K filing).
3. **Chamber rollup.** For each House Member with ≥20 transactions in mapped tickers, count the distinct same-day-8-K matches and compute the rate.

### Coverage limits

- **Item codes are not in the lake.** `lake.sec_8k_filing_index` carries `(cik, company_name, form_type, date_filed, filename, filing_url)`. The item codes live in each filing's body text at `filing_url`. Per-filing fetch via the SEC EDGAR REST API is deferred to a future materiality-enrichment session. A per-item-tier filter would allow the exhibit to promote specific matches to greater weight where the issuer's 8-K item is materially price-moving (e.g., Item 2.02 earnings, Item 5.02 officer departure, Item 8.01 material event).
- **Strict same-day window.** This exhibit reports only the strict calendar-day intersection. Some material patterns are T+1 or T−1 — announce-then-trade or trade-then-announce. Broadening to ±1 day would increase the count by an estimated 2–3× but would introduce timing-sequence noise. The conservative same-day count is the operative figure.
- **No false-positive pollution.** The 91% ticker-mapping coverage accepts a small false-negative rate (four unmapped tickers) to avoid false-positive matches from overly broad fuzzy matching.

---

## 7. Evidentiary value

This exhibit shows, on its own:

1. The household executed **186 distinct same-day-8-K trades across 2017–2026**, corresponding to 205 trade-by-8-K pairs, against 35 mapped issuers across five sectors (figures as of the 2026-04-25 substrate snapshot).
2. That count is the chamber maximum across all 96 House Members with ≥20 transactions in mapped tickers — **4.3× the next-highest Member** (McCaul TX-10 at 43) and **5.6× the third-highest** (Gottheimer NJ-05 at 33). The rank-by-absolute-count finding is not advanced as proof of per-trade outlier-uniqueness; on the rate dimension, the household sits at chamber percentile 62 and active-trader-cohort percentile 89 — above-median in both universes but not extreme. The probative force this exhibit supports is the conjunction of the absolute-count finding with **ticker-specificity** — the same-day intersections concentrate on issuers in sectors under the subject's HASC, HOGR, and HSGO committee jurisdictions — and **composite-pattern generality**, the parallel structure of this same-day-8-K finding with the NDAA-window, FDA advisory-committee-window, CMS-rulemaking-window, and aligned-officer Form 3/4/5 same-day patterns documented in Exhibits E, F, X, and Z.
3. The pattern is sustained across all ten filing years (2017 through 2026 year-to-date), averaging approximately 19 same-day-8-K trades per year, and ranging year-by-year from 12 (2017) to 25 (2018). No single year drives the aggregate.
4. Intra-day clustering — 6 trades on 2018-10-25, 3 trades on each of eleven additional sessions including 2024-08-06 (3 trades against 6 8-K pairs, the most pair-dense daily intersection in the record) — is difficult to reconcile with random-co-incidence accounts at the per-trade-day level.

This exhibit does not establish — and no reader should infer — that any individual trade was executed on material non-public information. What it does establish is the per-trade pattern evidence that Count 1's MNPI framing relies on in conjunction with the NDAA-window clustering (Exhibit E), the aligned-direction insider-trade intersection (Exhibit Z), the composite dollar-weighted severity ranking (Exhibit LATE_FILING_AUDIT and Exhibit DAMAGES), and the committee-jurisdiction overlap documented in the sector-specific exhibits (Exhibit N Palantir, Exhibit F CMS-pharma, Exhibit X FDA advisory-committee windows).

---

## 8. Deferred enrichment paths

- **Item-code tagging.** Fetch each filing body via SEC EDGAR REST API; tag each match by 8-K item code; promote specific matches where the issuer is in a sector under the subject's HASC, HOGR, or HSGO jurisdiction.
- **T±1 broadening.** Re-run with a one-day window in each direction; report against the stricter same-day baseline as a sensitivity analysis.
- **Peer-cohort parallel.** Extend the chamber-wide computation to the 46-Member active-trader cohort in the peer-baseline substrate, persisting as the `same_day_8k_pct` column on `ro_khanna.peer_baseline` (currently carried as a Khanna-only baseline awaiting the cohort CIK-bridge expansion).

---

**Cross-references:** Exhibit E (NDAA-window 14 cluster trades with overlapping 2017-11-30 and 2020-12-28 same-day 8-K intersections), Exhibit N (Palantir timeline including 2-of-31 same-day-8-K contract-award overlaps), Exhibit Z (aligned-direction insider-match intersection), Exhibit C (peer-cohort baseline with M7 same-day-8-K dimension currently chamber-only pending CIK-bridge expansion to peers), Exhibit DAMAGES §4 (8-K same-day contribution of $5.28M to windowed P&L, 57.7% of T+30 forward-mark P&L).
