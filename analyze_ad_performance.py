#!/usr/bin/env python3
"""Compute winner/loser/dormant buckets for currently-enabled YT DG ads."""
import json
ROWS = [
    # campaign_short, ad_group_short, ad_name, cost, imps, clicks, conv, value
    ("RET","JR UCG","Tidycal UGC",444.90,792407,4326,5.29,596.51),
    ("ACQ","Combined UGC","Tidycal UGC",243.56,627409,3354,0.46,50.75),
    ("ACQ","Monster May","Creator Female",211.72,552865,3317,0,0),
    ("RET","JR UCG","BrandJet Video",144.06,123496,509,15.91,1945.12),
    ("ACQ","Combined UGC","BrandJet Video",117.95,67994,378,1.14,191.00),
    ("RET","JR UCG","JournalIt",91.33,75116,315,10.81,1173.53),
    ("RET","JR UCG","ScaliQ Video",66.87,29262,121,5.10,479.32),
    ("RET","JR UCG","MagicFit UGC",50.77,12220,97,6.76,467.40),
    ("RET","JR UCG","Motionvid AI UGC",35.30,8195,58,5.43,474.79),
    ("RET","JR UCG","Pixefy Dave Swift",32.27,12128,105,1.79,68.59),
    ("ACQ","Monster May","Creator Male A",31.76,66547,253,0,0),
    ("ACQ","Combined UGC","Resume UP",28.39,31153,103,0,0),
    ("ACQ","Combined UGC","JournalIt",22.38,34411,178,1.10,166.75),
    ("ACQ","Combined UGC","ScaliQ Video",13.54,21570,132,0,0),
    ("RET","JR UCG","Resume UP",12.47,8052,26,0.89,102.19),
    ("RET","JR UCG","Tidycal Evyn UGC",11.81,5550,37,5.30,226.99),
    ("ACQ","Combined UGC","Syllabbles Matteo UGC",9.31,10189,62,2.00,992.84),
    ("RET","JR UCG","Tidycal Ming UGC",8.72,5529,39,3.37,152.90),
    ("RET","JR UCG","Lapis",8.71,4126,22,1.70,229.62),
    ("ACQ","Combined UGC","vidBoard Matteo UGC",8.30,14027,79,0,0),
    ("ACQ","Combined UGC","Lapis",6.54,6581,23,0.17,43.59),
    ("ACQ","Combined UGC","Tidycal UGC (dup)",5.94,14002,88,0,0),
    ("RET","JR UCG","Tidycal Sam UGC",5.90,1680,8,0.65,63.43),
    ("ACQ","Combined UGC","Tidycal Ming UGC",5.41,15047,71,0,0),
    ("ACQ","Monster May","Godzilla Teaser",4.72,10014,64,0,0),
    ("ACQ","Combined UGC","Tidycal Sam UGC",4.39,4918,12,0,0),
    ("ACQ","Combined UGC","Tidycal Evyn UGC",4.00,6439,27,0,0),
    ("RET","JR UCG","Tidycal UGC (dup)",3.97,682,5,1.43,245.83),
    ("RET","JR UCG","Tidycal UGC (dup2)",3.86,634,4,0,0),
    ("RET","Monster May","Creator Male A",3.16,2560,8,0,0),
    ("ACQ","Combined UGC","Pixefy Dave Swift",2.42,7739,42,0.13,7.80),
    ("ACQ","Monster May","Creator Male B",2.07,6875,46,0,0),
    ("RET","JR UCG","vidBoard Matteo UGC",1.68,643,4,0,0),
    ("ACQ","Combined UGC","Blip AI UGC",1.60,2128,13,0,0),
    ("RET","JR UCG","Syllabbles Matteo UGC",1.18,351,3,0,0),
    ("ACQ","Monster May","General Graphic",1.18,4945,32,0,0),
    ("ACQ","Monster May","Featured Deals",0.90,3675,31,0,0),
    ("ACQ","Combined UGC","Tidycal UGC (dup2)",0.47,643,5,0,0),
    ("ACQ","Combined UGC","Headway Video UGC",0.40,976,3,0,0),
    ("RET","Monster May","Godzilla Teaser",0.38,623,2,0,0),
    ("ACQ","Combined UGC","Remio Video UGC",0.25,584,3,0,0),
    ("RET","Monster May","Creator Male B",0.20,139,1,0,0),
    ("RET","Monster May","Featured Deals",0.19,128,2,0,0),
    ("RET","Monster May","Creator Female",0.17,143,1,0,0),
    ("RET","JR UCG","Blip AI UGC",0.12,87,0,0,0),
    ("ACQ","Combined UGC","MagicFit UGC",0.09,203,1,0,0),
    ("ACQ","Combined UGC","Motionvid AI UGC",0.05,55,0,0,0),
    ("RET","Monster May","General Graphic",0.03,64,0,0,0),
]
# Add 14 ads with zero impressions
ZEROS = [
    ("ACQ","Combined UGC","Alter AliMirza UGC"),
    ("ACQ","Combined UGC","Remio Ali Mirza UGC"),
    ("ACQ","Combined UGC","Adle Video"),
    ("ACQ","Combined UGC","Subscribr Video"),
    ("ACQ","Combined UGC","Subscribr Video Raffaele"),
    ("ACQ","Combined UGC","Pixefy Video UGC"),
    ("RET","JR UCG","Remio Ali Mirza UGC"),
    ("RET","JR UCG","Subscribr Video"),
    ("RET","JR UCG","Adle Video"),
    ("RET","JR UCG","Alter AliMirza UGC"),
    ("RET","JR UCG","Headway Video UGC"),
    ("RET","JR UCG","Remio Video UGC"),
    ("RET","JR UCG","Subscribr Video Raffaele"),
    ("RET","JR UCG","Pixefy Video UGC"),
]

print(f"\n{'='*70}\nFULL AD PERFORMANCE (live YT DG ads, LAST_30_DAYS)\n{'='*70}\n")
total_spend = sum(r[3] for r in ROWS)
total_val = sum(r[7] for r in ROWS)
print(f"Total spend across all 49 served ads: ${total_spend:,.2f}")
print(f"Total conv value: ${total_val:,.2f}")
print(f"Blended ROAS: {total_val/total_spend:.2f}x")
print(f"Ads with 0 impressions (zero-served): {len(ZEROS)}")
print()

# Sort by ROAS desc, with $5+ spend threshold
candidates = [(r, r[7]/r[3] if r[3] else 0) for r in ROWS if r[3] >= 5]
candidates.sort(key=lambda x: -x[1])

print(f"\n{'='*70}\nTOP WINNERS (ROAS, min $5 spend)\n{'='*70}")
print(f"{'Camp':<5}{'Ad':<28}{'Spend':>10}{'Conv':>8}{'Value':>10}{'ROAS':>8}")
for r, roas in candidates[:12]:
    print(f"{r[0]:<5}{r[2][:27]:<28}{'$'+f'{r[3]:.2f}':>10}{r[6]:>8.2f}{'$'+f'{r[7]:.2f}':>10}{roas:>7.2f}x")

print(f"\n{'='*70}\nLOSERS (high spend, ROAS < 1x)\n{'='*70}")
losers = [(r, r[7]/r[3] if r[3] else 0) for r in ROWS if r[3] >= 5 and (r[7]/r[3] if r[3] else 0) < 1]
losers.sort(key=lambda x: -x[0][3])  # by spend desc
for r, roas in losers:
    print(f"{r[0]:<5}{r[2][:27]:<28}{'$'+f'{r[3]:.2f}':>10}{r[6]:>8.2f}{'$'+f'{r[7]:.2f}':>10}{roas:>7.2f}x")

print(f"\n{'='*70}\nZERO-IMPRESSION ADS (algorithm not serving)\n{'='*70}")
from collections import Counter
zc = Counter([z[0] for z in ZEROS])
print(f"ACQ: {zc['ACQ']} ads | RET: {zc['RET']} ads")
acq_zeros = sorted({z[2] for z in ZEROS if z[0]=='ACQ'})
ret_zeros = sorted({z[2] for z in ZEROS if z[0]=='RET'})
print(f"  unique creatives never served: {sorted(set(acq_zeros) | set(ret_zeros))}")

# Same creative ACQ vs RET comparison
print(f"\n{'='*70}\nSAME CREATIVE, ACQ vs RET (where applicable)\n{'='*70}")
by_name = {}
for r in ROWS:
    by_name.setdefault(r[2], {})[r[0]] = r
for name in sorted(by_name):
    if 'ACQ' in by_name[name] and 'RET' in by_name[name]:
        a = by_name[name]['ACQ']; r = by_name[name]['RET']
        a_roas = a[7]/a[3] if a[3] else 0
        r_roas = r[7]/r[3] if r[3] else 0
        if a[3] >= 5 or r[3] >= 5:
            print(f"  {name:<26} ACQ ROAS {a_roas:>5.2f}x  vs  RET ROAS {r_roas:>5.2f}x")
