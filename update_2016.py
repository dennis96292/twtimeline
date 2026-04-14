#!/usr/bin/env python3
"""Update 2016 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "復興航空宣布解散":
        "https://ec.ltn.com.tw/article/breakingnews/1895213",
    "台中鐵路高架化通車":
        "https://www.cna.com.tw/news/firstnews/201610140240.aspx",
    "莫蘭蒂颱風侵襲金門":
        "https://www.cna.com.tw/news/firstnews/201609150191.aspx",
    "黨產會成立":
        "https://news.ltn.com.tw/news/politics/breakingnews/1811533",
    "肯亞案台人再遭送中":
        "https://news.ltn.com.tw/news/politics/breakingnews/1665555",
    "蔡英文向原住民道歉":
        "https://news.ltn.com.tw/news/politics/breakingnews/1780914",
    "一銀ATM盜領案爆發":
        "https://www.cna.com.tw/news/firstnews/201607125008.aspx",
    "尼伯特颱風重創台東":
        "https://www.cna.com.tw/news/firstnews/201607085007.aspx",
    "松山車站列車爆炸":
        "https://news.ltn.com.tw/news/society/breakingnews/1755575",
    "雄三飛彈誤射事件":
        "https://www.cna.com.tw/news/aipl/201607010492.aspx",
    "華航空服員罷工":
        "https://www.cna.com.tw/news/firstnews/201606245013.aspx",
    "蔡英文就任總統":
        "https://www.cna.com.tw/news/firstnews/201605205026.aspx",
    "鄭捷遭執行死刑":
        "https://www.cna.com.tw/news/firstnews/201605100494.aspx",
    "肯亞案台嫌遣送中國":
        "https://www.cna.com.tw/news/aipl/201604125012.aspx",
    "內湖女童隨機命案":
        "https://www.cna.com.tw/news/firstnews/201603280338.aspx",
    "洪秀柱當選國民黨主席":
        "https://www.cna.com.tw/news/firstnews/201603265009.aspx",
    "美濃地震重創台南":
        "https://www.cna.com.tw/news/firstnews/201602065004.aspx",
    "霸王級寒流襲台":
        "https://www.cna.com.tw/news/firstnews/201601240135.aspx",
}

# Events to REMOVE: borderline/procedural/redundant
remove_titles = {
    "新任大法官名單公布",      # Routine constitutional appointment, no clean URL
    "撤回司法院正副院長提名",  # Political embarrassment; no lasting milestone
    "桃園機場淹水癱瘓",        # One-day operational disruption, no lasting significance
    "鄭捷死刑定讞",            # Redundant with 鄭捷遭執行死刑 (execution is the milestone)
    "馬來西亞遣返台嫌返台",    # Sub-episode of Malaysia case; suspects all released without charge
    "鄭性澤案檢方聲請再審",    # Procedural step; no clean 2016 URL; acquittal is in 2017
    "林全獲蔡英文延攬組閣",    # Expected administrative step; subsumed by 520就職
    "蘇嘉全當選立法院長",      # Institutional change, not a distinct public milestone event
    "工時改為單週40小時",      # Regulatory implementation of 2015 law; not a news event
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

events_2016 = [e for e in result if e['date'].startswith('2016')]
with_url = [e for e in events_2016 if e.get('source_url', '')]
print(f"2016: {len(events_2016)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
