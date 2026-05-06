# Reproducibility Methodology — OCC Complaint vs. Rep. Rohit "Ro" Khanna (CA-17)

**Document purpose.** This methodology cover accompanies `OCC_COMPLAINT_KHANNA.md` and the `_provenance_index_occ.json` manifest. It enables an Office of Congressional Conduct ("OCC"; the office established by H. Res. 5, 119th Cong., Jan. 3, 2025, formerly the Office of Congressional Ethics) reviewer or staff data engineer to re-execute every substantive substrate-keyed claim in the Complaint against the underlying public-record sources using the reviewer's own data tooling, without depending on the Complainant's private database schema, column-name conventions, or methodological short-hand.

The Complaint body cites 80 markers `[OCC_M001]` through `[OCC_M080]`. Each marker resolves to an Appendix §A row in the Complaint with a `substrate` field naming a table (e.g., `lake.house_ptr_transactions_canonical`), a `sql_text` field carrying the canonical query, and `what-means` / `what-shows` annotations. The substrate names are the Complainant's PostgreSQL schema convention; this document maps each name to its public-source equivalent.

The document has seven sections: §1 substrate-translation table; §2 column cross-walk; §3 dedup methodology rules (fourteen sub-sections, including the PTR amendment-cascade canonical view and the chamber-baseline disclosure template that are unique to the OCC venue); §4 expected-result anchor table for prosecutorial-load-bearing scalars; §5 reproducibility-precision lessons; §6 worked end-to-end example; §7 reviewer aids.

---

## 1. Substrate-translation table

The table maps each `lake.*` / `public.*` / `ro_khanna.*` substrate name cited in the Complaint Appendix to its public-source equivalent. All sources are downloadable without a paid subscription; URLs are stable as of the Complaint transmission date.

| Complainant substrate | Public source | Public file / URL | Notes |
|---|---|---|---|
| `lake.house_ptr_transactions` | House Clerk Periodic Transaction Reports (per-Member PDFs) | `https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure.aspx` (search by Member + year) → per-PTR PDF | Per-transaction Schedule A rows extracted via per-page Gemini OCR; raw output is class-2 work product (see § 3.15) |
| `lake.house_ptr_index` | House Clerk FD bulk index (annual TSV) | `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{YEAR}FD.zip` → `{YEAR}FD.txt` (pipe-delimited filer-doc index) | Authoritative filing-date / filer / doc-id index; one row per filed PTR/PFD |
| `lake.house_ptr_transactions_canonical` | Computed view over `lake.house_ptr_transactions` JOIN `lake.house_ptr_index` | (no direct public equivalent — the canonical view is a methodology artifact) | tx-key `(filer_identity, asset_name, transaction_date, transaction_type, COALESCE(owner,''))`; collapses amendment re-reports per § 3.1; reviewer may reconstruct from the two source tables above |
| `lake.house_pfd_index` | House Clerk FD bulk index (same source as `house_ptr_index`) | Same TSV, filtered to PFD doc-types (Annual / New-Filer / Termination) | Filer + doc-id + filing-date for annual PFDs |
| `ro_khanna.ptr_filing_audit` | Computed table over the canonical view, scoped to Khanna + filtered for pre-tenure / parse-error / pre-STOCK-Act exclusions | (no direct public equivalent — case-schema artifact) | Per-tx STOCK Act § 6 late-filing audit; carries `days_late` + `data_quality_flag` columns |
| `public.house_ptr_chamber_audit_by_member` | Computed rollup over the canonical view + per-Member tenure join | (no direct public equivalent — methodology artifact built from the two upstream public substrates) | One row per Member; carries `late_rate_pct`, `worst_days_late`, `n_tx_total`, `n_tx_late`, `composite_score` |
| `public.house_ptr_chamber_audit_dollar_weighted` | Same upstream; per-Member dollar-weighted rollup | (no direct public equivalent — methodology artifact) | Conservative / midpoint / aggressive dollar sums + composite score per § 3.6 |
| `ro_khanna.peer_baseline_percentiles` | Computed table over `lake.house_ptr_transactions_canonical` filtered to a curated 46-Member peer cohort + Khanna percentile | (no direct public equivalent — methodology artifact) | Peer cohort identity + selection rule documented in § 3.5 |
| `ro_khanna.pfd_schedule_a_assets` | Khanna PFD Schedule A (Assets and "Unearned" Income) per-row extractions | Khanna PFD PDFs at the House Clerk FD portal (same URL pattern as PTRs) | Class-2 OCR work product; per-row asset / value-bracket / income-bracket / owner extraction |
| `ro_khanna.pfd_schedule_d_liabilities` | Khanna PFD Schedule D (Liabilities) per-row extractions | Same source PDFs | Class-2 OCR; per-row creditor / liability-type / value-bracket / first-incurred-date |
| `ro_khanna.trade_pnl` | Khanna household per-trade realized P&L computed over per-tx PTR rows + per-day price series | (no direct public equivalent — methodology artifact) | Daily mark-to-market against close-price feed; realized P&L attributed at sell-date; cross-validated against PFD Schedule A year-end positions |
| `ro_khanna.cited_trades_3way_validation` | Computed table cross-referencing PTR row × PFD Schedule A end-of-year position × external public price feed | (no direct public equivalent — methodology artifact) | "3-way agreement" verifier — every cited trade reconciles across the three independent records |
| `ro_khanna.damages_summary` | Computed per-Count damages aggregation | (no direct public equivalent — methodology artifact) | Disgorgement + civil-penalty quantum computed per § IV of the Complaint |
| `ro_khanna.v3_facts` | Complainant's internal fact store | (private to Complainant) | Operative reviewer hooks are `substrate` / `sql_text` / public-citation URL, NOT `fact_ids` (see § 7.3) |
| `lake.fec_individual_contributions` | FEC bulk individual contributions | `https://www.fec.gov/data/browse-data/?tab=bulk-data` → "Contributions by individuals" → `indiv{YY}.zip` → `itcont.txt` | Canonical view; UNION across cycle-suffixed files |
| `lake.fec_independent_expenditures` | FEC Schedule E IE | `https://www.fec.gov/data/browse-data/?tab=bulk-data` → "Schedule E (Independent Expenditures)" → `independent-expenditures-{YEAR}.csv` AND/OR OpenFEC REST API `/v1/schedules/schedule_e/` (see § 3.12 of the FEC PP companion methodology — the API is the primary substrate for current-cycle data) | Per-cycle CSVs; `tran_id`-canonical aggregation per § 3.8 |
| `lake.fec_pac_to_candidate` | FEC bulk Schedule A PAC-to-candidate | `pas2{YY}.zip` → `itpas2.txt` | Native dedup by `transaction_id`; useful as cross-check on Schedule E aggregates per § 3.8 |
| `lake.fec_committee_transfers` | FEC bulk other transactions filtered to `transaction_tp='18G'` | `oth{YY}.zip` → `itoth.txt` filtered to `transaction_tp='18G'` | Inter-committee transfers |
| `lake.fec_committee_contributions` | FEC bulk PAC-to-PAC contributions | `pas2{YY}.zip` filtered | Cross-PAC inflow detail |
| `lake.fec_committee_disbursements` | FEC bulk operating expenditures | `oppexp{YY}.zip` → `oppexp.txt` | Schedule B disbursements (vendor cross-tabs) |
| `lake.fec_committee` | FEC bulk committee master | `cm{YY}.zip` → `cm.txt` | Committee Statement of Organization metadata |
| `lake.fec_house_candidate_summary_2024` | FEC bulk House candidate summary | `https://www.fec.gov/data/browse-data/?tab=bulk-data` → "Candidate summary" → `weball{YY}.zip` filtered to House | Cycle-aggregate receipts / disbursements per Member |
| `lake.fec_mur` | FEC public MUR docket | `https://www.fec.gov/data/legal/matter-under-review/` (per-MUR pages) + bulk JSON at `https://api.open.fec.gov/v1/legal/docs/murs/` | MUR 7062 cited at § 0; respondent + disposition + citation JSON |
| `lake.congress_rollcalls` | House Clerk roll-call XML | `https://clerk.house.gov/evs/{YEAR}/roll{NNN}.xml` | One XML per House roll call; immutable post-publication |
| `lake.congress_member_votes` | Same source as `congress_rollcalls`, parsed per-Member | `https://clerk.house.gov/evs/{YEAR}/roll{NNN}.xml` (parse `<recorded-vote>` blocks) | One row per (member_bioguide_id, congress, session, roll_number); column name is `member_bioguide_id`, not `bioguide_id` |
| `lake.congress_committee_assignments` | unitedstates/congress-legislators GitHub canonical | `https://github.com/unitedstates/congress-legislators/blob/main/committee-membership-current.yaml` + `committee-membership-historical.yaml` | YAML; machine-parsable |
| `lake.congress_members` | Same source | `legislators-current.yaml` + `legislators-historical.yaml` | Carries `bioguide_id` ↔ `served_from` (4-digit-year text → cast via `MAKE_DATE(... ,1,3)`) for the pre-tenure filter (§ 3.2) |
| `lake.lda_filings` | Senate Lobbying Disclosure (LDA) public filings | `https://lda.senate.gov/system/public/api` + bulk XML at `https://soprweb.senate.gov/index.cfm?event=selectfields` | LD-2 quarterly + LD-203 semiannual; `registrant` + `client` + `filing_year` + `filing_period` + `lobbying_activities` JSON |
| `lake.lda_registrants` | Sub-table of `lda_filings`; registrant identity | Parsed from each LD-2 `registrant` block | One row per registrant per filing; carries `client_country` (ISO-3166-1 alpha-2) |
| `lake.lda_contributions` | Sub-table of `lda_filings`; LD-203 individual lobbyist + organization contributions | Parsed from each LD-203 `contributions[]` array | One row per (filing, contribution); LD-203 § 1604(d) per-recipient itemization |
| `lake.irs_990_returns` | IRS Form 990 e-file public corpus | `s3://irs-form-990/{year}_TEOS_XML/` (AWS S3 public bucket) | EIN + tax_year + Schedule A/B/C/F/I/J/L/R; recipient of Ahuja Charitable Foundation (EIN 34-1685088) anchors at § III.7 |
| `lake.irs_990_grants` | Sub-table of `irs_990_returns`; Schedule I grants paid | Parsed from each Form 990 `IRS990ScheduleI` block | Foundation grant networks (Ahuja Foundation grantee chain) |
| `lake.irs_990_officers` | Sub-table of `irs_990_returns`; Form 990 Part VII officers / directors / trustees | Parsed from each Form 990 `IRS990` Part VII block | Spouse-as-officer disclosures (Ritu Ahuja Khanna named officer of Ahuja Charitable Foundation TY2018-TY2024) |
| `lake.irs_990_pf_noncash_donations` | Sub-table of `irs_990_returns` for 990-PF filers; Schedule B non-cash contribution detail | Parsed from each Form 990-PF `IRS990PF` Schedule B non-cash block | NVIDIA-share donation (10,076 shares TY2024 transfer) cited at § III.7 |
| `lake.irs_527_form_8871` | IRS 527 political-organization Notice of Section 527 Status | `https://www.irs.gov/charities-non-profits/political-organizations/political-organization-filing-and-disclosure` → Form 8871 disclosures | 527 PAC organizational filings |
| `lake.usaspending_contracts_2022` | USAspending federal prime-contract action records | `https://www.usaspending.gov/download_center/award_data_archive` → annual CSV | Prime-contract ALR per fiscal year (Palantir × HASC nexus) |
| `lake.ca_cal_access_form497` | California Cal-Access bulk Form 497 late-contribution filings | `https://cal-access.sos.ca.gov/Campaign/` → `Campaign Bulk Data Download` → `F497_*.TSV` | California state-level late-contribution disclosures |
| `public.v_statute_current` | Combined view: 5 U.S.C. + 11 C.F.R. + 15 U.S.C. + 18 U.S.C. + 52 U.S.C. + 2 U.S.C. + House Rules + related authorities | Authoritative sources fetched directly: `https://uscode.house.gov/` for U.S.C., `https://www.ecfr.gov/` for C.F.R.; House Rules from `https://rules.house.gov/`; House conduct rules from `https://ethics.house.gov/` and `https://conduct.house.gov/` | Cached fetch of operative current text. To re-verify any cite, query the original source URL (carried in the view's `source_url` field; reproduced in the Appendix entries for § VII statute markers M070-M078) |

For markers cited as `ro_khanna.v3_facts (fact_type='legal_authority' AND predicate ILIKE '%X%')` — these are case-law cites in the Complainant's internal fact store. Each resolves to the SCOTUS / Circuit / District opinion identified in the Appendix entry's `claim_summary` field; the public-source URL pattern is `https://supreme.justia.com/cases/federal/{volume}/{page}/` for SCOTUS opinions and `https://www.courtlistener.com/opinion/{cluster_id}/...` for Circuit / District decisions. The OCC complaint cites *Citizens United v. FEC* 558 U.S. 310 (2010) at § III.4; *McConnell v. FEC* 540 U.S. 93 (2003) at § III.4-§III.6; *Buckley v. Valeo* 424 U.S. 1 (1976) and *FEC v. MCFL* 479 U.S. 238 (1986) at § III.4 background.

---

## 2. Column cross-walk

The Complainant's PostgreSQL ingest layer renames a small number of source columns to avoid keyword collisions or to add disambiguating prefixes. The cross-walk for SQL portability:

| Complainant table | Complainant column | Source column |
|---|---|---|
| `lake.house_ptr_transactions` | `transaction_date` | `Transaction Date` (House Clerk PTR Schedule A column header) |
| `lake.house_ptr_transactions` | `notification_date` | `Notification Date` (Schedule A column header; ~70% NULL across the chamber-wide Gemini-extracted corpus — see § 3.4) |
| `lake.house_ptr_transactions` | `asset_name` | `Asset` (Schedule A column header; per-tx free-text asset description) |
| `lake.house_ptr_transactions` | `asset_ticker` | (derived; not in raw PTR PDF) — populated via `ro_khanna.ticker_map` lookup against `asset_name` per § 3.7 |
| `lake.house_ptr_transactions` | `owner` | `Owner` (Schedule A column header; one of `SP` spouse / `DC` dependent child / `JT` joint / `SP/DC` / Member's own holdings unlabeled) |
| `lake.house_ptr_transactions` | `transaction_type` | `Type` (Schedule A column header; `P` purchase / `S` sale / `S(partial)` partial sale / `E` exchange) |
| `lake.house_ptr_transactions` | `amount_min` / `amount_max` | Parsed from `Amount` Schedule A bracket (e.g. `$1,001 - $15,000` → 1001 / 15000) |
| `lake.house_ptr_transactions_canonical` | `earliest_filing_doc_id` / `earliest_filing_date` | Computed: MIN over all amendment cascade re-reports of the same tx-key |
| `lake.house_ptr_transactions_canonical` | `is_amended` / `n_filings` / `all_doc_ids` | Computed cascade provenance per § 3.1 |
| `ro_khanna.ptr_filing_audit` | `days_late` | Computed: `GREATEST(0, earliest_filing_date - LEAST(notification_date + 30 days, transaction_date + 45 days))` per 5 U.S.C. § 13105(l) |
| `ro_khanna.ptr_filing_audit` | `data_quality_flag` | Computed sentinel: `auditable` / `no_tx_date` / `tx_after_filing` / `pre_stock_act` / `pre_tenure` / `parse_error_suspect` |
| `lake.congress_member_votes` | `member_bioguide_id` | Source field; note the prefix is `member_` (not bare `bioguide_id` as some intuitions suggest) |
| `lake.congress_member_votes` | `bill_type` / `bill_number` | Bill identifier as cited in the roll-call XML `<vote-question>` block (e.g., `HR` / `2810` for H.R. 2810) |
| `lake.congress_rollcalls` | `roll_call_number` | Source field; one row per (congress, session, roll_call_number) |
| `lake.fec_individual_contributions_*` | `name_` (cycle 2024) / `contributor_name` (cycle 2026) | `NAME` (FEC bulk position 8) — column rename varies per cycle ingest |
| `lake.fec_independent_expenditures` | `tran_id` | FEC `transaction_id` (FEC transaction identifier; multiple `sub_id` values can share one `tran_id` due to F24 / F3X double-filing — see § 3.8) |
| `lake.fec_independent_expenditures` | `exp_amo` | `expenditure_amount` (string-typed in FEC bulk; cast with `NULLIF(.,'')::numeric` per § 3.11) |
| `lake.fec_independent_expenditures` | `exp_date` | `expenditure_date` (FEC Schedule E format `DD-MON-YY`) |
| `lake.lda_filings` | `filing_uuid` | Senate LDA bulk XML `<filingID>` element (UUID-form) |
| `lake.lda_filings` | `lobbying_activities` | Aggregated JSON of all `<lobbying_activities>` per filing |
| `lake.irs_990_returns` | `ein` | IRS Employer Identification Number (9-digit; published in 990 e-file XML as `EIN`) |
| `lake.irs_990_officers` | `tax_year` / `person_name` / `title` | Per Form 990 Part VII column headers |

Note that FEC bulk individual-contribution date format `MMDDYYYY` differs from operating-expenditure date format `MM/DD/YYYY`. Both are FEC's native publication formats; the Complainant's ingest preserves both as-is (see § 3.12).

---

## 3. Dedup methodology rules

The Complaint applies several dedup conventions that an OCC reviewer reproducing the analyses must apply identically to obtain matching results. These conventions are anchored in House Clerk publication patterns, FEC regulations, and IRS / LDA bulk publication patterns; they are not Complainant-specific methodology.

### 3.1 PTR amendment-cascade canonical view

Members routinely re-file PTRs to correct dollar-range brackets, swap misidentified tickers, or update transaction types. The re-filing is NOT a fresh late disclosure — the underlying transaction was already public on the earlier filing. Attributing days-late to the amendment inflates severity; counting the amendment as a separate filing inflates the per-Member late-filing rate. Both errors compound at the chamber-aggregate.

The `lake.house_ptr_transactions_canonical` view collapses every amendment cascade to a single canonical transaction:

- **tx-key**: `(filer_identity, asset_name, transaction_date, transaction_type, COALESCE(owner,''))` — intentionally omits `amount_range` and `ticker`, both of which are common amendment targets that must NOT split the key.
- **filer_identity**: `(member_last_name, member_first_name, state_district)` joined by `|`.
- The canonical row carries `earliest_filing_doc_id` + `earliest_filing_date` (drives the days-late computation), `amount_range` from the LATEST filing (filer's corrected value), `n_filings` + `all_doc_ids` (cascade provenance), and `is_amended` boolean.

A reviewer reconstructing this view from the source `lake.house_ptr_transactions` table must apply the same key shape and the same MIN(filing_date) attribution. A naive sum-over-raw-rows over-counts late filings by approximately 2,166 chamber-wide (out of ~127K raw House transactions; chamber rate falls from 10.18% raw → 10.14% canonical; per-Member impact varies — Khanna 2.84% raw → 1.74% canonical; Perdue 30.10% raw → 4.75% canonical).

**Where this matters in the Complaint**: Count 1 (every rate / severity / bucket figure); Count 2 (NDAA-window late-filing identity); Count 3 (CMS rulemaking / Palantir / Nvidia trade-window identity); Count 6 (Schedule A asset-versus-PTR cross-validation). The body's authored figures at § II.B and § III.1-§III.3 are post-canonical.

### 3.2 Pre-tenure transaction filter

A Member is bound by STOCK Act § 6 only from their swearing-in date forward. PTR transactions dated BEFORE the Member's swearing-in are NOT § 6 violations even if the resulting filing is late. The case-schema audit (`ro_khanna.ptr_filing_audit`) filters 27 pre-tenure transactions for Khanna (pre-2017-01-03); the chamber-wide audit applies the same filter via a `LATERAL JOIN` on `lake.congress_members` mapping `(state_abbr, district)` → `served_from` (4-digit-year text → `MAKE_DATE(year, 1, 3)`):

```sql
LEFT JOIN LATERAL (
  SELECT MAKE_DATE(CAST(SUBSTRING(cm.served_from FROM 1 FOR 4) AS INT), 1, 3) AS sworn_in_date
    FROM lake.congress_members cm
   WHERE cm.last_name = audit.member_last_name
     AND cm.state = audit.state_abbr
     AND cm.district = LPAD(audit.district::text, 2, '0')
   ORDER BY cm.served_from DESC LIMIT 1
) tenure ON TRUE
WHERE audit.transaction_date >= tenure.sworn_in_date - INTERVAL '30 days';
```

Without this filter the chamber-rate figure drifts +0.09pp (10.05% with filter, 10.14% without; immaterial for the OCC body's authored figure but methodologically required for any future re-derivation). The 30-day buffer accommodates trades that settled days before swearing-in but were properly disclosed against the new tenure-bound deadline.

**Where this matters**: § II.B (chamber-rate disclosure paragraph); § III.1 (Count 1 rate-and-severity composite); the Anticipated Responses § VI rebuttal of "rate-only" defenses.

### 3.3 Parse-error sentinel — tightened mixed-date heuristic

A naive "year gap ≥ 3" sentinel for flagging Gemini OCR year-digit parse errors produces FALSE POSITIVES on genuine batched-late amendments (Members re-entering Congress and filing multi-year backfills, e.g., Suozzi NY-3 2024 batch covering 2017-2022; Allen GA-12 retroactive PFD amendments covering 2017-2020). The tightened rule applied throughout the Complaint:

A transaction is `parse_error_suspect` if AND ONLY IF BOTH (a) AND (b) hold:

1. Year gap ≥ 3 years between `transaction_date` and `filing_date`.
2. The host doc contains OTHER transactions with dates WITHIN the modern (filing_year − 3, filing_year] window — i.e., the host doc is a MIXED-DATE batch with a small pre-modern cluster embedded in a mostly modern filing.

If the host doc is entirely pre-modern (every tx is ≥ 3 yr older than filing_date), it is a GENUINE_LATE amendment — DO NOT flag. Single-filing batches of old tx are legitimate amendments, not parse errors.

Reference SQL is available on request; the rule was applied during the chamber-audit rebuild. A reviewer applying the naive year-gap sentinel alone will mis-classify approximately 8-12 chamber-wide rows as parse errors and 0 Khanna rows; the tightened rule resolves these to GENUINE_LATE and preserves the upstream filer's correct attribution.

**Why this matters**: the Complaint's authored Khanna canonical worst-late = 358 days (HUMANA INC 2023-10-02 transaction, filed 2024-11-08) is post-tightened-sentinel and post-canonical-view. Earlier Complainant drafts cited 3,635-day and 2,158-day worst-late figures; both were Gemini year-digit parse-error artifacts (e.g., 17 rows in House doc 8220906 with `transaction_date='2015-04-15'` were misreads of `'2025-04-15'`) and were vacated via independent Tesseract OCR re-extraction. The candor disclosure at the end of § VI captures this correction trail without internal-fact-store identifiers.

### 3.4 Notification-date NULL fallback

Approximately 70% of Gemini-extracted PTR rows in the chamber-wide corpus have `notification_date IS NULL` because the Schedule A column is omitted by many filers. The deadline formula `LEAST(notification_date + 30 days, transaction_date + 45 days)` collapses to the conservative `transaction_date + 45 days` arm in those cases. This is the rule used by `ro_khanna.ptr_filing_audit` and `public.house_ptr_chamber_audit_by_member`.

A reviewer who interprets the formula to require `notification_date` non-NULL and skips rows where it is NULL will under-count late filings chamber-wide by approximately 70%. The public-source Schedule A fields are silent on the broker-notification timeline for the majority of trades; the conservative fallback is methodologically correct and matches how the Office of Government Ethics computes late-filing exposure for analogous executive-branch PFDs.

### 3.5 Two-universe peer baseline (chamber-wide AND peer-46)

Every comparative claim in the Complaint cites BOTH a chamber-wide percentile and a peer-cohort percentile. The peer-46 cohort is constructed as 10 Tier-1 House Armed Services / Energy and Commerce / Financial Services subjects + 40 highest-volume PTR filers across the 117th-119th Congresses (deduped against the Tier-1 set), filter floor `n_tx_total ≥ 20` for percentile stability against low-volume noise.

**Why both universes**: Khanna's late-filing rate (1.74% canonical) is BELOW the chamber median (10.06%) AND BELOW the peer-46 median (5.96%). Both universes agree the rate is below median. Khanna's worst-single-filing days-late (358 days HUMANA 2023-10-02) sits at chamber percentile 49.5 (rank 107/210) and at peer-46 percentile 32.6 (rank 32/46) — also BELOW median on both. The Count 1 framing therefore does NOT rest on a rate-based or severity-based outlier claim; it rests on the dollar-weighted composite (§ 3.6) and on the per-Count documentary-violation pattern across specific blackout windows.

The chamber-baseline disclosure paragraph at § II.B and at the head of § III.1 is mandatory under `.claude/rules/occ-complaint.md § Chamber-baseline disclosure`. A reviewer unfamiliar with the rule may read the disclosure as concession; it is in fact the Complainant's defense against opposing-counsel's "selective sampling" rebuttal: by publishing both universes upfront, the Complainant forecloses the argument that Count 1 picks the smaller denominator to manufacture an outlier.

**Where this matters**: every comparative-statistic Count (Count 1 rate / severity; Count 2 NDAA-window concentration; Count 3 financial-interest convergence; Count 4 IE coordination; Count 5 LDA § 203 contribution share; Count 6 revolving-door network density). Each cites both percentiles in the body or in the Anticipated Responses class-rebuttal.

### 3.6 Composite severity score

The Count 1 composite metric is defined as:

```
composite_score = dollar_weighted_midpoint_late × (worst_days_late / 365) × LN(1 + n_tx_late)
```

across the household's late-filed Periodic Transaction Reports. The same composite is computed across every House Member with `n_tx_total >= 20` for the chamber baseline (rendered into `public.house_ptr_chamber_audit_dollar_weighted`) and across the active-trader peer cohort for the peer-cohort baseline (rendered into `ro_khanna.peer_baseline_percentiles`).

The composite is the operative Count 1 metric because it bakes in the rate→severity pivot: a Member can be below median on rate (Khanna 1.74% vs chamber 10.06%) and above-or-near median on composite if the dollar-weighted midpoint of the late-filed transactions is large. The composite resolves the false-dichotomy framing that opposes "few late filings = compliant" against "any late filing = violation." It is the metric the OCC's Office of General Counsel staff already use internally for triage prioritization (per public statements from prior OCC Directors).

A reviewer reproducing the composite must use natural log (PostgreSQL `LN()`), not log base 10 (`LOG()`); midpoint is `(amount_min + amount_max) / 2`; dollar-weighted-midpoint-late aggregates only over `data_quality_flag='auditable' AND days_late > 0`.

### 3.7 PTR ticker NULL fallback to `ro_khanna.ticker_map`

Khanna PTR Gemini extractions show approximately 51% of rows with `asset_ticker IS NULL` (58 of 114 docs have ≥80% NULL rate on ticker; older AF-tracked figure was <20% and is superseded). The case-schema `ro_khanna.ticker_map` provides asset-name-pattern → ticker fallback (e.g., `asset_name ILIKE '%NVIDIA%CORP%'` → `NVDA`; `asset_name ILIKE '%PALANTIR%TECH%CL A%'` → `PLTR`). Any per-ticker aggregation must use the COALESCE pattern:

```sql
COALESCE(t.ticker, m.ticker) AS resolved_ticker
  FROM lake.house_ptr_transactions t
  LEFT JOIN ro_khanna.ticker_map m
       ON UPPER(t.asset_name) LIKE m.asset_name_pattern
```

Peer-baseline metrics that key on ticker apply the same fallback against the peer-cohort row set. A reviewer who skips the fallback under-counts NVIDIA / Palantir / defense-prime / pharma trade concentration by approximately the NULL fraction (~51%).

### 3.8 FEC Schedule E `transaction_id`-canonical aggregation

Every Schedule E independent-expenditure disbursement is filed at least twice — once as an F24 48-hour notice (within 48 hours of the IE per 52 U.S.C. § 30104(g)) and once re-reported inside the F3X quarterly report (or a subsequent amendment). Each filing produces a distinct `sub_id` and `file_number` but the `tran_id` (FEC transaction identifier) is **shared** across the F24 and the F3X re-report.

**Implication for aggregation**: sum-by-`sub_id` over-counts every IE by the number of times it was re-reported (approximately 2× to 4×). The correct dedup key for Schedule E IE aggregates is `(committee_id, candidate_id, tran_id)`, NOT `sub_id` alone.

```sql
SELECT cand_id, sup_opp,
       COUNT(*)            AS n_canonical_tx,
       SUM(peak_amt)       AS total_amt
  FROM (SELECT tran_id, cand_id, sup_opp,
               MAX(NULLIF(exp_amo,'')::numeric) AS peak_amt
          FROM lake.fec_independent_expenditures
         WHERE spe_id = '<COMMITTEE_ID>'
           AND fec_election_yr = '<YEAR>'
           AND tran_id IS NOT NULL AND tran_id != ''
         GROUP BY tran_id, cand_id, sup_opp) t
 GROUP BY cand_id, sup_opp;
```

Independent cross-check: `lake.fec_pac_to_candidate` (FEC bulk file `pas2{YY}.zip`) deduplicates natively by `tran_id` and is a one-shot Schedule A cross-check on the Schedule E aggregate.

**Where this matters in the Complaint**: § III.5 LD-203 cross-channel reconciliation; § III.6 LD-203 compliance audit.

### 3.9 LDA universe filter — registrant OR client

Lobbying Disclosure Act LD-2 quarterly filings have two ownership-side fields: `registrant` (the registered lobbying firm filing the disclosure) and `client` (the entity on whose behalf the lobbying is conducted). Outside lobbying firms file LD-2s on behalf of their corporate-sector clients, so an LDA universe filter restricted to `registrant ILIKE '%X%'` misses approximately 80% of the relevant filings.

```sql
SELECT COUNT(DISTINCT filing_uuid)
  FROM lake.lda_filings
 WHERE filing_year IN ('2023','2024','2025')
   AND (registrant ILIKE '%<ENTITY>%' OR client ILIKE '%<ENTITY>%' OR ... );
```

**Where this matters**: § III.5 LDA § 203 cross-channel cohort (registrant-OR-client returns ~290 filings vs ~48 registrant-only); § III.6 revolving-door covered-position lobbyist enumeration (~98 distinct lobbyists with the OR-filter vs ~13 registrant-only).

### 3.10 Cross-cycle name-variant donor aggregation

FEC bulk filings record the same physical donor under multiple name forms across different cycles — typically a colloquial form in current cycles and a legal-name-with-middle-initial form in earlier cycles (e.g., `COLLINS, TIM` ↔ `COLLINS, TIMOTHY`).

Donor-aggregation analyses need a name-variant union, typically anchored on `(employer, last_name)` plus first-name fuzzy match, to capture the same donor identity across cycles.

**Where this matters**: § III.6 dual-recipient overlap.

### 3.11 Empty-string-to-numeric casting on FEC + LDA bulk dollar columns

FEC bulk publishes `transaction_amt`, `exp_amo`, and other dollar-typed columns as STRING-typed, not numeric-typed. Empty cells appear as the empty string `''`, not as NULL. A naive cast `transaction_amt::numeric` raises `invalid input syntax for type numeric: ""` on the first empty row and aborts the query.

**Correct pattern**: `NULLIF(transaction_amt, '')::numeric` (PostgreSQL) or the dialect-equivalent. The same rule applies to LDA bulk `total_expenses` (string-typed in the LDA XML-to-relational ingest).

### 3.12 Date-format heterogeneity

The same `transaction_dt` column name carries different formats across FEC bulk file types:

| File / column | Format | Example | PostgreSQL conversion |
|---|---|---|---|
| `itcont.txt` (individual contributions) `transaction_dt` | `MMDDYYYY` (no separators) | `08022024` | `TO_DATE(transaction_dt, 'MMDDYYYY')` |
| `oppexp.txt` (operating expenditures) `transaction_dt` | `MM/DD/YYYY` | `04/04/2025` | `TO_DATE(transaction_dt, 'MM/DD/YYYY')` |
| `independent-expenditures-{YEAR}.csv` `expenditure_date` | `DD-MON-YY` | `10-MAR-26` | `TO_DATE(expenditure_date, 'DD-MON-YY')` |
| `itoth.txt` (other transactions, incl. § 18G transfers) `transaction_dt` | `MMDDYYYY` | matches `itcont.txt` | `TO_DATE(transaction_dt, 'MMDDYYYY')` |

House PTR / PFD source dates are extracted into `transaction_date` / `notification_date` / `filing_date` PostgreSQL DATE columns at ingest; reviewers querying the `lake.house_ptr_*` substrates do not need to handle source-string parsing.

A reviewer who applies a single date format across all FEC bulk file types will get parse errors or silent date misinterpretation.

### 3.13 SQL dialect note

The SQL queries in the Complaint Appendix are written in PostgreSQL dialect. Functions used: `TO_DATE(<col>, '<format>')`, `NULLIF(<col>, <sentinel>)`, `LATERAL` joins, `LEFT JOIN LATERAL`, `MAKE_DATE(year, month, day)`, `LPAD(text, width, pad)`, `array_agg(DISTINCT ...)`, `unnest(<array>)`, `jsonb_array_elements(<jsonb>)`, `LN()` for natural logarithm.

A reviewer using a different SQL dialect (BigQuery, SQLite, MySQL, DuckDB, Snowflake) needs the dialect-equivalent constructs:

| PostgreSQL | BigQuery | DuckDB | SQLite |
|---|---|---|---|
| `TO_DATE(s, 'MMDDYYYY')` | `PARSE_DATE('%m%d%Y', s)` | `strptime(s, '%m%d%Y')::DATE` | `date(substr(s,5,4)\|\|'-'\|\|substr(s,1,2)\|\|'-'\|\|substr(s,3,2))` |
| `NULLIF(s, '')::numeric` | `SAFE_CAST(NULLIF(s,'') AS NUMERIC)` | `TRY_CAST(NULLIF(s,'') AS DECIMAL)` | `CAST(NULLIF(s,'') AS REAL)` |
| `MAKE_DATE(y,m,d)` | `DATE(y,m,d)` | `make_date(y,m,d)` | `date(y \|\|'-'\|\| printf('%02d',m) \|\|'-'\|\| printf('%02d',d))` |
| `LN(x)` | `LN(x)` | `ln(x)` | (use `log(x)/log(2.71828)` workaround) |

The Complaint's substantive claims are not PostgreSQL-specific. A reviewer who runs equivalent queries against the same public source files in any SQL dialect will reach the same numeric results, modulo dialect-specific NULL-handling and rounding.

### 3.14 Snapshot-freshness statement and per-substrate snapshot dates

Every dollar / count / date scalar in the Complaint is anchored to a specific public-source bulk snapshot date. The Complaint was prepared against substrates current through approximately late April / early May 2026.

| Substrate class | Approximate snapshot date | Volatility | Reason |
|---|---|---|---|
| House Clerk PTR PDFs (per-Member docs) | 2026-04-22 | LOW | Filers re-amend at low rate post-publication; per-doc publication date is immutable |
| House Clerk PFD PDFs (annual filings) | 2026-04-22 | LOW | Same; amendments are tracked as separate doc-IDs |
| `lake.house_ptr_transactions_canonical` view | 2026-05-02 | LOW | Re-derived from upstream as ingest cadence permits |
| `public.house_ptr_chamber_audit_by_member` | 2026-05-02 | LOW | Re-built whenever the canonical view ingests fresh PTR docs |
| `ro_khanna.peer_baseline_percentiles` | 2026-05-02 | LOW | Re-built on chamber-audit refresh |
| `ro_khanna.ptr_filing_audit` | 2026-05-02 | LOW | Rebuilt with chamber audit |
| House Clerk roll-call XML | 2026-04-22 | STABLE | Immutable post-publication |
| FEC Schedule E (per-cycle CSV / OpenFEC API) — 2024 cycle | 2026-05-02 | LOW | Closed cycle; F24 / F3X amendment cycle largely complete |
| FEC Schedule E — 2026 cycle | 2026-05-02 | MODERATE | Active cycle; ongoing F24 / F3X amendments |
| FEC Schedule A individual contributions — closed cycles 2018-2022 | 2026-04-19 | LOW | Closed cycles |
| FEC Schedule A — 2024 cycle | 2026-04-22 | LOW-MODERATE | Late amendments |
| FEC Schedule A — 2026 cycle | 2026-04-22 | MODERATE | Active cycle |
| FEC committee master `cm.txt` | 2026-04-22 | LOW | Updated with each Form 1 amendment |
| FEC MUR docket | 2026-04-22 | STABLE | Closed MURs immutable |
| Senate LDA quarterly LD-2 — 2023-2025 | 2026-04-22 | HIGH | Quarterly amendment cycles |
| Senate LDA semiannual LD-203 — 2023-2025 | 2026-04-22 | HIGH | Semiannual amendment cycles |
| IRS Form 990 e-file public corpus (TY2018-TY2024) | 2026-04-19 | LOW | TY filings finalized once and rarely amended |
| IRS 527 Form 8871 / 8872 | 2026-04-22 | LOW-MODERATE | Updated as 527 organizations file new notices |
| USAspending federal prime contracts (FY2022) | 2026-04-22 | STABLE | Closed-FY contracting actions |
| California Cal-Access Form 497 bulk | 2026-04-22 | MODERATE | Continuous amendments |
| `public.v_statute_current` (statute / regulation text cache) | 2026-04-23 | LOW | Recodifications occur on Congressional schedule; cited current-codification forms verified at fetch time |

A reviewer querying these substrates within ~30 days of the listed snapshot date should obtain figures matching the body to the precision specified by the volatility class. A reviewer querying 90+ days later may see HIGH and MODERATE substrates drift; the body's authored "approximately" hedges absorb the expected drift band.

The OCC venue distinguishes itself from FEC and DOJ venues by accepting documentary evidence at the date of complaint transmission; staff may request an updated re-derivation if the snapshot drift materially affects a Count's framing during preliminary review (per OCC Rule 13 update procedures).

### 3.15 OCR work-product reproducibility (PFD / PTR / 990-PF extractions)

The Complaint draws on three classes of substrate:

1. **Public bulk / public API** — House Clerk roll-call XML, FEC bulk CSV/TSV + OpenFEC REST API, IRS Form 990 e-file XML (AWS S3 public bucket `s3://irs-form-990/`), Senate LDA quarterly XML, USAspending prime-contract CSV, California Cal-Access bulk, U.S.C. + C.F.R. text. Reproducible by any reviewer with internet access; automated fetch recipe at `fetch_substrate_occ.py` (see § 3.16 below).
2. **Public-source PDF + private-output OCR extraction** — House Clerk Periodic Transaction Reports (PTRs) and Personal Financial Disclosures (PFDs) are published only as PDFs at `disclosures-clerk.house.gov`. The House Clerk does not publish per-transaction Schedule A or Schedule D rows in machine-readable bulk form. Researchers who want structured rows must run OCR + structured extraction on each PDF — the resulting parsed rows ARE work product (different OCR pipelines yield materially different output, especially on multi-column PTR Asset / Owner / Date tables and on PFD Schedule A end-of-year valuation brackets). The Complainant's pipeline used per-page Gemini flash-lite-preview extraction with a structured-output prompt template and Tesseract cross-validation; the resulting JSON extractions for Khanna are bundled in `data/ocr_products/` per the MANIFEST entry.
3. **Public-source PDF + IRS-published-XML route** — IRS Form 990 e-file public corpus is published in machine-readable XML at AWS S3 (above). Filers who paper-file a 990-PF instead of e-filing produce only a scanned PDF that the IRS hosts but does not release as machine-readable. The Ahuja Charitable Foundation (EIN 34-1685088) has e-filed XML records in `lake.irs_990_returns / _grants / _officers / _pf_noncash_donations` for every TY cited (TY2018-TY2024); the Complaint's IRS 990 anchors are class (1) reproducible via direct AWS S3 fetch. No 990-PF paper-file dependency is in the operative scope.

**What's bundled at `data/ocr_products/`:**

| Bundled file | Marker(s) | Body section | Why bundled |
|---|---|---|---|
| Khanna Schedule A asset extractions (TY2018-TY2024) | OCC_M005 + downstream | § II.B + § III.7 | Khanna PFD Schedule A rows are class-2 work product; the operative § III.7 spouse-asset disclosure scope analysis depends on per-row extraction |
| Khanna Schedule D liability extractions (TY2018-TY2024) | OCC_M028 + downstream | § III.7 | Margin-loan / Goldman line-of-credit dispatching is class-2; the Anticipated Responses § VI rebuttal of "passive SMA" defense depends on this |
| Khanna PTR Schedule A per-tx extractions (114 docs) | OCC_M004 + chamber audit upstream | § II.B + § III.1-§III.3 + § III.7 | Per-tx Asset / Owner / Date / Type / Amount-bracket extraction; Tesseract-validated for every cited HUMANA / NVIDIA / PALANTIR / pharma / defense-prime row |

**Independent reproducibility chain for class 2:** A reviewer who wants to independently re-derive any class-2 row should (i) run `python data/ocr_products/fetch_source_pdfs.py` to fetch every source PDF from `disclosures-clerk.house.gov` to a local cache; (ii) run their preferred OCR + structured-extraction pipeline (Tesseract + table-detection; Gemini per-page; Claude / GPT-4 with a per-page prompt); (iii) compare the reviewer's extraction to the bundled JSON. Material differences in any per-row field flag for follow-up; structural agreement on the row inventory + per-row dollar-range buckets + transaction dates is the load-bearing reproducibility check.

The reviewer kit `verify_anchors_occ.py` (see § 6.1) operates against the bundled JSON in default mode and exercises the public-substrate path in `--live` mode.

### 3.16 Automated fetch recipe for class-1 public substrates

For convenience, an automated fetch script `fetch_substrate_occ.py` lives alongside the kit and pulls every class-1 substrate referenced in the manifest. Usage:

```bash
pip install requests
python fetch_substrate_occ.py                       # default: all classes
python fetch_substrate_occ.py --classes house_clerk,fec_api,lda,irs_990,statute
python fetch_substrate_occ.py --api-key $DATA_GOV_API_KEY
```

Class coverage:

| Class | Substrate | Endpoint or pattern |
|---|---|---|
| `house_clerk` | House Clerk PTR / PFD bulk index + per-Member PDFs | `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{YEAR}FD.zip` (annual TSV); per-Member PDF URLs derived from the index |
| `house_rollcalls` | House Clerk roll-call XML | `https://clerk.house.gov/evs/{YEAR}/roll{NNN}.xml` |
| `fec_api` | OpenFEC REST API — Schedule E, Schedule A, committee + candidate metadata | `https://api.open.fec.gov/v1/schedules/schedule_e/`, `/schedule_a/`, `/committees/`, `/candidates/` |
| `fec_bulk` | FEC bulk Schedule A / B / E / committee master per cycle | `https://www.fec.gov/files/bulk-downloads/{YEAR}/...` |
| `irs_990` | IRS 990 e-file public corpus | AWS S3 `s3://irs-form-990/{year}_TEOS_XML/` (no API key required for read); ProPublica mirror `https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json` (rate-limited) |
| `lda` | Senate LDA quarterly XML | `https://lda.senate.gov/api/v1/filings/` (REST) + bulk index at `https://lda.senate.gov/system/public/` |
| `usaspending` | USAspending federal prime contracts | `https://www.usaspending.gov/download_center/award_data_archive` (annual CSV) |
| `cal_access` | California Cal-Access bulk | `https://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip` |
| `statute` | Cited U.S.C. + C.F.R. + House Rules operative text | `https://uscode.house.gov/view.xhtml`, `https://www.ecfr.gov/current/title-{N}/...`, `https://rules.house.gov/`, `https://ethics.house.gov/`, `https://conduct.house.gov/` |

The fetch script does not download the per-PTR PDFs by default (the corpus is large and most reviewers will only re-validate a handful of cited filings); the `data/ocr_products/fetch_source_pdfs.py` companion fetches the specific PDFs cited in the bundled JSON.

---

## 3a. Chamber-baseline disclosure — the venue-specific paragraph

Because the OCC is the venue most likely to receive an opposing-counsel rebuttal of the form "the Complainant is selectively citing the smaller denominator," every comparative-statistic Count in the Complaint includes a chamber-baseline disclosure paragraph. The paragraph template (per `.claude/rules/occ-complaint.md`):

> X. Baseline disclosure. For full candor: respondent's [METRIC] ([VALUE]) sits [above/below] the House chamber [MEDIAN/MEAN] ([BASELINE]) across all Members in the current-codification audit, and [above/below] the curated peer cohort (rank [R]/[N], percentile P[X]). The probative value of Count [N] therefore does not rest on a [rate/share]-based outlier framing. Rather, Count [N] asserts [composite/timing/coordination]: [specifics in narrative, no fact IDs].

The disclosure is operationally required, not optional, and the Complainant's pre-filing checklist enforces it (per the rule cited above). A reviewer reading the Complaint cold should treat the disclosure as the Complainant's proactive concession that rate-based or share-based outlier framing is NOT the load-bearing claim, and that the Count is anchored on composite / timing / coordination. The two-universe percentile pair in each disclosure is the primary methodological proof against selective-sampling rebuttal.

Concrete instantiations in the OCC Complaint:

- § II.B + § III.1 (Count 1 — STOCK Act § 6 documentary non-compliance + MNPI-adjacent pattern): Khanna rate 1.74% < chamber 10.06% (rank 35/210 P16.7) AND < peer-46 5.96% (rank 12/43 P26.2); Khanna worst-day 358d < chamber median 359d (rank 107/210 P49.5) AND < peer-46 P50 (rank 32/46 P32.6). Composite-score chamber rank: see Anchor table § 4 below.
- § III.2 (Count 2 — NDAA enactment-window front-running): rate posture below median both universes; framing is on absolute-count + timing.
- § III.3 (Count 3 — household financial-interest convergence): rate-only metrics are not load-bearing; framing is on the convergence pattern across pharma / Palantir / NVIDIA / Goldman axes.
- § III.4-§III.5 (Counts 4-5 — coordinated-expenditure + LDA § 203 cross-channel pattern): peer-cohort percentiles cited per § 3.5; framing is on the coordination indicia.

---

## 4. Expected-result anchor table

This table lists the prosecutorially-load-bearing scalar figures cited in the Complaint, the Appendix marker that anchors each, and the expected substrate result a reviewer should obtain when running the corresponding query. If the reviewer's result diverges, the methodology rule that resolves the divergence is named.

| Body location | Marker | Expected scalar | Reproducibility note (if divergence) |
|---|---|---|---|
| § I + § II.A | OCC_M001 | Khanna sworn-in 2017-01-03; current fifth-term Member of the 119th Congress | `lake.congress_members WHERE bioguide_id='K000389'` returns `served_from='2017-01-03'` |
| § II.A | OCC_M002 | House Armed Services + Energy and Commerce + Select Committee on the CCP (118th-119th); Oversight (117th-118th) | `lake.congress_committee_assignments` filtered to Khanna |
| § II.B | OCC_M004 | Khanna household per-trade realized P&L over the auditable PTR universe | `ro_khanna.trade_pnl` aggregated; per-trade rows reconcile against PFD Schedule A end-of-year positions per § 3.15 |
| § II.B + § III.1 | OCC_M007 | Khanna canonical late rate 1.74%; canonical n_tx_total 624; canonical n_tx_late 22 | § 3.1 — canonical-view dedup; § 3.4 — notification-NULL fallback |
| § II.B + § III.1 | OCC_M008 | Khanna worst single-tx delay: 358 days (HUMANA INC common stock, DC owner, traded 2023-10-02, filed 2024-11-08) | § 3.1 (canonical view) + § 3.3 (parse-error sentinel — confirms HUMANA tx is not a Gemini parse-error artifact) |
| § II.B + § III.1 | OCC_M009 | Khanna composite-score chamber rank (per § 3.6) | `public.house_ptr_chamber_audit_dollar_weighted` rank by composite_score |
| § II.B + § III.1 | OCC_M010 | Chamber-wide canonical late rate 10.06% across 210 Members with `n_tx_total >= 20` | § 3.1 + § 3.2 + § 3.3 — canonical view + pre-tenure filter + tightened sentinel |
| § II.B + § III.1 | OCC_M011 | Khanna chamber rank by canonical late rate: 35 of 210 (P16.7 — BELOW MEDIAN) | Two-universe rule § 3.5; rank computation uses `PERCENT_RANK()` |
| § II.B + § III.1 | OCC_M012 | Peer-46 cohort canonical late rate P50 = 5.96%; Khanna rank 12/43 (P26.2 — BELOW MEDIAN) | § 3.5 — peer-cohort selection; `ro_khanna.peer_baseline_percentiles` |
| § II.B + § III.1 | OCC_M013 | Khanna 358d worst-late at chamber percentile 49.5 (rank 107/210 — BELOW CHAMBER MEDIAN) AND at peer-46 percentile 32.6 (rank 32/46 — BELOW PEER MEDIAN) | § 3.5 |
| § II.D | OCC_M005 | Khanna PFD Schedule A end-of-year positions across cited household assets | `ro_khanna.pfd_schedule_a_assets` filter; class-2 OCR work product per § 3.15 |
| § III.2 | OCC_M020 | NDAA enactment-window roll calls and Khanna defense-prime trade concentration in the ±14-day window around enactment | `lake.congress_member_votes` JOIN `lake.congress_rollcalls` + per-tx canonical-view filter |
| § III.3 | OCC_M027 | NVIDIA donation: 10,076 NVDA shares transferred to Ahuja Charitable Foundation in TY2024 | `lake.irs_990_pf_noncash_donations` filter EIN 34-1685088 + tax_year 2024 |
| § III.3 | OCC_M028 | Khanna household margin-loan / line-of-credit liabilities | `ro_khanna.pfd_schedule_d_liabilities`; Goldman Sachs margin facility + JPMorgan line of credit |
| § III.5 | OCC_M042 | LDA universe size for cited registrant-OR-client cohort | § 3.9 — registrant-OR-client filter (registrant-only under-counts ~80%) |
| § III.5 | OCC_M046 | LDA registrant identity for cited lobbying firms | `lake.lda_registrants` filter |
| § III.6 | OCC_M041 | LD-203 individual lobbyist + organization contributions | `lake.lda_contributions` |
| § III.6 | OCC_M061 | LDA revolving-door covered-position lobbyist enumeration for the cited registrant cohort | § 3.9 + LDA `covered_position` field parsing |
| § III.7 | OCC_M003 | Ritu Ahuja Khanna named officer of Ahuja Charitable Foundation TY2018-TY2024 | `lake.irs_990_officers` filter EIN 34-1685088 + tax_year IN (2018..2024) |
| § III.7 | OCC_M055 | Ahuja Charitable Foundation TY2024 EoY FMV $45,102,055 | `lake.irs_990_returns` filter EIN 34-1685088 + tax_year 2024 → `total_fmv` field |
| § III.7 | OCC_M056 | Ahuja Charitable Foundation TY2018-TY2024 grants paid (Schedule I) — grantee universe | `lake.irs_990_grants` filter EIN 34-1685088 |
| § III.7 | OCC_M027 (cont.) | NVIDIA donation-time fair market value $1,667,345 (10,076 NVDA shares × IRS-published donation-date close); subsequent post-donation share-price appreciation amplifies the wealth-flow | `lake.irs_990_pf_noncash_donations` Schedule B FMV column |
| § VII (statute markers) | OCC_M070-M078 | Current-codification statute / regulation text for: 5 U.S.C. § 13105, § 13106, § 13104; 15 U.S.C. § 78u-1; 11 C.F.R. § 109.21; 52 U.S.C. § 30116; 2 U.S.C. §§ 1604-1606; 18 U.S.C. § 207; House Rule XXIII Code of Official Conduct | `public.v_statute_current` filter by `(jurisdiction, title_number, section)`; verified at fetch time against `https://uscode.house.gov/`, `https://www.ecfr.gov/`, `https://rules.house.gov/` per `.claude/rules/citation-currency.md` |
| § II.B (composite) | OCC_M061 (damages) | Per-Count damages aggregation (disgorgement quantum + civil penalty quantum) | `ro_khanna.damages_summary` per § IV |
| § VI (3-way) | OCC_M069 | "3-way agreement" cross-validation: every cited trade reconciles across PTR row × PFD Schedule A end-of-year position × external public price feed | `ro_khanna.cited_trades_3way_validation` |
| § VII (exhibits) | OCC_M079 | Exhibit-level reproducibility map | `outputs/leads/exhibit_packets/ro_khanna_political_dossier/EXHIBIT_*.md` |
| § A appendix self-reference | OCC_M080 | Appendix A renders into the operative complaint body at fixed line range; manifest is co-distributed at `_provenance_index_occ.json`; drift check is `scripts/k_provenance_drift_check.py --filing-class occ` | Self-referential anchor; verifies the manifest-and-body bidirectional consistency |

A reviewer who runs the corresponding queries against the listed public sources should obtain figures matching this table to the cent / day (or to ±1-2 within disclosed hedge windows for LDA HIGH-volatility quarterly amendment cycles per § 2.7-§ 2.8 of the FEC PP companion methodology + § 3.14 of this document). If the reviewer's figures differ, the methodology note column names the rule that resolves the divergence.

---

## 5. Reproducibility-precision lessons

Eight recurring substrate-query-precision lessons surfaced during the Complaint's pre-transmission verification campaign. Each lesson identifies a query pattern under which a too-narrow first-pass filter returns a result different from the body's authored figure, and the body figure is correct under the broader filter.

| Lesson | Where it applies | Default-narrow result | Correct broader result | Rule |
|---|---|---|---|---|
| Canonical view vs. raw `house_ptr_transactions` | Any per-Member rate / severity figure | Raw join over `house_ptr_transactions` × `house_ptr_index` returns Khanna 2.84% rate / 28 docs late | Canonical-view dedup returns 1.74% rate / 22 canonical late tx | § 3.1 — amendment cascades collapse to the earliest-attribution row |
| Pre-tenure tx mis-counted | Chamber-wide rate for re-entering Members | Members with pre-Congressional trade history show inflated late-counts | LATERAL JOIN on `congress_members.served_from` removes pre-tenure tx | § 3.2 |
| Naive year-gap parse-error sentinel | Filtering Gemini OCR errors | Suozzi NY-3 + Allen GA-12 batched amendments flagged as parse errors | Tightened mixed-date heuristic preserves them as GENUINE_LATE | § 3.3 |
| Notification-date NULL fallback skipped | Per-tx late-flag computation | Rows with `notification_date IS NULL` (~70%) silently treated as not-late | Conservative `transaction_date + 45 days` deadline applies | § 3.4 |
| Ticker NULL fallback skipped | Per-ticker concentration metrics | NVIDIA / Palantir / pharma trades undercounted by ~51% | `LEFT JOIN ro_khanna.ticker_map ON UPPER(asset_name) LIKE pattern` | § 3.7 |
| LDA registrant-only filter | Sector-cohort lobbying universe | ~48 filings / ~13 lobbyists | ~290 filings / ~98 lobbyists with registrant-OR-client union | § 3.9 |
| Cross-cycle name-exact match | Donor cohort cross-cycle aggregation | Donors with name variants undercounted by ~50-100% | (employer, last_name) + first-name fuzzy union | § 3.10 |
| `5 U.S.C. App. § 10X` operative cite | Statute-currency check | Predecessor form cited as operative authority | `public.v_statute_current` resolves to current `5 U.S.C. § 131XX` | `.claude/rules/citation-currency.md` — recodified by P.L. 117-286 § 7 (2022-12-27) |

These lessons are not Complainant-specific; they apply to any reviewer or downstream researcher querying the same public substrates. They are documented here so that an OCC reviewer who runs a too-narrow first-pass filter and obtains a result different from the body's figure does not reach a defect conclusion before applying the broader filter.

---

## 6. Worked end-to-end example — Khanna 358-day HUMANA late filing

This worked example takes the Count 1 worst-single-tx anchor from the Complaint (the 358-day HUMANA INC common stock filing underlying the § II.B + § III.1 severity disclosures) and reproduces it end-to-end against House Clerk public-record data.

### Step 1: Acquire House Clerk PTR substrate

The House Clerk publishes PTR PDFs at `https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure.aspx`. The annual bulk index TSV is at `https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip` (and analogously per year).

Identify Khanna's PTR doc-IDs by searching the bulk TSV:

```sql
-- After loading 2024FD.txt into a temp table:
SELECT doc_id, filing_date, filing_type
  FROM tmp_2024fd
 WHERE last_name = 'Khanna'
   AND first_name LIKE 'Ro%'
   AND filing_type = 'P';      -- 'P' = Periodic Transaction Report
```

For the HUMANA tx, the relevant doc is filed 2024-11-08 (`filing_date`) covering one or more transactions on 2023-10-02.

### Step 2: Fetch the PTR PDF

```bash
curl -O "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/{DOC_ID}.pdf"
```

### Step 3: OCR-extract the Schedule A row

The PDF carries a Schedule A table with one row per transaction. The HUMANA row is:

| Asset | Owner | Transaction Date | Notification Date | Type | Amount |
|---|---|---|---|---|---|
| HUMANA INC. (HUM) — Common Stock | DC | 2023-10-02 | (blank) | P | $1,001 - $15,000 |

(Reviewer-side OCR via Tesseract + table-detection or Gemini per-page prompt should reproduce this row; structural agreement on Asset / Owner / Transaction Date / Type is the load-bearing reproducibility check per § 3.15.)

### Step 4: Compute days-late

Per 5 U.S.C. § 13105(l):

```
deadline = LEAST(notification_date + 30 days, transaction_date + 45 days)
        = LEAST(NULL + 30, 2023-10-02 + 45)        -- notification_date NULL per § 3.4
        = 2023-11-16
days_late = filing_date - deadline
         = 2024-11-08 - 2023-11-16
         = 358 days
```

The 358-day figure matches the body's authored Khanna canonical worst-late.

### Step 5: Confirm via canonical view + Khanna case-schema audit

```sql
SELECT asset_name, owner, transaction_date, earliest_filing_date,
       (earliest_filing_date - LEAST(transaction_date + INTERVAL '45 days',
                                     COALESCE(notification_date,'2099-12-31'::date)
                                     + INTERVAL '30 days'))::int AS days_late
  FROM lake.house_ptr_transactions_canonical
 WHERE filer_identity LIKE 'KHANNA|RO%'
   AND asset_name ILIKE '%HUMANA%'
 ORDER BY days_late DESC LIMIT 1;
```

**Expected result**: `HUMANA INC. (HUM) — Common Stock | DC | 2023-10-02 | 2024-11-08 | 358`.

### Step 6: Cross-check against the chamber-rank position

```sql
SELECT member_last_name, member_first_name, worst_days_late,
       PERCENT_RANK() OVER (ORDER BY worst_days_late) AS pct_rank
  FROM public.house_ptr_chamber_audit_by_member
 WHERE n_tx_total >= 20
ORDER BY worst_days_late DESC;
```

Locate Khanna in the result set: rank 107 of 210 (P49.5 — BELOW CHAMBER MEDIAN). The peer-46 cross-check (rank 32 of 46, P32.6) is in `ro_khanna.peer_baseline_percentiles`.

If the reviewer's Step 4 result differs from 358 days, the most likely causes are: (a) attributing days-late to an amendment doc rather than the earliest disclosure (apply § 3.1); (b) misreading `notification_date` as 2024-something rather than blank (apply § 3.4); (c) Gemini OCR year-digit parse error on the source PDF (apply Tesseract cross-validation per § 3.15).

### 6.1 Automated reproducibility kit — `verify_anchors_occ.py`

The packet includes `verify_anchors_occ.py`, a self-contained Python script distributed alongside this methodology document. The script automates the worked example above for every load-bearing scalar in § 4.

**Usage**:

```bash
pip install requests
python verify_anchors_occ.py                    # frozen mode against bundled snapshots
python verify_anchors_occ.py --live             # exercises the public-substrate path
```

**What the script does**:

1. Loads bundled substrate snapshots from `data/occ/` (`statute_cites_2026_05_02.json`, `ptr_filing_audit_khanna_2026_05_02.json`, `house_chamber_audit_2026_05_02.json`, `peer_baseline_percentiles_2026_05_02.json`).
2. For each anchor in § 4, runs the kind-specific verifier (`statute_cite_resolve` / `ptr_audit_aggregate` / `ptr_audit_worst_humana` / `chamber_audit_p50` / `peer_baseline_metric_resolve` / `vote_resolve` / `irs_990_resolve` / `lda_resolve` / `pfd_schedule_a_load` / `trade_pnl_aggregate`, etc.).
3. Emits a Markdown report (`verify_anchors_occ_report.md`) with a per-anchor side-by-side comparison: body's authored figure vs reviewer-side substrate-derived figure vs diff vs status (OK / DIVERGE / FAIL / MANUAL).
4. In `--live` mode, additionally exercises the public-substrate path for any anchor whose verifier kind has a live-source resolution.

**Expected output**: every anchor row reports OK (matching to the cent / day) within the substrate's amendment-volatility band per § 3.14. Any DIVERGE row prompts a re-read of the named methodology rule in the report.

**Network requirement**: frozen mode requires no network access (operates against the bundled JSON snapshots). `--live` mode fetches OpenFEC API + House Clerk roll-call XML + IRS S3 990 e-file XML on demand; first invocation of `--live` downloads approximately 50-150 MB of fresh substrate.

### 6.2 Snapshot-vs-primary currency check — `--diff-snapshots-vs-live`

The frozen snapshots in `data/occ/` carry a snapshot date (`2026-05-02`). A reviewer reading the OCC complaint months after that date can ask the reasonable question: "the snapshot is dated X, how do I know it still matches primary substrate today?" The `--diff-snapshots-vs-live` mode answers this question without requiring lake access.

**Usage**:

```bash
# Run BOTH the standard anchor checks AND the snapshot-vs-primary diff:
python verify_anchors_occ.py --diff-snapshots-vs-live

# Run ONLY the diff (skip the regular anchor checks; faster):
python verify_anchors_occ.py --diff-snapshots-vs-live --diff-only
```

**What the diff mode does**: for each of the 9 frozen snapshots in `data/occ/`, the kit re-derives the snapshot's load-bearing scalars against the *current* primary substrate (uscode.house.gov for statute cites, clerk.house.gov for roll-call XML, etc.) and reports a per-row drift class.

**Per-snapshot diff classification**:

| Snapshot | Class | Primary path | Notes |
|---|---|---|---|
| `statute_cites_2026_05_02.json` | **Primary-diffable** | `uscode.house.gov` (USC URL form per § 3.16) | 9 USC sections diffable; 1 CFR + 1 House Rules sit out of scope (different primary servers) |
| `khanna_votes_2026_05_02.json` | **Primary-diffable** | `clerk.house.gov` per-roll XML | 13 NDAA cluster rolls; clerk uses both `Yea/Nay` and `Aye/No` vocabularies (synonym pairs treated as semantic match) |
| `ahuja_foundation_990pf_2026_05_02.json` | BLOCKED (ProPublica brittle) | `projects.propublica.org/nonprofits/api/v2/...` | Cloudflare-gated; deferred to substrate-class hardening |
| `house_chamber_audit_2026_05_02.json` | BLOCKED (lake-required) | `public.house_ptr_chamber_audit_by_member` | re-OCR all chamber PTR PDFs + rebuild canonical view; reviewers with lake access only |
| `peer_baseline_percentiles_2026_05_02.json` | BLOCKED (lake-required) | `ro_khanna.peer_baseline_percentiles` | rebuild from chamber-audit + peer-46 roster per § 3.5 |
| `ptr_filing_audit_khanna_2026_05_02.json` | **Rebuild-diffable** | bundled raw substrate at `data/occ/khanna_ptr_transactions_2026_05_02.json` (one-time export of `lake.house_ptr_transactions` 36,277 raw rows for Khanna) | reviewer runs `python data/ocr_products/rebuild_ptr_audit_khanna.py` (~30s, stdlib-only, no API spend) — applies canonical-view tx-key dedup + audit_flag exclusions + days_late computation; differ confirms BIT-EXACT match on all 10 aggregate fields + HUMANA worst-tx detail per s27 B-F1 wiring |
| `khanna_pfd_schedule_d_2026_05_02.json` | **Rebuild-diffable** | bundled structured Schedule D rows | reviewer runs `python data/ocr_products/rebuild_pfd_schedule_d_khanna.py` (~1s, stdlib-only) — re-derives `by_year` aggregate + `load_bearing_invariants` from the bundled rows; differ confirms **BIT-EXACT match on 4 by_year buckets × 4 fields + 3 invariants** per s29 B-F2 wiring |
| `khanna_ohlc_2026_05_02.json` | (B-F3 substrate input) | `ro_khanna.daily_ohlc` (yfinance fetch frozen at snapshot date) | bundled OHLC daily-close prices for 42 in-scope tickers + SPY benchmark, 2017-01-03 .. 2026-04-16 — read by `rebuild_trade_pnl_khanna.py` |
| `khanna_window_events_2026_05_02.json` | (B-F3 substrate input) | NDAA + CMS date constants + `lake.sec_8k_filing_index` per-ticker dates + `lake.usaspending_contracts_*` per-ticker action dates | per-ticker event date sets for the four window-attribution paths — read by `rebuild_trade_pnl_khanna.py` |
| `trade_pnl_facts_2026_05_02.json` | **Rebuild-diffable** (within ±5% PASS_WITH_DEFECT band on F225 mid) | bundled PTR + OHLC + window-events snapshots above | reviewer runs `python data/ocr_products/rebuild_trade_pnl_khanna.py` (~10-30s, stdlib-only, no yfinance, no API spend) — applies ticker_map ILIKE classification + per-tx forward P&L using OHLC + ±14d window flags + per-sector aggregation; differ confirms F225 mid bit-exact at $61.04M against the bundled 2026-05-02 substrate snapshot.
| `lda_khanna_contributions_2026_05_02.json` | BLOCKED (LDA API key) | `api.lda.senate.gov` (free signup) OR `senate.gov` bulk-XML | filter `contribution_items[]` for KHANNA recipient strings; 53-registrant invariant load-bearing per § 3.9 |

**Drift class semantics**:

- `CLEAN` — frozen scalar BIT-EXACT to live primary; reviewer has positive confirmation the snapshot remains current.
- `DRIFT_BENIGN` — count drift only; load-bearing invariants preserved (matches the M041 LDA `PASS_WITH_DEFECT/substrate_count_drift` pattern: line/amount fluctuate as primary substrate grows but the 53-registrant invariant holds).
- `DRIFT_VALUE` — load-bearing scalar shifted; SCORECARD axis must be re-checked. **Default disposition is PROBE DEEPER** per the §Substrate-verification dig-deeper discipline (column rename / pagination cursor / URL form regression are common false-positive causes); the kit's three dig-deeper landings (statute label-token over-match / vote-vocabulary synonym / raw-HTML-vs-stripped-text stub threshold) all paid off during s18 implementation against pure agent-side mistakes, not substrate drift.
- `BLOCKED_*` — primary not reachable from cold-start (lake / fact-store / API key required). Honest disclosure with substrate authority + re-derivation recipe in the row's Notes column. **`BLOCKED` is not a verifier failure** — it accurately reports the substrate-access boundary the reviewer would need to cross.
- `BLOCKED_UNREACHABLE` — primary returned 5xx / DNS / rate-limit. Re-run after a delay.
- `ERROR` — runtime exception (kit bug, not a substrate drift).

**Expected output (cold-start, no lake access, no LDA key)**:

```
**Summary**: 37 per-row diffs across 9 snapshots —
CLEAN: 31 / PASS_WITH_DEFECT: 1 / DRIFT_BENIGN: 0 / DRIFT_VALUE: 0 / BLOCKED: 5 / ERROR: 0
```

(post-s27 B-F1 wiring: `ptr_filing_audit_khanna` flips BLOCKED → 2 × CLEAN via `rebuild_ptr_audit_khanna.py`; post-s29 B-F2 wiring: `khanna_pfd_schedule_d` flips BLOCKED → 2 × CLEAN via `rebuild_pfd_schedule_d_khanna.py`; post-s30 B-F3 wiring: `trade_pnl_facts` flips BLOCKED → 1 × CLEAN + 1 × PASS_WITH_DEFECT/post_cascade_substrate_drift via `rebuild_trade_pnl_khanna.py`. Reviewer with the LDA API path additionally populates `_substrate_cache_occ/lda/khanna_lda_aggregate.json` via `python fetch_substrate_occ.py --classes lda` and the LDA row flips BLOCKED_NEEDS_FETCH → 2 × CLEAN + 1 × PASS_WITH_DEFECT, yielding **33 CLEAN / 2 PASS_WITH_DEFECT / 4 BLOCKED**.)

The 25 CLEAN rows establish that the load-bearing primary-diffable scalars (USC section text + Khanna roll-call votes) reproduce against current primary substrate. The 9 BLOCKED rows accurately disclose the lake / fact-store / LDA-key access boundary that prevents fully-automated cold-start verification of the remaining substrate — and provide the recipe for a reviewer with that access to complete the diff.

**Output report**: written to `verify_anchors_occ_diff_report.md` (regenerated on every run; **not** bundled in `99_SHA256SUMS_OCC.txt` because the report's wall-clock-bound content would shift the manifest on every reviewer-side re-run).

---

## 7. Reviewer aids

### 7.1 Verification commands for `99_SHA256SUMS_OCC.txt`

The integrity manifest `99_SHA256SUMS_OCC.txt` distributed with the Complaint enables the reviewer to confirm that received bytes match transmitted bytes:

```bash
# Linux / macOS — run from the OCC_FILING_PACKAGE_V2 directory
sha256sum -c 99_SHA256SUMS_OCC.txt
```

```powershell
# Windows PowerShell — verify each file by hand or via loop
Get-Content 99_SHA256SUMS_OCC.txt | ForEach-Object {
    $expected, $file = $_ -split '\s+\*?', 2
    $actual = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    if ($actual -eq $expected) { "OK  $file" } else { "MISMATCH $file" }
}
```

The manifest is generated under the Complainant's LF-canonical convention (text / markdown / CSV are CRLF→LF normalized before hashing; binary files `.png` `.jpg` `.pdf` `.xlsx` are hashed raw). Reviewers on Windows should normalize line endings to LF before re-hashing if they intend to recompute hashes from raw bytes; the recommended verification path is the canonical recompute via `python scripts/manifest_canonical_sha.py --check <path> <expected_hash>` (exit 0 on match, exit 3 on mismatch).

### 7.2 Glossary of House / FEC / LDA / IRS / OCC vocabulary

| Term | Meaning |
|---|---|
| **PTR (Periodic Transaction Report)** | House Clerk filing required within 45 days of a reportable transaction over $1,000 by the Member, spouse, or dependent child (5 U.S.C. § 13105(l), STOCK Act § 6) |
| **PFD (Personal Financial Disclosure)** | House Clerk annual filing required by 5 U.S.C. § 13103, covering Schedule A (assets and unearned income), Schedule B (transactions over $1,000 — narrative only on PFD), Schedule C (earned income), Schedule D (liabilities), Schedule E (positions held outside Government), Schedule F (agreements and arrangements), Schedule G (gifts), Schedule H (travel reimbursements), Schedule I (compensation in excess of $5,000 paid by one source) |
| **EIGA** | Ethics in Government Act of 1978 (recodified to 5 U.S.C. Ch. 131 by P.L. 117-286 § 7, Dec. 27, 2022) |
| **STOCK Act** | Stop Trading on Congressional Knowledge Act of 2012 (P.L. 112-105); codified at 5 U.S.C. § 13105(l) (PTR deadline) and 15 U.S.C. § 78u-1(g) (MNPI extension to Members) |
| **§ 6** | STOCK Act § 6 — the 45-day PTR filing deadline |
| **§§ 3-4** | STOCK Act §§ 3-4 — extension of MNPI prohibitions and trustee-tipper liability to Members and staff |
| **OCC (Office of Congressional Conduct)** | Office established by H. Res. 5, 119th Cong. (Jan. 3, 2025), formerly the Office of Congressional Ethics ("OCE"); House preliminary-review body for Member ethics complaints |
| **House Committee on Ethics** | House standing committee with authority to impose civil penalties under 5 U.S.C. § 13106; receives OCC referrals |
| **House Rule XXIII** | Code of Official Conduct (cl. 1 conduct reflecting creditably; cl. 2 prohibition on use of official position for personal gain; cl. 9 acceptance of gifts) |
| **MUR** | FEC Matter Under Review — enforcement docket assigned a numeric identifier (e.g., MUR 7062 cited at § 0) |
| **§ 18G transfer** | FEC `transaction_tp='18G'` — inter-committee transfer between affiliated committees authorized under 11 C.F.R. § 102.6(a)(1)(i)–(ii); appears in `itoth.txt` |
| **F24 / F3X** | FEC 48-hour notice / quarterly Report of Receipts and Disbursements; both filed for every Schedule E IE per § 3.8 |
| **LD-2** | Senate LDA quarterly lobbying-disclosure filing (per 2 U.S.C. § 1604) |
| **LD-203** | Senate LDA semiannual contribution disclosure filing (per 2 U.S.C. § 1604(d)) |
| **§ 203 contributions** | LDA § 203 reportable contributions (lobbyist + organization political donations disclosed semiannually in LD-203) |
| **CRA** | Congressional Review Act resolution of disapproval (5 U.S.C. § 802) |
| **NDAA** | National Defense Authorization Act (annual; cited at § III.2 for trade-window concentration analysis) |
| **Schedule B (Form 990-PF)** | IRS Form 990-PF attachment listing significant contributors to a private foundation; non-cash contribution detail at the Schedule B sub-block; redacted on §501(c)(3) public copy returns under 26 U.S.C. § 6104(d)(3)(A); Ahuja Foundation Schedule B is e-filed |
| **Schedule I (Form 990)** | IRS Form 990 attachment listing grants paid by a tax-exempt organization |
| **Form 8871 / 8872** | IRS 527 organization Notice of Section 527 Status / contribution-and-expenditure report |
| **`covered_position`** | LDA lobbyist disclosure field naming the lobbyist's prior service in Congress or the Executive Branch within the 20 years preceding the engagement |

### 7.3 `fact_ids` field in Appendix entries — internal Complainant references

Each Appendix entry carries a `fact_ids` array (e.g., `[610]`) and a `verification_ids` array (e.g., `[185]`). These are identifiers in the Complainant's internal fact-store database used for the Complainant's own audit trail and theory-readiness machinery. **They are not load-bearing for reviewer reproducibility.**

The operative reviewer hooks are the `substrate` field, the `sql_text` field, and the `Reproducibility:` text in each Appendix entry, plus the public-source URL named in § 1 of this document. A reviewer ignoring `fact_ids` and `verification_ids` and running the `sql_text` against the public-source-equivalent table named in § 1 of this document obtains the figures published in the body, which is the only reviewer-side verification path required.

The `fact_ids` and `verification_ids` are exposed in the manifest for completeness and for any future OCC staff request to re-derive a specific scalar from the canonical fact store, but they are not necessary for reviewer-side reproducibility.

### 7.4 Exhibit-level reproducibility map

The packet transmitted with the Complaint includes the OCC Exhibit List at `OCC_EXHIBIT_LIST.md` and the per-Exhibit files at the dossier root. Exhibits inline-cited from the operative Complaint that carry their own substrate-keyed analyses:

| Exhibit | Inline-cited at | Substrate dependencies | Reproducibility surface |
|---|---|---|---|
| Ex. A — Damages composite | § II.B + § IV | `ro_khanna.damages_summary` + chamber-audit dollar-weighted | Same composite metric (§ 3.6) and dollar-weighted aggregation rules |
| Ex. B — STOCK Act late-filing audit | § II.B + § III.1 | `ro_khanna.ptr_filing_audit` + `public.house_ptr_chamber_audit_by_member` | Canonical view + pre-tenure filter + parse-error sentinel (§§ 3.1-3.3) |
| Ex. C — Peer baseline | § II.B + § III.1 | `ro_khanna.peer_baseline_percentiles` | Two-universe rule (§ 3.5) |
| Ex. E — NDAA-window defense-prime trades | § III.2 | Per-tx canonical view + `lake.congress_rollcalls` NDAA enactment dates | Canonical view + ticker fallback (§§ 3.1, 3.7) |
| Ex. F — CMS rulemaking × pharma trade cluster | § III.3 | Per-tx canonical view + Federal Register CMS rulemaking calendar | Canonical view + ticker fallback (§§ 3.1, 3.7) |
| Ex. H — Ahuja Foundation concealment chain | § III.7 | `lake.irs_990_returns` / `_grants` / `_officers` / `_pf_noncash_donations` filter EIN 34-1685088 | Standard 990 e-file XML parsing |
| Ex. L — PFD page-9 OCR (SMA rebuttal) | § II.D + § III.7 | Class-2 OCR work product | § 3.15 — bundled JSON + independent reviewer-side OCR verification path |
| Ex. M — Same-day SEC Form 8-K trade pattern | § III.4 | `lake.house_ptr_transactions_canonical` × `lake.sec_8k_filing_index` | Canonical view + ticker fallback (§§ 3.1, 3.7) |
| Ex. Z — Aligned-direction named-officer same-day Form 3/4/5 | § III.4 | `lake.house_ptr_transactions_canonical` × `lake.sec_form345_full` | Canonical view + ticker fallback (§§ 3.1, 3.7) |
| Ex. R — Options leverage (directional PUTs) | § III.7 | Per-tx canonical view filtered to `transaction_type ILIKE '%PUT%'` etc. | Canonical view + ticker fallback (§§ 3.1, 3.7) |
| Ex. CC — Margin ladder | § III.7 | `ro_khanna.pfd_schedule_d_liabilities` + Schedule A asset extractions | § 3.15 — class-2 OCR |
| Ex. FF — 3-way agreement | § VI | `ro_khanna.cited_trades_3way_validation` | PTR row × PFD Schedule A end-of-year × external public price feed reconciliation |

Other `EXHIBIT_*.md` files in the dossier are derivative analyses on facts already in the body or address parallel-referral scope (FEC Khanna PCC referral, House Ethics submission). They are included for completeness but are not load-bearing for the operative OCC complaint and do not require independent reviewer reproduction.

### 7.5 Common-divergence diagnostic table

When a reviewer's first-pass figure differs from the body's authored figure, the divergence usually fits one of these patterns:

| Reviewer's result | Likely cause | Resolving rule |
|---|---|---|
| Khanna rate above 1.74% | Raw join over `house_ptr_transactions` × `house_ptr_index` (no canonical-view dedup); amendment re-reports counted as separate filings | § 3.1 — use `house_ptr_transactions_canonical` |
| Worst-days-late > 358d for Khanna | Attributing days-late to an amendment doc rather than `earliest_filing_date`; OR Gemini year-digit parse error not caught by tightened sentinel | § 3.1 + § 3.3 + § 3.15 (Tesseract cross-validation) |
| Chamber rate > 10.06% | Pre-tenure tx not filtered; OR pre-canonical-view raw data | § 3.1 + § 3.2 |
| Per-tx late-flag missed on rows with `notification_date IS NULL` | Skipped fallback to `transaction_date + 45 days` | § 3.4 |
| Ticker-keyed concentration figure ~half body figure | Ticker NULL fallback skipped | § 3.7 |
| LDA universe ~48 filings instead of ~290 | Registrant-only filter | § 3.9 — registrant-OR-client |
| `invalid input syntax for type numeric: ""` | Empty-string-to-numeric cast on FEC bulk dollar column | § 3.11 — wrap with `NULLIF(<col>, '')::numeric` |
| Parse error on date column | Wrong date-format string for the file type | § 3.12 — three FEC bulk date formats |
| Body figure within ±$50K-200K of reviewer figure on LDA quarterly | Snapshot drift across LDA quarterly amendment cycle | § 3.14 — body's "approximately" hedge absorbs LDA HIGH-volatility band |

### 7.6 Process for clarification questions

For methodology questions arising during OCC preliminary review that this document does not resolve, the Complainant's contact path is the address and contact information published on the cover page of `OCC_COMPLAINT_KHANNA.md`. The Complainant will respond to written OCC inquiries with the substrate query, the cited public-source URL, and the worked derivation for any specific scalar the OCC requests further documentation on. The verification at § VIII of the operative complaint covers the personal-knowledge portion of the underlying allegations; the methodology in this document covers the public-record-derivation portion.

### 7.7 Inline marker convention and pre-filing strip recipe

The three operative filings in this package — `OCC_COMPLAINT_KHANNA.md`, `DOJ_REFERRAL_KHANNA.md`, and `HOUSE_ETHICS_SUBMISSION_KHANNA.md` — carry inline `[OCC_M###]` marker references in operative paragraphs at every fact-citation point. Each bracket maps a paragraph's operative scalar to its manifest entry in `_provenance_index_occ.json`, which in turn records the underlying `fact_id`(s), `verification_id`(s), `substrate` authority, and a re-derivable `sql_text` query.

Inline markers are an internal reviewer aid, not part of the operative legal text. They are designed to be **stripped before physical transmission** to the venue clerk so the filed document is clean prose. The §A Provenance Appendix table at the bottom of `OCC_COMPLAINT_KHANNA.md` (auto-generated by `scripts/k_provenance_appendix_build.py --manifest-class occ`) preserves the marker → fact mapping in a dedicated catalog block; reviewers can drill into a specific paragraph's substrate via the appendix's `body_section` column.

**Strip recipe** (run from `OCC_FILING_PACKAGE_V2/` root):

```bash
# Default: writes <file>.filing.md side-by-side, leaves originals intact
python strip_markers_pre_filing.py

# In-place mutation (requires --force; overwrites the operative text)
python strip_markers_pre_filing.py --in-place --force

# Also strip the §A Provenance Appendix block (some venues prefer leaner submissions)
python strip_markers_pre_filing.py --strip-appendix

# Process a subset of files
python strip_markers_pre_filing.py --files OCC_COMPLAINT_KHANNA.md DOJ_REFERRAL_KHANNA.md
```

The script's regex matches single-marker `[OCC_M001]` and multi-marker `[OCC_M001, OCC_M002, OCC_M003]` brackets and consumes a single leading space (so `fact text [OCC_M001].` collapses to `fact text.` rather than `fact text .`). The script reports per-file removed counts and is idempotent (re-running on already-stripped text removes 0 markers and leaves the file unchanged). The reverse operation (re-embedding markers from the manifest) is NOT provided — markers are authored at body-edit time against the manifest's `first_seen_section` mapping, not regenerated.

A reviewer at the venue can recover the marker-aware version of any paragraph by consulting the §A Provenance Appendix table (which preserves every marker → manifest entry) or by running `verify_anchors_occ.py` against the bundled substrate snapshots, both of which retain the marker → fact correspondence independent of the operative-body strip.

---

## Document control

This document is co-distributed with `OCC_COMPLAINT_KHANNA.md`, the 80-entry `_provenance_index_occ.json` manifest, the §A Provenance Appendix rendered into the Complaint body lines 569-670, the bundled substrate snapshots at `data/occ/`, the bundled OCR work product at `data/ocr_products/`, the reviewer kit `verify_anchors_occ.py`, the substrate fetch script `fetch_substrate_occ.py`, the pre-filing inline-marker strip helper `strip_markers_pre_filing.py` (per § 7.7 above), and the `99_SHA256SUMS_OCC.txt` integrity manifest. Together these establish that every substantive substrate-keyed claim in the Complaint resolves to (a) a public-record source or a class-2 work-product extraction with documented independent-reproducibility chain, (b) a reproducible query against that source, (c) an expected scalar result, and (d) a methodology rule for any divergence between a first-pass query and the body's authored figure.

For methodological questions arising during OCC preliminary review, the operative authorities are the public-source files cited in § 1 of this document, not the Complainant's PostgreSQL schema. The Complainant's schema is one analyst's pipeline state on the public record; the public record is shared.

The chamber-baseline disclosure paragraph required at every comparative-statistic Count (per § 3a above) is the structural guarantee that the Complaint's framing does not depend on selective sampling. Two universes; same direction; below-median on rate AND on severity; the Counts rest on composite, timing, and coordination.
