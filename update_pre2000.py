#!/usr/bin/env python3
"""Update pre-2000 events: add verified Wikipedia source_urls, remove borderline events."""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/events.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

url_map = {
    # 1999
    "九二一大地震":
        "https://zh.wikipedia.org/zh-tw/921大地震",
    "全台無預警大停電":
        "https://zh.wikipedia.org/zh-tw/1999年台灣大停電",
    "兩國論引發震盪":
        "https://zh.wikipedia.org/zh-tw/特殊的國與國關係",
    # 1998
    "華航大園空難":
        "https://zh.wikipedia.org/zh-tw/中華航空676號班機空難",
    "腸病毒疫情爆發":
        "https://zh.wikipedia.org/zh-tw/1998年台灣腸病毒疫情",
    # 1997
    "民進黨縣市長大勝":
        "https://zh.wikipedia.org/zh-tw/1997年中華民國縣市長選舉",
    "林肯大郡坍塌":
        "https://zh.wikipedia.org/zh-tw/林肯大郡事件",
    "白曉燕綁架命案":
        "https://zh.wikipedia.org/zh-tw/白曉燕命案",
    "口蹄疫疫情肆虐":
        "https://zh.wikipedia.org/zh-tw/1997年台灣口蹄疫",
    # 1996
    "彭婉如命案":
        "https://zh.wikipedia.org/zh-tw/彭婉如命案",
    "劉邦友血案":
        "https://zh.wikipedia.org/zh-tw/劉邦友血案",
    "賀伯颱風侵台":
        "https://zh.wikipedia.org/zh-tw/颱風賀伯",
    "台海飛彈危機":
        "https://zh.wikipedia.org/zh-tw/1995年至1996年台灣海峽飛彈危機",
    # 1995
    "李登輝康乃爾演說":
        "https://zh.wikipedia.org/zh-tw/李登輝訪美事件",
    "全民健保開辦":
        "https://zh.wikipedia.org/zh-tw/全民健康保險",
    "政府為二二八道歉":
        "https://zh.wikipedia.org/zh-tw/二二八事件",
    "衛爾康大火":
        "https://zh.wikipedia.org/zh-tw/衛爾康西餐廳火災",
    # 1994
    "省市長首次民選":
        "https://zh.wikipedia.org/zh-tw/1994年中華民國省市長暨省市議員選舉",
    "山胞正名為原住民":
        "https://zh.wikipedia.org/zh-tw/台灣原住民族",
    "華航名古屋空難":
        "https://zh.wikipedia.org/zh-tw/中華航空140號班機空難",
    "千島湖事件受害":
        "https://zh.wikipedia.org/zh-tw/千島湖事件",
    # 1993
    "新黨成立":
        "https://zh.wikipedia.org/zh-tw/新黨_(台灣)",
    "首次辜汪會談":
        "https://zh.wikipedia.org/zh-tw/辜汪會談",
    "論情西餐廳大火":
        "https://zh.wikipedia.org/zh-tw/論情西餐廳火災",
    "中國劫機潮來台":
        "https://zh.wikipedia.org/zh-tw/1993年兩岸劫機事件",
    # 1992
    "金馬解除戰地政務":
        "https://zh.wikipedia.org/zh-tw/戰地政務",
    "與南韓斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國－韓國關係",
    "奧運棒球奪銀":
        "https://zh.wikipedia.org/zh-tw/1992年夏季奧林匹克運動會棒球",
    "刑法一百條修正":
        "https://zh.wikipedia.org/zh-tw/刑法第100條",
    "健康幼稚園火燒車":
        "https://zh.wikipedia.org/zh-tw/健康幼稚園火燒車事故",
    # 1991
    "資深中央民代退職":
        "https://zh.wikipedia.org/zh-tw/萬年國會",
    "國代全面改選":
        "https://zh.wikipedia.org/zh-tw/1991年中華民國國民大會代表選舉",
    "獨台會案開端":
        "https://zh.wikipedia.org/zh-tw/獨台會案",
    "動員戡亂時期終結":
        "https://zh.wikipedia.org/zh-tw/動員戡亂時期",
    # 1990
    "與沙烏地斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國－沙烏地阿拉伯關係",
    "中華職棒開幕":
        "https://zh.wikipedia.org/zh-tw/中華職業棒球大聯盟",
    "三月學運展開":
        "https://zh.wikipedia.org/zh-tw/野百合學運",
    # 1989
    "鴻源擠兌風暴":
        "https://zh.wikipedia.org/zh-tw/鴻源事件",
    "鄭南榕自焚殉道":
        "https://zh.wikipedia.org/zh-tw/鄭南榕",
    "誠品書店創立":
        "https://zh.wikipedia.org/zh-tw/誠品書店",
    # 1988
    "五二○農民運動":
        "https://zh.wikipedia.org/zh-tw/520農民運動",
    # 1987
    "開放赴陸探親":
        "https://zh.wikipedia.org/zh-tw/兩岸探親",
    # 1986
    "李遠哲獲諾貝爾獎":
        "https://zh.wikipedia.org/zh-tw/李遠哲",
    "民進黨正式成立":
        "https://zh.wikipedia.org/zh-tw/民主進步黨",
    "五一九綠色行動":
        "https://zh.wikipedia.org/zh-tw/五一九綠色行動",
    # 1985
    "勞基法正式施行":
        "https://zh.wikipedia.org/zh-tw/勞動基準法_(中華民國)",
    "十信案爆發":
        "https://zh.wikipedia.org/zh-tw/十信案",
    # 1984
    "江南命案發生":
        "https://zh.wikipedia.org/zh-tw/江南案",
    "海山煤礦爆炸案":
        "https://zh.wikipedia.org/zh-tw/海山煤礦爆炸事故",
    "中華台北重返奧運":
        "https://zh.wikipedia.org/zh-tw/中華台北奧委會",
    # 1983
    # 1982
    "墾丁國家公園成立":
        "https://zh.wikipedia.org/zh-tw/墾丁國家公園",
    "李師科銀行搶案":
        "https://zh.wikipedia.org/zh-tw/李師科搶案",
    # 1981
    "陳文成事件":
        "https://zh.wikipedia.org/zh-tw/陳文成事件",
    # 1980
    "竹科正式成立":
        "https://zh.wikipedia.org/zh-tw/新竹科學園區",
    "台灣關係法生效":
        "https://zh.wikipedia.org/zh-tw/台灣關係法",
    "林宅血案發生":
        "https://zh.wikipedia.org/zh-tw/林宅血案",
    # 1979
    "高雄市升格直轄市":
        "https://zh.wikipedia.org/zh-tw/高雄市",
    "桃園機場正式啟用":
        "https://zh.wikipedia.org/zh-tw/臺灣桃園國際機場",
    "橋頭事件發生":
        "https://zh.wikipedia.org/zh-tw/橋頭事件",
    "米糠油中毒事件":
        "https://zh.wikipedia.org/zh-tw/台灣多氯聯苯中毒事件",
    # 1978
    "美國宣布對中建交":
        "https://zh.wikipedia.org/zh-tw/中美建交",
    "中山高全線通車":
        "https://zh.wikipedia.org/zh-tw/國道一號_(台灣)",
    # 1975
    "蔣中正逝世":
        "https://zh.wikipedia.org/zh-tw/蔣中正",
    # 1972
    "中日正式斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國與日本關係",
    # 1970
    "紐約刺蔣未遂案":
        "https://zh.wikipedia.org/zh-tw/蔣經國遇刺事件",
    "泰源事件爆發":
        "https://zh.wikipedia.org/zh-tw/泰源事件",
    "台獨聯盟在美成立":
        "https://zh.wikipedia.org/zh-tw/台灣獨立建國聯盟",
    "彭明敏流亡瑞典":
        "https://zh.wikipedia.org/zh-tw/彭明敏",
    # 1969
    "柏楊案遭判刑":
        "https://zh.wikipedia.org/zh-tw/柏楊",
    # 1968
    "九年國教上路":
        "https://zh.wikipedia.org/zh-tw/九年國民義務教育",
    "紅葉少棒擊敗日本隊":
        "https://zh.wikipedia.org/zh-tw/紅葉少棒",
    # 1967
    "台北市升格直轄市":
        "https://zh.wikipedia.org/zh-tw/台北市",
    # 1965
    "高雄加工區籌備啟動":
        "https://zh.wikipedia.org/zh-tw/高雄加工出口區",
    "美援停止台灣":
        "https://zh.wikipedia.org/zh-tw/美援",
    # 1964
    "彭明敏案爆發":
        "https://zh.wikipedia.org/zh-tw/台灣自救宣言",
    "中華民國與法國斷交":
        "https://zh.wikipedia.org/zh-tw/中華民國－法國關係",
    "湖口兵變失敗":
        "https://zh.wikipedia.org/zh-tw/湖口兵變",
    # 1963
    "石門水庫開始蓄水":
        "https://zh.wikipedia.org/zh-tw/石門水庫",
    # 1962
    "台視正式開播":
        "https://zh.wikipedia.org/zh-tw/台灣電視公司",
    # 1961
    "蘇東啟案審判":
        "https://zh.wikipedia.org/zh-tw/蘇東啟案",
    # 1960
    "楊傳廣奪奧運銀牌":
        "https://zh.wikipedia.org/zh-tw/楊傳廣",
    "雷震案爆發":
        "https://zh.wikipedia.org/zh-tw/雷震案",
    # 1959
    "八七水災重創中南部":
        "https://zh.wikipedia.org/zh-tw/八七水災",
    # 1958
    "八二三炮戰爆發":
        "https://zh.wikipedia.org/zh-tw/第二次台灣海峽危機",
    # 1957
    "五二四事件爆發":
        "https://zh.wikipedia.org/zh-tw/劉自然事件",
    # 1955
    "孫立人事件發生":
        "https://zh.wikipedia.org/zh-tw/孫立人案",
    "大陳島撤退來台":
        "https://zh.wikipedia.org/zh-tw/大陳島撤退",
    # 1954
    "中美共同防禦條約簽署":
        "https://zh.wikipedia.org/zh-tw/中美共同防禦條約",
    # 1953
    "西螺大橋通車":
        "https://zh.wikipedia.org/zh-tw/西螺大橋",
    # 1952
    "鹿窟事件爆發":
        "https://zh.wikipedia.org/zh-tw/鹿窟事件",
    "中日和約簽訂":
        "https://zh.wikipedia.org/zh-tw/中日和平條約",
    # 1951
    "舊金山和約簽署":
        "https://zh.wikipedia.org/zh-tw/舊金山和約",
    "美援台灣正式展開":
        "https://zh.wikipedia.org/zh-tw/美援",
    # 1950
    "韓戰改變台海局勢":
        "https://zh.wikipedia.org/zh-tw/韓戰",
    "縣市長民選恢復舉行":
        "https://zh.wikipedia.org/zh-tw/中華民國地方自治",
    # 1949
    "中央政府遷台":
        "https://zh.wikipedia.org/zh-tw/中華民國政府遷台",
    "古寧頭戰役勝利":
        "https://zh.wikipedia.org/zh-tw/古寧頭戰役",
    "新台幣發行":
        "https://zh.wikipedia.org/zh-tw/新台幣",
    "台灣實施戒嚴":
        "https://zh.wikipedia.org/zh-tw/台灣戒嚴",
    "四六事件發生":
        "https://zh.wikipedia.org/zh-tw/四六事件",
    "三七五減租推行":
        "https://zh.wikipedia.org/zh-tw/三七五減租",
    # 1948
    "臨時條款實施":
        "https://zh.wikipedia.org/zh-tw/動員戡亂時期臨時條款",
    # 1947
    "二二八事件爆發":
        "https://zh.wikipedia.org/zh-tw/二二八事件",
    # 1946
    "台灣開始地方自治":
        "https://zh.wikipedia.org/zh-tw/臺灣光復",
    # 1945
    "台灣日軍受降":
        "https://zh.wikipedia.org/zh-tw/台灣光復",
    "日本宣布終戰":
        "https://zh.wikipedia.org/zh-tw/日本投降",
    # 1944
    "台灣人適用徵兵制":
        "https://zh.wikipedia.org/zh-tw/台灣人日本兵",
    # 1943
    "盟軍空襲台灣開始":
        "https://zh.wikipedia.org/zh-tw/台灣空襲",
    # 1941
    "皇民奉公會活動啟動":
        "https://zh.wikipedia.org/zh-tw/皇民奉公會",
    # 1940
    "改姓名運動開始":
        "https://zh.wikipedia.org/zh-tw/皇民化運動",
    # 1935
    "首屆地方議員選舉":
        "https://zh.wikipedia.org/zh-tw/1935年台灣地方選舉",
    "新竹台中大地震":
        "https://zh.wikipedia.org/zh-tw/1935年新竹-台中地震",
    # 1931
    "蔣渭水逝世":
        "https://zh.wikipedia.org/zh-tw/蔣渭水",
    # 1930
    "地方自治聯盟成立":
        "https://zh.wikipedia.org/zh-tw/台灣地方自治聯盟",
    "嘉南大圳啟用":
        "https://zh.wikipedia.org/zh-tw/嘉南大圳",
    # 1928
    "台灣共產黨成立":
        "https://zh.wikipedia.org/zh-tw/台灣共產黨",
    "台北帝大設立":
        "https://zh.wikipedia.org/zh-tw/國立臺灣大學",
    # 1927
    "台灣民眾黨成立":
        "https://zh.wikipedia.org/zh-tw/台灣民眾黨_(日治時期)",
    # 1925
    "二林事件發生":
        "https://zh.wikipedia.org/zh-tw/二林事件",
    # 1923
    "治警事件爆發":
        "https://zh.wikipedia.org/zh-tw/治警事件",
    "台灣民報創刊":
        "https://zh.wikipedia.org/zh-tw/台灣民報",
    # 1921
    "文化協會成立":
        "https://zh.wikipedia.org/zh-tw/台灣文化協會",
    "首次議會請願提出":
        "https://zh.wikipedia.org/zh-tw/台灣議會設置請願運動",
    # 1920
    "台灣青年雜誌刊行":
        "https://zh.wikipedia.org/zh-tw/台灣青年_(雜誌)",
    "新民會在東京成立":
        "https://zh.wikipedia.org/zh-tw/新民會_(台灣)",
    "地方制度全面改制":
        "https://zh.wikipedia.org/zh-tw/台灣日治時期行政區劃",
    # 1919
    "首任文官總督到任":
        "https://zh.wikipedia.org/zh-tw/田健治郎",
    "台灣電力會社設立":
        "https://zh.wikipedia.org/zh-tw/台灣電力公司",
    "總督府新廳舍落成":
        "https://zh.wikipedia.org/zh-tw/臺灣總督府",
    # 1915
    "西來庵事件爆發":
        "https://zh.wikipedia.org/zh-tw/西來庵事件",
    # 1914
    "台灣同化會成立":
        "https://zh.wikipedia.org/zh-tw/台灣同化會",
    # 1913
    "羅福星事件發生":
        "https://zh.wikipedia.org/zh-tw/羅福星事件",
    # 1912
    "林杞埔事件爆發":
        "https://zh.wikipedia.org/zh-tw/林杞埔事件",
    # 1911
    "阿里山鐵路通車":
        "https://zh.wikipedia.org/zh-tw/阿里山森林鐵路",
    # 1907
    "北埔事件發生":
        "https://zh.wikipedia.org/zh-tw/北埔事件",
    "枕頭山戰役爆發":
        "https://zh.wikipedia.org/zh-tw/枕頭山戰役",
    # 1906
    "嘉義地震重創中南部":
        "https://zh.wikipedia.org/zh-tw/1906年梅仔坑地震",
    # 1902
    "雲林歸順式屠殺":
        "https://zh.wikipedia.org/zh-tw/雲林大屠殺",
    # 1900
    "台灣製糖會社設立":
        "https://zh.wikipedia.org/zh-tw/台灣製糖株式會社",
    # 1899
    "台灣銀行開業":
        "https://zh.wikipedia.org/zh-tw/台灣銀行",
    "總督府醫學校成立":
        "https://zh.wikipedia.org/zh-tw/國立臺灣大學醫學院",
    # 1898
    "保甲制度設立":
        "https://zh.wikipedia.org/zh-tw/保甲制度",
    "兒玉後藤赴台就任":
        "https://zh.wikipedia.org/zh-tw/後藤新平",
    # 1896
    "六三法施行":
        "https://zh.wikipedia.org/zh-tw/六三法",
    # 1895
    "日軍澳底登陸":
        "https://zh.wikipedia.org/zh-tw/乙未戰爭",
}

# Events to REMOVE: below landmark threshold / minor incidents / routine infrastructure
remove_titles = {
    # Routine by-elections / minor political events
    "呂秀蓮補選桃園縣長",    # By-election; routine
    "美國移除超級301名單",    # Trade policy detail; not a Taiwan landmark
    # Minor criminal cases
    "光復橋殺警奪槍案",      # Individual crime; not a national landmark
    "吳銘漢夫婦命案",        # Individual crime
    "井口真理子命案",        # Individual crime
    "景美女中溺水案",        # Local accident
    # Transportation openings (consistent with policy for modern era)
    "木柵線全線通車",        # MRT line opening
    "北迴鐵路全線通車",      # Railway opening
    "澎湖跨海大橋通車",      # Bridge opening; not a national landmark
    "新店線停止營運",        # Railway closure
    "台北新店線通車",        # Colonial-era railway opening
    "台北基隆道路開通",      # Road opening
    "臨海道路竣工",          # Road opening
    "中央山脈公路完成",      # Road completion
    "南迴公路竣工",          # Road opening
    # Colonial-era minor events
    "台北首座號誌啟用",      # Traffic signal; trivial
    "台灣關係史料刊行",      # Academic publication; not a landmark
    "台北公車開始營運",      # Local transport
    "龜山發電所完工",        # Power station; infrastructure
    "總督府廳舍動工",        # Construction start; 落成 already kept
    "台北天然足會成立",      # Minor organization
    "嘉義置州運動啟動",      # Minor local political movement
    "日月潭電廠完工",        # Infrastructure
    "日月潭二期電廠竣工",    # Infrastructure
    "大湖抗暴案破獲",        # Minor anti-Japanese incident
    "中部強震連續發生",      # Vague; no clear landmark
    "社會教化會議召開",      # Government meeting; not a landmark
    "台灣商工創立",          # Business organization
    "台灣教育令頒布",        # Colonial-era education policy; borderline
    "土地調查展開",          # Administrative process start
    "土地調查完成",          # Administrative process end
    "內台航路開設",          # Shipping route
    "舊慣調查會設置",        # Research organization
    "公共埤圳規則頒布",      # Minor irrigation legislation
    "住民去就決定截止",      # Colonial administrative deadline
    "法三號開始施行",        # Minor colonial-era legislation
    "南蕃事件發生",          # Uncertain minor event
    "大分事件發生",          # Minor anti-Japanese incident
    "台灣同化會解散",        # Organization dissolution; 成立 kept
    "裕仁視察台灣",          # Royal visit; not a landmark
    "台灣新文學創刊",        # Literary journal; not a landmark
    "台灣軍伕赴中作戰",      # Borderline military event
    "革命同盟會在渝成立",    # Organization in wartime; limited significance
    "地方自治聯盟解散",      # Organization dissolution; 成立 kept
    "新聞漢文欄遭禁",        # Subsumed by 皇民化運動/改姓名運動 events
    "三座國立公園成立",      # Infrastructure/environmental; borderline
    "台灣財政自立",          # Administrative milestone; below threshold
    "首批台籍志願兵入伍",    # Subsumed by 台灣人適用徵兵制
    "六年義務教育實施",      # Colonial-era policy; borderline
    "台灣開始地方自治",      # Borderline; overlaps with 台灣日軍受降
    # Post-WWII borderline events
    "布袋事件發生",          # Minor 1946 local incident
    "新營事件發生",          # Minor 1946 local incident
    "員林事件發生",          # Minor 1946 local incident
    "台灣進入戰時狀態",      # Vague; subsumed by larger cross-strait events
    "吳三連當選台北市長",    # Individual election; not a national landmark
    # Borderline judicial/court events
    "蘇建和案再非常上訴",    # Court procedural step; not a discrete landmark
    # Borderline post-1987 events
    "新竹少監暴動",          # Prison riot; not a national landmark
    "造橋列車對撞事故",      # Railway accident
    "日月潭翻船事故",        # Local boating accident
    "李登輝訪問新加坡",      # Diplomatic visit; not a landmark
    "施明德主張台獨",        # Statement; subsumed by 美麗島事件 narrative
    # 1984 events
    "三峽煤礦再爆炸",        # Industrial accident (already have 海山煤礦)
    "煤山煤礦火警",          # Industrial accident
    "螢橋國小潑酸案",        # Individual criminal case
    "孫運璿中風送醫",        # Health news; not a national landmark
    # 1983
    "豐原高中禮堂倒塌",      # Local accident
    # 1982
    "二二八受刑人獲釋",      # Borderline; 政府為二二八道歉 covers the arc
    # Borderline pre-1895
    "新高港開工",            # Colonial infrastructure; start of construction
    "桃園大圳竣工",          # Irrigation infrastructure
    "始政四十年博覽會開幕",  # Colonial-era exhibition
    "竹南苗栗再遇強震",      # 1935 earthquake (already keep 新竹台中大地震)
    "台陽美術協會成立",      # Art organization
    "議會請願運動終止",      # End of movement; 首次議會請願提出 covers start
    "原子核撞擊實驗成功",    # Scientific experiment; questionable national significance
    "台灣文藝協會成立",      # Cultural organization
    "台灣通史出版",          # Academic publication
    "治安警察法在台實施",    # Minor colonial legislation
    "六三法改為三一法",      # Colonial-era minor legal revision
    "台灣戶口調查實施",      # Administrative census
    "國航客機遭劫來台",      # Individual hijacking; not a lasting landmark
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

print(f"\nRemoved {removed} borderline/minor events")
print(f"Updated {updated} events with URLs")

pre2000 = [e for e in result if e['date'] < '2000']
with_url = [e for e in pre2000 if e.get('source_url', '')]
print(f"Pre-2000: {len(pre2000)} events, {len(with_url)} with source_url")

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Saved {len(result)} events.")
