#!/usr/bin/env python3
"""Update 2010 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "五都正式升格":
        "https://www.cna.com.tw/news/aloc/202012200063.aspx",
    "連勝文遭槍擊":
        "https://news.ltn.com.tw/news/focus/paper/451189",
    "楊淑君亞運失格事件":
        "https://www.cna.com.tw/news/firstnews/201501040295.aspx",
    "蘇建和案三人再判無罪":
        "https://news.ltn.com.tw/news/society/paper/700052",
    "國道六號工地坍塌":
        "https://news.ltn.com.tw/news/focus/paper/431947",
    "ECFA正式生效":
        "https://www.cna.com.tw/news/firstnews/202009120139.aspx",
    "國道三號山崩":
        "https://time.udn.com/udntime/story/122833/8795149",
}

# Events to REMOVE: borderline/routine/below landmark threshold
remove_titles = {
    "第六次江陳會舉行",      # One of many Cross-Strait meetings; not a unique landmark
    "新莊線蘆洲線通車",      # MRT infrastructure opening (consistent removals)
    "松山羽田航線重開",      # Aviation route; routine transport event
    "兄弟象奪總冠軍",        # CPBL championship (annual); not a unique landmark
    "賴英照請辭司法院長",    # Routine personnel change; not an independent major event
    "翁奇楠遭槍擊身亡",      # Gang-related killing; significant but below historical landmark level
    "馬英九蔡英文辯論ECFA",  # Pre-ECFA debate; subsumed by ECFA signing/taking effect entries
    "甲仙地震發生",          # Minor casualties; not a landmark earthquake
    "行政院組織法修正",      # Administrative reform legislation; not a public landmark event
    "三席立委補選綠營全勝",  # By-election; not a major landmark
    "美國特定牛雜禁輸入",    # Trade regulation detail; not a landmark
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

events_2010 = [e for e in result if e['date'].startswith('2010')]
with_url = [e for e in events_2010 if e.get('source_url', '')]
print(f"2010: {len(events_2010)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
