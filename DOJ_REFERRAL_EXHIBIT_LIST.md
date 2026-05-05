---
*Drafted pro se by Kevin Bass. Signed draft; not yet physically transmitted to the Department of Justice pending the complainant's filing decision.*
---

# DOJ_REFERRAL_KHANNA — EXHIBIT LIST

Underlying referral: `DOJ_REFERRAL_KHANNA.md`

The referral selects from the dossier's exhibit pool the seven exhibits whose findings sound in criminal-prosecutorial review. Each exhibit is a standalone markdown document resident at the dossier root with a mirrored copy bundled at `exhibits/` in this reproducibility package; each is independently citable; each traces to primary-source records identified inline.

## Exhibit catalog

| Ex. | Title | File | Primary facts (predicate keywords) | Operative statutes |
|---|---|---|---|---|
| **E** | NDAA enactment-window defense-prime trades — 14 trades across four enactment cycles | `exhibits/EXHIBIT_E_NDAA_WINDOW.md` | NDAA enactment windows, defense-prime trade synthesis, per-trade table | 15 U.S.C. § 78u-1(g) (STOCK Act §§ 3-4 MNPI extension); 18 U.S.C. § 208 |
| **F** | CMS rulemaking × pharma trade cluster — 14 CMS events 2017-05 through 2024-08; § 3 August 2024 same-day cluster (eleven pharmaceutical positions including four-of-nine unique IRA-list manufacturers) with hypergeometric-null candor paragraph | `exhibits/EXHIBIT_F_CMS_PHARMA.md` | CMS rulemaking windows, pharma-sector trade synthesis, IRA pharma cohort four-of-nine same-day overlap | 15 U.S.C. § 78u-1(g); 18 U.S.C. § 208 |
| **FF** | Three-way agreement table (lake × Capitol Trades × QuiverQuant) — independent primary-source validation; 11 of 12 CMS IRA pharma-cohort trades three-way corroborated | `exhibits/EXHIBIT_FF_3WAY_AGREEMENT.md` | three-way per-trade match, tracker-defect pre-emption | corroborating substrate for §§ 78u-1(g), 78ff, 78j(b) |
| **M** | Same-day SEC Form 8-K trade pattern — 186 household trades filed the same calendar day as the issuer's 8-K; chamber rank 1 of 96 by absolute count; two-universe rate disclosure | `exhibits/EXHIBIT_M_SAME_DAY_8K.md` | same-day 8-K intersection, two-universe rate disclosure, ticker-specificity, composite-pattern parallelism | 15 U.S.C. §§ 78u-1(g), 78ff, 78j(b); 18 U.S.C. § 1348 (securities fraud) |
| **N** | Palantir 2022-05-10 same-day cluster — six household Palantir trades on the day of an Air Force award announcement | `exhibits/EXHIBIT_N_PALANTIR_TIMELINE.md` | Palantir defense-prime timeline, HASC jurisdictional nexus | 15 U.S.C. § 78u-1(g); 18 U.S.C. § 208 |
| **X** | FDA advisory-committee × pharma trade windows — 1,070 ±3-day / 4,595 ±14-day pharma transactions; chamber rank 1 of 66 | `exhibits/EXHIBIT_X_FDA_ADCOM_PHARMA_WINDOWS.md` | FDA advisory-committee windows, pharma-sector absolute-count chamber rank, saturation-rate candor | 15 U.S.C. § 78u-1(g); 18 U.S.C. § 208 |
| **Z** | Aligned-direction named-officer same-day trade matches — 86 household trades executed the same day as a same-direction Form 3/4/5 by a named corporate officer; chamber rank 3 of 156 | `exhibits/EXHIBIT_Z_86_ALIGNED_INSIDER_MATCHES.md` | named-officer Form 3/4/5 same-day same-direction intersection | 15 U.S.C. §§ 78u-1(g), 78ff, 78j(b) |

## Cross-reference to referral structure

| Referral section | Operative statutes | Exhibits |
|---|---|---|
| § II — Securities fraud / MNPI use under STOCK Act §§ 3-4 | 15 U.S.C. §§ 78u-1(g), 78ff, 78j(b); 17 C.F.R. § 240.10b-5 | M, Z, F, X |
| § III — Defense-sector front-running and conflict-of-interest | 18 U.S.C. § 208; 15 U.S.C. § 78u-1(g) | E, N |
| § IV — Substrate corroboration | — | FF |

## Provenance and archival

Every fact cited in every exhibit has complete provenance in the fact store. The authoritative per-fact SQL or primary-source URL and the archival timestamp are attached to each fact record; the referral citations reference primary-source documents (House Clerk Periodic Transaction Reports, SEC EDGAR Form 8-K and Form 3/4/5, Federal Register advisory-committee notices, CMS rulemaking dockets, USAspending federal-contract awards) in first position and lake substrate in second. The shared `exhibits/` pool is bit-identical across all four filing-class catalogs (OCC, DOJ, House Ethics, FEC referral); see `99_SHA256SUMS.txt`.

---

*End of DOJ exhibit list.*
