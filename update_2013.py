#!/usr/bin/env python3
"""Update 2013 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "日月明功虐死案爆發":
        "https://news.ltn.com.tw/news/society/paper/743664",
    "看見台灣上映":
        "https://udn.com/news/story/7160/4173709",
    "軍審法修正三讀":
        "https://news.ltn.com.tw/news/politics/paper/1696370",
    "林杰樑醫師病逝":
        "https://news.ltn.com.tw/news/life/breakingnews/849677",
    "台日漁業協議簽署":
        "https://news.ltn.com.tw/news/politics/paper/669898",
    "反核遊行串連全台":
        "https://news.ltn.com.tw/news/politics/breakingnews/964225",
    "九月政爭爆發":
        "https://time.udn.com/udntime/story/122833/9421324",
}

# Events to REMOVE: trivial/redundant/below landmark threshold
remove_titles = {
    "基隆大黃鴨爆裂",        # Trivial accident; not a historical event
    "信義線正式通車",        # Infrastructure opening (consistent with other MRT removals)
    "兄弟象宣布求售",        # Sports business event; not a national historical landmark
    "徐生明猝逝",            # Sports coach death; below national landmark threshold
    "中華男籃擊敗中國",      # Sports achievement; not a major historical event
    "李國修病逝",            # Theater director death; below national landmark threshold
    "南投再發規模6.3地震",   # No deaths; not a landmark seismic event
    "南投地震釀死傷",        # Magnitude 6.1 with minimal casualties; not landmark
    "嘉義醃頭案曝光",        # Sensational crime; no policy significance
    "是方電訊機房火警",      # Data center fire; no lasting historical significance
    "媽媽嘴命案發生",        # Criminal case; did not catalyze major policy change
    "江宜樺接任閣揆",        # Duplicate: announcement date; formal inauguration is Feb 18
    "顏寬恒贏得立委補選",    # Minor by-election; not a national landmark
    "人民火大遊行",          # Partisan DPP rally; not a civic landmark
    "廣電三法初審通過",      # Committee review only; bill never passed full legislature
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

events_2013 = [e for e in result if e['date'].startswith('2013')]
with_url = [e for e in events_2013 if e.get('source_url', '')]
print(f"2013: {len(events_2013)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
