#!/usr/bin/env python3
"""Upgrade URLs: replace Wikipedia placeholders with better specific sources."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Replace these existing URLs with better ones
upgrade_map = {
    # Better: Official Constitutional Court ruling page (釋字613號)
    "NCC組織法部分違憲": {
        "old": "https://zh.wikipedia.org/zh-tw/國家通訊傳播委員會",
        "new": "https://cons.judicial.gov.tw/jcc/zh-tw/jep03/show?expno=613",
    },
    # Better: specific Wikipedia article for the family accounts scandal
    "扁家四大案起訴": {
        "old": "https://zh.wikipedia.org/zh-tw/陳水扁",
        "new": "https://zh.wikipedia.org/zh-tw/陳水扁家庭密帳案",
    },
    # Better: LTN contemporaneous news article
    "十二年國教宣布推動": {
        "old": "https://zh.wikipedia.org/zh-tw/十二年國民基本教育",
        "new": "https://news.ltn.com.tw/news/focus/paper/457107",
    },
    # Better: PTS (public broadcaster) news article
    "法務部恢復執行死刑": {
        "old": "https://zh.wikipedia.org/zh-tw/中華民國死刑制度",
        "new": "https://news.pts.org.tw/article/229018",
    },
    # Better: LTN focus article
    "台北花博開幕": {
        "old": "https://zh.wikipedia.org/zh-tw/2010年臺北國際花卉博覽會",
        "new": "https://news.ltn.com.tw/news/focus/paper/427832",
    },
    # Better: LTN news article (Chen enters prison Dec 2010)
    "陳水扁入監服刑": {
        "old": "https://theme.udn.com/theme/story/7491/622114",
        "new": "https://news.ltn.com.tw/news/focus/paper/843253",
    },
    # Better: LTN focus article for the 818 protest
    "八一八反迫遷行動": {
        "old": "https://zh.wikipedia.org/zh-tw/大埔事件",
        "new": "https://news.ltn.com.tw/news/focus/paper/706434",
    },
    # Better: LTN society news article
    "洪仲丘案引爆爭議": {
        "old": "https://zh.wikipedia.org/zh-tw/洪仲丘事件",
        "new": "https://news.ltn.com.tw/news/society/breakingnews/848213",
    },
    # Better: specific Wikipedia article for the 2013 cooking oil scandal
    "油品混充爭議擴大": {
        "old": "https://zh.wikipedia.org/zh-tw/大統長基食品廠食品問題",
        "new": "https://zh.wikipedia.org/zh-tw/2013年臺灣食用油油品事件",
    },
    # Better: specific Wikipedia article for ASE wastewater incident
    "日月光排廢水遭罰": {
        "old": "https://zh.wikipedia.org/zh-tw/日月光半導體排放廢水事件",
        "new": "https://zh.wikipedia.org/zh-tw/2013年日月光半導體廢水事件",
    },
    # Better: LTN news article
    "美牛有條件解禁": {
        "old": "https://zh.wikipedia.org/zh-tw/台灣萊克多巴胺爭議",
        "new": "https://news.ltn.com.tw/news/life/breakingnews/611675",
    },
    # Better: LTN politics news article
    "林益世涉貪遭收押": {
        "old": "https://zh.wikipedia.org/zh-tw/林益世弊案",
        "new": "https://news.ltn.com.tw/news/politics/breakingnews/661462",
    },
    # Better: LTN life news article
    "毒澱粉食安風暴": {
        "old": "https://zh.wikipedia.org/zh-tw/台灣順丁烯二酸化製澱粉事件",
        "new": "https://news.ltn.com.tw/news/life/breakingnews/815088",
    },
}

result = []
upgraded = 0
not_found = []

for ev in data:
    if ev['title'] in upgrade_map:
        upgrade = upgrade_map[ev['title']]
        current = ev.get('source_url', '')
        if current == upgrade['old']:
            ev['source_url'] = upgrade['new']
            upgraded += 1
            print(f"UPGRADED: {ev['date']} {ev['title']}")
            print(f"  OLD: {upgrade['old']}")
            print(f"  NEW: {upgrade['new']}")
        elif current == upgrade['new']:
            print(f"ALREADY UPGRADED: {ev['date']} {ev['title']}")
        else:
            not_found.append(f"{ev['date']} {ev['title']} (current: {current[:60]}...)")
    result.append(ev)

print(f"\nUpgraded {upgraded} URLs")
if not_found:
    print(f"\nCould not match (different existing URL):")
    for nf in not_found:
        print(f"  {nf}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(result)} events.")
