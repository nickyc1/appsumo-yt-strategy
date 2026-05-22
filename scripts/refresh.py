#!/usr/bin/env python3
"""End-to-end weekly catalog refresh.

1. Exchange refresh_token for an access_token
2. Pull from Google Ads API v21:
   - Daily ad-level perf for last 30 days through yesterday (ad_group_ad)
   - Asset-level perf for yesterday / last 7d / last 30d (ad_group_ad_asset_view)
3. Transform responses to the snake-case dotted format the existing
   build_perf.py expects
4. Save to daily_raw_30d.json + asset_perf_{yesterday,7d,30d}.json
5. Run build_perf.py to regenerate all_videos.json
6. Regenerate daily_perf.json by aggregating segments.date
7. Re-embed both JSON files into index.html
8. Print a summary

Designed to run unattended in GitHub Actions; reads credentials from env vars.
"""
import collections
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 1. Auth + config ────────────────────────────────────────────────────────
CLIENT_ID = os.environ["GOOGLE_ADS_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_ADS_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GOOGLE_ADS_REFRESH_TOKEN"]
DEVELOPER_TOKEN = os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"]
LOGIN_CUSTOMER_ID = os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"]
APPSUMO_CUSTOMER_ID = "8540043636"
CAMPAIGN_IDS = "23554889940, 23594430656"  # ACQ + RET YT DG

today_utc = dt.datetime.utcnow().date()
YESTERDAY = (today_utc - dt.timedelta(days=1)).isoformat()
SEVEN_DAYS_AGO = (today_utc - dt.timedelta(days=7)).isoformat()
THIRTY_DAYS_AGO = (today_utc - dt.timedelta(days=30)).isoformat()
print(f"Refreshing through {YESTERDAY} (yesterday in UTC)")


def get_access_token() -> str:
    """Exchange refresh_token for a short-lived access_token."""
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["access_token"]


# ── 2. GAQL helper ──────────────────────────────────────────────────────────
def gaql(token: str, query: str) -> list[dict]:
    """Run a GAQL searchStream query. Returns a list of result rows."""
    url = f"https://googleads.googleapis.com/v21/customers/{APPSUMO_CUSTOMER_ID}/googleAds:searchStream"
    body = json.dumps({"query": query}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "developer-token": DEVELOPER_TOKEN,
        "login-customer-id": LOGIN_CUSTOMER_ID,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        chunks = json.load(resp)
    rows = []
    for chunk in chunks:
        rows.extend(chunk.get("results", []))
    return rows


# ── 3. Flatten nested API response → MCP-compatible dotted snake_case ─────
def to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def flatten(obj: dict, prefix: str = "") -> dict:
    """Convert nested camelCase JSON to dotted snake_case keys, matching the
    format the MCP returned (which build_perf.py was written against)."""
    flat = {}
    for k, v in obj.items():
        snake_k = to_snake(k)
        new_key = f"{prefix}.{snake_k}" if prefix else snake_k
        if isinstance(v, dict):
            flat.update(flatten(v, new_key))
        elif isinstance(v, list):
            # Preserve arrays as-is (rare for our queries)
            flat[new_key] = v
        else:
            flat[new_key] = v
    return flat


def normalize_rows(rows: list[dict]) -> list[dict]:
    return [flatten(r) for r in rows]


# ── 4. Run queries + save ───────────────────────────────────────────────────
def run_queries():
    token = get_access_token()
    print("✓ access token obtained")

    queries = {
        "daily_raw_30d.json": (
            "SELECT segments.date, metrics.cost_micros, metrics.impressions, "
            "metrics.clicks, metrics.conversions, metrics.conversions_value "
            f"FROM ad_group_ad WHERE campaign.id IN ({CAMPAIGN_IDS}) "
            "AND ad_group_ad.status = 'ENABLED' "
            "AND ad_group_ad.ad.type = 'DEMAND_GEN_VIDEO_RESPONSIVE_AD' "
            f"AND segments.date BETWEEN '{THIRTY_DAYS_AGO}' AND '{YESTERDAY}'"
        ),
        "asset_perf_yesterday.json": (
            "SELECT ad_group_ad_asset_view.asset, ad_group_ad_asset_view.field_type, "
            "ad_group.name, campaign.id, metrics.cost_micros, metrics.impressions, "
            "metrics.clicks, metrics.conversions, metrics.conversions_value "
            f"FROM ad_group_ad_asset_view WHERE campaign.id IN ({CAMPAIGN_IDS}) "
            f"AND segments.date BETWEEN '{YESTERDAY}' AND '{YESTERDAY}' "
            "AND ad_group_ad_asset_view.field_type = 'YOUTUBE_VIDEO' "
            "AND ad_group_ad_asset_view.enabled = TRUE"
        ),
        "asset_perf_7d.json": (
            "SELECT ad_group_ad_asset_view.asset, ad_group_ad_asset_view.field_type, "
            "ad_group.name, campaign.id, metrics.cost_micros, metrics.impressions, "
            "metrics.clicks, metrics.conversions, metrics.conversions_value "
            f"FROM ad_group_ad_asset_view WHERE campaign.id IN ({CAMPAIGN_IDS}) "
            f"AND segments.date BETWEEN '{SEVEN_DAYS_AGO}' AND '{YESTERDAY}' "
            "AND ad_group_ad_asset_view.field_type = 'YOUTUBE_VIDEO' "
            "AND ad_group_ad_asset_view.enabled = TRUE"
        ),
        "asset_perf_30d.json": (
            "SELECT ad_group_ad_asset_view.asset, ad_group_ad_asset_view.field_type, "
            "ad_group.name, campaign.id, metrics.cost_micros, metrics.impressions, "
            "metrics.clicks, metrics.conversions, metrics.conversions_value "
            f"FROM ad_group_ad_asset_view WHERE campaign.id IN ({CAMPAIGN_IDS}) "
            f"AND segments.date BETWEEN '{THIRTY_DAYS_AGO}' AND '{YESTERDAY}' "
            "AND ad_group_ad_asset_view.field_type = 'YOUTUBE_VIDEO' "
            "AND ad_group_ad_asset_view.enabled = TRUE"
        ),
    }

    for fname, q in queries.items():
        rows = gaql(token, q)
        flat = normalize_rows(rows)
        with open(ROOT / fname, "w") as f:
            json.dump({"result": flat}, f)
        total_cost = sum(int(r.get("metrics.cost_micros", 0)) for r in flat) / 1e6
        print(f"  → {fname}: {len(flat)} rows, total spend ${total_cost:,.2f}")


# ── 5. Daily aggregation (per-date totals for the chart) ────────────────────
def build_daily():
    with open(ROOT / "daily_raw_30d.json") as f:
        rows = json.load(f)["result"]
    daily = collections.defaultdict(lambda: {"spend": 0, "imps": 0, "clicks": 0, "conv": 0, "value": 0})
    for r in rows:
        date = r.get("segments.date")
        if not date:
            continue
        daily[date]["spend"]  += int(r.get("metrics.cost_micros", 0)) / 1e6
        daily[date]["imps"]   += int(r.get("metrics.impressions", 0))
        daily[date]["clicks"] += int(r.get("metrics.clicks", 0))
        daily[date]["conv"]   += float(r.get("metrics.conversions", 0))
        daily[date]["value"]  += float(r.get("metrics.conversions_value", 0))
    out = []
    for date in sorted(daily):
        v = daily[date]
        out.append({
            "date": date,
            "spend": round(v["spend"], 2),
            "imps":  v["imps"],
            "clicks": v["clicks"],
            "conv":  round(v["conv"], 2),
            "value": round(v["value"], 2),
            "roas":  round(v["value"] / v["spend"], 2) if v["spend"] > 0 else 0,
        })
    with open(ROOT / "daily_perf.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"✓ daily_perf.json: {len(out)} days ({out[0]['date']} → {out[-1]['date']})")


# ── 6. Run build_perf.py to regenerate all_videos.json ─────────────────────
def run_build_perf():
    print("Running build_perf.py …")
    res = subprocess.run([sys.executable, str(ROOT / "build_perf.py")], cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        print("build_perf.py STDOUT:", res.stdout)
        print("build_perf.py STDERR:", res.stderr)
        raise SystemExit(f"build_perf.py exited {res.returncode}")
    print(res.stdout.strip())


# ── 7. Re-embed JSON into index.html ───────────────────────────────────────
def embed():
    with open(ROOT / "all_videos.json") as f:
        videos = json.load(f)
    with open(ROOT / "daily_perf.json") as f:
        daily = json.load(f)
    with open(ROOT / "index.html") as f:
        html = f.read()
    html = re.sub(r"const DATA = \[.*?\];",
                  "const DATA = " + json.dumps(videos, ensure_ascii=False) + ";",
                  html, count=1, flags=re.DOTALL)
    html = re.sub(r"const DAILY = \[.*?\];",
                  "const DAILY = " + json.dumps(daily, ensure_ascii=False) + ";",
                  html, count=1, flags=re.DOTALL)
    with open(ROOT / "index.html", "w") as f:
        f.write(html)
    print(f"✓ index.html re-embedded ({len(videos)} videos, {len(daily)} days)")


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_queries()
    build_daily()
    run_build_perf()
    embed()
    print("\n✅ Refresh complete.")
