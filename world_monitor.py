#!/usr/bin/env python3
"""
World Monitor (ワールドモニター)
世界情勢・商品価格モニタリングダッシュボード

オープンソースライブラリ:
  - feedparser  : RSS/Atom フィード解析
  - yfinance    : Yahoo Finance 価格データ取得
  - rich        : リッチなターミナル UI 描画

使い方 / Usage:
  python world_monitor.py              # 通常起動 (5分ごと自動更新)
  python world_monitor.py --once       # 一度表示して終了
  python world_monitor.py --refresh 60 # 更新間隔を秒数で指定
"""

import argparse
import logging
import sys
import time
import urllib.parse
from datetime import datetime
from typing import Optional

# Windows では stdout/stderr を UTF-8 に再設定して日本語・特殊文字を正常出力
# Reconfigure stdout/stderr to UTF-8 on Windows for proper Japanese & Unicode output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import feedparser
import yfinance as yf
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# yfinance の不要な警告を抑制 / Suppress noisy yfinance warnings
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

# Windows レガシーコンソール API ではなく ANSI モードを強制し UTF-8 で描画
# Force ANSI mode (not legacy Win32 API) so emoji and Japanese chars render correctly
console = Console(legacy_windows=False)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 設定 / Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEFAULT_REFRESH_SECS = 300  # 5 分ごとに自動更新
MAX_ARTICLES_PER_TOPIC = 5

# ── ニューストピック設定 ──────────────────────────────────────────────────────
# 各トピックに日本語名・英語名・検索クエリ・表示色・アイコンを設定
TOPICS: dict = {
    "日米関係": {
        "label_en": "Japan-US Relations",
        "queries": [
            "Japan US relations 2025",
            "US Japan trade alliance tariffs",
            "日米同盟 関係",
        ],
        "color": "cyan",
        "icon": "[JP/US]",
    },
    "米中関係": {
        "label_en": "US-China Relations",
        "queries": [
            "US China relations 2025",
            "China tariffs trade war",
            "Sino-American diplomacy",
        ],
        "color": "yellow",
        "icon": "[US/CN]",
    },
    "米イラン関係": {
        "label_en": "US-Iran Relations",
        "queries": [
            "US Iran relations 2025",
            "Iran sanctions nuclear deal",
            "Iran United States diplomacy",
        ],
        "color": "red",
        "icon": "[US/IR]",
    },
    "自動車産業": {
        "label_en": "Automotive Industry",
        "queries": [
            "automotive industry 2025",
            "electric vehicle EV news manufacturer",
            "auto tariffs car industry",
        ],
        "color": "green",
        "icon": "[AUTO]",
    },
}

# ── エネルギー先物ティッカー (Yahoo Finance) ─────────────────────────────────
# 表示名に単位を含める (単位列を省いて 80 桁端末に収める)
ENERGY_TICKERS: dict[str, tuple[str, str]] = {
    "WTI 原油 [$/bbl]":          ("CL=F",  "USD/bbl"),
    "ブレント原油 [$/bbl]":       ("BZ=F",  "USD/bbl"),
    "天然ガス [$/MMBtu]":         ("NG=F",  "USD/MMBtu"),
    "灯油 [$/gal]":               ("HO=F",  "USD/gal"),
    "ガソリン RBOB [$/gal]":      ("RB=F",  "USD/gal"),
}

# ── レアアース関連指標 ────────────────────────────────────────────────────────
# ※ レアアースのスポット価格は上海金属市場 (SMM) 等の有料 API が必要なため、
#    関連 ETF・採掘会社株式を代理指標として使用します。
# ※ Direct rare earth spot prices require specialized APIs (e.g., Shanghai Metals
#    Market). The entries below use related ETFs and mining stocks as proxies.
RARE_EARTH_TICKERS: dict[str, tuple[str, str]] = {
    "REMX レアアース ETF":     ("REMX",  "USD"),
    "MP Materials (Nd採掘)":   ("MP",    "USD"),
    "Energy Fuels (UUUU)":     ("UUUU",  "USD"),
    "Lynas RE (ADR)":          ("LYSCF", "USD"),
    "Albemarle リチウム":      ("ALB",   "USD"),
    "SQM リチウム化合物":      ("SQM",   "USD"),
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データ取得 / Data Fetching
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _rss_fetch(query: str, lang: str = "en", n: int = 5) -> list[dict]:
    """Google News RSS から記事リストを返す"""
    q = urllib.parse.quote(query)
    if lang == "ja":
        url = f"https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja"
    else:
        url = f"https://news.google.com/rss/search?q={q}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(
            url,
            request_headers={"User-Agent": "WorldMonitor/1.0 (+feedparser)"},
        )
        return [
            {
                "title":     e.get("title", "").strip(),
                "source":    e.get("source", {}).get("title", ""),
                "published": e.get("published", ""),
            }
            for e in feed.entries[:n]
            if e.get("title", "").strip()
        ]
    except Exception:
        return []


def fetch_topic_news(config: dict) -> list[dict]:
    """トピック設定の全クエリからニュースを収集し、重複を除いて返す"""
    seen: set[str] = set()
    results: list[dict] = []

    for query in config["queries"]:
        # クエリに日本語文字が含まれる場合は ja モードで取得
        is_ja = any(ord(c) > 0x3000 for c in query)
        for art in _rss_fetch(query, lang="ja" if is_ja else "en", n=4):
            key = art["title"][:60].lower()
            if key not in seen:
                seen.add(key)
                results.append(art)
            if len(results) >= MAX_ARTICLES_PER_TOPIC:
                return results
    return results


def fetch_price(ticker: str) -> Optional[dict]:
    """Yahoo Finance から前日比付きの価格を返す。取得失敗時は None"""
    try:
        fi = yf.Ticker(ticker).fast_info
        price = fi.last_price
        prev  = fi.previous_close
        if price and prev and prev != 0:
            change = price - prev
            return {
                "price":   price,
                "change":  change,
                "chg_pct": change / prev * 100,
            }
    except Exception:
        pass
    return None


def fetch_all() -> tuple[dict, dict, dict]:
    """全トピックのニュースと全価格データを一括取得する"""
    news: dict = {}
    for name, cfg in TOPICS.items():
        news[name] = fetch_topic_news(cfg)

    energy = {ticker: fetch_price(ticker) for _, (ticker, _) in ENERGY_TICKERS.items()}
    rare   = {ticker: fetch_price(ticker) for _, (ticker, _) in RARE_EARTH_TICKERS.items()}

    return news, energy, rare


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 描画ヘルパー / Rendering Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _chg_markup(change: float, chg_pct: float) -> tuple[str, str]:
    """前日比の符号・色付き Rich マークアップを返す"""
    sign  = "+" if change >= 0 else ""
    color = "green" if change >= 0 else "red"
    return (
        f"[{color}]{sign}{change:.2f}[/{color}]",
        f"[{color}]{sign}{chg_pct:.2f}%[/{color}]",
    )


def _make_news_panel(name: str, cfg: dict, articles: list[dict]) -> Panel:
    tbl = Table(box=None, show_header=False, expand=True, padding=(0, 1))
    tbl.add_column("content", no_wrap=False, overflow="fold")

    if not articles:
        tbl.add_row(Text("記事なし / No articles found", style="dim italic"))
    else:
        for art in articles:
            title = art["title"]
            if len(title) > 86:
                title = title[:83] + "…"

            t = Text()
            t.append(f"• {title}", style="white")

            meta = [m for m in [art.get("source", ""), art.get("published", "")[:16]] if m]
            if meta:
                t.append(f"\n  {' | '.join(meta)}", style="dim")

            tbl.add_row(t)

    color = cfg["color"]
    return Panel(
        tbl,
        title=(
            f" {cfg['icon']} "
            f"[bold {color}]{name}[/bold {color}]  "
            f"[dim]{cfg['label_en']}[/dim] "
        ),
        border_style=color,
        expand=True,
    )


def _make_price_table(
    ticker_map: dict[str, tuple[str, str]],
    prices: dict,
    show_unit: bool = True,
) -> Table:
    # 列幅をコンパクトにして 80 桁端末でも全列が収まるよう設定
    # Compact widths so all columns fit in an 80-column terminal
    tbl = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        expand=True,
        header_style="bold dim",
        padding=(0, 1),
    )
    tbl.add_column("銘柄 / Name",        min_width=18, max_width=26, no_wrap=True)
    tbl.add_column("Ticker",             style="dim", width=7, justify="center")
    if show_unit:
        tbl.add_column("単位",           style="dim", width=11, justify="center")
    tbl.add_column("価格 / Price",       justify="right", min_width=12)
    tbl.add_column("前日比",             justify="right", width=10)
    tbl.add_column("変動率",             justify="right", width=8)

    for display_name, (ticker, unit) in ticker_map.items():
        data = prices.get(ticker)
        base_row = [display_name, f"[dim]{ticker}[/dim]"]
        if show_unit:
            base_row.append(f"[dim]{unit}[/dim]")

        if data is None:
            tbl.add_row(*base_row, "[dim]N/A[/dim]", "[dim]--[/dim]", "[dim]--[/dim]")
            continue

        p             = data["price"]
        chg_s, pct_s  = _chg_markup(data["change"], data["chg_pct"])
        color         = "green" if data["change"] >= 0 else "red"
        arrow         = "^" if data["change"] >= 0 else "v"
        price_str     = f"[bold {color}]{arrow} {p:.2f}[/bold {color}]"

        tbl.add_row(*base_row, price_str, chg_s, pct_s)

    return tbl


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 画面描画 / Display
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display(
    news: dict,
    energy: dict,
    rare: dict,
    last_updated: datetime,
    refresh_secs: int,
) -> None:
    console.clear()

    # ── ヘッダー ──────────────────────────────────────────────────────────
    header = Text(justify="center")
    header.append("  World Monitor  ",  style="bold bright_white on blue")
    header.append("  ワールドモニター  ", style="bold white")
    header.append("  世界情勢 & 市場価格ダッシュボード  ", style="bright_cyan")
    header.append(
        f"  最終更新 / Last update: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}  ",
        style="dim",
    )
    console.print(Panel(Align.center(header), border_style="bright_blue", padding=(0, 0)))

    # ── ニュースセクション (2 列 × 2 行) ─────────────────────────────────
    topic_list = list(TOPICS.items())
    for i in range(0, len(topic_list), 2):
        row = [
            _make_news_panel(name, cfg, news.get(name, []))
            for name, cfg in topic_list[i : i + 2]
        ]
        console.print(Columns(row, equal=True, expand=True))

    # ── エネルギー価格 ────────────────────────────────────────────────────
    console.print(Panel(
        _make_price_table(ENERGY_TICKERS, energy, show_unit=False),
        title=(
            " [bold yellow]*** エネルギー価格 ***[/bold yellow]"
            "  [dim]Energy Prices -- Yahoo Finance Futures[/dim] "
        ),
        border_style="yellow",
    ))

    # ── レアアース関連指標 ────────────────────────────────────────────────
    console.print(Panel(
        _make_price_table(RARE_EARTH_TICKERS, rare, show_unit=False),
        title=(
            " [bold white]*** レアアース関連指標 ***[/bold white]"
            "  [dim]Rare Earth Proxies -- ETFs & Mining Stocks[/dim] "
        ),
        subtitle=(
            "[dim]※ スポット価格は上海金属市場 (SMM) 等の専門 API が必要。"
            "ETF・関連株を代理指標として使用 / "
            "Spot prices require specialized APIs (SMM etc.). "
            "ETFs/stocks shown as proxies.[/dim]"
        ),
        border_style="bright_white",
    ))

    # ── フッター ──────────────────────────────────────────────────────────
    console.print(Text(
        f"  Ctrl+C: 終了 / Quit"
        f"   自動更新 / Auto-refresh: {refresh_secs} 秒"
        f"   データソース / Sources: Google News RSS + Yahoo Finance (yfinance)",
        style="dim",
    ))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# エントリーポイント / Entry Point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="World Monitor — 世界情勢・商品価格ダッシュボード",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="一度だけ表示して終了 / Display once and exit",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=DEFAULT_REFRESH_SECS,
        metavar="SECS",
        help=f"自動更新間隔（秒） / Auto-refresh interval in seconds (default: {DEFAULT_REFRESH_SECS})",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    console.print(
        "\n[bold bright_cyan]World Monitor[/bold bright_cyan]"
        " [dim]起動中 / Starting...[/dim]\n"
    )
    console.print("[dim]  ニュース & 価格データを取得中 / Fetching news & prices...[/dim]")

    news, energy, rare = fetch_all()
    last_updated = datetime.now()
    display(news, energy, rare, last_updated, args.refresh)

    if args.once:
        return

    try:
        elapsed = 0
        while True:
            time.sleep(1)
            elapsed += 1
            if elapsed >= args.refresh:
                console.print(
                    "\n[dim]  データ更新中 / Refreshing data...[/dim]",
                    end="",
                )
                news, energy, rare = fetch_all()
                last_updated = datetime.now()
                elapsed = 0
                display(news, energy, rare, last_updated, args.refresh)
    except KeyboardInterrupt:
        console.print("\n[dim]  終了しました / Exited.[/dim]\n")


if __name__ == "__main__":
    main()
