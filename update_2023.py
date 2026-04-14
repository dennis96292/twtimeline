#!/usr/bin/env python3
"""Update 2023 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === Verified URL assignments for 2023 events ===
url_map = {
    "新北國中殺人案":
        "https://www.cna.com.tw/news/asoc/202312250266.aspx",
    "最低工資法三讀":
        "https://www.cna.com.tw/news/ahel/202312120096.aspx",
    "獵風者衛星升空":
        "https://www.cna.com.tw/news/ait/202310090015.aspx",
    "小犬颱風創蘭嶼陣風紀錄":
        "https://www.cna.com.tw/news/aloc/202310050015.aspx",
    "海鯤號正式下水":
        "https://def.ltn.com.tw/article/breakingnews/4442089",
    "明揚國際工廠大火":
        "https://udn.com/news/story/123754/7463090",
    "大直民宅坍塌":
        "https://www.cna.com.tw/news/asoc/202309080199.aspx",
    "海葵颱風登陸台東":
        "https://www.cna.com.tw/news/ahel/202309030014.aspx",
    "高虹安涉詐助理費起訴":
        "https://news.ltn.com.tw/news/politics/breakingnews/4395445",
    "台灣碳權交易所成立":
        "https://udn.com/news/story/7238/7353769",
    "農委會升格農業部":
        "https://www.cna.com.tw/news/ahel/202305160045.aspx",
    "性平三法修正完成":
        "https://news.pts.org.tw/article/648902",
    "板橋幼兒園餵藥案":
        "https://news.pts.org.tw/article/645929",
    "中捷吊臂砸車廂事故":
        "https://news.ltn.com.tw/news/society/breakingnews/4296975",
    "聯華食品彰化廠大火":
        "https://www.cna.com.tw/news/asoc/202304250033.aspx",
    "蔡英文會晤麥卡錫":
        "https://www.cna.com.tw/news/aipl/202304060019.aspx",
    "馬英九訪中成首例":
        "https://www.cna.com.tw/news/acn/202303300107.aspx",
    "宏都拉斯與台灣斷交":
        "https://news.ltn.com.tw/news/politics/breakingnews/4251481",
    "二膽守軍上兵失聯":
        "https://www.cna.com.tw/news/aipl/202303140331.aspx",
    "疫後特別條例通過":
        "https://news.pts.org.tw/article/623852",
    "蘇貞昌內閣總辭":
        "https://www.cna.com.tw/news/aipl/202301300060.aspx",
    "賴清德當選民進黨主席":
        "https://www.cna.com.tw/news/aipl/202301155002.aspx",
}

# === Events to REMOVE (borderline, not major historical events) ===
remove_titles = {
    "716凱道居住正義遊行",   # Political rally, not a landmark historical event
    "TPASS月票正式上路",      # Routine transport policy launch
}

# Process
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

# Count 2023 stats
events_2023 = [e for e in result if e['date'].startswith('2023')]
with_url = [e for e in events_2023 if e.get('source_url', '')]
print(f"2023: {len(events_2023)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(result)} events.")
