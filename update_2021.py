#!/usr/bin/env python3
"""Update 2021 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "陳柏惟遭罷免成功":
        "https://www.cna.com.tw/news/firstnews/202110230226.aspx",
    "城中城大火":
        "https://www.cna.com.tw/news/firstnews/202110140032.aspx",
    "喬友大樓火災":
        "https://www.cna.com.tw/news/firstnews/202107010011.aspx",
    "蔡英文特赦王光祿":
        "https://www.cna.com.tw/news/firstnews/202105205005.aspx",
    "雙北升第三級警戒":
        "https://www.cna.com.tw/news/firstnews/202105155010.aspx",
    "黃捷罷免案未通過":
        "https://www.cna.com.tw/news/firstnews/202102060192.aspx",
    "王浩宇罷免成功":
        "https://www.cna.com.tw/news/firstnews/202101165005.aspx",
    "桃醫群聚爆首名醫師確診":
        "https://udn.com/news/story/121954/5213445",
    "新版護照正式啟用":
        "https://www.cna.com.tw/news/aipl/202101070072.aspx",
    "美國解除對台交往限制":
        "https://udn.com/news/story/121928/5162175",
    "台灣全面禁外籍旅客入境":
        "https://www.cna.com.tw/news/ahel/202012300251.aspx",
}

# Events to REMOVE: minor/borderline
remove_titles = {
    "虎豹潭溺水事故",    # Tragic accident but not a major historical event
    "中捷綠線正式通車",  # Routine infrastructure (consistent with earlier removals)
    "疫情升至第二級警戒", # Subsumed by the more significant Level 3 events
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

events_2021 = [e for e in result if e['date'].startswith('2021')]
with_url = [e for e in events_2021 if e.get('source_url', '')]
print(f"2021: {len(events_2021)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
