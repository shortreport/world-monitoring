#!/usr/bin/env python3
"""
make_en_midterm.py
Translates docs/midterm.html (Japanese) → docs/en/midterm.html (English).
Uses Claude Haiku to translate analysis paragraphs.
"""

import re
import os
import anthropic

try:
    from api_config import ANTHROPIC_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

MODEL = "claude-haiku-4-5-20251001"

# ── Helper: detect Japanese characters ──────────────────────────────────────
def has_japanese(text):
    return bool(re.search(r'[぀-ゟ゠-ヿ一-鿿]', text))

# ── Translate a batch of texts with Haiku ────────────────────────────────────
def translate_batch(texts, client):
    if not texts:
        return []
    sep = "\n|||NEXT|||\n"
    joined = sep.join(texts)
    msg = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        messages=[{
            "role": "user",
            "content": (
                "Translate the following Japanese HTML text fragments to English. "
                "Keep all HTML tags, CSS, and attribute names unchanged. "
                "Translate Japanese candidate names to their common English equivalents. "
                "Each fragment is separated by |||NEXT|||. "
                "Return the translated fragments in the same order separated by |||NEXT|||. "
                "Do not add commentary or numbering.\n\n"
                + joined
            )
        }]
    )
    result = msg.content[0].text.strip()
    parts = result.split("|||NEXT|||")
    # Pad if Haiku returned fewer items
    while len(parts) < len(texts):
        parts.append(texts[len(parts)])
    return parts[:len(texts)]

# ── Master replacement list ──────────────────────────────────────────────────
REPLACEMENTS = [
    # ── HTML head ──
    ('<html lang="ja">', '<html lang="en">'),
    ('<title>米国中間選挙 | World News</title>', '<title>US Midterms | World News</title>'),
    (
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">\n',
        ''
    ),
    (
        "font-family: 'Noto Sans JP', -apple-system, 'Hiragino Sans', 'Yu Gothic UI', sans-serif;",
        "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;"
    ),
    ("font-family=\"'Noto Sans JP', sans-serif\"", 'font-family="sans-serif"'),

    # ── Header ──
    ("onclick=\"location.href='index.html'\" title=\"ホームへ\"",
     "onclick=\"location.href='../index.html'\""),
    ('2026年06月25日', 'June 25, 2026'),

    # ── Nav links (relative paths for en/ subdirectory) ──
    ('href="index.html"', 'href="../index.html"'),
    ('href="mail.html"', 'href="intelligence.html"'),
    ('href="trump.html"', 'href="trump.html"'),
    ('href="theme.html"', 'href="theme.html"'),
    ('href="midterm.html" class="active"', 'href="midterm.html" class="active"'),
    ('href="midterm.html"', 'href="../midterm.html"'),
    ('href="summary.html"', 'href="../summary.html"'),

    # ── Nav labels ──
    ('>ホーム<', '>Home<'),
    ('>メール要約<', '>Intelligence<'),
    ('>USトランプ<', '>US Trump<'),
    ('>個別テーマ<', '>Themes<'),
    ('>米国中間選挙<', '>US Midterms<'),
    ('>エグゼクティブ・サマリー<', '>Exec Summary<'),

    # ── Section label ──
    ('>2026年 米国中間選挙マップ<', '>2026 US Midterms Map<'),

    # ── Chamber tabs (keep subtitle small but translate) ──
    ('>上院<br><small style="font-weight:400;font-size:10px;">Senate</small><',
     '>Senate<'),
    ('>下院<br><small style="font-weight:400;font-size:10px;">House</small><',
     '>House<'),
    ('>知事<br><small style="font-weight:400;font-size:10px;">Governor</small><',
     '>Governor<'),

    # ── Map ──
    ('>地図を読み込み中...</text>', '>Loading map...</text>'),
    ("'地図の読み込みに失敗しました'", "'Failed to load map'"),
    ('>地図の読み込みに失敗しました<', '>Failed to load map<'),
    ('id="map-title">上院 — 州別議席勢力図（2026年時点）',
     'id="map-title">Senate — Party Control by State (2026)'),

    # ── Map legend ──
    ('>共和党</div>',   '>Republican</div>'),
    ('>民主党</div>',   '>Democrat</div>'),
    ('>分裂</div>',     '>Split</div>'),
    ('>未確定</div>',   '>Undecided</div>'),
    ('>共和党知事</div>', '>Republican Governor</div>'),
    ('>民主党知事</div>', '>Democrat Governor</div>'),

    # ── State-info placeholder ──
    ('>州をクリックすると詳細を表示します<', '>Click a state for details<'),

    # ── Sidebar ──
    ('>🏛️ 議席数<', '>🏛️ Seats<'),
    ('>上院（Senate） 定数100<', '>Senate — 100 Seats<'),
    ('共和党 (R)', 'Republican (R)'),
    ('民主党 (D/I)', 'Democrat (D/I)'),
    ('>定数<', '>Total<'),
    ('▶ 2026年中間選挙 予測（Cook Political Report 参考）',
     '▶ 2026 Midterms Projections (ref. Cook Political Report)'),
    ("'過半数: 51'", "'Majority: 51'"),
    ('>過半数: 51<', '>Majority: 51<'),
    ('過半数: 51', 'Majority: 51'),
    ('>🗓 今後8週間のスケジュール<', '>🗓 Next 8 Weeks Schedule<'),
    ('>注目レース — 上院2026<', '>Key Races — Senate 2026<'),

    # ── Footer ──
    ('データ出典: Cook Political Report / 270toWin 参考 &nbsp;|&nbsp; 更新: 2026-06-25',
     'Data: Cook Political Report / 270toWin &nbsp;|&nbsp; Updated: 2026-06-25'),

    # ── JS: pred labels ──
    ("'過半数ライン'", "'Majority'"),
    ("過半数ライン", "Majority"),
    ("`D: ${d}${toss > 0 ? `　不確: ${toss}` : ''}`",
     "`D: ${d}${toss > 0 ? `  Toss-up: ${toss}` : ''}`"),
    ("不確 2", "Toss-up: 2"),

    # ── JS: titles/labels ──
    ("{ senate:'注目レース — 上院2026', house:'注目レース — 下院2026', governor:'注目知事選2026' }",
     "{ senate:'Key Races — Senate 2026', house:'Key Races — House 2026', governor:'Key Governor Races 2026' }"),
    ("senate:   '上院（Senate） 定数100 / 過半数51'",
     "senate:   'Senate — 100 Seats / Majority: 51'"),
    ("house:    '下院（House）  定数435 / 過半数218'",
     "house:    'House — 435 Seats / Majority: 218'"),
    ("governor: '知事（Governor）50州'",
     "governor: 'Governor — 50 States'"),
    ("senate:   '上院 — 州別議席勢力図（2026年時点）'",
     "senate:   'Senate — Party Control by State (2026)'"),
    ("house:    '下院 — 州別代表団勢力図（2026年時点）'",
     "house:    'House — Delegation Control by State (2026)'"),
    ("governor: '知事 — 州別政党（2026年時点）'",
     "governor: 'Governor — Party by State (2026)'"),

    # ── JS: stateData ──
    ("seats:['（連邦議会議員なし）']", "seats:['(No congressional senators)']"),

    # ── JS: keyRaces ──
    ("incumbent:'(R空席)'", "incumbent:'(R, Open)'"),
    ("incumbent:'(空席)'",  "incumbent:'(Open)'"),
    ("incumbent:'(D空席)'", "incumbent:'(D, Open)'"),
    ("label:'接戦'",        "label:'Toss-up'"),
    ("任期終",              "Term Ends"),

    # ── JS: HIGHLIGHT_STATES ──
    ("{ ja: 'テキサス州' }",         "{ en: 'Texas' }"),
    ("{ ja: 'ケンタッキー州' }",     "{ en: 'Kentucky' }"),
    ("{ ja: 'インディアナ州' }",     "{ en: 'Indiana' }"),
    ("{ ja: 'ミシシッピ州' }",       "{ en: 'Mississippi' }"),
    ("{ ja: 'ウェスト\\nバージニア州' }", "{ en: 'West\\nVirginia' }"),
    ("{ ja: 'ミズーリ州' }",         "{ en: 'Missouri' }"),
    ("{ ja: 'テネシー州' }",         "{ en: 'Tennessee' }"),
    ("{ ja: 'ミシガン州' }",         "{ en: 'Michigan' }"),
    ("{ ja: 'カリフォルニア州' }",   "{ en: 'California' }"),
    ("{ ja: 'アラバマ州' }",         "{ en: 'Alabama' }"),
    ("{ ja: 'ノース\\nカロライナ州' }", "{ en: 'North\\nCarolina' }"),
    ("info.ja.split", "info.en.split"),

    # ── JS: upcoming empty message ──
    ("'直近8週間に予定なし'",
     "'No events in the next 8 weeks'"),

    # ── JS: showStateInfo stateNames ──
    ("AL:'アラバマ'", "AL:'Alabama'"),
    ("AK:'アラスカ'", "AK:'Alaska'"),
    ("AZ:'アリゾナ'", "AZ:'Arizona'"),
    ("AR:'アーカンソー'", "AR:'Arkansas'"),
    ("CA:'カリフォルニア'", "CA:'California'"),
    ("CO:'コロラド'", "CO:'Colorado'"),
    ("CT:'コネチカット'", "CT:'Connecticut'"),
    ("DE:'デラウェア'", "DE:'Delaware'"),
    ("FL:'フロリダ'", "FL:'Florida'"),
    ("GA:'ジョージア'", "GA:'Georgia'"),
    ("HI:'ハワイ'", "HI:'Hawaii'"),
    ("ID:'アイダホ'", "ID:'Idaho'"),
    ("IL:'イリノイ'", "IL:'Illinois'"),
    ("IN:'インディアナ'", "IN:'Indiana'"),
    ("IA:'アイオワ'", "IA:'Iowa'"),
    ("KS:'カンザス'", "KS:'Kansas'"),
    ("KY:'ケンタッキー'", "KY:'Kentucky'"),
    ("LA:'ルイジアナ'", "LA:'Louisiana'"),
    ("ME:'メイン'", "ME:'Maine'"),
    ("MD:'メリーランド'", "MD:'Maryland'"),
    ("MA:'マサチューセッツ'", "MA:'Massachusetts'"),
    ("MI:'ミシガン'", "MI:'Michigan'"),
    ("MN:'ミネソタ'", "MN:'Minnesota'"),
    ("MS:'ミシシッピ'", "MS:'Mississippi'"),
    ("MO:'ミズーリ'", "MO:'Missouri'"),
    ("MT:'モンタナ'", "MT:'Montana'"),
    ("NE:'ネブラスカ'", "NE:'Nebraska'"),
    ("NV:'ネバダ'", "NV:'Nevada'"),
    ("NH:'ニューハンプシャー'", "NH:'New Hampshire'"),
    ("NJ:'ニュージャージー'", "NJ:'New Jersey'"),
    ("NM:'ニューメキシコ'", "NM:'New Mexico'"),
    ("NY:'ニューヨーク'", "NY:'New York'"),
    ("NC:'ノースカロライナ'", "NC:'North Carolina'"),
    ("ND:'ノースダコタ'", "ND:'North Dakota'"),
    ("OH:'オハイオ'", "OH:'Ohio'"),
    ("OK:'オクラホマ'", "OK:'Oklahoma'"),
    ("OR:'オレゴン'", "OR:'Oregon'"),
    ("PA:'ペンシルベニア'", "PA:'Pennsylvania'"),
    ("RI:'ロードアイランド'", "RI:'Rhode Island'"),
    ("SC:'サウスカロライナ'", "SC:'South Carolina'"),
    ("SD:'サウスダコタ'", "SD:'South Dakota'"),
    ("TN:'テネシー'", "TN:'Tennessee'"),
    ("TX:'テキサス'", "TX:'Texas'"),
    ("UT:'ユタ'", "UT:'Utah'"),
    ("VT:'バーモント'", "VT:'Vermont'"),
    ("VA:'バージニア'", "VA:'Virginia'"),
    ("WA:'ワシントン'", "WA:'Washington'"),
    ("WV:'ウェストバージニア'", "WV:'West Virginia'"),
    ("WI:'ウィスコンシン'", "WI:'Wisconsin'"),
    ("WY:'ワイオミング'", "WY:'Wyoming'"),
    ("DC:'コロンビア特別区'", "DC:'Washington D.C.'"),

    # ── JS: showStateInfo fallback labels ──
    ("'共和党 独占'", "'Republican Hold'"),
    ("'民主党 独占'", "'Democrat Hold'"),
    ("'2026年改選'", "'Up in 2026'"),
    ("'共和党 多数'", "'Republican Majority'"),
    ("'民主党 多数'", "'Democrat Majority'"),
    ("'共和党知事'", "'Republican Governor'"),
    ("'民主党知事'", "'Democrat Governor'"),
    ("'不明'", "'Unknown'"),
    ("下院代表団の多数派政党を表示しています。",
     "Showing the majority party of this state's House delegation."),

    # ── Helper functions ──
    # _seatsTable
    ('>現状の議席</h4>',  '>Current Seats</h4>'),
    ('>議員</th>',        '>Senator</th>'),
    ('>次回改選</th>',    '>Up for Election</th>'),
    # _sched
    ('>今後の選挙スケジュール</h4>', '>Election Schedule</h4>'),
    ('>日付</th>',   '>Date</th>'),
    ('>イベント</th>', '>Event</th>'),
    ('>状況</th>',   '>Status</th>'),
    ("'← 今後'",    "'← Upcoming'"),
    ('← 今後',      '← Upcoming'),
    # _pollTable
    ('>候補者</th>', '>Candidate</th>'),
    ('>支持率</th>', '>Poll %</th>'),

    # ── Common STATE_DETAIL table headers ──
    ('>予想</th>',   '>Projection</th>'),
    ('>議席</th>',   '>Seats</th>'),
    ('>選挙区</th>', '>District</th>'),
    ('>現職</th>',   '>Incumbent</th>'),
    ('>得票率</th>', '>Vote %</th>'),
    ('>結果</th>',   '>Result</th>'),
    ('>3月予備選</th>', '>March Primary</th>'),
    ('>5月ランオフ</th>', '>May Runoff</th>'),
    ('>議席数</th>', '>Seats</th>'),
    ('>備考</th>',   '>Notes</th>'),
    ('>区分</th>',   '>Category</th>'),
    ('>役職</th>',   '>Role</th>'),
    ('>氏名</th>',   '>Name</th>'),
    ('>所属</th>',   '>Affiliation</th>'),
    ('>選挙制度</th>', '>Electoral System</th>'),
    ('>内容</th>',   '>Details</th>'),
    ('>知事</th>',   '>Governor</th>'),
    ('>就任</th>',   '>Since</th>'),
    ('>任期</th>',   '>Term</th>'),
    ('>次回選挙</th>', '>Next Election</th>'),

    # ── Common section headers (h4) ──
    ('>分析</h4>',             '>Analysis</h4>'),
    ('>注目点</h4>',           '>Key Points</h4>'),
    ('>予備選の経緯</h4>',     '>Primary Race</h4>'),
    ('>予想レーティング</h4>', '>Rating</h4>'),
    ('>見通し</h4>',           '>Outlook</h4>'),
    ('>注目選挙区</h4>',       '>Key Races</h4>'),
    ('>現状の議席（',          '>Current Seats ('),
    ('>各党の候補者状況（',    '>Candidates by Party ('),
    ('>各党の候補者状況</h4>', '>Candidates by Party</h4>'),
    ('>2026年議席予想（',      '>2026 Seat Projections ('),
    ('>現職知事</h4>',         '>Current Governor</h4>'),

    # ── Common table cell content ──
    ('>共和党</td>', '>Republican</td>'),
    ('>民主党</td>', '>Democrat</td>'),
    ('>R 共和党<',  '>R Republican<'),
    ('>D 民主党<',  '>D Democrat<'),
    ('安全R',        'Safe R'),
    ('R優位',        'Lean R'),
    ('D優位',        'Lean D'),
    ('安全D',        'Safe D'),
    ('接戦',         'Toss-up'),
    ('落選',         'Lost'),
    ('現状維持',     'No change'),
    ('空席',         'Open Seat'),
    ('多数党',       'Majority'),
    ('少数党',       'Minority'),
    ('>議長<',       '>Speaker<'),
    ('>院内総務<',   '>Leader<'),
    ('>院内幹事<',   '>Whip<'),
    ('>仮議長<',     '>Pro Tempore<'),
    ('>上院仮議長<', '>President Pro Tempore<'),
    ('>議長（副大統領）<', '>President (VP)<'),

    # ── getDefaultPanel: House ──
    ('>無所属<',  '>Ind.<'),
    ('>欠員<',    '>Vacant<'),
    ('>議席数<',  '>Seats<'),
    ('>現在の議席<', '>Current Seats<'),
    ('>2026年改選<', '>Up in 2026<'),
    ('>2028年改選<', '>Up in 2028<'),
    ('>2030年改選<', '>Up in 2030<'),
    ('(*) 無所属議員（バーニー・サンダース、アンガス・キング）は民主党と投票を共にする',
     '(*) Independent senators (Bernie Sanders, Angus King) caucus with Democrats'),
    ('無所属(*)', 'Independent(*)'),
    ('435（人口分布に応じて各州に配分）',
     '435 (distributed to states by population)'),
    ('国勢調査に基づき人口比で州ごとに配分。州権限で小選挙区の区割りを決定',
     'Apportioned to states by census population. Each state draws its own district boundaries.'),
    ('2年（全435議席を改選）。大統領選と重ならない年の選挙を中間選挙と呼ぶ',
     '2-year terms (all 435 seats). Elections not coinciding with presidential elections are called midterms.'),
    ('州をクリックすると代表団の詳細を表示します',
     'Click a state for delegation details'),
    # Senate
    ('100', '100'),
    ('各州に2議席配分（人口に関わらず均等）',
     '2 seats per state regardless of population'),
    ('6年。2年ごとに議席の3分の1ずつ改選。大統領選挙と重ならない年の選挙を中間選挙と呼ぶ',
     '6-year terms. One-third of seats up every 2 years. Elections not coinciding with presidential elections are called midterms.'),
    ('>同数時の決裁<', '>Tie-breaking<'),
    ('50対50の場合、バンス副大統領（共和党）が投票に参加し決裁',
     'In a 50-50 tie, VP Vance (R) casts the deciding vote'),
    ('>フィリバスター<', '>Filibuster<'),
    ('本会議採決前に発言を続けて採決を引き延ばす議事妨害戦術。阻止するには60議席が必要',
     'A tactic to delay a vote by extended debate. Requires 60 votes to overcome.'),
    ('州をクリックすると選挙情報を表示します',
     'Click a state for election information'),

    # ── STATE_DETAIL: state name headers ──
    # Senate
    ('テキサス州（TX） — 2026年上院選挙あり', 'Texas (TX) — 2026 Senate Election'),
    ('ケンタッキー州（KY） — 2026年上院選挙あり', 'Kentucky (KY) — 2026 Senate Election'),
    ('ミシガン州（MI） — 2026年上院選挙あり', 'Michigan (MI) — 2026 Senate Election'),
    ('テネシー州（TN） — 2026年上院選挙あり', 'Tennessee (TN) — 2026 Senate Election'),
    ('ウェストバージニア州（WV） — 2026年上院選挙あり', 'West Virginia (WV) — 2026 Senate Election'),
    ('ミズーリ州（MO） — 上院選挙なし', 'Missouri (MO) — No Senate Election'),
    ('ミシシッピ州（MS） — 2026年上院選挙あり', 'Mississippi (MS) — 2026 Senate Election'),
    ('インディアナ州（IN） — 2026年上院選挙あり', 'Indiana (IN) — 2026 Senate Election'),
    ('ジョージア州（GA） — 2026年上院選挙あり', 'Georgia (GA) — 2026 Senate Election'),
    ('オハイオ州（OH） — 2026年上院選挙あり', 'Ohio (OH) — 2026 Senate Election'),
    # House
    ('テキサス州（TX） — 2026年下院選挙', 'Texas (TX) — 2026 House Election'),
    ('ケンタッキー州（KY） — 2026年下院選挙', 'Kentucky (KY) — 2026 House Election'),
    ('インディアナ州（IN） — 2026年下院選挙', 'Indiana (IN) — 2026 House Election'),
    ('ミシシッピ州（MS） — 2026年下院選挙', 'Mississippi (MS) — 2026 House Election'),
    ('ウェストバージニア州（WV） — 2026年下院選挙', 'West Virginia (WV) — 2026 House Election'),
    ('ミズーリ州（MO） — 2026年下院選挙', 'Missouri (MO) — 2026 House Election'),
    ('テネシー州（TN） — 2026年下院選挙', 'Tennessee (TN) — 2026 House Election'),
    ('ミシガン州（MI） — 2026年下院選挙', 'Michigan (MI) — 2026 House Election'),
    ('カリフォルニア州（CA） — 2026年下院選挙', 'California (CA) — 2026 House Election'),
    ('アラバマ州（AL） — 2026年下院選挙', 'Alabama (AL) — 2026 House Election'),
    ('ノースカロライナ州（NC） — 2026年下院選挙', 'North Carolina (NC) — 2026 House Election'),
    ('フロリダ州（FL） — 2026年下院選挙', 'Florida (FL) — 2026 House Election'),
    ('ニューヨーク州（NY） — 2026年下院選挙', 'New York (NY) — 2026 House Election'),
    ('ペンシルベニア州（PA） — 2026年下院選挙', 'Pennsylvania (PA) — 2026 House Election'),
    ('オハイオ州（OH） — 2026年下院選挙', 'Ohio (OH) — 2026 House Election'),
    ('ジョージア州（GA） — 2026年下院選挙', 'Georgia (GA) — 2026 House Election'),
    ('アリゾナ州（AZ） — 2026年下院選挙', 'Arizona (AZ) — 2026 House Election'),
    ('バージニア州（VA） — 2026年下院選挙', 'Virginia (VA) — 2026 House Election'),
    ('ネバダ州（NV） — 2026年下院選挙', 'Nevada (NV) — 2026 House Election'),
    ('コロラド州（CO） — 2026年下院選挙', 'Colorado (CO) — 2026 House Election'),
    ('ニューメキシコ州（NM） — 2026年下院選挙', 'New Mexico (NM) — 2026 House Election'),
    # Governor
    ('フロリダ州（FL） — 2026年知事選挙', 'Florida (FL) — 2026 Governor\'s Race'),
    ('テキサス州（TX） — 2026年知事選挙', 'Texas (TX) — 2026 Governor\'s Race'),
    ('イリノイ州（IL） — 2026年知事選挙', 'Illinois (IL) — 2026 Governor\'s Race'),
    ('ニューヨーク州（NY） — 2026年知事選挙', 'New York (NY) — 2026 Governor\'s Race'),
    ('ジョージア州（GA） — 2026年知事選挙', 'Georgia (GA) — 2026 Governor\'s Race'),
    ('ウィスコンシン州（WI） — 2026年知事選挙', 'Wisconsin (WI) — 2026 Governor\'s Race'),
    ('ペンシルベニア州（PA） — 2026年知事選挙', 'Pennsylvania (PA) — 2026 Governor\'s Race'),
    ('メリーランド州（MD） — 2026年知事選挙', 'Maryland (MD) — 2026 Governor\'s Race'),
    ('ルイジアナ州（LA） — 2026年知事選なし', 'Louisiana (LA) — No 2026 Governor\'s Race'),
    ('モンタナ州（MT） — 2026年知事選なし', 'Montana (MT) — No 2026 Governor\'s Race'),
    ('ノースダコタ州（ND） — 2026年知事選なし', 'North Dakota (ND) — No 2026 Governor\'s Race'),
    ('ニュージャージー州（NJ） — 2026年知事選なし', 'New Jersey (NJ) — No 2026 Governor\'s Race'),
    ('ユタ州（UT） — 2026年知事選なし', 'Utah (UT) — No 2026 Governor\'s Race'),
    ('バージニア州（VA） — 2026年知事選なし', 'Virginia (VA) — No 2026 Governor\'s Race'),
    ('ワシントン州（WA） — 2026年知事選なし', 'Washington (WA) — No 2026 Governor\'s Race'),
    ('デラウェア州（DE） — 2026年知事選なし', 'Delaware (DE) — No 2026 Governor\'s Race'),

    # ── Prediction labels ──
    ('予想結果：', 'Projected: '),
    ('※ 予備的な評価。', '* Preliminary projection.'),
    ('評価：共和党優位', 'Rating: Republican Favored'),
    ('評価：民主党優位', 'Rating: Democrat Favored'),
    ('評価：民主党ごく僅かに優位', 'Rating: Slight Democrat Edge'),
    ('評価：共和党僅かに優位', 'Rating: Slight Republican Edge'),
    ('評価：民主党安全圏（Safe D）', 'Rating: Safe D'),
    ('評価：共和党安全圏（Safe R）', 'Rating: Safe R'),
    ('評価：', 'Rating: '),

    # ── Schedule patterns ──
    ('予備選（両党）', 'Primary (both parties)'),
    ('予備選（共和党）', 'Primary (Republican)'),
    ('予備選（民主党）', 'Primary (Democrat)'),
    ('予備選（無党派一括・上位2名進出・', 'Open Primary (top-2, '),
    ('予備選（RCV・全候補一括）', 'Primary (RCV, all candidates)'),
    ('予備選（RCV・上位4名進出）', 'Primary (RCV, top-4)'),
    ('予備選（オープン・プライマリー）', 'Primary (Open Primary)'),
    ('本選（一般選挙）', 'General Election'),
    ('本選（上位2名対決）', 'General Election (Top-2)'),
    ('予備選決選投票（ランオフ）', 'Primary Runoff'),
    ('予備選ランオフ', 'Primary Runoff'),
    ('予備選（両党）—', 'Primary —'),
    ('民主党予備選', 'Democratic Primary'),
    ('終了', 'Completed'),

    # ── upcomingSchedules dates ──
    ("'7月21日頃（必要時）'", "'~July 21 (if needed)'"),
    ("'8月4日'",  "'Aug 4'"),
    ("'8月6日'",  "'Aug 6'"),
    ("'8月8日'",  "'Aug 8'"),
    ("'8月11日'", "'Aug 11'"),
    ("'8月18日'", "'Aug 18'"),

    # ── upcomingSchedules: state names ──
    ("'ジョージア（GA）'",   "'Georgia (GA)'"),
    ("'ミシガン（MI）'",     "'Michigan (MI)'"),
    ("'カンザス（KS）'",     "'Kansas (KS)'"),
    ("'テネシー（TN）'",     "'Tennessee (TN)'"),
    ("'ミネソタ（MN）'",     "'Minnesota (MN)'"),
    ("'アラスカ（AK）'",     "'Alaska (AK)'"),
    ("'ワイオミング（WY）'", "'Wyoming (WY)'"),
    ("'ミズーリ（MO）'",     "'Missouri (MO)'"),
    ("'アリゾナ（AZ）'",     "'Arizona (AZ)'"),
    ("'ワシントン（WA）'",   "'Washington (WA)'"),
    ("'ハワイ（HI）'",       "'Hawaii (HI)'"),
    ("'コネチカット（CT）'", "'Connecticut (CT)'"),
    ("'ウィスコンシン（WI）'", "'Wisconsin (WI)'"),
    ("'バーモント（VT）'",   "'Vermont (VT)'"),
    ("'フロリダ（FL）'",     "'Florida (FL)'"),

    # ── upcomingSchedules: event strings ──
    ("'上院予備選ランオフ（過半数未達の場合）'",
     "'Senate Primary Runoff (if no majority)'"),
    ("'上院予備選（両党）— G・ピータース D 改選'",
     "'Senate Primary — Gary Peters (D) up for election'"),
    ("'上院予備選（共和党）— J・モラン R 改選'",
     "'Senate Primary (R) — Jerry Moran (R) up for election'"),
    ("'上院予備選（両党）— B・ヘイガティ R 改選'",
     "'Senate Primary — Bill Hagerty (R) up for election'"),
    ("'上院予備選（両党）— T・スミス D 改選'",
     "'Senate Primary — Tina Smith (D) up for election'"),
    ("'上院予備選（RCV・全候補一括）— D・サリバン R 改選'",
     "'Senate Primary (RCV) — Dan Sullivan (R) up for election'"),
    ("'上院予備選（共和党）— 2026年改選'",
     "'Senate Primary (R) — 2026 seat'"),
    ("'下院予備選ランオフ（複数選挙区・過半数未達の場合）'",
     "'House Primary Runoffs (multiple districts, if no majority)'"),
    ("'下院予備選（両党・全13議席）'", "'House Primary (all 13 seats)'"),
    ("'下院予備選（両党・全8議席）'",  "'House Primary (all 8 seats)'"),
    ("'下院予備選（両党・全9議席）'",  "'House Primary (all 9 seats)'"),
    ("'下院予備選（無党派一括・上位2名進出・全10議席）'",
     "'House Primary — Open (top-2, all 10 seats)'"),
    ("'下院予備選（両党・全4議席）'",  "'House Primary (all 4 seats)'"),
    ("'下院予備選（両党・全9議席）'",  "'House Primary (all 9 seats)'"),
    ("'下院予備選（両党・全2議席）'",  "'House Primary (all 2 seats)'"),
    ("'下院予備選（両党・全8議席）'",  "'House Primary (all 8 seats)'"),
    ("'下院予備選（両党・全5議席）'",  "'House Primary (all 5 seats)'"),
    ("'下院予備選（両党・全1議席）'",  "'House Primary (at-large)'"),
    ("'下院予備選（両党・全28議席）'", "'House Primary (all 28 seats)'"),
    ("'下院予備選（RCV・上位4名進出・全1議席）'",
     "'House Primary (RCV top-4, at-large)'"),
    ("'下院予備選（共和党・全1議席）'", "'House Primary (R, at-large)'"),
    ("'知事選予備選ランオフ（オープン席・過半数未達の場合）'",
     "'Governor Primary Runoff (open seat, if no majority)'"),
    ("'知事選予備選（両党）— ホイットマー D 再選挑戦'",
     "'Governor Primary — Whitmer (D) seeking re-election'"),
    ("'知事選予備選（両党）— ホッブス D 再選挑戦'",
     "'Governor Primary — Hobbs (D) seeking re-election'"),
    ("'知事選予備選（両党）— オープン席（ケリー D 任期満了）'",
     "'Governor Primary — Open seat (Kelly D, term-limited)'"),
    ("'知事選予備選（両党）— オープン席（リー R 任期満了）'",
     "'Governor Primary — Open seat (Lee R, term-limited)'"),
    ("'知事選予備選（両党）— グリーン D 再選挑戦'",
     "'Governor Primary — Green (D) seeking re-election'"),
    ("'知事選予備選（両党）— エバース D 再選挑戦'",
     "'Governor Primary — Evers (D) seeking re-election'"),
    ("'知事選予備選（両党）— ウォルズ D 再選挑戦'",
     "'Governor Primary — Walz (D) seeking re-election'"),
    ("'知事選予備選（両党）— ラモント D 再選挑戦'",
     "'Governor Primary — Lamont (D) seeking re-election'"),
    ("'知事選予備選（両党・2年任期）— スコット R 再選挑戦'",
     "'Governor Primary (2-yr term) — Scott (R) seeking re-election'"),
    ("'知事選予備選（両党）— オープン席（デサンティス R 任期満了）'",
     "'Governor Primary — Open seat (DeSantis R, term-limited)'"),
    ("'知事選予備選（RCV・上位4名進出）— ダニリービー R 再選挑戦'",
     "'Governor Primary (RCV top-4) — Dunleavy (R) seeking re-election'"),
    ("'知事選予備選（共和党）— オープン席（ゴードン R 任期満了）'",
     "'Governor Primary (R) — Open seat (Gordon R, term-limited)'"),

    # ── switchChamber JS strings ──
    ("'州をクリックすると詳細を表示します'",
     "'Click a state for details'"),

    # ── Senate senator names (katakana → English) ──
    ('ジョン・コーニン', 'John Cornyn'),
    ('テッド・クルーズ', 'Ted Cruz'),
    ('ミッチ・マコーネル（退任）', 'Mitch McConnell (retiring)'),
    ('マコーネル（退任）', 'McConnell (retiring)'),
    ('ランド・ポール', 'Rand Paul'),
    ('ゲイリー・ピーターズ（退任）', 'Gary Peters (retiring)'),
    ('エリッサ・スロットキン', 'Elissa Slotkin'),
    ('ビル・ハガーティ（現職）', 'Bill Hagerty (incumbent)'),
    ('マーシャ・ブラックバーン', 'Marsha Blackburn'),
    ('シェリー・ムア・カピト（現職）', 'Shelley Moore Capito (incumbent)'),
    ('ジム・ジャスティス', 'Jim Justice'),
    ('マイク・ロジャース', 'Mike Rogers'),
    ('マロリー・マクモロー', 'Mallory McMorrow'),
    ('ヘイリー・スティーヴンス', 'Hailee Stevens'),
    ('アブドゥル・エル=サイード', 'Abdul El-Sayed'),
    ('マルキータ・ブラッドショー', 'Marquita Bradshaw'),
    ('アンディ・バー（下院議員 KY-6）共和', 'Andy Barr (Rep. KY-6) — Republican'),
    ('アンディ・バー（下院議員5期）', 'Andy Barr (5-term Rep.)'),
    ('チャールズ・ブッカー（元下院議員候補）', 'Charles Booker (former House candidate)'),
    ('ダニエル・キャメロン（元司法長官）共和', 'Daniel Cameron (former AG) — Republican'),
    ('チャールズ・ブッカー　民主', 'Charles Booker — Democrat'),
    ('エイミー・マクグラス（元海兵隊員）民主', 'Amy McGrath (former Marine) — Democrat'),
    ('ケン・パクストン（元司法長官・共和）', 'Ken Paxton (former AG — Republican)'),
    ('ジョン・コーニン（現職・共和）', 'John Cornyn (incumbent — Republican)'),
    ('ケン・パクストン', 'Ken Paxton'),
    ('ジェームズ・タラリコ（州議会議員）', 'James Talarico (State Rep.)'),
    ('ジェームズ・タラリコ', 'James Talarico'),
    ('レイチェル・フェッティ・アンダーソン（民主）', 'Rachel Fetty Anderson — Democrat'),
    ('ジェフ・ケスラー（元州上院議長・民主）', 'Jeff Kessler (former State Senate President) — Democrat'),
    ('トム・ウィリス（州上院議員・共和）', 'Tom Willis (State Senator) — Republican'),
    ('シェリー・ムア・カピト（現職・共和）', 'Shelley Moore Capito (incumbent — Republican)'),
    # Katakana candidate name patterns
    ('ビル・ハガーティ現職', 'Bill Hagerty (incumbent)'),
    ('バリー・ムア', 'Barry Moore'),

    # ── Governor candidate names ──
    ('ウェス・ムーア', 'Wes Moore'),
    ('ジェフ・ランドリー', 'Jeff Landry'),
    ('グレッグ・ジャンフォルテ', 'Greg Gianforte'),
    ('ケリー・アームストロング', 'Kelly Armstrong'),
    ('スペンサー・コックス', 'Spencer Cox'),
    ('アビゲイル・スパンバーガー', 'Abigail Spanberger'),
    ('ボブ・ファーガソン', 'Bob Ferguson'),
    ('マット・マイヤー', 'Matt Meyer'),
    ('マイク・ジョンソン', 'Mike Johnson'),
    ('スティーブ・スカリス', 'Steve Scalise'),
    ('トム・エマー', 'Tom Emmer'),
    ('ハキーム・ジェフリーズ', 'Hakeem Jeffries'),
    ('キャサリン・クラーク', 'Katherine Clark'),
    ('J.D.ヴァンス', 'J.D. Vance'),
    ('チャック・グラスリー', 'Chuck Grassley'),
    ('ジョン・スーン', 'John Thune'),
    ('ジョン・バラッソ', 'John Barrasso'),
    ('チャック・シューマー', 'Chuck Schumer'),
    ('ディック・ダービン', 'Dick Durbin'),
    ('2025年11月当選知事', 'Governor elected Nov 2025'),

    # ── Common note patterns ──
    ('Lean R（共和党優位）。世論調査のデータは公表されていない。',
     'Lean R. No detailed poll data available.'),
    ('Safe R（共和党安全）。詳細な世論調査データなし。',
     'Safe R. No detailed poll data available.'),

    # ── House section: governor-no-race note ──
    ('LAは奇数年に知事選を実施（2023・2027年サイクル）。2026年の知事選はなし。',
     'Louisiana holds gubernatorial elections in odd years (2023/2027 cycle). No 2026 governor\'s race.'),
    ('MTは偶数年（2020・2024・2028年）に知事選を実施。2026年の知事選はなし。',
     'Montana holds gubernatorial elections in even years (2020/2024/2028). No 2026 governor\'s race.'),
    ('NDは偶数年（2020・2024・2028年）に知事選を実施。2026年の知事選はなし。',
     'North Dakota holds gubernatorial elections in even years. No 2026 governor\'s race.'),
    ('NJは奇数年に知事選を実施（2021・2025・2029年サイクル）。2026年の知事選はなし。',
     'New Jersey holds gubernatorial elections in odd years (2021/2025/2029 cycle). No 2026 governor\'s race.'),
    ('UTは偶数年（2020・2024・2028年）に知事選を実施。2026年の知事選はなし。',
     'Utah holds gubernatorial elections in even years. No 2026 governor\'s race.'),
    ('VAは奇数年に知事選を実施（2021・2025・2029年サイクル）。知事の連続再選は禁止。2026年の知事選はなし。',
     'Virginia holds gubernatorial elections in odd years (2021/2025/2029 cycle). Governors cannot serve consecutive terms. No 2026 governor\'s race.'),
    ('WAは偶数年（2020・2024・2028年）に知事選を実施。2026年の知事選はなし。',
     'Washington holds gubernatorial elections in even years. No 2026 governor\'s race.'),
    ('DEは偶数年（2020・2024・2028年）に知事選を実施。2026年の知事選はなし。',
     'Delaware holds gubernatorial elections in even years. No 2026 governor\'s race.'),

    # ── House election district notes (small patterns) ──
    ('議席）', ' seats)'),
    ('全議席）', ' seats)'),
    ('（全', '('),
    ('2026年（2002年に当選）', '2026 (elected 2002)'),
    ('2028年（2013年に当選）', '2028 (elected 2013)'),
    ('2026年（2020年に再選）', '2026 (re-elected 2020)'),
    ('2028年（2022年に再選）', '2028 (re-elected 2022)'),
    ('2030年（2024年に当選）', '2030 (elected 2024)'),
    ('2026年（2020年に再選）', '2026 (re-elected 2020)'),
    ('1期目（再選挑戦）', '1st term (seeking re-election)'),
    ('2023年（2022年当選）', '2023 (elected 2022)'),
    ('2021年（2024年再選）', '2021 (re-elected 2024)'),
    ('2025年（2024年当選）', '2025 (elected 2024)'),
    ('2026年1月（2025年11月当選）', 'Jan 2026 (elected Nov 2025)'),
    ('2029年（連続再選は不可）', '2029 (cannot serve consecutive terms)'),
    ('連続再選は不可', 'cannot serve consecutive terms'),
    ('2024年（2023年ジャングル予備選で当選）', '2024 (elected 2023 jungle primary)'),
]

# ── Apply all replacements ───────────────────────────────────────────────────
def apply_replacements(html):
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    return html

# ── Find and translate remaining Japanese text segments ──────────────────────
def translate_remaining_japanese(html, client):
    """
    Find text content between HTML tags that still contains Japanese.
    Batch them and translate via Haiku.
    """
    # Pattern: text between > and < that contains Japanese characters
    # We'll find all such segments, deduplicate, translate, then replace
    pattern = re.compile(
        r'(?<=>)([^<>]*[぀-ゟ゠-ヿ一-鿿][^<>]*)(?=<)',
        re.DOTALL
    )

    # Find all matches (preserving context for replacement)
    all_matches = []
    seen = {}
    for m in pattern.finditer(html):
        text = m.group(1)
        if text.strip() and has_japanese(text):
            if text not in seen:
                seen[text] = None
                all_matches.append(text)

    if not all_matches:
        print("  No remaining Japanese text found.")
        return html

    print(f"  Found {len(all_matches)} unique Japanese segments to translate...")

    # Translate in batches of 20
    BATCH = 20
    translations = {}
    for i in range(0, len(all_matches), BATCH):
        batch = all_matches[i:i+BATCH]
        print(f"  Translating batch {i//BATCH + 1}/{(len(all_matches)+BATCH-1)//BATCH} ({len(batch)} items)...")
        translated = translate_batch(batch, client)
        for orig, trans in zip(batch, translated):
            # Only use if translation looks reasonable (not empty, not same)
            trans = trans.strip()
            if trans and trans != orig:
                translations[orig] = trans

    # Apply translations (longest first to avoid partial matches)
    for orig in sorted(translations.keys(), key=len, reverse=True):
        trans = translations[orig]
        html = html.replace(orig, trans)

    return html

# ── Add JP/EN toggle to nav ──────────────────────────────────────────────────
def add_lang_toggle(html):
    toggle = (
        '\n  <a href="../midterm.html" style="margin-left:auto;border-left:1px solid var(--border);">'
        '<span class="nav-icon">🇯🇵</span>JP</a>\n'
        '  <a href="midterm.html" class="active" style="border-left:1px solid var(--border);">'
        '<span class="nav-icon">🇺🇸</span>EN</a>\n'
    )
    # Insert before closing </nav>
    html = html.replace('</nav>', toggle + '</nav>', 1)
    return html

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("Reading docs/midterm.html...")
    with open("docs/midterm.html", "r", encoding="utf-8") as f:
        html = f.read()

    print("Applying string replacements...")
    html = apply_replacements(html)

    print("Translating remaining Japanese text with Claude Haiku...")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    html = translate_remaining_japanese(html, client)

    print("Adding JP/EN toggle...")
    html = add_lang_toggle(html)

    os.makedirs("docs/en", exist_ok=True)
    out_path = "docs/en/midterm.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Verify
    remaining = re.findall(r'[぀-ゟ゠-ヿ一-鿿]', html)
    print(f"\nDone! Written to {out_path}")
    print(f"Lines: {html.count(chr(10))}")
    print(f"Remaining Japanese characters: {len(remaining)}")
    if remaining and len(remaining) < 200:
        # Show context of remaining Japanese
        for m in re.finditer(r'[^\n]*[぀-ゟ゠-ヿ一-鿿][^\n]*', html):
            print(f"  → {m.group()[:100]}")

if __name__ == "__main__":
    main()
