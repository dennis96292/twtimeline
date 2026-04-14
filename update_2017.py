#!/usr/bin/env python3
"""Update 2017 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "新黨青年遭調查局搜索":
        "https://www.cna.com.tw/news/firstnews/201712190019.aspx",
    "李明哲中國受審":
        "https://news.ltn.com.tw/news/politics/breakingnews/2266661",
    "賴清德接任行政院長":
        "https://www.cna.com.tw/news/aipl/201709050148.aspx",
    "台北世大運開幕":
        "https://news.ltn.com.tw/news/focus/paper/1128443",
    "全台大停電":
        "https://www.cna.com.tw/news/firstnews/201708155021.aspx",
    "公務員年改三讀":
        "https://www.cna.com.tw/news/firstnews/201706275009.aspx",
    "巴拿馬與台灣斷交":
        "https://www.cna.com.tw/news/firstnews/201706135027.aspx",
    "同婚釋憲通過":
        "https://news.ltn.com.tw/news/society/breakingnews/2077776",
    "潛艦國造正式啟動":
        "https://news.ltn.com.tw/news/focus/paper/1087844",
    "南港遊覽車事故":
        "https://news.ltn.com.tw/news/society/breakingnews/1974133",
}

# Events to REMOVE: borderline/minor/redundant
remove_titles = {
    "中和出租套房縱火",        # Crime/accident, not a structural historical event
    "幻象戰機失聯引風波",      # Single aircraft accident, not a policy turning point
    "同志遊行聚焦性平教育",    # Subsumed by the far more significant 同婚釋憲 ruling
    "日常對話代表角逐奧斯卡",  # Factually inaccurate (film won Berlin award, not Oscar entry)
    "岡山交流道重大車禍",      # Traffic accident, not a national historical landmark
    "原轉小教室遭清場",        # Date/event unclear; no verifiable landmark URL found
    "豬哥亮病逝",              # Celebrity death, not a major historical event
    "首度驗出雞蛋戴奧辛",      # Single farm food incident, far smaller than other food scandals
    "八田與一銅像遭斷頭",      # Vandalism by individual, not a structural historical event
    "原團體抗議傳統領域劃設",  # Routine protest, not a landmark
    "機場捷運試營運開始",      # Redundant with 機場捷運正式通車 (Mar 2)
    "蔡英文出訪中美洲",        # Routine diplomatic transit visit
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

events_2017 = [e for e in result if e['date'].startswith('2017')]
with_url = [e for e in events_2017 if e.get('source_url', '')]
print(f"2017: {len(events_2017)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
