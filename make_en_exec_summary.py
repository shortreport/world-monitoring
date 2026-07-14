"""
make_en_exec_summary.py
-----------------------
毎朝 Home / Intelligence / US-Trump / Themes / Midterms の英語ソースから
4セクション形式の Executive Briefing を生成するスクリプト。

フロー:
  1. 英語ソースデータ (JSON + HTML) を読み込む
  2. Claude で英語 Exec Summary (4セクション) を生成
  3. docs/en/summary.html を上書き保存
  4. 4セクションを日本語に翻訳
  5. reportlab で docs/briefing_latest.pdf を更新
  6. docs/data/briefings/ にアーカイブコピー
  7. docs/summary.html のアーカイブリストを先頭追加
  8. git add / commit / push + GitHub Actions トリガー
"""

import os, re, sys, io, json, html as _html, shutil, subprocess, urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ── Windows レジストリから API キーを自動ロード ───────────────────────────
if not os.environ.get("ANTHROPIC_API_KEY"):
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as _k:
            _v, _ = winreg.QueryValueEx(_k, "ANTHROPIC_API_KEY")
            if _v: os.environ["ANTHROPIC_API_KEY"] = _v
    except Exception:
        pass

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import anthropic
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT

# ── Config ────────────────────────────────────────────────────────────────────
BASE          = Path(__file__).parent
DATA_DIR      = BASE / "docs" / "data"
BRIEFINGS_DIR = DATA_DIR / "briefings"
EN_SUMMARY    = BASE / "docs" / "en" / "summary.html"
JP_C_SUMMARY  = BASE / "docs" / "jp" / "summary.html"
PDF_LATEST    = BASE / "docs" / "briefing_latest.pdf"
MODEL         = "claude-haiku-4-5-20251001"
GH_TOKEN      = os.environ.get("GH_TOKEN", "")
JST           = timezone(timedelta(hours=9))

FONT_PATH     = r"C:\Windows\Fonts\YuGothM.ttc"
FONT_B_PATH   = r"C:\Windows\Fonts\YuGothB.ttc"


# ── Utilities ─────────────────────────────────────────────────────────────────
def _e(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def strip_html(text):
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<p[^>]*>",  "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>",   "",   text)
    return _html.unescape(text).strip()

def parse_json_safe(text):
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())


# ── Data loaders ──────────────────────────────────────────────────────────────
def load_home():
    path = DATA_DIR / "home_latest.json"
    if not path.exists(): return []
    data = json.loads(path.read_text(encoding="utf-8"))
    segments = data.get("segments", [])
    lines = []
    for seg in segments[:6]:
        title   = seg.get("title", "")
        sub     = seg.get("subtitle", "")
        bullets = seg.get("bullets", [])[:3]
        risk    = seg.get("risk", "")
        ctx     = seg.get("context", "")
        btext   = " / ".join(b.get("text","") for b in bullets if b.get("text"))
        lines.append(f"[Home] {title} — {sub}. {btext}. {risk} {ctx}")
    return lines

def load_intelligence():
    path = DATA_DIR / "mail_rolling.json"
    if not path.exists(): return []
    data  = json.loads(path.read_text(encoding="utf-8"))
    emails = data.get("emails", [])[:8]
    lines = []
    for em in emails:
        subj = em.get("subject_en") or em.get("subject","")
        summ = em.get("summary_en","")
        sender = em.get("sender_norm","")
        if subj:
            lines.append(f"[Intelligence/{sender}] {subj}. {summ}")
    sidebar = data.get("toyota_summary_en","")
    if sidebar:
        lines.append(f"[Intelligence/Auto Sidebar] {sidebar[:400]}")
    return lines

def load_en_page(filepath: Path, max_chars=4000) -> str:
    if not filepath.exists(): return ""
    raw = filepath.read_text(encoding="utf-8")
    text = strip_html(raw)
    text = re.sub(r"\s{3,}", "\n\n", text)
    return text[:max_chars]

def load_trump():
    return load_en_page(BASE / "docs" / "en" / "trump.html")

def load_themes():
    path = DATA_DIR / "theme_latest.json"
    if not path.exists():
        return load_en_page(BASE / "docs" / "en" / "theme.html")
    data = json.loads(path.read_text(encoding="utf-8"))
    themes = data.get("themes", [])[:4] if isinstance(data, dict) else []
    lines = []
    for t in themes:
        title = t.get("title","")
        body  = t.get("body","") or t.get("summary","")
        if title: lines.append(f"[Theme] {title}: {body[:200]}")
    return "\n".join(lines)

def load_midterms():
    return load_en_page(BASE / "docs" / "en" / "midterm.html")


# ── Claude: 英語 Exec Summary 生成 ───────────────────────────────────────────
SYSTEM_PROMPT = """\
You write one-page intelligence briefings for a senior executive.
Style: WSJ front page, direct and factual. No jargon. No consulting-speak.
Format: exactly 4 sections, each with a short sharp headline and 3-5 sentences.
Prioritize: what is most actionable and consequential TODAY.
"""

SECTION_SCHEMA = """\
Return JSON only — no prose, no markdown outside the JSON:
{
  "date_en": "Tuesday, July 8, 2026",
  "sections": [
    {
      "tag": "Heads Up",
      "headline": "One sharp sentence — the single most important thing today",
      "body": "3-5 sentences. Specific facts. Bold the one key number or phrase."
    },
    {
      "tag": "Changed",
      "headline": "What has already shifted since yesterday",
      "body": "3-5 sentences. Concrete. What is different now."
    },
    {
      "tag": "Changing Now",
      "headline": "What is in motion right now",
      "body": "3-5 sentences. What to watch in the next 24-72 hours."
    },
    {
      "tag": "Medium Term",
      "headline": "The 6-12 month signal buried in today's noise",
      "body": "3-5 sentences. Why this matters beyond this week."
    }
  ]
}
"""

def generate_en_summary(source_text: str, client, date_en: str) -> dict:
    prompt = (
        f"Today is {date_en}.\n\n"
        "Here is today's raw intelligence from multiple sources:\n\n"
        f"{source_text}\n\n"
        "Write an Executive Briefing with exactly 4 sections.\n"
        "Pick only the most important, consequential stories.\n"
        "Do NOT summarize every source — synthesize into the clearest possible picture.\n\n"
        + SECTION_SCHEMA
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return parse_json_safe(resp.content[0].text)


# ── Claude: 日本語翻訳 ─────────────────────────────────────────────────────────
def translate_sections_to_ja(sections: list, client) -> list:
    items = "\n".join(
        f'[{i}] headline: {s["headline"]}\nbody: {s["body"]}'
        for i, s in enumerate(sections)
    )
    prompt = (
        "以下の英語テキストを自然な日本語に翻訳してください。\n"
        "JSONのみ返してください（他のテキスト不要）:\n"
        "[\n"
        '  {"headline_ja": "...", "body_ja": "..."},\n'
        "  ... (同じ順序で4件)\n"
        "]\n\n"
        f"{items}"
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )
    return parse_json_safe(resp.content[0].text)


# ── EN HTML 生成 ──────────────────────────────────────────────────────────────
def bold_to_html(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

def build_en_html(result: dict, updated_at: str) -> str:
    now_jst = datetime.now(JST)
    date_en = result.get("date_en", now_jst.strftime("%A, %B %d, %Y"))
    sections = result.get("sections", [])

    sections_html = ""
    for sec in sections:
        tag      = _e(sec.get("tag",""))
        headline = _e(sec.get("headline",""))
        body     = bold_to_html(_e(sec.get("body","")))
        sections_html += f"""
    <div class="section">
      <hr class="section-rule">
      <div class="section-header">
        <span class="section-tag">[{tag}]</span>
        <span class="section-headline">{headline}</span>
      </div>
      <p class="section-body">{body}</p>
    </div>
"""

    # アーカイブ行
    archive_filename = f"briefing_{now_jst.strftime('%Y%m%d')}.pdf"
    archive_date_en  = now_jst.strftime("%B %d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Exec Summary | World Intelligence Monitor</title>
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
.summary-wrap {{ max-width: 820px; margin: 32px auto; padding: 0 20px 40px; }}
.toolbar {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }}
.toolbar-label {{ font-size: 12px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }}
.toolbar-right {{ display: flex; gap: 8px; align-items: center; }}
.btn-print {{ display: inline-flex; align-items: center; gap: 5px; background: #1a1a2e; color: #fff; border: none; border-radius: 20px; padding: 6px 18px; font-size: 12px; font-weight: 700; cursor: pointer; transition: opacity .15s; font-family: inherit; }}
.btn-print:hover {{ opacity: .82; }}
.btn-jp {{ display: inline-flex; align-items: center; gap: 5px; background: transparent; color: #6b7280; border: 1px solid #d1d5db; border-radius: 20px; padding: 5px 14px; font-size: 12px; font-weight: 700; text-decoration: none; transition: all .15s; }}
.btn-jp:hover {{ color: #1a1a2e; border-color: #9ca3af; }}
.a4-card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 4px; box-shadow: 0 4px 24px rgba(0,0,0,.10); padding: 48px 52px; min-height: 800px; position: relative; }}
.doc-title {{ font-size: 22px; font-weight: 800; color: #1a1a2e; text-align: center; letter-spacing: .5px; }}
.doc-meta {{ font-size: 13px; color: #6b7280; text-align: center; margin-top: 4px; }}
.doc-rule-thick {{ border: none; border-top: 3px solid #1a1a2e; margin: 16px 0 24px; }}
.section {{ margin-bottom: 28px; }}
.section-rule {{ border: none; border-top: 1.5px solid #1a1a2e; margin-bottom: 10px; }}
.section-header {{ display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px; }}
.section-tag {{ font-size: 12px; font-weight: 800; color: #1a1a2e; text-transform: uppercase; letter-spacing: .5px; white-space: nowrap; }}
.section-headline {{ font-size: 18px; font-weight: 700; color: #1a1a2e; line-height: 1.4; }}
.section-body {{ font-size: 15px; color: #2a2a3e; line-height: 1.85; text-align: justify; }}
.section-body strong {{ color: #1a1a2e; }}
.doc-rule-end {{ border: none; border-top: 1.5px solid #1a1a2e; margin: 24px 0 12px; }}
.doc-footer-line {{ text-align: right; font-size: 12px; color: #6b7280; }}
.archive-section {{ margin-top: 32px; background: #fff; border-radius: 8px; border: 1px solid #e5e7eb; padding: 16px 22px; }}
.arch-label {{ font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e5e7eb; }}
.arch-list {{ list-style: none; }}
.arch-list li {{ padding: 7px 0; border-bottom: 1px solid #f3f4f6; }}
.arch-list li:last-child {{ border-bottom: none; }}
.arch-link {{ color: #6b7280; text-decoration: none; font-size: 13px; display: flex; align-items: center; gap: 8px; transition: color .15s; }}
.arch-link:hover {{ color: #0096c8; }}
.site-footer {{ text-align: center; padding: 28px 20px; font-size: 11px; color: #9ca3af; margin-top: 32px; border-top: 1px solid #e5e7eb; }}
@media (max-width: 640px) {{
  .site-header {{ padding: 0 14px; }} .update-time {{ display: none; }}
  .page-nav {{ padding: 0 8px; }} .page-nav a {{ padding: 0 12px; font-size: 13px; }}
  .a4-card {{ padding: 28px 22px; }} .summary-wrap {{ padding: 0 12px 32px; }}
}}
@media print {{
  @page {{ size: A4; margin: 14mm 22mm 16mm; }}
  body {{ background: #fff; font-size: 11pt; }}
  .site-header, .page-nav, .toolbar, .archive-section, .site-footer {{ display: none !important; }}
  .summary-wrap {{ max-width: 100%; margin: 0; padding: 0; }}
  .a4-card {{ border: none; box-shadow: none; padding: 0; min-height: 0; }}
  .section-body {{ font-size: 10.5pt; }} .doc-title {{ font-size: 18pt; }}
}}
</style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'">World<em>News</em></div>
  <div class="header-date">{_e(date_en)}</div>
  <div class="header-spacer"></div>
  <div class="update-time">Updated: {_e(updated_at)}</div>
  <div class="lang-toggle">
    <a href="../jp/summary.html">JP</a>
    <a href="summary.html" class="active">EN</a>
  </div>
  <div class="live-badge">LIVE</div>
</header>
<nav class="page-nav">
  <a href="index.html"><span class="nav-icon">🏠</span>Home</a>
  <a href="intelligence.html"><span class="nav-icon">📋</span>Intelligence</a>
  <a href="trump.html"><span class="nav-icon">🇺🇸</span>US / Trump</a>
  <a href="theme.html"><span class="nav-icon">🔎</span>Themes</a>
  <a href="midterm.html"><span class="nav-icon">🗳️</span>US Midterms</a>
  <a href="summary.html" class="active"><span class="nav-icon">📋</span>Exec Summary</a>
</nav>

<div class="summary-wrap">
  <div class="toolbar">
    <span class="toolbar-label">Executive Briefing &nbsp;— {_e(date_en)}</span>
    <div class="toolbar-right">
      <button class="btn-print" onclick="window.print()">🖨 Print / Save PDF</button>
    </div>
  </div>

  <div class="a4-card">
    <div class="doc-title">EXECUTIVE BRIEFING</div>
    <div class="doc-meta">{_e(date_en)} &nbsp;|&nbsp; World Intelligence Monitor</div>
    <hr class="doc-rule-thick">
{sections_html}
    <hr class="doc-rule-end">
    <div class="doc-footer-line">— End of Briefing &nbsp;|&nbsp; World Intelligence Monitor</div>
  </div>

  <div class="archive-section">
    <p class="arch-label">Past Reports</p>
    <ul class="arch-list" id="archive-list">
      <li><a href="../data/briefings/{_e(archive_filename)}" download class="arch-link">📄 Executive Briefing &nbsp; {_e(archive_date_en)}</a></li>
    </ul>
  </div>
</div>

<footer class="site-footer">
  Sources: NHK &nbsp;|&nbsp; Nikkei &nbsp;|&nbsp; Sankei &nbsp;|&nbsp; CNBC &nbsp;|&nbsp; FT &nbsp;|&nbsp; BBC &nbsp;|&nbsp; Reuters &nbsp;|&nbsp; Eurasia Group &nbsp;|&nbsp; POLITICO<br>
  Updated: {_e(updated_at)} &nbsp;|&nbsp; Auto-updated every morning at 08:00 JST &nbsp;|&nbsp; World News
</footer>
</body>
</html>"""


# ── JP PDF 生成 (reportlab) ───────────────────────────────────────────────────
def build_jp_pdf(sections_ja: list, sections_en: list, date_jp: str):
    pdfmetrics.registerFont(TTFont('JPN',   FONT_PATH))
    pdfmetrics.registerFont(TTFont('JPN-B', FONT_B_PATH))

    BLK = colors.black
    GRY = colors.HexColor('#555555')

    def S(name, **kw):
        base = dict(fontName='JPN', fontSize=11, leading=20, textColor=BLK,
                    spaceAfter=0, spaceBefore=0)
        base.update(kw)
        return ParagraphStyle(name, **base)

    S_TITLE = S('title',  fontName='JPN-B', fontSize=16, alignment=TA_CENTER)
    S_META  = S('meta',   fontName='JPN',   fontSize=13, textColor=GRY, alignment=TA_CENTER)
    S_LABEL = S('label',  fontName='JPN-B', fontSize=12, leading=18)
    S_BODY  = S('body',   fontName='JPN',   fontSize=11, leading=19, alignment=TA_JUSTIFY)

    TAG_MAP = {
        "Heads Up":    "【Heads up】",
        "Changed":     "【変化済み】",
        "Changing Now":"【近く変化】",
        "Medium Term": "【中長期】",
    }

    doc = SimpleDocTemplate(
        str(PDF_LATEST), pagesize=A4,
        topMargin=11*mm, bottomMargin=13*mm,
        leftMargin=22*mm, rightMargin=22*mm,
        title=f"エグゼクティブ・ブリーフィング {date_jp}",
        author="World Intelligence Monitor",
    )

    story = [
        Paragraph("エグゼクティブ・ブリーフィング", S_TITLE),
        Spacer(1, 2*mm),
        Paragraph(date_jp, S_META),
        Spacer(1, 11*mm),
        HRFlowable(width="100%", thickness=3, color=BLK),
        Spacer(1, 6*mm),
    ]

    GAP = 14*mm
    for i, (sec_ja, sec_en) in enumerate(zip(sections_ja, sections_en)):
        tag_en  = sec_en.get("tag","")
        tag_jp  = TAG_MAP.get(tag_en, f"【{tag_en}】")
        hl_ja   = sec_ja.get("headline_ja","")
        body_ja = sec_ja.get("body_ja","")
        body_ja = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", body_ja)

        story.append(KeepTogether([
            HRFlowable(width="100%", thickness=1.5, color=BLK, spaceAfter=3*mm),
            Paragraph(f'<b>{tag_jp}</b>　{hl_ja}', S_LABEL),
            Spacer(1, 4*mm),
            Paragraph(body_ja, S_BODY),
        ]))
        if i < len(sections_ja) - 1:
            story.append(Spacer(1, GAP))

    story += [Spacer(1, 4*mm), HRFlowable(width="100%", thickness=1.5, color=BLK)]

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('JPN', 11)
        canvas.drawRightString(A4[0] - 22*mm, 8*mm, "以　　上")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"[PDF] 生成完了: {PDF_LATEST}")


# ── Type C JP summary.html 更新 ───────────────────────────────────────────────
def update_type_c_summary(archive_filename: str):
    if not JP_C_SUMMARY.exists(): return
    txt = JP_C_SUMMARY.read_text(encoding="utf-8")
    now_jst = datetime.now(JST)
    today = now_jst.strftime("%Y-%m-%d")
    pdf_path = f"../data/briefings/{archive_filename}"
    date_jp  = now_jst.strftime("%Y年%m月%d日")
    datetime_jp = now_jst.strftime("%Y年%m月%d日 %H:%M")

    # アーカイブに先頭追��（重複チェック）
    if today not in txt:
        new_entry = f'<li class="arch-item"><a class="arch-link" href="{pdf_path}" target="_blank">📄 {today} ブリーフィング</a></li>'
        txt = re.sub(r'(<ul[^>]*class="[^"]*arch[^"]*"[^>]*>)', r'\1\n    ' + new_entry, txt, count=1)

    # iframe src を今日の PDF に更新
    txt = re.sub(r'(<iframe[^>]*src=")[^"]*(")', rf'\g<1>{pdf_path}\g<2>', txt, count=1)

    # pdf-label の日付を更新
    txt = re.sub(r'(エグゼクティブ・ブリーフィング &nbsp;)\d{4}年\d{2}月\d{2}日',
                 rf'\g<1>{date_jp}', txt)

    # ヘッダー日付・フッター更新時刻を更新
    txt = re.sub(r'(<div class="header-date">)[^<]*(</div>)', rf'\g<1>{date_jp}\g<2>', txt)
    txt = re.sub(r'最終更新: [^<\n&]+', f'最終更新: {datetime_jp} JST', txt)

    JP_C_SUMMARY.write_text(txt, encoding="utf-8")
    print(f"[JP Summary] Type C アーカイブリスト更新完了")


# ── git + deploy ──────────────────────────────────────────────────────────────
def git_push_and_deploy(msg: str):
    def run(cmd): subprocess.run(cmd, cwd=str(BASE))
    run(["git", "add",
         "docs/en/summary.html",
         "docs/jp/summary.html",
         "docs/briefing_latest.pdf",
         "docs/data/briefings"])
    diff = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=str(BASE))
    if diff.returncode == 0:
        print("[Git] 変更なし。スキップ。")
        return
    run(["git", "commit", "-m", msg])
    push = subprocess.run(["git", "push"], cwd=str(BASE))
    if push.returncode != 0:
        run(["git", "fetch", "origin", "main"])
        run(["git", "merge", "-X", "ours", "origin/main", "--no-edit"])
        subprocess.run(["git", "push"], cwd=str(BASE))
    req = urllib.request.Request(
        "https://api.github.com/repos/shortreport/world-monitoring/actions/workflows/update.yml/dispatches",
        data=b'{"ref":"main"}',
        headers={"Authorization": f"token {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req)
        print("[Deploy] GitHub Actions トリガー完了。約5分で反映されます。")
    except Exception as ex:
        print(f"[Deploy] WARN: {ex}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    now_jst      = datetime.now(JST)
    date_en      = now_jst.strftime("%A, %B %d, %Y")
    date_jp      = now_jst.strftime("%Y年%m月%d日（") + "月火水木金土日"[now_jst.weekday()] + "）"
    date_jp_full = now_jst.strftime("%Y年%m月%d日")
    updated_at   = now_jst.strftime("%Y-%m-%d %H:%M JST")
    archive_name = f"briefing_{now_jst.strftime('%Y%m%d')}.pdf"

    client = anthropic.Anthropic()

    # ── 1. ソースデータ収集 ────────────────────────────────────────────────────
    print("ソースデータ収集中...")
    lines = []
    lines += load_home()
    lines += load_intelligence()
    trump_text = load_trump()
    if trump_text:
        lines.append(f"[US/Trump] {trump_text[:800]}")
    themes_text = load_themes()
    if themes_text:
        lines.append(f"[Themes] {themes_text[:800]}")
    midterms_text = load_midterms()
    if midterms_text:
        lines.append(f"[Midterms] {midterms_text[:600]}")

    source_text = "\n\n".join(lines)
    print(f"  ソース総文字数: {len(source_text)}")

    # ── 2. EN Exec Summary 生成 ─────────────────────────────────────────────
    print("英語 Exec Summary 生成中...")
    result = generate_en_summary(source_text, client, date_en)
    sections = result.get("sections", [])
    print(f"  セクション数: {len(sections)}")
    for sec in sections:
        print(f"  [{sec['tag']}] {sec['headline'][:60]}")

    # ── 3. EN HTML 書き出し ──────────────────────────────────────────────────
    html_content = build_en_html(result, updated_at)
    EN_SUMMARY.write_text(html_content, encoding="utf-8")
    print(f"[OK] EN Summary -> {EN_SUMMARY}")

    # ── 4. JP 翻訳 ─────────────────────────────────────────────────────────
    print("日本語翻訳中...")
    sections_ja = translate_sections_to_ja(sections, client)
    print(f"  翻訳完了: {len(sections_ja)} セクション")

    # ── 5. JP PDF 生成 ──────────────────────────────────────────────────────
    print("日本語 PDF 生成中...")
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    build_jp_pdf(sections_ja, sections, date_jp)
    archive_path = BRIEFINGS_DIR / archive_name
    shutil.copy2(PDF_LATEST, archive_path)
    print(f"[PDF] アーカイブ: {archive_path}")

    # ── 6. Type C JP summary.html 更新 ──────────────────────────────────────
    update_type_c_summary(archive_name)

    # ── 7. git + deploy ─────────────────────────────────────────────────────
    print("\n[Git] コミット＆プッシュ中...")
    git_push_and_deploy(f"Exec Summary: {updated_at}")


if __name__ == "__main__":
    main()
