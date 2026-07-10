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
    date_range = data.get("date_range", "")

    # EN → JP 翻訳（key_points + セクション bullets）
    def translate_bullets(bullets: list) -> list:
        if not bullets: return []
        texts = [b["text"] if isinstance(b, dict) else str(b) for b in bullets]
        prompt = "以下の英文を自然な日本語に翻訳してください。箇条書き形式を維持し、JSONリストで返してください。\n" + json.dumps(texts, ensure_ascii=False)
        resp = client.messages.create(model=MODEL, max_tokens=2048,
            messages=[{"role":"user","content":prompt}])
        raw = resp.content[0].text.strip()
        m = re.search(r'\[.*?\]', raw, re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
        return texts

    print("  key_points 翻訳中...")
    kp_en = [b["text"] if isinstance(b,dict) else str(b) for b in data.get("key_points",[])]
    kp_jp = translate_bullets(data.get("key_points",[]))

    def render_section(sec: dict) -> str:
        title_en = sec.get("title","")
        bullets_en = sec.get("bullets",[])
        if not bullets_en: return ""
        # タイトル翻訳
        resp = client.messages.create(model=MODEL, max_tokens=200,
            messages=[{"role":"user","content":f"次の英語タイトルを自然な日本語に翻訳（短く）: {title_en}"}])
        title_jp = resp.content[0].text.strip()
        bullets_jp = translate_bullets(bullets_en)
        li_html = "".join(f'<li class="trump-bullet">{e(b)}</li>' for b in bullets_jp)
        return f"""
    <div class="trump-section">
      <h3 class="trump-section-title">{e(title_jp)}</h3>
      <ul class="trump-bullets">{li_html}</ul>
    </div>"""

    sections_html = ""
    for sec in data.get("sections", []):
        print(f"  セクション翻訳中: {sec.get('title','')[:40]}")
        sections_html += render_section(sec)

    kp_html = "".join(f'<li class="trump-bullet featured">{e(b)}</li>' for b in kp_jp)

    content = f"""
<div class="trump-wrap">
  <div class="trump-banner">
    <div>
      <div class="trump-banner-title">TRUMP <span>MONITOR</span></div>
      <div class="trump-banner-sub">対象期間: {e(date_range)}</div>
    </div>
  </div>
  <div class="trump-section">
    <h3 class="trump-section-title">🔑 今日のポイント</h3>
    <ul class="trump-bullets featured-list">{kp_html}</ul>
  </div>
  {sections_html}
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
        "RED":  "#e63946", "ORG": "#f77f00", "YEL": "#f4c430",
        "GRN":  "#2a9d8f", "CYN": "#0096c8", "BLU": "#3a86ff",
        "PRP":  "#7b2d8b", "GRY": "#6b7280",
    }

    cards_html = ""
    for seg in home.get("segments", []):
        color = COLORS.get(seg.get("color","GRY"), "#6b7280")
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

        risk_html = f'<div class="card-risk">リスク: {e(risk)}</div>' if risk else ""
        ctx_html  = f'<div class="card-context">{e(ctx)}</div>' if ctx else ""

        cards_html += f"""
  <div class="news-card">
    <div class="card-header">
      <span class="badge" style="background:{color};color:#fff">{e(badge)}</span>
      <span class="card-title">{e(title)}</span>
    </div>
    <div class="card-sub">{e(subtitle)}</div>
    <ul class="bullet-list">{li_html}</ul>
    {risk_html}{ctx_html}
  </div>"""

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

def update_intelligence():
    print("\n=== [4/5] Intelligence ===")
    rolling = json.loads((DATA_DIR / "mail_rolling.json").read_text(encoding="utf-8"))
    emails  = rolling.get("emails", [])

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
        # JETROは subject_en（英訳件名）、それ以外はオリジナル件名
        display_title = subject_en if (code == "JET" and subject_en) else subject
        date_label = em.get("date_label","")
        read_min   = em.get("read_min","?")
        pdf        = em.get("pdf","")
        toyota     = em.get("toyota", False)
        summary_ja = em.get("summary_ja","")
        summary_pdf = em.get("summary_pdf","")

        dot = '<span class="v2-dot">🚗</span>' if toyota else ""
        excerpt_html = f'<div class="v2-excerpt">{e(summary_ja)}</div>' if summary_ja else ""

        pdf_btn = ""
        if summary_pdf:
            pdf_btn = f' &nbsp;<button class="v2-pdf-btn" onclick="event.stopPropagation();openPdfDirect(\'../{e(summary_pdf)}\',\'{e(display_title[:40])} — 要約\')">📄 要約</button>'

        cards_html += f"""
  <div class="v2-card" data-s="{code}" data-pdf="../{e(pdf)}" data-title="{e(display_title)}" onclick="openPdf(this)">
    {dot}
    <div class="v2-sender">{e(sender)}</div>
    <div class="v2-title">{e(display_title)}</div>
    {excerpt_html}
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
