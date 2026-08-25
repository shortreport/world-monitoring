#!/usr/bin/env python3
"""
midterm_monitor.py
==================
2026年米国中間選挙の最新情勢を収集・分析するスクリプト。
WorldNews API + Claude で上院・下院・知事の主要レースを分析し
docs/data/midterm_latest.json に保存する。

使い方:
  python midterm_monitor.py
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import anthropic
    import requests
except ImportError as e:
    print(f"[ERROR] 必要なパッケージが不足: {e}")
    sys.exit(1)

try:
    from api_config import ANTHROPIC_API_KEY, WORLDNEWS_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    WORLDNEWS_API_KEY = os.getenv("WORLDNEWS_API_KEY", "")

BASE     = Path(__file__).parent
DATA_DIR = BASE / "docs" / "data"
OUT_JSON = DATA_DIR / "midterm_latest.json"
JST      = timezone(timedelta(hours=9))
MODEL    = "claude-haiku-4-5-20251001"

# ── 2026年各州プライマリー日程（固定カレンダー） ───────────────────────────────
# format: (date_iso, state_code, state_name, chambers, description)
PRIMARY_CALENDAR = [
    ("2026-05-12", "WV", "West Virginia",  "all", "Primary Election"),
    ("2026-05-12", "IN", "Indiana",         "all", "Primary Election"),
    ("2026-05-12", "OH", "Ohio",            "all", "Primary Election"),
    ("2026-05-12", "NC", "North Carolina",  "all", "Primary Election"),
    ("2026-05-12", "GA", "Georgia",         "all", "Primary Election"),
    ("2026-05-19", "OR", "Oregon",          "all", "Primary Election"),
    ("2026-05-19", "ID", "Idaho",           "all", "Primary Election"),
    ("2026-05-19", "PA", "Pennsylvania",    "all", "Primary Election"),
    ("2026-05-19", "KY", "Kentucky",        "all", "Primary Election"),
    ("2026-06-02", "MT", "Montana",         "all", "Primary Election"),
    ("2026-06-02", "IA", "Iowa",            "all", "Primary Election"),
    ("2026-06-02", "CA", "California",      "all", "Top-2 Open Primary"),
    ("2026-06-02", "NJ", "New Jersey",      "all", "Primary Election"),
    ("2026-06-02", "SD", "South Dakota",    "all", "Primary Election"),
    ("2026-06-02", "NM", "New Mexico",      "all", "Primary Election"),
    ("2026-07-21", "GA", "Georgia",         "all", "Primary Runoff (if needed)"),
    ("2026-08-04", "MI", "Michigan",        "all", "Primary Election"),
    ("2026-08-04", "MO", "Missouri",        "house|governor", "Primary Election"),
    ("2026-08-04", "AZ", "Arizona",         "all", "Primary Election"),
    ("2026-08-04", "WA", "Washington",      "all", "Top-2 Open Primary"),
    ("2026-08-04", "KS", "Kansas",          "all", "Primary Election"),
    ("2026-08-06", "TN", "Tennessee",       "all", "Primary Election"),
    ("2026-08-08", "HI", "Hawaii",          "all", "Primary Election"),
    ("2026-08-11", "MN", "Minnesota",       "all", "Primary Election"),
    ("2026-08-11", "CT", "Connecticut",     "all", "Primary Election"),
    ("2026-08-11", "WI", "Wisconsin",       "all", "Primary Election"),
    ("2026-08-11", "VT", "Vermont",         "all", "Primary Election"),
    ("2026-08-18", "FL", "Florida",         "all", "Primary Election"),
    ("2026-08-18", "AK", "Alaska",          "all", "RCV Top-4 Primary"),
    ("2026-08-18", "WY", "Wyoming",         "all", "Primary Election"),
    ("2026-08-25", "OK", "Oklahoma",        "all", "Primary Election"),
    ("2026-09-01", "MA", "Massachusetts",   "all", "Primary Election"),
    ("2026-09-08", "DE", "Delaware",        "all", "Primary Election"),
    ("2026-09-08", "NH", "New Hampshire",   "all", "Primary Election"),
    ("2026-09-08", "RI", "Rhode Island",    "all", "Primary Election"),
    ("2026-09-15", "NY", "New York",        "all", "Primary Election"),
    ("2026-09-15", "ME", "Maine",           "all", "Primary Election"),
    ("2026-09-22", "ND", "North Dakota",    "all", "Primary Election"),
    ("2026-09-29", "LA", "Louisiana",       "all", "Jungle Primary"),
    ("2026-11-03", "ALL", "All States",     "all", "2026 Midterm General Election"),
]


def get_upcoming_schedule(weeks: int = 8) -> dict:
    """今日から指定週数以内のプライマリー日程を chamber 別に返す"""
    today = datetime.now(JST).date()
    cutoff = today + timedelta(weeks=weeks)
    result = {"senate": [], "house": [], "governor": []}
    for date_iso, code, name, chambers, desc in PRIMARY_CALENDAR:
        d = datetime.strptime(date_iso, "%Y-%m-%d").date()
        if d < today or d > cutoff:
            continue
        label = d.strftime("%b %d")
        item  = {"date": label, "state": f"{name} ({code})", "event": desc}
        if chambers == "all" or "senate" in chambers:
            result["senate"].append(item)
        if chambers == "all" or "house" in chambers:
            result["house"].append(item)
        if chambers == "all" or "governor" in chambers:
            result["governor"].append(item)
    return result


def collect_news(query: str, max_articles: int = 10) -> list[dict]:
    """WorldNews API から最近のニュース記事を取得"""
    if not WORLDNEWS_API_KEY:
        print("  [WARN] WORLDNEWS_API_KEY が未設定")
        return []
    try:
        r = requests.get(
            "https://api.worldnewsapi.com/search-news",
            params={
                "api-key":        WORLDNEWS_API_KEY,
                "text":           query,
                "language":       "en",
                "number":         max_articles,
                "sort":           "publish-time",
                "sort-direction": "DESC",
                "min-sentiment":  -1,
            },
            timeout=20,
        )
        if r.status_code == 200:
            articles = r.json().get("news", [])
            return [
                {
                    "title":   a.get("title", ""),
                    "summary": (a.get("text", "") or "")[:300],
                    "date":    (a.get("publish_date", "") or "")[:16],
                }
                for a in articles
            ]
        else:
            print(f"  [WARN] WorldNews API {r.status_code}")
            return []
    except Exception as e:
        print(f"  [WARN] WorldNews API error: {e}")
        return []


def analyze_with_claude(articles: list[dict], client) -> dict:
    """収集した記事を Claude で分析し、レース情勢を返す"""
    if not articles:
        return {"projections": {}, "key_developments": [], "key_races": {}}

    articles_text = "\n".join(
        f"[{a['date']}] {a['title']}\n{a['summary']}" for a in articles[:45]
    )
    today_str = datetime.now(JST).strftime("%Y-%m-%d")

    prompt = f"""\
Today: {today_str}

You are a US election analyst. Based on the following recent news articles about the 2026 US Midterm Elections, analyze:

{articles_text}

Output ONLY valid JSON (no markdown, no explanation) with this structure:
{{
  "projections": {{
    "senate":   {{"r": <int>, "d": <int>, "tossup": <int>}},
    "house":    {{"r": <int>, "d": <int>, "tossup": <int>}},
    "governor": {{"r": <int>, "d": <int>, "tossup": <int>}}
  }},
  "key_developments": [
    "<1-sentence development>",
    "<1-sentence development>"
  ],
  "key_races": {{
    "senate": [
      {{"state": "<2-letter code>", "incumbent": "<Name (Party)>", "party": "<R|D>", "rating": "<safe-r|likely-r|lean-r|tossup|lean-d|likely-d|safe-d>", "label": "<display label>", "note": "<1-sentence>"}},
      ...
    ],
    "house": [
      {{"state": "<CODE-DIST>", "incumbent": "<Name (Party)>", "party": "<R|D>", "rating": "<rating>", "label": "<label>", "note": "<1-sentence>"}}
    ],
    "governor": [
      {{"state": "<2-letter code>", "incumbent": "<Name (Party)>", "party": "<R|D>", "rating": "<rating>", "label": "<label>", "note": "<1-sentence>"}}
    ]
  }}
}}

Rules:
- projections: best estimate of final seat counts after 2026 election (Senate: 100 total, House: 435 total, Governor: 50 total active races ≈ 36 up in 2026)
- key_developments: top 3-5 notable changes or news items from the articles
- key_races: as many competitive/newsworthy races as the articles support, aim for 6-10 per chamber (fewer is fine if data is thin — do not invent races not grounded in the articles)
- rating must be one of: safe-r, likely-r, lean-r, toss, lean-d, likely-d, safe-d
- Use only information from the provided articles; do not invent data
- If articles are insufficient for a specific chamber, use reasonable defaults (Senate R:56 D:42 Tossup:2, House R:215 D:185 Tossup:35, Governor R:22 D:14 Tossup:0)
"""
    try:
        msg = client.messages.create(
            model=MODEL, max_tokens=3500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*", "", raw)
        return json.loads(raw)
    except Exception as e:
        print(f"  [WARN] Claude 分析失敗: {e}")
        return {
            "projections": {
                "senate":   {"r": 56, "d": 42, "tossup": 2},
                "house":    {"r": 215, "d": 185, "tossup": 35},
                "governor": {"r": 22, "d": 14, "tossup": 0},
            },
            "key_developments": [],
            "key_races": {"senate": [], "house": [], "governor": []},
        }


def main():
    print("=" * 60)
    print(f"midterm_monitor.py  {datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')}")
    print("=" * 60)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # ── ニュース収集（Senate / House / Governor 横断） ─────────────────────
    queries = [
        "2026 US Senate election race ratings Cook Political Report",
        "2026 US House election competitive districts forecast",
        "2026 US Governor race battleground states",
        "2026 midterm election polls swing states",
        "2026 midterm election toss-up races",
    ]
    all_articles = []
    for q in queries:
        print(f"  収集中: {q[:60]}...")
        arts = collect_news(q, max_articles=12)
        all_articles.extend(arts)
        time.sleep(1)

    print(f"  合計記事数: {len(all_articles)}")

    # ── Claude 分析 ──────────────────────────────────────────────────────
    print("  Claude で情勢分析中...")
    analysis = analyze_with_claude(all_articles, client)

    # ── 今後8週間のプライマリースケジュール ──────────────────────────────
    upcoming = get_upcoming_schedule(weeks=8)

    # ── JSON 保存 ─────────────────────────────────────────────────────────
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at":    datetime.now(JST).isoformat(),
        "article_count":   len(all_articles),
        "projections":     analysis.get("projections", {}),
        "key_developments": analysis.get("key_developments", []),
        "key_races":       analysis.get("key_races", {}),
        "upcoming_schedule": upcoming,
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [OK] {OUT_JSON} に保存")
    print("完了")


if __name__ == "__main__":
    main()
