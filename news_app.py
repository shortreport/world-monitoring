#!/usr/bin/env python3
"""
World News Dashboard — Port 5002
NHK / BBC / CNN / Nikkei Asia / FT / Fox News / ABC / ZDF / Al Jazeera / TVB / CNA
各RSSフィードを直接取得し、キーワードでトピック別にフィルタリングして表示する。
APIキー不要。
"""
import re, sys, json, os, threading, time, logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import requests
import feedparser
from flask import Flask, jsonify, request as flask_request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── 設定 ─────────────────────────────────────────────────────────────────────
REFRESH       = 21600  # 秒（6時間）— RSS制限なし
MAX_ART       = 20    # トピックごとの最大表示件数
JP_MAX        = 10    # 日本語メディアの上限（英字が足りない場合は追加可）
EN_MAX        = 10    # 英字メディアの上限
HISTORY_HOURS = 24    # 記事を何時間分蓄積するか（英字メディア対策）

JP_SOURCES = {"NHK", "日経", "産経", "毎日"}  # 日本語メディアの識別子

try:
    from api_config import GEMINI_API_KEY as _gemini_key
except ImportError:
    _gemini_key = ""
GEMINI_KEY = _gemini_key or os.environ.get("GEMINI_API_KEY", "")

# ── 日本語メディア RSSフィード（直接取得） ────────────────────────────────────
JP_FEEDS = [
    {"source": "NHK",  "name": "NHK トップ",       "url": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    {"source": "NHK",  "name": "NHK 国際",         "url": "https://www3.nhk.or.jp/rss/news/cat6.xml"},
    {"source": "NHK",  "name": "NHK 政治",         "url": "https://www3.nhk.or.jp/rss/news/cat4.xml"},
    {"source": "NHK",  "name": "NHK 経済",         "url": "https://www3.nhk.or.jp/rss/news/cat7.xml"},
    {"source": "日経", "name": "日経（Google経由）", "url": "https://news.google.com/rss/search?q=site:nikkei.com&hl=ja&gl=JP&ceid=JP:ja"},
    {"source": "産経", "name": "産経（Google経由）", "url": "https://news.google.com/rss/search?q=site:sankei.com&hl=ja&gl=JP&ceid=JP:ja"},
    {"source": "毎日", "name": "毎日新聞",          "url": "https://mainichi.jp/rss/etc/mainichi-flash.rss"},
]

# ── 英字メディア：トピック別 Google News キーワード検索 ────────────────────────
# Google News RSSはキーワードに合致した記事のみ返す（BBC/CNN/Reuters/FT等を横断）
# entry.source.titleで元メディア名を取得
EN_TOPIC_QUERIES = {
    "日米関係": [
        "Japan US relations trade",
        "Japan America alliance tariffs",
        "Ishiba Trump bilateral",
    ],
    "米中関係": [
        "US China relations trade war",
        "China tariffs decoupling sanctions",
        "Xi Trump Beijing Washington",
    ],
    "米イラン関係": [
        "US Iran relations sanctions",
        "Iran nuclear deal JCPOA",
        "Iran America tensions",
    ],
    "台湾関係": [
        "Taiwan China US relations",
        "Taiwan strait military tensions",
        "Taiwan TSMC semiconductor",
    ],
    "自動車産業": [
        "automotive industry electric vehicle 2025",
        "auto tariffs EV market",
        "Toyota Volkswagen Tesla Ford",
    ],
}

def _gnews_url(query: str) -> str:
    import urllib.parse
    # after: フィルタで2日以内の記事のみ取得
    after_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    return f"https://news.google.com/rss/search?q={urllib.parse.quote(query + ' after:' + after_date)}&hl=en&gl=US&ceid=US:en"

# ── トピック定義 ──────────────────────────────────────────────────────────────
TOPICS = {
    "日米関係": {
        "label": "日米関係 / Japan–US Relations",
        "badge": "JP/US",
        "color": "#00c8ff",
        "keywords": [
            # 英語
            "japan-us", "us-japan", "japan us ", " us japan",
            "japan america", "japan-usa", "usa-japan",
            "japan tariff", "japan trade", "japan alliance",
            "tokyo washington", "quad", "ishiba trump",
            "okinawa base", "us forces japan", "japan defense",
            # 日本語
            "日米", "日本とアメリカ", "日米同盟", "日米首脳",
            "日米貿易", "在日米軍", "石破トランプ", "日米関係",
            "対米", "日本の関税", "日米安保",
        ],
    },
    "米中関係": {
        "label": "米中関係 / US–China Relations",
        "badge": "US/CN",
        "color": "#ffbe30",
        "keywords": [
            # 英語
            "us-china", "china-us", "us china ", " china us",
            "sino-american", "china tariff", "china trade",
            "trade war", "beijing washington", "xi trump",
            "china sanction", "decoupling", "chip ban china",
            # 日本語
            "米中", "中国とアメリカ", "米中関係", "米中貿易",
            "中国の関税", "貿易戦争", "習近平", "中国制裁",
            "対中", "中国包囲", "デカップリング",
        ],
    },
    "米イラン関係": {
        "label": "米イラン関係 / US–Iran Relations",
        "badge": "US/IR",
        "color": "#ff3050",
        "keywords": [
            # 英語
            "us-iran", "iran-us", "us iran", "iran us",
            "iran sanction", "iran nuclear", "iran deal", "jcpoa",
            "tehran washington", "iran america", "irgc",
            "iran oil", "iran missile",
            # 日本語
            "イラン", "イランと米国", "イラン核", "イラン制裁",
            "核合意", "ホルムズ", "イラン情勢", "対イラン",
        ],
    },
    "台湾関係": {
        "label": "台湾関係 / Taiwan Relations",
        "badge": "TW",
        "color": "#ff9040",
        "keywords": [
            # 英語
            "taiwan", "taipei", "taiwan strait",
            "tsmc", "cross-strait", "prc taiwan",
            "taiwan independence", "taiwan military",
            # 日本語
            "台湾", "台湾海峡", "中台", "台湾有事",
            "台湾問題", "台湾防衛", "台湾独立", "ＴＳＭＣ",
        ],
    },
    "自動車産業": {
        "label": "自動車産業 / Automotive Industry",
        "badge": "AUTO",
        "color": "#30ff80",
        "keywords": [
            # 英語
            "automotive", "automobile industry", "auto industry",
            "electric vehicle", " bev ", "car tariff", "auto tariff",
            "toyota", "volkswagen", "ford motor", "general motors",
            "tesla", "hyundai motor", "bmw", "mercedes-benz",
            "stellantis", "nissan", "honda motor", "byd",
            "ev market", "car sales", "auto show",
            # 日本語
            "自動車", "電気自動車", "ＥＶ", "自動車産業",
            "自動車関税", "トヨタ", "ホンダ", "日産",
            "自動車メーカー", "ハイブリッド", "自動運転",
            "自動車輸出", "カーボンニュートラル",
        ],
    },
}

# ── RSS取得 ───────────────────────────────────────────────────────────────────
_TAG_RE = re.compile(r"<[^>]+>")

def fetch_feed(feed_info: dict, use_entry_source: bool = False) -> list[dict]:
    """1フィードをタイムアウト付きで取得し記事リストを返す"""
    arts = []
    try:
        resp = requests.get(
            feed_info["url"],
            headers={"User-Agent": "WorldNewsDash/1.0"},
            timeout=8,
        )
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
        for entry in parsed.entries:
            title = (getattr(entry, "title", "") or "").strip()
            link  = getattr(entry, "link",  "") or ""
            if not title or not link:
                continue
            summary = _TAG_RE.sub("", getattr(entry, "summary", "") or "").strip()
            pub_str = getattr(entry, "published", None)
            if pub_str:
                try:
                    pub = parsedate_to_datetime(pub_str).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    pub = pub_str[:16]
            else:
                pub = ""
            # Google News検索結果は各entryに元メディア名が入っている
            if use_entry_source:
                src = (getattr(entry, "source", None) or {}).get("title", "") or feed_info["source"]
            else:
                src = feed_info["source"]
            arts.append({
                "title":    title,
                "url":      link,
                "source":   src,
                "published": pub,
                "summary":  summary[:500],
                "haystack": (title + " " + summary).lower(),
            })
        if arts:
            logger.info("  %-28s %d件", feed_info["name"], len(arts))
    except Exception as exc:
        logger.warning("Feed error [%s]: %s", feed_info["name"], exc)
    return arts


def fetch_all_articles() -> list[dict]:
    """日本語フィード（直接RSS）＋英字（Google Newsトピック検索）を並列取得"""
    all_arts = []

    # 英字：トピック別Google News検索フィードを生成
    en_feeds = []
    for topic, queries in EN_TOPIC_QUERIES.items():
        for q in queries:
            en_feeds.append({
                "name": f"EN/{topic[:4]}: {q[:30]}",
                "url":  _gnews_url(q),
                "source": "EN-Search",  # use_entry_source=Trueで上書きされる
                "_topic_hint": topic,
            })

    with ThreadPoolExecutor(max_workers=12) as ex:
        # 日本語フィード
        jp_futures = {ex.submit(fetch_feed, f, False): f for f in JP_FEEDS}
        # 英字フィード（元メディア名を使用）
        en_futures = {ex.submit(fetch_feed, f, True): f for f in en_feeds}

        for future in as_completed({**jp_futures, **en_futures}):
            all_arts.extend(future.result())

    logger.info("合計取得: %d件", len(all_arts))
    return all_arts


def filter_by_topic(articles: list[dict], keywords: list[str]) -> list[dict]:
    seen = set()
    kws_lower = [kw.lower() for kw in keywords]
    jp_matched, en_matched = [], []
    cutoff_48h = datetime.utcnow() - timedelta(hours=48)

    for art in articles:
        if not any(kw in art["haystack"] for kw in kws_lower):
            continue
        # 日付フィルタ: publishedが取れる記事は48時間以内のみ
        pub = art.get("published", "")
        if pub:
            try:
                pub_dt = datetime.strptime(pub[:16], "%Y-%m-%d %H:%M")
                if pub_dt < cutoff_48h:
                    continue  # 古い記事を除外
            except ValueError:
                pass  # パース失敗は通す
        key = art["title"][:60].lower()
        if key in seen:
            continue
        seen.add(key)
        entry = {
            "title":     art["title"],
            "url":       art["url"],
            "source":    art["source"],
            "published": art["published"],
            "summary":   art.get("summary", ""),
        }
        if art["source"] in JP_SOURCES:
            jp_matched.append(entry)
        else:
            en_matched.append(entry)

    # 英字上限10件、日本語上限10件
    jp_out = jp_matched[:JP_MAX]
    en_out = en_matched[:EN_MAX]

    # 英字が10件未満なら日本語で残枠を埋める（合計最大MAX_ART）
    shortage = MAX_ART - len(jp_out) - len(en_out)
    if shortage > 0 and len(jp_matched) > JP_MAX:
        jp_out += jp_matched[JP_MAX: JP_MAX + shortage]

    result = jp_out + en_out

    # 最新順（published降順）。日付なしは末尾
    result.sort(key=lambda a: a.get("published", ""), reverse=True)
    return result[:MAX_ART]


# ── 記事履歴（24時間分蓄積） ──────────────────────────────────────────────────
_article_history: list[dict] = []

def update_article_history(new_articles: list[dict]) -> list[dict]:
    """新規記事を履歴に追加し、HISTORY_HOURS時間より古い記事を削除する"""
    global _article_history
    now_ts  = time.time()
    cutoff  = now_ts - HISTORY_HOURS * 3600
    new_titles = {a["title"][:60].lower() for a in new_articles}
    for art in new_articles:
        art["_fetched_ts"] = now_ts
    # 古い記事＆新規と重複する記事を除去してから新規を追加
    kept = [a for a in _article_history
            if a.get("_fetched_ts", 0) > cutoff
            and a["title"][:60].lower() not in new_titles]
    _article_history = kept + new_articles
    logger.info("記事履歴合計: %d件（今回新規: %d件）", len(_article_history), len(new_articles))
    return list(_article_history)


def get_all_news(articles: list[dict]) -> dict:
    out = {}
    for topic, cfg in TOPICS.items():
        out[topic] = filter_by_topic(articles, cfg["keywords"])
        logger.info("  [%s] %d件", topic, len(out[topic]))
    return out

# ── Gemini 一括翻訳（フェッチ時に全記事まとめて1〜2回で処理） ────────────────
BATCH_SIZE = 20   # 1リクエストあたりの最大記事数

def batch_translate(news: dict) -> dict:
    """全記事をバッチでGemini翻訳。1時間ごとに最大2回のAPIコール。"""
    if not GEMINI_KEY or GEMINI_KEY.startswith("ここに"):
        return news

    # フラットリスト化（topic, idx の対応を記録）
    flat, index_map = [], []
    for topic, arts in news.items():
        for i, art in enumerate(arts):
            flat.append(art)
            index_map.append((topic, i))

    if not flat:
        return news

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)

        for batch_start in range(0, len(flat), BATCH_SIZE):
            batch     = flat[batch_start: batch_start + BATCH_SIZE]
            arts_text = ""
            for idx, art in enumerate(batch, 1):
                body = (art.get("summary") or art["title"])[:400]
                arts_text += f"--- 記事{idx} ---\nタイトル: {art['title']}\n本文: {body}\n\n"

            prompt = (
                "以下の記事リストを日本語に翻訳・要約してください。\n"
                "必ず下記JSON形式のみで返してください（前置き・```不要）:\n"
                '[{"id":1,"title_ja":"日本語タイトル","bullets":["要点1","要点2","要点3"]}, ...]\n\n'
                "ルール:\n"
                "- title_ja: 自然な日本語訳\n"
                "- bullets: 重要ポイント3〜5項目、各50字以内の日本語\n"
                "- idは記事番号と一致させること\n\n"
                + arts_text
            )
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            raw  = resp.text.strip().replace("```json", "").replace("```", "").strip()
            results    = json.loads(raw)
            result_map = {item["id"]: item for item in results}

            for local_idx, art in enumerate(batch, 1):
                flat_idx       = batch_start + local_idx - 1
                topic, art_idx = index_map[flat_idx]
                item           = result_map.get(local_idx, {})
                news[topic][art_idx]["title_ja"] = item.get("title_ja") or art["title"]
                news[topic][art_idx]["bullets"]  = item.get("bullets")  or []

            if batch_start + BATCH_SIZE < len(flat):
                time.sleep(1)   # バッチ間のレート制限対策

        logger.info("Gemini 一括翻訳完了: %d件", len(flat))

    except Exception as exc:
        err = str(exc)
        if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
            logger.warning("Gemini 無料枠超過 — 今回は英語のまま表示します")
        else:
            logger.warning("Gemini batch error: %s", exc)

    return news

# ── キャッシュ ────────────────────────────────────────────────────────────────
_cache = {"articles": {}, "updated": None}
_lock  = threading.Lock()

def bg_loop():
    while True:
        logger.info("=== World News 取得開始 ===")
        try:
            new_articles = fetch_all_articles()
            articles     = update_article_history(new_articles)
            news         = get_all_news(articles)
            logger.info("=== Gemini 翻訳開始 ===")
            news = batch_translate(news)
            with _lock:
                _cache["articles"] = news
                _cache["updated"]  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info("=== 取得完了 ===")
        except Exception as exc:
            logger.error("bg_loop error: %s", exc)
        time.sleep(REFRESH)

# ── Flask ─────────────────────────────────────────────────────────────────────
app = Flask(__name__)

SOURCES_LABEL = "NHK・日経・産経・毎日 ／ BBC・CNN・Reuters・FT・Al Jazeera 他（Google News横断検索）"

@app.route("/api/news")
def api_news():
    with _lock:
        return jsonify(dict(_cache))


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """強制リフレッシュ（同期）— make_news_video2.py から呼び出す"""
    logger.info("=== 強制リフレッシュ要求を受信 ===")
    try:
        new_articles = fetch_all_articles()
        articles     = update_article_history(new_articles)
        news         = get_all_news(articles)
        news         = batch_translate(news)
        with _lock:
            _cache["articles"] = news
            _cache["updated"]  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("=== 強制リフレッシュ完了 ===")
        return jsonify({"status": "ok", "updated": _cache["updated"]})
    except Exception as exc:
        logger.error("api_refresh error: %s", exc)
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/")
def index():
    topics_js = str([
        {"key": k, "label": v["label"], "badge": v["badge"], "color": v["color"]}
        for k, v in TOPICS.items()
    ])
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>World News</title>
<style>
:root{{
  --bg:#04040c;--panel:#09091e;
  --border:#141430;--border2:#1e1e42;
  --text:#a8a8cc;--dim:#3a3a68;
  --green:#30ff80;--cyan:#00c8ff;
  --hh:52px;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;overflow:hidden}}
body{{
  display:flex;flex-direction:column;
  background:var(--bg);
  background-image:
    linear-gradient(rgba(0,60,120,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,60,120,.04) 1px,transparent 1px);
  background-size:48px 48px;
  color:var(--text);
  font-family:'Segoe UI','Noto Sans JP',system-ui,sans-serif;font-size:12px;
}}
body::after{{
  content:'';position:fixed;inset:0;z-index:8000;
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.04) 3px,rgba(0,0,0,.04) 4px);
  pointer-events:none;
}}
header{{
  flex-shrink:0;height:var(--hh);z-index:500;
  background:rgba(4,4,15,.98);border-bottom:1px solid var(--border2);
  display:flex;align-items:center;padding:0 16px;gap:12px;
}}
.logo{{font-size:17px;font-weight:900;color:#fff;white-space:nowrap;letter-spacing:.5px}}
.logo em{{color:var(--cyan);font-style:normal}}
.sep{{width:1px;height:28px;background:var(--border2);flex-shrink:0}}
.sources{{font-size:9px;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.live-badge{{
  display:flex;align-items:center;gap:5px;
  font-size:10px;font-weight:800;letter-spacing:2px;color:var(--green);
  border:1px solid rgba(48,255,128,.3);border-radius:4px;padding:3px 10px;flex-shrink:0;
}}
.live-dot{{
  width:7px;height:7px;border-radius:50%;
  background:var(--green);box-shadow:0 0 8px var(--green);
  animation:blink .9s ease-in-out infinite;
}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.15}}}}
.upd-label{{font-size:10px;color:var(--dim);margin-left:auto;white-space:nowrap}}
#pbar{{flex-shrink:0;height:2px;background:var(--border)}}
#pfill{{height:100%;transform-origin:left;background:linear-gradient(90deg,var(--cyan),var(--green));transition:transform 1s linear}}
.grid{{
  flex:1;min-height:0;
  display:grid;grid-template-columns:repeat(5,1fr);
  gap:1px;background:var(--border);overflow:hidden;
}}
.panel{{background:var(--panel);display:flex;flex-direction:column;overflow:hidden}}
.panel-bar{{
  flex-shrink:0;height:30px;
  display:flex;align-items:center;gap:7px;
  padding:0 10px;background:rgba(0,0,0,.5);
  border-bottom:1px solid var(--border2);
  white-space:nowrap;overflow:hidden;
}}
.pdot{{width:7px;height:7px;border-radius:50%;flex-shrink:0;animation:blink .9s ease-in-out infinite}}
.pbadge{{
  font-size:8px;font-weight:800;letter-spacing:1px;
  padding:1px 5px;border-radius:3px;font-family:'Consolas',monospace;
  border:1px solid currentColor;flex-shrink:0;
}}
.pname{{font-size:11px;font-weight:700;overflow:hidden;text-overflow:ellipsis}}
.panel-body{{flex:1;overflow-y:auto;padding:3px 8px;min-height:0}}
.panel-body::-webkit-scrollbar{{width:6px}}
.panel-body::-webkit-scrollbar-track{{background:rgba(255,255,255,.04)}}
.panel-body::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.25);border-radius:3px}}
.panel-body::-webkit-scrollbar-thumb:hover{{background:rgba(255,255,255,.45)}}
.art{{padding:6px 0;border-bottom:1px solid var(--border)}}
.art:last-child{{border-bottom:none}}
.art-title{{display:block;font-size:11px;color:var(--text);text-decoration:none;line-height:1.45;transition:color .15s}}
.art-title:hover{{color:#fff}}
.art-meta{{font-size:9px;color:var(--dim);margin-top:2px}}
.art-src{{
  display:inline-block;font-size:8px;font-weight:700;letter-spacing:.5px;
  padding:1px 4px;border-radius:2px;margin-right:4px;
  background:rgba(255,255,255,.07);color:var(--text);
}}
.empty{{padding:12px 8px;color:var(--dim);font-size:11px}}
footer{{
  flex-shrink:0;background:rgba(4,4,15,.98);border-top:1px solid var(--border);
  padding:4px 16px;font-size:9px;color:var(--dim);
  display:flex;align-items:center;gap:16px;
}}

/* ── モーダル ── */
#modal-overlay{{
  display:none;position:fixed;inset:0;z-index:9000;
  background:rgba(0,0,0,.72);
  align-items:center;justify-content:center;
}}
#modal-overlay.show{{display:flex}}
#modal-box{{
  background:#0e0e26;border:1px solid var(--border2);border-radius:8px;
  width:420px;max-width:92vw;max-height:80vh;
  display:flex;flex-direction:column;
  box-shadow:0 8px 40px rgba(0,0,0,.9);
  animation:modal-in .18s ease;
}}
@keyframes modal-in{{from{{opacity:0;transform:scale(.94)}}to{{opacity:1;transform:scale(1)}}}}
#modal-header{{
  padding:14px 16px 10px;border-bottom:1px solid var(--border);
}}
#modal-title{{
  font-size:13px;font-weight:700;color:#fff;line-height:1.5;margin:0;
}}
#modal-meta{{font-size:9px;color:var(--dim);margin-top:4px}}
#modal-body{{
  flex:1;overflow-y:auto;padding:12px 16px;
}}
#modal-body::-webkit-scrollbar{{width:3px}}
#modal-body::-webkit-scrollbar-thumb{{background:var(--border2)}}
#modal-body ul{{padding-left:16px;margin:0}}
#modal-body li{{
  font-size:11px;color:var(--text);line-height:1.7;
  margin-bottom:4px;
}}
#modal-body li:last-child{{margin-bottom:0}}
.modal-no-summary{{font-size:11px;color:var(--dim);font-style:italic}}
.modal-loading{{
  display:flex;align-items:center;gap:10px;
  padding:8px 0;font-size:11px;color:var(--dim);
}}
.modal-spinner{{
  width:16px;height:16px;border-radius:50%;flex-shrink:0;
  border:2px solid var(--border2);border-top-color:var(--cyan);
  animation:spin .7s linear infinite;
}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
#modal-footer{{
  padding:12px 16px;border-top:1px solid var(--border);
  display:flex;align-items:center;gap:8px;
}}
.modal-q{{font-size:11px;color:var(--text);margin-right:auto}}
.btn-go{{
  background:rgba(0,200,255,.15);border:1px solid var(--cyan);
  color:var(--cyan);font-size:11px;font-weight:700;
  padding:5px 14px;border-radius:4px;cursor:pointer;
  transition:background .15s;white-space:nowrap;
}}
.btn-go:hover{{background:rgba(0,200,255,.28)}}
.btn-close{{
  background:transparent;border:1px solid var(--border2);
  color:var(--dim);font-size:11px;font-weight:700;
  padding:5px 14px;border-radius:4px;cursor:pointer;
  transition:background .15s;white-space:nowrap;
}}
.btn-close:hover{{background:rgba(255,255,255,.06)}}
</style>
</head>
<body>
<header>
  <div class="logo">&#127758; World <em>News</em></div>
  <div class="sep"></div>
  <div class="sources">{SOURCES_LABEL}</div>
  <div class="sep"></div>
  <div class="live-badge"><span class="live-dot"></span>LIVE</div>
  <div class="upd-label" id="upd">取得中...</div>
</header>
<div id="pbar"><div id="pfill"></div></div>

<div class="grid" id="grid">
  <div style="grid-column:1/-1;padding:24px;text-align:center;color:var(--dim)">データ取得中 / Loading...</div>
</div>

<!-- モーダル -->
<div id="modal-overlay">
  <div id="modal-box">
    <div id="modal-header">
      <p id="modal-title"></p>
      <div id="modal-meta"></div>
    </div>
    <div id="modal-body"></div>
    <div id="modal-footer">
      <span class="modal-q">外部サイトへ移動しますか？</span>
      <button class="btn-go"    onclick="gotoSite()">はい（外部サイトへ）</button>
      <button class="btn-close" onclick="closeModal()">閉じる</button>
    </div>
  </div>
</div>

<footer>
  <span>ソース: {SOURCES_LABEL}</span>
  <span>自動更新: {REFRESH // 3600}時間ごと</span>
  <span id="ft-upd"></span>
</footer>

<script>
const TOPICS      = {topics_js};
const DATA_REFRESH = {REFRESH};
const UI_POLL      = 30;

let remaining = DATA_REFRESH;
const pfill = document.getElementById('pfill');
pfill.style.transform = 'scaleX(1)';
setInterval(() => {{
  remaining = Math.max(0, remaining - 1);
  pfill.style.transform = `scaleX(${{remaining / DATA_REFRESH}})`;
}}, 1000);

function esc(s) {{
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

/* ── モーダル ── */
let _currentUrl = '#';

function closeModal() {{
  document.getElementById('modal-overlay').classList.remove('show');
}}

function gotoSite() {{
  window.open(_currentUrl, '_blank', 'noopener');
  closeModal();
}}

document.getElementById('modal-overlay').addEventListener('click', function(e) {{
  if (e.target === this) closeModal();
}});

function openByIndex(el) {{
  const topic = el.dataset.topic;
  const idx   = parseInt(el.dataset.idx, 10);
  const a     = (_artStore[topic] || [])[idx];
  if (!a) return;

  _currentUrl = a.url || '#';
  document.getElementById('modal-title').textContent = a.title_ja || a.title;
  document.getElementById('modal-meta').innerHTML =
    (a.source   ? `<span class="art-src">${{esc(a.source)}}</span>` : '') +
    (a.published ? ' ' + esc(a.published) : '');
  const bullets = a.bullets || [];
  document.getElementById('modal-body').innerHTML = bullets.length
    ? '<ul>' + bullets.map(b => `<li>${{esc(b)}}</li>`).join('') + '</ul>'
    : '<p class="modal-no-summary">（要約なし）</p>';
  document.getElementById('modal-overlay').classList.add('show');
}}

/* ── グリッド描画 ── */
let _artStore = {{}};  // トピックキー → 記事配列

function renderGrid(articles) {{
  _artStore = articles || {{}};
  let html = '';
  TOPICS.forEach(t => {{
    const arts = _artStore[t.key] || [];
    html += `<div class="panel">
      <div class="panel-bar" style="border-left:3px solid ${{t.color}}">
        <span class="pdot" style="background:${{t.color}};box-shadow:0 0 5px ${{t.color}}"></span>
        <span class="pbadge" style="color:${{t.color}}">${{esc(t.badge)}}</span>
        <span class="pname" style="color:${{t.color}}">${{esc(t.label.split('/')[0].trim())}}</span>
      </div>
      <div class="panel-body">
        ${{arts.length
          ? arts.map((a, i) => `<div class="art">
              <a class="art-title" href="#"
                data-topic="${{t.key}}" data-idx="${{i}}"
                onclick="event.preventDefault();openByIndex(this)"
              >${{esc(a.title)}}</a>
              <div class="art-meta">
                ${{a.source ? `<span class="art-src">${{esc(a.source)}}</span>` : ''}}
                ${{a.published ? esc(a.published) : ''}}
              </div>
            </div>`).join('')
          : '<div class="empty">該当記事なし / No results</div>'
        }}
      </div>
    </div>`;
  }});
  document.getElementById('grid').innerHTML = html;
}}

/* ── データ取得ループ ── */
async function refresh() {{
  try {{
    const res  = await fetch('/api/news');
    const data = await res.json();
    renderGrid(data.articles || {{}});
    if (data.updated) {{
      const t = '更新: ' + data.updated;
      document.getElementById('upd').textContent = t;
      document.getElementById('ft-upd').textContent = t;
      document.title = 'World News — ' + data.updated.slice(11, 16);
    }}
  }} catch(e) {{
    console.error('refresh error:', e);
  }}
}}

refresh();
setInterval(refresh, UI_POLL * 1000);
</script>
</body>
</html>"""

if __name__ == "__main__":
    threading.Thread(target=bg_loop, daemon=True).start()
    app.run(host="127.0.0.1", port=5002, debug=False, use_reloader=False)
