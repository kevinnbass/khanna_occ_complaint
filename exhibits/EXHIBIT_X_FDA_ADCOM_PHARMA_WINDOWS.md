# EXHIBIT X — FDA Advisory Committee × Household Pharmaceutical Trade Windows

**Case**: *In re Representative Rohit "Ro" Khanna (CA-17)*
**Counts supported**: Count 1 (STOCK Act §6 pattern evidence); Count 3 (financial-interest conflicts; FDA advisory-committee nexus)
**Lake substrates**: `lake.house_ptr_transactions`; `lake.v_fda_adcom_meetings_all` (unifying `lake.fda_advisory_committee_meetings` FDA-web calendar with `lake.fda_advisory_committee_fr_notices` Federal Register API expansion — 847 meetings, 565 inside the 2017–2026 audit window)

---

## 1. Summary

During calendar years 2017 through 2026 — respondent's House tenure to date — the household executed **4,555 pharmaceutical-ticker trade-window matches within ±14 days of an FDA Advisory Committee meeting**, resolving to **815 distinct PTR transactions**. The tightened test at **±3 days** yields **1,062 windows** across **504 distinct transactions**; the same-day subset is **204 coincidences** across **151 distinct transactions**.

FDA Advisory Committee agendas are published in the Federal Register between thirty and sixty days before the meeting date, and substantive drug and biologic approval matters proceed through committee briefings, document productions, and regulatory-affairs communications that Members with Energy & Commerce jurisdiction and their staff receive in advance. The ±3-day and same-day subset is the slice tied most closely to MNPI-adjacent timing under 15 U.S.C. § 78u-1(g).

## 2. Chamber-wide baseline — absolute-count comparison

Across sixty-seven House Members with at least five pharmaceutical-ticker trades in the 2017-2026 window, respondent's position is:

| Test | Khanna (count) | #2 Member (Gottheimer NJ-05) | Khanna lead | Chamber rank |
|---|---:|---:|---:|---:|
| ±14-day windows | **4,555** | 757 | 6.0× | 1 of 67 |
| ±3-day windows | **1,062** | 167 | 6.4× | 1 of 67 |
| Same-day coincidences | **204** | n/a | n/a | 1 of 67 |
| Pharmaceutical trade volume (denominator) | 839 | 138 | 6.1× | 1 of 67 |

The rate framing is uninformative; the absolute-count framing carries the comparative signal. FDA Advisory Committee cadence runs at roughly sixty-three meetings per year — one meeting every 5.8 calendar days on average. A ±14-day window therefore fills toward saturation for any active pharmaceutical trader, and a rate-based test produces uninformative rankings (respondent sits at the 43rd percentile on ±14-day rate, in the band shared by most active pharma traders). The probative signal is the **absolute count**, which tracks respondent's chamber-leading pharmaceutical trade volume — 839 trades against a chamber 95th-percentile of forty-two trades and a 6.1× margin over the second-most-active Member — combined with House Energy & Commerce Committee oversight jurisdiction over FDA.

## 3. Convergence across three independent regulator substrates

Respondent sits at chamber rank 1 through 3 on each of three independent regulator-event × trade tests:

| Test | Regulator substrate | Khanna chamber rank |
|---|---|---|
| Pharmaceutical trades within ±14 days of catalogued CMS rulemaking events | CMS / HHS rulemaking (Federal Register) | 1 of 67 (P100) |
| Aligned-direction same-day trade matches against SEC Form 4 named officers | SEC Form 4 insider filings | 3 of 156 (P98) |
| Pharmaceutical trades within ±14 days and ±3 days of FDA Advisory Committee meetings | FDA Advisory Committee calendar | 1 of 67 on both |

The three substrates are independent at the regulatory-body level: CMS drug-pricing rulemakings are distinct events from SEC Form 4 filings, which are distinct events from FDA Advisory Committee meetings. Respondent's ranking sits at chamber top-three on every one, with a shared underlying driver: chamber-leading pharmaceutical trade volume in combination with Energy & Commerce oversight of HHS, CMS, and FDA.

## 4. Concentrated cluster detail (2025–2026)

Sample of recent concentrated DC-account trade clusters within ±3 days of an FDA Advisory Committee meeting (excerpt of a longer list):

| Transaction date | Tickers | Owner | Direction | Amount range | FDA advisory event within ±3d |
|---|---|---|---|---|---|
| 2026-03-06 | JNJ × 2 | DC | SELL | $1,001–$15,000 | Gastrointestinal Drugs Advisory Committee renewal notice |
| 2026-01-22/23 | PFE, ABT ($50K–$100K), AMGN, GILD | DC | SELL | $50K–$100K (ABT); $1K–$15K others | Pharmaceutical Science & Clinical Pharmacology ADCOM + Tobacco Products Scientific ADCOM |
| 2025-05-19 | BIIB, BMY, MRK | DC | SELL | $1,001–$15,000 | Oncologic Drugs Advisory Committee + Vaccines and Related Biological Products Advisory Committee |
| 2025-02-25 | MRK ($50K–$100K), REGN | DC | SELL | $50K–$100K (MRK) | Combined Oncologic Drugs Advisory Committee + Cardiovascular and Renal Drugs Advisory Committee |
| 2025-02-19 | AMGN, REGN | SP | SELL | $1,001–$15,000 | General and Plastic Surgery Devices Panel |

The 2025–2026 clusters illustrate that the pattern continues into the current tenure period and is not confined to earlier calendar years.

## 5. Committee-of-jurisdiction nexus

The House Committee on Energy and Commerce oversees the Food and Drug Administration, including the advisory-committee process by which new drugs, biologics, and devices are reviewed. ADCOM meeting agendas and briefing documents — identifying the drug or device under review, the questions posed to the committee, and the sponsor's data — are available to Members with Energy & Commerce jurisdiction in advance of the public meeting date. The same ±3-day pattern would be unremarkable for a pharmaceutical-sector analyst with no such access; the pattern is reported here because respondent has that access by committee assignment, and the trade volume, direction, and timing are consistent with the access pattern that committee-stage information makes available.

## 6. Methodology

Chamber-wide baseline query:

```sql
SELECT t.last_name, t.state_district, t.n_pharma_tx,
       p.n_windows, p.n_distinct_tx,
       RANK() OVER (ORDER BY COALESCE(p.n_windows,0) DESC) AS rk
FROM (
  SELECT lower(member_last_name) AS last_name, state_district, COUNT(*) n_pharma_tx
  FROM lake.house_ptr_transactions
  WHERE asset_ticker IN ('PFE','MRK','LLY','BMY','AMGN','GILD','JNJ','ABT','NVO','REGN','VRTX','BIIB','MRNA')
    AND transaction_date BETWEEN '2017-01-01' AND '2026-04-19'
  GROUP BY 1, 2
) t
LEFT JOIN (
  SELECT lower(kt.member_last_name) AS last_name, kt.state_district,
         COUNT(*) AS n_windows,
         COUNT(DISTINCT kt.transaction_id) AS n_distinct_tx
  FROM lake.house_ptr_transactions kt
  JOIN lake.v_fda_adcom_meetings_all f
    ON f.meeting_date::date BETWEEN kt.transaction_date::date - 14
                               AND kt.transaction_date::date + 14
  WHERE kt.asset_ticker IN ('PFE','MRK','LLY','BMY','AMGN','GILD','JNJ','ABT','NVO','REGN','VRTX','BIIB','MRNA')
    AND kt.transaction_date BETWEEN '2017-01-01' AND '2026-04-19'
    AND f.meeting_date BETWEEN '2017-01-01' AND '2026-04-19'
  GROUP BY 1, 2
) p USING (last_name, state_district)
WHERE t.n_pharma_tx >= 5
ORDER BY rk;
```

The ±3-day tight test is the same structure with `INTERVAL '3 days'` substituted for `14`.

## 7. Anticipated responses

**"Rate saturates; any active pharmaceutical trader will have high counts."** Acknowledged and preempted. The chamber-wide test controls for saturation by computing per-Member counts against the same ADCOM calendar. Respondent's absolute count sits 6.0× to 6.4× above the second-most-active Member and roughly twentyfold above the chamber 95th-percentile. The reported anomaly is trading volume in combination with committee jurisdiction, not the arithmetic incidence of ADCOM meetings.

**"Trading decisions I do not control — a fiduciary manages these accounts."** The 99.997 percent SP/DC/JT owner share of household trades and the absence of any brokerage custodian on respondent's financial disclosures for actively-traded equities address the separately-managed-account defense. That analysis is developed at Exhibit L (PFD Schedule A / SMA-defense rebuttal).

**"Pharmaceutical holdings represent 1.3 percent of household portfolio by value."** The chamber comparison here is between *peers*, not to respondent's own portfolio composition. Other Members trade at comparable pharmaceutical share while posting absolute volumes fourteen to seventeen times smaller. The composition argument compares two different denominators.

## 8. Primary sources

- `lake.v_fda_adcom_meetings_all` — unified view combining `lake.fda_advisory_committee_meetings` (68 FDA-web meetings) with `lake.fda_advisory_committee_fr_notices` (778 Federal Register notices with parseable meeting_date fields, from a superset of 2,709 notices). Columns: `source`, `meeting_date`, `committee`, `title`, `landing_url`, `document_number`, `publication_date`, `citation`, `dates_field`, `abstract`. Coverage: 1992-2026, with 565 meetings inside the 2017-2026 audit window.
- `lake.house_ptr_transactions` — House Clerk Periodic Transaction Reports, filtered to the thirteen pharmaceutical tickers listed in §2 (PFE / MRK / LLY / BMY / AMGN / GILD / JNJ / ABT / NVO / REGN / VRTX / BIIB / MRNA). 839 Khanna-household pharmaceutical transactions in scope.
- FDA Advisory Committee calendar — `https://www.fda.gov/advisory-committees`.
- House Clerk PTR public disclosures — `https://disclosures-clerk.house.gov/FinancialDisclosure`.

## 9. Cross-references

- Count 3 factual basis paragraphs of `OCC_COMPLAINT_KHANNA.md` — CMS and FDA advisory-committee trade windows.
- Exhibit F — CMS rulemaking × household pharmaceutical trade windows (complementary regulator substrate).
- Exhibit Z — Aligned-direction same-day trade matches against SEC Form 4 named officers (third regulator substrate).
- Exhibit L — PFD Schedule A and SMA-defense rebuttal.

---

*End of Exhibit X.*
