#!/usr/bin/env python3
"""Update 2009 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "台江國家公園成立":
        "https://www.cna.com.tw/news/ahel/202411045003.aspx",
    "中職假球案延燒":
        "https://www.cna.com.tw/news/aspt/202409275002.aspx",
    "澎湖博弈公投舉行":
        "https://vip.udn.com/vip/story/121160/5771460",
    "台北聽奧揭幕":
        "https://sports.ltn.com.tw/news/breakingnews/264966",
    "莫拉克颱風侵台":
        "https://news.ltn.com.tw/news/focus/paper/362759",
    "世運會高雄開幕":
        "https://sports.ltn.com.tw/news/paper/83786",
    "北捷內湖線通車":
        "https://time.udn.com/udntime/story/122833/6977718",
    "倪福德升上大聯盟":
        "https://sports.ltn.com.tw/news/breakingnews/5229457",
    "五都升格審核通過":
        "https://www.cna.com.tw/news/aloc/202012200068.aspx",
    "台灣重返世界衛生大會":
        "https://www.cna.com.tw/news/acn/201805080052.aspx",
    "22K實習方案上路":
        "https://news.ltn.com.tw/news/focus/paper/609206",
    "郭冠英遭免職":
        "https://news.ltn.com.tw/news/focus/paper/287436",
    "經典賽首戰敗韓":
        "https://sports.ltn.com.tw/news/paper/1743262",
    "聖嚴法師圓寂":
        "https://news.ltn.com.tw/news/life/breakingnews/176241",
    "消費券首階段發放":
        "https://time.udn.com/udntime/story/122833/7045421",
    "總統府共諜案爆發":
        "https://news.ltn.com.tw/news/politics/paper/273835",
    "李慶安辭去立委":
        "https://news.ltn.com.tw/news/politics/paper/346129",
}

# Events to REMOVE: redundant/borderline/trivial
remove_titles = {
    "高雄世運閉幕創佳績",    # Subsumed by 世運會高雄開幕; closing ceremony is a follow-up
    "行政院核定五都案",      # Redundant with 五都升格審核通過 (same policy, same week)
    "嗆馬保台大遊行",        # Partisan rally; no clean URL; not a landmark
    "H1N1防疫中心成立",      # Redundant with 首例H1N1病例出現; procedural step
    "信義區工地吊臂砸車",    # One-off construction accident; no landmark significance
    "歌手阿桑病逝",          # Celebrity death; not a historical landmark
    "地方制度法修正",        # Enabling legislation; subsumed by 五都升格審核通過
    "經典賽敗給中國",        # Redundant with 經典賽首戰敗韓 (same tournament, same day)
    "經濟成長預測轉負",      # Statistical announcement; not a discrete historical event
    "菸害防制新法上路",      # Regulatory implementation; below landmark threshold
    "擴大高中免試入學",      # Gradual education policy; not a discrete landmark
    "台南都會公園啟用",      # Local park opening; not a national landmark
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

events_2009 = [e for e in result if e['date'].startswith('2009')]
with_url = [e for e in events_2009 if e.get('source_url', '')]
print(f"2009: {len(events_2009)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
