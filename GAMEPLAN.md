# AppSumo YouTube Scaling Plan — One Page

**To:** the agency
**From:** Nick
**Date:** May 2026
**Status:** leadership greenlit — let's scale

---

## The opportunity, in 30 seconds

Google's analysis: peers in business/productivity software spend **98% more on video** than AppSumo. They invest **6 / 100 / 96** indexed across awareness / consideration / action. **AppSumo invests 0 / 0 / 2.** We have an upper-funnel hole and we're missing the "ocean of opportunity" that lives in generic, non-branded search.

We're greenlit to close that gap. The plan below scales YouTube from $58/day Demand Gen to a full-funnel program across Video Reach, Video Views, Demand Gen, and PMax. Target: **$2,500/day total YouTube spend by day 90 at 4x+ blended ROAS.**

---

## What the live data says (last 30d)

**RET is print money. ACQ is leaking budget. Both need creative changes.**

Top 5 ads by absolute value contribution:

| Ad (campaign) | Spend | Conv value | ROAS |
|---|---:|---:|---:|
| BrandJet Video (RET) | $144 | $1,945 | **13.5x** |
| JournalIt (RET) | $91 | $1,174 | **12.9x** |
| Syllabbles Matteo UGC (ACQ)¹ | $9 | $993 | 106.6x¹ |
| MagicFit UGC (RET) | $51 | $467 | 9.2x |
| Motionvid AI UGC (RET) | $35 | $475 | 13.5x |

¹ Small sample but consistent with the pattern — Syllabbles is the only ACQ ad pulling its weight.

**Kill list — these 4 ads burned $516 in 30 days at sub-1x ROAS in ACQ:**

| Ad | Spend | ROAS |
|---|---:|---:|
| Tidycal UGC (ACQ) | $244 | 0.21x |
| Monster May Creator Female (ACQ) | $212 | 0x |
| Monster May Creator Male A (ACQ) | $32 | 0x |
| Resume UP (ACQ) | $28 | 0x |

**14 ads have 0 impressions in 30 days** (algorithm never picked them up). Worth pausing and re-uploading — likely a creative-approval or format issue.

**The deepest insight from the same-creative comparison:**

| Creative | ACQ ROAS | RET ROAS | Gap |
|---|---:|---:|---:|
| Tidycal Evyn UGC | 0x | 19.2x | ∞ |
| Tidycal Ming UGC | 0x | 17.5x | ∞ |
| Motionvid AI UGC | 0x | 13.5x | ∞ |
| BrandJet Video | 1.6x | 13.5x | 8.4x |
| JournalIt | 7.5x | 12.9x | 1.7x |
| MagicFit UGC | 0x | 9.2x | ∞ |

**The same UGC product creative converts 10-20x better in retargeting than in cold prospecting.** This isn't a creative quality problem — it's a creative-audience match problem. **Cold audiences need brand storytelling. Warm audiences need product proof.** Fix: deploy our 82 dormant brand-evergreen videos into ACQ.

Full catalog with active-status badges: https://nickyc1.github.io/appsumo-yt-strategy/

---

## The plan: full-funnel YouTube engine

We're building Google's recommended 3-campaign stack on top of the Demand Gen we already run. **Each layer has its own bid strategy, KPI, and creative type.**

| Layer | Campaign type | Bid strategy | KPI | % of budget |
|---|---|---|---|---:|
| 🔵 **Awareness** | Video Reach (In-Stream) | Target CPM | CPM | 30% |
| ⚪ **Consideration** | Video View Campaigns (Shorts + In-feed) | Max CPV | CPV | 10% |
| ⚫ **Action** | Demand Gen + PMax | Max Conversions | CPA / ROAS | 60% |

Google modeled $500K full-funnel for AppSumo at this split: 42.9M impressions, 2.9M video views, 384 conversions. We're starting smaller and ramping.

---

## Creative & ad structure: 1 + 1 + 1 + many

Per Nate.Google's [Dec 2025 finding](https://twitter.com/Nate_Google_/status/...), Demand Gen now learns fastest with **1 campaign + 1 ad group + 1 ad** per launch — not 3-5 ads stuffed in one ad group. Launch many single-ad campaigns concurrently.

**Cadence target: 5 new 1+1+1 DG campaigns per week.**

Creative production (per [YouTube Growth System artifact](https://claude.ai/public/artifacts/fec2e601-6380-4278-a4e6-b56db075a97c)):
- **10+ hook variants per week**
- **6-8 short-form videos (Shorts/In-feed) per week**
- **1 long-form VSL (2-5 min, in-stream) per week**

VSL structure:
1. **Hook** (first 1-15s) — pattern interrupt, call out the exact viewer
2. **Problem setup** (15-60s) — what's broken (SaaS bloat, expensive tools)
3. **Villain creation** — name the enemy (overpriced enterprise SaaS, agency markups)
4. **Mechanism reveal** — how AppSumo works ("lifetime deals on tools that actually work")
5. **Benefits stack** — what they get
6. **CTA structure** — soft CTA → urgency → AppSumo deal page

---

## Audience targeting (from Google's audience study)

**Demographic:** Males 25-64 (77% male, 1.6x index; top age band 45-54 at 28%). Top 10-20% household income.

**Affinities (Awareness + Consideration):**
- Business Professionals
- Avid Business News Readers
- Value Shoppers
- Avid Investors

**In-Market (Consideration + Action):**
- CRM Solutions
- Email Marketing Services
- Advertising & Marketing Services
- Enterprise Software

**Life Events (Action):**
- Recently Started a Business
- Starting a Business Soon

**Custom Segments (Action):**
- AS / Marketplace - Software Deals (Intent + Websites)

**Geo:** US-first (CA, TX, FL are the top opportunity geos per Google's data — CA indexed 100 @ +11% YoY, TX 69 @ +15%). Add CA/UK/AU after week 4.

**Owned audiences as multiplier (existing in account):**
- Visitors 90 Days (290K) — warm prospects
- BFCM Lookalike (12M) — cold prospecting
- LAL Purchase (Conversion-based) — high-quality cold
- Purchasers GA4 (24K) — RET seed
- 1-Purchase-Only CRM — RET upsell target

---

## 30-day rollout

### Week 1 — Stop the bleeding, scale the winners

**Kill / pause:**
- [ ] Pause the 4 ACQ losers (Tidycal UGC ACQ, Monster May Creator Female ACQ, Monster May Creator Male A ACQ, Resume UP ACQ). Saves $400+/mo of waste.
- [ ] Pause the 14 zero-impression ads. Re-upload them after QC.

**Scale RET (12.1x ROAS, budget-constrained):**
- [ ] Lift `YTDemandGenRETShortsUGCCombined` daily cap from current to **$150/day.**
- [ ] Mirror the 6 Monster May creatives into RET (currently only in ACQ).
- [ ] Add the same 8 RET winners to PMax asset groups (BrandJet, JournalIt, MagicFit, Motionvid, ScaliQ, Tidycal Evyn, Tidycal Ming, Lapis).

**Launch awareness:**
- [ ] Create new campaign: `YT-Awareness-Reach-USCA-Males-2554-BizPros`. Video Reach Campaign. In-stream. Target CPM. KPI = CPM. **$200/day** to start.
- [ ] Audience: Males 25-54, Affinity: Business Professionals + Avid Business News.
- [ ] Creatives: 3 long-form brand evergreen pieces (start with "About AppSumo & Why Entrepreneurs Love Us!", "How AppSumo Works", "Grow Your Business With Noah Kagan" — all on YouTube channel already, just need to register them as ads).

### Week 2 — Launch the consideration layer + fix ACQ

**Consideration (new):**
- [ ] Create `YT-Consideration-VVC-USCA-InMarketSaaS-Shorts`. Video View Campaign (Shorts-only — only available format for VVC). Max CPV bid. KPI = CPV (target <$0.05).
- [ ] Audience: In-Market for CRM Solutions, Email Marketing, Enterprise Software + Life Event "Recently Started a Business."
- [ ] Creatives: 6 short-form videos (60-90s) — mix of brand evergreen + top product UGC reformatted vertical. **$100/day.**

**Fix ACQ with brand-evergreen creative (1+1+1 structure):**
- [ ] Launch 8 individual 1+1+1 ACQ campaigns, one per evergreen video:
  1. About AppSumo & Why Entrepreneurs Love Us!
  2. How AppSumo Works
  3. How AppSumo gets you insane deals on software
  4. AppSumo Plus Benefits
  5. Grow Your Business With Noah Kagan
  6. Keys to Success: Validating your Million Dollar Idea
  7. Building a 6 Figure Business with AppSumo
  8. AppSumo Success Story - Documentary Promo Video
- [ ] Each: $25/day budget cap, Max Conversions, target audience = BFCM Lookalike + Visitors 90 Days, EXCLUDE purchasers.
- [ ] **Total new ACQ spend: $200/day** (replaces the killed losers, net +$170/day).

### Week 3 — Optimize, kill, double down

**Apply kill rules:**
- [ ] Pause any DG ad with **<20% view-through after 5,000 impressions.**
- [ ] Pause any DG ad with **<1x ROAS after $50 in spend.**

**Double winners:**
- [ ] Identify top 2 hooks across all live ads. Pour budget there (+50%).
- [ ] Launch 8 more 1+1+1 campaigns: creative variants (hook swap, angle swap) of winning hooks.

**Measurement:**
- [ ] Set up Search Lift Study on the Video Reach campaign.
- [ ] Check Google Search Console for branded search lift.
- [ ] Pull Cross-Network Impact report.

### Week 4 — Scale & expand

- [ ] Top performing campaigns: **lift budgets +20%** (per artifact).
- [ ] Duplicate winning ad groups into new geos: CA-only, then TX, then FL, then UK/AU.
- [ ] Build new lookalikes from buyer segments: BrandJet buyers, JournalIt buyers (new fast-purchase signals).
- [ ] Run **GeoX held-out test** in 2 control markets to validate incrementality.
- [ ] Lock in **weekly creative production cadence** with the creative team (10 hooks, 6-8 shorts, 1 VSL per week).

---

## Targets

| Day | YT spend/day | Mix (Aw/Cn/Ac) | Blended ROAS target |
|---|---:|---|---:|
| Today | $58 (DG only) | 0 / 0 / $58 | 5.6x |
| Day 30 | **$650** | $200 / $100 / $350 | 4x |
| Day 60 | **$1,300** | $400 / $150 / $750 | 4x |
| Day 90 | **$2,500** | $750 / $250 / $1,500 | 3.5x |

ROAS floor declines as we climb the volume curve and add upper-funnel (which doesn't show direct ROAS — measured via Brand Lift, Search Lift, GeoX). At day 90 we expect AppSumo investment indexed at ~30 awareness / ~10 consideration / ~60 action (vs peers' 6/100/96 — still under-indexed on consideration but closing the gap).

Per Google: customers spending 8-20% of total Google Ads budget on Demand Gen see **-5% account CPA and +12% account conversions**. At $2.5K/day YT against the broader Google Ads spend, we hit that band.

---

## Weekly cadence — agency reports every Monday

Standing agenda. 15 minutes max.

1. **Top 5 ads by spend, per campaign, with ROAS** — both DG and PMax
2. **Impression share lost to budget** for each campaign (anywhere we're capped)
3. **Kill list** — what got paused this week, why
4. **Launch list** — what shipped this week (count + ad groups)
5. **Creative pipeline** — what's coming next week (hooks, shorts, VSL)
6. **Upper-funnel signals** — branded search trend, Search Console impressions

---

## Why this works

- **Google's data validates the structure.** Their $500K modeled scenario assumes exactly this 30/10/60 split and projects 384 conversions/mo at $777 CPA on Demand Gen alone.
- **Our own data validates the creative thesis.** Same UGC creative does 10-20x better in RET than in ACQ. The fix isn't "more UGC" — it's brand evergreen for cold pools.
- **The 1+1+1 structure is the new DG meta.** Nate.Google confirms it; we adopt it from day 1.
- **We already own the assets.** 82 brand evergreen videos sit dormant. 273 unique YT videos already in PMax. We don't need to produce a backlog before we scale — we need to deploy what we have.

---

## What I need from the agency this week

1. **Confirm receipt + estimated start date.** Anything blocking?
2. **Pause confirmation** on the 4 killed ads (with screenshots).
3. **Awareness campaign live by Friday** at $200/day.
4. **RET cap lift confirmed** ($30/day → $150/day) and live.

---

*Live catalog of every video in the account, with active-status flags: https://nickyc1.github.io/appsumo-yt-strategy/*
*Live ad-performance breakdown updated weekly via the Google Ads API.*
