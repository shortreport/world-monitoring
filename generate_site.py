#!/usr/bin/env python3
"""
World News マルチページサイト生成スクリプト v4
  docs/index.html  ← ホーム
  docs/mail.html   ← メール要約
  docs/trump.html  ← トランプ

変更点 (v4):
  - ホーム・トランプページの箇条書き / タイトルに元データURLを付与
  - クリックで別ウインドウ（target="_blank"）で元ソースを開く
  - 実運用時は各スクリプトから渡される url フィールドを使用

使用法: python generate_site.py
"""

import json
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta, timezone
import html as H

JST        = timezone(timedelta(hours=9))
TODAY      = datetime.now(JST)
YESTERDAY  = TODAY - timedelta(days=1)
DATE_JP    = TODAY.strftime("%Y年%m月%d日")
DATE_RANGE = f"{YESTERDAY.strftime('%Y-%m-%d')} ~ {TODAY.strftime('%Y-%m-%d')}"
TIME_JP    = TODAY.strftime("%H:%M") + " JST"

ECO_RED   = "#C8141E"

# ─────────────────────────────────────────────────────────────
#  URL ビルダー
# ─────────────────────────────────────────────────────────────
def gn(query: str) -> str:
    """Google News 検索URL（英語クエリ推奨・必ず開ける）"""
    return "https://news.google.com/search?q=" + urllib.parse.quote(query) + "&hl=en&gl=US"

def wh(path: str = "") -> str:
    """ホワイトハウス公式サイト"""
    return "https://www.whitehouse.gov/" + path.lstrip("/")

def yt(video_id: str) -> str:
    """YouTube 動画"""
    return f"https://www.youtube.com/watch?v={video_id}"

# ─────────────────────────────────────────────────────────────
#  update_home.py 連携：JSON 読み込み（ホームページ用）
# ─────────────────────────────────────────────────────────────
HOME_JSON_PATH      = Path(__file__).parent / "docs" / "data" / "home_latest.json"
ECONOMIST_JSON_PATH = Path(__file__).parent / "docs" / "data" / "economist_latest.json"
MAIL_JSON_PATH      = Path(__file__).parent / "docs" / "data" / "mail_latest.json"
ROLLING_JSON_PATH   = Path(__file__).parent / "docs" / "data" / "mail_rolling.json"

def load_home_data() -> list | None:
    """
    home_latest.json が存在すれば読み込んで NEWS_ITEMS 形式に変換して返す。
    なければ None を返す（ハードコードにフォールバック）。
    """
    if not HOME_JSON_PATH.exists():
        return None
    try:
        data     = json.loads(HOME_JSON_PATH.read_text(encoding="utf-8"))
        segments = data.get("segments", [])
        if not segments:
            return None
        items = []
        for seg in segments:
            title     = seg.get("title", "")
            search_en = seg.get("search_en", "").strip()

            # タイトルURL: search_en があれば英語 Google News、なければ日本語ロケールで日本語タイトル検索
            if search_en:
                title_url = ("https://news.google.com/search?q="
                             + urllib.parse.quote(search_en) + "&hl=en&gl=US&ceid=US:en")
            else:
                title_url = ("https://news.google.com/search?q="
                             + urllib.parse.quote(title) + "&hl=ja&gl=JP&ceid=JP:ja")

            # bullets: 文字列 or dict → dict（URLつき）に統一
            # 優先順: ① dict.url (記事URL直接) ② search_en (英語GNews) ③ 日本語GNews
            bullets = []
            for b in seg.get("bullets", []):
                if isinstance(b, dict):
                    # URL が空の場合は search_en フォールバック
                    if not b.get("url") and search_en:
                        b = dict(b, url=("https://news.google.com/search?q="
                                         + urllib.parse.quote(search_en)
                                         + "&hl=en&gl=US&ceid=US:en"))
                    bullets.append(b)
                else:
                    if search_en:
                        b_url = ("https://news.google.com/search?q="
                                 + urllib.parse.quote(search_en) + "&hl=en&gl=US&ceid=US:en")
                    else:
                        b_url = ("https://news.google.com/search?q="
                                 + urllib.parse.quote(str(b)[:40]) + "&hl=ja&gl=JP&ceid=JP:ja")
                    bullets.append({
                        "text":   str(b),
                        "source": "News",
                        "url":    b_url,
                    })
            # risk / context から先頭のラベルを除去
            risk = (seg.get("risk", "")
                    .replace("▲リスク【最緊急】：", "")
                    .replace("▲リスク：", ""))
            ctx  = seg.get("context", "").replace("背景：", "")
            items.append({
                "badge":     seg.get("badge", ""),
                "color":     seg.get("color", "CYAN"),
                "title":     title,
                "title_url": title_url,
                "subtitle":  seg.get("subtitle", ""),
                "bullets":   bullets,
                "risk":      risk,
                "context":   ctx,
            })
        gen_at = data.get("generated_at", "")
        print(f"[OK] home_latest.json から {len(items)} 件読み込み（{gen_at}）")
        return items
    except Exception as ex:
        print(f"[WARN] home_latest.json 読み込み失敗: {ex}")
        return None


def load_economist_data() -> dict | None:
    """
    economist_latest.json が存在すれば読み込んで ECONOMIST 形式に変換して返す。
    なければ None を返す（ハードコードにフォールバック）。
    """
    if not ECONOMIST_JSON_PATH.exists():
        return None
    try:
        data = json.loads(ECONOMIST_JSON_PATH.read_text(encoding="utf-8"))
        top  = data.get("top_bullets", [])
        day  = data.get("day_bullets", [])
        if not top and not day:
            return None
        def _clean(bullets):
            return [b.lstrip("●・▶︎▶ ").strip() for b in bullets if b.strip()]
        gen_at = data.get("generated_at", "")
        print(f"[OK] economist_latest.json から Economist データ読み込み（{gen_at}）")
        return {
            "available":      True,
            "world_in_brief": _clean(top),
            "day_ahead":      _clean(day),
            "generated_at":   gen_at,
            "cover_local":    data.get("cover_local", ""),
            "top_img_url":    data.get("top_img_url", ""),
        }
    except Exception as ex:
        print(f"[WARN] economist_latest.json 読み込み失敗: {ex}")
        return None


def load_mail_data() -> list | None:
    """
    mail_latest.json が存在すれば読み込んで MAIL_SUMMARIES 形式に変換して返す。
    なければ None を返す（ハードコードにフォールバック）。
    """
    if not MAIL_JSON_PATH.exists():
        return None
    try:
        data      = json.loads(MAIL_JSON_PATH.read_text(encoding="utf-8"))
        summaries = data.get("summaries", [])
        if not summaries:
            return None
        result = []
        for s in summaries:
            raw_subjects = s.get("subjects", [])
            subjects = []
            for item in raw_subjects:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    pdf_url = str(item[2]) if len(item) >= 3 else ""
                    subjects.append((str(item[0]), str(item[1]), pdf_url))
            if not subjects:
                subjects = [("", "（メールなし）", "")]
            color = s.get("color", "CYAN")
            if color not in COLOR_CSS:
                color = "CYAN"
            result.append({
                "sender":    s.get("sender", "不明"),
                "short":     s.get("short", "??"),
                "color":     color,
                "count":     int(s.get("count", 0)),
                "bullets":   [str(b) for b in s.get("bullets", [])],
                "subjects":  subjects,
                "pdf_files": [str(f) for f in s.get("pdf_files", [])],
            })
        gen_at = data.get("generated_at", "")
        print(f"[OK] mail_latest.json から {len(result)} 送信者読み込み（{gen_at}）")
        return result
    except Exception as ex:
        print(f"[WARN] mail_latest.json 読み込み失敗: {ex}")
        return None


# ─────────────────────────────────────────────────────────────
#  trump_monitor.py 連携：JSON 読み込み
# ─────────────────────────────────────────────────────────────

# trump_monitor.py が出力するJSONのパス
TRUMP_JSON_PATH = Path(__file__).parent / "db" / "north america" / "trump_latest.json"

def load_trump_data() -> dict | None:
    """trump_latest.json が存在すれば読み込んで返す。なければ None を返す。"""
    if not TRUMP_JSON_PATH.exists():
        return None
    try:
        return json.loads(TRUMP_JSON_PATH.read_text(encoding="utf-8"))
    except Exception as ex:
        print(f"[WARN] trump_latest.json 読み込み失敗: {ex}")
        return None


def build_trump_sections_from_json(data: dict) -> tuple[dict, list]:
    """trump_latest.json の内容から TRUMP_STATS と TRUMP_SECTIONS を構築する。"""

    # ── ソース統計 ──────────────────────────────────────────────────
    raw_sources = data.get("sources_summary", [])
    sources = [(s["icon"], s["label"], s["count"]) for s in raw_sources] if raw_sources else []

    stats = {
        "date_range": data.get("date_range", DATE_RANGE),
        "item_count": data.get("item_count", 0),
        "sources":    sources,
    }

    # ── bullets ヘルパー ────────────────────────────────────────────
    def bullets(key: str) -> list:
        items = data.get(key, [])
        return items if items else [{"text": "（該当情報なし）", "source": "", "url": ""}]

    # ── セクション定義（8セクション固定）──────────────────────────
    sections = [
        dict(
            id="key_points", icon="⭐", color="GOLD", featured=True,
            badge="主要ポイント", title="本日の主要ポイント",
            title_url=gn("Trump statement White House today"),
            bullets=bullets("key_points"),
        ),
        dict(
            id="sns", icon="\U0001f4f1", color="BLUE", featured=False,
            badge="SNS 発言", title="Truth Social 発言",
            title_url="https://truthsocial.com/@realDonaldTrump",
            bullets=bullets("sns"),
        ),
        dict(
            id="interviews", icon="\U0001f3a4", color="RED", featured=False,
            badge="記者会見・インタビュー", title="記者会見・メディアインタビュー",
            title_url=wh("briefings-statements/"),
            bullets=bullets("press_conference"),
        ),
        dict(
            id="official", icon="\U0001f4dc", color="GOLD", featured=False,
            badge="公式発表・大統領令", title="ホワイトハウス公式発表・大統領令",
            title_url=wh("presidential-actions/"),
            bullets=bullets("whitehouse_official"),
        ),
        dict(
            id="wh_briefing", icon="\U0001f399", color="BLUE", featured=False,
            badge="WH 記者会見", title="ホワイトハウス報道官ブリーフィング",
            title_url=wh("briefings-statements/"),
            bullets=bullets("wh_briefing"),
        ),
        dict(
            id="video", icon="\U0001f3ac", color="RED", featured=False,
            badge="動画コンテンツ", title="YouTube 動画・字幕コンテンツ",
            title_url="https://www.youtube.com/@WhiteHouse",
            bullets=bullets("video"),
        ),
        dict(
            id="cabinet", icon="\U0001f465", color="GOLD", featured=False,
            badge="閣僚動向", title="主要閣僚の動向",
            title_url=gn("Trump cabinet Bessent Rubio Hegseth Vance statement"),
            bullets=bullets("cabinet"),
        ),
        dict(
            id="japan", icon="\U0001f1ef\U0001f1f5", color="RED", featured=False,
            badge="日本への影響", title="日本への影響・注目点",
            title_url=gn("Japan security economy Trump policy impact"),
            bullets=bullets("japan_impact"),
        ),
    ]

    return stats, sections


# ─────────────────────────────────────────────────────────────
#  カラーパレット
# ─────────────────────────────────────────────────────────────
COLOR_CSS = {
    "YEL":  {"hex": "#B48200", "bg": "#FFF8E6", "label": "米中・貿易"},
    "RED":  {"hex": "#C81E32", "bg": "#FFF0F2", "label": "紛争・危機"},
    "CYAN": {"hex": "#0096C8", "bg": "#F0F8FF", "label": "外交・日米"},
    "ORG":  {"hex": "#D26400", "bg": "#FFF4EC", "label": "台湾・安保"},
    "GRN":  {"hex": "#00A046", "bg": "#F0FFF6", "label": "産業・技術"},
    "PRP":  {"hex": "#7832B4", "bg": "#F6F0FF", "label": "その他"},
}

SOURCES = "NHK・産経・日経・CNBC・FT・BBC・NYT・Reuters・Al Jazeera ほか"

# GitHub Actions 手動トリガー URL（「今すぐ更新」ボタンのリンク先）
GITHUB_ACTIONS_URL = "https://github.com/shortreport/world-monitoring/actions/workflows/update.yml"


# ═════════════════════════════════════════════════════════════
#  ① ホームページ データ
#     bullets の各要素は dict(text, source, url) または文字列
#     title_url  : カードタイトルのリンク先
# ═════════════════════════════════════════════════════════════
NEWS_ITEMS = [
    dict(
        badge="① 米中首脳会談", color="YEL",
        title="「G2」の衝撃と台湾への最強警告",
        title_url=gn("Trump Xi Beijing summit May 2026"),
        subtitle="習主席「対応誤れば衝突・非常に危険」/ トランプ「台湾武器売却は暫定保留」",
        bullets=[
            dict(text="5/14〜15 北京で米中首脳会談── トランプ大統領2017年以来の初訪中",
                 source="Reuters", url=gn("Trump Xi Beijing summit first visit 2017")),
            dict(text="習主席「対応誤れば両国衝突・非常に危険」── 近年最も強硬な台湾警告",
                 source="BBC", url=gn("Xi Jinping Taiwan warning collision dangerous Trump")),
            dict(text="トランプ「台湾武器売却140億ドルは暫定保留」── いかなる約束もしなかった",
                 source="NYT", url=gn("Trump Taiwan arms sale pause 14 billion")),
            dict(text="貿易合意：ボーイング200機・大豆2500万トン・LNG・農産物購入に合意",
                 source="FT", url=gn("US China trade deal Boeing soybeans LNG 2026")),
            dict(text="「測定された競争に基づく戦略的安定の米中関係」の枠組みを合意",
                 source="WSJ", url=gn("US China strategic stability managed competition framework")),
            dict(text="産経「G2時代の予感」── 日本の安保・同盟体制への影響を強く懸念",
                 source="産経新聞", url=gn("G2 Japan security alliance US China summit impact")),
        ],
        risk="数週間以内に台湾武器売却の可否が判明。米中G2合意が深化すれば日本が蚊帳の外に。",
        context="米中が「管理可能な競争」を演出しつつ経済的相互依存を維持。台湾は最大の未解決事項。",
    ),
    dict(
        badge="② 米イラン情勢", color="RED",
        title="交渉崩壊リスクとホルムズ長期封鎖",
        title_url=gn("Iran Hormuz strait closure oil 2026"),
        subtitle="トランプ「我慢の限界」/ 原油ピーク120ドル / 日本エネルギー危機",
        bullets=[
            dict(text="2/28 米・イスラエルが「エピック・フューリー作戦」開始。ハメネイ師死亡",
                 source="Al Jazeera", url=gn("US Israel Iran Operation Epic Fury Khamenei killed")),
            dict(text="3/4 イランがホルムズ海峡「閉鎖」宣言── 3/8迄に船舶10隻以上が攻撃被害",
                 source="Reuters", url=gn("Iran Hormuz strait closure declaration ships attacked")),
            dict(text="4/8 停戦合意も再エスカレート── トランプ「我慢の限界」と戦闘再開示唆",
                 source="CNBC", url=gn("Trump Iran ceasefire re-escalation patience limit")),
            dict(text="原油：開戦時67ドル→ピーク120ドル（+79%）── 5月初 114ドルで依然高値圏",
                 source="Bloomberg", url=gn("oil price Hormuz closure 120 dollars peak 2026")),
            dict(text="グローバル原油供給の約20%が影響── IEA「史上最大のエネルギー安全保障の挑戦」",
                 source="IEA", url=gn("IEA Hormuz 20 percent global oil supply energy security")),
            dict(text="日本：原油輸入の90%がホルムズ経由── 高市首相「6月に7割確保の見通し」",
                 source="NHK", url=gn("Japan oil import Hormuz 90 percent Takaichi energy security")),
        ],
        risk="数日〜数週間内に戦闘再開の可能性。長期封鎖で日本エネルギー危機・物価急騰。",
        context="ホルムズ封鎖が長期化すれば原油150ドル超も予測。日本はLNGの代替調達ルート確保を急ぐ。",
    ),
    dict(
        badge="③ 日米関係", color="CYAN",
        title="ベッセント来日とG2への強い懸念",
        title_url=gn("Bessent Japan visit rare earth alliance 2026"),
        subtitle="高市首相・上田日銀総裁と会談。レアアース・エネルギーで連携強化",
        bullets=[
            dict(text="ベッセント財務長官来日（5/11〜13）── 高市首相・片山財務相・上田総裁と会談",
                 source="日経新聞", url=gn("Bessent Japan Takaichi BOJ Ueda rare earth trade")),
            dict(text="主要議題：レアアース代替調達・イラン対応・円安・通貨政策を協議",
                 source="FT", url=gn("Bessent Japan rare earth Iran yen currency policy")),
            dict(text="中国がレアアース輸出規制を強化── 日本の半導体・防衛産業に直撃",
                 source="Nikkei Asia", url=gn("China rare earth export restrictions Japan semiconductor defense")),
            dict(text="G7が2026年1月にレアアース代替サプライチェーン構築で合意済み",
                 source="Reuters", url=gn("G7 rare earth alternative supply chain 2026 agreement")),
            dict(text="米中会談後、トランプ大統領が高市首相と電話── 会談内容を詳細に共有",
                 source="産経新聞", url=gn("Trump Takaichi phone call US China summit details")),
            dict(text="レアアースETF（REMX）-3.6%急落── 台湾武器売却保留で供給不安が継続",
                 source="Bloomberg", url=gn("REMX rare earth ETF drop Taiwan arms sale pause")),
        ],
        risk="150日関税暫定措置期限（2026年夏）と台湾武器売却保留が日米関係の試金石に。",
        context="日本の半導体・EV・防衛装備はレアアースに依存。中国の輸出規制が国家安全保障に直結。",
    ),
    dict(
        badge="④ 台湾問題", color="ORG",
        title="習主席の最強警告と武器売却の行方",
        title_url=gn("Taiwan arms sale Xi warning Trump pause 2026"),
        subtitle="140億ドル保留・12月承認分110億ドルは維持── 数週間〜数ヶ月が分岐点",
        bullets=[
            dict(text="習主席「対応誤れば衝突・非常に危険」── 近年最も強硬な台湾警告を公開発表",
                 source="AFP", url=gn("Xi Jinping Taiwan strongest warning collision dangerous public")),
            dict(text="トランプ「140億ドル武器売却は暫定保留」── 交渉カードとして活用の構え",
                 source="WSJ", url=gn("Trump Taiwan 14 billion arms sale pause negotiation card")),
            dict(text="中国：農産物・石油の購入増加を条件に、武器売却停止を強く要求",
                 source="NYT", url=gn("China demands Taiwan arms sale stop agricultural oil purchase")),
            dict(text="2025年12月承認済みの110億ドル武器パッケージは現時点で維持",
                 source="Reuters", url=gn("Taiwan 11 billion arms package December 2025 maintained")),
            dict(text="台湾：防衛費250億ドル可決済み── 独自抑止力の強化と徴兵制延長を継続",
                 source="AP", url=gn("Taiwan defense budget 25 billion deterrence conscription")),
            dict(text="高市「台湾有事」答弁後── 黄川田大臣が日本閣僚として初めて中国を訪問",
                 source="NHK", url=gn("Japan minister first visit China Taiwan contingency Kogawada")),
        ],
        risk="武器売却凍結→台湾の抑止力低下→中国の圧力増大。数週間〜数ヶ月が重要な分岐点。",
        context="習主席の発言は北京サミット前に中国側が公開。米側の沈黙と対照的で圧力戦略の一環。",
    ),
    dict(
        badge="⑤ 自動車産業", color="GRN",
        title="ホンダ上場来初赤字・EV撤退加速",
        title_url=gn("Honda EV loss first deficit Nissan merger 2026"),
        subtitle="1.45兆円EV損失 / 脱ガソリン撤回 / 日産とホンダが統合検討",
        bullets=[
            dict(text="ホンダ26年3月期：1.45兆円のEV関連損失── 上場来初の赤字4239億円",
                 source="Nikkei Asia", url=gn("Honda EV loss 14.5 trillion yen first deficit FY2026")),
            dict(text="ホンダ0シリーズSUV・セダン、オンタリオ州工場（1.5兆円規模）を無期限停止",
                 source="Reuters", url=gn("Honda 0 series EV Ontario factory suspension indefinite")),
            dict(text="日産：3400億円超の損失── 工場閉鎖・大規模リストラ。ホンダと統合を検討",
                 source="FT", url=gn("Nissan loss factory closure restructuring Honda merger")),
            dict(text="トヨタ：EV＋ハイブリッド両軸で米工場に1600億円投資。純利益22%減を予測",
                 source="Bloomberg", url=gn("Toyota EV hybrid US factory investment profit decline")),
            dict(text="日本郵船：ホルムズ封鎖で中東向け自動車輸送の代替ルートを緊急検討中",
                 source="日本郵船", url=gn("NYK Nippon Yusen Hormuz auto transport alternative route")),
            dict(text="トヨタがインドに新工場建設発表（2029年稼働）── BYDの世界シェア拡大に対抗",
                 source="日経新聞", url=gn("Toyota India new factory 2029 BYD market share")),
        ],
        risk="EV撤退の間にBYDが市場獲得加速。ホルムズ長期封鎖で輸送コストの恒常的上昇が懸念。",
        context="日本メーカーはEV移行に乗り遅れた一方、中国BYDが2025年に世界販売台数1位に浮上済み。",
    ),
]

ECONOMIST = {
    "available": True,
    "world_in_brief": [
        "米中首脳会談：ボーイング200機・大豆2500万トン購入で合意。台湾武器売却は暫定保留。",
        "イラン情勢：ホルムズ封鎖継続中。原油114ドル、IEA「史上最大の安全保障の挑戦」と警告。",
        "日米協議：ベッセント財務長官が来日し高市首相・上田総裁と会談。レアアース代替調達を協議。",
        "ホンダ：EV損失1.45兆円で上場来初の赤字。オンタリオ工場を無期限停止し日産との統合を検討。",
        "G7：2026年1月をめどにレアアース代替サプライチェーンの構築で合意済み。",
    ],
    "day_ahead": [
        "米財務省が2年・5年・7年債の四半期定例入札を発表。長期金利動向に注目。",
        "NATO国防相会議（ブリュッセル）。ウクライナ追加支援と防衛費2%目標達成状況を協議。",
        "日銀・上田総裁が参院財政金融委員会で金融政策について証言。利上げ時期が焦点。",
        "OPEC+非公式協議。7月の増産ペース維持か縮小かについて調整を図る。",
    ],
}


# ═════════════════════════════════════════════════════════════
#  ② メール要約 データ（mail_slides.py 出力をそのまま投入）
# ═════════════════════════════════════════════════════════════
MAIL_SUMMARIES = [
    dict(
        sender="Council on Foreign Relations", short="CFR", color="CYAN", count=3,
        bullets=["米中首脳会談後の地政学的リスク：G2構造の固定化が進む可能性を分析",
                 "台湾海峡の緊張：武器売却保留が抑止力低下につながるリスクを警告",
                 "日米同盟の試練：150日関税措置期限（2026年夏）が日本外交の試金石に"],
        subjects=[("2026-05-24", "US-China Summit: Strategic Implications for Asia"),
                  ("2026-05-23", "Taiwan Arms Sales: What the Pause Means"),
                  ("2026-05-22", "Japan-US Alliance Under Trump 2.0")],
    ),
    dict(
        sender="Eurasia Group", short="EG", color="YEL", count=2,
        bullets=["トランプ政権の対中政策転換：「競争的共存」モデルへのシフトを指摘",
                 "関税リスクの再評価：150日猶予後の第4次関税引き上げは「50%超」と予測",
                 "中東リスク：ホルムズ封鎖の長期化確率を60%と試算"],
        subjects=[("2026-05-25", "G2 and the New World Order: Risk Assessment"),
                  ("2026-05-24", "Iran-US: Escalation Scenarios and Market Impact")],
    ),
    dict(
        sender="Morgan Stanley Research", short="MS", color="RED", count=4,
        bullets=["原油市場：ホルムズ封鎖継続で第3四半期に120〜130ドルレンジを予想",
                 "日本株：円安継続と輸出企業業績への追い風を維持。日経42,000を目標維持",
                 "EV市場の再編：ホンダ・日産の撤退でBYDのシェアが2026年に35%超へ拡大",
                 "レアアース代替コスト：日本企業の半導体セクターへの影響は年間3000億円超と試算"],
        subjects=[("2026-05-25", "Asia Pacific Market Update: Oil & Auto Sector"),
                  ("2026-05-24", "Japan Equity Strategy: Q2 Earnings Review"),
                  ("2026-05-23", "EV Industry: Honda/Nissan and the BYD Threat"),
                  ("2026-05-22", "Rare Earth Supply Chain: Cost Impact Analysis")],
    ),
    dict(
        sender="IISS Strategic Comments", short="IISS", color="ORG", count=2,
        bullets=["台湾の防衛力評価：武器売却保留は短期的な抑止力低下につながらないと分析",
                 "習主席の「最強警告」：外交的シグナルとしての意図を過剰評価しないよう指摘",
                 "黄川田大臣訪中：日本の外交的バランス外交の新たな試みとして評価"],
        subjects=[("2026-05-24", "Taiwan Strait: Deterrence Assessment Post-Summit"),
                  ("2026-05-23", "China's Taiwan Strategy: Signals vs. Threats")],
    ),
    dict(
        sender="Nikkei Asia Newsletter", short="NA", color="GRN", count=5,
        bullets=["ホンダ・日産統合交渉：2026年末の最終合意を目標に進捗中",
                 "日本のエネルギー安全保障：LNGのオーストラリア・米国調達増加で対応",
                 "トヨタのインド戦略：BYD対抗でインド新工場に4000億円追加投資を検討",
                 "高市首相の外交姿勢：台湾有事答弁後の対中メッセージの読み方を分析"],
        subjects=[("2026-05-25", "Honda-Nissan Merger Talks: Latest Updates"),
                  ("2026-05-25", "Japan Energy Security: LNG Diversification"),
                  ("2026-05-24", "Toyota India: New Factory Details"),
                  ("2026-05-24", "Takaichi's China Policy: Reading the Signals"),
                  ("2026-05-23", "Rare Earth Crisis: Japan's Industry Response")],
    ),
    dict(
        sender="Economist Intelligence Unit", short="EIU", color="PRP", count=2,
        bullets=["グローバル経済見通し：ホルムズ封鎖継続で2026年世界成長率を2.1%に下方修正",
                 "インフレリスク：エネルギー価格上昇で日本の消費者物価指数は年末3.5%超予想",
                 "地政学リスク指数：中東・台湾海峡の同時緊張で過去10年で最高水準に達する"],
        subjects=[("2026-05-25", "Global Economic Outlook: Q2 2026 Update"),
                  ("2026-05-24", "Geopolitical Risk Index: Mid-Year Assessment")],
    ),
]


# ═════════════════════════════════════════════════════════════
#  ③ トランプページ データ
#     bullets の各要素は dict(text, source, url) または文字列
#     title_url  : セクションタイトルのリンク先（元データ）
# ═════════════════════════════════════════════════════════════
TRUMP_STATS = {
    "date_range": DATE_RANGE,
    "item_count": 47,
    "sources": [
        ("📱", "Truth Social",      "8件"),
        ("📜", "大統領令・行政措置", "3件"),
        ("🎤", "ホワイトハウスRSS", "12件"),
        ("🎬", "YouTube（字幕あり）","5件"),
        ("📰", "Google News",       "19件"),
    ],
}

TRUMP_SECTIONS = [
    dict(
        id="key_points", icon="⭐", color="GOLD", featured=True,
        badge="主要ポイント",
        title="本日の主要ポイント",
        title_url=gn("Trump Truth Social China Beijing summit Taiwan arms 2026"),
        bullets=[
            dict(text="北京訪問から帰国したトランプ大統領が Truth Social で「歴史的成果」と宣言",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="台湾武器売却の暫定保留を自ら認め「最終決定は数週間以内」と明言",
                 source="Reuters", url=gn("Trump Taiwan arms sale pause final decision weeks")),
            dict(text="ホルムズ封鎖に関し「イランが完全に封鎖を解除しない限り軍事行動を排除しない」",
                 source="AP", url=gn("Trump Iran Hormuz military action option warning")),
            dict(text="ベッセント財務長官の訪日結果を「大成功」と評価し対日貿易交渉の継続を示唆",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="Truth Social でホンダ赤字について「EVは失敗。ガソリン車こそ正解だった」と投稿",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
        ],
    ),
    dict(
        id="sns", icon="📱", color="BLUE", featured=False,
        badge="SNS 発言",
        title="Truth Social 発言",
        title_url="https://truthsocial.com/@realDonaldTrump",
        bullets=[
            dict(text="「北京会談は最高だった。習との関係は完璧だ。中国はボーイング200機を買う！」",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="「台湾の武器売却については数週間で決める。誰も私を急かすことはできない」",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="「イランはホルムズを開けろ。さもないと次は選択肢が限られる」",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="「ホンダの赤字はEVが失敗だった証拠。私が正しかった。ガソリン車で行け！」",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
            dict(text="「日本のベッセントとの会談は完璧。日米貿易は新たな時代に入った」",
                 source="Truth Social", url="https://truthsocial.com/@realDonaldTrump"),
        ],
    ),
    dict(
        id="interviews", icon="🎤", color="RED", featured=False,
        badge="記者会見・インタビュー",
        title="記者会見・メディアインタビュー",
        title_url=wh("briefings-statements/"),
        bullets=[
            dict(text="帰国後記者会見：「G2という言葉は使わない。米中は競争関係だが協力もする」",
                 source="WH Press Conf.", url=wh("briefings-statements/")),
            dict(text="Fox News独占インタビュー：「台湾は自分たちで防衛費を払え。米国は保険会社ではない」",
                 source="Fox News", url=gn("Trump Fox News interview Taiwan defense pay insurance")),
            dict(text="ホワイトハウス会見：「ホルムズ封鎖は容認しない。エネルギー安全保障は米国の核心利益」",
                 source="WH Press Conf.", url=wh("briefings-statements/")),
            dict(text="ロイター取材：「日本との貿易交渉は2026年夏の関税期限前に妥結できる」",
                 source="Reuters", url=gn("Trump Japan trade deal tariff deadline summer 2026")),
        ],
    ),
    dict(
        id="official", icon="📜", color="GOLD", featured=False,
        badge="公式発表・大統領令",
        title="ホワイトハウス公式発表・大統領令",
        title_url=wh("presidential-actions/"),
        bullets=[
            dict(text="大統領令：「米国産 LNG の中東地域への緊急輸出枠を30%増加」を署名",
                 source="WH 大統領令", url=wh("presidential-actions/")),
            dict(text="ホワイトハウス声明：「米中北京共同声明」の全文を公式発表",
                 source="WH 公式声明", url=wh("briefings-statements/")),
            dict(text="行政措置：「レアアース国内生産促進」に向け国防生産法の発動を検討中と発表",
                 source="WH ニュース", url=wh("news/")),
            dict(text="商務省指示：「中国向け半導体輸出規制の見直し」を180日以内に完了するよう命令",
                 source="Commerce Dept.", url=gn("Trump Commerce semiconductor export China review 180 days")),
        ],
    ),
    dict(
        id="wh_briefing", icon="🎙️", color="BLUE", featured=False,
        badge="WH 記者会見",
        title="ホワイトハウス報道官ブリーフィング",
        title_url=wh("briefings-statements/"),
        bullets=[
            dict(text="レービット報道官：「北京会談は米国の国益を最優先した交渉だった」と強調",
                 source="WH Briefing", url=wh("briefings-statements/")),
            dict(text="「台湾に関する大統領の立場は変わっていない」── 一つの中国政策を再確認",
                 source="WH Briefing", url=wh("briefings-statements/")),
            dict(text="「ホルムズ問題はイランが選択次第で即時解決できる」── 責任はイラン側にあると明言",
                 source="WH Briefing", url=wh("briefings-statements/")),
        ],
    ),
    dict(
        id="video", icon="🎬", color="RED", featured=False,
        badge="動画コンテンツ",
        title="YouTube 動画・字幕コンテンツ",
        title_url="https://www.youtube.com/@WhiteHouse",
        bullets=[
            dict(text="WH公式動画「President Trump Returns from China」：帰国演説（字幕あり）",
                 source="YouTube WH", url="https://www.youtube.com/@WhiteHouse"),
            dict(text="記者ブリーフィング動画：レービット報道官が北京会談を詳細説明",
                 source="YouTube WH", url="https://www.youtube.com/@WhiteHouse"),
            dict(text="大統領令署名式動画：LNG緊急輸出拡大命令への署名シーン（字幕付き）",
                 source="YouTube WH", url="https://www.youtube.com/@WhiteHouse"),
            dict(text="Fox Business インタビュー動画：ホンダ赤字・EV政策についてのコメント全文",
                 source="Fox Business", url=gn("Trump Fox Business interview Honda EV policy")),
        ],
    ),
    dict(
        id="cabinet", icon="👥", color="GOLD", featured=False,
        badge="閣僚動向",
        title="主要閣僚の動向",
        title_url=gn("Trump cabinet officials Bessent Rubio Hegseth statement May 2026"),
        bullets=[
            dict(text="ベッセント財務長官：訪日成果報告「円安是正には言及せず、通貨政策協議を継続」",
                 source="Treasury Dept.", url=gn("Bessent Treasury Japan visit yen currency report")),
            dict(text="ルビオ国務長官：「北京会談は台湾問題を解決しない。米国の防衛コミットは不変」",
                 source="State Dept.", url=gn("Rubio State Taiwan commitment unchanged Beijing")),
            dict(text="ヘグセス国防長官：「ホルムズ対応で第5艦隊を増強。B-52爆撃機を追加配備」",
                 source="Pentagon", url=gn("Hegseth Pentagon 5th Fleet Hormuz B-52 deployment")),
            dict(text="ヴァンス副大統領：NATO会議でウクライナ支援の「段階的縮小」を示唆",
                 source="VP Office", url=gn("Vance NATO Ukraine aid gradual reduction")),
        ],
    ),
    dict(
        id="japan", icon="🇯🇵", color="RED", featured=False,
        badge="日本への影響",
        title="日本への影響・注目点",
        title_url=gn("Japan security economy Trump policy impact 2026"),
        bullets=[
            dict(text="【緊急】台湾武器売却保留：「数週間以内に最終決定」→ 日本の安全保障環境に直結",
                 source="Reuters", url=gn("Taiwan arms sale pause Japan security implications")),
            dict(text="【貿易】関税150日猶予（2026年夏期限）：ベッセント訪日で暫定延長の可能性が浮上",
                 source="日経新聞", url=gn("Japan US tariff 150 day extension Bessent visit")),
            dict(text="【エネルギー】LNG緊急輸出拡大令：日本向けLNG供給の安定化に寄与する可能性",
                 source="METI", url=gn("US LNG export Japan energy security Hormuz")),
            dict(text="【産業】ホンダ赤字コメント：トランプのEV否定姿勢が日本の電動化戦略に逆風",
                 source="Bloomberg", url=gn("Trump EV opposition Japan automaker strategy")),
            dict(text="【安保】ヘグセスのB-52増派：横田・嘉手納への配備増強が日本防衛力を強化",
                 source="産経新聞", url=gn("B-52 Yokota Kadena deployment Japan defense")),
        ],
    ),
]


# ═════════════════════════════════════════════════════════════
#  共通テンプレート部品
# ═════════════════════════════════════════════════════════════
def e(text: str) -> str:
    return H.escape(str(text))

def href(url: str, text: str, cls: str = "", extra: str = "") -> str:
    """外部リンクタグ（常に target="_blank"）"""
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer"{cls_attr}{extra}>{text}</a>'

_FT_SOURCES = {"ft", "financial times", "ft.com"}

def render_bullet(b, accent: str) -> str:
    """文字列 or dict の bullet を <li> に変換。dict の場合はリンク付き"""
    if isinstance(b, dict):
        text = e(b.get("text", ""))
        src  = b.get("source", "")
        url  = b.get("url", "")
        tag_cls = "src-tag src-tag-ft" if src.lower() in _FT_SOURCES else "src-tag"
        if url:
            inner = (f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer" class="bullet-link">'
                     f'{text}'
                     f'<span class="{tag_cls}">{e(src)} ↗</span>'
                     f'</a>')
            return f'<li class="has-link">{inner}</li>'
        return f'<li>{text}</li>'
    return f'<li>{e(str(b))}</li>'


SHARED_CSS = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --primary:    #16163e;
      --eco-red:    #C8141E;
      --surface:    #ffffff;
      --surface-2:  #f3f4f6;
      --border:     #e2e4e9;
      --text:       #1a1a2e;
      --text-sub:   #5f6368;
      --radius:     12px;
      --accent:     #0096c8;
      --card-bg:    #f0f8ff;
    }

    body {
      font-family: 'Noto Sans JP', -apple-system, 'Hiragino Sans',
                   'Yu Gothic UI', 'Meiryo', sans-serif;
      background: var(--surface-2);
      color: var(--text);
      line-height: 1.65;
      font-size: 14px;
    }

    /* ── Site Header ── */
    .site-header {
      background: var(--primary); color: #fff;
      padding: 0 24px; height: 58px;
      display: flex; align-items: center; gap: 16px;
      position: sticky; top: 0; z-index: 300;
      box-shadow: 0 2px 8px rgba(0,0,0,.25);
    }
    .logo { font-size: 20px; font-weight: 700; letter-spacing: .5px; white-space: nowrap; }
    .logo em { color: #5bc8f5; font-style: normal; }
    .header-date { font-size: 12px; color: rgba(255,255,255,.5); white-space: nowrap; }
    .header-spacer { flex: 1; }
    .live-badge { background: #e63946; color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }
    .update-time { font-size: 11px; color: rgba(255,255,255,.4); white-space: nowrap; }
    .force-update-btn {
      display: inline-flex; align-items: center; gap: 4px;
      background: rgba(255,255,255,.1); color: rgba(255,255,255,.65);
      border: 1px solid rgba(255,255,255,.25); border-radius: 14px;
      padding: 4px 11px; font-size: 11px; font-weight: 600;
      cursor: pointer; white-space: nowrap; font-family: inherit;
      transition: background .15s, color .15s, border-color .15s;
    }
    .force-update-btn:hover { background: rgba(255,255,255,.22); color: #fff; border-color: rgba(255,255,255,.5); }
    .force-update-btn:disabled { opacity: .55; cursor: not-allowed; }

    /* ── Page Navigation Tabs ── */
    .page-nav {
      background: var(--surface); border-bottom: 1px solid var(--border);
      padding: 0 24px; display: flex; align-items: stretch;
      position: sticky; top: 58px; z-index: 200;
      box-shadow: 0 1px 4px rgba(0,0,0,.06);
    }
    .page-nav a {
      display: flex; align-items: center; gap: 6px;
      padding: 0 18px; height: 44px;
      font-size: 14px; font-weight: 500; color: var(--text-sub);
      text-decoration: none; border-bottom: 3px solid transparent;
      white-space: nowrap; transition: color .15s, border-color .15s;
    }
    .page-nav a:hover { color: var(--text); }
    .page-nav a.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 700; }
    .page-nav a .nav-icon { font-size: 15px; }
    .page-nav a:last-child { margin-left: auto; border-left: 1px solid var(--border); }

    /* ── Section label ── */
    .section-label {
      font-size: 11px; font-weight: 700; color: var(--text-sub);
      text-transform: uppercase; letter-spacing: 1.2px;
      margin: 0 0 12px; padding-bottom: 8px; border-bottom: 2px solid var(--border);
    }

    /* ── Clickable bullet styles ── */
    li.has-link { cursor: pointer; }
    .bullet-link {
      display: block;
      color: inherit;
      text-decoration: none;
      position: relative;
      padding-right: 4px;
      transition: color .15s;
    }
    .bullet-link:hover { color: var(--accent); }
    .src-tag {
      display: inline-block;
      font-size: 10px;
      font-weight: 600;
      color: var(--text-sub);
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 1px 5px;
      margin-left: 7px;
      vertical-align: middle;
      white-space: nowrap;
      opacity: 0.55;
      transition: opacity .15s, color .15s, background .15s, border-color .15s;
    }
    .bullet-link:hover .src-tag {
      opacity: 1;
      color: var(--accent);
      background: #e8f4ff;
      border-color: var(--accent);
    }
    /* FT (Financial Times) source highlight */
    .src-tag-ft {
      color: #c45000;
      background: #fff3ea;
      border-color: #e8925a;
      opacity: 0.85;
    }
    .bullet-link:hover .src-tag-ft {
      color: #a03800;
      background: #ffe8d6;
      border-color: #c45000;
    }

    /* ── Clickable card title ── */
    .card-title-link {
      color: inherit;
      text-decoration: none;
      transition: color .15s;
    }
    .card-title-link:hover { color: var(--accent); }
    .card-title-link:hover::after {
      content: " ↗";
      font-size: 14px;
      color: var(--accent);
      opacity: .7;
    }

    /* ── Footer ── */
    .site-footer {
      text-align: center; padding: 24px;
      font-size: 12px; color: var(--text-sub);
      margin-top: 32px; border-top: 1px solid var(--border);
    }

    @media (max-width: 640px) {
      .site-header { padding: 0 14px; gap: 10px; }
      .page-nav { padding: 0 8px; }
      .page-nav a { padding: 0 12px; font-size: 13px; }
      .update-time { display: none; }
      .force-update-btn { display: none; }
    }
"""

def build_head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)} | World News</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
{SHARED_CSS}
{extra_css}
  </style>
</head>"""

FORCE_UPDATE_SCRIPT = """<script>
(function(){
  function triggerSiteUpdate(){
    var btn=document.getElementById('force-update-btn');
    btn.textContent='⏳ 更新中…';
    btn.disabled=true;
    location.href=location.pathname+'?r='+Date.now();
  }
  if(location.search.startsWith('?r=')){
    history.replaceState(null,'',location.pathname);
  }
  window.triggerSiteUpdate=triggerSiteUpdate;
})();
</script>"""


def build_header_nav(active_page, data_updated_at=None):
    pages = [
        ("index.html",        "🏠",  "ホーム",                 "home"),
        ("intelligence.html", "🔍",  "インテリジェンス",       "intelligence"),
        ("trump.html",        "🇺🇸", "USトランプ",             "trump"),
        ("theme.html",        "🔎",  "個別テーマ",             "theme"),
        ("midterm.html",      "🗳️",  "米国中間選挙",           "midterm"),
        ("summary.html",      "📋",  "エグゼクティブ・サマリー", "summary"),
    ]
    tabs = ""
    for href_val, icon, label, pid in pages:
        cls = ' class="active"' if pid == active_page else ""
        tabs += f'  <a href="{href_val}"{cls}><span class="nav-icon">{icon}</span>{e(label)}</a>\n'

    # メール・The Economist は PC 更新のみ。それ以外は GitHub Actions が担当。
    update_note = "6時間ごと自動更新" if active_page in ("home", "trump", "theme") else "毎朝6:30更新（PC）"

    # data_updated_at が渡された場合はそのデータの実際の更新日時を表示
    # （generate_site.py の実行時刻ではなくデータ生成時刻を正直に表示する）
    if data_updated_at:
        upd_display = f"データ更新: {e(data_updated_at)}"
    else:
        upd_display = f"最終更新: {DATE_JP} {TIME_JP}"

    return f"""
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'" style="cursor:pointer;" title="ホームへ">World<em>News</em></div>
  <div class="header-date">{DATE_JP}</div>
  <div class="header-spacer"></div>
  <div class="update-time">{upd_display} &nbsp;|&nbsp; {update_note}</div>
  <button id="force-update-btn" class="force-update-btn" onclick="triggerSiteUpdate()" title="GitHub Actions ワークフローを起動してサイトを更新">🔄 今すぐ更新</button>
  <div class="live-badge">LIVE</div>
</header>
{FORCE_UPDATE_SCRIPT}
<nav class="page-nav">
{tabs}</nav>"""

def build_footer(data_updated_at=None):
    # data_updated_at が渡された場合はそのデータの実際の更新日時をフッターにも表示
    if data_updated_at:
        upd_line = f"データ更新: {e(data_updated_at)}"
    else:
        upd_line = f"最終更新: {DATE_JP} {TIME_JP}"
    return f"""
<footer class="site-footer">
  ソース: {SOURCES} &nbsp;|&nbsp; The Economist &nbsp;|&nbsp; White House RSS &nbsp;|&nbsp; Truth Social<br>
  {upd_line} &nbsp;|&nbsp;
  ☁️ ホーム・USトランプ: 6時間ごと自動更新 &nbsp;|&nbsp;
  🖥️ メール・The Economist: 毎朝6:30更新（PC）<br>
  <button onclick="triggerSiteUpdate()" style="background:none;border:none;color:var(--accent);font-size:11px;cursor:pointer;padding:0;font-family:inherit;">🔄 今すぐ更新（GitHub Actions）</button>
  &nbsp;|&nbsp; World News
</footer>"""


# ═════════════════════════════════════════════════════════════
#  ① ホームページ生成
# ═════════════════════════════════════════════════════════════
HOME_CSS = """
    .cat-bar {
      background: var(--surface); border-bottom: 1px solid var(--border);
      padding: 10px 24px; display: flex; align-items: center; gap: 8px;
      overflow-x: auto; -webkit-overflow-scrolling: touch;
    }
    .cat-bar::-webkit-scrollbar { display: none; }
    .cat-all {
      font-size: 13px; font-weight: 700; background: var(--primary); color: #fff;
      border: none; padding: 6px 16px; border-radius: 20px; cursor: pointer; white-space: nowrap;
    }
    .cat-tab {
      font-size: 13px; font-weight: 500; background: transparent;
      padding: 5px 14px; border-radius: 20px; border: 1.5px solid;
      cursor: pointer; white-space: nowrap; transition: all .15s;
    }
    .page-layout {
      max-width: 1140px; margin: 24px auto; padding: 0 20px;
      display: grid; grid-template-columns: 1fr 310px; gap: 24px; align-items: start;
    }
    .eco-sidebar { position: sticky; top: 110px; }
    .news-card {
      background: var(--surface); border-radius: var(--radius); padding: 18px 20px;
      border: 1px solid var(--border); border-left: 4px solid var(--accent);
      box-shadow: 0 1px 4px rgba(0,0,0,.06); transition: box-shadow .2s, transform .15s;
    }
    .news-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,.11); transform: translateY(-1px); }
    .news-card.featured {
      background: var(--card-bg); border-left-width: 6px; padding: 24px 28px; margin-bottom: 20px;
    }
    .news-card.featured .card-title { font-size: 22px; }
    .card-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
    .cat-badge { font-size: 11px; font-weight: 700; color: #fff; padding: 3px 10px; border-radius: 12px; white-space: nowrap; }
    .badge-sub { font-size: 12px; color: var(--text-sub); }
    .card-title { font-size: 17px; font-weight: 700; line-height: 1.4; margin-bottom: 6px; }
    .card-subtitle { font-size: 13px; color: var(--text-sub); line-height: 1.5; margin-bottom: 14px; }
    .card-bullets { list-style: none; padding: 0; margin-bottom: 14px; }
    .card-bullets li {
      position: relative; padding-left: 16px;
      font-size: 13px; color: #2a2a3a; margin-bottom: 7px; line-height: 1.55;
    }
    .card-bullets li::before { content: "●"; position: absolute; left: 0; color: var(--accent); font-size: 7px; top: 6px; }
    .card-details > summary {
      font-size: 12px; color: var(--accent); cursor: pointer; user-select: none;
      font-weight: 500; list-style: none; display: flex; align-items: center; gap: 5px; padding: 4px 0;
    }
    .card-details > summary::before { content: "▶"; font-size: 8px; }
    .card-details[open] > summary::before { content: "▼"; }
    .details-inner { margin-top: 12px; display: flex; flex-direction: column; gap: 10px; }
    .risk-box { padding: 10px 14px; border-radius: 8px; background: #fff0f2; border-left: 3px solid #c81e32; font-size: 12.5px; line-height: 1.65; }
    .risk-box p { color: #921020; }
    .ctx-box  { padding: 10px 14px; border-radius: 8px; background: #f0f4ff; border-left: 3px solid #4060c8; font-size: 12.5px; line-height: 1.65; }
    .ctx-box  p { color: #2a3880; }
    .box-label { display: block; font-size: 11px; font-weight: 700; margin-bottom: 5px; }
    .risk-label { color: #c81e32; }
    .ctx-label  { color: #4060c8; }
    .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
    /* Economist sidebar */
    .eco-card { background: var(--surface); border-radius: var(--radius); border: 1px solid #f0c8c8; overflow: hidden; box-shadow: 0 2px 8px rgba(200,20,30,.08); }
    .eco-header { background: #C8141E; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; }
    .eco-logo-text { font-size: 15px; font-weight: 700; color: #fff; font-family: Georgia, serif; }
    .eco-date { font-size: 11px; color: rgba(255,255,255,.7); }
    .eco-cover { background: linear-gradient(135deg, #1a1a3e 0%, #8b0000 100%); height: 120px; display: flex; align-items: center; justify-content: center; }
    .eco-cover-label { display: block; font-size: 13px; color: rgba(255,255,255,.7); font-weight: 700; font-family: Georgia, serif; text-align: center; }
    .eco-cover-sub { display: block; font-size: 10px; color: rgba(255,255,255,.4); text-align: center; margin-top: 4px; }
    .eco-section { padding: 12px 16px 8px; }
    .eco-section-title { font-size: 13px; font-weight: 700; color: #C8141E; font-family: Georgia, serif; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
    .eco-dot { display: inline-block; width: 6px; height: 6px; background: #C8141E; border-radius: 50%; }
    .eco-bullets { list-style: none; padding: 0; }
    .eco-bullets li { font-size: 12px; color: #2a2a2a; padding: 5px 0 5px 14px; border-bottom: 1px solid #f5e8e8; line-height: 1.55; position: relative; }
    .eco-bullets li:last-child { border-bottom: none; }
    .eco-bullets li::before { content: "▸"; position: absolute; left: 0; top: 5px; color: #C8141E; font-size: 10px; }
    .eco-divider { border: none; border-top: 1px solid #f0c8c8; margin: 0 16px; }
    .eco-source-note { font-size: 10px; color: #aaa; padding: 8px 16px 12px; text-align: center; }
    @media (max-width: 820px) { .page-layout { grid-template-columns: 1fr; } .eco-sidebar { position: static; order: -1; } }
    @media (max-width: 640px) { .page-layout { padding: 0 12px; margin: 16px auto; } .cat-bar { padding: 8px 12px; } .news-card.featured { padding: 18px; } .news-card.featured .card-title { font-size: 18px; } }
"""

def render_news_card(item, featured=False):
    color = item["color"]
    css   = COLOR_CSS[color]
    hex_  = css["hex"]
    bg_   = css["bg"]
    label = css["label"]

    # タイトル：URLがあればリンクに
    title_url = item.get("title_url", "")
    if title_url:
        title_html = href(title_url, e(item["title"]), "card-title-link")
    else:
        title_html = e(item["title"])

    # 箇条書き
    bullets_html = "\n".join(f"    {render_bullet(b, hex_)}" for b in item["bullets"])

    risk_html = f'<div class="risk-box"><span class="box-label risk-label">▲ リスク</span><p>{e(item["risk"])}</p></div>' if item.get("risk") else ""
    ctx_html  = f'<div class="ctx-box"><span class="box-label ctx-label">◆ 背景</span><p>{e(item["context"])}</p></div>' if item.get("context") else ""

    cls = "news-card featured" if featured else "news-card"
    details_open = " open" if featured else ""
    return f'''<article class="{cls}" data-color="{e(color)}" style="--accent:{hex_}; --card-bg:{bg_};">
  <div class="card-meta">
    <span class="cat-badge" style="background:{hex_};">{e(label)}</span>
    <span class="badge-sub">{e(item["badge"])}</span>
  </div>
  <h2 class="card-title">{title_html}</h2>
  <p class="card-subtitle">{e(item["subtitle"])}</p>
  <ul class="card-bullets">
{bullets_html}
  </ul>
  <details class="card-details"{details_open}>
    <summary>リスク・背景を見る</summary>
    <div class="details-inner">{risk_html}{ctx_html}</div>
  </details>
</article>'''

def render_economist_sidebar(eco):
    if not eco.get("available"):
        return ""
    wib = "\n".join(f'    <li>{e(b)}</li>' for b in eco["world_in_brief"])
    day = "\n".join(f'    <li>{e(b)}</li>' for b in eco["day_ahead"])

    # カバー画像：ローカル保存済み画像 → URL直接 → プレースホルダーの順で使用
    cover_local = eco.get("cover_local", "")
    top_img_url = eco.get("top_img_url", "")
    if cover_local:
        cover_html = f'<img src="{e(cover_local)}" alt="The Economist cover" style="width:100%;height:100%;object-fit:cover;display:block;">'
    elif top_img_url:
        cover_html = f'<img src="{e(top_img_url)}" alt="The Economist cover" style="width:100%;height:100%;object-fit:cover;display:block;" referrerpolicy="no-referrer">'
    else:
        cover_html = '<div><span class="eco-cover-label">Cover Image</span><span class="eco-cover-sub">Outlook メールから自動取得</span></div>'

    gen_note = (' / ' + e(eco.get('generated_at', ''))) if eco.get('generated_at') else ''

    return f'''<aside class="eco-sidebar">
  <div class="eco-card">
    <div class="eco-header">
      <span class="eco-logo-text">The Economist</span>
      <span class="eco-date">{DATE_JP}</span>
    </div>
    <div class="eco-cover" style="height:160px;overflow:hidden;padding:0;">
      {cover_html}
    </div>
    <div class="eco-section">
      <h3 class="eco-section-title"><span class="eco-dot"></span>The World in Brief</h3>
      <ul class="eco-bullets">
{wib}
      </ul>
    </div>
    <hr class="eco-divider">
    <div class="eco-section">
      <h3 class="eco-section-title"><span class="eco-dot"></span>The day ahead</h3>
      <ul class="eco-bullets">
{day}
      </ul>
    </div>
    <p class="eco-source-note">Outlook の Economist フォルダーから自動取得・Claude 要約{gen_note}</p>
  </div>
</aside>'''

def generate_home():
    # ── 動的データ読み込み（なければハードコードにフォールバック）────────
    news_items = load_home_data() or NEWS_ITEMS
    economist  = load_economist_data() or ECONOMIST

    cat_tabs = ""
    seen = set()
    for item in news_items:
        c = item["color"]
        if c not in seen and c in COLOR_CSS:
            seen.add(c)
            css = COLOR_CSS[c]
            cat_tabs += (f'  <button class="cat-tab" data-filter="{e(c)}" '
                         f'style="border-color:{css["hex"]};color:{css["hex"]};">'
                         f'{e(css["label"])}</button>\n')

    featured_html = render_news_card(news_items[0], featured=True) if news_items else ""
    grid_html     = "\n".join(render_news_card(item) for item in news_items[1:])
    eco_sidebar   = render_economist_sidebar(economist)

    return f"""{build_head("ホーム", HOME_CSS)}
<body>
{build_header_nav("home")}
<nav class="cat-bar">
  <button class="cat-all" data-filter="ALL">すべて</button>
{cat_tabs}</nav>
<div class="page-layout">
  <div class="news-main">
    <p class="section-label" style="margin-top:8px;">トップストーリー</p>
{featured_html}
    <p class="section-label">主要ニュース</p>
    <div class="news-grid" id="news-grid">
{grid_html}
    </div>
  </div>
{eco_sidebar}
</div>
{build_footer()}
<script>
(function(){{
  const cards = document.querySelectorAll('.news-card');
  const btns  = document.querySelectorAll('[data-filter]');
  btns.forEach(btn => {{
    btn.addEventListener('click', () => {{
      const f = btn.dataset.filter;
      btns.forEach(b => {{
        b.classList.remove('active');
        if (b.dataset.filter !== 'ALL') {{ b.style.background = 'transparent'; b.style.color = b.dataset.oc; }}
      }});
      btn.classList.add('active');
      if (f !== 'ALL') {{ btn.style.background = btn.dataset.oc; btn.style.color = '#fff'; }}
      cards.forEach(c => {{ c.style.display = (f === 'ALL' || c.dataset.color === f) ? '' : 'none'; }});
    }});
  }});
  btns.forEach(b => {{ if (b.dataset.filter !== 'ALL') b.dataset.oc = b.style.color; }});
}})();
</script>
</body></html>"""


# ═════════════════════════════════════════════════════════════
#  ② メール要約ページ生成
# ═════════════════════════════════════════════════════════════
MAIL_CSS = """
    .mail-wrap { max-width: 980px; margin: 24px auto; padding: 0 20px; }
    .mail-stats { display: flex; gap: 20px; flex-wrap: wrap; background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); padding: 14px 20px; margin-bottom: 20px; font-size: 13px; }
    .stat-item { display: flex; align-items: center; gap: 6px; }
    .stat-num  { font-size: 20px; font-weight: 700; color: var(--primary); }
    .stat-lbl  { color: var(--text-sub); font-size: 12px; }
    .mail-card { background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); border-left: 5px solid var(--accent); box-shadow: 0 1px 4px rgba(0,0,0,.06); margin-bottom: 16px; overflow: hidden; transition: box-shadow .2s; }
    .mail-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); }
    .mail-card-header { padding: 14px 20px 10px; display: flex; align-items: center; gap: 14px; border-bottom: 1px solid var(--border); }
    .sender-avatar { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 700; color: #fff; flex-shrink: 0; }
    .sender-name { font-size: 16px; font-weight: 700; }
    .sender-meta { font-size: 12px; color: var(--text-sub); margin-top: 2px; }
    .mail-count-badge { font-size: 12px; font-weight: 600; color: #fff; padding: 3px 10px; border-radius: 12px; }
    .mail-card-body { display: grid; grid-template-columns: 1fr 280px; }
    .mail-summary { padding: 14px 20px; border-right: 1px solid var(--border); }
    .summary-title { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .summary-bullets { list-style: none; padding: 0; }
    .summary-bullets li { position: relative; padding-left: 18px; font-size: 13px; color: #2a2a3a; margin-bottom: 9px; line-height: 1.6; }
    .summary-bullets li::before { content: "・"; position: absolute; left: 0; color: var(--accent); font-weight: 700; }
    .mail-list { padding: 14px 16px; background: #fafafa; }
    .mail-list-title { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .mail-item { padding: 6px 0; border-bottom: 1px solid #eee; }
    .mail-item:last-child { border-bottom: none; }
    .mail-item-date { font-size: 11px; color: var(--text-sub); margin-bottom: 2px; }
    .mail-item-subject { font-size: 12.5px; color: var(--text); line-height: 1.4; }
    @media (max-width: 700px) { .mail-card-body { grid-template-columns: 1fr; } .mail-summary { border-right: none; border-bottom: 1px solid var(--border); } .mail-wrap { padding: 0 12px; } }
    /* ── PDF モーダル ── */
    .mail-pdf-modal { display: none; position: fixed; inset: 0; z-index: 999; background: rgba(0,0,0,.65); align-items: center; justify-content: center; }
    .mail-pdf-modal-box { background: #fff; border-radius: 12px; overflow: hidden; width: 90vw; max-width: 920px; height: 88vh; display: flex; flex-direction: column; box-shadow: 0 12px 48px rgba(0,0,0,.4); animation: mailModalIn .18s ease; }
    @keyframes mailModalIn { from { transform: scale(.93); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    .mail-pdf-modal-header { display: flex; align-items: center; gap: 12px; padding: 10px 18px; background: var(--primary); color: #fff; flex-shrink: 0; }
    .mail-pdf-modal-title { font-size: 13px; font-weight: 600; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .mail-pdf-modal-close { background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.3); color: #fff; border-radius: 6px; padding: 4px 12px; cursor: pointer; font-size: 12px; flex-shrink: 0; }
    .mail-pdf-modal-close:hover { background: rgba(255,255,255,.28); }
    .mail-pdf-frame { flex: 1; border: none; width: 100%; }
    .mail-pdf-list-modal { flex: 1; overflow-y: auto; padding: 20px; }
    .mail-pdf-list-item { padding: 11px 16px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 10px; cursor: pointer; font-size: 13px; transition: background .15s, border-color .15s; display: flex; align-items: center; gap: 10px; }
    .mail-pdf-list-item:hover { background: #e8f4ff; border-color: var(--accent); color: var(--accent); }
    .pdf-list-icon { font-size: 18px; flex-shrink: 0; }
    .pdf-badge { display: inline-block; font-size: 9px; font-weight: 700; background: var(--accent); color: #fff; border-radius: 3px; padding: 1px 4px; margin-left: 5px; vertical-align: middle; }
    .mail-pdf-item { cursor: pointer; transition: background .12s; }
    .mail-pdf-item:hover { background: #e8f4ff; }
    .mail-pdf-list-trigger { cursor: pointer; }
    .mail-pdf-list-trigger:hover { color: var(--accent); }
"""

MAIL_MODAL_HTML = """\
<div id="mail-pdf-modal" class="mail-pdf-modal">
  <div class="mail-pdf-modal-box">
    <div class="mail-pdf-modal-header">
      <span id="mail-pdf-modal-title" class="mail-pdf-modal-title">PDF ビューア</span>
      <button id="mail-pdf-close-btn" class="mail-pdf-modal-close">✕ 閉じる</button>
    </div>
    <div id="mail-pdf-list-area" class="mail-pdf-list-modal" style="display:none;"></div>
    <iframe id="mail-pdf-frame" class="mail-pdf-frame" src="about:blank" style="display:none;"></iframe>
  </div>
</div>
<script>
(function(){
  var modal    = document.getElementById('mail-pdf-modal');
  var frame    = document.getElementById('mail-pdf-frame');
  var listArea = document.getElementById('mail-pdf-list-area');
  var titleEl  = document.getElementById('mail-pdf-modal-title');
  var closeBtn = document.getElementById('mail-pdf-close-btn');
  function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function openPdf(url, label) {
    titleEl.textContent    = label || 'PDF ビューア';
    listArea.style.display = 'none';
    frame.src              = url;
    frame.style.display    = 'block';
    modal.style.display    = 'flex';
  }
  function openPdfList(pdfsJson, senderName) {
    var pdfs = JSON.parse(pdfsJson);
    if (pdfs.length === 1) { openPdf(pdfs[0], senderName); return; }
    titleEl.textContent = senderName + ' — PDF 一覧 (' + pdfs.length + '件)';
    listArea.innerHTML = pdfs.map(function(url) {
      var fname = decodeURIComponent(url.split('/').pop()).replace(/_/g, ' ');
      return '<div class="mail-pdf-list-item" data-pdf="' + esc(url) + '" data-title="' + esc(fname) + '"><span class="pdf-list-icon">📄</span><span>' + esc(fname) + '</span></div>';
    }).join('');
    listArea.style.display = 'block';
    frame.src              = 'about:blank';
    frame.style.display    = 'none';
    modal.style.display    = 'flex';
  }
  function closeModal() {
    modal.style.display = 'none';
    frame.src           = 'about:blank';
  }
  document.addEventListener('click', function(ev) {
    var item = ev.target.closest('.mail-pdf-list-item');
    if (item) { openPdf(item.dataset.pdf, item.dataset.title); return; }
    var trigger = ev.target.closest('.mail-pdf-list-trigger');
    if (trigger) { openPdfList(trigger.dataset.pdfs, trigger.dataset.sender); return; }
    var pdfRow = ev.target.closest('.mail-pdf-item');
    if (pdfRow) { openPdf(pdfRow.dataset.pdf, pdfRow.dataset.title); return; }
    if (ev.target === modal) { closeModal(); }
  });
  closeBtn.addEventListener('click', closeModal);
  document.addEventListener('keydown', function(ev){ if(ev.key==='Escape') closeModal(); });
})();
</script>"""


def render_mail_card(s):
    hex_  = COLOR_CSS[s["color"]]["hex"]
    label = COLOR_CSS[s["color"]]["label"]
    bullets_html = "\n".join(f'        <li>{e(b)}</li>' for b in s["bullets"])

    pdf_files = s.get("pdf_files", [])
    has_pdfs  = bool(pdf_files)

    # subjects_html: 3要素タプル (date, subject, pdf_url) に対応
    subjects_html = ""
    for subj_tuple in s["subjects"]:
        date_str = subj_tuple[0] if len(subj_tuple) > 0 else ""
        subj_str = subj_tuple[1] if len(subj_tuple) > 1 else ""
        raw_pdf  = subj_tuple[2] if len(subj_tuple) > 2 else ""
        pdf_url  = urllib.parse.quote(raw_pdf, safe='/') if raw_pdf else ""
        if pdf_url:
            subjects_html += (
                f'      <div class="mail-item mail-pdf-item"'
                f' data-pdf="{e(pdf_url)}" data-title="{e(subj_str[:60])}"'
                f' title="クリックでPDF表示">'
                f'<div class="mail-item-date">{e(date_str)}</div>'
                f'<div class="mail-item-subject">{e(subj_str)}'
                f' <span class="pdf-badge">PDF</span></div>'
                f'</div>\n'
            )
        else:
            subjects_html += (
                f'      <div class="mail-item">'
                f'<div class="mail-item-date">{e(date_str)}</div>'
                f'<div class="mail-item-subject">{e(subj_str)}</div>'
                f'</div>\n'
            )

    # セクションタイトル: PDF があればクリッカブルに
    if has_pdfs:
        pdfs_json = json.dumps([urllib.parse.quote(f, safe='/') for f in pdf_files])
        sender_e  = e(s["sender"])
        summary_title_html = (
            f'<div class="summary-title mail-pdf-list-trigger"'
            f' data-pdfs=\'{pdfs_json}\' data-sender="{sender_e}"'
            f' title="クリックでPDF一覧表示">Claude 要約'
            f' <span class="pdf-badge">PDF</span></div>'
        )
        mail_list_title_html = (
            f'<div class="mail-list-title mail-pdf-list-trigger"'
            f' data-pdfs=\'{pdfs_json}\' data-sender="{sender_e}"'
            f' title="クリックでPDF一覧表示">受信メール一覧'
            f' <span class="pdf-badge">PDF</span></div>'
        )
    else:
        summary_title_html   = '<div class="summary-title">Claude 要約</div>'
        mail_list_title_html = '<div class="mail-list-title">受信メール一覧</div>'

    first_date = s["subjects"][0][0] if s["subjects"] else ""

    return f"""<div class="mail-card" style="--accent:{hex_};">
  <div class="mail-card-header">
    <div class="sender-avatar" style="background:{hex_};">{e(s["short"])}</div>
    <div style="flex:1;">
      <div class="sender-name">{e(s["sender"])}</div>
      <div class="sender-meta">{e(label)} &nbsp;|&nbsp; 最新: {e(first_date)}</div>
    </div>
    <div class="mail-count-badge" style="background:{hex_};">受信 {s["count"]} 件</div>
  </div>
  <div class="mail-card-body">
    <div class="mail-summary">
      {summary_title_html}
      <ul class="summary-bullets">
{bullets_html}
      </ul>
    </div>
    <div class="mail-list">
      {mail_list_title_html}
{subjects_html}    </div>
  </div>
</div>"""

def generate_mail():
    # ── 動的データ読み込み（なければハードコードにフォールバック）────────
    mail_summaries = load_mail_data() or MAIL_SUMMARIES

    # 生成日時を JSON から取得（表示用）
    mail_gen_at = ""
    if MAIL_JSON_PATH.exists():
        try:
            _d = json.loads(MAIL_JSON_PATH.read_text(encoding="utf-8"))
            mail_gen_at = _d.get("generated_at", "")
        except Exception:
            pass

    total    = sum(s["count"] for s in mail_summaries)
    cards    = "\n".join(render_mail_card(s) for s in mail_summaries)

    # メール要約ページは実データの更新日時を正直に表示する
    # （generate_site.py の実行時刻 ≠ メールデータの更新日時）
    mail_date_label = e(mail_gen_at) if mail_gen_at else "未取得"

    return f"""{build_head("メール要約", MAIL_CSS)}
<body>
{build_header_nav("mail", data_updated_at=mail_gen_at)}
<div class="mail-wrap">
  <p class="section-label" style="margin-top:8px;">メール要約 &nbsp;—&nbsp; データ更新: {mail_date_label}</p>
  <div class="mail-stats">
    <div class="stat-item"><span class="stat-num">{len(mail_summaries)}</span><span class="stat-lbl">送信者</span></div>
    <div class="stat-item"><span class="stat-num">{total}</span><span class="stat-lbl">受信メール</span></div>
    <div class="stat-item" style="margin-left:auto;color:var(--text-sub);font-size:12px;">
      📂 outlook_to_pdf.py + mail_slides.py から自動生成<br>
      <span style="opacity:.6;">毎朝 7:00（PC）実行 — データ更新: {mail_date_label}</span>
    </div>
  </div>
{cards}
</div>
{build_footer(data_updated_at=mail_gen_at)}
{MAIL_MODAL_HTML}
</body></html>"""


# ═════════════════════════════════════════════════════════════
#  ②-b メール要約 v2（ローリング50件）
# ═════════════════════════════════════════════════════════════
MAIL_V2_CSS = """
    :root { --primary:#16163e; --surface:#ffffff; --surface-2:#edeef1; --border:#d8dae0; --text:#1a1a2e; --text-sub:#6b6f7a; --accent:#0096c8; }
    .v2-wrap { max-width:1280px; margin:28px auto; padding:0 20px; display:grid; grid-template-columns:1fr 300px; gap:28px; align-items:start; }
    .v2-grid { display:flex; gap:14px; align-items:flex-start; }
    .v2-col  { flex:1; display:flex; flex-direction:column; gap:14px; }
    .v2-card { border-radius:4px; padding:14px 16px 12px; cursor:pointer; display:flex; flex-direction:column; gap:7px; box-shadow:2px 3px 8px rgba(0,0,0,.10),0 1px 2px rgba(0,0,0,.06); transition:transform .15s,box-shadow .15s; position:relative; }
    .v2-card:hover { transform:translateY(-3px); box-shadow:3px 6px 16px rgba(0,0,0,.15); }
    .v2-card[data-s="EG"]  { background:#fffaed; }
    .v2-card[data-s="POL"] { background:#fff0f1; }
    .v2-card[data-s="JET"] { background:#edfff4; }
    .v2-card[data-s="OTH"] { background:#f5f5ff; }
    .v2-sender { font-size:10px; font-weight:700; letter-spacing:.8px; text-transform:uppercase; }
    .v2-card[data-s="EG"]  .v2-sender { color:#8a6200; }
    .v2-card[data-s="POL"] .v2-sender { color:#a8121e; }
    .v2-card[data-s="JET"] .v2-sender { color:#007838; }
    .v2-card[data-s="OTH"] .v2-sender { color:#444488; }
    .v2-title   { font-size:13px; font-weight:700; line-height:1.45; color:#1a1a2e; flex:1; }
    .v2-excerpt { font-size:11.5px; color:#3a3a50; line-height:1.6; border-top:1px solid rgba(0,0,0,.08); padding-top:7px; }
    .v2-dot     { position:absolute; top:8px; right:10px; font-size:18px; opacity:.9; }
    .v2-meta    { font-size:10.5px; color:var(--text-sub); border-top:1px solid rgba(0,0,0,.07); padding-top:6px; }
    .v2-sidebar { position:sticky; top:112px; background:var(--surface); border:1px solid var(--border); border-radius:6px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.07); }
    .v2-sb-head { background:#f5f6f8; border-bottom:1px solid var(--border); padding:12px 18px; }
    .v2-sb-ttl  { font-size:13px; font-weight:700; color:var(--primary); }
    .v2-sb-sub  { font-size:11px; color:var(--text-sub); margin-top:2px; }
    .v2-sb-body { padding:16px 18px; }
    .v2-summary p { font-size:12.5px; line-height:1.75; color:#2a2a3e; margin-bottom:10px; }
    .v2-summary p:last-child { margin-bottom:0; }
    .v2-summary strong { color:#16163e; }
    .v2-hr      { border:none; border-top:1px solid var(--border); margin:14px 0; }
    .v2-src-lbl { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-sub); margin-bottom:8px; }
    .v2-src     { display:flex; align-items:flex-start; gap:8px; padding:7px 0; border-bottom:1px solid var(--border); cursor:pointer; font-size:12px; line-height:1.4; color:var(--text); transition:color .15s; }
    .v2-src:last-child { border-bottom:none; }
    .v2-src:hover { color:var(--accent); }
    .v2-badge   { font-size:9.5px; font-weight:700; color:#fff; padding:2px 5px; border-radius:3px; white-space:nowrap; flex-shrink:0; margin-top:1px; }
    .v2-rt      { font-size:10.5px; color:var(--text-sub); margin-top:10px; }
    .v2-modal   { display:none; position:fixed; inset:0; z-index:999; background:rgba(0,0,0,.65); align-items:center; justify-content:center; }
    .v2-modal-box { background:#fff; border-radius:10px; overflow:hidden; width:90vw; max-width:940px; height:88vh; display:flex; flex-direction:column; box-shadow:0 12px 48px rgba(0,0,0,.4); animation:mIn .16s ease; }
    @keyframes mIn { from{transform:scale(.94);opacity:0} to{transform:scale(1);opacity:1} }
    .v2-mh { display:flex; align-items:center; gap:12px; padding:10px 18px; background:var(--primary); color:#fff; flex-shrink:0; }
    .v2-mt { font-size:13px; font-weight:600; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .v2-mc { background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.3); color:#fff; border-radius:6px; padding:4px 12px; cursor:pointer; font-size:12px; }
    .v2-mc:hover { background:rgba(255,255,255,.28); }
    .v2-mf { flex:1; border:none; width:100%; }
    @media(max-width:960px){ .v2-wrap{grid-template-columns:1fr;} .v2-sidebar{position:static;} }
    @media(max-width:640px){ .v2-grid{flex-direction:column;} }
"""

_SENDER_CODE = {
    "Eurasia Group": ("EG",  "#8a6200"),
    "POLITICO":      ("POL", "#a8121e"),
    "Jetro":         ("JET", "#007838"),
}

def _sender_code(sender: str):
    return _SENDER_CODE.get(sender, ("OTH", "#444488"))


def _render_v2_card(email: dict) -> str:
    code, _ = _sender_code(email["sender_norm"])
    dot   = '<span class="v2-dot">🚗</span>' if email.get("toyota") else ""
    exc   = f'<div class="v2-excerpt">{e(email["excerpt"])}</div>' if email.get("excerpt") else ""
    subj  = e(email["subject"])
    pdf   = e(email.get("pdf", ""))
    title_attr = e(email["subject"])
    return (
        f'<div class="v2-card" data-s="{code}" data-pdf="{pdf}" '
        f'data-title="{title_attr}" onclick="openPdf(this)">\n'
        f'  {dot}\n'
        f'  <div class="v2-sender">{e(email["sender_norm"])}</div>\n'
        f'  <div class="v2-title">{subj}</div>\n'
        f'  {exc}\n'
        f'  <div class="v2-meta">{e(email["date_label"])} &nbsp;·&nbsp; {email["read_min"]} MIN READ</div>\n'
        f'</div>'
    )


def _render_v2_sidebar(toyota_emails: list, updated_at: str, toyota_summary: str = "") -> str:
    """統合要約（上）＋ソースPDFリンク（下）のサイドバー"""
    if not toyota_emails:
        body = "<p>No automotive-relevant emails today.</p>"
        sources = ""
    else:
        if toyota_summary:
            body = f'<p>{e(toyota_summary)}</p>'
        else:
            # フォールバック: excerpt を並べる
            body = "\n".join(
                f'<p><strong>{e(em["subject"][:55])}.</strong> {e(em["excerpt"] or "")}</p>'
                for em in toyota_emails[:4] if em.get("excerpt")
            ) or "<p>No summary available.</p>"

        src_items = ""
        for em in toyota_emails[:6]:
            code, col = _sender_code(em["sender_norm"])
            src_items += (
                f'<div class="v2-src" onclick="openPdfDirect(\'{e(em["pdf"])}\',\'{e(em["subject"][:60])}\')">'
                f'<span class="v2-badge" style="background:{col};">{e(em["sender_norm"])}</span>'
                f'<span>{e(em["subject"])}</span></div>\n'
            )
        sources = f'<hr class="v2-hr"><div class="v2-src-lbl">Source PDFs</div>\n{src_items}'

    total_min = sum(em.get("read_min", 0) for em in toyota_emails[:6])
    return f"""<div class="v2-sidebar">
  <div class="v2-sb-head">
    <div class="v2-sb-ttl">Today's Key Takeaways</div>
    <div class="v2-sb-sub">{e(updated_at)} &nbsp;·&nbsp; ~1 min read</div>
  </div>
  <div class="v2-sb-body">
    <div class="v2-summary">{body}</div>
    {sources}
    <div class="v2-rt">⏱ Full sources: ~{total_min} min total</div>
  </div>
</div>"""


def generate_mail_v2() -> str:
    if not ROLLING_JSON_PATH.exists():
        # フォールバック: 空ページ
        return f"""{build_head("インテリジェンス", MAIL_V2_CSS)}
<body>{build_header_nav("intelligence")}
<div style="padding:60px 20px;text-align:center;color:#888;">
  データ未生成。mail_slides.py を実行してください。
</div>{build_footer()}</body></html>"""

    try:
        data           = json.loads(ROLLING_JSON_PATH.read_text(encoding="utf-8"))
        emails         = data.get("emails", [])
        upd_at         = data.get("updated_at", "")
        toyota_summary = data.get("toyota_summary", "")
    except Exception:
        emails, upd_at, toyota_summary = [], "", ""

    # 3列に均等分配（新しい順に左列→中列→右列）
    n  = len(emails)
    c1 = (n + 2) // 3      # 切り上げ
    c2 = (n + 1) // 3
    # c3 = n - c1 - c2
    col1 = emails[:c1]
    col2 = emails[c1:c1+c2]
    col3 = emails[c1+c2:]

    col1_html = "\n".join(_render_v2_card(em) for em in col1)
    col2_html = "\n".join(_render_v2_card(em) for em in col2)
    col3_html = "\n".join(_render_v2_card(em) for em in col3)

    toyota_emails = [em for em in emails if em.get("toyota") and em.get("excerpt")]
    sidebar_html  = _render_v2_sidebar(toyota_emails, upd_at, toyota_summary)

    modal_js = """<div id="v2-modal" class="v2-modal">
  <div class="v2-modal-box">
    <div class="v2-mh">
      <span id="v2-mt" class="v2-mt">PDF</span>
      <button onclick="closeModal()" class="v2-mc">✕ 閉じる</button>
    </div>
    <iframe id="v2-mf" class="v2-mf" src="about:blank"></iframe>
  </div>
</div>
<script>
var modal=document.getElementById('v2-modal'),frame=document.getElementById('v2-mf'),ttl=document.getElementById('v2-mt');
function openPdf(c){ttl.textContent=c.dataset.title||'PDF';frame.src=c.dataset.pdf;modal.style.display='flex';}
function openPdfDirect(u,t){ttl.textContent=t||'PDF';frame.src=u;modal.style.display='flex';}
function closeModal(){modal.style.display='none';frame.src='about:blank';}
modal.addEventListener('click',function(e){if(e.target===modal)closeModal();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
</script>"""

    return f"""{build_head("インテリジェンス", MAIL_V2_CSS)}
<body>
{build_header_nav("intelligence", data_updated_at=upd_at)}
<div class="v2-wrap">
  <div>
    <div class="v2-grid">
      <div class="v2-col">{col1_html}</div>
      <div class="v2-col">{col2_html}</div>
      <div class="v2-col">{col3_html}</div>
    </div>
  </div>
  {sidebar_html}
</div>
{build_footer(data_updated_at=upd_at)}
{modal_js}
</body></html>"""


# ═════════════════════════════════════════════════════════════
#  ③ トランプページ生成
# ═════════════════════════════════════════════════════════════
TRUMP_CSS = """
    .trump-wrap { max-width: 1040px; margin: 24px auto; padding: 0 20px; }
    .trump-banner { background: linear-gradient(135deg, #16163e 0%, #3C3B6E 60%, #1a0a0a 100%); border-radius: var(--radius); padding: 18px 24px; margin-bottom: 16px; display: flex; align-items: center; gap: 20px; border: 1px solid #4a3a6e; flex-wrap: wrap; }
    .trump-banner-title { font-size: 22px; font-weight: 700; color: #fff; letter-spacing: .5px; }
    .trump-banner-title span { color: #C81E32; }
    .trump-banner-sub { font-size: 12px; color: rgba(255,255,255,.55); margin-top: 3px; }
    .trump-banner-spacer { flex: 1; }
    .trump-stats { display: flex; gap: 12px; flex-wrap: wrap; }
    .trump-stat { text-align: center; background: rgba(255,255,255,.08); border-radius: 8px; padding: 8px 14px; }
    .trump-stat-num { font-size: 18px; font-weight: 700; color: #B48200; }
    .trump-stat-lbl { font-size: 10px; color: rgba(255,255,255,.5); }
    .source-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
    .source-chip { display: flex; align-items: center; gap: 5px; background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 5px 12px; font-size: 12px; color: var(--text-sub); }
    /* Trump cards */
    .trump-card { background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); border-left: 5px solid var(--accent); box-shadow: 0 1px 4px rgba(0,0,0,.06); padding: 18px 22px; transition: box-shadow .2s; }
    .trump-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); }
    .trump-card.featured { background: linear-gradient(135deg, #fffbe6, #fff8e1); border-left-color: #B48200; border-left-width: 6px; padding: 22px 28px; margin-bottom: 20px; }
    .trump-card.japan-highlight { background: #fff0f2; border-left-color: #C81E32; }
    .trump-card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
    .trump-icon { font-size: 20px; }
    .trump-badge { font-size: 11px; font-weight: 700; color: #fff; padding: 3px 10px; border-radius: 12px; white-space: nowrap; }
    .trump-card-title { font-size: 17px; font-weight: 700; color: var(--text); margin-left: 4px; }
    .trump-card.featured .trump-card-title { font-size: 20px; color: #5a3a00; }
    /* Trump title link */
    .trump-title-link { color: inherit; text-decoration: none; transition: color .15s; }
    .trump-title-link:hover { color: var(--accent); }
    .trump-title-link:hover::after { content: " ↗"; font-size: 13px; opacity: .7; }
    /* Trump bullets */
    .trump-bullets { list-style: none; padding: 0; }
    .trump-bullets li { position: relative; padding-left: 20px; font-size: 13px; color: #2a2a3a; margin-bottom: 9px; line-height: 1.6; }
    .trump-bullets li::before { content: "▸"; position: absolute; left: 0; color: var(--accent); font-weight: 700; }
    .trump-card.featured .trump-bullets li { font-size: 14px; }
    .trump-card.featured .trump-bullets li::before { color: #B48200; }
    .trump-card.japan-highlight .trump-bullets li::before { color: #C81E32; }
    /* trump page の src-tag は accent を赤系に */
    .trump-card .src-tag { background: #fafafa; border-color: #ddd; }
    .trump-card .bullet-link:hover .src-tag { color: #C81E32; background: #fff0f2; border-color: #C81E32; }
    .trump-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
    @media (max-width: 640px) { .trump-wrap { padding: 0 12px; } .trump-banner { padding: 14px; } .trump-banner-title { font-size: 18px; } .trump-stats { display: none; } }
"""

BADGE_COLORS = {"GOLD": "#B48200", "BLUE": "#3C3B6E", "RED": "#C81E32"}

def render_trump_card(sec):
    badge_hex  = BADGE_COLORS.get(sec["color"], "#B48200")
    title_url  = sec.get("title_url", "")

    if title_url:
        title_html = href(title_url, e(sec["title"]), "trump-title-link")
    else:
        title_html = e(sec["title"])

    bullets_html = "\n".join(f"  {render_bullet(b, badge_hex)}" for b in sec["bullets"])

    if sec.get("featured"):
        cls = "trump-card featured"
    elif sec.get("id") == "japan":
        cls = "trump-card japan-highlight"
    else:
        cls = "trump-card"

    return f"""<div class="{cls}" style="--accent:{badge_hex};">
  <div class="trump-card-header">
    <span class="trump-icon">{sec["icon"]}</span>
    <span class="trump-badge" style="background:{badge_hex};">{e(sec["badge"])}</span>
    <span class="trump-card-title">{title_html}</span>
  </div>
  <ul class="trump-bullets">
{bullets_html}
  </ul>
</div>"""

def generate_trump():
    # trump_latest.json があれば実データを使用、なければハードコードのダミーデータ
    _json_data = load_trump_data()
    if _json_data:
        stats, sections = build_trump_sections_from_json(_json_data)
        data_label = f'実データ（{_json_data.get("generated_at","")} 生成）'
    else:
        stats, sections = TRUMP_STATS, TRUMP_SECTIONS
        data_label = "サンプルデータ（trump_monitor.py 未実行）"

    featured = next(s for s in sections if s.get("featured"))
    rest     = [s for s in sections if not s.get("featured")]

    source_chips = "".join(
        f'  <div class="source-chip"><span>{icon}</span>{e(label)}: {e(count)}</div>\n'
        for icon, label, count in stats["sources"]
    )
    grid_html = "\n".join(render_trump_card(s) for s in rest)

    return f"""{build_head("USトランプ", TRUMP_CSS)}
<body>
{build_header_nav("trump")}
<div class="trump-wrap">
  <div class="trump-banner">
    <div>
      <div class="trump-banner-title">TRUMP <span>MONITOR</span></div>
      <div class="trump-banner-sub">対象期間: {e(stats["date_range"])} (UTC)
        &nbsp;|&nbsp; <span style="opacity:.6;font-size:11px;">{e(data_label)}</span>
      </div>
    </div>
    <div class="trump-banner-spacer"></div>
    <div class="trump-stats">
      <div class="trump-stat"><div class="trump-stat-num">{stats["item_count"]}</div><div class="trump-stat-lbl">収集件数</div></div>
      <div class="trump-stat"><div class="trump-stat-num">{len(sections)}</div><div class="trump-stat-lbl">セクション</div></div>
    </div>
  </div>
  <div class="source-bar">
{source_chips}  </div>
  <p class="section-label">主要ポイント</p>
{render_trump_card(featured)}
  <p class="section-label">詳細分析</p>
  <div class="trump-grid">
{grid_html}
  </div>
</div>
{build_footer()}
<script>
document.addEventListener('DOMContentLoaded', () => {{
  const grid = document.querySelector('.trump-grid');
  const jp   = grid && grid.querySelector('.japan-highlight');
  if (jp) grid.appendChild(jp);
}});
</script>
</body></html>"""


# ═════════════════════════════════════════════════════════════
#  ④ 個別テーマページ生成
# ═════════════════════════════════════════════════════════════

THEME_JSON_PATH = Path(__file__).parent / "docs" / "data" / "theme_latest.json"
NEW_BADGE_DAYS  = 3   # この日数以内に追加されたアイテムに NEW バッジを付ける

def load_theme_data() -> dict | None:
    """theme_latest.json が存在すれば読み込んで返す。なければ None。"""
    if not THEME_JSON_PATH.exists():
        return None
    try:
        data = json.loads(THEME_JSON_PATH.read_text(encoding="utf-8"))
        return data if data.get("themes") else None
    except Exception as ex:
        print(f"[WARN] theme_latest.json 読み込み失敗: {ex}")
        return None

THEME_CUTOFF_DATE = (TODAY - timedelta(days=7)).strftime("%Y-%m-%d")

def _is_new(date_str: str) -> bool:
    """date（YYYY-MM-DD）が NEW_BADGE_DAYS 以内なら True"""
    try:
        return date_str >= (TODAY - timedelta(days=NEW_BADGE_DAYS)).strftime("%Y-%m-%d")
    except Exception:
        return False

THEME_CSS = """
    .theme-wrap { max-width: 1040px; margin: 24px auto; padding: 0 20px; }

    /* ── テーマ切り替えタブ ── */
    .theme-tabs-nav {
      display: flex; gap: 6px; flex-wrap: wrap;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 8px 12px;
      margin-bottom: 14px;
    }
    .theme-tab {
      padding: 6px 18px; border-radius: 20px; font-size: 13px; font-weight: 600;
      cursor: pointer; border: 1.5px solid #ccc; background: #fff; color: #555;
      transition: all .15s; white-space: nowrap;
    }
    .theme-tab.active { color: #fff; border-color: transparent; }
    .theme-tab:not(.active):hover { background: #f0f4ff; border-color: #aac; }

    /* ── テーマパネル（--tc = テーマカラー）── */
    .theme-panel { --tc: #003F8A; }

    /* ── バナー ── */
    .theme-banner {
      border-radius: var(--radius); padding: 18px 24px; margin-bottom: 16px;
      display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
    }
    .theme-banner-title { font-size: 20px; font-weight: 700; color: #fff; letter-spacing: .4px; }
    .theme-banner-title span { color: #FFCC00; font-size: 14px; font-weight: 500; }
    .theme-banner-desc { font-size: 11px; color: rgba(255,255,255,.6); margin-top: 3px; }
    .theme-banner-spacer { flex: 1; }
    .theme-stats { display: flex; gap: 12px; flex-wrap: wrap; }
    .theme-stat { text-align: center; background: rgba(255,255,255,.12); border-radius: 8px; padding: 8px 14px; }
    .theme-stat-num { font-size: 18px; font-weight: 700; color: #FFCC00; }
    .theme-stat-lbl { font-size: 10px; color: rgba(255,255,255,.5); }

    /* ── アイテム ── */
    .theme-item {
      background: var(--surface); border-radius: var(--radius);
      border: 1px solid var(--border); border-left: 4px solid var(--tc);
      padding: 14px 18px; margin-bottom: 10px; transition: box-shadow .2s;
    }
    .theme-item:hover { box-shadow: 0 4px 14px rgba(0,0,0,.08); }
    .theme-item.is-new { border-left-color: #F59E0B; background: #fffef0; }

    .theme-item-header { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }
    .theme-new-badge {
      background: #F59E0B; color: #fff; font-size: 10px; font-weight: 700;
      padding: 2px 7px; border-radius: 10px; white-space: nowrap; flex-shrink: 0; margin-top: 2px;
    }
    .theme-src-badge {
      font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px;
      white-space: nowrap; flex-shrink: 0; margin-top: 2px;
    }
    .theme-src-official   { background: #dbeafe; color: #1d4ed8; }
    .theme-src-politician { background: #fff3cd; color: #92400e; }
    .theme-src-industry   { background: #fce7f3; color: #9d174d; }
    .theme-src-china      { background: #fee2e2; color: #991b1b; }
    .theme-src-media      { background: #d1fae5; color: #065f46; }
    .theme-date { font-size: 11px; color: var(--text-sub); flex-shrink: 0; margin-top: 3px; white-space: nowrap; }
    .theme-item-title { font-size: 13px; font-weight: 600; color: var(--text); line-height: 1.5; flex: 1; min-width: 0; }
    .theme-item-title a { color: inherit; text-decoration: none; }
    .theme-item-title a:hover { color: var(--tc); text-decoration: underline; }
    .theme-summary { font-size: 12px; color: var(--text-sub); line-height: 1.75; margin-top: 5px; }
    .theme-source-name { font-size: 11px; color: #aaa; margin-top: 4px; }

    /* ── フィルタバー ── */
    .theme-filter-bar { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 14px; }
    .theme-filter-btn {
      padding: 4px 13px; border-radius: 20px; font-size: 12px; font-weight: 600;
      cursor: pointer; border: 1.5px solid #ccc; background: #fff; color: #555;
      transition: all .15s;
    }
    .theme-filter-btn.active { background: var(--tc); color: #fff; border-color: var(--tc); }
    .theme-filter-btn:not(.active):hover { border-color: var(--tc); color: var(--tc); }

    .theme-empty { text-align: center; color: var(--text-sub); font-size: 13px; padding: 40px 20px; }

    @media (max-width: 640px) {
      .theme-wrap { padding: 0 12px; }
      .theme-banner { padding: 14px; }
      .theme-banner-title { font-size: 16px; }
      .theme-stats { display: none; }
      .theme-tab { font-size: 12px; padding: 5px 12px; }
    }
"""

# source_type → (ラベル, CSSクラス, アイコン)
_SRC_META = {
    "official":   ("公式機関",     "theme-src-official",   "🏛️"),
    "politician":  ("政治家・要人", "theme-src-politician",  "👤"),
    "industry":   ("業界・企業",   "theme-src-industry",    "🏭"),
    "china":      ("中国政府・企業","theme-src-china",       "🇨🇳"),
    "media":      ("メディア",     "theme-src-media",       "📰"),
}

def _render_theme_item(item: dict) -> str:
    date_s   = e(item.get("date", ""))
    title    = e(item.get("title", ""))
    summary  = e(item.get("summary", ""))
    url      = item.get("url", "")
    src_type = item.get("source_type", "media")
    src_name = e(item.get("source", ""))
    is_new   = _is_new(item.get("date", ""))

    src_label, src_cls, src_icon = _SRC_META.get(src_type, ("情報", "theme-src-media", "📄"))

    new_badge = '<span class="theme-new-badge">🆕 NEW</span>' if is_new else ""
    src_badge = f'<span class="theme-src-badge {src_cls}">{src_icon} {src_label}</span>'
    date_span = f'<span class="theme-date">📅 {date_s}</span>'

    if url:
        title_html = (
            f'<span class="theme-item-title">'
            f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{title}</a>'
            f'</span>'
        )
    else:
        title_html = f'<span class="theme-item-title">{title}</span>'

    item_cls = "theme-item is-new" if is_new else "theme-item"
    return f"""<div class="{item_cls}" data-src="{e(src_type)}">
  <div class="theme-item-header">
    {new_badge}{src_badge}{date_span}
    {title_html}
  </div>
  <div class="theme-summary">{summary}</div>
  <div class="theme-source-name">出典: {src_name}</div>
</div>"""


def _render_theme_panel(theme: dict, active: bool, gen_at: str) -> str:
    """1テーマ分のパネル HTML を生成"""
    tid       = e(theme.get("id", ""))
    color     = e(theme.get("color", "#003F8A"))
    icon      = e(theme.get("icon", ""))
    name      = e(theme.get("name", ""))
    name_en   = e(theme.get("name_en", ""))
    desc      = e(theme.get("description", ""))
    last_chk  = e(theme.get("last_checked", gen_at))
    # 7日以内のアイテムのみ表示・日付降順（最新を上）にソート
    all_items = theme.get("items", [])
    items = sorted(
        [it for it in all_items if it.get("date", "") >= THEME_CUTOFF_DATE],
        key=lambda it: it.get("date", ""),
        reverse=True,
    )
    new_count = sum(1 for it in items if _is_new(it.get("date", "")))
    data_note = f"最終収集: {last_chk}" if last_chk else "未収集（次回 GitHub Actions 実行時に更新）"
    display_style = "display:none; " if not active else ""

    # バナー背景色（テーマカラーをベースに暗くする JS なしの簡易対応）
    banner_style = (
        f'style="background:linear-gradient(135deg,{color} 0%,{color}cc 70%,{color}88 100%);"'
    )

    stat_html = (
        f'<div class="theme-stat"><div class="theme-stat-num">{len(items)}</div>'
        f'<div class="theme-stat-lbl">直近7日</div></div>'
        f'<div class="theme-stat"><div class="theme-stat-num">{new_count}</div>'
        f'<div class="theme-stat-lbl">新着（3日）</div></div>'
    )

    # フィルタボタン（そのテーマに存在する source_type のみ表示）
    existing_types = {it.get("source_type","media") for it in items}
    filter_defs = [
        ("all",        "すべて"),
        ("official",   "🏛️ 公式機関"),
        ("politician", "👤 政治家・要人"),
        ("industry",   "🏭 業界・企業"),
        ("china",      "🇨🇳 中国政府・企業"),
        ("media",      "📰 メディア"),
    ]
    filter_btns = ""
    for ftype, flabel in filter_defs:
        if ftype == "all" or ftype in existing_types:
            active_cls = ' active' if ftype == "all" else ""
            filter_btns += (
                f'  <button class="theme-filter-btn{active_cls}" '
                f'data-filter="{ftype}">{flabel}</button>\n'
            )

    items_html = (
        "\n".join(_render_theme_item(it) for it in items)
        if items else
        '<div class="theme-empty">📡 データ収集中です。次回 GitHub Actions 実行時（6時間ごと）に更新されます。</div>'
    )

    return f"""<div id="panel-{tid}" class="theme-panel" style="{display_style}--tc:{color};">
  <div class="theme-banner" {banner_style}>
    <div>
      <div class="theme-banner-title">{icon} {name} <span>{name_en}</span></div>
      <div class="theme-banner-desc">{desc} &nbsp;|&nbsp; <span style="opacity:.7;font-size:10px;">{data_note}</span></div>
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


def generate_theme() -> str:
    data   = load_theme_data()
    gen_at = ""
    themes = []

    if data:
        gen_at = data.get("generated_at", "")
        themes = data.get("themes", [])
        total  = sum(len(t["items"]) for t in themes)
        print(f"[OK] theme_latest.json から {total} 件読み込み（{gen_at}）")

    # データがない場合のプレースホルダー（3テーマ分）
    if not themes:
        themes = [
            {
                "id": "iaa", "name": "欧州産業加速法案（IAA）",
                "name_en": "European Industrial Accelerator Act",
                "description": "欧州委員会・欧州議会の審議動向、EU要人発言、欧州メディア論調を追跡",
                "color": "#003F8A", "icon": "🇪🇺", "last_checked": "", "items": [],
            },
            {
                "id": "cvsa", "name": "米国接続車両安全保障法（S.4429）",
                "name_en": "Connected Vehicle Security Act of 2026",
                "description": "米議会審議・トランプ政権動向・業界団体意見・中国政府反応・メディア論調を追跡",
                "color": "#B22234", "icon": "🚗", "last_checked": "", "items": [],
            },
            {
                "id": "rare_earth", "name": "中国レアアース輸出管理",
                "name_en": "China Rare Earth Export Controls",
                "description": "中国商務省・輸出規制動向、欧米政府・業界の対応、代替調達・備蓄政策を追跡",
                "color": "#1a6b3a", "icon": "⛏️", "last_checked": "", "items": [],
            },
        ]

    # ── テーマ切り替えタブ ──
    tab_btns = ""
    for i, t in enumerate(themes):
        active_cls = " active" if i == 0 else ""
        tc = e(t.get("color", "#333"))
        style = f' style="background:{tc}; border-color:{tc};"' if i == 0 else ""
        tab_btns += (
            f'  <button class="theme-tab{active_cls}" data-theme="{e(t["id"])}"{style}>'
            f'{e(t["icon"])} {e(t["name"])}</button>\n'
        )

    # ── パネル HTML ──
    panels_html = "\n".join(
        _render_theme_panel(t, i == 0, gen_at)
        for i, t in enumerate(themes)
    )

    # テーマ色マップ（JS 用）
    color_map = "{" + ",".join(f'"{e(t["id"])}":"{e(t.get("color","#333"))}"' for t in themes) + "}"

    return f"""{build_head("個別テーマ", THEME_CSS)}
<body>
{build_header_nav("theme")}
<div class="theme-wrap">
  <p class="section-label" style="margin-top:8px;">モニタリングテーマ</p>
  <div class="theme-tabs-nav">
{tab_btns}  </div>
{panels_html}
</div>
{build_footer()}
<script>
(function(){{
  var colorMap = {color_map};

  // ── テーマタブ切り替え ──
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

  // ── フィルタボタン（パネルごとに独立）──
  panels.forEach(function(panel){{
    var tc    = panel.style.getPropertyValue('--tc') || '#003F8A';
    var btns  = panel.querySelectorAll('.theme-filter-btn');
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
</body></html>"""


# ═════════════════════════════════════════════════════════════
#  エントリーポイント
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    out_dir = Path(__file__).parent / "docs"
    out_dir.mkdir(exist_ok=True)

    pages = [
        ("index.html",        generate_home,     "Home"),
        ("mail.html",         generate_mail,     "Mail Summary"),
        ("intelligence.html", generate_mail_v2,  "Intelligence"),
        ("trump.html",        generate_trump,    "Trump Monitor"),
        ("theme.html",        generate_theme,    "個別テーマ"),
    ]
    for filename, gen_fn, label in pages:
        out_path = out_dir / filename
        out_path.write_text(gen_fn(), encoding="utf-8")
        print(f"[OK] {label:16s} -> {out_path.name}")

    print()
    print(f"    Open: file:///{(out_dir / 'index.html').resolve().as_posix()}")
    print()
    print("    Link behavior:")
    print("    - Card title    -> Google News search (new tab)")
    print("    - Bullet [SRC^] -> Original source URL (new tab)")
    print("    - Trump titles  -> WH/TruthSocial/YouTube (new tab)")
