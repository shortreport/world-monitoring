#!/usr/bin/env python3
"""
make_toyota_watch.py
====================
トヨタ・日本自動車産業 関連ニュース抽出レポート

毎朝、世界ニュースの中からトヨタ自動車および日本の自動車産業に
直接・間接的に関連するニュースを自動抽出してPDF化する。

接続経路の例:
  中国が日本企業を輸出管理リストに追加
  → 豊和工業㈱ が含まれる
  → 豊和工業は豊田佐吉の自動織機製造から発展した企業
  → トヨタグループの源流企業

【出力】
  docs/toyota_watch/toyota_watch_YYYYMMDD.pdf
  （関連ニュースがない場合も「本日はなし」として記録）

【メール送信（任意）】
  環境変数を設定すれば自動送信:
    SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS / WATCH_MAIL_TO
"""

import json
import os
import re
import smtplib
import sys
from datetime import datetime, timedelta, timezone
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("[ERROR] pip install anthropic")

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate,
                                 Spacer)
from reportlab.platypus.flowables import KeepTogether

pdfmetrics.registerFont(TTFont("JPN",   r"C:\Windows\Fonts\YuGothM.ttc"))
pdfmetrics.registerFont(TTFont("JPN-B", r"C:\Windows\Fonts\YuGothB.ttc"))

# ── 日付 ──────────────────────────────────────────────────────
JST      = timezone(timedelta(hours=9))
TODAY    = datetime.now(JST)
DATE_JP  = TODAY.strftime("%Y年%m月%d日").replace("年0","年").replace("月0","月")
DATE_KEY = TODAY.strftime("%Y%m%d")
WEEKDAY  = ["月","火","水","木","金","土","日"][TODAY.weekday()]
DATE_EN  = TODAY.strftime("%B %-d, %Y") if os.name != "nt" else TODAY.strftime("%B %d, %Y").replace(" 0", " ")

BASE       = Path(__file__).parent
DATA_DIR   = BASE / "docs" / "data"
WATCH_DIR  = BASE / "docs" / "toyota_watch"
OUTPUT_PDF = WATCH_DIR / f"toyota_watch_{DATE_KEY}.pdf"

# ── Claude API ────────────────────────────────────────────────
CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not CLAUDE_API_KEY:
    try:
        from api_config import ANTHROPIC_API_KEY as _k
        CLAUDE_API_KEY = _k
    except ImportError:
        pass
MODEL = "claude-sonnet-4-6"

# ── メール設定（任意）────────────────────────────────────────
SMTP_HOST    = os.environ.get("SMTP_HOST", "")
SMTP_PORT    = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER    = os.environ.get("SMTP_USER", "")
SMTP_PASS    = os.environ.get("SMTP_PASS", "")
WATCH_MAIL_TO = os.environ.get("WATCH_MAIL_TO", "satoshi.hondo@outlook.jp")


# ══════════════════════════════════════════════════════════════
#  STEP 1: ニュースデータ読み込み
# ══════════════════════════════════════════════════════════════
def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_news_text() -> str:
    parts = []

    home = load_json(DATA_DIR / "home_latest.json")
    for seg in home.get("segments", []):
        title   = seg.get("title", "")
        bullets = seg.get("bullets", [])
        texts   = [b.get("text", b) if isinstance(b, dict) else b for b in bullets[:4]]
        risk    = seg.get("risk", "")
        parts.append(f"【ニュース】{title}\n" +
                     "\n".join(f"  ・{t}" for t in texts) +
                     (f"\n  {risk}" if risk else ""))

    mail = load_json(DATA_DIR / "mail_latest.json")
    for item in mail.get("items", [])[:6]:
        subject = item.get("subject", "")
        summary = item.get("summary", "")
        parts.append(f"【メール】{subject}\n  {summary[:300]}")

    # theme_latest.jsonは大きいので上位テーマのsummaryのみ（短く）
    theme = load_json(DATA_DIR / "theme_latest.json")
    for t in theme.get("themes", [])[:3]:
        name    = t.get("name", "")
        summary = t.get("summary", "")
        if summary:
            parts.append(f"【テーマ】{name}\n  {str(summary)[:150]}")

    return "\n\n".join(parts)


# ══════════════════════════════════════════════════════════════
#  STEP 2: Claude API でトヨタ関連ニュースを抽出
# ══════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are an analyst specializing in Toyota Motor Corporation's supply chain, keiretsu network, and corporate history.

Analyze the given news and extract ALL news items that are directly or indirectly
connected to Toyota Motor or the Japanese automotive industry.

Note: the input news data is in Japanese. Read it carefully, but write your entire
output (all JSON field values) in English.

[SCOPE]
■ Direct connection (relevance 7-10)
- Toyota Motor itself and group companies (Denso, Aisin, Toyota Industries, JTEKT,
  Toyoda Gosei, Hino Motors, Daihatsu, Toyota Boshoku, Aichi Steel, etc.)
- Toyota's major suppliers (tier 1 / tier 2)
- Policy, regulation, or market trends with direct impact on Toyota

■ Indirect connection (relevance 4-6)
- Companies with historical or capital ties
  (e.g., Howa Industries <- descended from Sakichi Toyoda's automatic loom business)
- Impact on Honda, Nissan, Mazda, Subaru, Mitsubishi Motors, Suzuki, Isuzu, etc.
- Impact on auto parts/materials industries (steel, aluminum, semiconductors, resin, etc.)
- EV, battery, and charging infrastructure topics

■ Weak connection (relevance 1-3)
- Macro factors that could indirectly affect the auto industry as a whole
  (energy prices, FX, trade policy, geopolitical risk, etc.)

[IMPORTANT]
- For every company/organization/person mentioned in the news, investigate and
  explain step by step its connection path to Toyota
- If the connection is unclear, write "connection: unknown (possible)"
- If there is no relevant news, return an empty array

[MANDATORY DEPTH REQUIREMENTS - do not stop at surface-level correlation]

1. When a number or list appears, verify the actual breakdown via web_search.
   Example: if "32 Japan-related vessels" appears, search for the actual ship
   names, operators, and cargo where possible, and determine whether any are
   connected to Toyota/the auto industry.
   If "China adds 40 Japanese companies to the export control list" appears,
   search primary sources (MOFCOM, People's Daily, etc.) for the actual list of
   40 companies and individually check whether any Toyota-affiliated or auto
   parts companies are included.
   -> If, after verification, the conclusion is "no connection," that is a valid
      and acceptable finding to report.
      However, writing "no connection" WITHOUT having verified is forbidden.

2. Identify specific items/materials subject to restriction or sanctions.
   Example: for rare earth restrictions, use web_search to distinguish which
   elements are ALREADY under export control (e.g., neodymium, dysprosium) vs.
   NOT YET restricted (e.g., terbium, samarium), then predict which materials
   are likely to be restricted next, with reasoning.

3. Explain causality through a concrete chain of "who / what / by when."
   Do not end with vague words like "weakened" or "of concern" -- specify which
   policy, which actor, and over what time frame (months) the change will occur.

4. Do not stop at an obvious first-order effect ("supplier sales will decline").
   Add a second-order or counter-intuitive angle.
   Example: for a large-scale layoff, assess whether that country's government
   can stay politically silent, and -- based on historical precedent (e.g., how
   governments responded to past automotive scandals/crises) -- predict what
   intervention, support, or regulatory tightening might follow.

5. Use the web_search tool proactively and ground the analysis in primary
   sources (government agencies, regulators, original reporting from major
   media). Avoid speculation that was never checked against a search.

[OUTPUT LENGTH CONSTRAINTS]
- Up to the top 5 items by relevance (drop lower-importance items if there are
  too many)
- Keep verified_facts and deep_analysis to about 2-3 sentences each, concise
  (avoid verbosity so the response fits within the output token budget)

[OUTPUT FORMAT] The final answer must be JSON only (after any web_search calls,
state it in the final text), with ALL field values written in English:
{
  "date": "Month D, YYYY",
  "items": [
    {
      "news_title": "News headline (concise)",
      "news_summary": "Summary of the news (2-3 sentences)",
      "entities": ["company/organization names (be specific)"],
      "connection_chain": [
        "company/event in the news",
        "intermediate link (fact verified via web_search)",
        "point of contact with Toyota/the auto industry"
      ],
      "verified_facts": "Specific facts verified via web_search (ship names, company names, regulated material names, etc. State clearly if verification was not possible)",
      "deep_analysis": "Analysis via a concrete who/what/by-when chain, plus a second-order angle (2-3 sentences)",
      "relevance": 8,
      "relevance_label": "Direct connection",
      "implication": "Implication for the auto industry/Toyota (1 sentence)"
    }
  ],
  "no_news_today": false
}"""


def analyze_toyota_connections(news_text: str) -> dict:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    msg = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 12,
        }],
        messages=[{
            "role": "user",
            "content": (
                f"Here is today's ({DATE_EN}) news data (in Japanese). "
                "Analyze its connection to Toyota / the Japanese automotive industry in depth, "
                "verifying primary sources with web_search. "
                "Do not guess at numbers, company lists, or regulated items -- verify them via search. "
                "Write the entire output in English:\n\n"
                + news_text
            )
        }],
    )

    print(f"  [stop_reason: {msg.stop_reason}, web_search使用回数: "
          f"{sum(1 for b in msg.content if getattr(b, 'type', '') == 'server_tool_use')}]")

    text_blocks = [b.text for b in msg.content if getattr(b, "type", "") == "text"]
    print(f"  [text_blocks: {len(text_blocks)}個, 各長さ: {[len(t) for t in text_blocks]}]")
    raw_all = "\n".join(text_blocks)
    raw_all = re.sub(r"```[a-z]*\n?", "", raw_all)
    raw_all = raw_all.replace("```", "")

    # 最後に出現する { から最後の } までを候補にする（複数JSON断片混在対策）
    starts = [i for i, c in enumerate(raw_all) if c == "{"]
    ends   = [i for i, c in enumerate(raw_all) if c == "}"]
    if not starts or not ends:
        print(f"  [WARN] JSON not found in response: {raw_all[-300:]}")
        return {"date": DATE_JP, "items": [], "no_news_today": True}

    candidate = raw_all[starts[0]:ends[-1] + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        print(f"  [WARN] JSON parse error: {e}")
        print(f"  [DEBUG] candidate tail: {candidate[max(0, e.pos-150):e.pos+50]}")
        return {"date": DATE_JP, "items": [], "no_news_today": True}


# ══════════════════════════════════════════════════════════════
#  STEP 3: PDF 生成
# ══════════════════════════════════════════════════════════════
SCORE_COLOR = {
    range(7, 11): colors.HexColor("#c0392b"),  # 直接関連 → 赤系
    range(4, 7):  colors.HexColor("#e67e22"),  # 間接関連 → オレンジ
    range(1, 4):  colors.HexColor("#2980b9"),  # 弱い関連 → 青
}

def relevance_color(score: int):
    for rng, col in SCORE_COLOR.items():
        if score in rng:
            return col
    return colors.black


def make_pdf(result: dict, output: Path):
    BLK = colors.black
    GRY = colors.HexColor("#555555")
    items = result.get("items", [])
    no_news = result.get("no_news_today", False) or len(items) == 0

    def S(name, **kw):
        base = dict(fontName="JPN", fontSize=10.5, leading=18,
                    textColor=BLK, spaceAfter=0, spaceBefore=0)
        base.update(kw)
        return ParagraphStyle(name, **base)

    S_TITLE  = S("title", fontName="JPN-B", fontSize=15, alignment=TA_CENTER)
    S_META   = S("meta",  fontSize=12, textColor=GRY, alignment=TA_CENTER)
    S_H      = S("h",     fontName="JPN-B", fontSize=11.5, leading=20)
    S_BODY   = S("body",  fontSize=10.5, leading=18, alignment=TA_JUSTIFY)
    S_CHAIN  = S("chain", fontSize=10, leading=16, textColor=colors.HexColor("#2c3e50"))
    S_FACT   = S("fact",  fontSize=9.5, leading=15, textColor=colors.HexColor("#6b4f00"))
    S_DEEP   = S("deep",  fontSize=10, leading=17, alignment=TA_JUSTIFY)
    S_IMP    = S("imp",   fontSize=10, leading=16, textColor=colors.HexColor("#1a6a1a"),
                 fontName="JPN-B")
    S_NONE   = S("none",  fontSize=12, alignment=TA_CENTER, textColor=GRY)

    doc = SimpleDocTemplate(
        str(output), pagesize=A4,
        topMargin=12*mm, bottomMargin=14*mm,
        leftMargin=22*mm, rightMargin=22*mm,
        title=f"Toyota & Japan Auto Industry Watch {TODAY.strftime('%Y-%m-%d')}",
        author="World News Auto Watch",
    )

    story = []
    story.append(Paragraph("Toyota &amp; Japan Auto Industry Watch", S_TITLE))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(DATE_EN, S_META))
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=2.5, color=BLK))
    story.append(Spacer(1, 6*mm))

    if no_news:
        story.append(Spacer(1, 20*mm))
        story.append(Paragraph("No news related to Toyota or the Japanese automotive industry today.", S_NONE))
    else:
        for i, item in enumerate(items):
            score    = item.get("relevance", 5)
            label    = item.get("relevance_label", "")
            title    = item.get("news_title", "")
            summary  = item.get("news_summary", "")
            entities = ", ".join(item.get("entities", []))
            chain    = item.get("connection_chain", [])
            facts    = item.get("verified_facts", "")
            deep     = item.get("deep_analysis", "")
            impl     = item.get("implication", "")
            col      = relevance_color(score)

            chain_text = "  ->  ".join(chain) if chain else ""

            parts = [
                HRFlowable(width="100%", thickness=1.2, color=col, spaceAfter=2*mm),
                Paragraph(
                    f'<font color="#{col.hexval()[2:]}"><b>[Relevance {score} - {label}]</b></font>  {title}',
                    S_H
                ),
                Spacer(1, 2*mm),
                Paragraph(summary, S_BODY),
                Spacer(1, 2*mm),
                Paragraph(f"<b>Related companies/orgs:</b> {entities}", S_BODY),
                Spacer(1, 1.5*mm),
                Paragraph(f"<b>Connection chain:</b> {chain_text}", S_CHAIN),
            ]
            if facts:
                parts += [Spacer(1, 1.5*mm), Paragraph(f"<b>Verified facts:</b> {facts}", S_FACT)]
            if deep:
                parts += [Spacer(1, 1.5*mm), Paragraph(f"<b>Deep analysis:</b> {deep}", S_DEEP)]
            parts += [Spacer(1, 1.5*mm), Paragraph(f"&#9656; {impl}", S_IMP)]

            block = KeepTogether(parts)
            story.append(block)
            if i < len(items) - 1:
                story.append(Spacer(1, 8*mm))

    story.append(Spacer(1, 5*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLK))

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("JPN", 10)
        canvas.drawRightString(A4[0] - 22*mm, 8*mm, "— END —")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


# ══════════════════════════════════════════════════════════════
#  STEP 4: メール送信（任意）
# ══════════════════════════════════════════════════════════════
def send_email(pdf_path: Path, items_count: int):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print("  メール設定なし → スキップ")
        return

    subject = (
        f"[Auto Watch] {DATE_EN} - "
        + (f"{items_count} related item(s)" if items_count > 0 else "Nothing today")
    )
    body = (
        f"Toyota & Japan Auto Industry Watch - {DATE_EN}\n\n"
        + (f"Found {items_count} related news item(s) today.\nPlease see the attached PDF for details."
           if items_count > 0
           else "No news related to Toyota or the Japanese automotive industry today.")
    )

    msg = MIMEMultipart()
    msg["From"]    = SMTP_USER
    msg["To"]      = WATCH_MAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{pdf_path.name}"')
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, WATCH_MAIL_TO, msg.as_string())
        print(f"  メール送信完了 → {WATCH_MAIL_TO}")
    except Exception as e:
        print(f"  [WARN] メール送信失敗: {e}")


# ══════════════════════════════════════════════════════════════
#  メイン
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{TODAY.strftime('%Y-%m-%d %H:%M')} JST] トヨタウォッチ開始")

    WATCH_DIR.mkdir(parents=True, exist_ok=True)

    print("  ニュースデータ読み込み...")
    news_text = build_news_text()

    print("  Claude API 分析中...")
    result = analyze_toyota_connections(news_text)

    items = result.get("items", [])
    print(f"  関連ニュース: {len(items)}件")
    for it in items:
        print(f"    [{it.get('relevance',0)}] {it.get('news_title','')}")
        chain = it.get("connection_chain", [])
        if chain:
            print(f"         接続: {' → '.join(chain)}")

    print(f"  PDF生成: {OUTPUT_PDF}")
    make_pdf(result, OUTPUT_PDF)

    print("  メール送信...")
    send_email(OUTPUT_PDF, len(items))

    print(f"完了: {OUTPUT_PDF}")
