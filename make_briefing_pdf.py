"""
大統領インテリジェンス・ブリーフィング PDF生成スクリプト（黒のみ・シンプル）
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import KeepTogether

pdfmetrics.registerFont(TTFont('JPN',   r'C:\Windows\Fonts\YuGothM.ttc'))
pdfmetrics.registerFont(TTFont('JPN-B', r'C:\Windows\Fonts\YuGothB.ttc'))

OUTPUT = r"C:\Users\shondo\Desktop\agent_project\docs\briefing_latest.pdf"

BLK = colors.black
GRY = colors.HexColor('#555555')

def S(name, **kw):
    base = dict(fontName='JPN', fontSize=11, leading=20,
                textColor=BLK, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_TITLE  = S('title',  fontName='JPN-B', fontSize=16, alignment=TA_CENTER)
S_META   = S('meta',   fontName='JPN',   fontSize=13, textColor=GRY, alignment=TA_CENTER)
S_LABEL  = S('label',  fontName='JPN-B', fontSize=12, leading=18)
S_SUBLBL = S('sublbl', fontName='JPN',   fontSize=11, leading=18)
S_BODY   = S('body',   fontName='JPN',   fontSize=11, leading=19, alignment=TA_JUSTIFY)

GAP = 14*mm

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    topMargin=11*mm, bottomMargin=13*mm,
    leftMargin=22*mm, rightMargin=22*mm,
    title="エグゼクティブ・ブリーフィング 2026-05-28",
    author="国家情報機関",
)

def section(tag, headline, body):
    return KeepTogether([
        HRFlowable(width="100%", thickness=1.5, color=BLK, spaceAfter=3*mm),
        Paragraph(f'<b>{tag}</b>　{headline}', S_LABEL),
        Spacer(1, 4*mm),
        Paragraph(body, S_BODY),
    ])

story = []

# ─── タイトル ──────────────────────────────────────
story.append(Paragraph("エグゼクティブ・ブリーフィング", S_TITLE))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("2026年5月28日（木）", S_META))
story.append(Spacer(1, 11*mm))
story.append(HRFlowable(width="100%", thickness=3, color=BLK))
story.append(Spacer(1, 6*mm))

# ─── ① Heads up ────────────────────────────────────
story.append(section(
    "【Heads up】",
    "イラン合意の行方が全局面のトリガー",
    "イラン停戦合意の成否（<b>6月末期限</b>）が、原油価格・中東情勢・米中関係の"
    "三つを同時に動かす最大のトリガーです。専門家分析では合意確率65%。"
    "成立なら原油急落・株高継続、決裂なら攻撃再開・原油急騰です。"
))

story.append(Spacer(1, GAP))

# ─── ② 変化済み ────────────────────────────────────
story.append(section(
    "【変化済み】",
    "米中が「競争から安定」へ転換――台湾防衛を事実上棚上げ",
    "トランプ大統領の訪中で貿易・イラン両分野の大型合意が成立。その代償として"
    "台湾向け武器売却<b>14億ドル分を一時停止</b>しました。米中関係の「リセット」は"
    "既成事実となりつつあります。中国の台湾への軍事圧力は継続中であり、"
    "台湾・頼総統は武器供給再開を求めていますが、米側は対応を保留しています。"
))

story.append(Spacer(1, GAP))

# ─── ③ 近く変化 ────────────────────────────────────
story.append(section(
    "【近く変化】",
    "イラン停戦合意が6月末までに成立する確率65%",
    "軍事作戦開始から3か月。成立すれば原油が急落し、株高が継続します。"
    "ただし決裂なら攻撃再開・原油急騰です。"
    "トランプ大統領はホルムズ海峡の通航料をめぐりオマーンへの制裁も示唆しており、"
    "局面は流動的です。"
))

story.append(Spacer(1, GAP))

# ─── ④ 中長期 ──────────────────────────────────────
story.append(section(
    "【中長期】",
    "QUAD空洞化と台湾の防衛力低下リスク",
    "米中デタントの進行により、日米豪印のQUAD体制が形骸化しかねません。"
    "台湾は防衛予算を<b>8年連続で増額（203億ドル）</b>していますが、"
    "米国からの武器補給が止まれば対中抑止力が急速に低下します。"
    "同盟国の米国離れが連鎖する可能性があり、<b>今後6〜12か月が分岐点</b>です。"
))

story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="100%", thickness=1.5, color=BLK))

def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('JPN', 11)
    canvas.drawRightString(A4[0] - 22*mm, 8*mm, "以　　上")
    canvas.restoreState()

doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
print(f"PDF生成完了: {OUTPUT}")

