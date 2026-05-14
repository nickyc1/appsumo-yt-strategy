#!/usr/bin/env python3
"""Categorize AppSumo's 2,805 YouTube video assets into buckets so we know what's
deal-specific (and likely stale) vs evergreen vs UGC vs campaign-tied.

Reads the saved GAQL result of `SELECT asset.id, asset.name, asset.youtube_video_asset.*
FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'` and writes:
  - all_videos.json   — full categorized dataset
  - summary.json      — per-bucket counts + samples
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SRC = Path("/Users/nickchristensen/.claude/projects/-Users-nickchristensen/10fb1df6-112e-4ab4-b8e3-8aaf74529f9e/tool-results/mcp-plugin_google-ads-manager_google-ads-execute_gaql-1778705018260.txt")
OUT_DIR = Path("/Users/nickchristensen/appsumo-yt-strategy")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Heuristic rules — order matters (first match wins for primary category)
CAMPAIGN_PATTERNS = re.compile(
    r"\b(black\s*friday|bfcm|cyber\s*monday|sumo\s*day|sumoday|monster\s*may|"
    r"last\s*call|giveaway|year[-\s]?end|holiday|new\s*year|easter|"
    r"birthday|anniversary|valentine|halloween|prime\s*day|"
    r"summer\s*sale|spring\s*sale|aiweek|ai\s*week|bundle\s*sale)\b",
    re.IGNORECASE,
)

UGC_PATTERNS = re.compile(
    r"\b(ugc|creator|testimonial|ali\s*mirza|matteo|raffaele|evyn|sam|ming|"
    r"dave\s*swift|user[-\s]?generated|founder\s*story|partnership)\b",
    re.IGNORECASE,
)

# Specific brand/evergreen phrases — must be the *topic* of the video, not just a stray "AppSumo" mention.
BRAND_PATTERNS = re.compile(
    r"\b("
    r"about\s*appsumo|how\s*appsumo\s*(?:started|works|gets)|why\s*(?:entrepreneurs|appsumo)|"
    r"appsumo\s*(?:plus|originals|success\s*story|stack\s*codes?)|sumo\s*plus|"
    r"plus\s*(?:benefits?|member)|insane\s*deals|"
    r"noah\s*kagan|grow\s*your\s*business\s*with\s*noah|keys\s*to\s*success|"
    r"6[-\s]?figure|7[-\s]?figure|8[-\s]?figure|million\s*dollar|"
    r"self[-\s]?list(?:ing|er)|sell\s*on\s*appsumo|appsumo\s*marketplace|"
    r"founder\s*story|building\s*a\s*business|how\s*i\s*(?:made|created|run|built)"
    r")\b",
    re.IGNORECASE,
)

# "Foo Review on AppSumo" — the classic 2017–2020 deal-review format (mostly stale now)
DEAL_REVIEW = re.compile(r"\breview\s*on\s*appsumo\b", re.IGNORECASE)

# Noah-channel content uploaded to ad account but really organic YouTube content
NOAH_EDU = re.compile(
    r"\b(tim\s*ferriss|secrets?\s*to\s*success|marketing\s*strateg(?:y|ies)|"
    r"validating\s*your|how\s*to\s*make\s*\$|"
    r"how\s*to\s*create\s*digital|how\s*to\s*start\s*a\s*business)\b",
    re.IGNORECASE,
)

# Suffix tags that indicate a specific deal-attached creative
DEAL_HINTS = re.compile(
    r"\b(video|ad|hero|promo|teaser|product\s*demo|walkthrough|"
    r"explainer|how[-\s]to|hero\s*demo|launch|featured)\b",
    re.IGNORECASE,
)


def bucket(title: str, name: str) -> dict:
    """Return primary bucket + secondary flags. Empty-title videos are 'unknown'."""
    t = (title or "").strip()
    n = (name or "").strip()
    text = f"{t} {n}".strip()

    flags = []
    if not t:
        return {"primary": "dead_or_unknown", "flags": ["no_title"]}

    # Highest specificity first
    if DEAL_REVIEW.search(text):
        primary = "deal_legacy_review"
        flags.append("legacy_format")
    elif CAMPAIGN_PATTERNS.search(text):
        primary = "campaign_seasonal"
        flags.append("campaign_tied")
    elif UGC_PATTERNS.search(text):
        primary = "ugc_creator"
        if "testimonial" in text.lower():
            flags.append("testimonial")
    elif BRAND_PATTERNS.search(text):
        primary = "brand_evergreen"
    elif NOAH_EDU.search(text):
        primary = "brand_evergreen"
        flags.append("noah_educational")
    else:
        # Default: a specific product/deal video
        primary = "deal_specific"

    # Add secondary flags
    if DEAL_HINTS.search(text) and primary == "deal_specific":
        flags.append("has_deal_hint")
    if re.search(r"\b(short|shorts|9x16|vertical|portrait)\b", text, re.IGNORECASE):
        flags.append("vertical_short")
    if re.search(r"\b(1x1|square)\b", text, re.IGNORECASE):
        flags.append("square")
    if re.search(r"\b(16x9|horizontal|landscape)\b", text, re.IGNORECASE):
        flags.append("horizontal")

    return {"primary": primary, "flags": flags}


def main():
    print(f"Reading {SRC}", file=sys.stderr)
    with open(SRC) as f:
        data = json.load(f)
    rows = data.get("data", data) if isinstance(data, dict) else data

    out = []
    buckets = Counter()
    flag_counts = Counter()
    samples = defaultdict(list)

    for r in rows:
        asset_id = r.get("asset.id")
        name = r.get("asset.name", "") or ""
        yt_id = r.get("asset.youtube_video_asset.youtube_video_id", "") or ""
        title = r.get("asset.youtube_video_asset.youtube_video_title", "") or ""
        b = bucket(title, name)
        entry = {
            "asset_id": asset_id,
            "yt_id": yt_id,
            "title": title,
            "name": name,
            "primary": b["primary"],
            "flags": b["flags"],
            "yt_url": f"https://youtube.com/watch?v={yt_id}" if yt_id else "",
        }
        out.append(entry)
        buckets[b["primary"]] += 1
        for fl in b["flags"]:
            flag_counts[fl] += 1
        if len(samples[b["primary"]]) < 12:
            samples[b["primary"]].append({"title": title, "yt": yt_id})

    # Write all_videos.json
    with open(OUT_DIR / "all_videos.json", "w") as f:
        json.dump(out, f, indent=2)

    # Write summary
    summary = {
        "total": len(out),
        "by_bucket": dict(buckets.most_common()),
        "by_flag": dict(flag_counts.most_common()),
        "samples": dict(samples),
    }
    with open(OUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print human summary
    print(f"\nTotal videos: {len(out)}")
    print("\nBy bucket:")
    for b, n in buckets.most_common():
        pct = 100 * n / len(out)
        print(f"  {b:<22} {n:>5}  ({pct:>5.1f}%)")
    print("\nBy flag:")
    for fl, n in flag_counts.most_common():
        print(f"  {fl:<22} {n:>5}")

    print("\nSamples per bucket:")
    for b in buckets:
        print(f"\n  [{b}]")
        for s in samples[b][:6]:
            t = s["title"][:80] if s["title"] else "(no title)"
            print(f"    - {t}")


if __name__ == "__main__":
    main()
