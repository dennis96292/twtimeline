#!/usr/bin/env python3
"""Update 2000 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "新航空難發生":
        "https://zh.wikipedia.org/zh-tw/新加坡航空006號班機空難",
    "核四宣布停建":
        "https://zh.wikipedia.org/zh-tw/核四公投",
    "高屏大橋斷裂":
        "https://zh.wikipedia.org/zh-tw/高屏大橋",
    "八掌溪事件":
        "https://zh.wikipedia.org/zh-tw/八掌溪事件",
    "陳水扁就任總統":
        "https://zh.wikipedia.org/zh-tw/中華民國第十任總統就職典禮",
    "蘇建和案准再審":
        "https://zh.wikipedia.org/zh-tw/蘇建和案",
}

# Events to REMOVE
remove_titles = {
    "鄭太吉遭執行死刑",    # Individual criminal execution; below national landmark threshold
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

events_2000 = [e for e in result if e['date'].startswith('2000')]
with_url = [e for e in events_2000 if e.get('source_url', '')]
print(f"2000: {len(events_2000)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
