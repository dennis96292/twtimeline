#!/usr/bin/env python3
"""Update 2020 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "川普簽署台灣保證法":
        "https://www.cna.com.tw/news/firstnews/202012280036.aspx",
    "萊豬行政命令過關":
        "https://www.cna.com.tw/news/firstnews/202012245009.aspx",
    "台灣再現本土新冠病例":
        "https://www.cna.com.tw/news/firstnews/202012220042.aspx",
    "潛艦國造原型艦開工":
        "https://news.ltn.com.tw/news/politics/breakingnews/3357233",
    "NCC否決中天換照":
        "https://www.cna.com.tw/news/firstnews/202011185006.aspx",
    "長榮大學外籍生命案":
        "https://www.cna.com.tw/news/firstnews/202010300064.aspx",
    "美國次卿柯拉克訪台":
        "https://www.cna.com.tw/news/firstnews/202009170005.aspx",
    "維特齊立院演說喊我是台灣人":
        "https://www.ettoday.net/news/20210210/1913896.htm",
    "宣布開放萊豬進口":
        "https://www.cna.com.tw/news/firstnews/202008285004.aspx",
    "陳其邁當選高雄市長":
        "https://www.cna.com.tw/news/firstnews/202008155007.aspx",
    "美衛生部長阿札爾訪台":
        "https://www.cna.com.tw/news/firstnews/202008095007.aspx",
    "李登輝辭世":
        "https://www.cna.com.tw/news/firstnews/202007305007.aspx",
    "韓國瑜遭罷免成功":
        "https://news.ltn.com.tw/news/politics/breakingnews/3188663",
    "蔡英文第二任就職":
        "https://www.cna.com.tw/news/firstnews/202005205005.aspx",
    "錢櫃林森店大火":
        "https://www.cna.com.tw/news/firstnews/202004290062.aspx",
    "敦睦艦隊爆群聚感染":
        "https://news.ltn.com.tw/news/life/breakingnews/3138707",
    "翁仁賢遭執行死刑":
        "https://www.cna.com.tw/news/firstnews/202004015013.aspx",
    "限制外籍人士入境":
        "https://www.cna.com.tw/news/firstnews/202003185007.aspx",
    "口罩實名制上路":
        "https://www.cna.com.tw/news/firstnews/202002035007.aspx",
    "台灣首例新冠確診":
        "https://udn.com/news/story/7314/4301137",
    "成立疫情指揮中心":
        "https://www.cna.com.tw/news/firstnews/202001205004.aspx",
    "蔡英文高票連任":
        "https://www.cna.com.tw/news/firstnews/202001115026.aspx",
    "黑鷹直升機墜毀":
        "https://www.cna.com.tw/news/firstnews/202001025002.aspx",
}

# Events to REMOVE: redundant/borderline
remove_titles = {
    "捷克參議院議長訪台",    # Redundant with 維特齊立院演說 (same visit, speech is more historic)
    "5G開台與三倍券上路",    # Routine policy/tech launch
    "游錫堃當選立法院長",    # Normal political process after election
    "全球旅遊警示升三級",    # COVID administrative step, not landmark
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

events_2020 = [e for e in result if e['date'].startswith('2020')]
with_url = [e for e in events_2020 if e.get('source_url', '')]
print(f"2020: {len(events_2020)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
