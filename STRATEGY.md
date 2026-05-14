# AppSumo Demand Gen Scaling Plan — YouTube + Gmail

**Prepared for:** Rax Digital × AppSumo Demand Gen agency partner
**Account:** AppSumo (Google Ads customer 8540043636) under Rax Digital MCC (3661234611)
**Date:** May 2026
**Period covered by current state:** Last 30 days

---

## TL;DR

We have a **spend velocity problem, not a creative problem.** YouTube Demand Gen is spending **$58/day** with 60+ unique enabled creatives and a 12.1x ROAS retargeting campaign that's budget-constrained. We have **2,805 YouTube videos in the account** and **82 evergreen brand pieces currently unused.** This plan ramps YouTube DG to $250/day in 30 days while maintaining 6x+ blended ROAS, then to $1,000/day by day 90 if signals hold.

---

## What's actually running today

| Campaign | Format | Status | 30d Spend | ROAS |
|---|---|---|---:|---:|
| `YTDemandGenRETShortsUGCCombined` | YouTube Shorts (Retargeting) | ENABLED | $903 | **12.1x** |
| `YTDemandGenACQUGCCombined` | YouTube (Prospecting/ACQ) | ENABLED | $823 | 2.4x |
| `GmailDemandGenMissingDeals` | Gmail | ENABLED | $1,208 | 12.1x |
| `GmailDemandGenNewCreative` | Gmail | ENABLED | $105 | 21.3x |

**Total DG: $3,039 over 30 days (~$100/day). YouTube DG: $1,726 (~$58/day).** This is a pilot, not a scaled program.

---

## The audience setup (verified)

**ACQ (campaign 23554889940 — prospecting):**
- **Combined UGC ad group:** BFCM Top Audiences Lookalike (12M-record lookalike) — broad cold targeting
- **Monster May ad group:** 90-day visitors + lookalikes of all-time purchasers, with **negative list exclusion of existing email purchasers** + custom Search-intent audiences ("Software Deal Intent", "Featured Deal Intent")

**RET (campaign 23594430656 — retargeting/repeat):**
- Both ad groups target the actual purchaser list (24K from GA4), 1-purchase-only CRM segment, and 90-day visitors
- Uses the "CA-1PurchaseOnly + 90 Day Visitor + 540 Purchaser" combined Google audience

**The segmentation is sound.** ACQ excludes buyers (correct), RET includes them (correct). The reason ACQ is converting at 2.4x while RET hits 12.1x is **not** the audience — it's that the cold ACQ pool has higher acquisition cost by definition, and we have **the wrong creative mix in it.** Cold audiences need brand/storytelling creative; we're feeding ACQ exclusively product-UGC clips.

---

## Creative inventory — the smoking gun

Across the AppSumo Google Ads account we have **2,805 YouTube video assets.** Categorization:

| Bucket | Total | Currently running | % running |
|---|---:|---:|---:|
| Deal-specific (product/partner) | 2,393 | 255 | 10.7% |
| Campaign / seasonal (BF, Sumo Day, Monster May…) | 156 | 12 | 7.7% |
| UGC / creator | 119 | 57 | **47.9%** |
| **Brand evergreen (AppSumo Plus, Noah, Success Stories, How AppSumo Works)** | **82** | **0** | **0.0%** |
| Legacy "X Review on AppSumo" (2017–2020) | 15 | 0 | 0.0% |
| Dead / no title | 40 | 0 | 0.0% |

**Two things stand out:**
1. **88% of our video library (2,481 videos) is dormant.** Most are product-deal videos for deals that have likely expired.
2. **The 82 evergreen brand videos — our most reusable, never-expires asset class — has 0% utilization.** These are exactly what ACQ (cold) is starving for.

A browsable catalog of all 2,805 videos with active-status badges is at [`index.html`](./index.html).

---

## The plan — 4 weeks, clear actions

### Week 1 — Stop wasting ACQ budget on losing creatives

**Agency tasks:**
1. Pull ad-level performance for `YTDemandGenACQUGCCombined` (last 30 days). For each of the 31 enabled ads, list: impressions, clicks, conversions, conv value, ROAS.
2. **Pause every ad in ACQ with <1x ROAS and >5,000 impressions.** Concentrate spend on the 2-3 that are working.
3. Move the 6 Monster May creatives into `YTDemandGenRETShortsUGCCombined`. They're currently only in ACQ + Gmail — duplicating into RET adds proven creative to our highest-ROAS campaign.

**Budget change:** Hold YT DG total at $58/day this week. Reallocate, don't add.

### Week 2 — Deploy the dormant evergreen pile into ACQ

ACQ is cold-audience prospecting. Brand storytelling beats product-UGC for cold pools. We have 82 brand evergreen videos sitting unused.

**Agency tasks:**
1. **Add a new ad group to YT ACQ: `Brand Evergreen ACQ`.** Same audience targeting as Combined UGC, but a different creative bucket.
2. Launch 8 ads in this new ad group from the brand_evergreen bucket. Suggested starting set (from the catalog):
   - "About AppSumo & Why Entrepreneurs Love Us!"
   - "How AppSumo Works"
   - "How AppSumo gets you insane deals on software"
   - "AppSumo Plus Benefits"
   - "Grow Your Business With Noah Kagan"
   - "Keys to Success: Validating your Million Dollar Idea"
   - "Building a 6 Figure Business with AppSumo"
   - "AppSumo Success Story - Documentary Promo Video"
3. **Budget for this ad group: $50/day for 14 days.** Total YT DG goes from $58 → $108/day.

**Expected outcome:** If even half of these creatives match cold-audience intent, ACQ ROAS climbs from 2.4x toward the 4-6x range as winners surface.

### Week 3 — Break the budget ceiling on RET

RET is doing 12.1x ROAS on $30/day. This is print-money territory until impression share caps out.

**Agency tasks:**
1. Confirm `search_impression_share` and `search_lost_top_impression_share_budget` for `YTDemandGenRETShortsUGCCombined` over last 14 days.
2. If `impression_share_lost_to_budget > 10%`: lift RET daily budget from current to **$150/day.** Hold for 7 days.
3. Watch the curve: ROAS should remain >8x at $150/day. If it drops below 6x, hold; if it stays >8x, lift to $300/day in week 4.

### Week 4 — Restructure for ongoing testing

Both YT DG campaigns currently use one big "Combined UGC" ad group + Monster May. That's a single creative pool feeding a single audience. To scale, we need **dedicated ad groups per creative type per campaign** so the algorithm can test apples to apples.

**Target structure for each YT DG campaign:**
- Ad group A: **UGC** (current "Combined UGC" / "JR UGC Video")
- Ad group B: **Campaign/seasonal** (Monster May, future Sumo Day, BF)
- Ad group C: **Brand Evergreen** (new, from week 2)
- Ad group D: **Deal-specific — active partners only** (rotated based on what's in market)

**Agency tasks:**
1. Restructure both campaigns by week's end.
2. Add a **creative refresh cadence: 4 new ads per ad group per month.**
3. Establish a kill rule: any ad with <0.5x ROAS after 5,000 impressions gets paused.

---

## Targets

| Milestone | YT DG spend/day | Blended YT DG ROAS | Trigger to advance |
|---|---:|---:|---|
| Today | $58 | 5.6x | — |
| Day 30 | $250 | 6x+ | RET impression share <80% lost to budget |
| Day 60 | $500 | 5x+ | Ad-group structure live, 4 buckets each |
| Day 90 | $1,000 | 4x+ | Sustained 5x at Day 60 |

ROAS floor declines as we scale (expected — we're climbing the volume curve). Floor at $1K/day = 4x is still healthy on AppSumo's margins.

---

## Weekly checkpoint questions for the agency

Standing agenda for the weekly call:

1. **Top 5 ads by spend** in YT ACQ and YT RET — with ROAS each
2. **Impression share lost to budget** for both YT DG campaigns
3. **What creative shipped this week** — to which ad group, why
4. **Pause/kill list** — which ads were paused this week and why
5. **Next week's planned changes** — budget moves, structure changes, new creative

---

## Specific creative deployment recommendations

From the catalog at [`index.html`](./index.html), filter by:

- **`brand_evergreen` + dormant** → 82 candidates for the new Brand Evergreen ad group in Week 2. Start with the 8 listed above.
- **`campaign_seasonal` + dormant** → 144 stale moment-based creatives. Most are unusable now, but search for "Sumo Day" or upcoming-moment terms to find pieces to re-deploy at the right time.
- **`deal_specific` + dormant + active partner match** → recyclable when a partner re-features in current promotions.
- **`deal_legacy_review`** → archive. The 2017–2020 "X Review on AppSumo" format isn't worth re-deploying.
- **`dead_or_unknown`** → 40 videos with no title (private/deleted on YouTube). Skip.

---

## Appendix: data sources

All numbers in this document were pulled live from the Google Ads API on May 13, 2026. The catalog page uses the same data. To refresh:
- Run the `categorize_videos.py` script in this folder against a fresh `asset` query.
- The cross-reference for "currently active" comes from two API queries: enabled DEMAND_GEN_VIDEO_RESPONSIVE_AD videos in enabled DG campaigns, plus enabled YouTube assets in active PMax asset groups.
