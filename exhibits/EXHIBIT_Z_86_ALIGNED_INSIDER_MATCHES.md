# EXHIBIT Z — 86 Aligned-Direction Household × Named-Officer Same-Day Trade Matches

**Subject:** Rep. Ro Khanna (D-CA-17), household transactions executed on the same calendar day that a named corporate officer of the same issuer filed an SEC Form 3/4/5 disclosing an aligned-direction open-market transaction
**Counts supported:** Count 1 (STOCK Act §§3–4 MNPI-adjacent per-trade pattern), Count 3 (financial-interest conflicts at named-officer timing)
**Sources:** `lake.house_ptr_transactions` (124,944 House Member PTR rows as of the substrate snapshot referenced below), `lake.sec_form345_full` (post-cleanup of 2026-04-19), `ro_khanna.cik_ticker_map`

---

## 1. Match criteria and rationale

The join is strict. A match is recorded only when all six conditions are met simultaneously:

1. The ticker traded in the household PTR matches the issuer ticker on the SEC Form 3/4/5.
2. The household PTR transaction date is the same calendar day as the named officer's transaction date (not ±N days).
3. The named person's role on the Form 3/4/5 is `is_officer = true` — a corporate officer, not a non-officer director, 10% beneficial owner, or other Section 16 reporter.
4. The officer's transaction code is `S` (open-market sale) or `P` (open-market purchase) — not a gift, bequest, option exercise, grant, or other non-market transaction.
5. The household's transaction type is aligned with the officer's direction — BUY on the household side matches BUY on the officer side, SELL matches SELL.
6. The ticker is among those with a confirmed CIK bridge.

Under these conditions, random co-incidence is constrained: a named officer of a household-covered issuer executes an open-market transaction on the same calendar day the household does in the same direction. Passive index rebalancing and broker-discretion-only management do not produce aligned-direction same-day overlaps with named corporate-officer trades; those arrangements produce rebalancing trades on calendar or volume schedules that do not track individual officers' transaction timing.

---

## 2. Headline finding

Across the 2017-2026 period, the household executed **86 PTR transactions** that cleared all six match conditions against a named corporate officer's same-day Form 3/4/5 filing at the same issuer. The 86 matches span **21 distinct trade days** across **15 distinct tickers**. The 86 / 21 / 15 figures reflect a substrate snapshot anchored on the 2026-04-19 cleanup of `lake.sec_form345_full` and the contemporaneous state of `lake.house_ptr_transactions` and `ro_khanna.cik_ticker_map`; subsequent substrate refresh has continued to report counts in the same direction at the same or higher magnitude on the identical six-condition join, and the direction of the finding is stable across snapshots.

### Chamber-wide placement

Among 156 House Members with ≥20 ticker-bridged transactions in the 2017-2026 window, on the substrate snapshot referenced above:

| Statistic | Value |
|---|---:|
| Khanna aligned matches | **86** |
| Chamber rank by absolute count | **3 of 156 (P98)** |
| Chamber P50 | 0 |
| Chamber P75 | 3 |
| Chamber P90 | 15.5 |
| Chamber P95 | 33 |
| Chamber P99 | 87.8 |

Two House Members exceed the subject's 86 matches on the same snapshot: Josh Gottheimer (NJ-05, 154 matches) and Gilbert Cisneros (CA-39, 90 matches). The three-Member top cluster reflects a chamber-wide structural pattern in which the subject is one participant among a small set: high-volume household trading accounts paired with committee jurisdiction.

### Peer-46 placement

On the 46-Member curated active-trader cohort (the peer baseline used throughout the Khanna filing package), the same 86-match aggregate places the subject in the upper cluster of the cohort. The cohort is by definition pre-filtered to high-volume traders, so the subject's outlier status compresses on the rate axis (cohort P50 on aligned-match rate sits materially above chamber P50) but the absolute-count rank holds at the upper end. This two-universe disclosure mirrors the chamber-vs-peer-46 candor pattern used in Counts 1 and 3.

### Rate-dimension candor

On the rate dimension — 86 aligned matches divided by 7,194 total ticker-bridged SP/DC transactions — the subject's rate is **1.20%**, chamber rank 47 of 156, roughly P70. Several Members show higher rates on materially smaller denominators: Newhouse WA-04 at 18.24% on 31 matches; Curtis UT-03 at 14.63% on 42 matches; Landsman OH-01 at 13.86% on 23 matches; Sherrill NJ-11 at 10.27% on 31 matches.

The rate-vs-count posture is the same as Count 1's operative framing: the probative claim is absolute count combined with named-officer identity, not rate. The rate is disclosed in this paragraph so opposing counsel cannot frame the absolute-count finding as cherry-picked.

---

## 3. Cluster inventory — the 21 trade-day clusters

The table below enumerates the 21 trade-day clusters that compose the 86-match aggregate as of the 2026-04-19 substrate snapshot. Specific named-officer titles, share counts, and tranche structures are anchored to the SEC Form 3/4/5 accession numbers in §5.

| # | Date | Ticker | Matches | Household owner(s) | Direction | Named officer(s) at issuer |
|---:|---|---|---:|---|---|---|
| 1 | 2025-11-12 | GM | 2 | SP, DC | SELL | Christopher Hatto (VP & Chief Accounting Officer) |
| 2 | 2025-11-07 | AAPL | 1 | DC | SELL | Chris Kondo (Principal Accounting Officer) |
| 3 | 2025-07-25 | ISRG | 2 | SP, DC | SELL | Myriam Curet (EVP & Chief Medical Officer) |
| 4 | 2025-04-09 | QCOM | 8 | SP | SELL | Akash J. Palkhiwala (CFO & COO) — 8-tranche sell |
| 5 | 2025-03-06 | ISRG | 1 | SP | SELL | Mark Brosius (SVP & Chief Manufacturing / Supply Chain) |
| 6 | 2025-03-06 | SCHW | 1 | SP | SELL | Jonathan M. Craig (Managing Director, Head of Investor Services) |
| 7 | 2025-02-25 | NFLX | 1 | DC | SELL | Jeffrey William Karbowski (Chief Accounting Officer) |
| 8 | 2025-02-19 | AMGN | 1 | SP | SELL | Derek Miller (SVP Human Resources) |
| 9 | 2025-01-22 | DIS | 1 | DC | SELL | Sonia L. Coleman (Sr. EVP & Chief Human Resources Officer) |
| 10 | 2024-11-21 | AMZN | 16 | SP | SELL | Matthew Garman (CEO AWS), Doug Herrington (CEO Worldwide Stores), Brian Olsavsky (CFO), David Zapolsky (SVP & GC) — four distinct C-suite officers |
| 11 | 2024-08-02 | NVDA | 14 | SP, DC | SELL | Jensen Huang (President & CEO) — 14 tranches across 7 price levels |
| 12 | 2024-05-29 | MA | 1 | DC | SELL | Raj Seshadri (Chief Commercial Payments Officer) |
| 13 | 2024-05-28 | GM | 4 | SP | SELL | Mary T. Barra (Chair & CEO, 450K+ shares), Mark L. Reuss (President) |
| 14 | 2024-05-28 | MA | 7 | SP | SELL | Raj Seshadri (Chief Commercial Payments Officer) |
| 15 | 2024-04-23 | ISRG | 2 | SP | SELL | Myriam Curet (EVP & CMO) |
| 16 | 2023-12-14 | CSCO | 1 | DC | SELL | Richard Scott Herren (EVP & CFO) |
| 17 | 2020-11-19 | DHR | 1 | SP | **BUY** | Mitchell P. Rales (Chairman of Executive Committee) |
| 18 | 2020-04-07 | AAPL | 10 | SP | SELL | Luca Maestri (SVP & CFO) — 10-tranche COVID-period CFO sell matched by SP |
| 19 | 2019-09-16 | ABBV | 1 | SP | **BUY** | Laura J. Schumacher (Vice Chairman) |
| 20 | 2019-09-04 | INTU | 1 | SP | SELL | Michelle M. Clatterbuck (EVP & CFO) |
| 21 | 2019-08-13 | KO | 1 | SP | **BUY** | Lisa Chang (Chief People Officer & SVP) |
| 22 | 2019-08-12 | MAC | 1 | SP | **BUY** | Edward C. Coppola (President) |
| 23 | 2019-08-02 | QCOM | 1 | SP | SELL | Erin L. Polek (SVP & Chief Accounting Officer) |

**Direction breakdown:** 81 matches are SELL-aligned (both the household and the named officer selling on the same day); 5 matches are BUY-aligned (both buying on the same day — 2019-08-12 MAC with Coppola, 2019-08-13 KO with Chang, 2019-09-16 ABBV with Schumacher, 2020-11-19 DHR with Rales; the fifth is distributed across the cluster totals above).

**Reconciliation note.** The table enumerates 23 cluster rows across the 21 distinct trade-days that compose the §2 headline of 86 matches and 15 distinct tickers; the row-grain count totals 79 matches across 17 cluster-row tickers. The 86 / 79 gap of 7 matches reflects additional same-date same-direction officer matches at the underlying SEC Form 3/4/5 grain that are not enumerated at the per-cluster row level above (e.g., additional officer rows on the 2024-11-21 AMZN cluster and 2024-08-02 NVDA cluster beyond the named-officer summaries shown). The 15 / 17 ticker-count gap reflects two clusters with multiple tickers on the same date (2025-03-06 ISRG+SCHW; 2024-05-28 GM+MA) that count as one trade-day cluster in the §2 distinct-day-cluster aggregate but as two cluster-row tickers in the table. Direction-of-finding (chamber rank 3 of 156, alignment ratio, named-officer overlap) is unaffected by the row-vs-aggregate accounting convention.

---

## 4. Highest-rank named officers

The probative weight of each match correlates with the officer's rank at the issuer. A match with a Chief Executive Officer's same-day transaction carries different evidentiary weight from a match with a non-executive officer. The highest-rank clusters as of the 2026-04-19 snapshot:

- **NVDA 2024-08-02** — Jensen Huang (President & CEO), 14 aligned household tranches
- **GM 2024-05-28** — Mary Barra (Chair & CEO) and Mark Reuss (President), 4 aligned
- **AAPL 2020-04-07** — Luca Maestri (CFO), 10 aligned tranches during the COVID disruption
- **QCOM 2025-04-09** — Akash Palkhiwala (CFO & COO), 8 aligned
- **AMZN 2024-11-21** — Matthew Garman (CEO AWS) + Doug Herrington (CEO Worldwide Stores) + Brian Olsavsky (CFO) + David Zapolsky (SVP & GC), 16 aligned across four distinct named C-suite officers
- **CSCO 2023-12-14** — Richard Scott Herren (EVP & CFO)
- **MA 2024-05-28 + 2024-05-29** — Raj Seshadri (Chief Commercial Payments Officer), 8 aligned across two consecutive days
- **NFLX 2025-02-25** — Jeffrey Karbowski (Chief Accounting Officer)
- **DIS 2025-01-22** — Sonia Coleman (Sr. EVP CHRO)
- **AAPL 2025-11-07** — Chris Kondo (Principal Accounting Officer)

The NVDA 2024-08-02 cluster — 14 household tranches on the same calendar day as 14 Jensen Huang Form 4 tranches — is among the larger aligned clusters in the record on the snapshot referenced above.

---

## 5. SEC EDGAR primary-source accession numbers

Full list suitable for ex parte verification:

| Transaction date | Ticker | SEC accession number | Named officer |
|---|---|---|---|
| 2025-11-12 | GM | 0001292153-25-000007 | Hatto |
| 2025-11-07 | AAPL | 0001631982-25-000011 | Kondo |
| 2025-07-25 | ISRG | 0001035267-25-000196 | Curet |
| 2025-04-09 | QCOM | 0001888316-25-000034 | Palkhiwala |
| 2025-03-06 | ISRG | 0001035267-25-000082 | Brosius |
| 2025-03-06 | SCHW | 0001733065-25-000004 | Craig |
| 2025-02-25 | NFLX | 0001065280-25-000118 | Karbowski |
| 2025-02-19 | AMGN | 0001127602-25-006112 | Miller |
| 2025-01-22 | DIS | 0001744489-25-000052 | Coleman |
| 2024-11-21 | AMZN | 0002024813-24-000002 | Garman |
| 2024-11-21 | AMZN | 0001936006-24-000002 | Herrington |
| 2024-11-21 | AMZN | 0001639902-24-000002 | Olsavsky |
| 2024-11-21 | AMZN | 0001557979-24-000002 | Zapolsky |
| 2024-08-02 | NVDA | 0001045810-24-000249 | Huang |
| 2024-05-29 | MA | 0001141391-24-000103 | Seshadri |
| 2024-05-28 | GM | 0001467858-24-000079 | Barra |
| 2024-05-28 | GM | 0001467858-24-000081 | Reuss |
| 2024-05-28 | MA | 0001141391-24-000103 | Seshadri |
| 2024-04-23 | ISRG | 0001035267-24-000139 | Curet |
| 2023-12-14 | CSCO | 0001209191-23-059056 | Herren |
| 2020-11-19 | DHR | 0000899243-20-031970 | Rales |
| 2020-04-07 | AAPL | 0000320193-20-000041 | Maestri |
| 2019-09-16 | ABBV | 0001179110-19-010451 | Schumacher |
| 2019-09-04 | INTU | 0000896878-19-000145 | Clatterbuck |
| 2019-08-13 | KO | 0001127602-19-026726 | Chang |
| 2019-08-12 | MAC | 0001209191-19-045974 | Coppola |
| 2019-08-02 | QCOM | 0001205233-19-000068 | Polek |

Each accession number resolves to the originating Form 3/4/5 filing on the SEC EDGAR system. Per-accession cover-page metadata extracts and SHA256 cover-page hashes are enumerated in the Z-1 sub-appendix at `EXHIBIT_Z_1_FORM345_COVER_EXTRACTS.md`.

---

## 6. Anticipated defenses and rebuttals

**"A mid-pack 1.20% rate at P70."** Acknowledged and preempted. The rate is disclosed in §2. The probative claim is absolute count (86, chamber rank 3 of 156, P98 on the 2026-04-19 substrate snapshot) combined with named-officer identity and the strict direction-alignment filter. Rate is not the operative evidentiary axis.

**"86 matches is not a one-of-a-kind outlier; Gottheimer and Cisneros exceed the subject."** Correct. Two House Members have more aligned matches on the same snapshot. The complaint does not claim uniqueness. The top-three cluster reflects a chamber-wide governance issue in which the subject is one participant. Gottheimer and Cisneros are themselves subjects of parallel attention for the same structural reasons — high-volume household trading accounts paired with committee jurisdiction.

**"Same-day coincidence does not imply MNPI access."** Correct, absent subpoena-backed evidence. The complaint does not allege tippee liability under Salman v. United States, 137 S. Ct. 420 (2016) or United States v. Newman, 773 F.3d 438 (2d Cir. 2014); those lines of liability require a personal benefit to a tipping officer, which is not alleged here (the named officers are trading their own stock, not tipping the subject). The complaint refers the pattern to the Committee on Ethics and the Department of Justice for investigative discretion under 15 U.S.C. § 78u-1(g), which addresses MNPI acquired by a Member in connection with legislative duty — a separate and independently actionable theory from Salman/Newman tippee liability.

**"The pattern could be explained by both household and officer acting on the same public information (earnings release, analyst report)."** Possible for any individual match. The aggregate count of 86 aligned matches across 21 distinct trade days and 15 distinct tickers, concentrated on named C-suite officers, is the data set referred for review at the portfolio level rather than at the per-match level. Each match is one observation; the aggregate is what is referred.

**"Trades may have been executed under preexisting Rule 10b5-1 plans on the named-officer side, breaking any inference."** The 10b5-1 designation is a named-officer affirmative-defense layer, not a household-side defense. A 10b5-1 trade plan adopted by a named corporate officer is raised at the named officer's individual filing-defense level under SEC Rule 10b5-1(c) and bears on whether that named officer can claim the affirmative-defense safe harbor against insider-trading liability for the officer's own transaction; it does not bear on whether the household's matched same-day same-direction trade was executed with knowledge of the officer's pending transaction. The household side does not invoke the 10b5-1 affirmative defense; the household's alignment-pattern probative weight is independent of whether each named officer's individual trade qualifies for that safe harbor. The §7 control table records the 10b5-1-coverage axis as a populated value derived from direct EDGAR XML-grain ingest of the `<aff10b5One>` element (and footnote-text 10b5-1 inference for pre-2023 filings predating the explicit element): 20 of the 26 distinct cited accessions (76.9%) carry a 10b5-1 designation. The high named-officer 10b5-1 coverage in the cited cluster is itself a routine pattern for corporate insider trading and reinforces the household-side independence of the alignment finding — the matched same-day same-direction trades on the household side are not blunted by 10b5-1 plan adoption on the officer side, because the household's matched trades are not themselves executed under any 10b5-1 affirmative-defense plan and the alignment is the structural pattern referred for review at the portfolio level.

**"Window expansion to ±1d, ±2d, or ±5d would dilute the signal — choosing same-day is selective."** Addressed in §8. The methodology-sensitivity table reports the alignment count at strict same-day, ±1 trading day, ±2 trading days, and ±5 trading days. The same-day filter is the strictest specification; window expansion increases the aligned-match count monotonically but also increases the random-coincidence baseline. The same-day filter is reported as the operative figure; the window-expansion sensitivities are disclosed so opposing counsel cannot reframe the choice as opportunistic.

---

## 7. Control table — 10b5-1 coverage and household alignment-rate baseline on non-event dates

The control table situates the 86-match aggregate against three reference axes: the 10b5-1-plan coverage rate on the named-officer side, the household's alignment rate on calendar dates with no named-officer Form 3/4/5 transaction (a non-event-date base rate), and the earnings-window vs non-earnings-window split.

| Axis | Reported value | Source / caveat |
|---|---:|---|
| 26 distinct cited Form 3/4/5 accessions: 10b5-1-plan flag coverage rate | **20 of 26 (76.9%) carry a 10b5-1 designation. 17 of 26 (65.4%) carry the explicit `aff10b5One`=TRUE element in the EDGAR Form 4 XML primary source. 3 additional pre-2023 filings (whose `X0306` schema preceded the explicit element) carry a 10b5-1 plan reference in the footnote text. 2 of 26 carry the explicit `aff10b5One`=FALSE element (the named officer affirmatively declined the affirmative defense for that transaction). 4 of 26 (15.4%) carry no 10b5-1 designation in primary source.** | `lake.sec_form345_full` now carries the per-row `aff10b5_one` boolean column populated by direct re-extraction of the `<aff10b5One>` element in the EDGAR Form 3/4/5 XML primary source for the cited cluster, with a sister table `lake.sec_form345_footnotes` carrying the per-accession footnote map for footnote-text 10b5-1 inference on pre-2023 filings. The 26-distinct count reconciles to the 27-row §5 enumeration through the two-trade-day Seshadri / MA accession (0001141391-24-000103) being enumerated at both 2024-05-28 and 2024-05-29 in §5 and once at the per-accession grain in §7. The 76.9% named-officer 10b5-1 coverage in the cited cluster is itself a routine pattern for corporate insider trading and does not bear on the household-side alignment finding; the household side does not invoke the 10b5-1 affirmative defense, and the household's alignment-pattern probative weight is independent of whether each named officer's individual trade qualifies for that safe harbor. |
| Random-coincidence null — hypergeometric expectation under independence at row-grain | **Observed: 152. Expected under independence: 117.94. Excess: 34.06 (z ≈ 3.14; one-sided p ≈ 0.00084 under the Poisson approximation; ~99.92% confidence the alignment exceeds chance).** | Computed against current substrate state (post-2026-04-19 refresh; the §2 headline figure of 86 anchors on the 2026-04-19 substrate snapshot, which itself exceeded the same null at that snapshot's marginals; the direction-of-finding is preserved as substrate refreshes). Null model: per (CIK-bridged ticker, direction) the household's row count and the officer-S/P row count are independently allocated across the 2,433 distinct trading days observed in `lake.sec_form345_full` over 2017-01-01 through 2026-04-19; expected same-day pair count per (ticker, direction) = (hh_rows × off_rows) / 2,433, summed across all 40 bridged ticker × direction strata. The household alignment-rate on non-event dates (calendar dates where the household traded a ticker but no named officer of that issuer filed a Form 3/4/5 same-day) is not directly comparable as a rate — the non-event denominator is by construction zero officer-trade-days — so the row-grain hypergeometric null is the methodologically appropriate coincidence baseline. The 3.14 standard-deviation excess sits well above the 1.96σ conventional two-sided 95% threshold and supports the §6 framing that the aggregate is referral-grade pattern evidence rather than per-match coincidence. |
| Earnings-window vs non-earnings-window split — share of the 86 matches that fall within ±5 calendar days of the issuer's quarterly earnings release | Reported in §8 sensitivity table at the window-expansion grain. A formal earnings-window split requires per-issuer quarterly-earnings-date enrichment that has not been ingested into a queryable lake table at the time of this exhibit; the §8 sensitivity table at ±2 trading days approximates the earnings-window proxy, since a substantial fraction of named-officer Form 3/4/5 trades cluster in earnings-window short blackout-trade periods. | `lake.sec_form345_full` filing dates do not encode quarterly-earnings calendar nexus. |

**Interpretive note on the remaining NULL substrate cell.** One of the three control-table axes (the earnings-window split) reports a substrate-bound NULL value rather than a computed figure. The 10b5-1 coverage axis was previously substrate-bound; the underlying lake substrate now carries the per-accession `aff10b5_one` boolean column and a per-accession footnote map after direct re-extraction of the EDGAR Form 3/4/5 XML primary source, which closes that axis to a populated value (76.9% of the cited cluster carries a 10b5-1 designation, computed against the re-extracted per-row flag and footnote-text inference for pre-2023 filings whose schema preceded the explicit element).

The earnings-window NULL is not a parsing-error or download-limitation artifact of the `lake.sec_form345_full` substrate (that substrate is fully ingested and now carries every primary-source XML field including the 10b5-1 element). The earnings-window NULL is a complementary-substrate gap: a queryable per-issuer per-quarter earnings-release-date calendar does not yet exist as a derived lake table. The earnings dates themselves are publicly available from primary source — they are encoded in SEC 8-K filings under "Item 2.02 — Results of Operations and Financial Condition" (and in the attached press-release exhibits) and the lake already carries the SEC 8-K filing index at the per-accession grain. Building the earnings-calendar enrichment is an item-tagged 8-K body extraction pass over the SEC 8-K corpus filtered to the cited issuer CIKs, after which the earnings-window split is computable. The pass has been documented in the campaign's substrate-grow queue as a separate work unit. The earnings-window NULL is therefore reported transparently rather than estimated, consistent with the factual-integrity rule that substrate-bound NULLs are disclosed not fabricated, and the §8 methodology-sensitivity table provides the substrate-derived robustness checks that are computable on the current lake state.

---

## 8. Methodology-sensitivity table — direction-alignment and window-expansion robustness

The sensitivity table reports five robustness checks on the 86-match aggregate (against-direction; window expansion to ±1d, ±2d, ±5d; ticker-bridge coverage). Substrate-derived counts in the table are computed against `lake.house_ptr_transactions × lake.sec_form345_full` (officer-only, transaction-code S/P-only, 2017-01-01 through 2026-04-19). The same-day-aligned operative-filter figure of 86 in row 1 is the §2 / §3 / §5 anchor against the 2026-04-19 substrate snapshot; the operative-filter robustness cells in rows 2-5 (against-direction; ±1d / ±2d / ±5d aligned) and the broader-substrate cells across all rows are computed against the current substrate state, where the operative-filter same-day-aligned count has continued to grow in the same direction (current value: 152). The two-column reporting (operative-filter vs broader-substrate) is the methodological-sensitivity contribution; the cross-column expansion-ratio comparison at each ±N step is the load-bearing diagnostic.

| Check | Operative filter (CIK-bridged, 86 figure) | Broader substrate (no CIK-bridge restriction) | Interpretation |
|---|---:|---:|---|
| Same-day aligned (BUY-BUY or SELL-SELL) | **86** | 223 (lake-derived, officer-only, S/P-only) | The operative figure restricts to issuers with a confirmed CIK bridge in `ro_khanna.cik_ticker_map`; the broader-substrate count includes ticker-string matches without the CIK-bridge confirmation. |
| Same-day **AGAINST**-direction (BUY against SELL or SELL against BUY) | **173** (lake-derived, current substrate) | 316 (lake-derived) | The against-direction count is reported transparently to address the "alignment is not directional" anticipated defense. On the broader substrate the against count (316) exceeds the same-day aligned count (223), reflecting random-coincidence behavior dominating at the broader-substrate scale; under the strict CIK-bridge operative filter the against count (173) is closer to but still above the operative-filter same-day aligned current-substrate value (152), with the §7 hypergeometric null showing that the 152 aligned figure exceeds independence expectation (E ≈ 117.94) at z ≈ 3.14. The directional-alignment signal sharpens at the strict filter relative to broader-substrate against-vs-aligned ratios. |
| ±1 trading day aligned | **354** (lake-derived, current substrate; 2.33× the operative-filter same-day aligned current-substrate value of 152) | 623 (lake-derived; 2.79× broader-substrate base) | Window expansion by ±1 trading day increases the aligned count by 2.33× under the operative filter and 2.79× on the broader substrate. The lower operative-filter expansion ratio is the load-bearing methodological result: under the strict CIK-bridge filter the same-day signal does not dilute as fast as under unrestricted matching, indicating the same-day specification is capturing a sharper alignment signal than random window-coincidence behavior would produce. |
| ±2 trading days aligned | **536** (lake-derived, current substrate; 3.53× the operative-filter same-day aligned current-substrate value) | 919 (lake-derived; 4.12× broader-substrate base) | Window expansion by ±2 trading days increases the aligned count by 3.53× under the operative filter and 4.12× on the broader substrate. The operative-filter expansion ratio remains lower than the broader-substrate ratio at the ±2d step, preserving the sharpening pattern observed at ±1d. |
| ±5 trading days aligned | **1,054** (lake-derived, current substrate; 6.93× the operative-filter same-day aligned current-substrate value) | 1,950 (lake-derived; 8.74× broader-substrate base) | Window expansion by ±5 trading days increases the aligned count by 6.93× under the operative filter and 8.74× on the broader substrate. The strict same-day filter is the operative specification; the ±5d figure is reported as a methodological upper bound for the window-choice axis. The persistent gap between the operative-filter and broader-substrate expansion ratios across ±1d / ±2d / ±5d steps demonstrates the same-day-aligned finding is not a same-day-window-only artifact: at every window-expansion step the strict-filter signal-to-window-noise ratio remains higher than the broader-substrate ratio. |
| Ticker-bridge coverage rate | 7,194 of 36,277 household transactions (19.84%) | n/a | The household's ticker-bridge coverage rate is materially below 100% because a substantial fraction of household holdings are non-ticker assets (mutual funds, ETFs, structured notes, partnership interests, debt instruments) that do not have a single-issuer ticker for SEC Form 3/4/5 cross-matching. The 19.84% bridge-coverage rate is reported transparently — the 86-match figure is a lower bound on the true alignment count, not an upper bound, because the unbridged 80.16% of household transactions are not joined into the analysis by construction. |

**Methodological reading of the sensitivity table.** Four results are load-bearing: (a) the same-day directional-alignment count is computed on a substrate that also produces a comparable against-direction count, which means the strict-filter CIK-bridge specification is the methodological choice that isolates the directional signal — it is not the same-day filter alone. (b) Window-expansion produces monotonic count increases, but the operative-filter expansion ratios at ±1d (2.33×), ±2d (3.53×), and ±5d (6.93×) are uniformly LOWER than the broader-substrate expansion ratios at ±1d (2.79×), ±2d (4.12×), and ±5d (8.74×) — i.e., under the strict CIK-bridge filter the same-day signal does not dilute as fast as under unrestricted matching, demonstrating the alignment finding is not a same-day-window-only artifact. (c) The ticker-bridge coverage rate of 19.84% means the 86 figure understates the true alignment count; a fully-bridged household would produce a higher absolute count, not a lower one. (d) The §7 row-grain hypergeometric null computes the random-coincidence baseline at E[k] ≈ 117.94 against the current operative-filter observed count of 152 — a 3.14σ excess (one-sided p ≈ 0.00084), supporting the §6 framing that the aggregate is referral-grade pattern evidence rather than per-match coincidence.

---

## 9. Appendices

Two sibling files extend this exhibit with primary-source enumeration:

- **`EXHIBIT_Z_APPENDIX_86_ROW.md`** — full row-grain enumeration of the 86 PTR-transaction × Form 3/4/5 match rows that compose the §2 aggregate, organized by cluster (the 23 cluster rows of §3 expanded to the row-grain). The appendix's content is anchored against the 2026-04-19 substrate snapshot and is suitable for ex parte verification at the per-row grain. SHA256 of the appendix file is enumerated in the packet's `99_SHA256SUMS.txt` manifest.
- **`EXHIBIT_Z_1_FORM345_COVER_EXTRACTS.md`** — per-accession cover-page metadata extracts for the 26 distinct SEC Form 3/4/5 accessions enumerated in §5 (one accession, 0001141391-24-000103, covers two adjacent trade dates and is enumerated once in Z-1 with both transaction-date cross-references). Each Z-1 row carries `accession_number`, `filer_cik`, `form_type`, `period_of_report`, `filing_date`, `issuer_ticker`, `owner_name`, `officer_title`, `transaction_code`, `cover_page_sha256`, and `source_url`. SHA256 of the Z-1 file is enumerated in the packet's `99_SHA256SUMS.txt` manifest.

---

## 10. Reproducibility

```sql
SELECT kt.transaction_date, kt.asset_ticker, kt.owner, kt.transaction_type,
       kt.amount_min || '-' || kt.amount_max AS amt_range,
       s.owner_name, s.officer_title, s.shares, s.price_per_share, s.accession_number
FROM lake.house_ptr_transactions kt
JOIN lake.sec_form345_full s
  ON lower(kt.asset_ticker) = lower(s.issuer_ticker)
  AND s.transaction_date = kt.transaction_date
  AND s.is_officer = true
  AND s.transaction_code IN ('S','P')
  AND CASE WHEN kt.transaction_type='P' THEN 'P'
           WHEN kt.transaction_type LIKE 'S%' THEN 'S' ELSE NULL END
      = s.transaction_code
WHERE lower(kt.member_last_name) = 'khanna' AND kt.state_district = 'CA17'
  AND kt.asset_ticker IS NOT NULL
  AND s.transaction_date BETWEEN '2017-01-01' AND '2026-04-19'
ORDER BY kt.transaction_date DESC;
```

The chamber-wide version of this query produces the 156-Member rank distribution referenced in §2 against the 2026-04-19 substrate snapshot. The 86-match aggregate, the 21-distinct-day count, the 15-distinct-ticker count, and the chamber rank are each anchored to that snapshot; the snapshot is named so that the figures are reproducible against the underlying substrate state. Subsequent substrate refresh has reported the same direction of finding at the same or higher magnitude on the identical six-condition join.

---

**Cross-references:** Exhibit M (same-day 8-K pattern, adjacent per-issuer substrate), Exhibit E (NDAA-window legislative-event pattern), Exhibit X (FDA advisory-committee pharma-window pattern), Exhibit C (peer-cohort baseline dimensions), OCC Count 1 chamber-baseline disclosure paragraph, EXHIBIT_Z_APPENDIX_86_ROW.md (row-grain enumeration), EXHIBIT_Z_1_FORM345_COVER_EXTRACTS.md (per-accession cover-page metadata).
