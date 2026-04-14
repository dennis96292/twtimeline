#!/usr/bin/env python3
"""Update 2002 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "噶瑪蘭族獲正名":
        "https://zh.wikipedia.org/zh-tw/噶瑪蘭族",
    "一邊一國說提出":
        "https://zh.wikipedia.org/zh-tw/一邊一國",
    "華航澎湖空難":
        "https://zh.wikipedia.org/zh-tw/中華航空611號班機空難",
    "花蓮外海強震":
        "https://zh.wikipedia.org/zh-tw/2002年花蓮地震",
    "台灣正式加入WTO":
        "https://zh.wikipedia.org/zh-tw/台灣世界貿易組織會籍",
}

# Events to REMOVE: borderline/routine
remove_titles = {
    "黑面琵鷺中毒暴斃",    # Wildlife incident; not a national landmark
    "九二八教師大遊行",    # Labor protest; below national landmark threshold
    "陳金鋒登上大聯盟",    # Individual sports milestone; not national historical event
    "游錫堃接任閣揆",      # Routine cabinet change; no lasting significance
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

events_2002 = [e for e in result if e['date'].startswith('2002')]
with_url = [e for e in events_2002 if e.get('source_url', '')]
print(f"2002: {len(events_2002)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
