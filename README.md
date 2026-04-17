<div align="center">

# 台灣發生了什麼？

**Taiwan Historical Events Timeline**

[![Events](https://img.shields.io/badge/events-584-FF6B00?style=flat-square&labelColor=1e1e1e)](https://dennis96292.github.io/twtimeline/)
[![Range](https://img.shields.io/badge/189526-timeline-FF8C33?style=flat-square&labelColor=1e1e1e)](https://dennis96292.github.io/twtimeline/)
[![Auto Update](https://img.shields.io/badge/auto--update-every%203%20days-994000?style=flat-square&labelColor=1e1e1e)](/.github/workflows/daily_news.yml)

**[→ 線上瀏覽](https://dennis96292.github.io/twtimeline/)**

</div>

---

從 **1895 年馬關條約** 到今日，台灣歷史里程碑完整記錄，每則事件附原始來源連結。

涵蓋：政治 · 外交 · 兩岸 · 選舉 · 社會 · 司法 · 災難 · 經濟 · 科技

## 收錄標準

奉行「**寧缺勿濫**」原則，只收錄評分 ≥ 7/10 的歷史里程碑。不收錄例行政治活動、個人運動成就、地方新聞。

## 自動更新

每三天由 GitHub Actions 執行 Claude Sonnet web search agent，搜尋近期台灣重大事件並評分，符合標準的候選事件以 Pull Request 形式提交**人工審查**後才合併。

## 資料格式

```jsonc
{
  "date": "YYYY-MM-DD",
  "title": "15字以內精確標題",
  "desc": "80–120字事件描述",
  "tags": ["政治", "外交"],
  "source_url": "https://..."
}
```

詳見 [`EVENT_FORMAT.md`](EVENT_FORMAT.md)。

## 本地開發

```bash
open web/index.html  # 無需 build
```

---

<div align="center">

資料以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權釋出

</div>
