#!/usr/bin/env python3
"""
make_en_trump.py
================
Trump Monitor 英語ファースト更新スクリプト

手順:
  1. データ収集（trump_monitor.py の収集関数を再利用）
  2. Claude で英語構造化JSON を生成 → trump_en_latest.json に保存
  3. docs/en/trump.html を英語JSONから生成
  4. 英語JSONのbulletsを日本語に翻訳 → trump_latest.json に保存
  5. generate_site.py を呼び出して docs/trump.html を更新

使い方:
  python make_en_trump.py
  python make_en_trump.py --skip-collect   # 既存JSON再利用（翻訳・HTML生成のみ）
  python make_en_trump.py --en-only        # 英語HTML生成のみ（日本語更新なし）
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import anthropic

try:
    from api_config import ANTHROPIC_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ── パス ──────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
OUT_EN       = BASE_DIR / "docs" / "en" / "trump.html"
OUT_EN_JSON  = BASE_DIR / "db" / "north america" / "trump_en_latest.json"
OUT_JA_JSON  = BASE_DIR / "db" / "north america" / "trump_latest.json"

MODEL = "claude-haiku-4-5-20251001"

TODAY     = datetime.now(timezone.utc).date()
YESTERDAY = TODAY - timedelta(days=1)
DATE_RANGE = f"{YESTERDAY} ~ {TODAY}"

# ── 収集関数を trump_monitor.py から import ──────────────────────────────────
sys.path.insert(0, str(BASE_DIR))
from trump_monitor import (
    collect_truth_social,
    collect_whitehouse_rss,
    collect_whitehouse_youtube,
    collect_google_news,
    collect_world_news,
    _build_input,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 1: データ収集
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def collect_all() -> list[dict]:
    print("── データ収集中 ─────────────────────────────")
    all_items = []
    tasks = [
        ("📱 Truth Social",          collect_truth_social),
        ("🏛  White House RSS",       collect_whitehouse_rss),
        ("🎬 YouTube",                collect_whitehouse_youtube),
        ("📰 Google News",            collect_google_news),
        ("🌐 World News API",         collect_world_news),
    ]
    for label, fn in tasks:
        result = fn()
        all_items.extend(result)
        print(f"  {label}: {len(result)} 件")
    print(f"  合計: {len(all_items)} 件\n")
    return all_items


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 2: 英語構造化JSON生成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EN_SYSTEM = """\
You are a senior political analyst writing for a wire-service terminal (Reuters/Bloomberg style).
Summarize Trump administration activity in tight, punchy English — headline style.
Output ONLY valid JSON. No markdown fences, no explanations.\
"""

def summarize_en(items: list[dict]) -> dict:
    print("── 英語構造化JSON生成中（Claude）─────────────")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    data   = _build_input(items)

    prompt = f"""\
Data collected {YESTERDAY}~{TODAY} (UTC) — {len(items)} items on Trump and key cabinet.

{data}

────────────────────────────────────────────
Output this JSON schema ONLY (no fences, no prose):

{{
  "key_points":          [{{"text":"...","source":"...","url":"..."}}],
  "sns":                 [{{"text":"...","source":"...","url":"..."}}],
  "press_conference":    [{{"text":"...","source":"...","url":"..."}}],
  "whitehouse_official": [{{"text":"...","source":"...","url":"..."}}],
  "wh_briefing":         [{{"text":"...","source":"...","url":"..."}}],
  "video":               [{{"text":"...","source":"...","url":"..."}}],
  "cabinet":             [{{"text":"...","source":"...","url":"..."}}],
  "japan_impact":        [{{"text":"...","source":"...","url":"..."}}]
}}

Wire-service style rules:
- Every bullet: max 12 words, active voice, no filler
  Good: "Trump arrives Ankara; bilateral with Erdogan precedes NATO plenary"
  Bad:  "President Trump has arrived in Ankara, Turkey for the NATO summit meeting"
- "text" field is the bullet. "source" is the outlet name. "url" is from the input data.
- Empty sections → []
- Counts: key_points 3-6 / sns up to 6 / press_conference up to 5
  whitehouse_official up to 5 / wh_briefing up to 4 / video up to 4
  cabinet up to 5 (lead with name) / japan_impact up to 5 (lead with [CATEGORY])
"""
    resp = client.messages.create(
        model=MODEL, max_tokens=8000, system=EN_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*\n?', '', raw)
    raw = re.sub(r'\n?```\s*$', '', raw)
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        result = json.loads(m.group()) if m else {}
    print(f"  key_points: {len(result.get('key_points',[]))} 件")
    print(f"  sections:   {sum(len(v) for k,v in result.items() if k != 'key_points')} 件\n")
    return result


def save_en_json(structured: dict, items: list[dict]) -> Path:
    OUT_EN_JSON.parent.mkdir(parents=True, exist_ok=True)
    type_counts: dict[str, int] = {}
    for it in items:
        t = it.get("type", "news")
        type_counts[t] = type_counts.get(t, 0) + 1

    sources_summary = []
    for key, label, icon in [
        ("sns",                  "Truth Social",            "📱"),
        ("video",                "YouTube (captioned)",     "🎬"),
        ("news",                 "Google News",             "📰"),
        ("briefings",            "White House RSS",         "🏛"),
        ("presidential_actions", "Executive Actions",       "📜"),
    ]:
        cnt = type_counts.get(key, 0)
        if cnt > 0:
            sources_summary.append({"icon": icon, "label": label, "count": f"{cnt} items"})

    output = {
        "generated_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date_range":      DATE_RANGE,
        "item_count":      len(items),
        "sources_summary": sources_summary,
        **structured,
    }
    OUT_EN_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  保存: {OUT_EN_JSON}\n")
    return OUT_EN_JSON


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 3: docs/en/trump.html 生成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _e(s: str) -> str:
    return html.escape(str(s))

def _gn(q: str) -> str:
    import urllib.parse
    return f"https://news.google.com/search?q={urllib.parse.quote(q)}&hl=en&gl=US"

def _src_tag(source: str) -> str:
    return f'<span class="src-tag">{_e(source)} ↗</span>' if source else ""

def _bullet_html(b: dict) -> str:
    text = b.get("text", "")
    url  = b.get("url", "")
    src  = b.get("source", "")
    if url:
        return (
            f'<li class="has-link">'
            f'<a href="{_e(url)}" target="_blank" rel="noopener noreferrer" class="bullet-link">'
            f'{_e(text)}{_src_tag(src)}</a></li>'
        )
    return f'<li>{_e(text)}{_src_tag(src)}</li>'

def _card_html(icon: str, badge: str, badge_color: str, title: str,
               title_url: str, bullets: list[dict],
               extra_class: str = "") -> str:
    title_html = (
        f'<a href="{_e(title_url)}" target="_blank" rel="noopener noreferrer" '
        f'class="trump-title-link">{_e(title)}</a>'
        if title_url else _e(title)
    )
    bullets_html = (
        "\n".join(_bullet_html(b) for b in bullets)
        if bullets
        else '<li class="no-data">No data for this period.</li>'
    )
    return f"""
    <div class="trump-card {extra_class}" style="border-left-color:{badge_color};">
      <div class="trump-card-header">
        <span class="trump-icon">{icon}</span>
        <span class="trump-badge" style="background:{badge_color};">{_e(badge)}</span>
        <span class="trump-card-title">{title_html}</span>
      </div>
      <ul class="trump-bullets">
        {bullets_html}
      </ul>
    </div>"""

SECTIONS_DEF = [
    ("📱", "Social Media",         "#3C3B6E", "Truth Social Posts",
     "https://truthsocial.com/@realDonaldTrump", "sns", ""),
    ("🎤", "Press / Interviews",   "#C81E32", "Press Conferences & Media",
     "https://www.whitehouse.gov/briefings-statements/", "press_conference", ""),
    ("📜", "Executive Actions",    "#B48200", "White House Orders & Releases",
     "https://www.whitehouse.gov/presidential-actions/", "whitehouse_official", ""),
    ("🎙", "WH Briefing",          "#3C3B6E", "Press Secretary Briefing",
     "https://www.whitehouse.gov/briefings-statements/", "wh_briefing", ""),
    ("🎬", "Video Content",        "#C81E32", "YouTube / White House Video",
     "https://www.youtube.com/@WhiteHouse", "video", ""),
    ("👥", "Cabinet Moves",        "#B48200", "Key Cabinet Activity",
     _gn("Trump cabinet Bessent Rubio Hegseth Vance statement"), "cabinet", ""),
    ("🇯🇵", "Japan Impact",       "#C81E32", "Impact on Japan",
     _gn("Japan security economy Trump policy impact"), "japan_impact", "japan-highlight"),
]

def generate_en_html(data: dict) -> None:
    print("── docs/en/trump.html 生成中 ────────────────")

    now_jst = datetime.now(timezone(timedelta(hours=9)))
    date_en  = now_jst.strftime("%B %d, %Y")
    updated  = now_jst.strftime("%Y-%m-%d %H:%M JST")
    dr       = data.get("date_range", DATE_RANGE)
    gen_at   = data.get("generated_at", "")
    item_cnt = data.get("item_count", 0)
    sources  = data.get("sources_summary", [])

    # Source bar chips
    source_chips = "\n".join(
        f'<div class="source-chip"><span>{s["icon"]}</span>{_e(s["label"])}: {_e(s["count"])}</div>'
        for s in sources
    )

    # Featured card (key_points)
    key_bullets = data.get("key_points", [])
    featured_html = _card_html(
        "⭐", "Key Points", "#B48200",
        "Today's Highlights",
        _gn("Trump statement White House today"),
        key_bullets, "featured",
    )

    # Grid cards
    grid_cards = []
    for icon, badge, color, title, title_url, key, extra in SECTIONS_DEF:
        grid_cards.append(_card_html(
            icon, badge, color, title, title_url,
            data.get(key, []), extra,
        ))
    grid_html = "\n".join(grid_cards)

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>US / Trump | World Intelligence Monitor</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif; background: #f4f5f7; color: #1a1a2e; font-size: 16px; line-height: 1.7; }}
.site-header {{ background: #1a1a2e; color: #fff; padding: 0 24px; height: 58px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 300; box-shadow: 0 2px 8px rgba(0,0,0,.25); }}
.logo {{ font-size: 20px; font-weight: 700; letter-spacing: .5px; white-space: nowrap; cursor: pointer; }}
.logo em {{ color: #5bc8f5; font-style: normal; }}
.header-date {{ font-size: 12px; color: rgba(255,255,255,.5); white-space: nowrap; }}
.header-spacer {{ flex: 1; }}
.live-badge {{ background: #e63946; color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }}
.update-time {{ font-size: 11px; color: rgba(255,255,255,.4); white-space: nowrap; }}
.lang-toggle {{ display: flex; gap: 6px; font-size: 12px; }}
.lang-toggle a {{ color: rgba(255,255,255,.6); text-decoration: none; padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,.3); transition: all .15s; font-weight: 600; }}
.lang-toggle a.active {{ color: #fff; background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.7); }}
.lang-toggle a:hover {{ color: #fff; background: rgba(255,255,255,.12); }}
.page-nav {{ background: #fff; border-bottom: 1px solid #e5e7eb; padding: 0 24px; display: flex; align-items: stretch; position: sticky; top: 58px; z-index: 200; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
.page-nav a {{ display: flex; align-items: center; gap: 6px; padding: 0 18px; height: 44px; font-size: 14px; font-weight: 500; color: #6b7280; text-decoration: none; border-bottom: 3px solid transparent; white-space: nowrap; transition: color .15s, border-color .15s; }}
.page-nav a:hover {{ color: #1a1a2e; }}
.page-nav a.active {{ color: #1a1a2e; border-bottom-color: #1a1a2e; font-weight: 700; }}
.page-nav a .nav-icon {{ font-size: 15px; }}
.page-nav a:last-child {{ margin-left: auto; border-left: 1px solid #e5e7eb; }}
.page-nav a.dim {{ opacity: .45; pointer-events: none; }}
.section-label {{ font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1.2px; margin: 0 0 12px; padding-bottom: 8px; border-bottom: 2px solid #e5e7eb; }}
li.has-link {{ cursor: pointer; }}
.bullet-link {{ display: block; color: inherit; text-decoration: none; transition: color .15s; }}
.bullet-link:hover {{ color: #0096c8; }}
.src-tag {{ display: inline-block; font-size: 11px; font-weight: 600; color: #9ca3af; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 4px; padding: 1px 6px; margin-left: 6px; vertical-align: middle; white-space: nowrap; opacity: 0.75; transition: opacity .15s, color .15s, background .15s, border-color .15s; }}
.bullet-link:hover .src-tag {{ opacity: 1; color: #0096c8; background: #e8f4ff; border-color: #0096c8; }}
.trump-title-link {{ color: inherit; text-decoration: none; transition: color .15s; }}
.trump-title-link:hover {{ color: #0096c8; }}
.trump-title-link:hover::after {{ content: " ↗"; font-size: 13px; opacity: .7; }}
.site-footer {{ text-align: center; padding: 28px 20px; font-size: 11px; color: #9ca3af; margin-top: 32px; border-top: 1px solid #e5e7eb; }}
@media (max-width: 640px) {{ .site-header {{ padding: 0 14px; }} .update-time {{ display: none; }} .page-nav {{ padding: 0 8px; }} .page-nav a {{ padding: 0 12px; font-size: 13px; }} }}
.trump-wrap {{ max-width: 1040px; margin: 24px auto; padding: 0 20px; }}
.trump-banner {{ background: linear-gradient(135deg, #16163e 0%, #3C3B6E 60%, #1a0a0a 100%); border-radius: 8px; padding: 18px 24px; margin-bottom: 16px; display: flex; align-items: center; gap: 20px; border: 1px solid #4a3a6e; flex-wrap: wrap; }}
.trump-banner-title {{ font-size: 22px; font-weight: 700; color: #fff; letter-spacing: .5px; }}
.trump-banner-title span {{ color: #C81E32; }}
.trump-banner-sub {{ font-size: 12px; color: rgba(255,255,255,.55); margin-top: 3px; }}
.trump-banner-spacer {{ flex: 1; }}
.trump-stats {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.trump-stat {{ text-align: center; background: rgba(255,255,255,.08); border-radius: 8px; padding: 8px 14px; }}
.trump-stat-num {{ font-size: 18px; font-weight: 700; color: #B48200; }}
.trump-stat-lbl {{ font-size: 10px; color: rgba(255,255,255,.5); }}
.source-bar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }}
.source-chip {{ display: flex; align-items: center; gap: 5px; background: #fff; border: 1px solid #e5e7eb; border-radius: 20px; padding: 5px 12px; font-size: 12px; color: #6b7280; }}
.trump-card {{ background: #fff; border-radius: 8px; border: 1px solid #e5e7eb; border-left: 5px solid #0096c8; box-shadow: 0 1px 4px rgba(0,0,0,.06); padding: 18px 22px; transition: box-shadow .2s; }}
.trump-card:hover {{ box-shadow: 0 4px 16px rgba(0,0,0,.1); }}
.trump-card.featured {{ background: linear-gradient(135deg, #fffbe6, #fff8e1); border-left-color: #B48200; border-left-width: 6px; padding: 22px 28px; margin-bottom: 20px; }}
.trump-card.japan-highlight {{ background: #fff0f2; border-left-color: #C81E32; }}
.trump-card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }}
.trump-icon {{ font-size: 20px; }}
.trump-badge {{ font-size: 11px; font-weight: 700; color: #fff; padding: 3px 10px; border-radius: 12px; white-space: nowrap; }}
.trump-card-title {{ font-size: 18px; font-weight: 700; color: #1a1a2e; margin-left: 4px; }}
.trump-card.featured .trump-card-title {{ font-size: 20px; color: #5a3a00; }}
.trump-bullets {{ list-style: none; padding: 0; }}
.trump-bullets li {{ position: relative; padding-left: 20px; font-size: 15px; color: #2a2a3e; margin-bottom: 9px; line-height: 1.6; }}
.trump-bullets li::before {{ content: "▸"; position: absolute; left: 0; color: #0096c8; font-weight: 700; }}
.trump-card.featured .trump-bullets li::before {{ color: #B48200; }}
.trump-card.japan-highlight .trump-bullets li::before {{ color: #C81E32; }}
.trump-card .bullet-link:hover .src-tag {{ color: #C81E32; background: #fff0f2; border-color: #C81E32; }}
.no-data {{ font-size: 14px; color: #9ca3af; font-style: italic; }}
.trump-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
@media (max-width: 640px) {{ .trump-wrap {{ padding: 0 12px; }} .trump-banner {{ padding: 14px; }} .trump-banner-title {{ font-size: 18px; }} .trump-stats {{ display: none; }} }}
</style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'">World<em>News</em></div>
  <div class="header-date">{date_en}</div>
  <div class="header-spacer"></div>
  <div class="update-time">Updated: {updated} &nbsp;|&nbsp; auto-update every 6h</div>
  <div class="lang-toggle">
    <a href="../trump.html">JP</a>
    <a href="trump.html" class="active">EN</a>
  </div>
  <div class="live-badge">LIVE</div>
</header>
<nav class="page-nav">
  <a href="index.html"><span class="nav-icon">🏠</span>Home</a>
  <a href="intelligence.html"><span class="nav-icon">📋</span>Intelligence</a>
  <a href="trump.html" class="active"><span class="nav-icon">🇺🇸</span>US / Trump</a>
  <a href="theme.html" class="dim"><span class="nav-icon">🔎</span>Themes</a>
  <a href="midterm.html" class="dim"><span class="nav-icon">🗳️</span>US Midterms</a>
  <a href="summary.html" class="dim"><span class="nav-icon">📋</span>Exec Summary</a>
</nav>
<div class="trump-wrap">
  <div class="trump-banner">
    <div>
      <div class="trump-banner-title">TRUMP <span>MONITOR</span></div>
      <div class="trump-banner-sub">Coverage: {_e(dr)} (UTC)
        &nbsp;|&nbsp; <span style="opacity:.6;font-size:11px;">Generated: {_e(gen_at)}</span>
      </div>
    </div>
    <div class="trump-banner-spacer"></div>
    <div class="trump-stats">
      <div class="trump-stat"><div class="trump-stat-num">{item_cnt}</div><div class="trump-stat-lbl">Items</div></div>
      <div class="trump-stat"><div class="trump-stat-num">8</div><div class="trump-stat-lbl">Sections</div></div>
    </div>
  </div>
  <div class="source-bar">
    {source_chips}
  </div>
  <p class="section-label">Key Points</p>
  {featured_html}
  <p class="section-label">Detailed Analysis</p>
  <div class="trump-grid">
    {grid_html}
  </div>
</div>
<footer class="site-footer">
  Sources: NHK &middot; Nikkei &middot; Reuters &middot; Bloomberg &middot; FT &middot; BBC &middot; NYT &middot; Al Jazeera &middot; White House RSS &middot; Truth Social &middot; The Economist<br>
  Updated: {updated} &nbsp;|&nbsp; Auto-update every 6h &nbsp;|&nbsp; World Intelligence Monitor
</footer>
<script>
document.addEventListener('DOMContentLoaded', () => {{
  const grid = document.querySelector('.trump-grid');
  const jp = grid && grid.querySelector('.japan-highlight');
  if (jp) grid.appendChild(jp);
}});
</script>
</body>
</html>
"""
    OUT_EN.parent.mkdir(parents=True, exist_ok=True)
    OUT_EN.write_text(html_out, encoding="utf-8")
    print(f"  保存: {OUT_EN}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 4: 英語JSON → 日本語JSON に翻訳
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JA_SYSTEM = """\
あなたはアメリカ政治の専門アナリストです。
英語のbulletsを自然な日本語に翻訳してください。
出力はJSON配列のみ。マークダウンフェンス・説明文は不要です。\
"""

def translate_to_japanese(en_data: dict) -> dict:
    print("── 日本語翻訳中（Claude）────────────────────")
    client  = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    ja_data = dict(en_data)

    keys_to_translate = [
        "key_points", "sns", "press_conference", "whitehouse_official",
        "wh_briefing", "video", "cabinet", "japan_impact",
    ]

    for key in keys_to_translate:
        bullets = en_data.get(key, [])
        if not bullets:
            ja_data[key] = []
            continue

        texts = [b.get("text", "") for b in bullets]
        prompt = (
            "以下の英語bulletsを日本語に翻訳してください。\n"
            "wire-serviceスタイルの短い英語を、自然な日本語の短文（最大60文字）に。\n"
            "URLとsourceはそのまま維持し、textのみ翻訳します。\n"
            "出力はJSON配列のみ（{\"text\":\"...\"}のリスト）:\n\n"
            + json.dumps(texts, ensure_ascii=False, indent=2)
        )
        resp = client.messages.create(
            model=MODEL, max_tokens=2000, system=JA_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        raw = re.sub(r'^```(?:json)?\s*\n?', '', raw)
        raw = re.sub(r'\n?```\s*$', '', raw)

        try:
            ja_texts = json.loads(raw)
            ja_bullets = []
            for i, b in enumerate(bullets):
                ja_text = (
                    ja_texts[i].get("text", b["text"])
                    if i < len(ja_texts) and isinstance(ja_texts[i], dict)
                    else (ja_texts[i] if i < len(ja_texts) and isinstance(ja_texts[i], str)
                          else b["text"])
                )
                ja_bullets.append({"text": ja_text, "source": b.get("source", ""), "url": b.get("url", "")})
            ja_data[key] = ja_bullets
        except (json.JSONDecodeError, IndexError):
            ja_data[key] = bullets  # 翻訳失敗時は英語のまま

        print(f"  {key}: {len(ja_data[key])} 件翻訳")

    # sources_summary も日本語ラベルに変換
    ja_sources_map = {
        "Truth Social":        "Truth Social",
        "YouTube (captioned)": "YouTube（字幕あり）",
        "Google News":         "Google News",
        "White House RSS":     "ホワイトハウスRSS",
        "Executive Actions":   "大統領令・行政措置",
    }
    ja_sources = []
    for s in en_data.get("sources_summary", []):
        ja_label = ja_sources_map.get(s["label"], s["label"])
        cnt_str  = s["count"].replace(" items", "件")
        ja_sources.append({"icon": s["icon"], "label": ja_label, "count": cnt_str})
    ja_data["sources_summary"] = ja_sources

    print()
    return ja_data


def save_ja_json(ja_data: dict) -> Path:
    OUT_JA_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JA_JSON.write_text(json.dumps(ja_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  保存: {OUT_JA_JSON}\n")
    return OUT_JA_JSON


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 5: generate_site.py → docs/trump.html 更新
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def update_ja_html() -> None:
    print("── docs/trump.html 更新中（generate_site.py）─")
    python = sys.executable
    result = subprocess.run(
        [python, str(BASE_DIR / "generate_site.py")],
        capture_output=True, text=True, encoding="utf-8",
        cwd=str(BASE_DIR),
    )
    if result.returncode == 0:
        print("  docs/trump.html 更新完了\n")
    else:
        print(f"  [WARN] generate_site.py エラー:\n{result.stderr[:500]}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メイン
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    parser = argparse.ArgumentParser(description="Trump Monitor 英語ファースト更新")
    parser.add_argument("--skip-collect", action="store_true",
                        help="データ収集をスキップし既存の trump_en_latest.json を再利用")
    parser.add_argument("--en-only", action="store_true",
                        help="英語HTML生成のみ（日本語更新をスキップ）")
    args = parser.parse_args()

    print("=" * 52)
    print("  Trump Monitor — English-First Update")
    print(f"  Coverage: {YESTERDAY} ~ {TODAY} (UTC)")
    print("=" * 52 + "\n")

    if args.skip_collect and OUT_EN_JSON.exists():
        print("── 既存JSONを再利用 ──────────────────────────")
        en_data = json.loads(OUT_EN_JSON.read_text(encoding="utf-8"))
        print(f"  {OUT_EN_JSON}\n")
    else:
        # Step 1: 収集
        items = collect_all()
        # Step 2: 英語JSON生成
        structured = summarize_en(items)
        en_data = {
            "generated_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date_range":      DATE_RANGE,
            "item_count":      len(items),
            "sources_summary": [],
            **structured,
        }
        save_en_json(structured, items)

    # Step 3: 英語HTML生成
    generate_en_html(en_data)
    print("✓ docs/en/trump.html 完成")

    if not args.en_only:
        # Step 4: 日本語翻訳
        ja_data = translate_to_japanese(en_data)
        save_ja_json(ja_data)
        # Step 5: 日本語HTML更新
        update_ja_html()
        print("✓ docs/trump.html 完成")

    print("\n完了。")
    print(f"  EN: {OUT_EN}")
    print(f"  JP: {BASE_DIR / 'docs' / 'trump.html'}")


if __name__ == "__main__":
    main()
