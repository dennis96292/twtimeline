#!/usr/bin/env python3
"""Update 2024 events with verified source_urls."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "全聯台中倉儲火災":
        "https://www.cna.com.tw/news/asoc/202412190188.aspx",
    "台灣首奪12強冠軍":
        "https://www.cna.com.tw/news/aspt/202411245003.aspx",
    "安泰醫院火災":
        "https://www.cna.com.tw/news/asoc/202410030121.aspx",
    "柯文哲遭羈押禁見":
        "https://www.cna.com.tw/news/asoc/202409050315.aspx",
    "應曉薇沈慶京遭羈押":
        "https://www.cna.com.tw/news/asoc/202408290399.aspx",
    "台股單日重挫逾1800點":
        "https://www.cna.com.tw/news/afe/202408050135.aspx",
    "鄭文燦涉貪遭羈押":
        "https://news.ltn.com.tw/news/politics/breakingnews/4730907",
    "林士傑遭槍擊身亡":
        "https://www.cna.com.tw/news/asoc/202407080125.aspx",
    "中國快艇闖入淡水港":
        "https://www.cna.com.tw/news/aipl/202406100193.aspx",
    "共軍環台軍演":
        "https://news.ltn.com.tw/news/politics/breakingnews/4681595",
    "台中捷運隨機傷人案":
        "https://www.cna.com.tw/news/asoc/202405215003.aspx",
    "公然侮辱罪合憲限縮":
        "https://www.cna.com.tw/news/asoc/202404260194.aspx",
    "馬習二會在北京舉行":
        "https://www.cna.com.tw/news/acn/202404100316.aspx",
    "花蓮規模7.2強震":
        "https://news.ltn.com.tw/news/life/breakingnews/4628206",
    "寶林茶室中毒案":
        "https://www.cna.com.tw/news/ahel/202403290321.aspx",
    "金門近海快艇翻覆事件":
        "https://udn.com/news/story/123923/7770138",
}

updated = 0
for ev in data:
    if ev['title'] in url_map and not ev.get('source_url', ''):
        ev['source_url'] = url_map[ev['title']]
        updated += 1
        print(f"URL: {ev['date']} {ev['title']}")

print(f"\nUpdated {updated} events")

events_2024 = [e for e in data if e['date'].startswith('2024')]
with_url = [e for e in events_2024 if e.get('source_url', '')]
print(f"2024: {len(events_2024)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Saved {len(data)} events.")
