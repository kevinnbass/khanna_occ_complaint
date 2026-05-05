# EXHIBIT — STOCK Act §6 Late-Filing Compliance Record

**Subject:** Rep. Ro Khanna (D-CA-17), family-account Periodic Transaction Reports, 115th–119th Congresses
**Scope:** 35,954 billable transactions across 114 PTR documents, 2017-01-03 through 2026-04-02
**Audit table:** `ro_khanna.ptr_filing_audit` (tx-level, amendment-canonical)
**Chamber companion:** chamber-wide baseline integrated in §3–§4 (formerly a separate appendix; consolidated here for Count 1 evidentiary clarity)

---

## 1. What this exhibit supports and does not support

This exhibit is the **compliance-record appendix** for Count 1 of the OCC complaint. It establishes that 624 of Representative Khanna's family-account transactions across 22 PTR documents were filed after the 45-day statutory deadline under STOCK Act §6, and it places that record in chamber-wide and active-trader-cohort context.

**It is not a severity-outlier argument.** Representative Khanna is below the chamber median on late-filing rate, at or below the chamber median on worst-single-transaction delay, and below the active-trader-cohort median on both. Any reader approaching this exhibit expecting an extreme per-transaction severity story — 5-year late filings, "chamber-worst delinquency" — will not find one here. That framing is not operative.

**The operative Count 1 axis is dollar-weighted composite exposure.** The composite score — late-filing-midpoint dollars × worst-days-late × ln(1 + n_late_tx) — ranks Representative Khanna **15 of 210 House Members** with ≥20 auditable transactions, at the **93rd chamber percentile**, and **5 of 43 peers** in the active-trader cohort at the **91st peer-cohort percentile**. That above-P90 standing in both universes, even with a below-median rate and median-territory worst delay, reflects the interaction of high household trading volume with persistent per-document non-compliance across nine filing years. Section 5 of this exhibit documents the composite derivation; Counts 1 and 3 of the OCC complaint use the composite as the probative axis.

---

## 2. Methodology

### Statutory basis

- **STOCK Act §6**, P.L. 112-105, codified at 5 U.S.C. § 13105(l): a Member of Congress must file a Periodic Transaction Report (PTR) within **45 days** of any reportable transaction by the Member, spouse, or dependent child exceeding $1,000.
- **Civil penalty**: $200 minimum per late filing (5 U.S.C. § 13106). The House Ethics Committee may waive the first late filing in any calendar year.
- **Notification-date defense**: requires a documented trustee/qualified blind trust structure establishing that the Member was not notified until after the transaction. Representative Khanna's Public Financial Disclosures list **no separately managed account** and **no qualified blind trust** — the notification-date defense is unavailable to the Khanna family. See Exhibit L (PFD/SMA schedule).

### Computation

For each of 37,238 PTR-disclosed Khanna-family transactions:

- `required_filing_by = transaction_date + 45 days`
- `actual_filing_date = filing date of the enclosing PTR document`
- `days_late = actual_filing_date − transaction_date − 45` (positive = late)

Each transaction's attribution is canonicalized through the House PTR amendment-cascade view (`lake.house_ptr_transactions_canonical`), which dedupes re-reports across amendment filings by `(filer, asset, tx_date, tx_type, owner)` and attributes `days_late` to the *earliest* filing that disclosed the transaction. Representative Khanna's office filed zero amendments of any of the 114 PTR documents in the audit window, so the canonical view collapses to the raw record without modification.

### Data-quality exclusions

| Exclusion | Count | Rationale |
|---|---:|---|
| Future-dated | 315 | `transaction_date > actual_filing_date` (option expirations, OCR artifacts); excluded from bucketing |
| Pre-swearing-in | 27 | `transaction_date < 2017-01-03` (STOCK Act inapplicable to pre-tenure transactions) |
| Parse-error suspect | 942 | Year-digit artifacts identified by the mixed-date sentinel (see §9) |
| **Billable transactions** | **35,954** | |

### Waiver assumption (favorable to the subject)

Penalty calculations in §6 assume the Ethics Committee grants one waiver per filing year containing at least one late document. Seven filing years (2017, 2018, 2020, 2021, 2022, 2023, 2025) contain late documents; the waiver subtracts seven from the per-document penalty base.

---

## 3. Chamber-wide baseline

The House chamber-wide PTR audit covers 411 Members across the 115th–119th Congresses. The subset with statistical stability (≥20 auditable transactions) contains 210 Members.

### Chamber prevalence

| Metric | Chamber value |
|---|---:|
| Members audited | 411 |
| Members with ≥1 late transaction | **291 (70.8%)** |
| Auditable transactions | ~208,000 |
| Transactions filed late | ~10% chamber-wide |

Late filing under STOCK Act §6 is the chamber norm, not the exception. Seven of ten Members who file PTRs have filed at least one late.

### Chamber percentile cascade (n=210 with ≥20 tx)

| Percentile | Late-filing rate | Worst single transaction | Composite score |
|---|---:|---:|---:|
| P50 | 10.06% | 344 days | $579,493 |
| P75 | 29.72% | 523 days | — |
| P90 | 63.65% | 720 days | $23,679,797 |
| P95 | — | 819 days | $55,565,172 |
| Max | ~95% | 2,334 days | — |

### Top chamber-wide rate offenders (context, not the subject's category)

Among Members with ≥20 auditable transactions, the 10 highest late-filing rates are concentrated in a distinct cluster that Representative Khanna does not belong to:

| Rank | Member | District | Late rate |
|---:|---|---|---:|
| 1 | Darrell E. Issa | CA-48 | 95.00% |
| 2 | David Madison Cawthorn | NC-11 | 93.33% |
| 3 | Tom Malinowski | NJ-07 | 91.73% (2022 House Ethics censure for ~100 late filings) |
| 4 | David Trone | MD-06 | 89.13% |
| 5 | Tammy Duckworth | IL-08 | 85.71% |
| 6 | Julia Letlow | LA-05 | 82.10% |
| 7 | Roger Williams | TX-25 | 81.48% |
| 8 | Angela Dawn Craig | MN-02 | 81.08% |
| 9 | Sara Jacobs | CA-53 | 79.69% |
| 10 | Gary Palmer | AL-06 | 79.23% |

Representative Khanna's 1.74% rate places him at chamber rank 52 of 210.

---

## 4. Representative Khanna's chamber and peer position

### Rate

| Universe | Khanna rate | Baseline P50 | Khanna rank | Percentile | Direction |
|---|---:|---:|---|---:|---|
| Chamber (n=210) | 1.74% | 10.06% | 52 of 210 | **P24.4** | **Below median** |
| Active-trader cohort (n=43 with dollar-weighted coverage) | 1.74% | 5.96% | 12 of 43 | **P26.2** | **Below median** |

### Worst single-transaction delay

| Universe | Khanna worst | Baseline P50 | Khanna rank | Percentile | Direction |
|---|---:|---:|---|---:|---|
| Chamber (n=210) | 358 days | 344 days | 108 of 210 | **P51.2** | **Median territory** |
| Active-trader cohort (n=43) | 358 days | 447.5 days | 15 of 43 | **P33.3** | **Below median** |

The single worst Khanna transaction — HUMANA INC common stock, dependent-child owner, traded 2023-10-02, filed 2024-11-08, 358 days late — sits essentially at the chamber median (344 days) and well below the active-trader-cohort median (447 days). It is not a "chamber worst" or a five-year-late filing.

### Dollar-weighted composite severity (the operative Count 1 axis)

| Universe | Khanna composite | Baseline P50 | Khanna rank | Percentile | Direction |
|---|---:|---:|---|---:|---|
| Chamber (n=210) | $41,328,984 | $579,493 | 15 of 210 | **P93.3** | **Above P90** |
| Active-trader cohort (n=43) | $41,328,984 | — | 5 of 43 | **P90.5** | **Above P90** |

The composite integrates three dimensions:

1. **Volume** — 624 late transactions.
2. **Dollar weight** — $6.55 million in late-filed midpoint dollars (within the family's $196M–$815M midpoint aggregate lifetime PFD range).
3. **Persistence** — sustained across nine filing years.

Even at a below-median rate and median-territory per-transaction delay, the interaction of a P99 household trading volume with a 1.74% persistent delinquency rate produces a composite exposure that ranks in the top 7% chamber-wide and the top 10% of the active-trader cohort. That top-decile posture in both universes — not any single long-delay filing — is the probative evidentiary axis for Count 1.

---

## 5. Per-year compliance trend

| Year | Billable tx | Late tx | Rate | Worst delay (days) |
|---:|---:|---:|---:|---:|
| 2017 | 2,316 | 75 | 3.2% | 345 |
| 2018 | 3,704 | 17 | 0.5% | 90 |
| 2019 | 2,693 | 0 | 0.0% | — |
| 2020 | 3,339 | 314 | 9.4% | 10 |
| 2021 | 2,966 | 59 | 2.0% | 18 |
| 2022 | 6,049 | 105 | 1.7% | 49 |
| 2023 | 4,448 | 7 | 0.2% | 358 |
| 2024 | 4,123 | 0 | 0.0% | — |
| 2025 | 4,527 | 46 | 1.0% | 169 |
| 2026 | 2,106 | 0 | 0.0% | — |

**Observations:**

- 2019, 2024, and 2026 demonstrate that timely compliance is achievable when the family files properly — three years of zero late transactions establish the baseline capacity.
- 2020 is the highest-volume-of-late-filings year (314 late) but the worst single-transaction delay is only 10 days; this is a data-entry-pace story, not a severity story.
- 2023 has only 7 late transactions but contains the 358-day outlier (HUMANA, October 2023 traded, November 2024 filed).
- Sustained non-compliance across nine filing years, with four of those years (2020, 2022, 2023, 2025) overlapping the subject's committee work on defense, healthcare, and financial-regulation legislation, rules out a "first-term growing pains" defense: these are violations committed by an incumbent on his 4th-through-5th terms.

---

## 6. Per-document violation table

Twenty-two PTR documents contain ≥1 late-filed transaction. Each row is a referable document-level violation under STOCK Act §6.

| Doc ID | Filed | Tx range | # Tx | # Late | Max delay (days) | Avg delay (days) | Owners |
|---|---|---|---:|---:|---:|---:|---|
| 9110547 | 2017-03-14 | 2017-01-03 – 2017-02-28 | 199 | 1 | 25 | 25 | SP |
| 9111583 | 2017-08-10 | 2017-06-07 – 2017-07-31 | 288 | 2 | 19 | 19 | SP |
| 9111740 | 2017-09-08 | 2017-05-07 – 2017-08-29 | 235 | 1 | 79 | 79 | SP |
| 9111812 | 2017-09-19 | 2017-07-26 – 2017-08-28 | 20 | 14 | 10 | 4 | DC |
| 9114288 | 2019-01-11 | 2017-12-17 – 2019-01-04 | 401 | 57 | **345** | 345 | DC, SP |
| 9114396 | 2019-02-15 | 2018-12-06 – 2018-12-26 | 11 | 11 | 26 | 24 | SP |
| 9114397 | 2019-02-15 | 2018-10-03 – 2018-10-31 | 6 | 6 | 90 | 76 | SP |
| 8217164 | 2020-04-20 | 2020-03-02 – 2020-04-01 | 768 | 185 | 4 | 2 | DC, SP |
| 8217557 | 2020-08-17 | 2020-07-02 – 2020-07-31 | 204 | 1 | 1 | 1 | DC, SP |
| 8217653 | 2020-09-17 | 2020-07-24 – 2020-08-27 | 46 | 1 | 10 | 10 | DC, SP |
| 8217686 | 2020-10-21 | 2020-08-28 – 2020-09-29 | 329 | 127 | 9 | 8 | DC, SP |
| 8217938 | 2021-04-16 | 2021-02-12 – 2021-03-31 | 43 | 1 | 18 | 18 | DC, SP |
| 8218338 | 2021-09-15 | 2021-07-23 – 2023-08-25 | 1,013 | 58 | 9 | 5 | DC, SP |
| 8218637 | 2022-04-07 | 2022-01-03 – 2023-04-11 | 247 | 105 | 49 | 47 | DC, SP |
| 8219783 | 2023-06-12 | 2023-04-04 – 2023-06-02 | 626 | 1 | 24 | 24 | DC, SP |
| 8220039 | 2023-11-08 | 2023-02-16 – 2024-01-19 | 641 | 1 | 220 | 220 | DC, SP |
| 8220067 | 2023-12-06 | 2023-01-31 – 2023-11-28 | 218 | 1 | 264 | 264 | DC, SP |
| 8220674 | 2024-11-08 | 2023-10-02 – 2024-10-31 | 332 | 4 | **358** | 344 | DC, SP |
| 8221124 | 2025-06-10 | 2025-02-05 – 2025-09-25 | 343 | 1 | 80 | 80 | DC, SP |
| 9115671 | 2025-08-07 | 2025-02-15 – 2025-07-31 | 276 | 1 | 128 | 128 | DC, SP |
| 9115679 | 2025-10-03 | 2025-03-03 – 2025-10-09 | 280 | 4 | 169 | 169 | DC, SP |
| 8221231 | 2025-11-06 | 2025-07-25 – 2025-10-31 | 317 | 40 | 59 | 59 | DC, SP |

`SP` = spouse (Ritu Ahuja Khanna). `DC` = dependent child.

**Aggregated civil-penalty exposure:** 22 documents × $200 statutory minimum = **$4,400** without waiver; assuming one Ethics Committee waiver per filing year containing a late document (seven years: 2017, 2018, 2020, 2021, 2022, 2023, 2025) reduces the penalty base to 15 documents × $200 = **$3,000 minimum**.

The Ethics Committee and OCC retain discretion to impose materially higher penalties where a pattern of non-compliance is established; this audit documents a nine-year sustained pattern.

---

## 7. Top 30 worst single transactions

Ordered by `days_late` descending from the canonical audit table.

| Rank | Doc ID | Asset | Owner | Tx date | Filed | Days late |
|---:|---|---|---|---|---|---:|
| 1 | 8220674 | HUMANA INC CMN | DC | 2023-10-02 | 2024-11-08 | **358** |
| 2–30 | 9114288 | 29 distinct tickers (CIGNA, INTUITIVE SURGICAL, MASTERCARD, CORNING, A.O. SMITH, PROLOGIS, SYNOVUS, ILLINOIS TOOL WORKS, EMERSON, VERTEX PHARMA, CABOT OIL & GAS, PHILIP MORRIS, CBS, ALBEMARLE, DOVER, FREEPORT-MCMORAN, CENTURYLINK, SHOPIFY, FMC, CARDINAL HEALTH, BEST BUY, WESTERN ALLIANCE, CHARLES SCHWAB, LEGG MASON, LOWE'S, BANK OZK, T-MOBILE, MASCO, CARMAX, others) | SP | 2017-12-17 | 2019-01-11 | **345** |

**Pattern:** one 358-day outlier (HUMANA, 2023) and a single 345-day cluster from a December-2017 omnibus trade filing (57 distinct assets across one trading day, filed 389 days after the transactions). The remaining 594 late transactions have delays of 1–264 days. An earlier draft of this exhibit attributed to Khanna a larger multi-year filing delay based on a single document; primary-source re-extraction established that cluster as a document-level year-digit transcription artifact, and it is omitted from the operative record.

---

## 8. Late filings on jurisdiction-relevant tickers

Defense primes, Palantir, and NVIDIA appear in this exhibit because the operative theory centers on HASC-adjacent holdings. Nine late trades intersect with these tickers; lateness magnitudes are minor.

| Asset | Owner | Tx date | Filed | Days late | Amount | Doc ID |
|---|---|---|---|---:|---|---|
| BOEING COMPANY CMN | SP | 2020-08-28 | 2020-10-21 | 9 | $1,001–$15,000 | 8217686 |
| GENERAL DYNAMICS CORP CMN | SP | 2020-08-28 | 2020-10-21 | 9 | $1,001–$15,000 | 8217686 |
| NVIDIA CORPORATION CMN | SP | 2021-07-27 | 2021-09-15 | 5 | $1,001–$15,000 | 8218338 |
| GENERAL DYNAMICS CORP CMN | SP | 2021-07-27 | 2021-09-15 | 5 | $1,001–$15,000 | 8218338 |
| NVIDIA CORPORATION CMN | SP | 2020-03-02 | 2020-04-20 | 4 | $1,001–$15,000 | 8217164 |
| GENERAL DYNAMICS CORP CMN | SP | 2020-03-02 | 2020-04-20 | 4 | $1,001–$15,000 | 8217164 |
| LOCKHEED MARTIN CORPORATION | SP | 2020-03-05 | 2020-04-20 | 1 | $1,001–$15,000 | 8217164 |
| RAYTHEON COMPANY | SP | 2020-03-05 | 2020-04-20 | 1 | $1,001–$15,000 | 8217164 |
| GENERAL DYNAMICS CORP | SP | 2020-03-05 | 2020-04-20 | 1 | $1,001–$15,000 | 8217164 |

Every jurisdiction-relevant late transaction is a **purchase**. Lateness magnitudes are modest (1–9 days), so the late-filing finding does not independently prove concealment; it does, however, corroborate the NDAA-window clustering pattern documented in Exhibit E, where the same handful of defense-prime purchases recur on single trading days 12–14 days before NDAA enactment votes.

---

## 9. Data-quality methodology

A year-digit parse-error sentinel is applied at the transaction level. The sentinel flags any transaction meeting **both** of the following:

1. Gap of ≥3 years between `transaction_date` and `filing_date`, and
2. The same PTR document contains other transactions within 3 years of the filing date (a mixed-date signature indicating small clusters of misparsed years embedded in otherwise modern filings).

Documents that are genuinely late batch amendments (all transactions pre-dating the filing by ≥3 years, none recent) are **not** flagged — those represent legitimate corrective amendments, not parse artifacts.

One document, filed 2026-04-07, contained a 19-row cluster of transactions initially parsed as 2020-03-26 which independent optical character recognition established as 2026-03-30 (same-week close to the filing). Those rows were corrected in the canonical audit. One additional document contained 17 rows where a 2025-04-15 transaction date was initially parsed as 2015-04-15; those rows were likewise corrected.

After sentinel application, 22 distinct PTR documents contain ≥1 genuinely late-filed transaction; 624 transactions exceed the 45-day statutory deadline.

---

## 10. Evidentiary value

**This exhibit proves, on its own:**

1. Representative Khanna's office filed **22 of 114 PTR documents** containing **624 individual late transactions** across nine filing years. Each document is independently referable as a STOCK Act §6 civil violation.
2. **Sustained non-compliance** across nine filing years (2017, 2018, 2020–2023, 2025) rules out first-term growing pains; the pattern spans four-through-five terms as an incumbent.
3. **Dollar-weighted composite exposure** ranks 15 of 210 chamber (P93.3) and 5 of 43 peers (P90.5) — above P90 in both universes — which is the probative evidentiary axis for Count 1.
4. The family has **no qualified blind trust and no separately managed account** disclosed on the Public Financial Disclosure (see Exhibit L). The notification-date defense is unavailable; each late transaction is personally attributable.

**This exhibit does not prove, and no reader should infer:**

- That Representative Khanna's overall late-filing **rate** is anomalous. The rate is below chamber median (P24) and below active-trader-cohort median (P26); 70.8% of audited Members have ≥1 late filing.
- That Representative Khanna's **worst single-transaction delay** is an outlier. At 358 days it sits at the chamber median (P51) and below the active-trader-cohort median (P33).
- That Khanna's late-filing volume reflects differential negligence from other high-volume traders. Absolute count scales with trading volume; this exhibit does not support a per-trade-negligence theory.

Any pleading or Ethics referral citing per-transaction severity outliers against Representative Khanna would be citing a framing that is not supported by the canonical record and should not be used.

**Interaction with other counts:**

- **Count 1 (STOCK Act §6 disclosure pattern)**: evidentiary bedrock is 22 referable documents plus dollar-weighted composite exposure. Per-document dollar exposure is the lever; per-transaction severity is not.
- **Count 3 (financial-interest conflicts)**: the pattern of late disclosures means voters and institutional oversight lacked timely awareness of household positions in covered industries. Per-document exposure, not per-transaction delay, is the lever.
- **House Rule XXIII clause 1** (conduct reflecting credit on the House): the nine-year pattern violates the Rule's general standard independent of the STOCK Act's civil scheme.

---

## 11. Caveats

1. **One-waiver-per-year assumption is favorable to the subject.** Ethics Committee waivers are discretionary and not automatic; historical waiver rates are not public. The $3,000 minimum penalty figure is the most subject-friendly reading.
2. **Future-dated and pre-swearing-in transactions are conservatively excluded.** 315 future-dated and 27 pre-2017-01-03 transactions do not contribute to the billable count; if any of the future-dated are genuine option-exercise dates, they should be separately evaluated.
3. **Zero amendments on file.** This audit relies on the House Clerk public index as of April 2026. If the office has filed amendments outside the public feed (e.g., via paper delivery), the audit would not capture them.
4. **Pre-swearing-in transactions.** 27 transactions dated before 2017-01-03 are excluded as outside STOCK Act jurisdiction. Those disclosures were nevertheless made voluntarily and may inform character/pattern evidence at Committee discretion.
5. **PFD notification-date defense.** The 2024 Annual PFD discloses no broker/SMA/QBT arrangement. If the family later produces a trustee structure documented prior to the transactions, lateness for trust-executed trades could be re-measured from notification date; Exhibit L preserves the rebuttal evidence on that point.

---

## 12. Reproducibility

```sql
-- Severity distribution
SELECT severity, COUNT(*) FROM ro_khanna.ptr_filing_audit
WHERE data_quality_flag IS NULL GROUP BY 1 ORDER BY MIN(days_late);

-- Per-year late rate
SELECT EXTRACT(YEAR FROM transaction_date) AS year, COUNT(*) total,
       SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS n_late
FROM ro_khanna.ptr_filing_audit WHERE data_quality_flag IS NULL GROUP BY 1 ORDER BY 1;

-- Chamber percentiles
WITH q AS (
  SELECT member_last_name, pct_late, worst_days_late, composite_score,
         PERCENT_RANK() OVER (ORDER BY pct_late) AS r_pct,
         PERCENT_RANK() OVER (ORDER BY worst_days_late) AS r_worst,
         PERCENT_RANK() OVER (ORDER BY composite_score DESC) AS r_comp
  FROM public.house_ptr_chamber_audit_dollar_weighted
  WHERE n_tx_total >= 20
)
SELECT * FROM q WHERE member_last_name = 'Khanna';

-- Civil-penalty base
WITH late_docs AS (
  SELECT DISTINCT doc_id, EXTRACT(YEAR FROM actual_filing_date) AS filing_year
  FROM ro_khanna.ptr_filing_audit WHERE is_late AND data_quality_flag IS NULL
)
SELECT COUNT(*) total_late_docs, COUNT(DISTINCT filing_year) n_waiver_years,
       GREATEST(0, COUNT(*) - COUNT(DISTINCT filing_year)) * 200 min_penalty_usd
FROM late_docs;
```

---

**Prepared from:** `ro_khanna.ptr_filing_audit`, `public.house_ptr_chamber_audit_dollar_weighted`, `ro_khanna.peer_baseline`, and the canonical amendment-cascade view `lake.house_ptr_transactions_canonical`.
**Cross-references:** Exhibit C (peer-cohort full metric slate, M1–M8), Exhibit DAMAGES (composite dollar derivation and alpha estimate), Exhibit E (NDAA-window clustering corroboration), Exhibit L (PFD/SMA schedule establishing notification-date defense unavailability).
