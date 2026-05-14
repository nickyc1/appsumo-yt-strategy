# AppSumo YouTube Video Asset Catalog + Demand Gen Strategy

Live, browsable catalog of every YouTube video asset in the AppSumo Google Ads account, with categorization (deal-specific vs evergreen vs UGC vs seasonal) and active-campaign status. Plus a concise scaling plan for the agency.

## What's in here

- **[`index.html`](./index.html)** — self-contained, browsable catalog of all 2,805 YouTube videos. Filter by bucket, search by title, click to open on YouTube. Shows which are currently running in DG vs PMax. Open it directly in a browser, no server needed.
- **[`STRATEGY.md`](./STRATEGY.md)** — 4-week agency-facing plan for scaling YouTube Demand Gen from $58/day → $250/day at 6x+ ROAS.
- **`all_videos.json`** — full categorized dataset (raw, machine-readable).
- **`summary.json`** — bucket counts + flag counts + samples.
- **`categorize_videos.py`** — script that produces the JSON files from a raw Google Ads `asset` query.
- **`pmax_active_videos.json` / `dg_active_videos.json`** — raw asset linkage data used to compute the "currently running" badges.

## How to host on GitHub Pages

```bash
# From this directory:
git init
git add .
git commit -m "AppSumo YouTube catalog + DG strategy"
git remote add origin git@github.com:<user>/appsumo-yt-strategy.git
git branch -M main
git push -u origin main

# In GitHub: Settings → Pages → Source: "Deploy from branch", branch: main, folder: /
# Catalog goes live at https://<user>.github.io/appsumo-yt-strategy/
```

## How to refresh the catalog

The catalog reflects a point-in-time snapshot. To refresh:

1. Re-run the GAQL query for all YouTube video assets in the AppSumo account.
2. Re-run the GAQL queries for active DG ads + active PMax YouTube assets.
3. Run `python3 categorize_videos.py` to regenerate `all_videos.json` and `summary.json`.
4. Re-embed the JSON into `index.html` (one substitution of the `__DATA_PLACEHOLDER__` token).

## Quick facts (snapshot)

- **2,805** YouTube videos in the account
- **324** currently used in an active campaign (12%)
- **2,481** dormant (88%)
- **82** brand evergreen videos — **0 currently running**
- **60** unique videos across the two active YouTube Demand Gen campaigns
- **273** unique videos across active Performance Max campaigns

See [`STRATEGY.md`](./STRATEGY.md) for what to do about it.
