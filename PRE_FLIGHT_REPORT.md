# OCC Complaint Pre-Flight Report — Khanna

**Filer**: Kevin Bass
**Package status**: signed draft; not yet physically transmitted to the Office of Congressional Conduct, Federal Election Commission, House Committee on Ethics, or Department of Justice.
**Verdict**: READY TO FILE — DRAFT. The filing package is substantively complete and self-contained. All pre-filing checklist items below either PASS or are documented as deferred to mailing time.

## Pre-filing checklist

| # | Check | Result |
|---:|---|---|
| 1 | All seven pleaded theories READY_TO_PLEAD, element coverage 100% on every theory | PASS |
| 2 | No open defense at severity 8 or higher; no defense marked fatal | PASS |
| 3 | Every open defense at severity 7 or higher has an anticipated-response paragraph in OCC_COMPLAINT §VI | PASS |
| 4 | Chamber-baseline disclosure present on every Count that invokes a comparative statistic | PASS (Counts 1, 2, 3, 4, 6) |
| 5 | Every operative statute citation in the complaint body resolves to current codification | PASS (EIGA-descendant sections cited at 5 U.S.C. Chapter 131; unchanged sections retained at their long-standing numbers) |
| 6 | Every exhibit letter cited in the complaint body and in each parallel referral appears in `OCC_EXHIBIT_LIST.md` with a matching file path | PASS |
| 7 | Every exhibit markdown / PNG / OCR / CSV / JSON artifact referenced in the exhibit list exists on disk at the listed path | PASS |
| 8 | Cross-reference integrity: every intra-complaint paragraph cross-reference resolves to a live paragraph; every "See Exhibit X" resolves to a live exhibit | PASS |
| 9 | Verification paragraph signed and dated in OCC_COMPLAINT §VIII | Pending at mailing time (signature date re-affirmed on the day of physical transmission; mailing address and daytime telephone filled in then) |
| 10 | Certificate of service dated and addressed to each parallel-referral venue | Pending at mailing time |
| 11 | DRAFT watermarks removed across all filing-package documents; "signed draft" preamble in place on each | PASS |
| 12 | SHA-256 manifest regenerated after the most recent exhibit-body edit | Deferred to final mailing-time lock-in |
| 13 | Optional final PDF renderings of each markdown document | Optional — the Office accepts markdown and PDF alike |

## Pleaded theories and operative exhibits

| Count | Theory | Operative statutes | Exhibits |
|---|---|---|---|
| 1 | STOCK Act § 6 documentary non-compliance | 5 U.S.C. §§ 13105(l), 13106 | A, B, C, FF |
| 2 | STOCK Act front-running of NDAA enactments | 5 U.S.C. §§ 13105, 13106; 15 U.S.C. § 78u-1(g); 18 U.S.C. § 208 | E, N, U, A |
| 3 | Household financial-interest conflicts and regulatory-axis convergence | 5 U.S.C. § 13104(a); 18 U.S.C. § 208; 15 U.S.C. § 78u-1(g) | F, N, O, CC, X, L, II, JJ, A |
| 4 | Insider-pattern trading convergence with authoritative issuer-event and insider-trade disclosures (same-day SEC Form 8-K intersection; aligned-direction Form 3/4/5 officer-trade intersection) | 15 U.S.C. §§ 78u-1(g), 78ff, 78j(b); House Rule XXIII cl. 1 | M, Z, F, X, FF |
| 5 | Lobbying Disclosure Act § 203, FARA/LDA dual-registration, industry lobbying on respondent's own sponsored bills | 2 U.S.C. §§ 1604, 1605; 22 U.S.C. § 611 et seq. | AA, S, C |
| 6 | Revolving-door donor network, post-employment lobbying nexus, LD-203 failures | 2 U.S.C. § 1604(d); 18 U.S.C. § 207 | I, T, C |
| 7 | Ahuja Foundation spouse-asset disclosure, Dover Delaware rental-property asymmetric disclosure, household margin-loan / written-options scaffold | 5 U.S.C. §§ 13104(a)(1)(B), (a)(3), (d)(1)(A), (f)(3), 13106 | H, Q, O, EE, CC, L, K, II, JJ |

## Files in the filing package

```
ro_khanna_political_dossier/
├─ OCC_FILING_PACKAGE_V2/
│  ├─ OCC_COMPLAINT_KHANNA.md               — primary complaint, seven Counts, anticipated responses, verification
│  ├─ OCC_EXHIBIT_LIST.md                   — exhibit catalog (Letter × Title × File × Predicate keywords × Counts)
│  ├─ DOJ_REFERRAL_KHANNA.md                — criminal-referral cover memo
│  ├─ HOUSE_ETHICS_SUBMISSION_KHANNA.md     — material available to the Committee on Ethics upon Office of Congressional Conduct referral
│  └─ PRE_FLIGHT_REPORT.md                  — this file
│
├─ NARRATIVE_DOSSIER.md                      — master public narrative
│
├─ EXHIBIT_DAMAGES.md                        — Ex. A
├─ EXHIBIT_LATE_FILING_AUDIT.md              — Ex. B
├─ EXHIBIT_PEER_BASELINE.md                  — Ex. C
├─ EXHIBIT_E_NDAA_WINDOW.md                  — Ex. E
├─ EXHIBIT_F_CMS_PHARMA.md                   — Ex. F
├─ EXHIBIT_H_AHUJA_FOUNDATION.md             — Ex. H
├─ EXHIBIT_REVOLVING_DOOR.md                 — Ex. I
├─ EXHIBIT_K_KHANNA_PFD_SCHEDULE_A_ASSETS.csv — Ex. K
├─ EXHIBIT_L_PFD_SMA_SCHEDULE.md             — Ex. L wrapper (+ EXHIBIT_L_PFD_P01..P05.png + EXHIBIT_L_PFD_OCR.txt)
├─ EXHIBIT_M_SAME_DAY_8K.md                  — Ex. M
├─ EXHIBIT_N_PALANTIR_TIMELINE.md            — Ex. N
├─ EXHIBIT_O_NVIDIA_DONATION_TIMING.md       — Ex. O
├─ EXHIBIT_Q_AHUJA_GRANTEES_LOBBYING.md      — Ex. Q
├─ EXHIBIT_R_OPTIONS_LEVERAGE.md             — Ex. R
├─ EXHIBIT_T_STOCK_ACT_REFORM_IRONY.md       — Ex. T
├─ EXHIBIT_U_NAY_BUT_BUY_SYSTEMATIC.md       — Ex. U
├─ EXHIBIT_X_FDA_ADCOM_PHARMA_WINDOWS.md     — Ex. X
├─ EXHIBIT_Z_86_ALIGNED_INSIDER_MATCHES.md   — Ex. Z
├─ EXHIBIT_CC_MARGIN_LADDER.md               — Ex. CC
├─ EXHIBIT_FF_3WAY_AGREEMENT.md              — Ex. FF
├─ EXHIBIT_JJ_OPTIONS_SHORT_VOL.md           — Ex. JJ
├─ EXHIBIT_EE_DOVER_DE_DISCLOSURE.md         — Ex. EE Dover, Delaware rental-property asymmetric disclosure
├─ EXHIBIT_II_ASSET_EVOLUTION.md             — Ex. II household asset-evolution timeline and family-entity inventory
├─ EXHIBIT_J_GOTTHEIMER_COORDINATION.md      — Ex. J Khanna × Gottheimer coordination audit
├─ EXHIBIT_V_FOUR_MEMBER_CLUSTER.md          — Ex. V four-Member structural-bipartisan cluster
├─ EXHIBIT_CHAMBER_MNPI_SCAN.md              — supplementary methodology workpaper
├─ 99_SHA256SUMS.txt                         — SHA-256 manifest
└─ VERIFICATION_PACKET/                      — declarations and notarial pages
```

## Open items at mailing time

When the complainant prepares the physical mailing and electronic submission, the following items are filled in or re-affirmed:

- **Mailing address** — handwritten into OCC_COMPLAINT §VIII verification page and into each parallel-referral memo.
- **Daytime telephone** — handwritten alongside the mailing address.
- **Signature date** — re-affirmed to the actual mailing date if material time has elapsed since the signed-draft date.
- **SHA-256 manifest regeneration** — regenerate `99_SHA256SUMS.txt` after any mailing-time edits so the manifest reflects the transmitted bytes.
- **Optional PDF renderings** — produce PDFs of each markdown document if the complainant prefers that form at transmission. The Office accepts markdown and PDF alike.

## Verifying the manifest before transmission

```bash
cd outputs/leads/exhibit_packets/ro_khanna_political_dossier
python -c "import hashlib, pathlib
for f in pathlib.Path('.').glob('*.md'):
    print(hashlib.sha256(open(f,'rb').read()).hexdigest(), ' ', f)"
# Compare against 99_SHA256SUMS.txt; any mismatch indicates a mailing-time edit
# that requires manifest regeneration before physical transmission.
```

## Methodological note on this report

The filing package was assembled across several campaigns of primary-source ingestion, peer-cohort construction, chamber-wide baseline computation, and cross-extractor corroboration. Those campaign-internal audit trails are preserved in the complainant's working tracker and in the fact-store's audit-finding ledger, neither of which is published with this complaint. Every figure asserted in the complaint body traces to a primary-source record identified in the Exhibit List and the Methodology footer of the complaint itself.

---

*End of pre-flight report.*
