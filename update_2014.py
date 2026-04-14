#!/usr/bin/env python3
"""Update 2014 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "桃園升格直轄市":
        "https://www.cna.com.tw/news/firstnews/201412150027.aspx",
    "九合一選舉藍營重挫":
        "https://news.ltn.com.tw/news/politics/breakingnews/1169833",
    "松山線正式通車":
        "https://www.cna.com.tw/news/firstnews/201411150005.aspx",
    "頂新飼料油風暴":
        "https://news.ltn.com.tw/news/focus/paper/820116",
    "巢運夜宿帝寶":
        "https://news.ltn.com.tw/news/focus/paper/819016",
    "台灣聲援雨傘革命":
        "https://news.ltn.com.tw/news/politics/breakingnews/1117999",
    "信義警夜店執勤殉職":
        "https://www.cna.com.tw/news/firstnews/201409140225.aspx",
    "黑心餿水油案爆發":
        "https://www.cna.com.tw/news/firstnews/201409045015.aspx",
    "復興航空澎湖空難":
        "https://www.cna.com.tw/news/firstnews/201407240479.aspx",
    "張志軍遭潑漆灑冥紙":
        "https://news.ltn.com.tw/news/politics/paper/847005",
    "鄭捷北捷隨機殺人":
        "https://www.cna.com.tw/news/firstnews/201405210423.aspx",
    "太陽花撤出立法院":
        "https://news.ltn.com.tw/news/politics/paper/863823",
    "凱道五十萬人反服貿":
        "https://news.ltn.com.tw/news/focus/paper/766655",
    "砂石車衝撞總統府":
        "https://www.cna.com.tw/news/firstnews/201401250011.aspx",
}

# Events to REMOVE: redundant/procedural/below landmark threshold
remove_titles = {
    "馬英九辭國民黨主席",    # Routine post-election political consequence
    "毛治國接任閣揆",        # Routine caretaker cabinet; no landmark significance
    "江宜樺宣布請辭",        # Post-election consequence, subsumed by election entry
    "雷虎小組訓練擦撞墜機",  # Training accident, not a policy-changing landmark
    "魏應充遭收押",          # Legal consequence of oil scandal; not standalone landmark
    "海研五號沉沒",          # Minor maritime accident (2 deaths); not landmark
    "邱文達因油品事件請辭",  # Ministerial consequence; subsumed by oil scandal entries
    "蔣偉寧因論文審查案請辭", # Academic integrity scandal, not a major historical event
    "行政院驅離引爆爭議",    # Sub-event of Sunflower Movement; subsumed by 3/18 and 3/30
    "群眾佔領行政院",        # Sub-event of Sunflower Movement; subsumed by 3/18 and 3/30
    "王金平承諾先立法再審",  # Negotiating milestone inside movement; not standalone
    "再度執行死刑",          # Not a unique milestone; Taiwan resumed executions in 2010
    "反核群眾遭水車驅離",    # Annual anti-nuclear protest; not a landmark
    "孫中山銅像遭拉倒",      # Single act of vandalism; no lasting significance; no URL found
    "黃景泰遭聲押",          # Local-level corruption case; below national landmark threshold
    "蔡英文重任民進黨主席",  # No verified news URL found; borderline event
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

events_2014 = [e for e in result if e['date'].startswith('2014')]
with_url = [e for e in events_2014 if e.get('source_url', '')]
print(f"2014: {len(events_2014)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
