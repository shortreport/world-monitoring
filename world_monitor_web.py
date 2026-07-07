#!/usr/bin/env python3
"""
World Monitor Web (ワールドモニター Web版)
Flask ベース世界情勢・市場価格ダッシュボード

使い方 / Usage:
  python world_monitor_web.py
  → ブラウザが自動で http://localhost:5000 を開きます
"""

import logging
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime
from typing import Optional

import feedparser
import yfinance as yf
from flask import Flask, jsonify, render_template

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 設定 / Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MAX_ARTICLES = 6
REFRESH_INTERVAL = 300  # 秒

TOPICS: dict = {
    "日米関係": {
        "label_en": "Japan-US Relations",
        "queries": [
            "Japan US relations 2025",
            "US Japan trade alliance tariffs",
            "日米同盟 関係",
        ],
        "color": "#00c8ff",
        "icon": "JP/US",
        "css_class": "topic-japan-us",
    },
    "米中関係": {
        "label_en": "US-China Relations",
        "queries": [
            "US China relations 2025",
            "China tariffs trade war",
            "Sino-American diplomacy",
        ],
        "color": "#ffc840",
        "icon": "US/CN",
        "css_class": "topic-us-china",
    },
    "米イラン関係": {
        "label_en": "US-Iran Relations",
        "queries": [
            "US Iran relations 2025",
            "Iran sanctions nuclear deal",
            "Iran United States diplomacy",
        ],
        "color": "#ff4060",
        "icon": "US/IR",
        "css_class": "topic-us-iran",
    },
    "自動車産業": {
        "label_en": "Automotive Industry",
        "queries": [
            "automotive industry 2025",
            "electric vehicle EV news manufacturer",
            "auto tariffs car industry",
        ],
        "color": "#40ff90",
        "icon": "AUTO",
        "css_class": "topic-auto",
    },
}

ENERGY_TICKERS: dict[str, tuple[str, str]] = {
    "WTI 原油": ("CL=F", "USD/bbl"),
    "ブレント原油": ("BZ=F", "USD/bbl"),
    "天然ガス (HH)": ("NG=F", "USD/MMBtu"),
    "灯油": ("HO=F", "USD/gal"),
    "ガソリン RBOB": ("RB=F", "USD/gal"),
}

RARE_EARTH_TICKERS: dict[str, tuple[str, str]] = {
    "REMX レアアース ETF": ("REMX", "USD"),
    "MP Materials (Nd採掘)": ("MP", "USD"),
    "Energy Fuels (UUUU)": ("UUUU", "USD"),
    "Lynas RE (ADR)": ("LYSCF", "USD"),
    "Albemarle リチウム": ("ALB", "USD"),
    "SQM リチウム化合物": ("SQM", "USD"),
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データ取得 / Data Fetching
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _rss_fetch(query: str, lang: str = "en", n: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    if lang == "ja":
        url = f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja"
    else:
        url = f"https://news.google.com/rss/search?q={q}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "WorldMonitor/1.0"})
        return [
            {
                "title":     e.get("title", "").strip(),
                "source":    e.get("source", {}).get("title", ""),
                "published": e.get("published", ""),
                "link":      e.get("link", ""),
            }
            for e in feed.entries[:n]
            if e.get("title", "").strip()
        ]
    except Exception:
        return []


def fetch_topic_news(config: dict) -> list[dict]:
    seen: set[str] = set()
    results: list[dict] = []
    for query in config["queries"]:
        is_ja = any(ord(c) > 0x3000 for c in query)
        for art in _rss_fetch(query, lang="ja" if is_ja else "en", n=4):
            key = art["title"][:60].lower()
            if key not in seen:
                seen.add(key)
                results.append(art)
            if len(results) >= MAX_ARTICLES:
                return results
    return results


def fetch_price(ticker: str) -> Optional[dict]:
    try:
        fi = yf.Ticker(ticker).fast_info
        price = fi.last_price
        prev  = fi.previous_close
        if price and prev and prev != 0:
            change = price - prev
            return {"price": price, "change": change, "chg_pct": change / prev * 100}
    except Exception:
        pass
    return None


def fetch_all() -> tuple[dict, list, list]:
    news: dict = {}
    for name, cfg in TOPICS.items():
        news[name] = fetch_topic_news(cfg)

    energy: list = []
    for display_name, (ticker, unit) in ENERGY_TICKERS.items():
        d = fetch_price(ticker)
        energy.append({
            "name":    display_name,
            "ticker":  ticker,
            "unit":    unit,
            "price":   d["price"]   if d else None,
            "change":  d["change"]  if d else None,
            "chg_pct": d["chg_pct"] if d else None,
        })

    rare: list = []
    for display_name, (ticker, unit) in RARE_EARTH_TICKERS.items():
        d = fetch_price(ticker)
        rare.append({
            "name":    display_name,
            "ticker":  ticker,
            "unit":    unit,
            "price":   d["price"]   if d else None,
            "change":  d["change"]  if d else None,
            "chg_pct": d["chg_pct"] if d else None,
        })

    return news, energy, rare


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# キャッシュ & バックグラウンドスレッド / Cache & Background Thread
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_cache: dict = {"news": {}, "energy": [], "rare": [], "last_updated": None}
_lock = threading.Lock()


def _bg_refresh() -> None:
    """初回は即座に取得、以降は REFRESH_INTERVAL 秒ごとに更新"""
    while True:
        try:
            news, energy, rare = fetch_all()
            with _lock:
                _cache["news"]         = news
                _cache["energy"]       = energy
                _cache["rare"]         = rare
                _cache["last_updated"] = datetime.now().isoformat()
        except Exception:
            pass
        time.sleep(REFRESH_INTERVAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Flask ルート / Routes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route("/")
def index():
    topics_meta = [
        {
            "id":        name,
            "label_en":  cfg["label_en"],
            "icon":      cfg["icon"],
            "css_class": cfg["css_class"],
            "color":     cfg["color"],
        }
        for name, cfg in TOPICS.items()
    ]
    return render_template("dashboard.html",
                           topics=topics_meta,
                           refresh_interval=REFRESH_INTERVAL)


@app.route("/api/data")
def api_data():
    with _lock:
        return jsonify(dict(_cache))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# エントリーポイント / Entry Point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _open_browser():
    time.sleep(1.8)
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    print("━" * 60)
    print("  World Monitor (ワールドモニター) Web版")
    print("━" * 60)
    print("  サーバー起動中 / Starting server...")
    print("  データはバックグラウンドで取得します (約30〜60秒)")
    print("  Data will be fetched in the background (~30-60 sec)")
    print("  http://localhost:5000")
    print("  停止: Ctrl+C")
    print("━" * 60)

    # Flask を先に起動 → データはバックグラウンドスレッドが取得
    threading.Thread(target=_bg_refresh,   daemon=True).start()
    threading.Thread(target=_open_browser, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
