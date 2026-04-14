#!/usr/bin/env python3
"""Update 2003 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "公投法三讀通過":
        "https://zh.wikipedia.org/zh-tw/公民投票法_(台灣)",
    "白米炸彈案爆發":
        "https://zh.wikipedia.org/zh-tw/楊儒門",
    "台北同志大遊行首辦":
        "https://zh.wikipedia.org/zh-tw/台灣同志遊行",
    "台灣自SARS疫區除名":
        "https://zh.wikipedia.org/zh-tw/2002年至2003年SARS事件",
    "SARS疫情蔓延台灣":
        "https://zh.wikipedia.org/zh-tw/嚴重急性呼吸道症候群台灣疫情",
}

# Events to REMOVE: borderline/trivial/redundant
remove_titles = {
    "賴比瑞亞與台斷交",      # Minor diplomatic severance; Liberia had limited formal ties
    "苗栗偷渡船翻覆案",      # Maritime accident; below landmark threshold
    "台商受害者協會成立",    # Interest group formation; not a landmark
    "WHA再拒台灣參與",        # Annual routine rejection; not a discrete landmark
    "SARS單日死亡飆升",      # Sub-event of SARS crisis; covered by main SARS entries
    "中華郵政公司成立",      # Administrative reorganization; below landmark threshold
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

events_2003 = [e for e in result if e['date'].startswith('2003')]
with_url = [e for e in events_2003 if e.get('source_url', '')]
print(f"2003: {len(events_2003)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
