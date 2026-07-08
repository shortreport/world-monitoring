"""
generate_en_home.py
英語版ホームページ (docs/en/index.html) を生成するスクリプト

- home_latest.json の日本語テキストを Claude Haiku で英訳
- economist_latest.json の日本語要約を自然な英語に変換（元が英語のため）
- docs/en/index.html として出力
- 手動実行のみ（自動更新なし）
"""
import os
import json
import sys
from pathlib import Path
import anthropic

# ── パス設定 ────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).parent
DOCS_DATA_DIR    = BASE_DIR / "docs" / "data"
HOME_JSON        = DOCS_DATA_DIR / "home_latest.json"
ECONOMIST_JSON   = DOCS_DATA_DIR / "economist_latest.json"
OUT_DIR          = BASE_DIR / "docs" / "en"
OUT_HTML         = OUT_DIR / "index.html"

CLAUDE_MODEL     = "claude-haiku-4-5-20251001"
CLAUDE_API_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ── 翻訳 ────────────────────────────────────────────────────────────────────
def _parse_json(text: str):
    """マークダウンフェンスを除去してJSONをパース"""
    import re
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text.strip())


def translate_home(segments: list, client: anthropic.Anthropic) -> list:
    """home_latest.json の segments を英訳して返す"""
    payload = [
        {
            "badge":    s["badge"],
            "title":    s["title"],
            "subtitle": s["subtitle"],
            "bullets":  [b["text"] for b in s["bullets"]],
            "risk":     s.get("risk", ""),
            "context":  s.get("context", ""),
        }
        for s in segments
    ]
    prompt = (
        "You are translating an executive intelligence briefing from Japanese to English.\n"
        "Translate the following JSON naturally into English. Rules:\n"
        "- 'badge': translate the label only (e.g. '① 米イラン関係' → '① US-Iran')\n"
        "- 'title': crisp headline, 3-6 words\n"
        "- 'subtitle': concise sub-headline\n"
        "- 'bullets': each bullet as a clean declarative sentence (no leading bullet symbol)\n"
        "- 'risk': translate the risk note; keep '▲Risk:' prefix in English\n"
        "- 'context': translate the background note; keep 'Background:' prefix\n"
        "Return ONLY a valid JSON array with the same structure. No markdown fences.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )
    msg = client.messages.create(
        model=CLAUDE_MODEL, max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    return _parse_json(msg.content[0].text)


def translate_economist(bullets: list, section: str, client: anthropic.Anthropic) -> list:
    """Economist 要約（日本語）を自然な英語に戻す"""
    payload = "\n".join(f"- {b}" for b in bullets)
    prompt = (
        f"The following are Japanese summaries of The Economist's '{section}' section.\n"
        "The original source was English. Translate these back into crisp, natural English "
        "in the style of The Economist — authoritative, precise, no bullet symbols.\n"
        "Return ONLY a JSON array of strings, one per bullet. No markdown fences.\n\n"
        f"{payload}"
    )
    msg = client.messages.create(
        model=CLAUDE_MODEL, max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return _parse_json(msg.content[0].text)


# ── HTML ヘルパー ─────────────────────────────────────────────────────────────
def e(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


BADGE_COLORS = {
    "RED":  {"bg": "#fee2e2", "border": "#ef4444", "text": "#991b1b"},
    "ORG":  {"bg": "#fff7ed", "border": "#f97316", "text": "#9a3412"},
    "CYAN": {"bg": "#ecfeff", "border": "#06b6d4", "text": "#155e75"},
    "YEL":  {"bg": "#fefce8", "border": "#eab308", "text": "#854d0e"},
    "GRN":  {"bg": "#f0fdf4", "border": "#22c55e", "text": "#166534"},
    "PRP":  {"bg": "#faf5ff", "border": "#a855f7", "text": "#6b21a8"},
}


def render_segment(seg: dict, orig: dict, idx: int) -> str:
    color = orig.get("color", "RED")
    c = BADGE_COLORS.get(color, BADGE_COLORS["RED"])
    search_en = orig.get("search_en", seg["title"])

    bullets_html = ""
    for i, bullet in enumerate(seg["bullets"]):
        url = orig["bullets"][i]["url"] if i < len(orig["bullets"]) else "#"
        src = orig["bullets"][i].get("source", "")
        bullets_html += (
            f'<li><a href="{e(url)}" target="_blank" rel="noopener">'
            f'{e(bullet)}</a>'
            f'<span class="src-tag">{e(src)}</span></li>\n'
        )

    risk_text    = seg.get("risk", "").replace("▲Risk:", "").strip()
    context_text = seg.get("context", "").replace("Background:", "").strip()

    google_news_url = f"https://news.google.com/search?q={search_en.replace(' ', '+')}&hl=en"

    return f"""<article class="news-card" style="border-left:4px solid {c['border']}; background:{c['bg']};">
  <div class="card-header">
    <span class="badge" style="background:{c['border']};color:#fff;">{e(seg['badge'])}</span>
    <a href="{google_news_url}" target="_blank" rel="noopener" class="card-title">{e(seg['title'])}</a>
  </div>
  <p class="card-sub">{e(seg['subtitle'])}</p>
  <ul class="bullet-list">{bullets_html}</ul>
  <details class="card-details">
    <summary>▲ Risk / Background</summary>
    <p class="risk-text"><strong>Risk:</strong> {e(risk_text)}</p>
    <p class="ctx-text"><strong>Background:</strong> {e(context_text)}</p>
  </details>
</article>"""


def render_economist(eco: dict, top_en: list, day_en: list) -> str:
    subject = eco.get("subject", "The Economist")
    generated = eco.get("generated_at", "")
    cover = "../data/economist_cover.jpg"

    top_items = "\n".join(f"<li>{e(b)}</li>" for b in top_en)
    day_items = "\n".join(f"<li>{e(b)}</li>" for b in day_en)

    return f"""<aside class="eco-sidebar">
  <div class="eco-head">
    <img src="{cover}" alt="Economist cover" class="eco-cover">
    <div>
      <div class="eco-label">THE ECONOMIST</div>
      <div class="eco-sub">{e(subject)}</div>
      <div class="eco-date">{e(generated)}</div>
    </div>
  </div>
  <section class="eco-section">
    <h3 class="eco-sec-title">Today's Top Stories</h3>
    <ul class="eco-list">{top_items}</ul>
  </section>
  <section class="eco-section">
    <h3 class="eco-sec-title">The Day Ahead</h3>
    <ul class="eco-list">{day_items}</ul>
  </section>
</aside>"""


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif; background: #f4f5f7; color: #1a1a2e; font-size: 14px; line-height: 1.65; }

/* ── Site Header ── */
.site-header { background: #1a1a2e; color: #fff; padding: 0 24px; height: 58px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 300; box-shadow: 0 2px 8px rgba(0,0,0,.25); }
.logo { font-size: 20px; font-weight: 700; letter-spacing: .5px; white-space: nowrap; cursor: pointer; }
.logo em { color: #5bc8f5; font-style: normal; }
.header-date { font-size: 12px; color: rgba(255,255,255,.5); white-space: nowrap; }
.header-spacer { flex: 1; }
.live-badge { background: #e63946; color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }
.update-time { font-size: 11px; color: rgba(255,255,255,.4); white-space: nowrap; }
.lang-toggle { display: flex; gap: 6px; font-size: 12px; }
.lang-toggle a { color: rgba(255,255,255,.6); text-decoration: none; padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,.3); transition: all .15s; font-weight: 600; }
.lang-toggle a.active { color: #fff; background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.7); }
.lang-toggle a:hover { color: #fff; background: rgba(255,255,255,.12); }

/* ── Page Navigation Tabs ── */
.page-nav { background: #fff; border-bottom: 1px solid #e5e7eb; padding: 0 24px; display: flex; align-items: stretch; position: sticky; top: 58px; z-index: 200; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.page-nav a { display: flex; align-items: center; gap: 6px; padding: 0 18px; height: 44px; font-size: 14px; font-weight: 500; color: #6b7280; text-decoration: none; border-bottom: 3px solid transparent; white-space: nowrap; transition: color .15s, border-color .15s; }
.page-nav a:hover { color: #1a1a2e; }
.page-nav a.active { color: #1a1a2e; border-bottom-color: #1a1a2e; font-weight: 700; }
.page-nav a .nav-icon { font-size: 15px; }
.page-nav a.dim { opacity: .45; pointer-events: none; }

/* ── Layout ── */
.page-wrap { max-width: 1200px; margin: 24px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 300px; gap: 24px; align-items: start; }
@media (max-width: 860px) { .page-wrap { grid-template-columns: 1fr; } .eco-sidebar { order: -1; position: static; max-height: none; overflow-y: visible; } }

/* ── News cards ── */
.news-grid { display: flex; flex-direction: column; gap: 16px; }
.news-card  { background: #fff; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 4px rgba(0,0,0,.07); }
.card-header { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 6px; }
.badge { font-size: 10px; font-weight: 700; padding: 3px 7px; border-radius: 4px; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }
.card-title { font-size: 15px; font-weight: 700; color: #1a1a2e; text-decoration: none; line-height: 1.4; }
.card-title:hover { text-decoration: underline; color: #0096c8; }
.card-sub { font-size: 12px; color: #6b7280; margin-bottom: 10px; }
.bullet-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 6px; }
.bullet-list li { font-size: 13px; line-height: 1.55; padding-left: 12px; border-left: 2px solid #e5e7eb; color: #2a2a3e; }
.bullet-list li a { color: inherit; text-decoration: none; }
.bullet-list li a:hover { color: #0096c8; text-decoration: underline; }
.src-tag { display: inline-block; font-size: 10px; font-weight: 600; color: #9ca3af; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 4px; padding: 1px 5px; margin-left: 6px; vertical-align: middle; white-space: nowrap; }
.card-details { margin-top: 12px; border-top: 1px solid #f3f4f6; padding-top: 8px; }
.card-details summary { font-size: 11px; color: #9ca3af; cursor: pointer; user-select: none; }
.card-details[open] summary { color: #6b7280; }
.risk-text, .ctx-text { font-size: 11.5px; color: #4b5563; line-height: 1.65; margin-top: 8px; }

/* ── Economist sidebar ── */
.eco-sidebar { position: sticky; top: 112px; max-height: calc(100vh - 130px); overflow-y: auto; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 6px rgba(0,0,0,.07); }
.eco-sidebar::-webkit-scrollbar { width: 4px; } .eco-sidebar::-webkit-scrollbar-thumb { background: rgba(0,0,0,.15); border-radius: 2px; }
.eco-head { display: flex; gap: 12px; padding: 14px 16px; background: #f9fafb; border-bottom: 1px solid #e5e7eb; align-items: flex-start; }
.eco-cover { width: 60px; height: 80px; object-fit: cover; border-radius: 3px; flex-shrink: 0; }
.eco-label { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: #e63c2f; margin-bottom: 4px; }
.eco-sub   { font-size: 11px; font-weight: 600; color: #1a1a2e; line-height: 1.4; }
.eco-date  { font-size: 10px; color: #9ca3af; margin-top: 4px; }
.eco-section { padding: 12px 16px; border-bottom: 1px solid #f3f4f6; }
.eco-section:last-child { border-bottom: none; }
.eco-sec-title { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin-bottom: 8px; }
.eco-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.eco-list li { font-size: 11.5px; line-height: 1.65; color: #2a2a3e; padding-left: 10px; border-left: 2px solid #e63c2f; }

/* ── Footer ── */
.site-footer { text-align: center; padding: 28px 20px; font-size: 11px; color: #9ca3af; margin-top: 32px; border-top: 1px solid #e5e7eb; }

@media (max-width: 640px) { .site-header { padding: 0 14px; } .update-time { display: none; } .page-nav { padding: 0 8px; } .page-nav a { padding: 0 12px; font-size: 13px; } }
"""


NAV_PAGES = [
    ("index.html",        "🏠", "Home",          "home",          False),
    ("intelligence.html", "📋", "Intelligence",  "intelligence",  True),
    ("trump.html",        "🇺🇸", "US / Trump",   "trump",         True),
    ("theme.html",        "🔎", "Themes",         "theme",         True),
    ("midterm.html",      "🗳️", "US Midterms",   "midterm",       True),
    ("summary.html",      "📋", "Exec Summary",  "summary",       True),
]


def build_html(segments_en: list, segments_orig: list, eco: dict,
               top_en: list, day_en: list, generated_at: str) -> str:
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")

    cards = "\n".join(
        render_segment(seg_en, seg_orig, i)
        for i, (seg_en, seg_orig) in enumerate(zip(segments_en, segments_orig))
    )
    eco_html = render_economist(eco, top_en, day_en)

    nav_tabs = ""
    for href, icon, label, pid, coming in NAV_PAGES:
        cls_parts = []
        if pid == "home":
            cls_parts.append("active")
        if coming:
            cls_parts.append("dim")
        cls = f' class="{" ".join(cls_parts)}"' if cls_parts else ""
        nav_tabs += f'  <a href="{href}"{cls}><span class="nav-icon">{icon}</span>{label}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>World Intelligence Monitor</title>
<style>{CSS}</style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'">World<em>News</em></div>
  <div class="header-date">{today}</div>
  <div class="header-spacer"></div>
  <div class="update-time">Updated: {e(generated_at)}</div>
  <div class="lang-toggle">
    <a href="../index.html">JP</a>
    <a href="index.html" class="active">EN</a>
  </div>
  <div class="live-badge">LIVE</div>
</header>
<nav class="page-nav">
{nav_tabs}</nav>
<div class="page-wrap">
  <main class="news-grid">
    {cards}
  </main>
  {eco_html}
</div>
<footer class="site-footer">
  World Intelligence Monitor &mdash; For internal use only &mdash; Updated: {e(generated_at)}
</footer>
</body>
</html>"""


# ── メイン ───────────────────────────────────────────────────────────────────
def main():
    if not CLAUDE_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY が設定されていません。")
        sys.exit(1)

    print("データ読み込み中...")
    home = json.loads(HOME_JSON.read_text(encoding="utf-8"))
    eco  = json.loads(ECONOMIST_JSON.read_text(encoding="utf-8"))
    segments_orig = home["segments"]
    generated_at  = home.get("generated_at", "")

    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    print("ニュース記事を英訳中 (Claude Haiku)...")
    segments_en = translate_home(segments_orig, client)
    print(f"  → {len(segments_en)} セグメント翻訳完了")

    print("Economist Today's Top Stories を英語化中...")
    top_en = translate_economist(eco["top_bullets"], "Today's Top Stories", client)
    print(f"  → {len(top_en)} 件")

    print("Economist The Day Ahead を英語化中...")
    day_en = translate_economist(eco["day_bullets"], "The Day Ahead", client)
    print(f"  → {len(day_en)} 件")

    print("HTML 生成中...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html(segments_en, segments_orig, eco, top_en, day_en, generated_at)
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] {OUT_HTML}")


if __name__ == "__main__":
    main()
