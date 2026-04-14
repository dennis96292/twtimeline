#!/usr/bin/env python3
"""Update 2022 events: add verified source_urls."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === Verified URL assignments for 2022 events ===
url_map = {
    "義務役恢復一年":
        "https://news.ltn.com.tw/news/politics/breakingnews/4167390",
    "地方選舉國民黨大勝":
        "https://www.cna.com.tw/news/aipl/202211265003.aspx",
    "金門大橋正式通車":
        "https://www.cna.com.tw/news/ahel/202210300111.aspx",
    "台東連續強震開始":
        "https://news.ltn.com.tw/news/life/breakingnews/4062185",
    "台南警察遭殺害":
        "https://news.ltn.com.tw/news/society/breakingnews/4033933",
    "產業電價調漲":
        "https://www.cna.com.tw/news/ahel/202206275006.aspx",
    "台鐵公司化法案三讀":
        "https://www.cna.com.tw/news/ahel/202205270143.aspx",
    "花蓮規模6.6地震":
        "https://news.ltn.com.tw/news/life/breakingnews/3868495",
    "興達電廠事故全台停電":
        "https://www.cna.com.tw/news/afe/202203085009.aspx",
}

updated = 0
for ev in data:
    if ev['title'] in url_map and not ev.get('source_url', ''):
        ev['source_url'] = url_map[ev['title']]
        updated += 1
        print(f"URL: {ev['date']} {ev['title']}")

print(f"\nUpdated {updated} events with URLs")

events_2022 = [e for e in data if e['date'].startswith('2022')]
with_url = [e for e in events_2022 if e.get('source_url', '')]
print(f"2022: {len(events_2022)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} events.")
