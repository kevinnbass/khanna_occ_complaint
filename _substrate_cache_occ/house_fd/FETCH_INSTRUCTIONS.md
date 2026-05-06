# House Clerk FD fetch (Khanna K000389)

## What this directory contains (auto-generated)

  khanna_fd_index_<year>.tsv     # per-year filtered Khanna rows
  khanna_fd_index_all_years.tsv  # combined Khanna rows across all years

Columns (per the House Clerk FD bulk feed):
  Prefix | Last | First | Suffix | FilingType | StateDst | Year | FilingDate | DocID

FilingType codes: C=candidate annual, O=officer (Member) annual PFD,
P=PTR, A=amendment, X=extension, D=DC, W=withdrawal.

## Per-doc PDF URL pattern

  PFD: https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf
  PTR: https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf

Where {year} is the disclosure year column from the index and {doc_id}
is the DocID column. Example PFD anchor cited at OCC §III.7:

  https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024/8221318.pdf

## OCC-specific load-bearing claims grounded against this substrate

Count 1 (STOCK Act §6 late-filing audit): every Khanna PTR cited in the
operative §A Provenance Appendix (OCC body lines 569-670) carries a
DocID that matches the DocID column in khanna_fd_index_all_years.tsv
(filtered to FilingType='P'). Cross-reference Khanna's 9 PTRs cited in
the late-filing audit by joining DocID against this TSV.

Count 6 (Schedule A spousal-asset disclosure): every Khanna annual PFD
(FilingType='O') across TY2014-TY2023 is enumerated in the combined
TSV with its filing-date and DocID. Join against this TSV to confirm
filing-date ordering for the late-amendment timing claim at OCC §III.7.

## Fetch this directory anytime

Re-running `python fetch_substrate_occ.py --classes house_fd` re-pulls
every per-year ZIP (~80-200 KB each) and re-emits the filtered TSVs.
Idempotent — overwrites prior output. No API key, no auth.
