#!/usr/bin/env python3
"""
make_en_theme.py
================
Individual Theme Monitor — English version generator

Steps:
  1. Load docs/data/theme_latest.json (collected by theme_monitor.py)
  2. Translate Japanese summaries + descriptions to English (Claude Haiku)
  3. Generate docs/en/theme.html

Usage:
  python make_en_theme.py
  python make_en_theme.py --skip-translate   # re-generate HTML without Claude call
"""

import argparse
import html
import json
import os
import re
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

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
THEME_JSON    = BASE_DIR / "docs" / "data" / "theme_latest.json"
OUT_EN        = BASE_DIR / "docs" / "en" / "theme.html"
EN_CACHE_JSON = BASE_DIR / "db" / "theme_en_cache.json"

MODEL         = "claude-haiku-4-5-20251001"
CUTOFF_DAYS   = 7   # show items from the last N days
NEW_BADGE_DAYS = 3  # mark items as NEW within this many days

# ── Source-type metadata (English labels) ─────────────────────────────────────
_SRC_META_EN = {
    "official":   ("Official",     "theme-src-official",   "🏛️"),
    "politician":  ("Politicians",  "theme-src-politician",  "👤"),
    "industry":   ("Industry",     "theme-src-industry",    "🏭"),
    "china":      ("China Gov't",  "theme-src-china",       "🇨🇳"),
    "media":      ("Media",        "theme-src-media",       "📰"),
}

FILTER_DEFS_EN = [
    ("all",        "All"),
    ("official",   "🏛️ Official"),
    ("politician", "👤 Politicians"),
    ("industry",   "🏭 Industry"),
    ("china",      "🇨🇳 China Gov't"),
    ("media",      "📰 Media"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def _e(s: str) -> str:
    return html.escape(str(s))

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def _cutoff_date() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=CUTOFF_DAYS)).strftime("%Y-%m-%d")

def _new_cutoff() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=NEW_BADGE_DAYS)).strftime("%Y-%m-%d")

def _is_new(date_str: str) -> bool:
    return date_str >= _new_cutoff()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 1: Load JSON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_theme_data() -> dict:
    if not THEME_JSON.exists():
        print(f"[ERROR] {THEME_JSON} not found. Run theme_monitor.py first.")
        sys.exit(1)
    data = json.loads(THEME_JSON.read_text(encoding="utf-8"))
    if not data.get("themes"):
        print("[ERROR] theme_latest.json has no themes.")
        sys.exit(1)
    print(f"Loaded {THEME_JSON}")
    return data


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 2: Translate Japanese text to English (batch per theme)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EN_TRANSLATE_SYSTEM = """\
You are a political/economic analyst. Translate Japanese text to English.
Wire-service style: concise, active voice, max 80 words per summary.
Output ONLY a JSON array of translated strings, same order as input.
No markdown fences, no explanations.\
"""

def _translate_batch(texts: list[str], label: str) -> list[str]:
    """Translate a list of Japanese strings to English via Claude Haiku."""
    if not texts:
        return []
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = (
        "Translate each Japanese text below to English (wire-service style, max 80 words each).\n"
        "Return a JSON array of strings in the same order:\n\n"
        + json.dumps(texts, ensure_ascii=False, indent=2)
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=4000, system=EN_TRANSLATE_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*\n?', '', raw)
    raw = re.sub(r'\n?```\s*$', '', raw)
    try:
        result = json.loads(raw)
        if isinstance(result, list) and len(result) == len(texts):
            print(f"  {label}: {len(result)} texts translated")
            return result
    except json.JSONDecodeError:
        pass
    print(f"  [WARN] {label}: translation parse failed, using originals")
    return texts


def translate_themes(data: dict) -> dict:
    """
    For each theme:
      - translate description (Japanese → English)
      - translate summaries of recent items (Japanese → English)
    Returns a new dict with English text injected.
    """
    print("── Translating Japanese text to English (Claude Haiku) ──────────")
    cutoff = _cutoff_date()
    client_data = json.loads(json.dumps(data))  # deep copy

    for theme in client_data.get("themes", []):
        tid = theme.get("id", "")

        # Translate theme description
        ja_desc = theme.get("description", "")
        if ja_desc:
            en_descs = _translate_batch([ja_desc], f"{tid}.description")
            theme["description_en"] = en_descs[0] if en_descs else ja_desc

        # Filter to recent items, then translate summaries
        recent = [it for it in theme.get("items", []) if it.get("date", "") >= cutoff]
        ja_summaries = [it.get("summary", "") for it in recent]

        # Split into chunks of 20 to stay within token limits
        CHUNK = 20
        en_summaries: list[str] = []
        for i in range(0, len(ja_summaries), CHUNK):
            chunk = ja_summaries[i:i + CHUNK]
            translated = _translate_batch(chunk, f"{tid}.summaries[{i}:{i+len(chunk)}]")
            en_summaries.extend(translated)

        # Inject translations back
        for it, en_sum in zip(recent, en_summaries):
            it["summary_en"] = en_sum

    print()
    return client_data


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Step 3: Generate docs/en/theme.html
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _render_item(item: dict) -> str:
    date_s   = _e(item.get("date", ""))
    title    = _e(item.get("title", ""))
    summary  = _e(item.get("summary_en") or item.get("summary", ""))
    url      = _e(item.get("url", ""))
    src_type = item.get("source_type", "media")
    src_name = _e(item.get("source", ""))
    is_new   = _is_new(item.get("date", ""))

    src_label, src_cls, src_icon = _SRC_META_EN.get(src_type, ("Info", "theme-src-media", "📄"))

    new_badge = '<span class="theme-new-badge">🆕 NEW</span>' if is_new else ""
    src_badge = f'<span class="theme-src-badge {src_cls}">{src_icon} {src_label}</span>'
    date_span = f'<span class="theme-date">📅 {date_s}</span>'

    if url:
        title_html = (
            f'<span class="theme-item-title">'
            f'<a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>'
            f'</span>'
        )
    else:
        title_html = f'<span class="theme-item-title">{title}</span>'

    item_cls = "theme-item is-new" if is_new else "theme-item"
    return f"""<div class="{item_cls}" data-src="{_e(src_type)}">
  <div class="theme-item-header">
    {new_badge}{src_badge}{date_span}
    {title_html}
  </div>
  <div class="theme-summary">{summary}</div>
  <div class="theme-source-name">Source: {src_name}</div>
</div>"""


def _render_panel(theme: dict, is_first: bool, gen_at: str) -> str:
    tid      = _e(theme.get("id", ""))
    color    = _e(theme.get("color", "#003F8A"))
    icon     = theme.get("icon", "")
    name_en  = _e(theme.get("name_en") or theme.get("name", ""))
    desc_en  = _e(theme.get("description_en") or theme.get("description", ""))
    last_chk = _e(theme.get("last_checked", gen_at))

    cutoff = _cutoff_date()
    all_items = theme.get("items", [])
    items = sorted(
        [it for it in all_items if it.get("date", "") >= cutoff],
        key=lambda it: it.get("date", ""),
        reverse=True,
    )
    new_count  = sum(1 for it in items if _is_new(it.get("date", "")))
    display_style = "" if is_first else "display:none;"
    banner_style  = f'style="background:linear-gradient(135deg,{color} 0%,{color}cc 70%,{color}88 100%);"'

    stat_html = (
        f'<div class="theme-stat"><div class="theme-stat-num">{len(items)}</div>'
        f'<div class="theme-stat-lbl">Last 7 days</div></div>'
        f'<div class="theme-stat"><div class="theme-stat-num">{new_count}</div>'
        f'<div class="theme-stat-lbl">New (3d)</div></div>'
    )

    data_note = f'Last collected: {last_chk}'

    existing_types = {it.get("source_type", "media") for it in items}
    filter_btns = ""
    for ftype, flabel in FILTER_DEFS_EN:
        if ftype == "all" or ftype in existing_types:
            active_cls = ' active' if ftype == "all" else ""
            filter_btns += (
                f'  <button class="theme-filter-btn{active_cls}" '
                f'data-filter="{ftype}">{flabel}</button>\n'
            )

    if items:
        items_html = "\n".join(_render_item(it) for it in items)
    else:
        items_html = '<div class="theme-empty">📡 Data collection in progress. Updates every 6 hours via GitHub Actions.</div>'

    return f"""<div id="panel-{tid}" class="theme-panel" style="{display_style}--tc:{color};">
  <div class="theme-banner" {banner_style}>
    <div>
      <div class="theme-banner-title">{icon} {name_en}</div>
      <div class="theme-banner-desc">{desc_en} &nbsp;|&nbsp; <span style="opacity:.7;font-size:10px;">{data_note}</span></div>
    </div>
    <div class="theme-banner-spacer"></div>
    <div class="theme-stats">{stat_html}</div>
  </div>
  <div class="theme-filter-bar">
{filter_btns}  </div>
  <div class="theme-list">
{items_html}
  </div>
</div>"""


def generate_en_html(data: dict) -> None:
    print("── Generating docs/en/theme.html ────────────────────────────────")

    now_jst  = datetime.now(timezone(timedelta(hours=9)))
    date_en  = now_jst.strftime("%B %d, %Y")
    updated  = now_jst.strftime("%Y-%m-%d %H:%M JST")
    gen_at   = data.get("generated_at", "")
    themes   = data.get("themes", [])

    # Tab buttons
    tab_btns = ""
    for i, t in enumerate(themes):
        active_cls = " active" if i == 0 else ""
        tc    = _e(t.get("color", "#333"))
        style = f' style="background:{tc}; border-color:{tc};"' if i == 0 else ""
        name_en = _e(t.get("name_en") or t.get("name", ""))
        icon    = t.get("icon", "")
        tab_btns += (
            f'  <button class="theme-tab{active_cls}" data-theme="{_e(t["id"])}"{style}>'
            f'{icon} {name_en}</button>\n'
        )

    # Panels
    panels_html = "\n".join(
        _render_panel(t, i == 0, gen_at)
        for i, t in enumerate(themes)
    )

    # JS color map
    color_map = "{" + ",".join(f'"{_e(t["id"])}":"{_e(t.get("color","#333"))}"' for t in themes) + "}"

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Themes | World Intelligence Monitor</title>
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
.site-footer {{ text-align: center; padding: 28px 20px; font-size: 11px; color: #9ca3af; margin-top: 32px; border-top: 1px solid #e5e7eb; }}
@media (max-width: 640px) {{ .site-header {{ padding: 0 14px; }} .update-time {{ display: none; }} .page-nav {{ padding: 0 8px; }} .page-nav a {{ padding: 0 12px; font-size: 13px; }} }}
.theme-wrap {{ max-width: 1040px; margin: 24px auto; padding: 0 20px; }}
.theme-tabs-nav {{ display: flex; gap: 6px; flex-wrap: wrap; background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 8px 12px; margin-bottom: 14px; }}
.theme-tab {{ padding: 6px 18px; border-radius: 20px; font-size: 13px; font-weight: 600; cursor: pointer; border: 1.5px solid #ccc; background: #fff; color: #555; transition: all .15s; white-space: nowrap; }}
.theme-tab.active {{ color: #fff; border-color: transparent; }}
.theme-tab:not(.active):hover {{ background: #f0f4ff; border-color: #aac; }}
.theme-panel {{ --tc: #003F8A; }}
.theme-banner {{ border-radius: 12px; padding: 18px 24px; margin-bottom: 16px; display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }}
.theme-banner-title {{ font-size: 20px; font-weight: 700; color: #fff; letter-spacing: .4px; }}
.theme-banner-desc {{ font-size: 11px; color: rgba(255,255,255,.6); margin-top: 3px; }}
.theme-banner-spacer {{ flex: 1; }}
.theme-stats {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.theme-stat {{ text-align: center; background: rgba(255,255,255,.12); border-radius: 8px; padding: 8px 14px; }}
.theme-stat-num {{ font-size: 18px; font-weight: 700; color: #FFCC00; }}
.theme-stat-lbl {{ font-size: 10px; color: rgba(255,255,255,.5); }}
.theme-item {{ background: #fff; border-radius: 12px; border: 1px solid #e5e7eb; border-left: 4px solid var(--tc); padding: 14px 18px; margin-bottom: 10px; transition: box-shadow .2s; }}
.theme-item:hover {{ box-shadow: 0 4px 14px rgba(0,0,0,.08); }}
.theme-item.is-new {{ border-left-color: #F59E0B; background: #fffef0; }}
.theme-item-header {{ display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }}
.theme-new-badge {{ background: #F59E0B; color: #fff; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 10px; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }}
.theme-src-badge {{ font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }}
.theme-src-official   {{ background: #dbeafe; color: #1d4ed8; }}
.theme-src-politician {{ background: #fff3cd; color: #92400e; }}
.theme-src-industry   {{ background: #fce7f3; color: #9d174d; }}
.theme-src-china      {{ background: #fee2e2; color: #991b1b; }}
.theme-src-media      {{ background: #d1fae5; color: #065f46; }}
.theme-date {{ font-size: 11px; color: #6b7280; flex-shrink: 0; margin-top: 3px; white-space: nowrap; }}
.theme-item-title {{ font-size: 16px; font-weight: 600; color: #1a1a2e; line-height: 1.5; flex: 1; min-width: 0; }}
.theme-item-title a {{ color: inherit; text-decoration: none; }}
.theme-item-title a:hover {{ color: var(--tc); text-decoration: underline; }}
.theme-summary {{ font-size: 14px; color: #374151; line-height: 1.75; margin-top: 5px; }}
.theme-source-name {{ font-size: 11px; color: #aaa; margin-top: 4px; }}
.theme-filter-bar {{ display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 14px; }}
.theme-filter-btn {{ padding: 4px 13px; border-radius: 20px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1.5px solid #ccc; background: #fff; color: #555; transition: all .15s; }}
.theme-filter-btn.active {{ background: var(--tc); color: #fff; border-color: var(--tc); }}
.theme-filter-btn:not(.active):hover {{ border-color: var(--tc); color: var(--tc); }}
.theme-empty {{ text-align: center; color: #6b7280; font-size: 14px; padding: 40px 20px; }}
@media (max-width: 640px) {{ .theme-wrap {{ padding: 0 12px; }} .theme-banner {{ padding: 14px; }} .theme-banner-title {{ font-size: 16px; }} .theme-stats {{ display: none; }} .theme-tab {{ font-size: 12px; padding: 5px 12px; }} }}
</style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'">World<em>News</em></div>
  <div class="header-date">{date_en}</div>
  <div class="header-spacer"></div>
  <div class="update-time">Updated: {updated} &nbsp;|&nbsp; auto-update every 6h</div>
  <div class="lang-toggle">
    <a href="../jp/theme.html">JP</a>
    <a href="theme.html" class="active">EN</a>
  </div>
  <div class="live-badge">LIVE</div>
</header>
<nav class="page-nav">
  <a href="index.html"><span class="nav-icon">🏠</span>Home</a>
  <a href="intelligence.html"><span class="nav-icon">📋</span>Intelligence</a>
  <a href="trump.html"><span class="nav-icon">🇺🇸</span>US / Trump</a>
  <a href="theme.html" class="active"><span class="nav-icon">🔎</span>Themes</a>
  <a href="midterm.html"><span class="nav-icon">🗳️</span>US Midterms</a>
  <a href="summary.html"><span class="nav-icon">📋</span>Exec Summary</a>
</nav>
<div class="theme-wrap">
  <p class="section-label" style="margin-top:8px;">Monitoring Themes</p>
  <div class="theme-tabs-nav">
{tab_btns}  </div>
{panels_html}
</div>
<footer class="site-footer">
  Sources: Reuters &middot; Bloomberg &middot; FT &middot; EURACTIV &middot; EUobserver &middot; EU Parliament &middot; European Commission &middot; Automotive News &middot; POLITICO &middot; The Hill &middot; Google News<br>
  Updated: {updated} &nbsp;|&nbsp; Auto-update every 6h &nbsp;|&nbsp; World Intelligence Monitor
</footer>
<script>
(function(){{
  var colorMap = {color_map};

  var tabs   = document.querySelectorAll('.theme-tab');
  var panels = document.querySelectorAll('.theme-panel');
  tabs.forEach(function(tab){{
    tab.addEventListener('click', function(){{
      var tid = tab.dataset.theme;
      tabs.forEach(function(t){{
        var c = colorMap[t.dataset.theme] || '#333';
        if(t.dataset.theme === tid){{
          t.classList.add('active');
          t.style.background = c; t.style.borderColor = c;
        }} else {{
          t.classList.remove('active');
          t.style.background = ''; t.style.borderColor = '';
        }}
      }});
      panels.forEach(function(p){{
        p.style.display = (p.id === 'panel-' + tid) ? '' : 'none';
      }});
    }});
  }});

  panels.forEach(function(panel){{
    var tc   = panel.style.getPropertyValue('--tc') || '#003F8A';
    var btns = panel.querySelectorAll('.theme-filter-btn');
    var cards = panel.querySelectorAll('.theme-list .theme-item');
    btns.forEach(function(btn){{
      btn.addEventListener('click', function(){{
        btns.forEach(function(b){{
          b.classList.remove('active');
          b.style.background=''; b.style.borderColor=''; b.style.color='';
        }});
        btn.classList.add('active');
        btn.style.background = tc; btn.style.borderColor = tc; btn.style.color = '#fff';
        var f = btn.dataset.filter;
        cards.forEach(function(c){{
          c.style.display = (f === 'all' || c.dataset.src === f) ? '' : 'none';
        }});
      }});
    }});
  }});
}})();
</script>
</body>
</html>
"""
    OUT_EN.parent.mkdir(parents=True, exist_ok=True)
    OUT_EN.write_text(html_out, encoding="utf-8")
    print(f"  Saved: {OUT_EN}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    parser = argparse.ArgumentParser(description="Theme Monitor — English HTML generator")
    parser.add_argument("--skip-translate", action="store_true",
                        help="Skip Claude translation; use existing text (titles are already English)")
    args = parser.parse_args()

    print("=" * 52)
    print("  Theme Monitor — English Version Generator")
    print(f"  Cutoff: last {CUTOFF_DAYS} days")
    print("=" * 52 + "\n")

    data = load_theme_data()

    if args.skip_translate:
        print("── Skipping translation (--skip-translate) ──────────────────────\n")
        en_data = data
    else:
        en_data = translate_themes(data)

    generate_en_html(en_data)
    print(f"✓ {OUT_EN}")


if __name__ == "__main__":
    main()
