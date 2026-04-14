#!/usr/bin/env python3
"""Update 2026 events: add verified source_urls, fix/remove inaccurate events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === URL assignments for 2026 events (verified via web search) ===
url_map = {
    "共機大舉擾台二十六架次":
        "https://www.cna.com.tw/news/aipl/202603150068.aspx",  # CNA not found exactly, use LTN
    "台灣首度在WBC擊敗韓國":
        "https://www.cna.com.tw/news/aspt/202603085002.aspx",
    "卓榮泰成台日斷交後首位公開訪日閣揆":
        "https://www.chinatimes.com/realtimenews/20260308000835-260408",
    "立院通過國民黨版國防特別條例":
        "https://www.cna.com.tw/news/aipl/202603050129.aspx",
    "美台簽署對等貿易協定":
        "https://www.cna.com.tw/news/aipl/202602130015.aspx",
    "中共宣布恢復上海居民赴金馬旅遊":
        "https://www.cna.com.tw/news/acn/202602040202.aspx",
    "總統特赦長照悲劇八旬婦人":
        "https://udn.com/news/story/124763/9327570",
    "美國眾院通過臺灣保護法案":
        "https://www.cna.com.tw/news/aipl/202602100131.aspx",
    "第三批M1A2T戰車完成生產":
        "https://def.ltn.com.tw/article/breakingnews/5328848",
    "藍白會期末通過中天條款與黨產條例修法":
        "https://www.cna.com.tw/news/aipl/202601300311.aspx",
    "陳菊因健康因素請辭監察院長":
        "https://www.chinatimes.com/realtimenews/20260128004507-260407",
    "霍諾德徒手攀登台北101":
        "https://udn.com/news/story/124745/9287414",
    "海鯤號首度潛航測試成功":
        "https://www.cna.com.tw/news/aipl/202601290354.aspx",
    "共軍無人機闖東沙領空":
        "https://www.cna.com.tw/news/aipl/202601170068.aspx",
    "中天記者涉共諜案遭羈押":
        "https://www.cna.com.tw/news/asoc/202601170176.aspx",
    "臺美完成關稅協議":
        "https://www.cna.com.tw/news/aipl/202601200201.aspx",
    "台灣新生兒數再創新低":
        "https://www.cna.com.tw/news/ahel/202601090067.aspx",
    "F16V戰機花東外海失聯":
        "https://www.cna.com.tw/news/aipl/202601070128.aspx",
    "台積電帶動臺股首登3萬點":
        "https://www.cna.com.tw/news/afe/202601050030.aspx",
    "賴清德發表元旦談話":
        "https://news.ltn.com.tw/news/politics/breakingnews/5296004",
}

# Fix the LTN URL for 共機 (the CNA one was guessed, use the confirmed one)
url_map["共機大舉擾台二十六架次"] = "https://def.ltn.com.tw/article/breakingnews/5370614"

# === Events to REMOVE (inaccurate) ===
remove_titles = {
    "賴清德與習近平通話成國際焦點",  # INACCURATE: no such call happened
    "美國授權新一輪對台大型軍售",     # NOT VERIFIABLE as distinct 2026-03 event
}

# === Event to ADD (correction for the above) ===
new_event = {
    "date": "2026-02-05",
    "title": "川習通話涉台議題成國際焦點",
    "desc": "美國總統川普與中國國家主席習近平通話，習近平要求美方慎重處理對台軍售，川普表示重視中方關切。賴清德回應稱台美溝通管道暢通、合作計畫不變，兩岸及美中台關係成為國際焦點。",
    "tags": ["兩岸", "外交", "政治"],
    "source_url": "https://www.cna.com.tw/news/acn/202602050008.aspx"
}

# Process
result = []
for ev in data:
    if ev['title'] in remove_titles:
        print(f"REMOVED: {ev['date']} {ev['title']}")
        continue
    # Apply URL if available
    if ev['title'] in url_map and not ev.get('source_url', ''):
        ev['source_url'] = url_map[ev['title']]
        print(f"URL ADDED: {ev['date']} {ev['title']} -> {url_map[ev['title']][:60]}")
    result.append(ev)

# Insert the corrected event in the right position (sorted by date desc)
result.append(new_event)
result.sort(key=lambda e: e['date'], reverse=True)
print(f"\nADDED: {new_event['date']} {new_event['title']}")

# Count 2026 stats
events_2026 = [e for e in result if e['date'].startswith('2026')]
with_url_2026 = [e for e in events_2026 if e.get('source_url', '')]
print(f"\n2026: {len(events_2026)} events, {len(with_url_2026)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Total events saved: {len(result)}")
