#!/usr/bin/env python3
"""Curate events.json: keep only genuine major historical events."""
import json, sys, io, copy

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data)

# === 2026: Explicit keep-list (titles of events to KEEP) ===
keep_2026 = {
    "鄭習會登場",
    "中共宣布十項惠台措施",
    "鄭麗文結束訪陸返台",
    "國民黨主席鄭麗文啟程訪陸",
    "柯文哲京華城案一審判刑十七年",
    "賴清德宣布評估核電重啟",
    "WBC經典賽中華隊止步預賽",
    "台積電帶動臺股首登3萬點",
    "臺美完成關稅協議",
    "F16V戰機花東外海失聯",
    "共軍無人機闖東沙領空",
    "海鯤號首度潛航測試成功",
    "美國眾院通過臺灣保護法案",
    "白沙屯媽祖進香起駕",
    "陳菊因健康因素請辭監察觀長",  # typo check below
    "陳菊因健康因素請辭監察院長",
    "賴清德與習近平通話成國際焦點",
    "二二八79週年中樞紀念儀式",
    "霍諾德徒手攀登台北101",
    "台灣新生兒數再創新低",
    "中天記者涉共諜案遭羈押",
    "海鯤號海測影片公開",
    "台灣首度在WBC擊敗韓國",
    "立院通過國民黨版國防特別條例",
    "美台簽署對等貿易協定",
    "藍白會期末通過中天條款與黨續條例修法",  # check
    "藍白會期末通過中天條款與黨產條例修法",
    "總統特赦長照悲劇八旬婦人",
    "賴清德發表元旦談話",
    "卓榮泰成台日斷交後首位公開訪日閣揆",
    "第三批M1A2T戰車完成生產",
    "共機大舉擾台二十六架次",  # noteworthy if largest
    "美國授權新一輪對台大型軍售",
    "共軍發動正義使命2025圍臺軍演",  # wait this is 2025
    "李貞秀雙重戶籍與國籍爭議升高",  # keep as political controversy
    "賴清德推客家六箭政策",  # actually minor, remove
    "日本眾院大選自民黨壓倒性勝利",  # foreign event, remove
    "共機大規模擾臺再現高峰",
    "中共宣布恢復上海居民赴金馬旅遊",
    "美國撥款法轊編列對臺軍援",  # check
    "美國撥款法案編列對臺軍援",
    "海鯤號完成第六次潛航測試",  # merge with earlier tests?
    "台灣連十年調升基本工資",
    "主計總處估2025經濟成長8.63%",
    "中共公布沈伯洋住居衛星影像",  # intimidation, noteworthy
    "考試院就停砍年金聲請釋憲",
    "中共點名劉世芳親屬投資遭查處",  # intimidation
    "勁蜂一型無人機首度實彈射擊公開",
    "台灣總統直選三十週年研討會登場",
}

# Actually let me be more selective - truly MAJOR events only
keep_2026_final = {
    # Cross-strait landmark
    "鄭習會登場",
    "中共宣布十項惠台措施",
    "國民黨主席鄭麗文啟程訪陸",
    "鄭麗文結束訪陸返台",
    "賴清德與習近平通話成國際焦點",
    "中共宣布恢復上海居民赴金馬旅遊",
    # Judicial
    "柯文哲京華城案一審判刑十七年",
    "中天記者涉共諜案遭羈押",
    "總統特赦長照悲劇八旬婦人",
    # Energy policy
    "賴清德宣布評估核電重啟",
    # Sports
    "WBC經典賽中華隊止步預賽",
    "台灣首度在WBC擊敗韓國",
    # Economy
    "台積電帶動臺股首登3萬點",
    "臺美完成關稅協議",
    "美台簽署對等貿易協定",
    "主計總處估2025經濟成長8.63%",
    "台灣連十年調升基本工資",
    # Military/defense
    "F16V戰機花東外海失聯",
    "共軍無人機闖東沙領空",
    "海鯤號首度潛航測試成功",
    "美國眾院通過臺灣保護法案",
    "共機大舉擾台二十六架次",
    "美國授權新一輪對台大型軍售",
    "第三批M1A2T戰車完成生產",
    "立院通過國民黨版國防特別條例",
    # Politics
    "陳菊因健康因素請辭監察院長",
    "藍白會期末通過中天條款與黨產條例修法",
    "賴清德發表元旦談話",
    "二二八79週年中樞紀念儀式",
    "台灣新生兒數再創新低",
    # Social/cultural
    "白沙屯媽祖進香起駕",
    "霍諾德徒手攀登台北101",
    # Diplomacy
    "卓榮泰成台日斷交後首位公開訪日閣揆",
}

# === 2025: Explicit keep-list ===
keep_2025 = {
    # Military
    "共軍發動正義使命2025圍臺軍演",
    "共軍對臺實施大規模實彈射擊",
    "國軍啟動立即備戰操演",
    "共軍軍演後國軍持續高戒備",
    "M1A2T戰車首度營外演訓",
    "海鯤號首次海測",
    "共軍再啟環台軍演",
    "賴清德宣布恢復軍審",
    # Disasters
    "宜蘭外海規模7.0地震",
    "嘉義大埔規模6.4地震",
    # Politics
    "立院啟動彈劾賴清德程序",
    "黃國昌當選民眾黨主席",
    "柯文哲辭民眾黨主席",
    "美國簽署友台國防授權法",
    "憲法訴訟法修法遭判違憲",
    "大罷免首輪全數未過",
    "第二輪罷免與核三公投未過",
    "韌性特別預算與普發現金",
    "韌性特別條例送審",
    "政院對反年改修法聲請釋憲",
    "黃麟凱遭執行死刑",
    "大罷免第一波案成案",
    # Economy
    "臺股創歷史新高封關",
    "台積電宣布對美增資",
    "核三廠正式停機",
    # Social
    "台北無差別攻擊案",  # or 台北捷運隨機攻擊案
    "台北捷運隨機攻擊案",
    "剴剴虐童案一審宣判",
    "五億高中案不起訴確定",
    "桃機第三航廈北廊廳啟用",
    "世壯運雙北開幕",
    "三峽重大車輛衝撞案",
    "輝達宣布設台灣總部",
    "台中新光三越氣爆",
    "五一勞工遊行登場",
    "貴婦奈奈返台投案",
    "亞亞離台事件",
    "非洲豬瘟感染事件",
    "馬太鞍溪堰塞湖溢流災變",
    "解嚴時長超越戒嚴時長",
    # Culture/Sports
    "樂天桃猿奪中職總冠軍",
    "統一獅奪第18座季冠軍",
    "第36屆金曲獎登場",
    # Defense
    "美國再批准大規模對臺軍售",
    "全社會防衛韌性委員會定調法制化",
}

# Filter 2026 and 2025
filtered = []
removed_2026 = 0
removed_2025 = 0

for ev in data:
    year = ev['date'][:4]
    if year == '2026':
        if ev['title'] in keep_2026_final:
            filtered.append(ev)
        else:
            removed_2026 += 1
    elif year == '2025':
        if ev['title'] in keep_2025:
            filtered.append(ev)
        else:
            removed_2025 += 1
    else:
        filtered.append(ev)

# De-duplicate: if there are events with very similar titles in 2025, keep only one
# Check for台北無差別攻擊案 vs 台北捷運隨機攻擊案 (same event on same date)
seen = set()
deduped = []
for ev in filtered:
    key = (ev['date'], ev['title'])
    if key in seen:
        continue
    # Special dedup: same date, same event described differently
    if ev['date'] == '2025-12-19' and ev['title'] in ('台北無差別攻擊案', '台北捷運隨機攻擊案'):
        dedup_key = ('2025-12-19', 'taipei_attack')
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
    if ev['date'] == '2025-06-21' and '金曲獎' in ev['title']:
        dedup_key = ('2025-06', 'golden_melody')
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
    seen.add(key)
    deduped.append(ev)

filtered = deduped

# Also check for duplicate events across 2025-12-29~31 military exercise
# 共軍發動正義使命2025圍臺軍演 and related updates should be consolidated
# Keep the main event, remove daily updates
exercise_dates = set()
exercise_main = None
final = []
for ev in filtered:
    final.append(ev)

print(f"Original: {original_count}")
print(f"Removed from 2026: {removed_2026}")
print(f"Removed from 2025: {removed_2025}")
print(f"After dedup: {len(final)}")

# Count by year
from collections import Counter
years = Counter(e['date'][:4] for e in final)
for y in sorted(years.keys(), reverse=True)[:10]:
    print(f"  {y}: {years[y]}")

# Print kept 2026 events
print("\n=== Kept 2026 events ===")
for e in final:
    if e['date'].startswith('2026'):
        print(f"  {e['date']} {e['title']}")

print("\n=== Kept 2025 events ===")
for e in final:
    if e['date'].startswith('2025'):
        print(f"  {e['date']} {e['title']}")

# Save
with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(final)} events.")
