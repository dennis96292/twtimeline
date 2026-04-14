#!/usr/bin/env python3
"""Update 2018 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "勞基法再修正三讀":
        "https://news.ltn.com.tw/news/politics/breakingnews/2307459",
    "花蓮強震釀重大災情":
        "https://news.ltn.com.tw/news/life/breakingnews/2334993",
    "台灣旅行法生效":
        "https://www.cna.com.tw/news/firstnews/201803170014.aspx",
    "多明尼加與台灣斷交":
        "https://news.ltn.com.tw/news/politics/breakingnews/2411756",
    "布吉納法索斷交":
        "https://www.cna.com.tw/news/firstnews/201805245003.aspx",
    "AIT內湖新館落成":
        "https://www.cna.com.tw/news/aipl/201806120035.aspx",
    "台灣省政府走入歷史":
        "https://news.ltn.com.tw/news/politics/breakingnews/2467023",
    "九合一選舉民進黨重挫":
        "https://www.cna.com.tw/news/firstnews/201811245007.aspx",
    "憲法訴訟法三讀":
        "https://www.cna.com.tw/news/aipl/201812180326.aspx",
    "金門海漂豬驗出非洲豬瘟":
        "https://www.cna.com.tw/news/firstnews/201901035005.aspx",
}

# Events to REMOVE: redundant/borderline
remove_titles = {
    "花蓮地震發生",    # Feb 4 precursor quake, subsumed by the major Feb 6 disaster entry
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

events_2018 = [e for e in result if e['date'].startswith('2018')]
with_url = [e for e in events_2018 if e.get('source_url', '')]
print(f"2018: {len(events_2018)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
