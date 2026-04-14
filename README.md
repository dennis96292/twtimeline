<div align="center">

# 台灣發生了什麼？
### Taiwan Historical Events Timeline

**[→ 線上瀏覽 ↗](https://dennis96292.github.io/twtimeline/)**

</div>

---

```
1895 ──────────────────────────────────────────────────── 2026
  │                                                          │
  ▼   583 則重大事件  ·  寧缺勿濫  ·  每則附原始來源連結    ▼
```

---

## 內容

從 **1895 年馬關條約** 到今日，涵蓋台灣歷史上真正值得記錄的里程碑——

- 政治 · 外交 · 兩岸 · 選舉
- 社會 · 司法 · 災難
- 經濟 · 科技 · 產業

每則事件均附可信來源（中央社、自由時報、聯合報、BBC 中文、維基百科等）。

## 收錄標準

> **寧缺勿濫。**

只收錄評分 ≥ 7/10 的歷史里程碑，不收錄例行政治活動、個人運動成就、地方新聞。

## 自動更新

每三天由 GitHub Actions 執行 Claude Sonnet web search agent，搜尋近期台灣重大事件並評分，符合標準的候選事件以 **Pull Request** 形式提交人工審查後才合併。

## 本地開發

```bash
# 無需 build，直接開啟
open web/index.html
```

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

---

<div align="center">

資料以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權釋出

</div>
