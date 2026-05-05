# Exhibit U — NAY-but-BUY Across Sectors

**Count supported.** Count 2 (front-running of NDAA enactments) extension, with corroboration on Count 3 (financial-interest conflicts) and Count 1 (composite axis) at the chamber-wide scale.

**Question.** Respondent's household trading cluster around NDAA enactment dates is documented in Exhibit E. Does that pattern extend across other sectors where the Member publicly votes against the bill while the household trades the bill's beneficiaries during the same window?

**Short answer.** It extends. Across 62 distinct respondent NAY passage-votes on sectoral bills during 2017–2026, the household traded in beneficiary-sector tickers in 67 bill × sector pairings, with a **2.39× aggregate BUY-versus-SELL ratio across 458 trades** (323 buys to 135 sells). The ratio is highest in defense and energy; the Healthcare Seniors Access bill is associated with a single-day 57-trade cross-sector cluster.

---

## 1. Method

For each respondent NAY passage-vote during 2017–2026 on a sectoral bill (defense, energy, healthcare, intelligence, appropriations, supplementals — 62 unique NAY votes identified), classify the bill's beneficiary sector, then count household PTR trades in beneficiary-sector tickers within ±30 days of the vote date. Aggregate by sector. The ticker sector map (defense prime; defense tech; big tech; pharma; healthcare devices; healthcare services; energy; crypto; intel / cyber) follows the case-schema ticker normalization. NAY votes are sourced from the canonical roll-call ledger filtered to bioguide K000389 voting Nay/No on passage-class questions. Trades are sourced from the household PTR canonical view (amendment-cascade deduplicated) and limited to BUY/SELL transaction types in beneficiary-sector tickers within the ±30-day window.

The hypothesis under test is whether the NDAA-window NAY-but-BUY pattern documented in Exhibit E is confined to defense or recurs in other sectors whose beneficiaries the household holds or accumulates.

## 2. Sector aggregates

Across 62 sectoral NAY votes, the household traded beneficiary-sector tickers in 67 bill × sector pairings:

| Sector | NAY votes covered | ±30d trades | Upper-bound $ | BUYs | SELLs | BUY:SELL ratio |
|---|---:|---:|---:|---:|---:|---:|
| **Defense prime** | **37** | **187** | **$3,190,000** | **145** | **42** | **3.45×** |
| **Energy** | **21** | **183** | **$3,240,000** | **127** | **56** | **2.27×** |
| Pharma | 1 | 28 | $490,000 | 8 | 20 | 0.40× |
| Intel / cyber | 3 | 25 | $635,000 | 19 | 6 | 3.17× |
| Healthcare devices | 1 | 16 | $240,000 | 11 | 5 | 2.20× |
| Healthcare services | 1 | 13 | $195,000 | 8 | 5 | 1.60× |
| Defense tech | 3 | 6 | $90,000 | 5 | 1 | 5.00× |

Reader-evaluable observations on the per-sector rows:

- **Defense prime — 145 buys and 42 sells across 37 NAY votes.** Extends the NDAA-enactment-window pattern documented in Exhibit E into DoD appropriations, DHS appropriations, intelligence authorizations, supplementals, and the Israel security supplemental — votes the NDAA-only framing in Exhibit E does not capture.
- **Energy — 127 buys and 56 sells across 21 NAY votes.** A second-sector extension into energy primes (XOM, CVX, COP, DVN, OXY, SLB, and analogs). The 2017–2018 stretch carries the highest trade density and falls in the same period during which respondent was publicly establishing his anti-fossil-fuel posture.
- **Intel / cyber — 19 buys and 6 sells across 3 NAY votes.** Respondent NAYs on intelligence authorizations and DHS appropriations during windows in which the household held cyber- and intel-adjacent primes.
- **Healthcare cluster on 2017-11-02, H.R. 849 Protecting Seniors Access to Medicare Act — 57 trades on a single NAY vote across pharma + healthcare devices + healthcare services.** The pharma component carries 8 buys and 20 sells; the healthcare-devices component carries 11 buys and 5 sells; the healthcare-services component carries 8 buys and 5 sells. One vote falls in a window containing differentiated trading across three healthcare sub-sectors on the same calendar week.

## 3. Highest-volume single-event pairings

The 30 highest-volume bill × sector pairings:

| Vote date | Bill | Sector | ±30d trades | BUYs | SELLs | Sample tickers | Bill title |
|---|---|---|---:|---:|---:|---|---|
| 2017-07-19 | H.R. 2883 | Energy | 32 | 26 | 6 | COP, CVX, DVN, OXY, XOM | Promoting Cross-Border Energy Infrastructure Act |
| 2017-11-02 | H.R. 849 | Pharma | 28 | 8 | 20 | ABBV, AMGN, BIIB, BMY, GILD, JNJ, MRK, PFE, REGN | Protecting Seniors Access to Medicare Act |
| 2018-03-08 | H.R. 1119 | Energy | 27 | 27 | 0 | COP, CVX, DVN, OXY, SLB, XOM | SENSE Act — buys only, zero sells |
| 2017-09-14 | H.R. 3354 | Energy | 26 | 11 | 15 | COP, DVN, OXY, SLB, XOM | DOI / environment appropriations FY2018 |
| 2018-07-19 | H.R. 6147 | Energy | 18 | 18 | 0 | COP, CVX, DVN, OXY, SLB, XOM | DOI / environment appropriations FY2019 — buys only |
| 2017-11-02 | H.R. 849 | Healthcare devices | 16 | 11 | 5 | ISRG, SYK | Protecting Seniors Access to Medicare Act |
| 2020-09-24 | H.R. 4447 | Energy | 14 | 9 | 5 | CVX, DVN, OXY, XOM | Expanding Access to Sustainable Energy Act |
| 2024-07-24 | H.R. 8998 | Defense prime | 13 | 8 | 5 | HON | DOI / environment FY2025 |
| 2017-11-02 | H.R. 849 | Healthcare services | 13 | 8 | 5 | CI, CVS, HUM | Protecting Seniors Access to Medicare Act |
| 2017-12-07 | H.J. Res. 123 | Defense prime | 11 | 9 | 2 | HON | Continuing appropriations FY2018 |
| 2017-12-21 | H.R. 4667 | Defense prime | 11 | 9 | 2 | HON | Supplemental disaster appropriations FY2018 |
| 2026-03-05 | H.R. 7744 | Intel / cyber | 11 | 7 | 4 | (sector-mapped by issuer) | DHS appropriations FY2026 |
| 2018-05-24 | H.R. 5515 | Defense prime | 10 | 7 | 3 | HON, LMT | NDAA FY2019 |
| 2018-07-12 | H.R. 6237 | Defense prime | 10 | 8 | 2 | LMT | Matthew Young Pollard Intelligence Authorization FY2018–19 |
| 2024-06-28 | H.R. 8752 | Intel / cyber | 10 | 10 | 0 | (sector-mapped) | DHS Appropriations FY2025 |
| 2018-07-12 | H.R. 3281 | Defense prime | 10 | 8 | 2 | LMT | Reclamation Title Transfer Act |
| 2025-03-11 | H.R. 1968 | Defense prime | 8 | 5 | 3 | (sector-mapped) | Full-Year Continuing Appropriations FY2025 |
| 2026-03-05 | H.R. 7744 | Defense prime | 8 | 3 | 5 | HON, PLTR | DHS Appropriations FY2026 |
| 2017-02-02 | H.J. Res. 37 | Defense prime | 7 | 6 | 1 | HON | Disapproving DoD / GSA rule |
| 2020-07-31 | H.R. 7617 | Defense prime | 7 | 7 | 0 | (sector-mapped) | DoD Appropriations FY2021 |

Two single-event rows show buys with no sells (BUYs > 0 and SELLs = 0):

- 2018-03-08 SENSE Act NAY followed by 27 energy-prime buys and zero sells in the ±30-day window.
- 2018-07-19 Interior appropriations FY2019 NAY followed by 18 energy-prime buys and zero sells.

The 2017-07-19 NAY on the Cross-Border Energy Infrastructure Act falls in a window containing 32 trades with a 26-to-6 buy distribution.

## 4. Defense-prime extension

Exhibit E documents 14 NDAA-enactment-window defense-prime trades across four NDAA enactments. This exhibit broadens that to **187 trades across 37 NAY votes on defense-related bills** (NDAA + DoD appropriations + DHS appropriations + intelligence authorizations + supplementals + the Israel security supplemental). The aggregate distribution is 145 buys to 42 sells — a 3.45× ratio, which is in the same direction as the pre-passage-accumulation pattern Exhibit E documents on the NDAA-specific subset.

The defense-prime cells with BUYs exceeding SELLs at n ≥ 5:

| Date | Bill | n | BUYs | SELLs | Bill title |
|---|---|---:|---:|---:|---|
| 2017-12-21 | H.R. 4667 | 11 | 9 | 2 | Supplemental appropriations FY2018 |
| 2017-12-07 | H.J. Res. 123 | 11 | 9 | 2 | Continuing appropriations FY2018 |
| 2018-07-12 | H.R. 3281 | 10 | 8 | 2 | Reclamation Title Transfer |
| 2018-07-12 | H.R. 6237 | 10 | 8 | 2 | Pollard Intelligence Authorization FY2018–19 |
| 2024-07-24 | H.R. 8998 | 13 | 8 | 5 | DOI / environment FY2025 |
| 2020-07-31 | H.R. 7617 | 7 | 7 | 0 | DoD Appropriations FY2021 |
| 2018-05-24 | H.R. 5515 | 10 | 7 | 3 | NDAA FY2019 |
| 2018-07-19 | H.R. 6147 | 6 | 6 | 0 | DOI / environment FY2019 |
| 2017-07-27 | H.R. 3219 | 6 | 6 | 0 | DoD Appropriations FY2018 |
| 2017-07-28 | H.R. 3180 | 6 | 6 | 0 | Intelligence Authorization FY2018 |
| 2017-02-02 | H.J. Res. 37 | 7 | 6 | 1 | Disapproving DoD / GSA rule |
| 2020-07-21 | H.R. 6395 | 6 | 5 | 1 | NDAA FY2021 |
| 2017-07-14 | H.R. 2810 | 5 | 5 | 0 | NDAA FY2018 (initial passage) |

The NDAA-only 14-trade Exhibit E subset broadens into a 187-trade defense-NAY-vote-window population with a 3.45× buy-to-sell ratio across the full respondent voting record.

## 5. The 2017-11-02 H.R. 849 healthcare cluster

A single NAY vote on the Protecting Seniors Access to Medicare Act falls in a window containing trade activity in three healthcare sub-sectors within ±30 days:

- Pharma — 28 trades (8 buys, 20 sells) across ABBV, AMGN, BIIB, BMY, GILD, JNJ, MRK, PFE, REGN. The sell-direction distribution is in the direction of a household reducing pharma exposure ahead of anticipated regulation-driven sector compression.
- Healthcare devices — 16 trades (11 buys, 5 sells) in ISRG and SYK. The buy-direction distribution on devices runs opposite the pharma sell-direction distribution.
- Healthcare services — 13 trades (8 buys, 5 sells) in CI, CVS, HUM, the Medicare-Advantage-relevant insurers. Mixed direction.

The 57-trade single-bill-vote cluster falls in a window containing differentiated trading across three healthcare sub-sectors on the same calendar week.

## 6. Energy NAY-but-BUY rows

Energy NAYs and the household ±30-day trade distribution:

| Vote date | Bill | n | BUYs | SELLs | Bill summary |
|---|---|---:|---:|---:|---|
| 2017-07-19 | H.R. 2883 | 32 | 26 | 6 | Cross-Border Energy Infrastructure Act |
| 2017-09-14 | H.R. 3354 | 26 | 11 | 15 | DOI / environment appropriations FY2018 |
| 2018-03-08 | H.R. 1119 | 27 | 27 | 0 | SENSE Act |
| 2018-06-08 | H.R. 5895 | 3 | 0 | 3 | Energy & water appropriations FY2019 |
| 2018-07-19 | H.R. 6147 | 18 | 18 | 0 | DOI / environment appropriations FY2019 |
| 2020-09-24 | H.R. 4447 | 14 | 9 | 5 | Expanding Access to Sustainable Energy Act |
| 2023-03-30 | H.R. 1 | 4 | 2 | 2 | Lower Energy Costs Act |
| 2023-10-26 | H.R. 4394 | 5 | 3 | 2 | Energy & water FY2024 |
| 2024-07-24 | H.R. 8998 | 5 | 3 | 2 | DOI / environment FY2025 |
| 2025-02-07 | H.R. 26 | 5 | 3 | 2 | Protecting American Energy Production Act |
| 2025-03-05 | H.J. Res. 42 | 6 | 3 | 3 | DOE rule disapproval |
| 2025-03-06 | S.J. Res. 11 | 6 | 3 | 3 | DOE rule disapproval |
| 2025-03-27 | H.J. Res. 24 | 7 | 3 | 4 | DOE rule disapproval |
| 2025-03-27 | H.J. Res. 75 | 7 | 3 | 4 | DOE / efficiency rule disapproval |
| 2025-09-04 | H.R. 4553 | 4 | 3 | 1 | Energy & water FY2026 |
| 2025-09-18 | H.R. 3062 | 5 | 3 | 2 | Cross-Border Energy Infrastructure |

The table enumerates the 16 highest-volume energy NAY-vote rows, totaling 174 trades / 120 BUYs / 54 SELLs; the §2 sector aggregate of 183 / 127 / 56 across 21 NAY votes includes 5 additional low-volume votes (cumulatively 9 trades / 7 BUYs / 2 SELLs) not enumerated at row grain in this section. The 2017–2018 buy-direction cluster (32 + 27 + 18 = 77 trades, with most labeled BUY) falls in the period during which respondent was publicly establishing his anti-fossil-fuel posture. The 2025-onward rows show a smaller per-vote trade count, which is reader-evaluable as a household winding-down in energy or as a reflection of a Trump-era regulatory environment with a different trade signal.

## 7. Headline metric

Across 62 sectoral NAY passage-votes during 2017–2026, the household executed **458 trades within ±30 days, with 323 buys and 135 sells — a 2.39× aggregate BUY-versus-SELL ratio**. The pre-passage-accumulation pattern documented on the NDAA-specific subset in Exhibit E recurs across the sector groupings respondent's committees touch.

---

*End of exhibit.*
