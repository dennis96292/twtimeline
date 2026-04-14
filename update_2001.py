#!/usr/bin/env python3
"""Update 2001 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "民進黨成國會最大黨":
        "https://zh.wikipedia.org/zh-tw/2001年中華民國立法委員選舉",
    "納莉颱風重創北台灣":
        "https://zh.wikipedia.org/zh-tw/颱風納莉_(2001年)",
    "桃芝颱風重創中部":
        "https://zh.wikipedia.org/zh-tw/颱風桃芝_(2001年)",
    "核四工程宣布復工":
        "https://zh.wikipedia.org/zh-tw/核四公投",
    "釋字520號公布":
        "https://zh.wikipedia.org/zh-tw/釋字第520號解釋",
}

# Events to REMOVE: borderline/trivial/routine
remove_titles = {
    "台灣獲准加入WTO",        # Procedural approval step; 台灣正式加入WTO in 2002 is the landmark
    "世界盃棒球賽在台舉行",   # International sports hosting; not a permanent landmark
    "台聯正式成立",            # Party founding; below threshold vs major party milestones
    "潭美颱風侵台",            # Minor typhoon; below landmark threshold
    "吳憶樺監護權風波",       # Family legal case; not a national landmark
    "航海王台視首播",          # Pop culture; not a historical landmark
    "金融控股公司法三讀",     # Financial legislation; below public landmark threshold
    "湖口化工廠爆炸",          # Industrial accident; local significance only
    "東方科學園區大火",       # Industrial fire; local significance only
    "豐原站列車溜逸事故",     # Railway accident; below landmark threshold
}

result = []
removed = 0
updated = 0

for ev in data:
    if ev['title'] in remove_titles:
        print(f"REMOVED: {ev['date']} {ev['title']}")
        removed += 1
        continue
    if ev['title'] in url_map and not ev.get('source_url', ''):
        ev['source_url'] = url_map[ev['title']]
        updated += 1
        print(f"URL: {ev['date']} {ev['title']}")
    result.append(ev)

print(f"\nRemoved {removed} borderline events")
print(f"Updated {updated} events with URLs")

events_2001 = [e for e in result if e['date'].startswith('2001')]
with_url = [e for e in events_2001 if e.get('source_url', '')]
print(f"2001: {len(events_2001)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
