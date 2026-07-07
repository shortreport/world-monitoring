#!/usr/bin/env python3
"""
make_briefing_auto.py
=====================
毎朝自動実行スクリプト（Task Scheduler 8:00 JST）

1. home_latest.json / mail_latest.json / theme_latest.json を読み込み
2. Claude API で 4 セクションのブリーフィング文を生成
3. ReportLab で A4 1 枚 PDF を生成
4. docs/briefing_latest.pdf を更新
5. docs/data/briefings/briefing_YYYYMMDD.pdf にアーカイブ保存
6. docs/summary.html を再生成（PDF 埋め込み＋アーカイブ一覧）
7. git add / commit / push
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── 日付 ──────────────────────────────────────────────────────
JST       = timezone(timedelta(hours=9))
TODAY     = datetime.now(JST)
DATE_JP   = TODAY.strftime("%Y年%m月%d日").replace("年0", "年").replace("月0", "月")
DATE_KEY  = TODAY.strftime("%Y%m%d")            # ファイル名用
DATE_FULL = TODAY.strftime("%Y年%m月%d日")      # ヘッダー表示用
WEEKDAY   = ["月", "火", "水", "木", "金", "土", "日"][TODAY.weekday()]

BASE      = Path(__file__).parent
DATA_DIR  = BASE / "docs" / "data"
BRIEF_DIR = BASE / "docs" / "data" / "briefings"
LATEST    = BASE / "docs" / "briefing_latest.pdf"
ARCHIVE   = BRIEF_DIR / f"briefing_{DATE_KEY}.pdf"
SUMMARY   = BASE / "docs" / "summary.html"

# ── ネットワーク待機（スリープ解除直後のDNS失敗対策）─────────────
import socket, time as _time
def _wait_for_network(host="api.anthropic.com", port=443, timeout=60):
    deadline = _time.time() + timeout
    while _time.time() < deadline:
        try:
            socket.setdefaulttimeout(5)
            socket.getaddrinfo(host, port)
            return True
        except OSError:
            print(f"  [待機] ネットワーク未接続、リトライ中...")
            _time.sleep(5)
    return False

if not _wait_for_network():
    sys.exit("[ERROR] ネットワーク接続タイムアウト（60秒）")

# ── Claude API ────────────────────────────────────────────────
try:
    import anthropic
except ImportError:
    sys.exit("[ERROR] pip install anthropic")

CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not CLAUDE_API_KEY:
    try:
        from api_config import ANTHROPIC_API_KEY as _k
        CLAUDE_API_KEY = _k
    except ImportError:
        pass
MODEL = "claude-sonnet-4-6"

# ── ReportLab ─────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import KeepTogether

pdfmetrics.registerFont(TTFont("JPN",   r"C:\Windows\Fonts\YuGothM.ttc"))
pdfmetrics.registerFont(TTFont("JPN-B", r"C:\Windows\Fonts\YuGothB.ttc"))


# ══════════════════════════════════════════════════════════════
#  STEP 1: ニュースデータを読み込む
# ══════════════════════════════════════════════════════════════
def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def summarize_news() -> str:
    """home / mail / theme の JSON を読み込み、Claude に渡すテキストを生成"""
    parts = []

    # ── home_latest.json ──
    home = load_json(DATA_DIR / "home_latest.json")
    for seg in home.get("segments", []):
        title = seg.get("title", "")
        bullets = seg.get("bullets", [])
        risk    = seg.get("risk", "")
        context = seg.get("context", "")
        b_texts = []
        for b in bullets[:3]:
            b_texts.append(b.get("text", b) if isinstance(b, dict) else b)
        parts.append(f"【ホーム】{title}\n" +
                     "\n".join(f"  ・{t}" for t in b_texts) +
                     (f"\n  リスク: {risk}" if risk else "") +
                     (f"\n  背景: {context}" if context else ""))

    # ── mail_latest.json ──
    mail = load_json(DATA_DIR / "mail_latest.json")
    for item in mail.get("items", [])[:5]:
        subject = item.get("subject", "")
        summary = item.get("summary", "")
        parts.append(f"【メール】{subject}\n  {summary[:200]}")

    # ── theme_latest.json ──
    theme = load_json(DATA_DIR / "theme_latest.json")
    for t in theme.get("themes", [])[:3]:
        name    = t.get("name", "")
        summary = t.get("summary", "")
        parts.append(f"【テーマ】{name}\n  {summary[:200]}")

    return "\n\n".join(parts)


# ══════════════════════════════════════════════════════════════
#  STEP 2: Claude API でブリーフィング文を生成
# ══════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """あなたは外交・安全保障の専門アナリストです。
与えられたニュースデータを分析し、以下の4セクションのエグゼクティブ・ブリーフィングを生成してください。

【出力形式】必ず以下のJSONのみを返してください（説明文不要）:
{
  "sections": [
    {
      "tag": "【Heads up】",
      "headline": "見出し（20字以内）",
      "body": "本文（3〜4文、120字以内）"
    },
    {
      "tag": "【変化済み】",
      "headline": "見出し（20字以内）",
      "body": "本文（3〜4文、120字以内）"
    },
    {
      "tag": "【近く変化】",
      "headline": "見出し（20字以内）",
      "body": "本文（3〜4文、120字以内）"
    },
    {
      "tag": "【中長期】",
      "headline": "見出し（20字以内）",
      "body": "本文（3〜4文、120字以内）"
    }
  ]
}

各セクションの定義:
- Heads up: 今最も注目すべき1案件（今後数週間の最大リスク）
- 変化済み: すでに世界情勢が大きく変化したこと（既成事実）
- 近く変化: 近く大きく変化しそうなこと（今後1〜2か月）
- 中長期: 中長期的に大きな影響を及ぼしそうな事象（6か月〜1年）

制約:
- bodyは必ず3〜4文で収める（PDF A4 1枚に収めるため）
- 重要な固有名詞・数字は残す
- JSON以外は出力しない
- 【具体性の確保】①各事象には発生日（M/D形式）を付記して時期を明確にすること（例：「日本企業20社を輸出管理リストに追加（6/29）し、」）。②企業・人物・機関は可能な限り具体的な固有名詞で表記すること（例：「三菱電機系、日鋼特機など」）。"""

def generate_briefing(news_text: str) -> list[dict]:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"以下のニュースデータに基づいてブリーフィングを生成してください:\n\n{news_text}"}],
    )
    raw = msg.content[0].text.strip()
    # JSON部分だけ抽出
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(f"JSON not found in response: {raw[:200]}")
    data = json.loads(m.group())
    return data["sections"]


# ══════════════════════════════════════════════════════════════
#  STEP 3: PDF 生成 + 1ページ自動調整
# ══════════════════════════════════════════════════════════════

def count_pdf_pages(path: Path) -> int:
    """PDFのページ数を返す"""
    from pypdf import PdfReader
    return len(PdfReader(str(path)).pages)


def shorten_one_sentence(body: str) -> str | None:
    """句点で区切って末尾の1文を削除して返す。これ以上削れない場合は None"""
    parts = [s.strip() for s in body.split("。") if s.strip()]
    if len(parts) <= 1:
        return None
    return "。".join(parts[:-1]) + "。"


def fit_to_one_page(sections: list[dict], output: Path) -> tuple[list[dict], int]:
    """
    1ページに収まるまで内容を削減する。
    削減順（循環）: 中長期 → 近く変化 → 変化済み

    STEP 1: まず現状のまま生成してページ数確認
    STEP 2: 2ページ以上なら削減が必要な文数を順番に特定
    STEP 3: 1ページに収まるまで削減を繰り返す
    """
    REDUCE_ORDER = ["【中長期】", "【近く変化】", "【変化済み】"]

    # STEP 1: 現状のままPDF生成・ページ数確認
    make_pdf(sections, output)
    pages = count_pdf_pages(output)
    print(f"  初回PDF: {pages}ページ")

    if pages <= 1:
        return sections, 0

    # STEP 2: 削減開始（何文削れば収まるか確認しながら進める）
    print(f"  {pages}ページ検出 → 1ページに収める処理開始")
    print(f"  削減順: 中長期 → 近く変化 → 変化済み（循環）")
    total_reduced = 0

    # STEP 3: 削減ループ（最大30回試行）
    for _ in range(30):
        for tag in REDUCE_ORDER:
            sec = next((s for s in sections if s["tag"] == tag), None)
            if sec is None:
                continue
            shortened = shorten_one_sentence(sec["body"])
            if shortened is None:
                continue  # これ以上削れないのでスキップ
            sec["body"] = shortened
            total_reduced += 1
            make_pdf(sections, output)
            pages_now = count_pdf_pages(output)
            print(f"    {tag}: 1文削減 → {pages_now}ページ（累計{total_reduced}文削減）")
            if pages_now <= 1:
                print(f"  ✓ 1ページに収まりました（計{total_reduced}文削減）")
                return sections, total_reduced

    print(f"  [WARN] {total_reduced}文削減後も1ページに収まりませんでした")
    return sections, total_reduced


def make_pdf(sections: list[dict], output: Path):
    BLK = colors.black
    GRY = colors.HexColor("#555555")
    GAP = 14 * mm

    def S(name, **kw):
        base = dict(fontName="JPN", fontSize=11, leading=20,
                    textColor=BLK, spaceAfter=0, spaceBefore=0)
        base.update(kw)
        return ParagraphStyle(name, **base)

    S_TITLE = S("title", fontName="JPN-B", fontSize=16, alignment=TA_CENTER)
    S_META  = S("meta",  fontName="JPN",   fontSize=13, textColor=GRY, alignment=TA_CENTER)
    S_LABEL = S("label", fontName="JPN-B", fontSize=12, leading=18)
    S_BODY  = S("body",  fontName="JPN",   fontSize=11, leading=19, alignment=TA_JUSTIFY)

    doc = SimpleDocTemplate(
        str(output), pagesize=A4,
        topMargin=11*mm, bottomMargin=13*mm,
        leftMargin=22*mm, rightMargin=22*mm,
        title=f"エグゼクティブ・ブリーフィング {TODAY.strftime('%Y-%m-%d')}",
        author="国家情報機関",
    )

    def section(tag, headline, body):
        return KeepTogether([
            HRFlowable(width="100%", thickness=1.5, color=BLK, spaceAfter=3*mm),
            Paragraph(f"<b>{tag}</b>　{headline}", S_LABEL),
            Spacer(1, 4*mm),
            Paragraph(body, S_BODY),
        ])

    story = []
    story.append(Paragraph("エグゼクティブ・ブリーフィング", S_TITLE))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(f"{DATE_JP}（{WEEKDAY}）", S_META))
    story.append(Spacer(1, 11*mm))
    story.append(HRFlowable(width="100%", thickness=3, color=BLK))
    story.append(Spacer(1, 6*mm))

    for i, sec in enumerate(sections):
        story.append(section(sec["tag"], sec["headline"], sec["body"]))
        if i < len(sections) - 1:
            story.append(Spacer(1, GAP))

    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLK))

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("JPN", 11)
        canvas.drawRightString(A4[0] - 22*mm, 8*mm, "以　　上")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


# ══════════════════════════════════════════════════════════════
#  STEP 4: summary.html を再生成
# ══════════════════════════════════════════════════════════════
NAV = """\
<nav class="page-nav">
  <a href="index.html"><span class="nav-icon">🏠</span>ホーム</a>
  <a href="mail.html"><span class="nav-icon">📧</span>メール要約</a>
  <a href="trump.html"><span class="nav-icon">🇺🇸</span>USトランプ</a>
  <a href="theme.html"><span class="nav-icon">🔎</span>個別テーマ</a>
  <a href="summary.html" class="active"><span class="nav-icon">📋</span>エグゼクティブ・サマリー</a>
</nav>"""

def build_summary_html() -> str:
    # アーカイブ一覧（日付降順）
    archives = sorted(BRIEF_DIR.glob("briefing_????????.pdf"), reverse=True)

    archive_items = ""
    for p in archives:
        m = re.search(r"briefing_(\d{4})(\d{2})(\d{2})\.pdf", p.name)
        if not m:
            continue
        y, mo, d = m.group(1), m.group(2), m.group(3)
        label = f"エグゼクティブ・ブリーフィング　{y}年{int(mo)}月{int(d)}日"
        rel   = f"data/briefings/{p.name}"
        archive_items += f'    <li><a href="{rel}" download class="arch-link">📄 {label}</a></li>\n'

    archive_block = ""
    if archive_items:
        archive_block = f"""
  <div class="archive-section">
    <p class="arch-label">過去のレポート</p>
    <ul class="arch-list">
{archive_items}    </ul>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>エグゼクティブ・サマリー | World News</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --primary: #16163e; --surface: #ffffff; --surface-2: #f3f4f6;
      --border: #e2e4e9; --text: #1a1a2e; --text-sub: #5f6368;
      --radius: 12px; --accent: #0096c8;
    }}
    body {{ font-family: 'Noto Sans JP', -apple-system, 'Hiragino Sans', 'Yu Gothic UI', sans-serif;
            background: var(--surface-2); color: var(--text); line-height: 1.65; font-size: 14px; }}
    .site-header {{ background: var(--primary); color: #fff; padding: 0 24px; height: 58px;
                    display: flex; align-items: center; gap: 16px;
                    position: sticky; top: 0; z-index: 300; box-shadow: 0 2px 8px rgba(0,0,0,.25); }}
    .logo {{ font-size: 20px; font-weight: 700; letter-spacing: .5px; white-space: nowrap; }}
    .logo em {{ color: #5bc8f5; font-style: normal; }}
    .header-date {{ font-size: 12px; color: rgba(255,255,255,.5); white-space: nowrap; }}
    .header-spacer {{ flex: 1; }}
    .live-badge {{ background: #e63946; color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }}
    .update-time {{ font-size: 11px; color: rgba(255,255,255,.4); white-space: nowrap; }}
    .force-update-btn {{ display: inline-flex; align-items: center; gap: 4px; background: rgba(255,255,255,.1);
      color: rgba(255,255,255,.65); border: 1px solid rgba(255,255,255,.25); border-radius: 14px;
      padding: 4px 11px; font-size: 11px; font-weight: 600; cursor: pointer; white-space: nowrap;
      font-family: inherit; transition: background .15s, color .15s, border-color .15s; }}
    .force-update-btn:hover {{ background: rgba(255,255,255,.22); color: #fff; border-color: rgba(255,255,255,.5); }}
    .force-update-btn:disabled {{ opacity: .55; cursor: not-allowed; }}
    .page-nav {{ background: var(--surface); border-bottom: 1px solid var(--border);
                 padding: 0 24px; display: flex; align-items: stretch;
                 position: sticky; top: 58px; z-index: 200; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .page-nav a {{ display: flex; align-items: center; gap: 6px; padding: 0 18px; height: 44px;
                   font-size: 14px; font-weight: 500; color: var(--text-sub);
                   text-decoration: none; border-bottom: 3px solid transparent;
                   white-space: nowrap; transition: color .15s, border-color .15s; }}
    .page-nav a:hover {{ color: var(--text); }}
    .page-nav a.active {{ color: var(--primary); border-bottom-color: var(--primary); font-weight: 700; }}
    .page-nav a .nav-icon {{ font-size: 15px; }}
    .page-nav a:last-child {{ margin-left: auto; border-left: 1px solid var(--border); }}
    .site-footer {{ text-align: center; padding: 24px; font-size: 12px; color: var(--text-sub);
                    margin-top: 32px; border-top: 1px solid var(--border); }}
    @media (max-width: 640px) {{
      .site-header {{ padding: 0 14px; gap: 10px; }}
      .page-nav {{ padding: 0 8px; }}
      .page-nav a {{ padding: 0 12px; font-size: 13px; }}
      .update-time {{ display: none; }}
      .force-update-btn {{ display: none; }}
    }}
    .summary-wrap {{ max-width: 900px; margin: 24px auto; padding: 0 20px; }}
    .pdf-toolbar {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}
    .pdf-label {{ font-size: 13px; font-weight: 700; color: var(--text-sub); letter-spacing: .5px; }}
    .pdf-download-btn {{ display: inline-flex; align-items: center; gap: 5px;
      background: var(--primary); color: #fff; border-radius: 20px; padding: 6px 18px;
      font-size: 12px; font-weight: 700; text-decoration: none; transition: opacity .15s; }}
    .pdf-download-btn:hover {{ opacity: .82; }}
    .pdf-frame {{ width: 100%; height: calc(100vh - 160px); min-height: 600px;
                  border: 1px solid var(--border); border-radius: var(--radius); background: #fff; }}
    .archive-section {{ margin-top: 28px; background: var(--surface); border-radius: var(--radius);
                         border: 1px solid var(--border); padding: 16px 22px; }}
    .arch-label {{ font-size: 11px; font-weight: 700; color: var(--text-sub);
                   text-transform: uppercase; letter-spacing: 1.2px;
                   margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }}
    .arch-list {{ list-style: none; padding: 0; }}
    .arch-list li {{ padding: 7px 0; border-bottom: 1px solid var(--border); }}
    .arch-list li:last-child {{ border-bottom: none; }}
    .arch-link {{ color: var(--text-sub); text-decoration: none; font-size: 13px;
                  display: flex; align-items: center; gap: 8px; transition: color .15s; }}
    .arch-link:hover {{ color: var(--accent); }}
    @media (max-width: 640px) {{
      .summary-wrap {{ padding: 0 12px; margin: 16px auto; }}
      .pdf-frame {{ height: 70vh; min-height: 400px; }}
    }}
  </style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'" style="cursor:pointer;" title="ホームへ">World<em>News</em></div>
  <div class="header-date">{DATE_FULL}</div>
  <div class="header-spacer"></div>
  <div class="update-time">最終更新: {DATE_FULL} 08:00 JST &nbsp;|&nbsp; 毎朝8:00自動更新</div>
  <button id="force-update-btn" class="force-update-btn" onclick="triggerSiteUpdate()" title="GitHub Actions ワークフローを起動してサイトを更新">🔄 今すぐ更新</button>
  <div class="live-badge">LIVE</div>
</header>
<script>
(function(){{
  function triggerSiteUpdate(){{
    var btn=document.getElementById('force-update-btn');
    btn.textContent='⏳ 更新中…'; btn.disabled=true;
    location.href=location.pathname+'?r='+Date.now();
  }}
  if(location.search.startsWith('?r=')) history.replaceState(null,'',location.pathname);
  window.triggerSiteUpdate=triggerSiteUpdate;
}})();
</script>
{NAV}
<div class="summary-wrap">
  <div class="pdf-toolbar">
    <span class="pdf-label">エグゼクティブ・ブリーフィング &nbsp;{DATE_FULL}</span>
    <a href="briefing_latest.pdf" download class="pdf-download-btn">⬇ ダウンロード</a>
  </div>
  <iframe src="briefing_latest.pdf" class="pdf-frame" title="エグゼクティブ・ブリーフィング"></iframe>
{archive_block}
</div>
<footer class="site-footer">
  ソース: NHK・産経・日経・CNBC・FT・BBC・NYT・Reuters・Al Jazeera ほか &nbsp;|&nbsp; The Economist &nbsp;|&nbsp; White House RSS &nbsp;|&nbsp; Truth Social<br>
  最終更新: {DATE_FULL} 08:00 JST &nbsp;|&nbsp;
  ☁️ ホーム・USトランプ: 6時間ごと自動更新 &nbsp;|&nbsp;
  🖥️ エグゼクティブ・サマリー: 毎朝8:00更新（PC）<br>
  <button onclick="triggerSiteUpdate()" style="background:none;border:none;color:var(--accent);font-size:11px;cursor:pointer;padding:0;font-family:inherit;">🔄 今すぐ更新（GitHub Actions）</button>
  &nbsp;|&nbsp; World News
</footer>
</body></html>
"""


# ══════════════════════════════════════════════════════════════
#  STEP 5: git push
# ══════════════════════════════════════════════════════════════
def git_push():
    add_commit = [
        ["git", "add",
         "docs/briefing_latest.pdf",
         f"docs/data/briefings/briefing_{DATE_KEY}.pdf",
         "docs/summary.html"],
        ["git", "commit", "-m",
         f"Auto briefing: {TODAY.strftime('%Y-%m-%d')} 08:00 JST"],
    ]
    for cmd in add_commit:
        result = subprocess.run(cmd, cwd=str(BASE), capture_output=True, text=True)
        print(" ".join(cmd))
        if result.stdout:
            print(result.stdout.strip())
        if result.returncode != 0:
            print("[WARN]", result.stderr.strip())

    # push失敗時はpull --rebaseして再試行
    for attempt in range(2):
        result = subprocess.run(["git", "push", "origin", "main"],
                                cwd=str(BASE), capture_output=True, text=True)
        print("git push origin main")
        if result.stdout:
            print(result.stdout.strip())
        if result.returncode == 0:
            print("[OK] push完了")
            return
        print("[WARN] push失敗 →", result.stderr.strip())
        if attempt == 0:
            print("  git pull --rebase してリトライ...")
            subprocess.run(["git", "stash"], cwd=str(BASE), capture_output=True)
            pull = subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                                  cwd=str(BASE), capture_output=True, text=True)
            subprocess.run(["git", "stash", "pop"], cwd=str(BASE), capture_output=True)
            print(pull.stdout.strip())
            if pull.returncode != 0:
                print("[WARN] pull失敗:", pull.stderr.strip())
                return
    print("[ERROR] push最終失敗")


# ══════════════════════════════════════════════════════════════
#  メイン
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{TODAY.strftime('%Y-%m-%d %H:%M')} JST] ブリーフィング生成開始")

    # ① ニュース読み込み
    print("  ニュースデータ読み込み...")
    news = summarize_news()

    # ② Claude API でブリーフィング生成
    print("  Claude API 呼び出し中...")
    sections = generate_briefing(news)
    for s in sections:
        print(f"    {s['tag']} {s['headline']}")

    # ③ PDF 生成（1ページ自動調整）
    print(f"  PDF 生成: {LATEST}")
    BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    import shutil
    sections, reduced = fit_to_one_page(sections, LATEST)
    shutil.copy(LATEST, ARCHIVE)
    print(f"  アーカイブ保存: {ARCHIVE}")

    # ④ 90日超のPDFを削除
    cutoff = TODAY - timedelta(days=90)
    for old_pdf in sorted(BRIEF_DIR.glob("briefing_????????.pdf")):
        try:
            d = datetime.strptime(old_pdf.stem.replace("briefing_", ""), "%Y%m%d").replace(tzinfo=JST)
            if d < cutoff:
                old_pdf.unlink()
                print(f"  削除（90日超）: {old_pdf.name}")
        except ValueError:
            pass

    # ⑤ summary.html 再生成
    print("  summary.html 再生成...")
    SUMMARY.write_text(build_summary_html(), encoding="utf-8")

    # ⑥ git push
    print("  git push...")
    git_push()

    print("完了")
