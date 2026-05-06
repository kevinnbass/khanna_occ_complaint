# Exhibit V — Four-Member Cluster: Respondent plus Gottheimer, McCaul, and Austin Scott

This exhibit collects the four-Member cluster context that bears on Counts 4 and 7. It is offered as structural context, not as a coordination charge: the unit of analysis is not a pattern of communicated trades among the four Members, but the shared structural condition — committee-jurisdictional access to material non-public information overlaid on active household-portfolio trading in the same jurisdictional sectors — that the four Members share across two parties and three geographic regions.

---

## 1. Scope

Four House Members active in the 117th through 119th Congresses comprise the cluster, each identified through independent primary-source analysis:

| Member | Bioguide | Party / District | Structural finding |
|---|---|---|---|
| Ro Khanna | K000389 | D / CA-17 | Subject of this complaint: six theories pleaded as ready on Counts 1 through 6 |
| Josh Gottheimer | G000583 | D / NJ-5 | Second-respondent coordination framing on Count 4: shared crypto-industry donor cluster; PROTECT PROGRESS dual-recipient; 11 C.F.R. § 109.21(d)(4) common-vendor coordination indicia via Global Strategy Group |
| Michael McCaul | M001157 | R / TX-10 | Chair of the House Foreign Affairs Committee (118th Congress); prior Chair of the House Committee on Homeland Security (113th–115th Congresses); household General Electric purchase nine days before FY2023 National Defense Authorization Act enactment and twenty days before swearing-in as HSFA Chair |
| Austin Scott | S001189 | R / GA-8 | House Armed Services Committee member continuously since 2013; spouse-owner General Electric purchase nine days before FY2021 NDAA enactment; batched eight-defense-prime spouse-sell disclosure 241 to 313 days past the STOCK Act deadline |

The four do not form a uniform political bloc — two Democrats, two Republicans; California, New Jersey, Texas, and Georgia. What they share is the structural condition set out in Section 3.

### 1.1 Cluster-Member selection criteria

The four-Member cluster is the output of a three-filter ex-ante selection rule applied to the full 435-Member House universe across the 115th through 119th Congresses. The rule was specified before any same-day-trade-coincidence screen was run, so the cluster's composition is not the product of post-hoc cherry-picking against the trade-overlap variable that Section 4 reports.

**Filter 1 — Committee-jurisdictional MNPI-access overlap with respondent.** A candidate Member must have served, at any point during the 115th through 119th Congresses, on the House Armed Services Committee (HSAS), the House Permanent Select Committee on Intelligence (HLIG), or the House Committee on Foreign Affairs (HSFA). These three committees are the jurisdictional vehicles for the defense-procurement, classified-intelligence, and foreign-policy material non-public-information streams to which respondent has independently been credentialed through HSAS membership. Committees outside this set (HSHM in isolation, House Financial Services, House Oversight, House Energy and Commerce) are excluded from the access-overlap test, even though they carry their own MNPI surfaces, because the overlap with respondent's jurisdictional credentials is what the cluster is built to isolate. Filter 1 narrows the 435-Member universe to approximately seventy-five Members.

**Filter 2 — Active household-portfolio trading.** A candidate Member's household, aggregated across the Member, spouse, dependent children, joint accounts, and trusts, must have filed at least four hundred Periodic Transaction Report transactions across the Member's full chamber-tenure span. Four hundred is the ninetieth percentile of chamber-wide household PTR transaction count for the 119th Congress as drawn from `lake.house_ptr_transactions_canonical`. This filter excludes Members whose household trading is sporadic or absent — a Member with three lifetime PTR transactions, even on a defense-jurisdiction committee, lacks the volume signal that gives a cluster pattern probative weight. Filter 2 narrows the seventy-five-Member set to approximately nineteen Members.

**Filter 3 — Independent primary-source nexus to a covered enactment or independent-expenditure axis.** A candidate Member must, on disclosed-on-the-PTR-or-FEC-record evidence alone, exhibit either (a) a household trade in a defense-prime ticker — Lockheed Martin, RTX, General Dynamics, Northrop Grumman, Boeing, L3Harris, General Electric (defense-aerospace segment), Honeywell (aerospace segment), TransDigm, GE Vernova — within plus-or-minus thirty days of either FY2021 NDAA enactment (Public Law 116-283, January 1, 2021) or FY2023 NDAA enactment (Public Law 117-263, December 23, 2022); or (b) PROTECT PROGRESS or FAIRSHAKE PAC independent-expenditure activity benefiting the Member's principal campaign committee in the 2024 cycle, drawn from the FEC Schedule E disbursement substrate after transaction-id-canonical de-duplication. Filter 3 narrows the nineteen-Member set to four Members: respondent, Gottheimer, McCaul, and Scott.

The three filters operate sequentially and conjunctively. None of the four cluster Members was identified by trade-coincidence screening against respondent; the same-day-pair signal at Section 4 is observed within the four-Member cluster after the cluster is fixed, not used to seed cluster membership.

### 1.2 Methodology

**Data sources.** Household PTR transaction data is drawn from `lake.house_ptr_transactions_canonical`, the amendment-cascade-deduplicated canonical view that collapses re-filed Periodic Transaction Reports to the earliest filing-level disclosure of each transaction (per the canonical-view convention; the view's tx-key omits amount-range and ticker because both fields are common amendment targets and must not split a single underlying tx into two rows). Committee-roster data is drawn from House Clerk roster files for the 115th through 119th Congresses; HLIG roster data, which is not published in the standard committee roster file because HLIG membership is by Speaker's appointment, is drawn from the Speaker's appointment letters published in the Congressional Record at the convening of each Congress. NDAA enactment dates are drawn from the Public Law slip-law records on congress.gov. PROTECT PROGRESS and FAIRSHAKE FEC Schedule E disbursement records are drawn from the FEC bulk-data Schedule E corpus after transaction-id-canonical de-duplication (a single independent expenditure is filed at least twice — once as a Form F24 forty-eight-hour notice and again inside a Form F3X quarterly report or amendment — and the disbursement records share a transaction_id; aggregating without transaction-id dedup over-counts the underlying expenditure approximately twofold).

**De-fan-out rule.** The same-day-pair screen at Section 4 treats any (Member, owner-class, ticker, calendar-date, direction) tuple as one trade pair regardless of subaccount multiples. A single trading decision split across four sibling trusts of the same dependent-child owner-class on the same calendar date appears as one pair, not four. This rule is necessary because PTR sub-account proliferation is a disclosure artifact rather than a multiplication of underlying trades; counting sub-accounts as independent observations would inflate the trade-coincidence signal.

**Mega-cap suppression.** The top-twenty highest-volume tickers by chamber-wide household PTR count are suppressed in the lowest two amount brackets ($1,001 to $15,000 and $15,001 to $50,000) on the theory that low-bracket positions in mega-capitalization tickers — Apple, Microsoft, Nvidia, Amazon, Berkshire Hathaway B, and the like — are dominated by separately-managed-account model-portfolio trades that two Members holding similar SMA model portfolios at the same custodian will execute on the same day for reasons unrelated to coordination or shared MNPI. Higher-bracket pairs in the same tickers are retained because the SMA-model-portfolio explanation weakens as bracket size rises (a $1M-to-$5M bracket Microsoft purchase is not a model-portfolio rebalance).

**Chamber-wide pair-count distribution.** Across the chamber-wide 435-Member universe in the 119th Congress, the distribution of same-day same-ticker same-direction pair counts per Member-pair after de-fan-out and mega-cap suppression has a median of one pair, a 75th-percentile value of two pairs, a 95th-percentile value of six pairs, and a maximum that places the Khanna-McCaul cell at chamber rank-1 post-filter. The Khanna-McCaul thirty-pair count therefore sits well above the chamber-wide upper-tail of the pair-count distribution.

**Null hypothesis.** Under a random-trade null in which each Member's household trades are independently drawn from the empirical chamber-wide ticker-and-date distribution, the expected same-day same-ticker same-direction pair count between Khanna and McCaul over the observed 2018-through-2026 window is approximately 4.7 pairs (computed via the hypergeometric methodology developed at Exhibit Z Section 7.2). Observed pair count is thirty. The two-sided p-value under the null is below 0.001. The signal is statistically real; whether it is shared-SMA-model-portfolio in origin or shared-MNPI-information in origin is a separate question that this exhibit does not adjudicate (and that, as Section 3.1 makes explicit, this exhibit cannot adjudicate without classified-briefing-schedule access).

## 2. Cluster transaction profile

Aggregate household PTR transaction volume across each Member's full chamber-tenure span:

| Member | Transactions | Disclosed value, minimum | Disclosed value, maximum | Buys | Sells | Buy:Sell |
|---|---:|---:|---:|---:|---:|---:|
| Khanna (2017–) | 36,288 | $196M | $815M | 24,624 | 11,660 | 2.11× |
| McCaul (2012–) | 11,328 | $863M | $3,791M | 8,992 | 2,117 | 4.25× |
| Gottheimer (2015–) | 3,404 | $43M | $224M | 1,420 | 1,982 | 0.72× |
| Austin Scott (2013–) | 418 | $1.08M | $7.9M | 272 | 145 | 1.88× |
| **Cluster aggregate** | **51,438** | **$1.10B** | **$4.84B** | **35,308** | **15,904** | **2.22×** |

McCaul's dollar-bucket totals reflect family-limited-partnership transfer batches rather than realized-value liquidity; the realized-value cluster total is materially smaller than the aggregate disclosed ceiling. Khanna leads the cluster on transaction count (36,288, approximately 70% of the cluster total). Gottheimer is the only net-seller (more sales than purchases; consistent with active rebalancing rather than directional accumulation). Scott's disclosed volume is a small share of the cluster but rises in structural significance once the committee-access overlap in Section 3 is combined with the NDAA-window and batched-sell patterns.

### 2.1 McCaul realized-value recompute

The McCaul disclosed-value column above ($863M minimum to $3.79B maximum across 11,328 household PTR transactions) materially overstates the realized-value liquidity that flowed through McCaul's household trading account during the 2012-through-2026 window. The overstatement has two distinct sources, each documented from the household's own PTR substrate.

**Family-limited-partnership transfer pattern.** Approximately 348 transactions in the McCaul household PTR record match family-limited-partnership name patterns — "Linda Mays McCaul Partners II Ltd," "LLM Family Investments LP," "McCaul Family Limited Partnership," and analogous corporate-form variants of the spouse's family-LP holdings. The aggregate midpoint dollar volume on the LP-pattern transactions is approximately $159.8M (range $101.2M to $218.4M across the LP rows alone). These transactions are intra-family transfers between LP entities and the household's individual brokerage accounts; they are reportable under 5 U.S.C. § 13104(d)(1)(A) as transactions in reportable assets but are not, in the ordinary case, realized-value liquidity events directionally deployed against external counterparties — they are bookkeeping movements within a single estate-administered family vehicle.

**High-bracket batched-transfer character.** Within the higher PTR amount brackets, an additional concentration is observable. The $1,000,001 to $5,000,000 bracket alone contains 665 McCaul-household transactions, with an aggregate midpoint of approximately $2B. The high-bracket assets concentrate in a small number of estate-administered concentrated positions: Loral Space Communications, Cardtronics, Riviera Resources, JPM Treasury sweep, Core-Mark Holding, Newell Brands, and adjacent former-private-company positions held in LP wrappers. The high-bracket batched-transfer character of these positions cannot be isolated from the aggregate solely on asset_name grounds — some Loral and Cardtronics positions are open-market trades, some are estate-administered batched transfers — and the partial-coverage caveat applies.

**Realized-value floor.** Net of the LP-pattern transactions, the McCaul household disclosed midpoint sums to approximately $2.31B in non-LP-pattern volume across the 2012-through-2026 window. This is an upper bound on realized-value liquidity, not a lower bound: the high-bracket batched-transfer character above further reduces the directionally-deployed-liquidity figure by an amount that this exhibit does not attempt to quantify because the attribution work would require access to internal estate-administration records that the household's PTR substrate alone does not expose.

**Conclusion on cluster aggregate ceiling.** The cluster-aggregate disclosed-value range of $1.10B-to-$4.84B at the head of Section 2 should be read as a CEILING on combined household PTR-disclosed bracket sums, not as a measure of realized liquidity directionally deployed across the four Members' trading accounts. The narrowing carries one important caveat: it does NOT diminish the structural-condition proposition for which the cluster is offered. The unit of analysis is committee-jurisdictional MNPI access overlaid on active household trading in the same jurisdictional sectors, not aggregate dollar volume. McCaul's 2022-12-14 General Electric household purchase nine days before FY2023 NDAA enactment is an event-window observation that is independent of the household-aggregate dollar figures, is anchored on a specific calendar date and a specific defense-aerospace ticker, and is not reduced or rebutted by the LP-transfer recharacterization above.

## 3. Committee co-membership — the MNPI-access overlap

The cluster's structural backbone is committee-jurisdictional access overlap:

| Pair | Committee | Overlap Congresses | Structural note |
|---|---|---|---|
| **Khanna and Austin Scott** | **House Armed Services Committee** | **115th, 116th, 117th, 118th, 119th — five consecutive Congresses, 2017 through the present** | Respondent is ranking member of the Subcommittee on Cyber, Information Technologies, and Innovation (118th and 119th). Scott serves on the Subcommittees on Tactical Air and Land Forces and on Strategic Forces. Defense-procurement material non-public-information access overlap is continuous. |
| **Gottheimer and Austin Scott** | **House Permanent Select Committee on Intelligence** | **118th and 119th — two consecutive Congresses, 2023 through the present** | Gottheimer serves as ranking member of the Subcommittee on the Central Intelligence Agency (118th and 119th). Scott chairs the Subcommittee on the National Security Agency and Cybersecurity (119th). Classified-intelligence briefings material non-public-information access overlap. |
| McCaul and Gottheimer | House Committee on Homeland Security | 117th — single overlap | Limited overlap. McCaul chaired HSHM in the 113th through 115th Congresses, then served as a minority member in the 116th and 117th; Gottheimer served on HSHM in the 117th only. |
| McCaul and Khanna | (none) | — | McCaul's HSFA and HSHM jurisdictions are distinct from respondent's HSAS, House Committee on Oversight, and House Budget Committee jurisdictions. A same-day pair signal between the two Members exists at the chamber rank-one level in a volume-weighted screen, but is not committee-driven. |
| McCaul and Scott | (none) | — | No committee-jurisdictional overlap. |
| Khanna and Gottheimer | (none) | — | No committee-jurisdictional overlap. The coordination indicia on this Member pair, developed at Exhibit J, are donor-universe and shared-vendor in nature, not committee-driven. |

Two structural MNPI-access pairs anchor the cluster:

1. **Khanna plus Scott at HSAS** — five-Congress continuous defense-procurement access overlap.
2. **Gottheimer plus Scott at HLIG** — two-Congress intelligence access overlap.

Austin Scott is the cross-link between the two access pairs; he sits on both HSAS (with respondent) and HLIG (with Gottheimer). McCaul is jurisdictionally separate from the other three.

### 3.1 Limitation framing — classified-briefing-schedule unavailability

The committee-jurisdictional access overlap that Section 3 establishes is general access — it places each cluster Member in the room where the relevant material non-public-information stream flows — but the specific calendars of classified briefings, the specific items briefed at each session, and the specific Members in attendance at each briefing are themselves classified. This exhibit does not have access to those calendars; the public is not a permitted recipient of HSAS, HLIG, or HSFA classified-briefing-schedule records, and the in-camera proceedings of the relevant Subcommittee chairs and ranking members are not subject to the public-disclosure regime that governs PTR and PFD substrate.

The consequence for what this exhibit asserts and what it cannot assert is direct and operative. **This exhibit cannot assert that any specific cluster-Member trade was preceded by a specific classified briefing.** It cannot assert that any cluster Member traded on a specific item of material non-public information conveyed at a specific briefing. It cannot trace a specific same-day-pair tuple in Section 4 back to a specific classified-briefing event. The unit of analysis is therefore the structural pattern-of-conduct — committee-jurisdictional MNPI-access credentials overlaid on active household trading in the same jurisdictional sectors — not specific-tip identification.

A specific-tip claim would require either (a) declassification of the relevant briefing-schedule and attendance records, by the House Speaker or the relevant committee chair, or by the Director of National Intelligence on referral; or (b) in-camera review by the Committee on Ethics under House Rule XI, with subpoena authority over the briefing-schedule records and over the cluster Members' contemporaneous communications. Neither pathway is available to a private complainant on the public record. The relief this complaint seeks at Section V — referral to the Committee on Ethics for in-camera review and to DOJ under 15 U.S.C. § 78u-1(g) for criminal MNPI-trading review — is the procedural vehicle through which the specific-tip question would be reached, not a question this exhibit attempts to reach itself.

The structural-pattern proposition is sufficient on its own for the purpose this exhibit is offered: rebutting the suggestion that the conduct alleged against respondent is sui generis or partisan. The specific-tip question is reserved to the ethics-and-criminal-referral fora that have the procedural tools to reach it.

## 4. Pairwise same-day same-ticker same-direction trade pairs

Aggregate same-day trade coincidence across the four Members after de-fan-out and mega-cap suppression:

| Pair | Pairs | Distinct days | Distinct tickers | First | Last |
|---|---:|---:|---:|---|---|
| Khanna and McCaul | 30 | 21 | 16 | 2018-10-17 | 2026-02-17 |
| Gottheimer and McCaul | 8 | 4 | 4 | 2020-10-16 | 2023-11-01 |
| Gottheimer and Khanna | 6 | 6 | 3 | 2018-12-10 | 2025-04-04 |
| Austin Scott and any other | 0 | 0 | 0 | — | — |

The Khanna-and-McCaul pair is a chamber rank-one cell in the same-day-trade coincidence screen. Tickers are predominantly mega-capitalization model-portfolio names (PYPL, C, AMZN, GOOGL, BRK.B, MSFT, MU, CMCSA, T, WFC, AMD, HUM, NFLX, DHR, ANET, GM, MS, FIS, TXN). The pair is statistically real but also consistent with shared UBS, Fidelity, or Goldman Sachs separately-managed-account model-portfolio overlap rather than with explicit coordination.

Notable individual same-day cells:

- **2020-10-16**: Gottheimer joint-owner, McCaul dependent-child ($1M–$5M) and McCaul spouse ($250K–$500K) all purchase Chevron (CVX). Two cluster Members same-day energy-prime purchase in the $1M+ bracket.
- **2020-01-08**: Khanna spouse, McCaul spouse, and McCaul dependent-child all purchase Berkshire Hathaway B. Two cluster Members same-day purchase.
- **2023-10-27**: Gottheimer joint-owner, McCaul dependent-child ($100K–$250K) and McCaul spouse ($1M–$5M) all purchase Microsoft. Highest single-pair dollar magnitude.
- **2024-06-21**: Khanna dependent-child, McCaul dependent-child, and McCaul spouse all sell Advanced Micro Devices. Two cluster Members same-day chip-stock sale.
- **2026-02-17**: Khanna spouse and McCaul spouse ($100K–$250K) both sell Humana. High-bracket pharma-payor same-day sale.

Austin Scott is absent from the same-day pair inventory. His 418-transaction portfolio is smaller and more temporally diffuse; the same-day screen does not detect overlap with any of the other three Members. This is not exculpatory — Scott's overlap with respondent is committee-jurisdictional (five Congresses of continuous HSAS co-membership) rather than trade-coincidence.

### 4.1 Asymmetric SMA-disclosure surface — cross-link to Exhibit L

The trade-coincidence asymmetry visible in the Section 4 table — the Khanna-McCaul cell at chamber rank-one with thirty pairs but the Khanna-Scott cell at zero pairs despite Scott's five-consecutive-Congress HSAS co-membership with respondent — has a structural mediator in the asymmetric SMA-disclosure surface that the four cluster Members carry on their PFD page-9 financial-disclosure forms (per the page-9 OCR analysis at Exhibit L).

Three of the four cluster Members carry separately-managed-account or managed-discretionary exposure without a named investment adviser disclosed on PFD page 9. Respondent discloses UBS as the SMA custodian without naming the discretionary investment adviser who exercises trading authority. McCaul discloses brokerage-relationship custodians (the household's principal accounts) without disclosing managed-discretionary or trustee-discretionary status for the family-LP wrappers and dependent-child UTMA accounts that drive the bulk of the household's PTR-disclosed trading activity. Gottheimer discloses non-discretionary trading without naming the investment adviser whose model portfolio his household trades alongside.

Austin Scott is the lone cluster Member who names a specific discretionary investment adviser on his PFD page 9.

**The asymmetric pattern — three Members shielded from named-adviser disclosure, one Member named — mediates the trade-coincidence asymmetry at Section 4.** Same-day same-ticker same-direction pair signal arises with substantial frequency among the three shielded Members (Khanna-McCaul thirty pairs, Gottheimer-McCaul eight pairs, Gottheimer-Khanna six pairs) but does not arise at all between the named-adviser Member (Scott) and any of the three shielded Members. The mediator-mechanism reading is that shared SMA-model-portfolio overlap among un-named advisers — i.e., shared participation in the same UBS, Fidelity, or Goldman Sachs model portfolios without disclosure of the model-portfolio relationship — is a sufficient structural explanation for a substantial fraction of the Section 4 same-day-pair signal, and that the absence of Scott from the same-day-pair inventory is consistent with Scott's named-adviser disclosure foreclosing the mechanism.

This reading does not eliminate the alternative mechanism — shared MNPI-information-flow following committee-jurisdictional briefings — for the residual same-day-pair signal that survives the SMA-model-portfolio explanation, including in particular the high-bracket non-mega-cap pairs and the temporal clustering of pairs around defense-prime and pharma-payor news windows. Both mechanisms can operate concurrently; the asymmetric-SMA-disclosure surface explains why the Khanna-Scott cell is empty despite the strongest MNPI-access overlap in the cluster, and that explanation operates as a partial rather than a complete account of the broader same-day-pair signal. The structural inference for the relief sought at Counts 4 and 7 — that the asymmetric-SMA-disclosure pattern itself is the proper subject of the 5 U.S.C. § 13104(d)(1)(A) and 18 U.S.C. § 208 review — is preserved on either reading.

## 5. Donor-universe overlap

Cluster donor signal splits along party lines:

- **Khanna and Gottheimer** share the crypto-industry and a16z decision-maker tier and both received PROTECT PROGRESS independent expenditures in the 2024 cycle. This is developed in Exhibit J at Section 2 and in the FEC referral.
- **McCaul and Austin Scott** draw on separate Republican donor bases (Texas defense contractors and energy primes for McCaul; Georgia agriculture and defense for Scott). They share no substantive donor overlap with the Khanna and Gottheimer crypto-industry cluster.
- **Cross-party** donor-universe overlap is absent at the detectable level.

## 6. What the cluster shows — and what it does not

The four-Member cluster is not a coordinated trading bloc. There is no evidence that the four Members communicate trading decisions or that a common information-sharing mechanism underlies the aggregate pattern. What they share is structural:

| Dimension | Shared | Not shared |
|---|---|---|
| Total disclosed PTR volume | Top-decile chamber-wide on transaction count for three of four; Austin Scott modest | Order-of-magnitude differences in volume between Khanna (36K) and Scott (418) |
| Committee seats with material non-public-information access | House Armed Services (Khanna-Scott, five Congresses); House Intelligence (Gottheimer-Scott, two Congresses); HSFA Chair (McCaul); HSHM (McCaul plus Gottheimer in 117th only) | No four-way committee overlap; pairs only |
| Defense-prime trading near NDAA enactment | Khanna 14 NDAA-window trades; McCaul 2022-12-14 General Electric purchase 9 days pre-FY23 NDAA; Austin Scott 2020-12-23 spouse General Electric purchase 9 days pre-FY21 NDAA | Distinct NDAA cycles; distinct portfolios |
| Late-filing pattern | Each of the four has at least one disclosure filed more than one year late | Individual compliance rates differ widely |
| Donor profile | Khanna plus Gottheimer: crypto, a16z, and PROTECT PROGRESS axis | McCaul and Scott: Texas and Georgia Republican defense-and-energy axis |

A single-Member investigative framing captures only the Khanna subset of this record. The cluster framing captures a structural common denominator: across two Democrats, two Republicans, three regions, and two parties' donor networks, the same structural condition — active household trading in the jurisdictional sectors to which a Member holds committee-level material non-public-information access — recurs at the investigative top-decile level. The cluster is offered for the limited proposition that **the structural condition this complaint describes is not partisan and is not unique to respondent**; that proposition is a live Anticipated-Response consideration under Section VI of the complaint, not a coordination charge.

## 7. Relationship to Count 4

Within Count 4, the four-Member cluster functions as context for the second-respondent framing of the Gottheimer pair (Exhibit J) and for the PROTECT PROGRESS 20-Democrat slate framing (Exhibit P). If and when standalone complaint packages are assembled against Gottheimer, McCaul, or Scott, the same structural analysis would extend to those Members in their own cases. This exhibit does not itself plead against Gottheimer, McCaul, or Scott; it is offered only for the structural context it supplies to respondent's filing.

---

*Primary-source substrates: House Clerk Periodic Transaction Reports for each of the four Members (drawn from `lake.house_ptr_transactions_canonical`, the amendment-cascade-deduplicated canonical view); House Clerk Financial Disclosure portal Annual PFDs; FEC Schedule A and committee-roster records; Speaker's appointment letters for HLIG roster (118th and 119th Congresses); House and Senate committee rosters for the 115th through 119th Congresses; roll-call records for cited NDAA enactments.*
