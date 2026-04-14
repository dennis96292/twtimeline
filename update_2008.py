#!/usr/bin/env python3
"""Update 2008 events: add verified source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    "立委單一選區改制首選":
        "https://www.cna.com.tw/news/aipl/202401055002.aspx",
    "與馬拉威斷交":
        "https://global.udn.com/global_vision/story/8663/1628600",
    "高雄捷運紅線通車":
        "https://news.ltn.com.tw/news/Kaohsiung/breakingnews/5363912",
    "賽德克族獲正名":
        "https://news.ltn.com.tw/news/local/paper/206510",
    "蔡英文當選民進黨主席":
        "https://vip.udn.com/vip/story/121160/6321173",
    "馬英九就任總統":
        "https://vip.udn.com/vip/story/121160/5249600",
    "聯合號遭日艦撞沉":
        "https://m.ltn.com.tw/news/politics/paper/218774",
    "兩會協商恢復":
        "https://www.cna.com.tw/news/acn/202409080061.aspx",
    "奧運棒球敗給中國":
        "https://sports.ltn.com.tw/news/paper/1456705",
    "后豐大橋遭洪水沖斷":
        "https://news.ltn.com.tw/news/society/breakingnews/128167",
    "國民年金正式上路":
        "https://vip.udn.com/vip/story/121160/4899672",
    "王永慶病逝美國":
        "https://ec.ltn.com.tw/article/breakingnews/139418",
    "陳水扁首度遭收押":
        "https://vip.udn.com/vip/story/121160/5004366",
    "野草莓運動全台串連":
        "https://time.udn.com/udntime/story/122833/7538997",
    "消費券政策拍板":
        "https://time.udn.com/udntime/story/122833/7045421",
    "兩岸全面三通實施":
        "https://vip.udn.com/vip/story/121160/5959841",
    "第二次江陳會談登場":
        "https://news.ltn.com.tw/news/politics/paper/258840",
    "陳水扁登太平島":
        "https://news.ltn.com.tw/news/politics/paper/187930",
}

# Events to REMOVE: redundant/borderline/data errors
remove_titles = {
    "蔡明憲任首位文人國防部長",  # Cabinet appointment; no mass public impact; no clean URL
    "中華隊取得奧運門票",        # Sports qualification; 奧運棒球敗給中國 is the landmark moment
    "信義鄉土石流埋車",          # Same typhoon as 后豐大橋; less nationally iconic
    "反黑心顧台灣再遊行",        # Repetitive protest; no landmark significance; no clean URL
    "圍陳爆發流血衝突",          # Sub-event absorbed into 野草莓運動全台串連 narrative
    "扁家四大弊案起訴",          # Consolidated into 陳水扁首度遭收押 (detention is more landmark)
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

events_2008 = [e for e in result if e['date'].startswith('2008')]
with_url = [e for e in events_2008 if e.get('source_url', '')]
print(f"2008: {len(events_2008)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
