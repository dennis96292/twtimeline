#!/usr/bin/env python3
"""Update 2005 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "三合一選舉完成":
        "https://zh.wikipedia.org/zh-tw/2005年中華民國縣市長選舉",
    "與塞內加爾斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國－塞內加爾關係",
    "按捺指紋規定違憲":
        "https://zh.wikipedia.org/zh-tw/釋字第603號解釋",
    "對日免簽正式上路":
        "https://zh.wikipedia.org/zh-tw/日本免簽證入境地區",
    "高捷泰勞深夜抗爭":
        "https://zh.wikipedia.org/zh-tw/高雄捷運泰勞事件",
    "中華電信完成民營化":
        "https://zh.wikipedia.org/zh-tw/中華電信",
    "馬英九當選黨主席":
        "https://zh.wikipedia.org/zh-tw/2005年中國國民黨黨主席選舉",
    "原住民族日入法":
        "https://zh.wikipedia.org/zh-tw/臺灣原住民族日",
    "國民大會正式廢除":
        "https://zh.wikipedia.org/zh-tw/中華民國國民大會",
    "親民黨展開搭橋之旅":
        "https://zh.wikipedia.org/zh-tw/2005年親民黨搭橋之旅",
    "國民黨展開和平之旅":
        "https://zh.wikipedia.org/zh-tw/2005年中國國民黨和平之旅",
    "三二六護台灣遊行":
        "https://zh.wikipedia.org/zh-tw/三二六護台灣大遊行",
    "春節包機澳門協議":
        "https://zh.wikipedia.org/zh-tw/兩岸包機",
}

# Events to REMOVE: borderline/trivial/redundant
remove_titles = {
    "高捷中正地下道塌陷",    # Construction accident; local significance only
    "台灣可自製克流感",      # Medical capability announcement; not a landmark
    "中時晚報停刊",          # Media closure; not a national landmark
    "楊儒門一審判刑",        # Individual criminal case; not a landmark
    "選舉無效案定讞敗訴",    # Procedural ruling; subsumed by 陳水扁連任 narrative
    "台灣叩關聯合國失敗",    # Annual routine failure; not a discrete landmark
    "南部砂石弊案起訴",      # Local corruption case; not a landmark
    "三一九案偵查結案",      # Procedural closure; not a landmark
    "民主太平洋聯盟成立",    # Regional diplomatic group; limited significance
    "日本通過台灣觀光免簽",  # Legislative process; subsumed by 對日免簽正式上路
    "類鼻疽疫情擴大",        # Regional public health event; not a national landmark
    "中職假球風暴再起",      # Sports scandal recurrence; below landmark threshold
    "海棠颱風造成死傷",      # Routine typhoon; no uniquely landmark destruction
    "張錫銘中彈落網",        # Individual criminal capture; not a national landmark
    "吳珈慶奪撞球世界冠軍",  # Individual sports achievement; not national landmark
    "當選無效案定讞敗訴",    # Procedural ruling (duplicate theme); below landmark
    "六一二水災爆發",        # Regional flooding; not a landmark disaster
    "毒蠻牛事件爆發",        # Consumer safety incident; not a lasting landmark
    "台灣與諾魯建交",        # Diplomatic recognition (not severance); less landmark
    "任務型國代選舉舉行",    # Procedural electoral step; subsumed by 國民大會正式廢除
    "文山溫泉坍方意外",      # Local accident; no lasting policy significance
    "謝長廷接任閣揆",        # Routine cabinet change; no lasting landmark significance
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

events_2005 = [e for e in result if e['date'].startswith('2005')]
with_url = [e for e in events_2005 if e.get('source_url', '')]
print(f"2005: {len(events_2005)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
