#!/usr/bin/env python3
"""Fix remaining missing URLs: add Wikipedia URLs, remove final borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "日月光排廢水遭罰":
        "https://zh.wikipedia.org/zh-tw/日月光半導體排放廢水事件",
    "油品混充爭議擴大":
        "https://zh.wikipedia.org/zh-tw/大統長基食品廠食品問題",
    "監聽國會爭議爆發":
        "https://zh.wikipedia.org/zh-tw/特偵組違法監聽事件",
    "王金平黨籍案爆發":
        "https://zh.wikipedia.org/zh-tw/王金平黨籍案",
    "毒澱粉食安風暴":
        "https://zh.wikipedia.org/zh-tw/台灣順丁烯二酸化製澱粉事件",
    "同志遊行訴求婚姻平權":
        "https://zh.wikipedia.org/zh-tw/台灣同志遊行",
    "美牛有條件解禁":
        "https://zh.wikipedia.org/zh-tw/台灣萊克多巴胺爭議",
    "中華民國建國百年":
        "https://zh.wikipedia.org/zh-tw/中華民國建國百年系列活動",
    "馬祖博弈公投通過":
        "https://zh.wikipedia.org/zh-tw/2012年馬祖博弈業開放公民投票",
}

# Final borderline removals
remove_titles = {
    "蘇貞昌內閣上任",    # Routine cabinet change; consistent removal (謝長廷, 游錫堃, etc already removed)
    "性騷擾防治法施行",  # Minor law implementation; below landmark threshold
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

print(f"\nRemoved {removed} events")
print(f"Updated {updated} events with URLs")

missing = [e for e in result if not e.get('source_url', '')]
print(f"\nStill missing URLs ({len(missing)}):")
for e in missing:
    print(f"  {e['date']} {e['title']}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(result)} events.")
