#!/usr/bin/env python3
"""Update 2007 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "台灣高鐵正式通車":
        "https://time.udn.com/udntime/story/122392/6886035",
    "力霸金融危機爆發":
        "https://time.udn.com/udntime/story/122833/7575262",
    "撒奇萊雅族獲正名":
        "https://news.ltn.com.tw/news/politics/paper/111906",
    "馬英九遭起訴辭黨魁":
        "https://news.ltn.com.tw/news/focus/paper/116505",
    "特偵組正式掛牌":
        "https://news.ltn.com.tw/news/politics/breakingnews/1832800",
    "中正紀念堂改名":
        "https://news.ltn.com.tw/news/focus/paper/129757",
    "與哥斯大黎加斷交":
        "https://www.cna.com.tw/news/aipl/202401150242.aspx",
    "大里列車相撞事故":
        "https://news.ltn.com.tw/news/society/paper/135885",
    "楊儒門獲總統特赦":
        "https://www.cna.com.tw/news/ahel/202406205002.aspx",
    "陽明山遊覽車墜谷":
        "https://udn.com/news/story/7320/8623311",
    "罪犯減刑條例生效":
        "https://news.ltn.com.tw/news/politics/paper/135822",
    "華航沖繩機場起火":
        "https://news.ltn.com.tw/news/focus/paper/149065",
    "李安奪威尼斯金獅獎":
        "https://news.ltn.com.tw/news/focus/paper/153110",
    "民主紀念館掛自由廣場":
        "https://news.ltn.com.tw/news/focus/paper/173853",
    "李慶安美籍文件曝光":
        "https://news.ltn.com.tw/news/focus/paper/268371",
}

# Events to REMOVE: borderline/wrong-year/routine
remove_titles = {
    "周俊勳成世界棋王",        # Individual sports achievement; not national historical landmark
    "張俊雄接任閣揆",          # Routine cabinet change; no lasting significance
    "貓空纜車正式營運",        # Local infrastructure opening
    "鹿林彗星被發現",          # Scientific discovery; not political/social history landmark
    "聖帕颱風登陸台灣",        # Routine typhoon; no confirmed major casualties
    "台北縣升格準直轄市",      # Administrative reclassification step (not yet full upgrade)
    "柯羅莎颱風警報發布",      # Routine weather event
    "漁業署南遷高雄",          # Routine government agency relocation
    "野草莓運動持續擴大",      # DATA ERROR: Wild Strawberry Movement was 2008, not 2007
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

events_2007 = [e for e in result if e['date'].startswith('2007')]
with_url = [e for e in events_2007 if e.get('source_url', '')]
print(f"2007: {len(events_2007)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
