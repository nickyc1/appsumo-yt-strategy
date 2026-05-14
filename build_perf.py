#!/usr/bin/env python3
"""Aggregate DG ad performance per video asset and merge into all_videos.json.

For each ad in active YT DG campaigns: that ad has 1-5 video assets attached
(horizontal, vertical, square, etc). When an ad serves, all of its videos
get credit. So we sum each ad's metrics across every video it references.

This means: an ad spending $100 with 4 videos attached gives EACH of those
4 videos a $100 spend credit. That's correct — they all contributed to the
ad's serving. If a video appears in multiple ads, its totals reflect the
combined exposure.
"""
import json
import re
from pathlib import Path

ROOT = Path("/Users/nickchristensen/appsumo-yt-strategy")

# The raw GAQL response was inline; load all_videos.json and the DG perf data.
# DG perf data: paste from the latest query (saved here for reproducibility).
with open(ROOT / "dg_ad_perf.json") as f:
    perf_data = json.load(f)["data"]
print(f"Loaded perf data: {len(perf_data)} ads")

# Aggregate per video asset ID
perf_by_video = {}  # asset_id (str) -> {spend, imps, clicks, conv, value, n_ads}
for ad in perf_data:
    cost = int(ad.get("metrics.cost_micros", 0)) / 1_000_000
    imps = int(ad.get("metrics.impressions", 0))
    clicks = int(ad.get("metrics.clicks", 0))
    conv = float(ad.get("metrics.conversions", 0))
    val = float(ad.get("metrics.conversions_value", 0))
    videos = ad.get("ad_group_ad.ad.demand_gen_video_responsive_ad.videos", []) or []
    for v in videos:
        asset_path = v.get("asset", "")
        aid = asset_path.split("/")[-1] if asset_path else ""
        if not aid:
            continue
        p = perf_by_video.setdefault(aid, {"spend": 0, "imps": 0, "clicks": 0, "conv": 0, "value": 0, "n_ads": 0})
        p["spend"] += cost
        p["imps"] += imps
        p["clicks"] += clicks
        p["conv"] += conv
        p["value"] += val
        p["n_ads"] += 1

# Compute ROAS
for aid, p in perf_by_video.items():
    p["roas"] = p["value"] / p["spend"] if p["spend"] > 0 else 0
    p["spend"] = round(p["spend"], 2)
    p["value"] = round(p["value"], 2)
    p["conv"] = round(p["conv"], 2)
    p["roas"] = round(p["roas"], 2)

print(f"\nUnique videos with DG perf data: {len(perf_by_video)}")
spent = [p for p in perf_by_video.values() if p["spend"] > 0]
print(f"  with non-zero spend: {len(spent)}")
print(f"  with zero impressions: {sum(1 for p in perf_by_video.values() if p['imps']==0)}")
print(f"\nTotals:")
print(f"  spend: ${sum(p['spend'] for p in perf_by_video.values()):,.2f}")
print(f"  imps: {sum(p['imps'] for p in perf_by_video.values()):,}")
print(f"  clicks: {sum(p['clicks'] for p in perf_by_video.values()):,}")
print(f"  value: ${sum(p['value'] for p in perf_by_video.values()):,.2f}")

# Merge into all_videos.json
with open(ROOT / "all_videos.json") as f:
    videos = json.load(f)

matched = 0
for v in videos:
    aid = str(v.get("asset_id", ""))
    if aid in perf_by_video:
        v["perf"] = perf_by_video[aid]
        matched += 1
    else:
        v["perf"] = None

print(f"\nMatched perf into {matched} of {len(videos)} videos in catalog")

with open(ROOT / "all_videos.json", "w") as f:
    json.dump(videos, f, indent=2)

# Also write a standalone perf-only JSON
with open(ROOT / "perf_by_video.json", "w") as f:
    json.dump(perf_by_video, f, indent=2)

print("\nDone. all_videos.json and perf_by_video.json updated.")
