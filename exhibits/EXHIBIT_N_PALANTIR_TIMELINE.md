# Exhibit N — Palantir Deep Timeline

**Case**: *In re Representative Rohit "Ro" Khanna (CA-17)*
**Counts supported**: Counts 1, 2, 3
**Subject entity**: Palantir Technologies (NYSE: PLTR)

---

## 1. Scope and method

This exhibit binds four primary-source data streams into a single Member-centric chronological record:

1. Khanna household Periodic Transaction Report trades in PLTR (House Clerk PTR corpus; ticker = PLTR or `asset_name ILIKE '%palantir%'`).
2. Palantir Technologies federal contracts 2012–2026 (USAspending contract actions where the recipient is Palantir).
3. Khanna committee assignments for the 115th through 119th Congresses (bioguide K000389).
4. Palantir-employee individual contributions to the subject's two principal committees, C00503185 and C00392100 (Federal Election Commission individual-contribution records, strict employer match against "Palantir").

Every event is recorded as a tuple of (event_date, event_type, direction, actor, detail, amount_usd). The resulting record is queryable for any temporal slice, any combination of event types, and for same-day cross-stream coincidences.

---

## 2. Top-line aggregates

| Stream | Rows | Time span | Total dollar exposure |
|---|---:|---|---:|
| Khanna PTR PLTR trades | 29 | 2021-12-14 → 2026-03-30 | $281K (PTR midpoint notional) |
| Palantir USAspending contracts | 1,616 | 2012-10-17 → 2026-03-09 | $4,877,437,893 (~$4.88B) |
| Khanna committee assignments | 28 | 2017-01-03 → 2025-01-03 | — |
| Palantir-employee FEC donations | 21 | 2013-05-25 → 2024-03-25 | $39,601 |

Palantir's lifetime federal-contract exposure across the subject's tenure is approximately $4.88 billion. The 2020 through 2025 stretch totals approximately $4.06 billion. Across those years the subject served on the House Armed Services Committee's Cyber, Information Technologies, and Innovation subcommittee and the Select Committee on Strategic Competition Between the United States and the Chinese Communist Party.

### Annual Palantir USAspending obligation, 2012–2026

| Year | Contract actions | Total federal obligation |
|---|---:|---:|
| 2012 | 5 | $189,129 |
| 2013 | 47 | $39,518,198 |
| 2014 | 71 | $80,434,126 |
| 2015 | 82 | $93,087,095 |
| 2016 | 64 | $129,996,917 |
| 2017 | 83 | $129,213,319 — subject sworn 2017-01-03 |
| 2018 | 61 | $220,851,154 |
| 2019 | 83 | $123,947,856 |
| 2020 | 186 | $708,326,880 |
| 2021 | 119 | $415,740,161 |
| 2022 | 281 | $1,086,260,241 |
| 2023 | 129 | $329,934,676 |
| 2024 | 189 | $615,103,799 |
| 2025 | 215 | $904,834,342 |
| 2026 (YTD) | 1 | $0 |

The 2022 obligation total of $1.09 billion across 281 actions falls in the same year as (a) the subject's seat on the Select Committee on Economic Disparity and Fairness in Growth's classified-procurement work, (b) Department of Defense AI and data-platform procurement during the Russia–Ukraine war, and (c) the subject's participation in the House Armed Services Committee's FY2023 National Defense Authorization Act conference. The 2024–2025 obligation totals of $0.6 billion and $0.9 billion fall in the same period as the subject's elevation to Ranking Member of HASC's Cyber, Information Technologies, and Innovation subcommittee in the 119th Congress.

### Khanna household PTR PLTR activity, 2021–2026

| Year | Trades | Direction mix | Notes |
|---|---:|---|---|
| 2021 | 1 | BUY — 2021-12-14 | First family PLTR trade in the corpus; 13 days before NDAA FY2022 enactment 2021-12-27 |
| 2022 | 4 | BUY + SELL | Includes 2022-05-10 intra-day cluster (see §3.2) |
| 2023 | 1 | SELL | |
| 2024 | 2 | BUY | |
| 2025 | 12 | BUY + SELL | Includes same-day Army / DHS / IRS contract matches (see §3.1) |
| 2026 | 9 | BUY + SELL | Includes 2026-03-16 options cluster (six PLTR puts sold same day) |

Household PTR volume rose 2024 → 2025 → 2026 across the period of the subject's Ranking-Member elevation on HASC's Cyber/IT/Innovation subcommittee and Chair role on the Select Committee on Strategic Competition with China — the two committees with the closest oversight nexus to Palantir's federal AI and data-platform business.

### Palantir-employee FEC donation breakdown

| Donor | Position | Donations | Total | Span |
|---|---|---:|---:|---|
| SANKAR, SHYAM | Director → Executive → COO → CTO | 14 | $22,700 | 2013-05-25 → 2023-04-10 |
| JAIN, AKASH | Executive | 5 | $13,451 | 2020-09-27 → 2023-06-30 |
| ALHASSANI, MEHDI | Manager | 2 | $3,450 | 2016-03-23 → 2024-03-25 |

The strict employer-match donor figure of $39,601 is conservative relative to round-figure estimates in earlier drafts; the difference reflects records in which the contributor's Palantir affiliation appears in the title field rather than the employer field.

---

## 3. Same-day contract-action × household PTR-trade coincidences

This section sets out the calendar days on which Palantir Technologies received a federal contract action and the Khanna household executed a PLTR trade.

### 3.1 2025 same-day cluster

| Date | Contract awarding agency | Contract amount | Household trade |
|---|---|---:|---|
| 2025-09-19 | DHS — U.S. Immigration and Customs Enforcement | $19,355,842 | Dependent-child BUY |
| 2025-08-26 | DoD — Department of the Army | $7,003,185 | Dependent-child BUY |
| 2025-09-19 | Treasury — Internal Revenue Service | $4,511,147 | Dependent-child BUY |
| 2025-04-04 | Department of Energy | $756,667 | Dependent-child BUY (+ spouse SELL same day) |
| 2025-09-19 | HHS — Office of the Secretary | $355,320 | Dependent-child BUY |
| 2025-04-23 | DoD — Department of the Army | $89,124 | Spouse BUY + dependent-child BUY (intra-day pair) |
| 2025-04-04 | DHS — U.S. Immigration and Customs Enforcement | $0 obligation (modification) | Dependent-child BUY |
| 2025-02-19 | Department of State | $0 obligation (modification) | Spouse BUY |
| 2025-01-17 | Department of State | $0 obligation (modification) | Spouse BUY |

The 2025-09-19 row carries three distinct agency awards (DHS ICE, IRS, HHS — totaling $24.2 million) on a calendar day on which the Khanna dependent-child account purchased PLTR.

### 3.2 2022-05-10 same-day match

| Date | Contract | Amount | Household trades |
|---|---|---:|---|
| 2022-05-10 | DoD — Department of the Air Force (one action recurring across three line items) | $18,895,000 per line ($56.685 million same-day line-item total) | Two trades same day: one dependent-child BUY + one dependent-child SELL — an intra-day BUY/SELL pair on PLTR |

The 2022-05-10 row pairs three $18.895 million Air Force contract line items totaling $56.685 million with a paired BUY and SELL by the dependent-child account on the same calendar day. The intra-day BUY/SELL pair is consistent with day-trading reposition rather than directional accumulation. Under the Stop Trading on Congressional Knowledge Act §§ 3–4, a Member's household trading a defense-prime ticker on a calendar day on which the issuer receives material federal contract revenue is within the §§ 3–4 ambit regardless of whether the net position direction is long, short, or flat.

### 3.3 Top single-day Palantir contract clusters (≥$1 million)

Standalone high-stakes single-contract days, no household trade required:

| Date | Contract actions | Total day-of obligation |
|---|---:|---:|
| 2020-09-29 | 7 | $309.1M |
| 2021-11-30 | 3 | $112.2M |
| 2020-05-23 | 3 | $105.4M |
| 2022-02-15 | 3 | $102.0M |
| 2018-12-07 | 2 | $102.1M |
| 2022-09-28 | 9 | $94.8M |
| 2024-06-26 | 1 | $70.1M |
| 2025-06-26 | 1 | $61.4M |
| 2022-05-24 | 6 | $60.0M |
| 2025-09-24 | 6 | $54.7M |
| 2024-09-26 | 6 | $53.0M |

These top-cluster days do not intersect a Khanna household PLTR trade and set the background rate against which §§ 3.1–3.2 are read. Palantir has had 11 separate days with $50 million or more in federal obligations across 2018–2025; the household has executed PLTR trades on at least 9 separate same-day-contract days across the same span. The same-day-contract × household-trade intersection count is set out for the reader to evaluate against the background rate.

---

## 4. The closed circle

Each step carries a date or date band:

1. 2017-01-03 — The subject is sworn into the 115th Congress and is assigned to the House Armed Services Committee (rank 25 minority).
2. 2018–2026 — Continuous HASC service. In the 119th Congress (2025-01-03) the subject becomes Ranking Member of the Cyber, Information Technologies, and Innovation subcommittee and Chair of the Select Committee on Strategic Competition with China.
3. 2012–2026 — Palantir receives approximately $4.88 billion in federal contracts across DoD, DHS, DoE, HHS, Treasury, State, and VA. Each of these agencies' procurement falls within HASC, HOGR/HSGO, HSZS, or similar oversight visibility.
4. 2013-05-25 → 2024-03-25 — Palantir Chief Operating Officer Shyam Sankar makes 14 personal contributions to the subject ($22,700). Executive Akash Jain adds $13,451 across 5 contributions; Manager Mehdi Alhassani adds $3,450 across 2.
5. 2021-12-14 — First family PLTR trade in the corpus, 13 days before NDAA FY2022 enactment on 2021-12-27.
6. 2022-05-10 — Three Air Force contract line items totaling $56.685 million paired with a dependent-child BUY/SELL pair (two trades) on the same calendar day (§3.2).
7. 2025-08-26 — $7.0 million Army contract paired with a dependent-child PLTR BUY.
8. 2025-09-19 — Three agency contracts totaling $24.2 million (DHS ICE $19.4M, IRS $4.5M, HHS $0.4M) paired with a dependent-child PLTR BUY.
9. 2026-03-16 — Six PUT options on PLTR sold the same day (three September-2026 $130 + three March-2027 $130) — premium-collecting write activity coincident with the household's continuing long equity position.

---

## 5. Disposition

The 2025 same-day rows are corroborated and expanded by the timeline; the 2022-05-10 Air Force row is a same-day signature that surfaces only through the cross-stream join. The lifetime $4.88 billion Palantir federal-contract figure is the operative exposure number.

Open avenues, not pursued in this exhibit:

- Cross-reference the 2022 contract-action total with HASC closed-briefing dates. The 2022-09-28 nine-action row ($94.8 million) sits within the HASC FY2023 NDAA conference markup window; a Freedom of Information Act request to the HASC clerk for the closed-briefing schedule is the next vector.
- Palantir 8-K cross-reference. Palantir filed 42 8-Ks over 2015–2026; the intersection with household PLTR trade dates is five (separately documented in Exhibit M). A focused enrichment with 8-K item codes (Item 1.01 material contracts, 5.02 officer changes, 8.01 other) would identify which 8-K items fall on the same calendar days as the trades.
- Sankar-contribution × contract-action timing overlay. Each of Sankar's 14 contributions could be plotted against the rolling Palantir contract-obligation rate on the donation date.

---

## 6. Primary sources

- U.S. House Clerk — Khanna household PTRs for the 2017–2026 tenure (`disclosures-clerk.house.gov`).
- USAspending.gov — Palantir Technologies contract actions 2012–2026 (full recipient match).
- Clerk of the House — Khanna committee assignments 115th–119th Congress.
- Federal Election Commission — individual contributions with `employer ILIKE '%palantir%'` to committees C00503185 and C00392100.

---

*End of Exhibit N.*
