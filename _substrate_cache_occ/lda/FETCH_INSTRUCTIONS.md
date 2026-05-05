# Senate LDA fetch (Khanna recipient)

## What this directory contains (auto-generated)

  khanna_lda_raw_filings.json    # every LD-203 filing where any line
                                  # item named a Khanna-PCC payee variant
  khanna_lda_line_items.json     # flattened per-line-item rows (Khanna-only)
  khanna_lda_aggregate.json      # OCC_M041 load-bearing scalars

## How this was fetched (automated, no auth)

  https://lda.senate.gov/api/v1/contributions/?contribution_payee={variant}

  Variants pulled: 'Ro for Congress', 'Ro Khanna', 'RO KHANNA FOR CONGRESS'
  Per-line-item filter: payee_name ILIKE '%KHANNA%' OR '%RO FOR CONGRESS%'
  Pagination: page_size=100; rate ~1 req/s; no API key required.

## OCC-specific load-bearing claims grounded against this substrate

OCC_M041 — Aggregate registrant-originated LD-203 contributions to
Khanna principal campaign committee (Ro For Congress, FEC C00503185)
across 2011-Q4 through 2026-Q1. Body cites:
  - $299,197.54 across 147 line items
  - 53 distinct registrants

Body invariant cited via F1135 wave-19 substrate-keyed empirical
verification: 53-distinct-registrant universe is BIT-EXACT preserved.
Line / amount totals are PASS_WITH_DEFECT/substrate_count_drift
acknowledged when current API count exceeds 147 / $299,197.54
(corpus-grown beyond snapshot date 2026-05-02).

## Optional: API key for higher rate-limit

Sign up at https://lda.senate.gov/api/ for a free API key; pass via
header `Authorization: Token <key>` for higher-volume access. Not
required for the Khanna-recipient fetch (small result universe;
no rate-limit hits observed at 1 req/s in this script).

## Re-fetch this directory anytime

  python fetch_substrate_occ.py --classes lda

Idempotent. Overwrites prior output. No auth.
