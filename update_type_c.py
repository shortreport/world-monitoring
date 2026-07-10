#!/usr/bin/env python3
"""
update_type_c.py
================
Type C (docs/jp/) の全ページを更新するスクリプト。
Type A (docs/) を一切参照しない。
ソースデータ (docs/data/*.json, db/) と Type B (docs/en/) から生成。

対象ページ:
  1. trump.html   - trump_en_latest.json → JP翻訳
  2. theme.html   - theme_latest.json (JP済み)
  3. index.html   - home_latest.json + economist_latest.json (JP済み)
  4. intelligence.html - mail_rolling.json (summary_ja)
  5. summary.html - アーカイブリスト更新
"""

import io, json, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import html as _html

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import anthropic

try:
    from api_config import ANTHROPIC_API_KEY
    os.environ.setdefault("ANTHROPIC_API_KEY", ANTHROPIC_API_KEY)
except ImportError:
    pass

BASE     = Path(__file__).parent
JP_DIR   = BASE / "docs" / "jp"
DATA_DIR = BASE / "docs" / "data"
DB_DIR   = BASE / "db"
JST      = timezone(timedelta(hours=9))

MODEL    = "claude-haiku-4-5-20251001"
client   = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY",""))

now_jst  = datetime.now(JST)
DATE_JP  = now_jst.strftime("%Y年%m月%d日")
DATETIME_JP = now_jst.strftime("%Y年%m月%d日 %H:%M JST")


def e(s): return _html.escape(str(s))


def get_shell(path: Path) -> tuple[str, str]:
    """既存 Type C HTML から <head>+<body>ヘッダー+ナビ部分と閉じタグを返す"""
    html = path.read_text(encoding="utf-8")
    # </nav> の位置で分割
    nav_end = html.find("</nav>")
    if nav_end == -1:
        raise ValueError(f"</nav> not found in {path}")
    shell_top = html[:nav_end + len("</nav>")]
    # 最後の </body></html>
    shell_bot = "\n</body></html>"
    return shell_top, shell_bot


def update_header_date(shell: str) -> str:
    """シェル内のヘッダー日付・更新時刻を今日に更新"""
    shell = re.sub(r'(<div class="header-date">)[^<]*(</div>)',
                   rf'\g<1>{DATE_JP}\2', shell)
    shell = re.sub(r'(最終更新:)[^<]*(</div>)',
                   rf'\g<1> {DATETIME_JP}\2', shell)
    return shell


# ─────────────────────────────────────────────────────────────
#  1. TRUMP
# ─────────────────────────────────────────────────────────────

def update_trump():
    print("\n=== [1/5] Trump ===")
    json_path = DB_DIR / "north america" / "trump_en_latest.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))
    date_range  = data.get("date_range", "")
    item_count  = data.get("item_count", 0)

    SECTIONS = [
        ("sns",                "📱", "SNS",          "Truth Social ポスト",          "#3C3B6E", ""),
        ("press_conference",   "🎤", "記者会見",      "記者会見・メディア",             "#C81E32", ""),
        ("whitehouse_official","📜", "大統領令",      "大統領令・ホワイトハウス発表",    "#B48200", ""),
        ("wh_briefing",        "🎙", "WH会見",        "報道官ブリーフィング",            "#3C3B6E", ""),
        ("video",              "🎬", "動画",          "YouTube・ホワイトハウス動画",     "#C81E32", ""),
        ("cabinet",            "👥", "閣僚の動き",    "閣僚の主な動き",                 "#B48200", ""),
        ("japan_impact",       "🇯🇵","日本への影響",  "日本への影響",                   "#C81E32", "japan-highlight"),
    ]

    def translate_list(texts: list) -> list:
        if not texts: return []
        prompt = ("以下の英文リストを自然な日本語に翻訳してください。"
                  "箇条書き形式を維持し、JSONリスト（文字列のリスト）で返してください。\n"
                  + json.dumps(texts, ensure_ascii=False))
        resp = client.messages.create(model=MODEL, max_tokens=2048,
            messages=[{"role": "user", "content": prompt}])
        raw = resp.content[0].text.strip()
        m = re.search(r'\[.*?\]', raw, re.DOTALL)
        if m:
            try:
                result = json.loads(m.group())
                if len(result) == len(texts):
                    return result
            except Exception:
                pass
        return texts

    def build_li(bullets: list, texts_jp: list) -> str:
        li = ""
        for b, txt in zip(bullets, texts_jp):
            url = b.get("url", "") if isinstance(b, dict) else ""
            src = b.get("source", "") if isinstance(b, dict) else ""
            src_tag = f'<span class="src-tag">{e(src)} ↗</span>' if src else ""
            if url:
                li += (f'<li class="has-link"><a href="{e(url)}" target="_blank"'
                       f' rel="noopener noreferrer" class="bullet-link">'
                       f'{e(txt)}{src_tag}</a></li>\n')
            else:
                li += f'<li>{e(txt)}</li>\n'
        return li

    # key_points
    print("  key_points 翻訳中...")
    kp_items = data.get("key_points", [])
    kp_texts = [b["text"] if isinstance(b, dict) else str(b) for b in kp_items]
    kp_jp    = translate_list(kp_texts)
    kp_li    = build_li(kp_items, kp_jp)

    # グリッドカード
    active_count = sum(1 for key, *_ in SECTIONS if data.get(key))
    grid_html = ""
    for key, icon, badge, title_jp, color, extra_class in SECTIONS:
        bullets = data.get(key, [])
        print(f"  セクション: {badge} ({len(bullets)} items)")
        if not bullets:
            li_html = '<li class="no-data">この期間のデータはありません。</li>'
        else:
            texts   = [b["text"] if isinstance(b, dict) else str(b) for b in bullets]
            jp      = translate_list(texts)
            li_html = build_li(bullets, jp)
        card_class = f"trump-card {extra_class}".strip()
        grid_html += f"""
    <div class="{card_class}" style="border-left-color:{color};">
      <div class="trump-card-header">
        <span class="trump-icon">{icon}</span>
        <span class="trump-badge" style="background:{color};">{e(badge)}</span>
        <span class="trump-card-title">{e(title_jp)}</span>
      </div>
      <ul class="trump-bullets">
        {li_html}
      </ul>
    </div>
"""

    content = f"""
<div class="trump-wrap">
  <div class="trump-banner">
    <div>
      <div class="trump-banner-title">TRUMP <span>MONITOR</span></div>
      <div class="trump-banner-sub">対象期間: {e(date_range)}</div>
    </div>
    <div class="trump-banner-spacer"></div>
    <div class="trump-stats">
      <div class="trump-stat"><div class="trump-stat-num">{item_count}</div><div class="trump-stat-lbl">Items</div></div>
      <div class="trump-stat"><div class="trump-stat-num">{active_count}</div><div class="trump-stat-lbl">Sections</div></div>
    </div>
  </div>
  <p class="section-label">Key Points</p>
  <div class="trump-card featured" style="border-left-color:#B48200;">
    <div class="trump-card-header">
      <span class="trump-icon">⭐</span>
      <span class="trump-badge" style="background:#B48200;">今日のポイント</span>
      <span class="trump-card-title">本日のハイライト</span>
    </div>
    <ul class="trump-bullets">
      {kp_li}
    </ul>
  </div>
  <p class="section-label">詳細分析</p>
  <div class="trump-grid">
    {grid_html}
  </div>
</div>
"""
    path = JP_DIR / "trump.html"
    shell_top, shell_bot = get_shell(path)
    shell_top = update_header_date(shell_top)
    path.write_text(shell_top + "\n" + content + shell_bot, encoding="utf-8")
    print(f"  保存: {path}")


# ─────────────────────────────────────────────────────────────
#  2. THEME
# ─────────────────────────────────────────────────────────────

def update_theme():
    print("\n=== [2/5] Theme ===")
    data = json.loads((DATA_DIR / "theme_latest.json").read_text(encoding="utf-8"))
    themes = data.get("themes", [])

    cards_html = ""
    for th in themes:
        name = th.get("name", "")
        desc = th.get("description", "")
        color = th.get("color", "#555")
        icon  = th.get("icon", "")
        items = th.get("items", [])
        items_html = ""
        for it in items[:5]:
            title = it.get("title","")
            summary = it.get("summary","")
            date = it.get("date","")
            url = it.get("url","")
            link = f'href="{e(url)}" target="_blank"' if url else ""
            items_html += f"""
      <div class="theme-item">
        <a class="theme-item-title" {link}>{e(title)}</a>
        <div class="theme-summary">{e(summary)}</div>
        <div class="theme-item-date">{e(date)}</div>
      </div>"""
        cards_html += f"""
  <div class="theme-card" style="border-top:3px solid {color}">
    <div class="theme-header">
      <span class="theme-icon">{icon}</span>
      <h2 class="theme-name">{e(name)}</h2>
    </div>
    <div class="theme-desc">{e(desc)}</div>
    <div class="theme-items">{items_html}</div>
  </div>"""

    content = f'<div class="theme-wrap"><div class="theme-grid">{cards_html}</div></div>\n'

    path = JP_DIR / "theme.html"
    shell_top, shell_bot = get_shell(path)
    shell_top = update_header_date(shell_top)
    path.write_text(shell_top + "\n" + content + shell_bot, encoding="utf-8")
    print(f"  保存: {path}")


# ─────────────────────────────────────────────────────────────
#  3. HOME
# ─────────────────────────────────────────────────────────────

def update_home():
    print("\n=== [3/5] Home ===")
    home = json.loads((DATA_DIR / "home_latest.json").read_text(encoding="utf-8"))
    eco  = json.loads((DATA_DIR / "economist_latest.json").read_text(encoding="utf-8"))

    COLORS = {
        "RED":  {"border": "#e63946", "bg": "#fee2e2"},
        "ORG":  {"border": "#f77f00", "bg": "#fff7ed"},
        "YEL":  {"border": "#f4c430", "bg": "#fefce8"},
        "GRN":  {"border": "#2a9d8f", "bg": "#f0fdf4"},
        "CYN":  {"border": "#0096c8", "bg": "#ecfeff"},
        "BLU":  {"border": "#3a86ff", "bg": "#eff6ff"},
        "PRP":  {"border": "#7b2d8b", "bg": "#faf5ff"},
        "GRY":  {"border": "#6b7280", "bg": "#f9fafb"},
    }

    cards_html = ""
    for seg in home.get("segments", []):
        c = COLORS.get(seg.get("color","GRY"), COLORS["GRY"])
        color = c["border"]
        bg_color = c["bg"]
        badge = seg.get("badge","")
        title = seg.get("title","")
        subtitle = seg.get("subtitle","")
        bullets = seg.get("bullets", [])
        risk = seg.get("risk","")
        ctx  = seg.get("context","").replace("背景：","")

        li_html = ""
        for b in bullets:
            if isinstance(b, dict):
                text = b.get("text","")
                src  = b.get("source","")
                url  = b.get("url","")
                link_s = f'<a href="{e(url)}" target="_blank">' if url else ""
                link_e = "</a>" if url else ""
                src_tag = f'<span class="src-tag">{e(src)}</span>' if src else ""
                li_html += f'<li>{link_s}{e(text)}{link_e}{src_tag}</li>'
            else:
                li_html += f'<li>{e(str(b))}</li>'

        details_html = ""
        if risk or ctx:
            risk_p = f'<p class="risk-text"><strong>リスク:</strong> {e(risk)}</p>' if risk else ""
            ctx_p  = f'<p class="ctx-text"><strong>背景:</strong> {e(ctx)}</p>' if ctx else ""
            details_html = f'<details class="card-details"><summary>▲ リスク・背景</summary>{risk_p}{ctx_p}</details>'

        cards_html += f"""
  <article class="news-card" style="border-left:4px solid {color}; background:{bg_color};">
    <div class="card-header">
      <span class="badge" style="background:{color};color:#fff">{e(badge)}</span>
      <span class="card-title">{e(title)}</span>
    </div>
    <p class="card-sub">{e(subtitle)}</p>
    <ul class="bullet-list">{li_html}</ul>
    {details_html}
  </article>"""

    # Economist サイドバー
    top_b = "".join(f"<li>{e(b)}</li>" for b in eco.get("top_bullets",[]))
    day_b = "".join(f"<li>{e(b)}</li>" for b in eco.get("day_bullets",[]))
    eco_subject = eco.get("subject","")
    cover_img = eco.get("cover_local","economist_cover.jpg")

    eco_html = f"""
  <aside class="eco-sidebar">
    <div class="eco-header">
      <span class="eco-logo-text">The Economist</span>
      <span class="eco-hdate">{DATE_JP}</span>
    </div>
    <div class="eco-cover-wrap">
      <img src="../data/{cover_img}" alt="The Economist cover">
    </div>
    <div class="eco-sub">{e(eco_subject)}</div>
    <div class="eco-section">
      <div class="eco-sec-title">Today's Top Stories</div>
      <ul class="eco-list">{top_b}</ul>
    </div>
    <div class="eco-section">
      <div class="eco-sec-title">The Day Ahead</div>
      <ul class="eco-list">{day_b}</ul>
    </div>
  </aside>"""

    content = f"""
<div class="page-wrap">
  <div class="news-grid">{cards_html}</div>
  {eco_html}
</div>
"""
    path = JP_DIR / "index.html"
    shell_top, shell_bot = get_shell(path)
    shell_top = update_header_date(shell_top)
    path.write_text(shell_top + "\n" + content + shell_bot, encoding="utf-8")
    print(f"  保存: {path}")


# ─────────────────────────────────────────────────────────────
#  4. INTELLIGENCE
# ─────────────────────────────────────────────────────────────

def _load_en_intel_title_map() -> dict:
    """Bタイプのintelligence HTMLからタイムスタンプ→フルタイトルのマッピングを取得"""
    import html as html_lib
    en_path = BASE / "docs" / "en" / "intelligence.html"
    if not en_path.exists():
        return {}
    content = en_path.read_text(encoding="utf-8")
    title_map = {}
    pattern = re.compile(
        r"openFile\('[^']*/(\d{8}_\d{4}_[^']+)\.[a-z]+'[^>]*>.*?<div class=\"v2-title\">(.*?)</div>",
        re.DOTALL
    )
    for m in pattern.finditer(content):
        ts = m.group(1)[:13]  # "20260710_1023"
        title = html_lib.unescape(m.group(2))
        title_map[ts] = title
    return title_map


def update_intelligence():
    print("\n=== [4/5] Intelligence ===")
    rolling = json.loads((DATA_DIR / "mail_rolling.json").read_text(encoding="utf-8"))
    emails  = rolling.get("emails", [])

    # Bタイプのフルタイトルマップ（YYYYMMDD_HHMM → full title）
    en_title_map = _load_en_intel_title_map()
    print(f"  Bタイプタイトル取得: {len(en_title_map)}件")

    # サイドバー要約（summary_ja が空でないもの）
    toyota_emails = [em for em in emails if em.get("toyota") and em.get("summary_ja")]

    # サイドバー生成
    if toyota_emails:
        sidebar_summary = "".join(
            f'<p>{e(em.get("summary_ja",""))}</p>' for em in toyota_emails[:3]
        )
        src_links = "".join(f"""
    <div class="v2-src" onclick="openPdfDirect('../{e(em.get('pdf',''))}','{e(em.get('subject',''))}')">
      <span class="v2-badge" style="background:#007838">JET</span>
      {e(em.get('subject','')[:60])}
    </div>""" for em in toyota_emails)
    else:
        sidebar_summary = "<p>本日の自動車関連メールはありません。</p>"
        src_links = ""

    sidebar_html = f"""
<div class="v2-sidebar">
  <div class="v2-sb-head">
    <div class="v2-sb-ttl">🚗 自動車産業サマリー</div>
    <div class="v2-sb-sub">最終更新: {DATETIME_JP}</div>
  </div>
  <div class="v2-sb-body">
    <div class="v2-summary-block">{sidebar_summary}</div>
    <hr class="v2-hr">
    <div class="v2-src-lbl">ソース</div>
    {src_links}
  </div>
</div>"""

    # カード生成
    SENDER_CODE = {
        "Eurasia Group": ("EG", "#8a6200"),
        "POLITICO":      ("POL", "#a8121e"),
        "Jetro":         ("JET", "#007838"),
    }

    cards_html = ""
    for em in emails:
        sender = em.get("sender_norm","")
        code, _ = SENDER_CODE.get(sender, ("OTH", "#444488"))
        subject = em.get("subject","")
        subject_en = em.get("subject_en","")
        pdf        = em.get("pdf","")
        date_label = em.get("date_label","")
        read_min   = em.get("read_min","?")
        toyota     = em.get("toyota", False)
        summary_pdf = em.get("summary_pdf","")

        # JETROは subject_en（英訳件名）、それ以外はBタイプのフルタイトル優先
        if code == "JET" and subject_en:
            display_title = subject_en
        else:
            ts = pdf.split("/")[-1][:13]  # "20260710_1023"
            display_title = en_title_map.get(ts, subject)

        dot = '<span class="v2-dot">🚗</span>' if toyota else ""

        pdf_btn = ""
        if summary_pdf:
            pdf_btn = f' &nbsp;<button class="v2-pdf-btn" onclick="event.stopPropagation();openPdfDirect(\'../{e(summary_pdf)}\',\'{e(subject[:40])} — 要約\')">📄 要約</button>'

        cards_html += f"""
  <div class="v2-card" data-s="{code}" data-pdf="../{e(pdf)}" data-title="{e(display_title)}" onclick="openPdf(this)">
    {dot}
    <div class="v2-sender">{e(sender)}</div>
    <div class="v2-title">{e(display_title)}</div>
    <div class="v2-meta">{e(date_label)} &nbsp;·&nbsp; {e(str(read_min))} MIN{pdf_btn}</div>
  </div>"""

    upd_time = rolling.get("generated_at", DATETIME_JP)

    content = f"""
<div class="v2-wrap">
  <div class="v2-left">
    <div class="v2-grid">
      {cards_html}
    </div>
  </div>
  {sidebar_html}
</div>

<div class="v2-modal" id="pdfModal" onclick="if(event.target===this)this.style.display='none'">
  <div class="v2-modal-box">
    <div class="v2-mh">
      <span class="v2-mt" id="modalTitle">-</span>
      <button class="v2-mc" onclick="document.getElementById('pdfModal').style.display='none'">✕ 閉じる</button>
    </div>
    <iframe class="v2-mf" id="modalFrame" src=""></iframe>
  </div>
</div>
<script>
function openPdf(card){{
  var pdf=card.dataset.pdf, title=card.dataset.title;
  document.getElementById('modalTitle').textContent=title;
  document.getElementById('modalFrame').src=pdf;
  document.getElementById('pdfModal').style.display='flex';
}}
function openPdfDirect(url,title){{
  document.getElementById('modalTitle').textContent=title;
  document.getElementById('modalFrame').src=url;
  document.getElementById('pdfModal').style.display='flex';
}}
</script>
"""
    path = JP_DIR / "intelligence.html"
    shell_top, shell_bot = get_shell(path)
    shell_top = update_header_date(shell_top)
    path.write_text(shell_top + "\n" + content + shell_bot, encoding="utf-8")
    print(f"  保存: {path}")


# ─────────────────────────────────────────────────────────────
#  5. SUMMARY
# ─────────────────────────────────────────────────────────────

def update_summary():
    print("\n=== [5/5] Summary ===")
    path = JP_DIR / "summary.html"
    html = path.read_text(encoding="utf-8")

    today = now_jst.strftime("%Y-%m-%d")
    pdf_path = f"../data/briefings/briefing_{today.replace('-','')}.pdf"

    # アーカイブリストに今日分が既にあるか確認
    if today in html:
        print(f"  {today} は既にアーカイブ済み")
    else:
        # アーカイブリストの先頭に追加
        new_entry = f'<li class="arch-item"><a class="arch-link" href="{pdf_path}" target="_blank">📄 {today} ブリーフィング</a></li>'
        html = re.sub(r'(<ul[^>]*class="[^"]*arch[^"]*"[^>]*>)', r'\1\n    ' + new_entry, html, count=1)
        print(f"  {today} をアーカイブに追加")

    # iframeのsrcを今日のPDFに更新
    html = re.sub(r'(<iframe[^>]*src=")[^"]*(")',
                  rf'\g<1>{pdf_path}\2', html, count=1)

    # 最終更新時刻更新
    html = re.sub(r'(最終更新:)[^<]*(</div>)',
                  rf'\g<1> {DATETIME_JP}\2', html)
    html = re.sub(r'(<div class="header-date">)[^<]*(</div>)',
                  rf'\g<1>{DATE_JP}\2', html)

    path.write_text(html, encoding="utf-8")
    print(f"  保存: {path}")


# ─────────────────────────────────────────────────────────────
#  メイン
# ─────────────────────────────────────────────────────────────

def main():
    print(f"Type C 更新開始: {DATETIME_JP}")
    update_trump()
    update_theme()
    update_home()
    update_intelligence()
    update_summary()

    print("\n=== git commit & push ===")
    cmds = [
        ["git", "add", "docs/jp/"],
        ["git", "commit", "-m", f"Update Type C: {now_jst.strftime('%Y-%m-%d %H:%M JST')}"],
        ["git", "push", "origin", "main"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, cwd=str(BASE), capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  [OK] {' '.join(cmd[:2])}")
        else:
            print(f"  [ERR] {' '.join(cmd[:2])}: {r.stderr.strip()[:100]}")

    print(f"\n完了: {datetime.now(JST).strftime('%H:%M JST')}")

if __name__ == "__main__":
    main()
