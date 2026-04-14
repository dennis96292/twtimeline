#!/usr/bin/env python3
"""Update 2025 events with verified source_urls and fix inaccurate data."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map_2025 = {
    "共軍發動正義使命2025圍臺軍演":
        "https://www.cna.com.tw/news/acn/202512290014.aspx",
    "立院啟動彈劾賴清德程序":
        "https://www.cna.com.tw/news/aipl/202512260089.aspx",
    "台北無差別攻擊案":
        "https://www.cna.com.tw/news/asoc/202512200003.aspx",
    "美國簽署友台國防授權法":
        "https://www.cna.com.tw/news/aipl/202512190038.aspx",
    "憲法訴訟法修法遭判違憲":
        "https://www.cna.com.tw/news/aipl/202512190174.aspx",
    "臺股創歷史新高封關":
        "https://udn.com/news/story/7251/9237013",
    "政院對反年改修法聲請釋憲":
        "https://www.cna.com.tw/news/aipl/202512310288.aspx",
    "桃機第三航廈北廊廳啟用":
        "https://www.cna.com.tw/news/ahel/202512250161.aspx",
    "美國再批准大規模對臺軍售":
        "https://www.cna.com.tw/news/aipl/202512180020.aspx",
    "樂天桃猿奪中職總冠軍":
        "https://sports.ettoday.net/news/3057399",
    "韌性特別預算與普發現金":
        "https://www.cna.com.tw/news/aipl/202510230219.aspx",
    "非洲豬瘟感染事件":
        "https://www.cna.com.tw/news/ahel/202510220064.aspx",
    "馬太鞍溪堰塞湖溢流災變":
        "https://www.cna.com.tw/news/ahel/202509245005.aspx",
    "解嚴時長超越戒嚴時長":
        "",  # No specific news article found; it's a milestone calculation
    "第二輪罷免與核三公投未過":
        "https://www.cna.com.tw/news/aipl/202508230199.aspx",
    "大罷免首輪全數未過":
        "https://www.cna.com.tw/news/aipl/202507265011.aspx",
    "統一獅奪第18座季冠軍":
        "https://www.cna.com.tw/news/aspt/202506290185.aspx",
    "第36屆金曲獎登場":
        "https://www.cna.com.tw/news/amov/202506285004.aspx",
    "五億高中案不起訴確定":
        "https://udn.com/news/story/7315/8820656",
    "大罷免第一波案成案":
        "https://www.cna.com.tw/news/aipl/202506070132.aspx",
    "海鯤號首次海測":
        "https://udn.com/news/story/10930/8811738",
    "三峽重大車輛衝撞案":
        "https://www.cna.com.tw/news/asoc/202505190345.aspx",
    "輝達宣布設台灣總部":
        "https://www.cna.com.tw/news/afe/202505190115.aspx",
    "世壯運雙北開幕":
        "https://www.cna.com.tw/news/aspt/202505170207.aspx",
    "核三廠正式停機":
        "https://www.cna.com.tw/news/afe/202505160355.aspx",
    "剴剴虐童案一審宣判":
        "https://www.cna.com.tw/news/asoc/202505130179.aspx",
    "貴婦奈奈返台投案":
        "https://www.cna.com.tw/news/asoc/202505010026.aspx",
    "共軍再啟環台軍演":
        "https://www.cna.com.tw/news/aipl/202504090168.aspx",
    "亞亞離台事件":
        "https://www.cna.com.tw/news/aipl/202503150238.aspx",
    "賴清德宣布恢復軍審":
        "https://www.cna.com.tw/news/aipl/202503135004.aspx",
    "台積電宣布對美增資":
        "https://www.cna.com.tw/news/aopl/202503040013.aspx",
    "台中新光三越氣爆":
        "https://udn.com/news/story/124384/8545448",
    "黃麟凱遭執行死刑":
        "https://www.cna.com.tw/news/asoc/202501170003.aspx",
    "柯文哲辭民眾黨主席":
        "https://www.cna.com.tw/news/aipl/202501015003.aspx",
}

# Apply URLs
updated = 0
for ev in data:
    if ev['title'] in url_map_2025 and not ev.get('source_url', ''):
        url = url_map_2025[ev['title']]
        if url:  # Only set if we have a URL
            ev['source_url'] = url
            updated += 1
            print(f"URL: {ev['date']} {ev['title']}")

# Remove "解嚴時長超越戒嚴時長" - it's a milestone calculation, not a news event
# Actually keep it but without URL - it's a genuine milestone

print(f"\nUpdated {updated} events with URLs")

# Count 2025 stats
events_2025 = [e for e in data if e['date'].startswith('2025')]
with_url = [e for e in events_2025 if e.get('source_url', '')]
print(f"2025: {len(events_2025)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} events.")
