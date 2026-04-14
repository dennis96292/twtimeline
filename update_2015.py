#!/usr/bin/env python3
"""Update 2015 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "國民黨撤換洪秀柱":
        "https://www.cna.com.tw/news/firstnews/201510170154.aspx",
    "林冠華身亡震撼反課綱":
        "https://news.ltn.com.tw/news/focus/paper/902622",
    "反課綱學生攻入教育部":
        "https://news.ltn.com.tw/news/life/breakingnews/1358655",
    "北投文化國小命案":
        "https://news.ltn.com.tw/news/focus/paper/884889",
    "北市府勒令大巨蛋停工":
        "https://www.cna.com.tw/news/firstnews/201505205019.aspx",
    "RCA汙染案一審判賠":
        "https://www.cna.com.tw/news/asoc/202203110177.aspx",
    "台中捷運鋼梁墜落":
        "https://www.cna.com.tw/news/firstnews/201504105015.aspx",
    "慈濟撤回內湖開發案":
        "https://www.cna.com.tw/news/firstnews/201503165012.aspx",
    "廢核遊行三地登場":
        "https://news.ltn.com.tw/news/life/breakingnews/1257044",
    "高雄監獄脅持事件":
        "https://www.cna.com.tw/news/firstnews/201502115016.aspx",
    "太陽花參與者遭起訴":
        "https://news.ltn.com.tw/news/focus/paper/855119",
    "新屋保齡球館火災":
        "https://www.cna.com.tw/news/asoc/201501205002.aspx",
    "陳水扁保外就醫":
        "https://www.cna.com.tw/news/firstnews/201501050205.aspx",
}

# Events to REMOVE: borderline/data errors/redundant
remove_titles = {
    "反滲透法三讀通過",  # DATA ERROR: 反滲透法 passed 2019-12-31, not 2015; 2019 entry already exists
    "馬習會宣布舉行",    # Redundant precursor to 馬習會登場 (Nov 7 already has URL)
    "鄭捷一審判死",      # Redundant: 2016 execution entry is the definitive milestone
    "李全教涉賄案遭羈押", # Municipal-level corruption case; below national landmark threshold
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

events_2015 = [e for e in result if e['date'].startswith('2015')]
with_url = [e for e in events_2015 if e.get('source_url', '')]
print(f"2015: {len(events_2015)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
