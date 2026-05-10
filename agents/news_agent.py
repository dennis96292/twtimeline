#!/usr/bin/env python3
"""
Taiwan History Web Search Agent (runs every 3 days)
=====================================================
Uses Claude Sonnet 4.6 + web_search to find major Taiwan events from the past 72 hours,
cross-verify them, and append qualifying events to data/events.json.

Curation standard: 寧缺勿濫 — only true historical landmarks, not routine news.
"""

import anthropic
import httpx
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

# ─── paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
EVENTS_FILE = REPO_ROOT / "data" / "events.json"
OUTPUT_FILE = REPO_ROOT / "data" / "events.json"

# ─── constants ────────────────────────────────────────────────────────────────
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096

# Major Taiwanese news outlets the agent should pull cross-references from.
# Order roughly reflects mainstream prominence; agent picks 2–4 different ones.
PREFERRED_OUTLETS = [
    "中央社", "自由時報", "聯合新聞網", "公視新聞", "新頭殼",
    "TVBS新聞網", "三立新聞網", "ETtoday", "中時新聞網", "東森新聞",
    "鏡週刊", "報導者", "客新聞", "商業周刊", "華視新聞", "民視新聞",
    "台視新聞", "蘋果新聞網", "風傳媒", "鉅亨網", "BBC", "Reuters",
]

# Skip URL liveness check via env var (for testing without network).
SKIP_URL_CHECK = os.environ.get("SKIP_URL_CHECK", "").lower() in ("1", "true", "yes")

# ─── system prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""\
你是台灣歷史年表的資深策展人，負責維護一份從1895年至今的重大歷史事件資料庫。

## 任務
搜尋過去 48 小時內台灣發生的重大事件，評估哪些值得納入歷史年表，並為每筆事件**蒐集多家媒體交叉佐證**。

## 年表收錄標準（寧缺勿濫）
✅ 收錄：
- 重大政治事件（選舉結果、政府重大決策、憲政變化）
- 重要外交事件（邦交建立/斷絕、重要國際協議、重大外交聲明）
- 重大災難（地震、颱風、工安事故，造成重大傷亡或影響）
- 影響深遠的社會/經濟事件（重大法律通過、重要政策實施）
- 具歷史意義的司法判決
- 重大社會運動或抗爭（有重要政策結果）
- 重大科技/產業里程碑（台灣企業、半導體、科技政策）

❌ 不收錄：
- 例行性政治活動（例行記者會、例行施政）
- 個人運動成就（除非破紀錄且有全國象徵意義）
- 純娛樂/流行文化事件
- 政黨內部人事（除非影響重大政策走向）
- 地方性事件（除非有全國影響）
- 尚未確定的事件或謠言
- 連續事件的例行進展（如某案的一般審理）

## 評分門檻
每個候選事件給予 0–10 分，**≥7 分才收錄**：
- 9–10：憲政/歷史轉折（如總統選舉、戒嚴解除級別）
- 7–8：重大政策/外交/災難（如重大地震、重要法律三讀）
- 5–6：重要但非里程碑（不收錄）
- 1–4：例行或地方性（不收錄）

## 搜尋策略（搜尋次數上限 18 次）
1. 先用 1–2 次搜尋廣泛瀏覽過去 72 小時台灣重大新聞
2. 對候選事件（初步 ≥7 分）做**多媒體交叉驗證**：
   - 為每筆事件找 **2–4 個不同媒體**的報導
   - 每媒體最多 1 筆，**禁止同一媒體多筆**
   - 優先媒體：{', '.join(PREFERRED_OUTLETS[:10])}
3. 若該事件只有單一媒體願意報、或非常冷門，可以**只回 1 個來源**——但**不可為了湊數捏造**
4. 不夠格的事件直接跳過

## 來源 URL 嚴格規範（防止 hallucination）
- 每個 URL **必須來自你實際做過的 web_search 結果**，從搜尋回傳的 link 直接複製
- **不可從記憶推測 URL**、**不可用搜尋頁面 URL 取代文章 URL**
- URL 應指向**單篇文章頁面**（非首頁、非分類頁、非搜尋結果頁）
- 同一事件若同個 outlet 出現多篇，挑**最完整**的一篇即可

## 輸出格式
完成搜尋後，輸出 JSON 陣列（若無符合事件則輸出空陣列 []）：

```json
[
  {{
    "date": "YYYY-MM-DD",
    "title": "15字以內精確標題",
    "desc": "80-120字的中文描述，說明事件背景、經過、意義",
    "tags": ["政治"|"外交"|"社會"|"經濟"|"災難"|"司法"|"科技"|"兩岸"|"選舉"],
    "sources": [
      {{
        "outlet": "中央社",
        "title": "報導實際標題（不要含媒體名稱與分類後綴）",
        "url": "https://www.cna.com.tw/news/.../article.aspx"
      }},
      {{
        "outlet": "自由時報",
        "title": "...",
        "url": "https://news.ltn.com.tw/news/..."
      }}
    ],
    "score": 7
  }}
]
```

標題規範：簡潔精準，15字以內，不含標點符號，類似「總統大選開票完成」「921大地震發生」格式。
sources 中至少 1 筆，理想 2-4 筆，**每筆來自不同 outlet**。
"""

# ─── user prompt ──────────────────────────────────────────────────────────────
def build_user_prompt(target_date: date, existing_titles: set[str]) -> str:
    start_date = target_date - timedelta(days=3)
    recent_titles = "\n".join(f"- {t}" for t in sorted(existing_titles)[-30:])
    return f"""\
今天是 {target_date.isoformat()}（台灣時間）。

請搜尋 {start_date.isoformat()} 至 {target_date.isoformat()} 期間台灣發生的重大事件，
並為每筆事件找 2-4 個不同媒體的交叉佐證來源。
搜尋次數總計不超過 18 次。

【已收錄的近期事件（請勿重複）】
{recent_titles}

請開始搜尋並評估，最後輸出符合標準的事件 JSON 陣列。
"""


# ─── run agent ────────────────────────────────────────────────────────────────
def run_agent(target_date: date, existing_events: list[dict]) -> list[dict]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    existing_titles = {e["title"] for e in existing_events}
    user_prompt = build_user_prompt(target_date, existing_titles)

    print(f"[agent] Searching for events on {target_date.isoformat()} ...", flush=True)

    # web_search_20260209 is a fully server-side tool: Anthropic executes searches
    # internally; the API returns end_turn with the completed answer in one call.
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    print(f"[agent] stop_reason={response.stop_reason}", flush=True)

    # Log any search queries Claude performed (visible as server_tool_use blocks)
    for block in response.content:
        block_type = getattr(block, "type", "")
        if block_type == "server_tool_use":
            query = getattr(block, "input", {})
            if isinstance(query, dict):
                print(f"[agent] web_search: {query.get('query', '')[:80]}", flush=True)

    # Extract final text
    final_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_text += block.text

    print(f"[agent] Final response length: {len(final_text)} chars", flush=True)
    return parse_events(final_text, existing_titles)


# ─── parse output ─────────────────────────────────────────────────────────────
def parse_events(text: str, existing_titles: set[str]) -> list[dict]:
    """Extract JSON array from agent response text."""
    # Try to find a JSON array in the response
    json_match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.DOTALL)
    if not json_match:
        json_match = re.search(r"(\[\s*\{.*?\}\s*\])", text, re.DOTALL)

    if not json_match:
        # Check if response explicitly says no events
        if "[]" in text or "無符合" in text or "沒有" in text or "no qualifying" in text.lower():
            print("[parse] No qualifying events found.", flush=True)
            return []
        print("[parse] WARNING: Could not parse JSON from response.", flush=True)
        print("[parse] Raw response snippet:", text[:500], flush=True)
        return []

    try:
        events = json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        print(f"[parse] JSON decode error: {e}", flush=True)
        print("[parse] Raw JSON snippet:", json_match.group(1)[:500], flush=True)
        return []

    if not isinstance(events, list):
        print("[parse] Parsed result is not a list.", flush=True)
        return []

    # Validate and filter
    valid = []
    required_fields = {"date", "title", "desc", "tags", "sources"}
    for ev in events:
        if not isinstance(ev, dict):
            continue
        # Backward compat: if agent still returned legacy `source_url`, wrap it
        if "sources" not in ev and "source_url" in ev:
            ev["sources"] = [{
                "outlet": _outlet_from_url(ev["source_url"]),
                "title": ev.get("title", ""),
                "url": ev["source_url"],
            }]
        if not required_fields.issubset(ev.keys()):
            missing = required_fields - ev.keys()
            print(f"[parse] Skipping event missing fields {missing}: {ev.get('title', '?')}", flush=True)
            continue
        if ev["title"] in existing_titles:
            print(f"[parse] Skipping duplicate: {ev['title']}", flush=True)
            continue
        score = ev.get("score", 0)
        if score < 7:
            print(f"[parse] Skipping low-score ({score}) event: {ev['title']}", flush=True)
            continue
        # Validate date format
        try:
            datetime.strptime(ev["date"], "%Y-%m-%d")
        except ValueError:
            print(f"[parse] Invalid date format for: {ev['title']}", flush=True)
            continue
        # Validate + sanitize sources
        sources = _sanitize_sources(ev.get("sources"), ev["title"])
        if not sources:
            print(f"[parse] Skipping event with 0 valid sources: {ev['title']}", flush=True)
            continue
        # Sanitize event: remove internal 'score' field before saving
        clean_ev = {
            "date": ev["date"],
            "title": ev["title"],
            "desc": ev["desc"],
            "tags": ev["tags"] if isinstance(ev["tags"], list) else [ev["tags"]],
            "sources": sources,
        }
        valid.append(clean_ev)
        outlets = ", ".join(s["outlet"] for s in sources)
        print(f"[parse] Accepted: [{ev['date']}] {ev['title']} (score={score}, {len(sources)} sources: {outlets})", flush=True)

    return valid


# ─── source validation helpers ────────────────────────────────────────────────
_OUTLET_HOST_HINTS = [
    ("中央社", "cna.com.tw"),
    ("自由時報", "ltn.com.tw"),
    ("聯合新聞網", "udn.com"),
    ("中時新聞網", "chinatimes.com"),
    ("三立新聞網", "setn.com"),
    ("TVBS新聞網", "tvbs.com.tw"),
    ("ETtoday", "ettoday.net"),
    ("東森新聞", "ebc.net.tw"),
    ("公視新聞", "pts.org.tw"),
    ("民視新聞", "ftvnews.com.tw"),
    ("華視新聞", "cts.com.tw"),
    ("台視新聞", "ttv.com.tw"),
    ("關鍵評論網", "thenewslens.com"),
    ("報導者", "twreporter.org"),
    ("鏡週刊", "mirrormedia.mg"),
    ("新頭殼", "newtalk.tw"),
    ("風傳媒", "storm.mg"),
    ("商業周刊", "businessweekly.com.tw"),
    ("鉅亨網", "cnyes.com"),
    ("客新聞", "hakkanews.tw"),
    ("BBC", "bbc.com"),
    ("Reuters", "reuters.com"),
]


def _outlet_from_url(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return "來源"
    for name, hint in _OUTLET_HOST_HINTS:
        if host == hint or host.endswith("." + hint):
            return name
    return "來源"


def _is_valid_url(url: str) -> bool:
    """Basic shape check for a real article URL."""
    if not isinstance(url, str) or len(url) < 12:
        return False
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False
    # Reject obvious non-article paths (search/category pages)
    bad_path_patterns = ("/search", "/list", "/category", "/tag/", "/index", "/cate")
    path = parsed.path.lower()
    if any(p in path for p in bad_path_patterns):
        return False
    # Real articles usually have a non-trivial path
    if path in ("", "/", "/index.html"):
        return False
    return True


def _check_url_alive(url: str, timeout: float = 8.0) -> bool:
    """HEAD-check a URL. Returns False on 4xx/5xx/error. Defaults to True if SKIP."""
    if SKIP_URL_CHECK:
        return True
    try:
        with httpx.Client(follow_redirects=True, timeout=timeout) as client:
            r = client.head(url, headers={"User-Agent": "Mozilla/5.0 twtimeline-agent"})
            # Some sites return 405 to HEAD; fall back to GET (range 0-0 is light)
            if r.status_code in (403, 405, 501):
                r = client.get(url, headers={"User-Agent": "Mozilla/5.0 twtimeline-agent", "Range": "bytes=0-1023"})
            return r.status_code < 400
    except Exception as e:
        print(f"[url-check] {url}: {type(e).__name__}", flush=True)
        return False


def _sanitize_sources(sources, event_title: str) -> list[dict]:
    """Validate and clean a list of source objects. Drops bad ones, dedupes by outlet, HEAD-checks live URLs."""
    if not isinstance(sources, list) or not sources:
        return []
    cleaned = []
    seen_outlets = set()
    seen_urls = set()
    for s in sources:
        if not isinstance(s, dict):
            continue
        outlet = (s.get("outlet") or "").strip()
        title = (s.get("title") or "").strip() or event_title
        url = (s.get("url") or "").strip()
        if not outlet or not _is_valid_url(url):
            print(f"[parse]   ! drop source (bad outlet/url): {outlet} {url[:60]}", flush=True)
            continue
        # Dedupe within event
        if outlet in seen_outlets or url in seen_urls:
            print(f"[parse]   ! drop duplicate source: {outlet} {url[:60]}", flush=True)
            continue
        if not _check_url_alive(url):
            print(f"[parse]   ! drop dead source: {outlet} {url[:60]}", flush=True)
            continue
        seen_outlets.add(outlet)
        seen_urls.add(url)
        cleaned.append({"outlet": outlet, "title": title, "url": url})
    return cleaned


# ─── merge into events.json ────────────────────────────────────────────────────
def merge_events(new_events: list[dict], existing_events: list[dict]) -> list[dict]:
    """Merge new events into existing list, sorted by date descending."""
    if not new_events:
        return existing_events
    combined = existing_events + new_events
    combined.sort(key=lambda e: e["date"], reverse=True)
    return combined


# ─── main ─────────────────────────────────────────────────────────────────────
def main():
    # Allow overriding target date via env var (for testing)
    target_date_str = os.environ.get("TARGET_DATE", "")
    if target_date_str:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    else:
        target_date = date.today()

    print(f"[main] Target date: {target_date.isoformat()}", flush=True)
    print(f"[main] Events file: {EVENTS_FILE}", flush=True)

    # Load existing events
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        existing_events = json.load(f)
    print(f"[main] Loaded {len(existing_events)} existing events.", flush=True)

    # Run agent
    new_events = run_agent(target_date, existing_events)
    print(f"\n[main] Found {len(new_events)} new qualifying event(s).", flush=True)

    if not new_events:
        print("[main] Nothing to add. Exiting.", flush=True)
        # Write a marker file so the workflow knows there's nothing to PR
        marker = REPO_ROOT / "agents" / ".no_new_events"
        marker.write_text(f"No new events for {target_date.isoformat()}\n", encoding="utf-8")
        sys.exit(0)

    # Merge and save
    merged = merge_events(new_events, existing_events)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"[main] Saved {len(merged)} events to {OUTPUT_FILE}", flush=True)

    # Print summary
    print("\n[main] New events added:", flush=True)
    for ev in new_events:
        print(f"  - [{ev['date']}] {ev['title']}", flush=True)
        print(f"    {ev['desc'][:60]}...", flush=True)
        for s in ev["sources"]:
            print(f"    [{s['outlet']}] {s['url']}", flush=True)

    # Write commit-message body for the workflow's `git commit -m ... -m "$body"`
    pr_body_file = REPO_ROOT / "agents" / ".pr_body.md"
    lines = [
        f"自動新增台灣重大事件 ({target_date.isoformat()})\n\n",
        "由 Claude Sonnet 4.6 + web_search 搜尋並驗證，符合「寧缺勿濫」收錄標準（評分 ≥ 7/10）。\n",
        "每筆事件已交叉驗證 1-4 個不同媒體來源。\n\n",
        "新增事件：\n",
    ]
    for ev in new_events:
        lines.append(f"\n[{ev['date']}] {ev['title']}\n")
        lines.append(f"{ev['desc']}\n")
        lines.append(f"標籤：{', '.join(ev['tags'])}\n")
        lines.append(f"來源（{len(ev['sources'])} 筆）：\n")
        for s in ev["sources"]:
            lines.append(f"  - {s['outlet']}: {s['url']}\n")
    pr_body_file.write_text("".join(lines), encoding="utf-8")
    print(f"[main] Commit body written to {pr_body_file}", flush=True)


if __name__ == "__main__":
    main()
