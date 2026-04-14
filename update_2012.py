#!/usr/bin/env python3
"""Update 2012 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "鳳飛飛逝世消息證實":
        "https://ent.ltn.com.tw/news/breakingnews/602714",
    "士林王家遭強拆":
        "https://news.ltn.com.tw/news/focus/paper/571934",
    "北門醫院火警12死":
        "https://news.ltn.com.tw/news/society/breakingnews/712495",
    "TPA奪英雄聯盟世界冠軍":
        "https://3c.ltn.com.tw/news/7286",
    "興農牛宣布停止經營":
        "https://sports.ltn.com.tw/news/breakingnews/737505",
    "蘇建和案無罪定讞":
        "https://www.cna.com.tw/news/ahel/202401125003.aspx",
    "保釣船隊與日艦對峙":
        "https://news.ltn.com.tw/news/society/paper/960603",
}

# Events to REMOVE: borderline/redundant/below landmark threshold
remove_titles = {
    "義聯接手興農牛",        # Follow-up to 興農牛宣布停止經營; subsumed by that entry
    "埔心平交道事故",        # Regional accident; no lasting policy significance
    "Makiyo毆打司機案",      # Celebrity tabloid incident; not a historical event
    "電價調漲方案公布",      # Policy announcement; not landmark
    "證所稅方案出爐",        # Short-lived policy (abolished within years); not landmark
    "蘇貞昌當選民進黨主席",  # Internal party election; not a major public event
    "東門站啟用中和新蘆線成形", # MRT infrastructure opening (consistent removals)
    "李宗瑞投案收押",        # Celebrity crime case; no lasting policy significance
    "證所稅與美牛法案過關",  # Redundant with 美牛有條件解禁; duplicate policy event
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

events_2012 = [e for e in result if e['date'].startswith('2012')]
with_url = [e for e in events_2012 if e.get('source_url', '')]
print(f"2012: {len(events_2012)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
