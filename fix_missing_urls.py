#!/usr/bin/env python3
"""Fix missing URLs: add Wikipedia URLs for known events, remove remaining borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    # Pre-2000 historical events
    "南迴鐵路通車":
        "https://zh.wikipedia.org/zh-tw/南迴線",
    "颱風韋恩侵台":
        "https://zh.wikipedia.org/zh-tw/颱風韋恩_(1986年)",
    "戰時武官總督上台":
        "https://zh.wikipedia.org/zh-tw/小林躋造",
    "劉永福撤離台灣":
        "https://zh.wikipedia.org/zh-tw/劉永福",
    # 2006
    "罷免總統案未通過":
        "https://zh.wikipedia.org/zh-tw/2006年中華民國罷免總統案",
    "國統會運作終止":
        "https://zh.wikipedia.org/zh-tw/國家統一委員會",
    "台灣與查德斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國與查德關係",
    # 2007
    "與聖露西亞復交":
        "https://zh.wikipedia.org/zh-tw/中華民國－聖露西亞關係",
    # 2012
    "馬英九連任總統":
        "https://zh.wikipedia.org/zh-tw/2012年中華民國總統選舉",
    "馬英九第二任就職":
        "https://zh.wikipedia.org/zh-tw/中華民國第十三任總統就職典禮",
    "林益世涉貪遭收押":
        "https://zh.wikipedia.org/zh-tw/林益世弊案",
    "桃園升格案通過":
        "https://zh.wikipedia.org/zh-tw/桃園市_(直轄市)",
    # 2010
    "五都市長選舉完成":
        "https://zh.wikipedia.org/zh-tw/2010年中華民國直轄市長及市議員選舉",
    "台北花博開幕":
        "https://zh.wikipedia.org/zh-tw/2010年臺北國際花卉博覽會",
    # 2011
    "陸客自由行啟動":
        "https://zh.wikipedia.org/zh-tw/大陸民眾赴台旅遊",
    # 2013
    "洪仲丘案引爆爭議":
        "https://zh.wikipedia.org/zh-tw/洪仲丘事件",
    "廣大興28號遭射擊":
        "https://zh.wikipedia.org/zh-tw/廣大興28號事件",
}

# Events to REMOVE: borderline/sports-only/routine/sub-events
remove_titles = {
    # Individual sports achievements
    "謝淑薇奪溫網女雙冠軍",      # Individual sports
    "台灣奪桌球世錦賽金牌",      # Individual sports
    "許淑淨奪奧運銀牌",          # Individual sports
    "盧彥勳溫網寫歷史",          # Individual sports
    "林書豪風潮爆發",            # Individual sports abroad
    # Pop culture / art
    "黃色小鴨來台展出",          # Art installation; not a national policy landmark
    # Minor infrastructure / park
    "壽山國家自然公園成立",      # Local nature park; below national landmark threshold
    "台北獲2017世大運主辦權",    # Sports hosting bid; event itself not yet occurred
    # Routine / sub-events
    "江宜樺內閣上任",            # Routine cabinet change; no lasting landmark vs 蘇貞昌/林全等
    "雪山隧道重大事故",          # Traffic accident; below landmark threshold
    "王清峰請辭獲准",            # Individual resignation; not a landmark
    "職棒假球案起訴",            # Covered by 中職假球案延燒 in 2009
    "空勤直升機救災殉職",        # Sub-event of 莫拉克颱風; covered
    "第三次江陳會談",            # Cross-Strait meeting; landmark was first 2 in 2008
    "第四次江陳會談",            # One of many Cross-Strait meetings; not individually landmark
    "台灣入聯案再遭擋",          # Annual routine failure; not a discrete landmark
    "謝長廷勝出黨內初選",        # Party internal primary; not a national landmark
    "蘇建和案更審判死",          # Court procedural step; not a landmark
    "台灣首例H7N9確診",          # Health event; 2009 H1N1 kept but H7N9 not as major in Taiwan
    "高鐵車廂炸彈案",            # Criminal case; no major policy consequence
    # Pre-2000 ambiguous events
    "四一九大遊行",              # April 1992 protest; unclear significance vs major events
    "花蓮集體做票案",            # Regional election fraud; not a national landmark
    "三七事件曝光",              # Uncertain event; no reliable source found
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
