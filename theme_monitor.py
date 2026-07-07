#!/usr/bin/env python3
"""
theme_monitor.py
================
個別テーマのモニタリングツール

現在のテーマ:
  - iaa: 欧州産業加速法案（Industrial Accelerator Act）

データソース:
  1. Google News RSS（テーマ関連キーワード検索）
  2. 欧州議会 RSS フィード
  3. EURACTIV / EUobserver 等の欧州メディア RSS

動作:
  - 既存の theme_latest.json を読み込み、新規アイテムのみ Claude で要約
  - 過去データを保持しつつ先頭に追記（最大 200 件）
  - added_at を記録（generate_site.py が NEW バッジ判定に利用）

出力: docs/data/theme_latest.json

使い方:
  python theme_monitor.py
"""

import hashlib
import json
import logging
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# Windows UTF-8 対応
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import anthropic
    import feedparser
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 必要なパッケージが不足しています: {e}")
    print("   pip install anthropic feedparser requests beautifulsoup4")
    sys.exit(1)

# ── API キー ─────────────────────────────────────────────────────────────────
try:
    from api_config import ANTHROPIC_API_KEY, WORLDNEWS_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    WORLDNEWS_API_KEY = os.getenv("WORLDNEWS_API_KEY", "")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 設定
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MODEL            = "claude-haiku-4-5-20251001"
THEME_JSON_PATH  = Path(__file__).parent / "docs" / "data" / "theme_latest.json"
MAX_ITEMS        = 200   # 1テーマあたりの最大保持件数
MAX_AGE_DAYS     = 90    # この日数より古い記事は収集しない
GNEWS_MAX        = 8     # 1クエリあたりの最大取得件数

logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# テーマ定義
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEMES = [
    {
        "id":          "iaa",
        "name":        "欧州産業加速法案（IAA）",
        "name_en":     "European Industrial Accelerator Act",
        "description": "欧州委員会・欧州議会の審議動向、EU要人発言、欧州メディア論調を追跡",
        "color":       "#003F8A",   # EU ブルー
        "icon":        "🇪🇺",
        # Google News RSS 検索クエリ
        "gnews_queries": [
            {
                "q":           '"Industrial Accelerator Act" EU',
                "source":      "Google News",
                "source_type": "media",
            },
            {
                "q":           '"Industrial Accelerator Act" European Commission Parliament',
                "source":      "欧州公式機関",
                "source_type": "official",
            },
            {
                "q":           '"Competitiveness Compass" EU industrial policy legislation 2025 2026',
                "source":      "欧州産業政策",
                "source_type": "media",
            },
            {
                "q":           '"von der Leyen" OR "Teresa Ribera" OR "Stéphane Séjourné" industrial accelerator',
                "source":      "欧州委員会要人",
                "source_type": "politician",
            },
            {
                "q":           'European Parliament committee vote industrial competitiveness 2026',
                "source":      "欧州議会",
                "source_type": "official",
            },
            {
                "q":           'EURACTIV "industrial accelerator" OR "IAA" EU legislation',
                "source":      "EURACTIV",
                "source_type": "media",
            },
            {
                "q":           'EU "Clean Industrial Deal" industrial accelerator act',
                "source":      "EU産業政策",
                "source_type": "official",
            },
        ],
        # RSS フィード（キーワードフィルタ付き）
        "rss_feeds": [
            {
                "url":         "https://www.europarl.europa.eu/rss/en/newsroom-feed.xml",
                "source":      "欧州議会",
                "source_type": "official",
                "keywords":    ["industrial", "accelerat", "competitiveness", "IAA", "Clean Industrial"],
            },
            {
                "url":         "https://ec.europa.eu/commission/presscorner/api/rss/en",
                "source":      "欧州委員会",
                "source_type": "official",
                "keywords":    ["industrial", "accelerat", "competitiveness", "IAA", "Clean Industrial"],
            },
            {
                "url":         "https://www.euractiv.com/sections/industrial-policy/feed/",
                "source":      "EURACTIV",
                "source_type": "media",
                "keywords":    None,   # 産業政策セクション全件取得
            },
            {
                "url":         "https://euobserver.com/rss/news",
                "source":      "EUobserver",
                "source_type": "media",
                "keywords":    ["industrial", "accelerat", "competitiveness", "IAA"],
            },
        ],
    },
    # ──────────────────────────────────────────────────────────────────────
    # テーマ②: 米国接続車両安全保障法（S.4429）
    # ──────────────────────────────────────────────────────────────────────
    {
        "id":          "cvsa",
        "name":        "米国接続車両安全保障法（S.4429）",
        "name_en":     "Connected Vehicle Security Act of 2026",
        "description": "米議会審議・トランプ政権動向・業界団体意見・中国政府反応・メディア論調を追跡",
        "color":       "#B22234",   # US レッド
        "icon":        "🚗",
        "gnews_queries": [
            # ── 米議会・審議状況 ──
            {
                "q":           '"Connected Vehicle Security Act" OR "S. 4429" Congress Senate',
                "source":      "米議会",
                "source_type": "official",
            },
            {
                "q":           '"connected vehicle" security China ban Senate Commerce Committee 2026',
                "source":      "上院商業委員会",
                "source_type": "official",
            },
            {
                "q":           '"connected vehicle" China BIS Commerce Department rule ban 2026',
                "source":      "米商務省・BIS",
                "source_type": "official",
            },
            # ── トランプ政権・議員発言 ──
            {
                "q":           'Trump "connected vehicle" China security ban executive order',
                "source":      "トランプ政権",
                "source_type": "politician",
            },
            {
                "q":           '"Marsha Blackburn" OR "Maria Cantwell" OR "Ted Cruz" connected vehicle security China',
                "source":      "上院議員",
                "source_type": "politician",
            },
            {
                "q":           '"Elissa Slotkin" OR "Mark Warner" OR "John Thune" connected vehicle China security',
                "source":      "議員発言",
                "source_type": "politician",
            },
            # ── 業界団体・企業 ──
            {
                "q":           '"Alliance for Automotive Innovation" connected vehicle security China regulation',
                "source":      "業界団体（自動車）",
                "source_type": "industry",
            },
            {
                "q":           'automaker Ford GM Stellantis Toyota "connected vehicle" China security ban response',
                "source":      "自動車メーカー",
                "source_type": "industry",
            },
            {
                "q":           '"Motor Equipment Manufacturers" OR "Auto Alliance" OR "MEMA" connected vehicle China',
                "source":      "自動車部品業界",
                "source_type": "industry",
            },
            {
                "q":           'Qualcomm OR "NXP Semiconductors" OR Harman "connected vehicle" China security rule',
                "source":      "半導体・Tier1サプライヤー",
                "source_type": "industry",
            },
            # ── 中国政府・中国企業 ──
            {
                "q":           'China government response "connected vehicle" US ban security rule retaliation',
                "source":      "中国政府",
                "source_type": "china",
            },
            {
                "q":           'BYD OR CATL OR Huawei "connected vehicle" US security ban response 2026',
                "source":      "中国自動車・IT企業",
                "source_type": "china",
            },
            {
                "q":           'China MOFCOM "connected vehicle" US trade restriction response',
                "source":      "中国商務省",
                "source_type": "china",
            },
            # ── メディア論調 ──
            {
                "q":           '"connected vehicle" security legislation analysis opinion 2026',
                "source":      "メディア分析",
                "source_type": "media",
            },
            {
                "q":           '"connected vehicle" China software hardware ban supply chain impact',
                "source":      "業界分析",
                "source_type": "media",
            },
        ],
        "rss_feeds": [
            {
                "url":         "https://feeds.feedburner.com/thenewsroom/SenateCommerceCommittee",
                "source":      "上院商業委員会",
                "source_type": "official",
                "keywords":    ["connected vehicle", "S. 4429", "China", "automotive security"],
            },
            {
                "url":         "https://www.federalregister.gov/api/v1/documents.rss?conditions[agencies][]=commerce-department&conditions[term]=connected+vehicle",
                "source":      "連邦官報（商務省）",
                "source_type": "official",
                "keywords":    None,
            },
            {
                "url":         "https://thehill.com/feed/",
                "source":      "The Hill",
                "source_type": "media",
                "keywords":    ["connected vehicle", "S. 4429", "China automotive"],
            },
            {
                "url":         "https://www.politico.com/rss/politicopicks.xml",
                "source":      "POLITICO",
                "source_type": "media",
                "keywords":    ["connected vehicle", "China", "automotive security"],
            },
            {
                "url":         "https://www.autonews.com/rss.xml",
                "source":      "Automotive News",
                "source_type": "media",
                "keywords":    ["connected vehicle", "China", "security", "ban"],
            },
        ],
    },
    # ──────────────────────────────────────────────────────────────────────
    # テーマ③: 中国レアアース輸出管理
    # ──────────────────────────────────────────────────────────────────────
    {
        "id":          "rare_earth",
        "name":        "中国レアアース輸出管理",
        "name_en":     "China Rare Earth Export Controls",
        "description": "中国商務省・輸出規制動向、欧米政府・業界の対応、代替調達・備蓄政策を追跡",
        "color":       "#1a6b3a",   # ミネラルグリーン
        "icon":        "⛏️",
        "gnews_queries": [
            # ── 中国政府・商務省 ──
            {
                "q":           'China rare earth export controls ban restriction MOFCOM 2025 2026',
                "source":      "中国商務省（MOFCOM）",
                "source_type": "china",
            },
            {
                "q":           '"Ministry of Commerce" China "rare earth" export license restrictions',
                "source":      "中国商務省",
                "source_type": "china",
            },
            {
                "q":           'China rare earth gallium germanium antimony export ban retaliation tariffs',
                "source":      "中国輸出規制",
                "source_type": "china",
            },
            # ── 中国企業 ──
            {
                "q":           '"China Rare Earth Group" OR "China Northern Rare Earth" OR "Shenghe Resources" export controls',
                "source":      "中国レアアース企業",
                "source_type": "china",
            },
            {
                "q":           '"Baotou Steel" OR "China Minmetals" rare earth export restriction production',
                "source":      "中国素材大手",
                "source_type": "china",
            },
            # ── 米国政府・政策 ──
            {
                "q":           'US government rare earth China export controls response critical minerals supply chain',
                "source":      "米国政府",
                "source_type": "official",
            },
            {
                "q":           'Trump rare earth China ban executive order critical minerals stockpile',
                "source":      "トランプ政権",
                "source_type": "politician",
            },
            {
                "q":           '"Department of Energy" OR "Pentagon" OR "DOD" rare earth China supply chain shortage',
                "source":      "米国防・エネルギー省",
                "source_type": "official",
            },
            {
                "q":           '"critical minerals" rare earth China ban US Congress Senate legislation 2026',
                "source":      "米議会",
                "source_type": "official",
            },
            # ── 欧州政府・EU ──
            {
                "q":           'EU European Commission rare earth China export controls response "Critical Raw Materials"',
                "source":      "欧州委員会",
                "source_type": "official",
            },
            {
                "q":           '"Critical Raw Materials Act" EU rare earth China supply strategic autonomy',
                "source":      "EU戦略的原材料法",
                "source_type": "official",
            },
            {
                "q":           'Europe Japan Australia "rare earth" China export ban alternative supply response',
                "source":      "同盟国対応",
                "source_type": "politician",
            },
            # ── 欧米の要人発言 ──
            {
                "q":           '"von der Leyen" OR "Ursula" OR "Janet Yellen" OR "Gina Raimondo" rare earth China minerals',
                "source":      "欧米要人発言",
                "source_type": "politician",
            },
            {
                "q":           '"Howard Lutnick" OR "Chris Wright" rare earth critical minerals China 2026',
                "source":      "米閣僚発言",
                "source_type": "politician",
            },
            # ── 業界団体・企業 ──
            {
                "q":           '"Rare Earth Industry Association" OR "Critical Minerals Institute" OR "REITA" China export controls',
                "source":      "業界団体",
                "source_type": "industry",
            },
            {
                "q":           '"MP Materials" OR "Lynas" OR "Energy Fuels" rare earth China alternative supply production',
                "source":      "欧米レアアース企業",
                "source_type": "industry",
            },
            {
                "q":           'defense aerospace automaker EV battery manufacturer rare earth China ban supply shortage impact',
                "source":      "需要産業（防衛・EV・航空）",
                "source_type": "industry",
            },
            {
                "q":           '"Lockheed Martin" OR "Raytheon" OR "Boeing" rare earth China export controls defense supply',
                "source":      "防衛産業",
                "source_type": "industry",
            },
            {
                "q":           'Tesla OR "General Motors" OR Volkswagen OR Toyota rare earth China export ban battery motor',
                "source":      "自動車・EV大手",
                "source_type": "industry",
            },
            # ── メディア論調 ──
            {
                "q":           'China rare earth export controls global impact analysis supply chain 2026',
                "source":      "メディア分析",
                "source_type": "media",
            },
            {
                "q":           'rare earth China ban Europe US response critical minerals alternative 2026',
                "source":      "欧米メディア",
                "source_type": "media",
            },
            {
                "q":           'China minerals export restriction trade war retaliation tariffs rare earth',
                "source":      "貿易・資源メディア",
                "source_type": "media",
            },
        ],
        "rss_feeds": [
            {
                "url":         "https://www.ft.com/rss/home/uk",
                "source":      "Financial Times",
                "source_type": "media",
                "keywords":    ["rare earth", "critical mineral", "China export", "gallium", "germanium", "antimony"],
            },
            {
                "url":         "https://feeds.reuters.com/reuters/businessNews",
                "source":      "Reuters",
                "source_type": "media",
                "keywords":    ["rare earth", "rare-earth", "critical mineral", "China export control", "gallium", "antimony"],
            },
            {
                "url":         "https://www.mining.com/feed/",
                "source":      "Mining.com",
                "source_type": "industry",
                "keywords":    ["rare earth", "rare-earth", "China", "export control", "gallium", "germanium"],
            },
            {
                "url":         "https://www.spglobal.com/commodityinsights/en/rss-feed/metals",
                "source":      "S&P Global Commodity",
                "source_type": "media",
                "keywords":    ["rare earth", "China", "export", "critical mineral"],
            },
            {
                "url":         "https://ec.europa.eu/commission/presscorner/api/rss/en",
                "source":      "欧州委員会",
                "source_type": "official",
                "keywords":    ["rare earth", "critical raw materials", "China", "minerals", "strategic"],
            },
            {
                "url":         "https://thehill.com/feed/",
                "source":      "The Hill",
                "source_type": "media",
                "keywords":    ["rare earth", "critical minerals", "China", "export controls"],
            },
        ],
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ユーティリティ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def make_uid(url: str) -> str:
    """URL の MD5 ハッシュ（重複チェック用）"""
    return hashlib.md5(url.strip().encode()).hexdigest()[:12]

def now_jst() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))

def now_str() -> str:
    return now_jst().strftime("%Y-%m-%d %H:%M:%S")

def fmt_date(dt: Optional[datetime]) -> str:
    if dt is None:
        return now_jst().strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")

def parsed_to_dt(t) -> Optional[datetime]:
    if t is None:
        return None
    try:
        return datetime(*t[:6], tzinfo=timezone.utc)
    except Exception:
        return None

def strip_html_text(html: str) -> str:
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

def is_too_old(date_str: str) -> bool:
    """MAX_AGE_DAYS より古い記事を除外"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days > MAX_AGE_DAYS
    except Exception:
        return False

def fetch_url(url: str, timeout: int = 12) -> Optional[str]:
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; WorldNewsBot/1.0)"},
            timeout=timeout,
        )
        r.raise_for_status()
        return r.text
    except Exception as e:
        logger.debug("fetch_url %s: %s", url, e)
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Google News RSS 検索
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fetch_gnews(query: str, max_items: int = GNEWS_MAX) -> list[dict]:
    url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query)
        + "&hl=en&gl=US&ceid=US:en"
    )
    try:
        feed = feedparser.parse(url)
    except Exception:
        return []
    items = []
    for entry in feed.entries[:max_items * 2]:
        pub_dt  = parsed_to_dt(entry.get("published_parsed"))
        date_s  = fmt_date(pub_dt)
        if is_too_old(date_s):
            continue
        summary = strip_html_text(entry.get("summary", ""))[:600]
        items.append({
            "title":   entry.get("title", ""),
            "url":     entry.get("link", ""),
            "date":    date_s,
            "content": summary,
        })
        if len(items) >= max_items:
            break
    return items


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. RSS フィード（キーワードフィルタ付き）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fetch_rss(feed_url: str, keywords: Optional[list[str]], max_items: int = 10) -> list[dict]:
    try:
        feed = feedparser.parse(feed_url)
    except Exception:
        return []
    items = []
    for entry in feed.entries[:50]:
        title   = entry.get("title", "")
        summary = strip_html_text(entry.get("summary", entry.get("description", "")))[:600]
        pub_dt  = parsed_to_dt(entry.get("published_parsed"))
        date_s  = fmt_date(pub_dt)

        if is_too_old(date_s):
            continue

        # キーワードフィルタ（None の場合はすべて通す）
        if keywords:
            text = (title + " " + summary).lower()
            if not any(kw.lower() in text for kw in keywords):
                continue

        items.append({
            "title":   title,
            "url":     entry.get("link", ""),
            "date":    date_s,
            "content": summary,
        })
        if len(items) >= max_items:
            break
    return items


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Claude 要約（1件）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def summarize_item(title: str, content: str, theme_name: str) -> str:
    """タイトル＋本文を日本語 1〜2 文に要約"""
    if not ANTHROPIC_API_KEY:
        return (content[:200] + "…") if len(content) > 200 else content
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = (
        f"以下の記事を「{theme_name}」に関する文脈で日本語 1〜2 文に要約してください。\n"
        "要点を具体的に述べ、前置きなしで直接要約を出力してください。\n\n"
        f"タイトル: {title}\n"
        f"内容: {content[:1200]}"
    )
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        logger.warning("summarize_item error: %s", e)
        return (content[:200] + "…") if len(content) > 200 else content


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. テーマ別アイテム収集
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def collect_theme_items(theme: dict, existing_uids: set) -> list[dict]:
    """テーマに関する新着アイテムを収集し、Claude で要約して返す"""
    raw: list[dict] = []

    # ① Google News RSS クエリ
    for q_def in theme.get("gnews_queries", []):
        print(f"  → Google News: {q_def['q'][:60]}...")
        results = fetch_gnews(q_def["q"])
        for r in results:
            r["source"]      = q_def["source"]
            r["source_type"] = q_def["source_type"]
            raw.append(r)

    # ② RSS フィード
    for feed_def in theme.get("rss_feeds", []):
        print(f"  → RSS [{feed_def['source']}]: {feed_def['url'][:60]}...")
        results = fetch_rss(
            feed_def["url"],
            keywords=feed_def.get("keywords"),
            max_items=10,
        )
        for r in results:
            r["source"]      = feed_def["source"]
            r["source_type"] = feed_def["source_type"]
            raw.append(r)

    # URL ベースで重複除去
    seen_urls: set = set()
    unique: list[dict] = []
    for item in raw:
        url = item.get("url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        unique.append(item)

    # 既知 UID を除いた新規アイテムのみ Claude 要約
    new_items: list[dict] = []
    added_at = now_str()
    for item in unique:
        uid = make_uid(item["url"])
        if uid in existing_uids:
            continue   # 既知 → スキップ

        print(f"    [NEW] {item['title'][:65]}")
        summary = summarize_item(item["title"], item["content"], theme["name"])

        new_items.append({
            "uid":         uid,
            "date":        item["date"],
            "title":       item["title"],
            "summary":     summary,
            "source":      item["source"],
            "source_type": item["source_type"],   # official / politician / media
            "url":         item["url"],
            "added_at":    added_at,
        })

    return new_items


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. JSON 読み込み / 保存
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_existing() -> dict:
    if THEME_JSON_PATH.exists():
        try:
            return json.loads(THEME_JSON_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ⚠ theme_latest.json 読み込み失敗: {e}")
    return {"generated_at": "", "themes": []}

def save_json(data: dict):
    THEME_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    THEME_JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. メイン
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    logging.basicConfig(level=logging.WARNING)
    print("=" * 60)
    print("  個別テーマ モニタリング")
    print("=" * 60)

    existing     = load_existing()
    exist_map    = {t["id"]: t for t in existing.get("themes", [])}

    updated_themes = []
    total_new      = 0

    for theme in THEMES:
        tid = theme["id"]
        print(f"\n▶ テーマ: {theme['name']}")

        existing_theme  = exist_map.get(tid, {})
        existing_items  = existing_theme.get("items", [])
        existing_uids   = {it["uid"] for it in existing_items}

        # 新着アイテムを収集
        new_items = collect_theme_items(theme, existing_uids)
        total_new += len(new_items)

        # 新規を先頭に追記 → MAX_ITEMS で切り詰め
        all_items = new_items + existing_items
        all_items = all_items[:MAX_ITEMS]

        updated_themes.append({
            "id":           tid,
            "name":         theme["name"],
            "name_en":      theme["name_en"],
            "description":  theme["description"],
            "color":        theme["color"],
            "icon":         theme["icon"],
            "last_checked": now_str(),
            "items":        all_items,
        })
        print(f"  → 新着 {len(new_items)} 件 / 累計 {len(all_items)} 件")

    output = {
        "generated_at": now_str(),
        "themes":       updated_themes,
    }
    save_json(output)
    print(f"\n✅ theme_latest.json を更新しました（新着合計 {total_new} 件）")
    print(f"   保存先: {THEME_JSON_PATH}")


if __name__ == "__main__":
    main()
