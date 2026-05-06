# Exhibit CC — Goldman Margin Ladder and Paired-Trust Label Scaffold

**Case**: *In re Representative Rohit "Ro" Khanna (CA-17)*
**Counts supported**: Count 1 (STOCK Act § 6 severity context); Count 3 (financial-interest conflicts — conflict triangle); Count 6 (§ 13104(f)(3) SMA/QBT/EIF defense foreclosure)
**Subject entities**: Goldman Sachs & Co.; Ritu Ahuja 1994 Trust; Ritu Ahuja 1995 Trust

---

## 1. Purpose

Across tax years 2017 through 2019, respondent's Annual Personal Financial Disclosures — visually verified against the primary-doc PDFs filed with the House Clerk — show a continuous margin-loan scaffold on the spouse-owned (SP) investment account. Two facts about that scaffold dispose of the passive-account affirmative defense:

1. A brokerage margin loan is itself a reportable liability under 5 U.S.C. § 13104(a)(4); its disclosure, year after year, acknowledges that the account against which it is collateralized is **not** a broker-discretionary arrangement insulated from Member control.
2. Customer-protection rules promulgated under Regulation T and FINRA Rule 4210 prohibit a broker-dealer from writing uncovered options or carrying short-put exposure on an account unless the account holder affirmatively authorizes the options level. That authorization — executed by the Member or the Member's spouse, not by a discretionary trustee — independently forecloses the qualified-blind-trust, exempt-investment-fund, and separately-managed-account defenses under 5 U.S.C. § 13104(f)(3).

The scaffold carries a structurally distinctive paired-label feature on the form itself across all three years TY2017 through TY2019: each Goldman Sachs Margin line is preceded in the Schedule D creditor column by a label naming a spouse-affiliated family trust — the **Ritu Ahuja 1994 Trust** above the early-year Goldman Margin line, and the **Ritu Ahuja 1995 Trust** above the later-year Goldman Margin line. The trust-label rows are SP-owned, carry the trust's name in the creditor column only, and leave the date / type / amount-band columns blank. Neither trust is registered in Delaware or Nevada Secretary of State corporate records; neither is registered with the Securities and Exchange Commission.

---

## 2. The four-year Schedule D ladder (TY2017–TY2020)

Each row below reflects the Schedule D liabilities section of the Member's Annual PFD filed with the U.S. House Clerk, visually verified against the primary-doc PDF:

| Tax year | Doc ID | Schedule D structure (top-to-bottom on the form) | Aggregate Goldman margin band | Notes |
|---|---|---|---|---|
| TY2017 | 9113638 | (NONE) Nelnet 4/03 Student Loan; (SP) **Ritu Ahuja 1994 Trust** label (empty); (SP) Goldman Sachs 2/17 Margin $250,001–$500,000; (SP) **Ritu Ahuja 1995 Trust** label (empty); (SP) Goldman Sachs 6/17 Margin $500,001–$1,000,000 | $750K – $1.5M | Two concurrent Goldman Margin lines, each preceded by a paired trust-label row |
| TY2018 | 9115242 | (NONE) Nelnet 4/03 Student Loan; (SP) **Ritu Ahuja 1994 Trust** label (empty); (SP) Goldman Sachs 4/18 Margin $500,001–$1,000,000; (SP) **Ritu Ahuja 1995 Trust** label (empty); (SP) Goldman Sachs 1/18 Margin $100,001–$250,000 | $600K – $1.25M | Same paired-label structure as TY2017 |
| TY2019 | 8217503 | (NONE) Nelnet 4/03 Student Loan; (SP) **Ritu Ahuja 1994 Trust** label (empty); (SP) Goldman Sachs 1/19 Margin $500,001–$1,000,000; (SP) **Ritu Ahuja 1995 Trust** label (empty); (SP) Goldman Sachs 4/19 Margin $15,001–$50,000 | $515K – $1.05M | Same paired-label structure as TY2017 / TY2018 |
| TY2020 | 8218200 | (SP) Nelnet Student Loan $10,001–$15,000 — no Goldman entries, no trust labels | $0 | Margin scaffold and paired-label structure both end between TY2019 and TY2020 |

All Schedule D margin rows on the TY2017–TY2019 forms are owner-coded SP (spouse Ritu Ahuja Khanna). The trust-label rows are also owner-coded SP. The Goldman Margin lines all carry a date in MM/YY form in the date-incurred column; the trust-label rows carry no date.

The Schedule D records are lake-resident via `lake.house_pfd_schedule_d_liabilities` keyed on member_last_name = "Khanna".

---

## 3. The paired-trust label structure on the form

The paired-label structure is itself probative even though the trust-label rows leave the date / type / amount-band columns blank. Three structural facts make the finding worth surfacing:

1. **The labels disclose named-account titles for each Goldman sub-account.** The Ritu Ahuja 1994 Trust and Ritu Ahuja 1995 Trust appear in Schedule D's creditor column immediately above the corresponding Goldman Sachs Margin lines for three consecutive tax years. The structurally cleanest reading is that each Goldman margin sub-account is held under one of the two named-trust titles, with Goldman Sachs as the actual lender; the trust labels disclose the account-title identifier on the form. The same paired structure is reproduced in TY2017, TY2018, and TY2019 — six trust-label rows in total — which makes the label discipline part of the household's reporting practice across the entire pre-2020 margin period.
2. **Neither trust holds itself out as an independently registered entity.** Delaware and Nevada Secretary of State corporate records return zero hits for "Ritu Ahuja 1994 Trust" or "Ritu Ahuja 1995 Trust"; SEC EDGAR returns zero registrant hits for either. The entities operate as named family trusts, not as registered investment companies or registered fund vehicles.
3. **Both trusts also appear on Schedule A as asset-holding vehicles.** The Ritu Ahuja 1994 Trust and Ritu Ahuja 1995 Trust are listed as asset wrappers in multiple years of the same filing series (including the 2024 Annual PFD catalogued in Exhibit L). The same trusts therefore carry both an asset-holding posture on Schedule A and a named-account-title posture on Schedule D's margin-loan scaffold, against accounts on which the household separately authorized the systematic short-volatility options program documented at Exhibit JJ.

---

## 4. Goldman Sachs as dual principal

The Goldman Sachs relationship is not solely a creditor relationship. Independent FEC individual-contribution records identify Goldman Sachs employees and affiliates as itemized donors to respondent's principal committees, with approximately $48,000 in aggregate individual contributions from Goldman-affiliated donors across respondent's House tenure cycles. The same counterparty is therefore simultaneously (a) the household's margin lender, (b) the counterparty to the household's active options writing (see Exhibit JJ), and (c) a material individual-contribution donor cluster to the principal committee. Whether any of those roles, in isolation, would trigger House Rule XXIII concerns is an interpretive question for the Committee on Ethics; what the present exhibit documents is the structural convergence.

---

## 5. Why this forecloses the passive-account defense

The affirmative defenses most commonly raised in STOCK Act § 6 late-filing inquiries — the separately-managed-account (SMA) defense, the qualified-blind-trust (QBT) defense, and the exempt-investment-fund (EIF) defense — each turn on a factual premise that a third-party fiduciary makes trading decisions without the Member's or the Member's spouse's participation.

That premise fails against the margin-ladder record for at least three independent reasons:

1. **The PFD itself.** The respondent's 2024 Annual PFD (Exhibit L) does not disclose any SMA, any qualified blind trust, or any third-party discretionary custodian for the actively-traded equity portfolio. The 37,238 reportable common-stock transactions cannot originate from an account that is not on the filing.
2. **Margin is an authorization artifact.** Extending margin requires a signed customer agreement and options authorization (Level 2 or Level 3) executed by the account holder. A third-party discretionary manager acting without the spouse's participation could not have opened the Goldman facility, nor authorized the written-PUT activity documented in the companion Exhibit JJ.
3. **Named-trust account titles.** The two spouse-affiliated family trusts whose names appear in the creditor column above each Goldman Sachs Margin line are entities whose composition and beneficiaries are known to the Member's household (the trusts are also asset-holding vehicles disclosed on Schedule A, including in the 2024 Annual PFD). A blind trust by definition does not transact under named-account titles whose identity and composition are known to the Member.

Each of these three grounds is independent of the others. Any one of them, on its own, disposes of the passive-account defense against Counts 1, 2, 3, and 7.

---

## 6. Statutory framing

- **5 U.S.C. § 13104(a)(4)** — disclosure of liabilities exceeding $10,000. The Goldman Sachs Margin lines and the paired Ritu Ahuja 1994 Trust / 1995 Trust account-title labels are properly disclosed; their presence on the filing is, by itself, an acknowledgment that the account is not a blind trust.
- **5 U.S.C. § 13104(f)(3)** — conditions for qualification as a blind trust or an exempt investment fund. Neither the TY2017–TY2019 margin scaffold nor the accompanying options authorization record is compatible with § 13104(f)(3) eligibility.
- **Regulation T** (12 C.F.R. Part 220) and **FINRA Rule 4210** — customer-authorization requirements for margin and options accounts.
- **5 U.S.C. § 13105(l)** — 45-day PTR filing deadline applies without regard to an SMA's notification cadence when no SMA is disclosed on the PFD.

---

## 7. Primary sources

- U.S. House Clerk Financial Disclosure portal — respondent's Annual PFDs TY2017 through TY2020 (docs 9113638, 9115242, 8217503, 8218200; URLs at `disclosures-clerk.house.gov/public_disc/financial-pdfs/`).
- `lake.house_pfd_schedule_d_liabilities` — row-level liability entries for member_last_name = "Khanna" (paired-label and Goldman Margin rows for TY2017–TY2020).
- Federal Election Commission — individual contributions filtered to `employer ILIKE '%goldman%'` against respondent's principal committees.
- Delaware and Nevada Secretary of State online business-entity searches — negative returns for "Ritu Ahuja 1994 Trust" and "Ritu Ahuja 1995 Trust".
- SEC EDGAR full-text search — negative returns for "Ritu Ahuja 1994 Trust" and "Ritu Ahuja 1995 Trust".

---

*End of Exhibit CC.*
