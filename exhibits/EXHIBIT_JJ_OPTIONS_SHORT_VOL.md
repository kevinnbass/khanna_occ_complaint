# Exhibit JJ — Systematic XSP Short-Volatility Program (Spouse Account)

**Case**: *In re Representative Rohit "Ro" Khanna (CA-17)*
**Counts supported**: Count 3 (financial-interest conflicts — independent confirmation that the household's options activity is not broker-discretionary); Count 6 (§ 13104(f)(3) SMA/QBT/EIF defense foreclosure)
**Subject accounts**: SP owner (spouse Ritu Ahuja Khanna) options activity, 2017–2026

---

## 1. Purpose and analytic scope

This exhibit characterizes, from primary-source Periodic Transaction Reports, the systematic S&P 500 mini-index ("XSP") PUT-option writing program run out of the spouse-owned account during respondent's House tenure. The analytic posture is deliberately narrow: the exhibit does **not** assert that the XSP program is driven by Member-side material non-public information. It asserts the opposite — that the program is a systematic short-volatility / cash-secured-put income strategy — and then shows why that characterization, properly credited, still defeats the passive-account affirmative defense relevant to Counts 3 and 7.

The related directional cluster (the 2026-03-16 twenty-contract single-stock PUT book in NVDA, AMD, AVGO, MSFT, and PLTR) is documented in Exhibit R and is intentionally excluded from this exhibit's MNPI-adjacent analysis.

---

## 2. The 282-transaction XSP baseline

Across respondent's House tenure, the spouse-owned account executed **282 separate XSP PUT-option transactions** (PUT options on the S&P 500 mini-index), every row owner-coded SP. Amount bands on each individual transaction are $1,001 to $15,000 — the typical footprint of a premium-receipt record, not a notional-exposure record. Strike prices span roughly $585 to $669; expiries roll across weeks and months in a continuous overlay.

The activity is structurally consistent with cash-secured short-PUT writing — a systematic income strategy in which the account sells PUT options at strikes below current market level, collects premium, and rolls positions continuously. It is **not** consistent with event-timed speculation: a targeted query of XSP transactions by calendar month across the full tenure returns a baseline of 2–6 options per month with no systematic spikes around MNPI-adjacent policy events. The FIT21 vote month (May 2024) shows 5 options (baseline); the Building Chips in America Act NAY vote month (September 2024) shows 2 options (below baseline). An isolated April 2025 spike (13 options, two to three times baseline) is unexplained but is a single data point, not a pattern.

---

## 3. Re-analysis of PUT-sale transactions — "S" transaction-type collapse

The PTR reporting schema records a PUT option sale as `transaction_type = 'S'` (Sale). That code collapses two distinct economic operations:

- **Sell-to-open** (short-PUT writing) — bullish premium collection, resulting in positive P&L if the underlying stays above strike;
- **Sell-to-close** (long-PUT unwinding) — removing a prior bearish hedge, resulting in either gain or loss depending on basis.

Neither directly reads as a directional bearish MNPI bet. Multiple pieces of evidence on the record are consistent with the short-PUT premium-harvest interpretation:

1. **Deep out-of-the-money strikes.** The 2025-04-08 NVDA PUT activity prices the strike at $75 against a day-of close of $96.30 — 22% out-of-the-money.
2. **Uniform tiny amount bands.** Rows report $1,001–$15,000 buckets — premium receipts, not underlying notional.
3. **Same-day multi-ticker multi-expiry SP+DC pairing.** Identical strikes and expiries executed simultaneously across the spouse and dependent-child owner codes is an algorithmic / managed-account execution signature, not a volitional Member decision.
4. **Post-trade outcome.** NVDA closed at $96.30 on 2025-04-08 and closed at $114.33 on 2025-04-09, sustained through $114.50 on 2025-05-02 — a +18.7% move the day after the PUT activity. A rising stock is profitable for the short-PUT writer and inconsequential to the long-PUT closer; it is disconfirming of a bearish-MNPI reading.

**Operational conclusion.** The PUT-sale activity is most plausibly characterized as a systematic short-premium income strategy executed across the spouse and dependent-child accounts by a managed-account routine, not as Member-informed directional speculation. The complaint credits that characterization explicitly.

---

## 4. Why the short-vol characterization still defeats the passive-account defense

Crediting the short-volatility characterization does not save the SMA / QBT / EIF affirmative defense; it is the characterization that the defense must in fact rely on to be plausible. Three independent consequences follow:

1. **Short-PUT writing on a cash-secured account requires options authorization.** Under Regulation T and FINRA Rule 4210, a broker-dealer cannot write uncovered PUTs or carry short-put exposure on an account unless the account holder affirmatively authorizes the options level. That authorization is executed by the spouse, not by a discretionary trustee. The authorization fact, by itself, defeats § 13104(f)(3) blind-trust posture and the parallel SMA-defense premise (an SMA requires that the third party, not the Member's spouse, be the account decision-maker for risk-category purposes).
2. **Short-PUT writing on a margin-collateralized account compounds the authorization finding.** The margin-loan scaffold documented in Exhibit CC extends through the TY2017–TY2019 period and overlaps the sustained XSP short-vol program; writing PUTs against a margined account that the spouse holds in her own name is, under customer-protection rules, an affirmatively authorized account structure.
3. **Absence of any SMA on the PFD.** The 2024 Annual PFD (Exhibit L) discloses no separately managed account, no qualified blind trust, and no third-party discretionary custodian. A systematic short-volatility program running out of the spouse's account, with no SMA documented on the filing, is simply the spouse's own investment activity.

The conclusion is therefore asymmetric. On one axis (the STOCK Act §§ 3–4 MNPI-adjacent framing), the exhibit narrows what can responsibly be pleaded: the XSP program as a whole is not an MNPI smoking gun; per-trade MNPI scrutiny appropriately focuses on individual-stock clusters and legislative-window trades, not on the index-option baseline. On the other axis (the § 13104(f)(3) passive-account defense), the exhibit strengthens the case: the most plausible charitable reading of the activity — systematic premium harvest — is itself incompatible with the blind-trust posture the defense requires.

---

## 5. Disposition

The XSP short-volatility program is documented as a systematic income strategy run from an SP-owned account, not as an MNPI-adjacent directional bet. The 282 distinct transactions represent 282 distinct disclosure obligations under STOCK Act § 6, each evaluable for timeliness on its own merits irrespective of directional content. Nothing in this characterization disturbs the per-trade MNPI evaluations applied separately to individual-stock equity clusters in Exhibits M, N, and F.

---

## 6. Statutory framing

- **STOCK Act § 6 / 5 U.S.C. § 13105(l)** — each XSP option transaction is an independent reportable event subject to the 45-day filing deadline.
- **5 U.S.C. § 13104(a)(3), (a)(5), and (a)(8)** — disclosure of interests in property, of reportable transactions, and of qualified blind trusts; a cash-secured options account executing 282 transactions must be reflected on the PFD asset catalog under at least one of these provisions.
- **5 U.S.C. § 13104(f)(3)** — qualified-blind-trust and exempt-investment-fund conditions; incompatible with an account holder (the spouse) who executes options-level authorization.
- **Regulation T**, 12 C.F.R. Part 220; **FINRA Rule 4210** — options-account and margin-account customer-authorization requirements.
- **15 U.S.C. § 78u-1(g)** — STOCK Act §§ 3–4 MNPI framework, applied here at the individual-stock per-trade level rather than to the index-option baseline.

---

## 7. Primary sources

- U.S. House Clerk — respondent's Periodic Transaction Reports, full tenure, filtered to `asset_name ILIKE 'PUT/XSP%'` with `owner='SP'`.
- `lake.house_ptr_transactions` — transaction-level counts and monthly cadence.
- `lake.stock_ohlc_daily` — NVDA daily prices 2025-04-08 through 2025-05-02.
- Clerk of the House — roll-call vote records for FIT21 (May 2024) and S 2228 Building Chips in America Act (September 2024).

---

*End of Exhibit JJ.*
