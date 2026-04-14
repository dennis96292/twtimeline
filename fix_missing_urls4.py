#!/usr/bin/env python3
"""Final URL fix: add remaining source URLs."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    # 2013
    "4G競標創天價":
        "https://ec.ltn.com.tw/article/paper/726623",
    # 2010
    "陳水扁入監服刑":
        "https://theme.udn.com/theme/story/7491/622114",
    "法務部恢復執行死刑":
        "https://zh.wikipedia.org/zh-tw/中華民國死刑制度",
    "美國宣布對台軍售":
        "https://zh.wikipedia.org/zh-tw/美國對台軍售",
    # 2009
    "首例H1N1病例出現":
        "https://zh.wikipedia.org/zh-tw/2009年H1N1流感大流行台灣情況",
    # 2006
    "扁家四大案起訴":
        "https://zh.wikipedia.org/zh-tw/陳水扁",
    # 2005
    "全國取消髮禁":
        "https://news.ltn.com.tw/news/life/paper/30887",
}

result = []
updated = 0

for ev in data:
    if ev['title'] in url_map and not ev.get('source_url', ''):
        ev['source_url'] = url_map[ev['title']]
        updated += 1
        print(f"URL: {ev['date']} {ev['title']}")
    result.append(ev)

print(f"\nUpdated {updated} events with URLs")

missing = [e for e in result if not e.get('source_url', '')]
print(f"\nStill missing URLs ({len(missing)}):")
for e in missing:
    print(f"  {e['date']} {e['title']}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(result)} events.")
