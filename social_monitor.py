"""
social_monitor.py
=================
企業・業界のSNS/ニュース騒動監視ツール（POC版）

【データソース】
  - Google News RSS（フリー・APIキー不要）
  - Yahoo Newsトップ（スクレイピング、参考程度）

【分析】
  - Claude Haiku API で各記事の感情・事業影響をスコアリング

【出力】
  - HTMLインタラクティブ散布図
    X軸: ネガティブ ←→ ポジティブ（同調度が高いほど端に寄る）
    Y軸: 事業影響度 0〜10（レピュテーションリスク）
  - コンソールにトップリスク一覧

【使い方】
  python social_monitor.py
  python social_monitor.py --company "ソニー" --industry "電機" --hours 24
  python social_monitor.py --company "トヨタ" --industry "自動車" --hours 12 --output report.html
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

try:
    import anthropic
except ImportError:
    sys.exit("❌ anthropic が未インストールです: pip install anthropic")

try:
    import feedparser
except ImportError:
    sys.exit("❌ feedparser が未インストールです: pip install feedparser")

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    sys.exit("❌ plotly が未インストールです: pip install plotly")

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── 設定 ────────────────────────────────────────────────────
CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"

CATEGORY_LIST = ["製品/技術", "財務/業績", "労務/人事", "法規制/訴訟", "環境/ESG", "経営戦略", "その他"]

CATEGORY_COLORS = {
    "製品/技術":  "#4ECDC4",
    "財務/業績":  "#FF6B6B",
    "労務/人事":  "#FFD93D",
    "法規制/訴訟": "#C77DFF",
    "環境/ESG":   "#6BCB77",
    "経営戦略":   "#4D96FF",
    "その他":     "#AAAAAA",
}


# ═══════════════════════════════════════════════════════════
# 1. データ収集
# ═══════════════════════════════════════════════════════════

def fetch_google_news(query: str, hours: int) -> list[dict]:
    """Google News RSSから記事を取得"""
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=ja&gl=JP&ceid=JP:ja"
    print(f"  [RSS] Google News RSS: {query}")
    feed = feedparser.parse(url)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    articles = []
    for entry in feed.entries:
        try:
            pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pub = datetime.now(timezone.utc)
        if pub < cutoff:
            continue
        articles.append({
            "title":     entry.title,
            "summary":   re.sub(r"<[^>]+>", "", entry.get("summary", "")),
            "link":      entry.link,
            "published": pub.strftime("%Y-%m-%d %H:%M"),
            "source":    entry.get("source", {}).get("title", ""),
            "platform":  "Google News",
        })
    print(f"  → {len(articles)} 件（過去{hours}時間）")
    return articles


def fetch_yahoo_news(query: str, hours: int) -> list[dict]:
    """Yahoo! Japan ニュース検索（スクレイピング）"""
    if not HAS_REQUESTS:
        return []
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://news.yahoo.co.jp/search?p={encoded}&ei=UTF-8"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        print(f"  [RSS] Yahoo! Japan ニュース: {query}")
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = []
        for item in soup.select("li.newsFeed_item")[:20]:
            title_el = item.select_one(".newsFeed_item_title")
            link_el  = item.select_one("a")
            if not title_el or not link_el:
                continue
            articles.append({
                "title":     title_el.get_text(strip=True),
                "summary":   "",
                "link":      "https://news.yahoo.co.jp" + link_el.get("href", ""),
                "published": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source":    "Yahoo! Japan",
                "platform":  "Yahoo News",
            })
        print(f"  → {len(articles)} 件")
        return articles
    except Exception as e:
        print(f"  [WARN]  Yahoo取得失敗: {e}")
        return []


# ═══════════════════════════════════════════════════════════
# 2. Claude API 分析
# ═══════════════════════════════════════════════════════════

ANALYSIS_PROMPT = """あなたはコーポレートリスク分析の専門家です。
対象企業/業界: {company}（{industry}業界）

以下のニュース記事を分析し、JSONのみで返してください（説明文不要）:

タイトル: {title}
概要: {summary}

評価項目:
1. sentiment: -1.0〜+1.0（-1=非常にネガティブ, 0=中立, +1=非常にポジティブ）
2. consensus: 0.0〜1.0（社会的同調・拡散度。大炎上/広く共有=1.0, 一般的話題=0.5, マイナー=0.1）
3. business_impact: 0〜10（事業影響度 — 単なる感想・日常的なもの=1〜2, 株価・売上に直結するリスク=8〜10）
4. category: {categories} のいずれか1つ
5. reason: 評価の根拠（日本語・40文字以内）

JSON例:
{{"sentiment": -0.7, "consensus": 0.8, "business_impact": 8, "category": "法規制/訴訟", "reason": "リコール隠蔽疑惑で集団訴訟リスク"}}"""


def analyze_article(client: anthropic.Anthropic, article: dict, company: str, industry: str) -> dict:
    """Claude Haiku で記事をスコアリング"""
    prompt = ANALYSIS_PROMPT.format(
        company=company,
        industry=industry,
        title=article["title"],
        summary=article["summary"][:500],
        categories="、".join(CATEGORY_LIST),
    )
    try:
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            result = json.loads(m.group())
            # 値の範囲クランプ
            result["sentiment"]        = max(-1.0, min(1.0, float(result.get("sentiment", 0))))
            result["consensus"]        = max(0.0,  min(1.0, float(result.get("consensus", 0.5))))
            result["business_impact"]  = max(0,    min(10,  int(result.get("business_impact", 3))))
            result["category"]         = result.get("category", "その他")
            result["reason"]           = result.get("reason", "")
            return result
    except Exception as e:
        print(f"    [WARN]  分析エラー: {e}")
    return {"sentiment": 0.0, "consensus": 0.3, "business_impact": 2, "category": "その他", "reason": "分析失敗"}


def analyze_all(articles: list[dict], company: str, industry: str, client: anthropic.Anthropic) -> list[dict]:
    print(f"\n[AI] Claude Haiku で {len(articles)} 件を分析中...")
    results = []
    for i, article in enumerate(articles, 1):
        print(f"  [{i:2d}/{len(articles)}] {article['title'][:50]}...")
        scores = analyze_article(client, article, company, industry)
        results.append({**article, **scores})
        time.sleep(0.3)  # レート制限対策
    return results


# ═══════════════════════════════════════════════════════════
# 3. 散布図生成
# ═══════════════════════════════════════════════════════════

def calc_x_position(sentiment: float, consensus: float) -> float:
    """
    同調度（consensus）が高いほど感情軸の端に引っ張られる。
    consensus=0 → x = sentiment * 0.4（中央寄り）
    consensus=1 → x = sentiment * 1.0（端まで）
    """
    return sentiment * (0.4 + consensus * 0.6)


def build_chart(data: list[dict], company: str, industry: str, hours: int) -> go.Figure:
    fig = go.Figure()

    # カテゴリ別にプロット
    by_category: dict[str, list] = {}
    for d in data:
        cat = d.get("category", "その他")
        by_category.setdefault(cat, []).append(d)

    for cat, items in by_category.items():
        xs = [calc_x_position(d["sentiment"], d["consensus"]) for d in items]
        ys = [d["business_impact"] for d in items]
        titles   = [d["title"][:60]    for d in items]
        sources  = [d["source"][:12]   for d in items]
        reasons  = [d["reason"]        for d in items]
        sents    = [d["sentiment"]     for d in items]
        conses   = [d["consensus"]     for d in items]
        links    = [d["link"]          for d in items]
        pub      = [d["published"]     for d in items]

        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="markers",
            name=cat,
            marker=dict(
                size=14,
                color=CATEGORY_COLORS.get(cat, "#AAAAAA"),
                opacity=0.85,
                line=dict(width=1.5, color="white"),
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "出典: %{customdata[1]} | %{customdata[5]}<br>"
                "感情スコア: %{customdata[2]:.2f} | 同調度: %{customdata[3]:.2f}<br>"
                "事業影響度: %{y}/10<br>"
                "理由: %{customdata[4]}<br>"
                "<a href='%{customdata[6]}'>記事を開く↗</a>"
                "<extra>%{fullData.name}</extra>"
            ),
            customdata=list(zip(titles, sources, sents, conses, reasons, pub, links)),
        ))

    # 象限の背景色
    shapes = [
        dict(type="rect", x0=-1.1, x1=0, y0=5, y1=10.5,
             fillcolor="rgba(255,100,100,0.07)", line_width=0),
        dict(type="rect", x0=0, x1=1.1, y0=5, y1=10.5,
             fillcolor="rgba(100,200,100,0.07)", line_width=0),
        dict(type="rect", x0=-1.1, x1=0, y0=-0.5, y1=5,
             fillcolor="rgba(255,200,100,0.05)", line_width=0),
        dict(type="rect", x0=0, x1=1.1, y0=-0.5, y1=5,
             fillcolor="rgba(100,150,255,0.05)", line_width=0),
    ]

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    fig.update_layout(
        title=dict(
            text=(f"<b>{company}（{industry}業界）SNS・ニュース騒動マップ</b><br>"
                  f"<sup>過去{hours}時間 | {now_str} 時点 | 計{len(data)}件</sup>"),
            x=0.5, xanchor="center",
        ),
        xaxis=dict(
            title="← ネガティブ　　感情軸（同調度で端に引張）　ポジティブ →",
            range=[-1.1, 1.1],
            zeroline=True, zerolinewidth=2, zerolinecolor="gray",
            gridcolor="#eeeeee", showgrid=True,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["強ネガ", "ネガ", "中立", "ポジ", "強ポジ"],
        ),
        yaxis=dict(
            title="事業影響度（レピュテーションリスク）",
            range=[-0.5, 10.5],
            gridcolor="#eeeeee", showgrid=True,
            tickvals=[0, 2, 4, 6, 8, 10],
            ticktext=["影響なし", "軽微", "小", "中", "大", "危機的"],
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            title="カテゴリ",
            bordercolor="#cccccc", borderwidth=1,
            bgcolor="rgba(255,255,255,0.9)",
        ),
        height=650,
        shapes=shapes,
        annotations=[
            dict(x=-0.75, y=9.5, text="[WARN] 危機対応必要", showarrow=False,
                 font=dict(color="rgba(200,50,50,0.7)", size=11)),
            dict(x=0.75, y=9.5, text="[OK] PR機会", showarrow=False,
                 font=dict(color="rgba(50,150,50,0.7)", size=11)),
            dict(x=-0.75, y=0.5, text="[NOTE] ウォッチ", showarrow=False,
                 font=dict(color="rgba(200,130,0,0.7)", size=11)),
            dict(x=0.75, y=0.5, text="[POS] 日常会話", showarrow=False,
                 font=dict(color="rgba(50,100,200,0.7)", size=11)),
        ],
        hoverlabel=dict(bgcolor="white", bordercolor="#cccccc", font_size=13),
    )

    return fig


# ═══════════════════════════════════════════════════════════
# 4. コンソール サマリー
# ═══════════════════════════════════════════════════════════

def print_summary(data: list[dict], company: str):
    print("\n" + "="*60)
    print(f"  {company} 騒動分析サマリー")
    print("="*60)

    # トップリスク（ネガティブ×高影響）
    risks = [d for d in data if d["sentiment"] < -0.2 and d["business_impact"] >= 6]
    risks.sort(key=lambda x: x["business_impact"], reverse=True)
    print(f"\n[RISK] 要注意記事（ネガ×高影響）: {len(risks)} 件")
    for r in risks[:5]:
        print(f"  [{r['business_impact']:2d}/10] {r['title'][:55]}")
        print(f"         → {r['reason']}  [{r['source']}]")

    # ポジティブ機会
    opps = [d for d in data if d["sentiment"] > 0.3 and d["business_impact"] >= 5]
    opps.sort(key=lambda x: x["business_impact"], reverse=True)
    print(f"\n[OK] 好機記事（ポジ×高影響）: {len(opps)} 件")
    for o in opps[:3]:
        print(f"  [{o['business_impact']:2d}/10] {o['title'][:55]}")
        print(f"         → {o['reason']}  [{o['source']}]")

    # 統計
    avg_sent = sum(d["sentiment"] for d in data) / len(data) if data else 0
    avg_imp  = sum(d["business_impact"] for d in data) / len(data) if data else 0
    print(f"\n[CHART] 全体統計")
    print(f"  記事数: {len(data)} 件")
    print(f"  平均感情スコア: {avg_sent:+.2f}  ({'ポジ寄り' if avg_sent > 0 else 'ネガ寄り' if avg_sent < 0 else '中立'})")
    print(f"  平均事業影響度: {avg_imp:.1f}/10")
    print("="*60)


# ═══════════════════════════════════════════════════════════
# 5. メイン
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="企業・業界のSNS騒動を監視・分析・可視化")
    parser.add_argument("--company",  default="トヨタ",  help="監視企業名（例: トヨタ）")
    parser.add_argument("--industry", default="自動車",  help="業界名（例: 自動車）")
    parser.add_argument("--hours",    type=int, default=12, help="収集時間範囲（時間）")
    parser.add_argument("--output",   default="", help="HTMLファイル出力先（省略時は自動生成）")
    parser.add_argument("--api-key",  default="", help="Anthropic APIキー（省略時はスクリプト内のキーを使用）")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "") or CLAUDE_API_KEY
    client  = anthropic.Anthropic(api_key=api_key)

    print(f"\n{'='*60}")
    print(f"  SNS騒動監視 POC - {args.company}({args.industry}業界)")
    print(f"  対象期間: 過去{args.hours}時間")
    print(f"{'='*60}\n")

    # ── データ収集 ─────────────────────────────────────────
    print("[DL] ニュース収集中...")
    articles = []

    # Google News: 企業名 + 業界キーワード
    for q in [args.company, f"{args.industry} 業界"]:
        articles += fetch_google_news(q, args.hours)

    # Yahoo News（任意）
    articles += fetch_yahoo_news(args.company, args.hours)

    # 重複除去（タイトルベース）
    seen = set()
    unique = []
    for a in articles:
        key = a["title"][:30]
        if key not in seen:
            seen.add(key)
            unique.append(a)
    articles = unique

    if not articles:
        print("[WARN]  記事が見つかりませんでした。検索キーワードを変えてください。")
        sys.exit(1)

    print(f"\n合計 {len(articles)} 件の記事を収集しました。")

    # ── 分析 ───────────────────────────────────────────────
    data = analyze_all(articles, args.company, args.industry, client)

    # ── サマリー表示 ───────────────────────────────────────
    print_summary(data, args.company)

    # ── 散布図生成 ─────────────────────────────────────────
    print("\n[CHART] 散布図を生成中...")
    fig = build_chart(data, args.company, args.industry, args.hours)

    output_path = args.output or f"social_monitor_{args.company}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    fig.write_html(output_path, include_plotlyjs="cdn")
    print(f"[OK] 散布図を保存しました: {output_path}")
    print("   ブラウザで開いてポイントにカーソルを当てると詳細が見えます。\n")


if __name__ == "__main__":
    main()
