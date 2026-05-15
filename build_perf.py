#!/usr/bin/env python3
"""Aggregate per-asset (per-video) performance for live YT DG videos.

Source: ad_group_ad_asset_view — this is the same view that backs Google
Ads' 'Asset details' UI page. Provides TRUE per-asset metrics (vs the
old approach of dividing ad metrics equally across video variants).
"""
import json
from pathlib import Path
ROOT = Path("/Users/nickchristensen/appsumo-yt-strategy")

RANGES = {
    "d1":  "asset_perf_yesterday.json",
    "d7":  "asset_perf_7d.json",
    "d30": "asset_perf_30d.json",
}

with open(ROOT / "ad_campaign_map.json") as f:
    AD_MAP = json.load(f)
CAMPAIGNS = AD_MAP["campaigns"]


def aggregate(rows):
    per_video = {}
    campaigns_seen = {}
    ad_groups_seen = {}
    for r in rows:
        asset_path = r.get("ad_group_ad_asset_view.asset", "")
        aid = asset_path.split("/")[-1] if asset_path else ""
        if not aid:
            continue
        p = per_video.setdefault(aid, {"spend": 0, "imps": 0, "clicks": 0, "conv": 0, "value": 0})
        p["spend"]  += int(r.get("metrics.cost_micros", 0)) / 1_000_000
        p["imps"]   += int(r.get("metrics.impressions", 0))
        p["clicks"] += int(r.get("metrics.clicks", 0))
        p["conv"]   += float(r.get("metrics.conversions", 0))
        p["value"]  += float(r.get("metrics.conversions_value", 0))
        camp_id = str(r.get("campaign.id", ""))
        camp_full = CAMPAIGNS.get(camp_id, {}).get("full_name", "")
        if camp_full:
            campaigns_seen.setdefault(aid, set()).add(camp_full)
        ag = r.get("ad_group.name", "")
        if ag:
            ad_groups_seen.setdefault(aid, set()).add(ag)

    for aid, p in per_video.items():
        p["roas"] = round(p["value"] / p["spend"], 2) if p["spend"] > 0 else 0
        p["spend"] = round(p["spend"], 2)
        p["value"] = round(p["value"], 2)
        p["conv"] = round(p["conv"], 2)
        p["imps"] = round(p["imps"])
        p["clicks"] = round(p["clicks"])
        p["campaigns"] = sorted(campaigns_seen.get(aid, set()))
        p["ad_groups"] = sorted(ad_groups_seen.get(aid, set()))
    return per_video


all_perf = {}
for label, fname in RANGES.items():
    with open(ROOT / fname) as f:
        raw = json.load(f)
        data = raw.get("result") or raw.get("data") or []
    all_perf[label] = aggregate(data)
    total_spend = sum(p["spend"] for p in all_perf[label].values())
    print(f"{label}: {len(all_perf[label])} videos, total spend ${total_spend:,.2f}")

# Merge into all_videos.json
with open(ROOT / "all_videos.json") as f:
    videos = json.load(f)

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
print("Updated all_videos.json with TRUE per-asset perf (3 date ranges).")
