#!/usr/bin/env python3
"""Second curation pass: remove borderline events from all years."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Events to REMOVE (by exact title match) - not major historical events
remove_titles = {
    # 2025 - daily military follow-ups (main event already captured)
    "共軍軍演後國軍持續高戒備",
    "國軍啟動立即備戰操演",
    "共軍對臺實施大規模實彈射擊",  # part of 正義使命 exercise
    "五一勞工遊行登場",  # annual routine
    "韌性特別條例送審",  # process, not outcome
    "M1A2T戰車首度營外演訓",  # minor military
    "全社會防衛韌性委員會定調法制化",  # process
    # 2024 - minor
    "晚安小雞事件",  # viral internet, not historical
    "高捷岡山車站啟用",  # routine infrastructure
    "行人交通安全設施條例三讀",  # minor legislation
    "賓士衝撞總統府",  # minor incident
    "德軍艦通過台海",  # routine transit
    "柯文哲政治獻金風波記者會",  # process (arrest event kept)
    # 2023 - minor
    "新埔站冷氣砸死人",  # accident
    "飛龍瀑布溯溪意外",  # accident
    "安坑輕軌通車",  # routine infrastructure
    "王鴻薇當選北市立委",  # by-election
    "蔡培慧當選南投立委",  # by-election
    # 2022 - minor
    "林姿妙涉弊遭搜索",  # minor political
    "林靜儀贏得中二補選",  # by-election
    "東南水泥壓斷電塔",  # minor
    "開放中國快篩試劑輸入",  # minor policy
    "台鐵工會發動依法休假",  # labor action
    # 2021 - minor
    "鮭魚之亂爆發",  # viral trend
    "長賜號阻塞蘇伊士運河",  # foreign event
    "陽明交大正式合校",  # routine admin
    "F5E戰機擦撞墜海",  # accident (太魯閣號 already kept)
    # 2020 - minor
    "賴清德訪美出席祈禱早餐會",  # routine
    "環狀線正式通車",  # routine infrastructure
    # 2026 - further trim
    "二二八79週年中樞紀念儀式",  # annual routine (228 event itself in 1947 is kept)
    "台灣連十年調升基本工資",  # routine policy
    "主計總處估2025經濟成長8.63%",  # routine economic data
}

filtered = [e for e in data if e['title'] not in remove_titles]

removed = len(data) - len(filtered)
print(f"Removed {removed} more events")
print(f"Total: {len(filtered)}")

from collections import Counter
years = Counter(e['date'][:4] for e in filtered)
for y in sorted(years.keys(), reverse=True)[:10]:
    print(f"  {y}: {years[y]}")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"Saved {len(filtered)} events.")
