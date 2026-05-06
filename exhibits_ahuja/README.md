# Ahuja Charitable Foundation — Data-Lineage Workpaper for Exhibit H

**Subject.** The Ahuja Charitable Foundation (EIN 34-1685088), a private family foundation whose spouse-trustee and corpus-composition record is developed operatively at Exhibit H and whose grantees-by-lobbying-overlap record is developed at Exhibit Q.

**Scope of this workpaper.** This directory is a methodology workpaper: four CSV data-lineage files and this narrative reference explaining how the Foundation's IRS Form 990-PF records were parsed from primary-source XML to the figures cited in Exhibit H, Exhibit Q, and Count 6 of the operative complaint. It is not itself a pleading. The CSV files are retained in the filing package for transparency so that any reviewer may independently verify every Exhibit H claim against the Foundation's own e-filed 990-PF returns.

**Primary sources.** IRS 990-PF e-filed XML returns for tax years 2013 through 2024, obtained from the IRS Statistics of Income and from the ProPublica Nonprofit Explorer mirror. The four CSVs are the deduplicated roll-ups of the four Schedule-B-and-Investment-schedule query outputs listed below.

---

## CSV 1 — Foundation corpus end-of-year fair-market value by tax year

`E_corpus_by_year.csv` (12 rows covering TY2013 through TY2024).

| Tax year | End-of-year fair market value | End-of-year book value | Managed investment accounts |
|---:|---:|---:|---:|
| 2013 | $9,157,725 | $7,486,898 | 6 |
| 2014 | $11,115,686 | $8,603,430 | 6 |
| 2015 | $11,767,987 | $10,809,648 | 6 |
| 2016 | $12,490,121 | $12,077,636 | 5 |
| 2017 | $14,537,424 | $14,979,270 | 2 |
| 2018 | $16,429,113 | $16,617,404 | 3 |
| 2019 | $19,979,152 | $18,381,702 | 3 |
| 2020 | $23,165,915 | $18,994,054 | 3 |
| 2021 | $38,034,959 | $31,120,487 | 8 |
| 2022 | $32,164,292 | $33,081,241 | 8 |
| 2023 | $38,778,235 | $35,551,282 | 7 |
| **2024** | **$45,102,055** | **$35,621,181** | **9** |

The end-of-year fair-market-value trajectory grows from $9.16 million in tax year 2013 to $45.10 million in tax year 2024 — a roughly 4.9× accretion over eleven years. The largest single-year inflection is from tax year 2020 to tax year 2021 (from $23.17 million to $38.03 million, up 64 percent), coinciding with the pandemic-era technology-sector run. The account-count column measures the number of distinct managed investment accounts disclosed on the Foundation's Schedule of Investments in that year; by tax year 2024 the corpus is held across a primary Goldman Sachs / Fidelity account plus eight Fidelity sub-accounts (including a dedicated covered-calls account and a Diamond Hill sleeve).

## CSV 2 — NVIDIA non-cash contributions to the Foundation by tax year

`F_nvidia_transfers.csv` (the NVIDIA-identified rows of the Schedule B non-cash contributions ledger).

| Tax year | Contributor | Issuer | Shares | Donation-time fair market value |
|---:|---|---|---:|---:|
| 2023 | Monte and Usha Ahuja Family Trust | NVIDIA Corporation | 545 | $804,606 |
| 2023 | Manisha Neil Sethi | NVIDIA Corporation | 68 | $60,616 |
| 2024 | Ritu Ahuja Khanna | NVIDIA Corporation | 2,821 | $386,096 |
| 2024 | Monte and Usha Ahuja Family Trust | NVIDIA Corporation | 7,255 | $1,281,249 |
| **Cumulative TY2023 and TY2024** | — | — | **10,689** | **$2,532,567** |

The tax-year-2024 combined NVIDIA transfer totals **10,076 shares at $1,667,345 donation-time fair-market value**. Ritu Ahuja Khanna's 2,821-share transfer carries a contributor address that matches respondent's Washington, D.C. residence (4432 Chestnut Lane NW) — corroborating her Schedule B contributor status at the spouse-trustee nexus developed in Exhibit H at Section 2(B). The Monte and Usha Ahuja Family Trust's 7,255-share transfer carries the Naples, Florida residence address (81 Seagate Drive, Naples, FL 34103). The fair-market values are at donation-time per IRS Form 990-PF Schedule B reporting convention; subsequent NVIDIA share-price appreciation amplifies the household-to-Foundation wealth flow represented by the transfer.

## CSV 3 — Sector concentration of Foundation non-cash holdings

`G_sector_concentration.csv` (sector-level totals per tax year).

| Tax year | Sector | Total donation-time fair market value | Share of year's non-cash receipts |
|---:|---|---:|---:|
| 2024 | Financial (Goldman Sachs) | $2,317,615 | approximately 37% |
| 2024 | Semiconductor and artificial-intelligence (NVIDIA, KLA, Broadcom, Applied Materials) | $1,899,308 | approximately 30% |
| 2024 | Defense, energy, and industrial (GE Vernova) | $1,281,249 | approximately 21% |
| 2024 | Consumer technology (Apple, Amazon, Netflix) | $694,539 | approximately 11% |
| 2024 | Other | approximately $340,000 | under 5% |
| 2023 | Defense prime (TransDigm) | $804,606 | approximately 22% |
| 2023 | Semiconductor and artificial-intelligence (NVIDIA, Keysight) | $1,292,888 | approximately 35% |
| 2023 | Consumer technology (Meta) | $433,998 | approximately 12% |
| 2023 | Consumer | approximately $1,100,000 | approximately 30% |

Across tax years 2023 and 2024, defense-prime and semiconductor / artificial-intelligence holdings together constitute approximately 50 percent of the Foundation's non-cash receipt portfolio — the same sectors on which respondent's House Armed Services Committee, Committee on Oversight and Government Reform, and Select Committee on Strategic Competition with China hold jurisdiction.

## CSV 4 — Grantmaking pattern (top 100 grants by amount)

`H_grantmaking_top_recipients.csv` (the top-100 grants by grant-amount across the 2018-through-2024 window).

Headline recipients include University Hospitals Health System (Cleveland, Ohio, recurring across tax years 2020 through 2024), NCH Healthcare System and the Naples Children and Education Foundation (Naples, Florida), the Cleveland Clinic Foundation, Case Western Reserve University, Ford's Theatre Society (Washington, D.C.), and Georgetown University. The grantmaking totals by year:

| Tax year | Total grants | Grant count |
|---:|---:|---:|
| 2020 | $707,500 | 30 |
| 2021 | $4,443,038 | 66 |
| 2022 | $1,004,533 | 41 |
| 2023 | $1,411,200 | 46 |
| 2024 | $2,078,500 | 35 |

The grantmaking is geographically concentrated in Ohio (aligning with the Ahuja family's Cleveland-area base, where Monte Ahuja served as a Director of University Hospitals Health System through 2019) and in Naples, Florida (aligning with the family's Florida residence). None of the top recipients sit within respondent's CA-17 district. The complaint accordingly does not plead Count 6 on a district-enrichment theory — Exhibit Q develops the grantees-by-lobbying-overlap dimension on which the Count 6 substrate rests — but rather on the § 13104(d)(1)(A) spouse-asset-disclosure scope question addressed to the spouse-trustee relationship and to the corpus composition.

---

## Relationship to Exhibits H and Q

Exhibit H uses the TY2024 corpus figure and the TY2024 NVIDIA transfer figures developed above in its Section 2(C) and Section 2(D). Exhibit Q uses the grantmaking pattern developed in CSV 4 to identify federal-lobbying overlap among the top grantees and to identify donor-chairman and officer structural overlap between Foundation grantees and respondent's principal-committee donor clusters. Both exhibits are operative pleadings; this workpaper is their shared data-lineage companion.

---

*Primary-source substrates: IRS 990-PF e-filed XML returns for EIN 34-1685088, tax years 2013 through 2024; ProPublica Nonprofit Explorer mirror of the same filings; IRS Statistics of Income individual-return file.*
