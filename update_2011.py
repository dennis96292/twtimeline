#!/usr/bin/env python3
"""Update 2011 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "器官誤植愛滋事件":
        "https://news.ltn.com.tw/news/society/breakingnews/537004",
    "塑化劑食安風暴":
        "https://news.ltn.com.tw/news/focus/paper/722936",
    "國光石化案喊停":
        "https://news.ltn.com.tw/news/life/breakingnews/487830",
    "台灣援助東日本震災":
        "https://www.cna.com.tw/news/firstnews/202103110084.aspx",
    "ALA夜店火災":
        "https://news.ltn.com.tw/news/society/breakingnews/470155",
    "曾雅妮登上世界第一":
        "https://news.ltn.com.tw/news/local/paper/469767",
    "羅賢哲共諜案爆發":
        "https://news.ltn.com.tw/news/politics/breakingnews/461077",
    "江國慶案重大轉折":
        "https://www.cna.com.tw/news/asoc/201902150303.aspx",
}

# Events to REMOVE: election details/routine appointments/borderline
remove_titles = {
    "盛治仁因夢想家請辭",    # Government spending controversy; ministerial resignation below landmark
    "蔡英文公布副手蘇嘉全",  # Election campaign detail; not an independent historical event
    "馬吳配正式成形",        # Election campaign detail; subsumed by the election result
    "民進黨提名蔡英文",      # Internal party nomination; not a standalone major event
    "中華隊奪少棒世界冠軍",  # Date/fact uncertain in source; frequent title not uniquely landmark
    "金門大橋動工",          # Date likely incorrect (construction began 2012); bridge already in DB as 2022 completion
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

events_2011 = [e for e in result if e['date'].startswith('2011')]
with_url = [e for e in events_2011 if e.get('source_url', '')]
print(f"2011: {len(events_2011)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
