#!/usr/bin/env python3
"""Fix remaining missing URLs via Wikipedia."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "八一八反迫遷行動":
        "https://zh.wikipedia.org/zh-tw/大埔事件",
    "奢侈稅法三讀":
        "https://zh.wikipedia.org/zh-tw/特種貨物及勞務稅條例",
    "再生能源法三讀":
        "https://zh.wikipedia.org/zh-tw/再生能源發展條例",
    "國民年金法三讀":
        "https://zh.wikipedia.org/zh-tw/國民年金法",
    "十二年國教宣布推動":
        "https://zh.wikipedia.org/zh-tw/十二年國民基本教育",
    "NCC組織法部分違憲":
        "https://zh.wikipedia.org/zh-tw/國家通訊傳播委員會",
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
