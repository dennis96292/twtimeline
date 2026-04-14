#!/usr/bin/env python3
"""Update 2019 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "反滲透法通過":
        "https://www.cna.com.tw/news/firstnews/201912315003.aspx",
    "遠東航空突停飛":
        "https://www.cna.com.tw/news/firstnews/201912125004.aspx",
    "向心夫婦涉共諜案":
        "https://www.cna.com.tw/news/firstnews/201911300058.aspx",
    "同志遊行逾20萬人":
        "https://www.cna.com.tw/news/firstnews/201910260144.aspx",
    "南方澳跨港大橋斷裂":
        "https://www.cna.com.tw/news/firstnews/201910015004.aspx",
    "索羅門與台灣斷交":
        "https://news.ltn.com.tw/news/politics/breakingnews/2917663",
    "美准售66架F16V":
        "https://www.cna.com.tw/news/firstnews/201908190056.aspx",
    "中國禁參加金馬獎":
        "https://www.cna.com.tw/news/firstnews/201908070018.aspx",
    "嘉義鐵警李承翰殉職":
        "https://news.ltn.com.tw/news/society/breakingnews/2898233",
    "福衛七號成功升空":
        "https://news.ltn.com.tw/news/life/breakingnews/2832796",
    "反紅媒大遊行":
        "https://www.cna.com.tw/news/firstnews/201906235002.aspx",
    "長榮空服員罷工":
        "https://www.cna.com.tw/news/firstnews/201906205006.aspx",
    "國安法修正納入網路共諜":
        "https://news.ltn.com.tw/news/politics/breakingnews/2827198",
    "蔡英文挺香港反送中":
        "https://www.cna.com.tw/news/firstnews/201906090175.aspx",
    "公投法修正過關":
        "https://www.cna.com.tw/news/firstnews/201906175003.aspx",
    "北美事務協調會更名":
        "https://www.cna.com.tw/news/firstnews/201905255002.aspx",
    "美眾院通過台灣保證法案":
        "https://www.cna.com.tw/news/firstnews/201905080016.aspx",
    "共機越過海峽中線":
        "https://www.cna.com.tw/news/firstnews/201903315002.aspx",
    "還願遭中國抵制":
        "https://www.cna.com.tw/news/firstnews/201902260020.aspx",
    "華航機師罷工":
        "https://www.cna.com.tw/news/firstnews/201902080014.aspx",
}

# Events to REMOVE: routine/minor/borderline
remove_titles = {
    "宋楚瑜宣布參選總統",    # Routine presidential candidacy announcement
    "世大運台灣創境外最佳",  # Sports achievement, not major historical event
    "蔡英文加勒比海出訪",    # Routine diplomatic transit visit
    "四席立委補選投票",      # Routine by-election, not landmark
    "花蓮發生規模6.1地震",   # Minor quake, no significant casualties
    "民進黨主席補選",        # Internal party election, not landmark
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

events_2019 = [e for e in result if e['date'].startswith('2019')]
with_url = [e for e in events_2019 if e.get('source_url', '')]
print(f"2019: {len(events_2019)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
