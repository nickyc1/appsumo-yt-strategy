#!/usr/bin/env python3
"""Aggregate DG ad performance per video asset for 3 date ranges.

Each video gets:
  perf: { d1: {...}, d7: {...}, d30: {...} }
where each {...} is { spend, imps, clicks, conv, value, roas, n_ads }.
"""
import json
from pathlib import Path
ROOT = Path("/Users/nickchristensen/appsumo-yt-strategy")

RANGES = {
    "d1":  "dg_ad_perf_yesterday.json",
    "d7":  "dg_ad_perf_7d.json",
    "d30": "dg_ad_perf.json",
}

# Load ad → campaign map
with open(ROOT / "ad_campaign_map.json") as f:
    AD_MAP = json.load(f)
CAMPAIGNS = AD_MAP["campaigns"]
AD_TO_CAMP = AD_MAP["ad_to_campaign"]

def aggregate(rows):
    """For each ad, divide its metrics equally among the N video variants
    attached to that ad. DG Video Responsive Ads serve one variant per
    impression based on placement (Shorts vs in-stream vs in-feed),
    but the API doesn't expose per-variant serving, so equal split is
    the most honest approximation."""
    per_video = {}
    max_variants = {}  # asset_id -> max ad-variant count seen (for "1 of N" label)
    campaigns_seen = {}  # asset_id -> set of campaign labels
    for ad in rows:
        cost_total = int(ad.get("metrics.cost_micros", 0)) / 1_000_000
        imps_total = int(ad.get("metrics.impressions", 0))
        clicks_total = int(ad.get("metrics.clicks", 0))
        conv_total = float(ad.get("metrics.conversions", 0))
        val_total = float(ad.get("metrics.conversions_value", 0))
        videos = ad.get("ad_group_ad.ad.demand_gen_video_responsive_ad.videos", []) or []
        n = len(videos)
        if n == 0:
            continue
        # Distribute equally among variants
        cost = cost_total / n
        imps = imps_total / n
        clicks = clicks_total / n
        conv = conv_total / n
        val = val_total / n
        ad_id = str(ad.get("ad_group_ad.ad.id", ""))
        camp_id = AD_TO_CAMP.get(ad_id, "")
        camp_label = CAMPAIGNS.get(camp_id, {}).get("label", "")
        for v in videos:
            asset_path = v.get("asset", "")
            aid = asset_path.split("/")[-1] if asset_path else ""
            if not aid: continue
            p = per_video.setdefault(aid, {"spend": 0, "imps": 0, "clicks": 0, "conv": 0, "value": 0, "n_ads": 0})
            p["spend"] += cost
            p["imps"] += imps
            p["clicks"] += clicks
            p["conv"] += conv
            p["value"] += val
            p["n_ads"] += 1
            max_variants[aid] = max(max_variants.get(aid, 1), n)
            if camp_label:
                campaigns_seen.setdefault(aid, set()).add(camp_label)
    for aid, p in per_video.items():
        p["roas"] = round(p["value"] / p["spend"], 2) if p["spend"] > 0 else 0
        p["spend"] = round(p["spend"], 2)
        p["value"] = round(p["value"], 2)
        p["conv"] = round(p["conv"], 2)
        p["imps"] = round(p["imps"])
        p["clicks"] = round(p["clicks"])
        p["max_variants"] = max_variants.get(aid, 1)
        p["campaigns"] = sorted(campaigns_seen.get(aid, set()))
    return per_video

all_perf = {}
for label, fname in RANGES.items():
    with open(ROOT / fname) as f:
        data = json.load(f)["data"]
    all_perf[label] = aggregate(data)
    total_spend = sum(p["spend"] for p in all_perf[label].values())
    print(f"{label}: {len(all_perf[label])} videos, total spend ${total_spend:,.2f}")

# Merge into all_videos.json
with open(ROOT / "all_videos.json") as f:
    videos = json.load(f)

# Build combined perf per video
matched = 0
for v in videos:
    aid = str(v.get("asset_id", ""))
    combined = {}
    for label in RANGES:
        if aid in all_perf[label]:
            combined[label] = all_perf[label][aid]
    if combined:
        v["perf"] = combined
        matched += 1
    else:
        v["perf"] = None

print(f"\nMatched perf into {matched} of {len(videos)} videos")

with open(ROOT / "all_videos.json", "w") as f:
    json.dump(videos, f, indent=2)
print("Updated all_videos.json with multi-range perf.")
