#!/usr/bin/env python3
"""Update 2006 events: add verified source_urls, remove borderline/duplicate events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "李安奪奧斯卡導演獎":
        "https://time.udn.com/udntime/story/122834/8794550",
    "福衛三號成功升空":
        "https://www.cna.com.tw/news/ahel/202504145002.aspx",
    "倒扁紅衫軍啟動":
        "https://udn.com/news/story/123482/7710050",
}

# Events to REMOVE: data errors (wrong year), redundant, or below landmark threshold
remove_titles = {
    # DATA ERRORS — These events belong to 2008 (already have correct 2008 entries)
    "王永慶逝世",              # Wang passed away Oct 2008, not 2006
    "陳水扁遭羈押",            # Chen detained Nov 2008, not 2006
    "消費券政策宣布",          # Consumer vouchers were announced in 2008, not 2006
    "兩岸全面三通啟動",        # Full Three Links launched Dec 2008, not 2006
    # REDUNDANT — covered by other 2006 events that are being kept
    "謝長廷辭閣揆",            # Precursor to 蘇貞昌內閣上任; administrative transition step
    "蘇貞昌將接任閣揆",        # Duplicate announcement; 蘇貞昌內閣上任 is the milestone
    "圍陳抗議爆警民衝突",      # Sub-event of Red Shirt movement; covered by 倒扁紅衫軍啟動
    "江陳會台北登場",          # Uncertain event; formal SEF-ARATS talks resumed in 2008
    # BORDERLINE — below national landmark threshold
    "游錫堃當選黨主席",        # Routine party internal election
    "北宜高頭城蘇澳通車",      # Regional highway section; not national landmark
    "林義傑極地馬拉松奪冠",    # Individual athletic achievement
    "高速公路電子收費啟用",    # Infrastructure technology rollout
    "崇德新城工安撞車案",      # Local accident; no lasting policy significance
    "龔照勝遭停職",            # Individual official case; limited national significance
    "顏萬進遭收押",            # Individual judicial case; limited national significance
    "遠通ETC資格遭撤銷",       # Infrastructure contract dispute; not a landmark
    "王建民奪第19勝",          # Individual sports milestone; not national historical event
    "米迪亞假球案爆發",        # Sports scandal; below significance of 2009 黑象事件
    "反黑心顧台灣遊行",        # Repetitive protest; covered by main Red Shirt events
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

print(f"\nRemoved {removed} borderline/error events")
print(f"Updated {updated} events with URLs")

events_2006 = [e for e in result if e['date'].startswith('2006')]
with_url = [e for e in events_2006 if e.get('source_url', '')]
print(f"2006: {len(events_2006)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
