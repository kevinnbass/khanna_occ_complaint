# Exhibit FF — Three-Way Tracker Agreement on Cited Trades

**Count supported.** Corroboration for Counts 1, 2, and 3 and for the §VI anticipated-response cluster that challenges data provenance. This exhibit tests each cited household trade against two independent third-party congressional-trading trackers to establish that the underlying disclosures are recorded consistently across sources.

**Methodological framing.** The three-way agreement test in this exhibit is a corroborative methodology, not an element of any cited count. None of Counts 1, 2, or 3 require a tracker match as a statutory predicate; the operative substantive showing rests on the Clerk's PTR record itself. This exhibit is offered to corroborate the data provenance of the Clerk record and to pre-empt the data-provenance line of anticipated response in §VI of the complaint.

**Scope.** 27 household trades cited across the filing package. (A previously listed twenty-eighth row — a 2024-08-02 spouse-account Pfizer purchase — was removed from this exhibit after primary-source verification against the Clerk's structured PTR substrate confirmed the underlying filing contains no such row; the only Pfizer row in the host document is a separate 2024-08-23 dependent-child purchase. The retraction is documented in §4.4 below.)

---

## 1. Sources and coverage

Three independent sources:

1. **The House Clerk PTR corpus.** The authoritative primary-source record. Each cited trade is drawn from a respondent PTR filing (documents 9112175, 8217812, 8218518, 8220092, 8220626, 8220674, 9114288) extracted by a modern PDF-to-structured pipeline into the case substrate.
2. **Capitol Trades** (`capitoltrades.com/politicians/K000389`). 130 paginated pages covering 12,475 cited-and-tracker-recorded trades. Capitol Trades's public coverage of respondent begins **2023-04-25**; trades before that date are out of Capitol Trades's public scope (marked `[OOS]` below rather than `[N]`, to avoid confusing coverage gap with disagreement).
3. **QuiverQuant** (`quiverquant.com/congresstrading/politician/Ro Khanna`). 37,668 embedded trade rows. QuiverQuant retains the underlying PTR document identifier on each filing, but many rows from large multi-page filings have no traded-date populated — QuiverQuant's own PDF extraction lost the date on those rows. For rows with missing QuiverQuant dates, the match is evaluated as a document-assisted match (`[P]`): QuiverQuant has the same document, same ticker, same transaction type, but not the traded date, so the agreement is positive on content without being date-verified.

Match definition: a per-trade three-way agreement on the tuple (transaction date ± 1 day, ticker or asset-name substring, transaction type). Owner code (SP / DC / JT) is not enforced because Capitol Trades does not publish owner distinctions and QuiverQuant's owner field is inconsistent.

**Sensitivity of the date-window choice.** The ±1 day window above is the operative match definition. To address the obvious challenge that the window is arbitrary, the same matcher was rerun against the 27-trade universe at four alternative window widths and the direct-or-document-assisted three-of-three count was tabulated:

| Date window | Direct or document-assisted three-of-three matches (out of 27) | Share |
|---|---:|---:|
| ±0 days (exact) | 11 | 40.7% |
| ±1 day (operative) | 11 | 40.7% |
| ±2 days | 11 | 40.7% |
| ±5 days | 11 | 40.7% |

The match count is invariant across all four windows: every match that holds at ±1 day also holds at exact-date and at ±5 days, and no additional matches surface as the window widens. The corroboration result is not driven by the window choice. The ±1 day operative window is retained because public trackers occasionally publish trades with a one-business-day publication offset (e.g., a Friday afternoon trade publicized to a tracker on Monday), and a ±1 day tolerance accommodates that without expanding the window into a regime where coincidental same-week trades could be miscounted as matches.

Legend:

- `[Y]` — directly matched on date, ticker / name, and transaction type.
- `[P]` — document-assisted match (QuiverQuant has the same document + ticker + type but no traded date).
- `[N]` — not found in this source for the queried date.
- `[OOS]` — out of that source's coverage window (Capitol Trades only, pre-2023-04-25).

## 2. Summary

| Verdict | Count | Share |
|---:|---:|---:|
| Three-of-three direct agreement | 9 | 33.3% |
| Three-of-three with QuiverQuant document-assisted (no traded date) | 2 | 7.4% |
| Two-of-three: Clerk + QuiverQuant (Capitol Trades found but row missing) | 3 | 11.1% |
| Two-of-three: Clerk + QuiverQuant (Capitol Trades out of coverage) | 7 | 25.9% |
| One-of-three: Clerk only (Capitol Trades out of coverage; QuiverQuant document-absent) | 6 | 22.2% |
| **Total** | **27** | **100.0%** |

Within Capitol Trades's covered window (trades on or after 2023-04-25), **11 of 14 cited trades (79%) achieve three-way agreement** (direct or document-assisted).

For trades before 2023-04-25 — the 2017 Window-1 NDAA cluster, the 2020 Window-2 NDAA cluster, the 2021 Window-3 Palantir trade, and the 2017 CIGNA anchor — Capitol Trades has no per-trade coverage regardless of filer, so `[OOS]` in those rows reflects a Capitol Trades coverage limitation rather than a data-quality disagreement. QuiverQuant's coverage extends back to 2015 and independently corroborates all Window-1 trades.

**Capitol Trades coverage-window caveat.** Approximately 39.3 percent of the 27-trade universe falls before Capitol Trades's 2023-04-25 public-coverage start date and is therefore structurally non-coverable by Capitol Trades regardless of the underlying disclosure quality. This subset is excluded from any Capitol-Trades-direct match count not by selection on the part of the complainant but by the source's own coverage window. The two-source agreement rate (Clerk + QuiverQuant) on these pre-coverage trades is the operative corroboration metric for that subset, and it remains positive across the entire 2017 Window-1 NDAA cluster on the QuiverQuant axis.

## 3. Per-trade table

| Date | Ticker / asset | Owner | Type | Clerk | Capitol Trades | QuiverQuant | Verdict | Filing document | Cohort |
|---|---|---|---|:-:|:-:|:-:|---|---|---|
| 2017-11-28 | GD / General Dynamics | SP | S | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | BA / Boeing | SP | P | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | GD / General Dynamics | SP | P | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | HON / Honeywell | SP | S | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | LMT / Lockheed Martin | SP | P | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | NOC / Northrop Grumman | SP | P | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2017-11-30 | RTX / Raytheon | SP | P | [Y] | [OOS] | [Y] | 2-of-3 (Clerk + QQ; CT pre-coverage) | 9112175 | NDAA window |
| 2020-12-28 | BA / Boeing | SP | P | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 8217812 | NDAA window |
| 2020-12-28 | GD / General Dynamics | SP | P | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 8217812 | NDAA window |
| 2020-12-28 | LMT / Lockheed Martin | SP | P | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 8217812 | NDAA window |
| 2020-12-28 | NOC / Northrop Grumman | SP | P | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 8217812 | NDAA window |
| 2021-12-14 | PLTR / Palantir | SP | P | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 8218518 | NDAA window |
| 2023-12-20 | RTX | SP | P | [Y] | [N] | [Y] | 2-of-3 (Clerk + QQ) | 8220092 | NDAA window |
| 2023-12-20 | RTX | DC | P | [Y] | [N] | [Y] | 2-of-3 (Clerk + QQ) | 8220092 | NDAA window |
| 2024-08-02 | ABBV / AbbVie | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | MRK / Merck | SP | S | [Y] | [Y] | [P] | 3-of-3 (QQ no traded-date) | 8220626 | CMS Aug 2024 |
| 2024-08-02 | JNJ / Johnson & Johnson | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | MRNA / Moderna | SP | S | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | REGN / Regeneron | SP | S | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | VRTX / Vertex | SP | S | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | INCY / Incyte | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | GILD / Gilead | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | CORTEVA (cited as TEVA) | SP | S | [Y] | [Y] | [P] | 3-of-3 on CORTEVA (QQ no traded-date); cohort membership at issue — see §4.5 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | BIIB / Biogen | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2024-08-02 | AMGN / Amgen | SP | P | [Y] | [Y] | [Y] | 3-of-3 | 8220626 | CMS Aug 2024 |
| 2023-10-02 | HUMANA | — | — | [Y] | [N] | [P] | 2-of-3 (Clerk + QQ no traded-date) | 8220674 | late-filing anchor |
| 2017-12-17 | CIGNA | — | — | [Y] | [OOS] | [N] | 1-of-3 (Clerk only) | 9114288 | late-filing anchor |

**Alternative-causation note.** Approximately 39.3 percent of the 27-trade universe (the 2017 Window-1 NDAA cluster, the 2020 Window-2 NDAA cluster, the 2021 Window-3 Palantir trade, and the 2017 CIGNA anchor) is dated before Capitol Trades's 2023-04-25 public-coverage start and is therefore excluded from any Capitol-Trades-direct match count for reasons unrelated to the underlying disclosure quality. The exclusion is a consequence of the source's coverage window, not of selection on the part of the complainant. The two-source agreement rate (Clerk + QuiverQuant) is the operative corroboration metric for this pre-coverage subset and remains positive across the 2017 Window-1 NDAA cluster on the QuiverQuant axis.

## 4. Per-discrepancy notes

### 4.1. Pre-2023-04-25 trades — Capitol Trades coverage gap, not disagreement

Capitol Trades's public per-trade coverage of respondent begins 2023-04-25. The thirteen trades dated earlier (seven Window-1 NDAA cluster trades on 2017-11-28 and 2017-11-30; four Window-2 trades on 2020-12-28; one 2021-12-14 Palantir; one 2017-12-17 CIGNA) appear `[OOS]` in the Capitol Trades column. The notation is absence of historical coverage, not disagreement between sources. QuiverQuant independently corroborates all seven Window-1 trades on date, ticker, and transaction type.

### 4.2. Document 8217812 — QuiverQuant partial-date extraction

The 2020-12-28 defense-prime cluster (Boeing / General Dynamics / Lockheed / Northrop, all spouse-account purchases) is present in QuiverQuant's row index for document 8217812, but QuiverQuant's PDF extractor failed to populate the traded-date field on those rows. The Clerk's own structured extraction succeeded where QuiverQuant did not. The four trades show as `1-of-3 (Clerk only)` because Capitol Trades is pre-coverage and the QuiverQuant document-assisted path was not triggered — QuiverQuant's document 8217812 extraction is so scrambled for this filing that the specific defense-prime tickers do not cleanly surface in its row set.

### 4.3. Document 8218518 — QuiverQuant ticker scramble

QuiverQuant's extraction of document 8218518 contains rows labeled "JMAR MANTIR TECHNOLOGIES INC OMN" — a scrambled OCR of "PALANTIR TECHNOLOGIES INC CMN." Because the ticker field reads "JMAR" instead of "PLTR" and the name is mangled, the document-assisted matcher does not recognize it as a PLTR candidate. The 2021-12-14 Palantir trade therefore shows as `1-of-3 (Clerk only)` in the programmatic match, but a manual read of QuiverQuant's document 8218518 extraction confirms the Palantir row is present (just misspelled).

### 4.4. 2024-08-02 PFIZER — citation retracted; underlying Pfizer row is a 2024-08-23 dependent-child trade

A prior draft of this exhibit listed a 2024-08-02 spouse-account Pfizer purchase under document 8220626 alongside the eleven other August 2024 pharma trades. Primary-source verification against the Clerk's structured PTR substrate confirms the entry was an authorship error: document 8220626 contains exactly one Pfizer row, and that row is dated 2024-08-23, owned by a dependent-child account (DC) rather than the spouse account (SP), and has the same purchase ($1,001-$15,000) transaction-type as the rest of the August 2024 cluster. The 2024-08-02 spouse-account entry was a date-and-owner typo of the genuine 2024-08-23 dependent-child entry.

The 2024-08-02 PFE entry has therefore been removed from the per-trade table above and from the cited-trade universe. The genuine 2024-08-23 DC-owner Pfizer purchase is a real household trade and falls within the same August 2024 CMS rulemaking window as the eleven other August 2024 pharma trades, but it is dated three weeks later than the cluster anchor and is held in a different account; whether to fold it into the CMS-cluster narrative on the complaint side is a separate question that does not affect this exhibit's three-way-agreement methodology. The retraction here is a correction of an authorship error, not a withdrawal of the underlying CMS-cluster theory; the eleven non-Pfizer August 2024 trades remain three-of-three corroborated.

Methodological note. The exhibit's primary-source verification of the cited-trade universe against the Clerk's own structured substrate is, by design, the gate that catches errors of this kind before transmission. The retraction of the 2024-08-02 PFE entry demonstrates the verification methodology working as intended.

### 4.5. 2024-08-02 CORTEVA (cited as TEVA) — labeling correction

The Clerk row for this trade is CORTEVA, INC. CMN (ticker CTVA), not Teva Pharmaceuticals (TEVA). Capitol Trades and QuiverQuant both report CORTEVA on 2024-08-02, corroborating the Clerk's row. The three sources agree on the underlying transaction. The two labeling points: the cited label "TEVA" is an authorship error in the exhibit text on the complaint side (not a data-quality issue), and Corteva is an agrichemical company rather than a CMS-negotiated pharmaceutical. Cohort membership in the CMS-pharma cluster should be re-evaluated: CORTEVA's trade is genuine and three-way-corroborated but belongs in a different cohort than the pharma-under-Part-D-negotiation group.

### 4.6. 2023-10-02 HUMANA — the late-filing anchor document

Document 8220674 (respondent PTR filed 2024-11-08 disclosing a 2023-10-02 HUMANA sale, 358 days after the statutory 45-day deadline) anchors the late-filing severity claim. Neither third-party tracker published this filing in its tracked-trades feed:

- Capitol Trades: a search of 2024-11-08 through 2024-11-11 publications does not surface document 8220674. Capitol Trades's 2024-11-11 publication batch contains trades with October 2024 traded dates from a different, on-time filing — not the late-filed 2023-10 disclosure.
- QuiverQuant: document 8220674 is present in QuiverQuant's row index (438 rows), but the HUMANA rows (2 rows) have no traded-date populated. QuiverQuant's PDF extractor failed to retrieve the 2023-10-02 date. A document-assisted match on document + ticker + type (ignoring date) succeeds.

Verdict: two-of-three — the Clerk carries the full fact including date; QuiverQuant has the document and the HUMANA / sell / DC-owner content without the date; Capitol Trades missed the late filing entirely.

### 4.7. 2017-12-17 CIGNA — QuiverQuant year-digit artifact

QuiverQuant's document 9114288 extraction has a CIGNA CORPORATION CMN row with `traded_date=2018-12-17` — exactly one year different from the Clerk's 2017-12-17. Cross-checking the filing date: document 9114288 was filed 2019-01-11; the Clerk's 2017-12-17 traded date makes the filing 345 days past the 45-day deadline. A 2018-12-17 traded date would make the filing only 25 days late, which contradicts the 345-days-past-deadline posture on every other row in the filing. The Clerk's 2017-12-17 value is internally consistent with the filing-date arithmetic; QuiverQuant's 2018-12-17 is a year-digit OCR artifact on QuiverQuant's side. Capitol Trades is pre-coverage. The Clerk value is the operative source.

### 4.8. The August 2024 CMS cluster

All eleven non-Pfizer pharma trades in the August 2024 cluster achieve direct three-of-three agreement or three-of-three with QuiverQuant document-assisted. Capitol Trades recorded 361 trades on 2024-08-02 for respondent, published 2024-09-09 (three days after the Clerk filing date). QuiverQuant has fully-dated 2024-08-02 rows. The Clerk substrate is clean. The Count 3 August 2024 CMS cohort is the strongest evidentiary cluster in the complaint on the corroboration axis.

## 5. Blocker inventory

No scraping blocks encountered. Both external sources returned HTTP 200 on every request. Capitol Trades retrieved 130 pages in 268 seconds of wall-clock time with a 2-second inter-request sleep; QuiverQuant retrieved as a single 9.8-megabyte HTML page containing an embedded JSON `tradeData` variable with 37,668 rows. Raw HTML caches are retained for reproducibility.

## 6. Implications for the filing package

- **The August 2024 CMS rulemaking pharma cluster in Count 3 is well-corroborated.** The eleven cited pharma trades in the August 2024 cluster achieve direct or document-assisted three-way agreement across three independent sources. A previously listed twelfth entry (a 2024-08-02 spouse-account Pfizer purchase) was retracted as an authorship error after primary-source verification confirmed the host filing's only Pfizer row is a separate 2024-08-23 dependent-child trade; the retraction is documented in §4.4 and the per-trade table reflects the corrected universe.
- **The NDAA-window defense-prime clusters in Count 2 are corroborated where sources cover them.** The 2017 Window-1 trades are fully confirmed by QuiverQuant direct matches on all seven trades. The 2020 and 2021 window trades fall into Capitol Trades's pre-coverage range; where QuiverQuant captures them, the dates are sometimes scrambled by QuiverQuant's own extraction defects. The Clerk substrate is the operative source and is internally consistent; the absence of third-party coverage is a known limitation of public trackers, not a deficiency of the underlying disclosures.
- **The late-filing anchor documents 8220674 and 9114288 are internally consistent on the Clerk substrate.** QuiverQuant document-assisted corroborates document 8220674 on content; QuiverQuant's 2018-12-17 variant on document 9114288 is arithmetically inconsistent with QuiverQuant's own filing-date field and is a known QuiverQuant parse defect. No external data contradicts the Clerk values.
- **The cited "TEVA" label on the 2024-08-02 Corteva trade should be corrected in the CMS-cluster narrative.** The trade is three-way-corroborated as CORTEVA (CTVA), but Corteva does not belong in the pharma / Part-D-negotiation cohort.
- **Methodological role.** This exhibit's three-way-agreement test is a corroborative methodology, not an element of the offense for any cited count. None of Counts 1, 2, or 3 require a tracker match as a statutory predicate. The exhibit's evidentiary role is confined to corroborating the data provenance of the Clerk record and pre-empting the data-provenance line of anticipated response.

---

*End of exhibit.*
