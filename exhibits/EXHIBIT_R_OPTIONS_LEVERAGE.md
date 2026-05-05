# Exhibit R — Directional Options Leverage (Single-Name Puts)

**Count supported.** Count 2 (NDAA enactment-window trades) and Count 3 (financial-interest conflicts) — the options activity is the leverage layer on the underlying NDAA-window and chip-policy patterns.

**Scope.** This exhibit is narrowed to single-name directional puts on individual equities — the operative MNPI signal. Index-level and FLEX EURO PM dividend-capture structures are inventoried below for completeness but are not load-bearing; the short-volatility index-level activity is addressed in a separate exhibit.

---

## 1. Method

Single-name options trades carry a directional signature that does not depend on Black-Scholes fair-value pricing. A household selling puts on a specific stock takes a position consistent with a non-bearish view on that stock; selling calls is consistent with a non-bullish view; buying puts is consistent with a bearish view; buying calls is consistent with a bullish view. The *direction* of the option trade is the case-relevant fact, independent of dollar-precision premium pricing. Black-Scholes fair-value computation of premium captured is deferred pending an options-pricing data source.

The full inventory of options trades on the household PTR record is queried from the PTR substrate on any row whose asset name contains PUT or CALL. The 598 total rows span index puts, FLEX EURO PM dividend-collection structures, and single-name options spanning 2017-02-16 through 2026-03-30.

## 2. Household options inventory by class

| Class | Count | BUYs | SELLs | Date span |
|---|---:|---:|---:|---|
| PUT — index (XSP / SPY / IWM / SPX / RUT / QQQ / VIX) | 319 | 231 | 88 | 2017-03-02 – 2026-03-30 |
| CALL / PUT — FLEX EURO PM (European-ADR dividend capture) | 137 | 122 | 15 | 2022-01-07 – 2026-03-13 |
| **PUT — single-name** | **99** | **54** | **45** | **2017-02-16 – 2026-03-23** |
| **CALL — single-name** | **43** | **31** | **12** | **2019-09-19 – 2026-02-12** |
| **Total options rows** | **598** | | | **2017-02-16 – 2026-03-30** |

The single-name PUT inventory is the operative cluster for the directional analysis. The single-name CALL inventory is smaller and mixed-direction. The 319 + 137 = 456 index and FLEX EURO PM rows are predominantly hedging or dividend-collection structures — XSP and SPY puts as portfolio hedges, FLEX EURO PM calls as European-ADR dividend-capture structures — rather than directional positions on specific policy outcomes.

## 3. Cluster A — 2025-04-08 post-tariff-dip broad-market SELL-PUT cluster

Four calendar days after the 2025-04-04 "Liberation Day" tariff-driven equity selloff began, the household executed a multi-ticker SELL-PUT cluster across nine underlyings (17 positions total, all expiring 2025-07-18):

| Underlying | SELL-PUT count | BUY-PUT count | Owner allocation |
|---|---:|---:|---|
| NVDA | 2 | 0 | SP + DC |
| AAPL | 2 | 0 | SP + DC |
| GOOGL | 2 | 0 | SP + DC |
| GS | 2 | 0 | SP + DC |
| IWM | 2 | 0 | SP + DC |
| SPY | 2 | 0 | SP + DC |
| JPM | 1 | 1 | SP (S) + DC (P) |
| TSLA | 1 | 0 | SP |
| V | 1 | 0 | DC |
| (additional row recorded with ticker "JPN" but `asset_name` reads "JPMORGAN CHASE & CO. JUL 18 25 $170" — strike, expiry, and underlying match the JPM row above; treated as a JPM duplicate or ticker-OCR variant) | 1 | 0 | DC |

The structure is a buy-the-dip SELL-PUT posture: the household saw the 2025-04-04 tariff-driven drop and wrote puts to either collect premium (if the tickers recovered, which they did by mid-May 2025) or take assignment at lower prices. Either outcome is consistent with a non-bearish view on the underlyings — a position consistent with an expectation that the tariff shock would be temporary.

The MNPI-relevance question: what did respondent know about the trajectory of U.S.–China tariff policy on 2025-04-08? Respondent sat as Ranking Member of the House Select Committee on Strategic Competition between the United States and the Chinese Communist Party at this time; House Armed Services covers AI and data-platform procurement (NVDA-dominant). Both committees provided visibility into administration tariff-walkback negotiations not available to public investors. The household's same-day broad-market SELL-PUT across NVDA, GOOGL, AAPL, and TSLA is consistent with a non-public expectation that the tariff shock would unwind.

## 4. Cluster B — 2026-03-16 chip / AI single-day SELL-PUT cluster

The largest single-day options cluster in the dataset — and the one that broadens the earlier Palantir-puts finding into a full chip / AI stack position. On 2026-03-16, the household executed **20 SELL-PUT positions** across five tickers, two expiries, and two owner accounts:

| Ticker | Expiry | Strike | SP | DC | Total |
|---|---|---:|:-:|:-:|---:|
| NVDA | 2026-09-18 | $155 | yes | yes | 2 |
| NVDA | 2027-03-19 | $155 | yes | yes | 2 |
| AVGO | 2026-09-18 | $280 | yes | yes | 2 |
| AVGO | 2027-03-19 | $280 | yes | yes | 2 |
| AMD | 2026-09-18 | $170 | yes | yes | 2 |
| AMD | 2027-03-19 | $165 | yes | yes | 2 |
| MSFT | 2026-09-18 | $340 | yes | yes | 2 |
| MSFT | 2027-03-19 | $340 | yes | yes | 2 |
| PLTR | 2026-09-18 | $130 | yes | yes | 2 |
| PLTR | 2027-03-19 | $130 | yes | yes | 2 |
| **Total** | | | **10** | **10** | **20** |

The five tickers cover the AI / chip / data-platform stack — NVIDIA (AI accelerator GPUs); Broadcom (AI networking and custom silicon); AMD (AI accelerator and datacenter CPU); Microsoft (Azure AI plus OpenAI); Palantir (AI / ML platform for DoD and the intelligence community). Each SELL-PUT carries the obligation to buy 100 shares at the strike if the price falls below it, with premium as the payoff if the price stays above; the position is consistent with a non-bearish view on the five underlyings through expiry.

The structural concentration is probative. Twenty SELL-PUT positions across five names in a single calendar day across both spouse and dependent-child accounts is a record at variance with passive index rebalancing — a separately-managed account does not write naked puts on individual chip stocks — and is at variance with dividend capture or portfolio hedging. It is consistent with a unified household directional view across the AI stack six to twelve months forward.

The MNPI-relevance question for 2026-03-16: what did respondent know about U.S. chip policy, NVIDIA China-export licensing, or AI legislation on that date? Respondent chaired the China Select Committee at this point; House Armed Services covers AI procurement; the FY2026 NDAA had been moving through markup since mid-2025. Respondent had structural visibility into AI-procurement appropriations and chip-export-license modifications during the same week the household placed the 20-position chip-stack position.

## 5. Cluster C — FLEX EURO PM dividend-capture (documented, not load-bearing)

On 2026-03-13, the spouse account purchased four FLEX EURO PM CALL contracts on European-ADR tickers expiring the same day:

| Ticker | Underlying | Strike | Expiry |
|---|---|---:|---|
| SHEL | Shell plc (U.K. oil major) | $76 | 2026-03-13 |
| TTE | TotalEnergies (French oil major) | $69 | 2026-03-13 |
| NGG | National Grid plc (U.K. utility) | $85 | 2026-03-13 |
| CCEP | Coca-Cola Europacific Partners (U.K. consumer) | $94 | 2026-03-13 |

These are dividend-capture trades — the FLEX EURO PM (European Per-Mark) CALL structure with same-day expiry is a standard mechanism for capturing dividend payment on the underlying without holding the stock through tax-disadvantageous events. The trades carry a limited MNPI-relevant signal; they are a tax-arbitrage construct routinely used by sophisticated households with European-ADR holdings. Documented for inventory completeness; not load-bearing for the counts.

## 6. Disposition

The directional single-name PUT inventory broadens the prior Palantir-puts finding into a recurrent pattern:

- A 20-position SELL-PUT chip / AI stack on 2026-03-16 across NVDA, AVGO, AMD, MSFT, and PLTR, across both spouse and dependent-child accounts, across two expiries spanning September 2026 to March 2027.
- A 9-underlying broad-market SELL-PUT buy-the-dip cluster on 2025-04-08, four days after the tariff-driven equity selloff began, across NVDA, AAPL, GOOGL, GS, IWM, SPY, JPM, TSLA, and V, with 17 positions total.

Both clusters are non-bearish directional positions placed at moments when respondent's committee jurisdictions provided structural visibility into administration policy direction not available to public investors. The exhibit supports the §VI anticipated-response cluster that addresses the passive-SMA framing, because the structural concentration on specific names in specific committee-sensitive policy windows is at variance with model-portfolio rebalancing or dividend-capture mechanics.

Fair-value pricing of the puts' premium at trade date — which would quantify the premium-captured dollars — is deferred pending an options-pricing data source.

---

*End of exhibit.*
