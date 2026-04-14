#!/usr/bin/env python3
"""Update 2004 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "台北101正式啟用":
        "https://zh.wikipedia.org/zh-tw/台北101",
    "陳詩欣奪奧運首金":
        "https://zh.wikipedia.org/zh-tw/陳詩欣",
    "七二水災重創中南部":
        "https://zh.wikipedia.org/zh-tw/2004年七二水災",
    "性平教育法公布":
        "https://zh.wikipedia.org/zh-tw/性別平等教育法",
    "第十一任總統就職":
        "https://zh.wikipedia.org/zh-tw/中華民國第十一任總統就職典禮",
    "陳水扁連任總統":
        "https://zh.wikipedia.org/zh-tw/2004年中華民國總統選舉",
    "二二八手護台灣":
        "https://zh.wikipedia.org/zh-tw/二二八百萬人手護台灣",
    "國道三號全線通車":
        "https://zh.wikipedia.org/zh-tw/國道三號_(台灣)",
}

# Events to REMOVE: borderline/trivial/redundant
remove_titles = {
    "南瑪都颱風冬季登台",    # Unusual-season typhoon; minor casualties; below landmark
    "楊儒門投案",            # Individual case step; subsumed by 白米炸彈案 in 2003
    "當選無效訴訟駁回",      # Procedural ruling; subsumed by election narrative
    "小碧潭支線通車",        # Local MRT extension; consistent removal of infrastructure
    "艾利颱風致桃園停水",    # Typhoon infrastructure disruption; below landmark threshold
    "鯉魚潭水庫閘門脫落",    # Infrastructure malfunction; not a landmark
    "公投拚真相集會",        # Pre-election rally; subsumed by 三一九槍擊事件 narrative
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

events_2004 = [e for e in result if e['date'].startswith('2004')]
with_url = [e for e in events_2004 if e.get('source_url', '')]
print(f"2004: {len(events_2004)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
