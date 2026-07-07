#!/usr/bin/env python3
import sys, logging, threading, time, urllib.parse
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime as _parse_rss_date
from flask import Flask, jsonify

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

import feedparser
import yfinance as yf

app = Flask(__name__)

# ── 設定 ──────────────────────────────────────────────────────────────────
REFRESH = 21600
MAX_ART = 6

TOPICS = {
    "日米関係": {
        "label": "[JP/US] 日米関係 — Japan-US Relations",
        "color": "#00c8ff",
        "queries": ["Japan US relations", "US Japan trade tariffs alliance"],
    },
    "米中関係": {
        "label": "[US/CN] 米中関係 — US-China Relations",
        "color": "#ffc840",
        "queries": ["US China relations", "China tariffs trade war"],
    },
    "米イラン関係": {
        "label": "[US/IR] 米イラン関係 — US-Iran Relations",
        "color": "#ff4060",
        "queries": ["US Iran relations", "Iran sanctions nuclear deal"],
    },
    "台湾関係": {
        "label": "[Taiwan] 台湾関係 — Taiwan",
        "color": "#ff9040",
        "queries": ["Taiwan China US relations", "Taiwan strait tensions"],
    },
    "自動車産業": {
        "label": "[AUTO] 自動車産業 — Automotive Industry",
        "color": "#40ff90",
        "queries": ["automotive industry 2025", "electric vehicle EV tariffs"],
    },
}

ENERGY = {
    "WTI 原油":        "CL=F",
    "ブレント原油":    "BZ=F",
    "天然ガス":        "NG=F",
    "灯油":            "HO=F",
    "ガソリン RBOB":   "RB=F",
}

RARE = {
    "REMX ETF":            "REMX",
    "MP Materials":        "MP",
    "Energy Fuels (UUUU)": "UUUU",
    "Lynas RE (ADR)":      "LYSCF",
    "Albemarle リチウム":  "ALB",
    "SQM リチウム":        "SQM",
}

# ── データ取得 ────────────────────────────────────────────────────────────
def _pub_to_str(pub_raw: str) -> str:
    """RSS published 文字列を 'YYYY-MM-DD HH:MM' (UTC) に変換"""
    if not pub_raw:
        return ""
    try:
        return _parse_rss_date(pub_raw).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""

def rss(query, n=6):
    # Google News に after: フィルタを付けて2日以内の記事のみ取得
    after_date = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
    q = urllib.parse.quote(f"{query} after:{after_date}")
    url = f"https://news.google.com/rss/search?q={q}&hl=en&gl=US&ceid=US:en"
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "WorldDash/1.0"})
        results = []
        for e in feed.entries:
            title = e.get("title", "").strip()
            if not title:
                continue
            pub_raw = e.get("published", "")
            # 日付が取れる場合は2日以内か確認
            if pub_raw:
                try:
                    if _parse_rss_date(pub_raw) < cutoff:
                        continue  # 2日より古い記事はスキップ
                except Exception:
                    pass  # パース失敗は通す
            results.append({
                "title":     title,
                "source":    e.get("source", {}).get("title", ""),
                "link":      e.get("link", ""),
                "published": _pub_to_str(pub_raw),
            })
            if len(results) >= n:
                break
        return results
    except Exception:
        return []

def get_news():
    out = {}
    for name, cfg in TOPICS.items():
        seen, arts = set(), []
        for q in cfg["queries"]:
            for a in rss(q):
                k = a["title"][:50].lower()
                if k not in seen:
                    seen.add(k)
                    arts.append(a)
                if len(arts) >= MAX_ART:
                    break
            if len(arts) >= MAX_ART:
                break
        out[name] = arts
    return out

def get_price(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="5d", auto_adjust=True)
        if hist.empty:
            return None
        closes = hist["Close"].dropna()
        if len(closes) < 1:
            return None
        p    = float(closes.iloc[-1])
        prev = float(closes.iloc[-2]) if len(closes) >= 2 else p
        if prev == 0:
            return None
        chg = p - prev
        return {"price": round(p, 2), "change": round(chg, 2), "pct": round(chg / prev * 100, 2)}
    except Exception:
        return None

def get_prices(tmap):
    return [{"name": name, "ticker": t, "data": get_price(t)} for name, t in tmap.items()]

# ── キャッシュ ────────────────────────────────────────────────────────────
_cache = {"news": {}, "energy": [], "rare": [], "updated": None}
_lock  = threading.Lock()

def fetch_all():
    """全データを取得してキャッシュに書き込む"""
    try:
        news   = get_news()
        energy = get_prices(ENERGY)
        rare   = get_prices(RARE)
        with _lock:
            _cache.update({"news": news, "energy": energy, "rare": rare,
                           "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        logging.info("キャッシュ更新完了")
    except Exception as e:
        logging.error("fetch_all エラー: %s", e)

def bg_loop():
    while True:
        fetch_all()
        time.sleep(REFRESH)

# ── ルート ────────────────────────────────────────────────────────────────
@app.route("/api/data")
def api_data():
    with _lock:
        return jsonify(dict(_cache))

@app.route("/")
def index():
    topics_js = str([
        {"key": k, "label": v["label"], "color": v["color"]}
        for k, v in TOPICS.items()
    ])
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>World Dashboard</title>
<style>
:root{{--bg:#04040c;--panel:#0a0a1e;--border:#1a1a36;--text:#b0b0d0;--dim:#404060;--up:#30ff80;--dn:#ff3050}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI','Noto Sans JP',sans-serif;font-size:12px;min-height:100vh;display:flex;flex-direction:column}}
header{{background:#060614;border-bottom:1px solid var(--border);padding:10px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0}}
.logo{{font-size:16px;font-weight:900;color:#fff}}.logo em{{color:#00c8ff;font-style:normal}}
.badge{{font-size:9px;font-weight:800;letter-spacing:2px;color:#30ff80;border:1px solid rgba(48,255,128,.4);padding:2px 8px;border-radius:3px}}
.dot{{width:7px;height:7px;border-radius:50%;background:#30ff80;box-shadow:0 0 6px #30ff80;animation:blink .9s ease-in-out infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.15}}}}
.upd{{font-size:10px;color:var(--dim);margin-left:auto}}
main{{flex:1;display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:auto auto;gap:1px;background:var(--border)}}
.panel{{background:var(--panel);display:flex;flex-direction:column;overflow:hidden}}
.ph{{padding:7px 10px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:6px;flex-shrink:0}}
.ph-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0;animation:blink .9s ease-in-out infinite}}
.ph-label{{font-size:11px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pb{{flex:1;overflow-y:auto;padding:4px 8px}}
.pb::-webkit-scrollbar{{width:3px}}.pb::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
.art{{padding:5px 0;border-bottom:1px solid var(--border)}}
.art:last-child{{border-bottom:none}}
a.at{{display:block;color:var(--text);text-decoration:none;font-size:11px;line-height:1.4}}
a.at:hover{{color:#fff}}
.am{{font-size:9px;color:var(--dim);margin-top:1px}}
.price-section{{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border)}}
.ptbl{{width:100%;border-collapse:collapse;font-size:11px}}
.ptbl th{{padding:3px 8px;font-size:8px;font-weight:700;letter-spacing:1px;color:var(--dim);text-transform:uppercase;border-bottom:1px solid var(--border);text-align:right}}
.ptbl th:first-child{{text-align:left}}
.ptbl td{{padding:4px 8px;border-bottom:1px solid var(--border);text-align:right;white-space:nowrap}}
.ptbl td:first-child{{text-align:left}}
.ptbl tr:last-child td{{border-bottom:none}}
.ptbl tr:hover td{{background:rgba(255,255,255,.02)}}
.up{{color:var(--up)}}.dn{{color:var(--dn)}}.na{{color:var(--dim)}}
footer{{flex-shrink:0;background:#060614;border-top:1px solid var(--border);padding:5px 16px;font-size:9px;color:var(--dim)}}
</style>
</head>
<body>
<header>
  <div class="logo">&#127758; World <em>Dashboard</em></div>
  <div class="badge"><span class="dot"></span>&nbsp;LIVE</div>
  <div class="upd" id="upd">取得中...</div>
</header>
<main id="main">
  <div style="grid-column:1/-1;padding:24px;text-align:center;color:var(--dim)">データ取得中 / Loading...</div>
</main>
<footer>データソース: Google News RSS + Yahoo Finance (yfinance) &nbsp;|&nbsp; 自動更新: {REFRESH}秒ごと</footer>
<script>
const TOPICS = {topics_js};
const REFRESH = {REFRESH};

function esc(s){{return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}}
function chg(d){{
  if(!d||d.data===null||d.data===undefined)return '<span class="na">N/A</span>';
  const c=d.data.change,p=d.data.pct,cls=c>=0?'up':'dn',a=c>=0?'▲':'▼',s=c>=0?'+':'';
  return `<span class="${{cls}}">${{a}} ${{s}}${{c.toFixed(2)}} (${{s}}${{p.toFixed(2)}}%)</span>`;
}}

async function refresh(){{
  try{{
    const res = await fetch('/api/data');
    const data = await res.json();
    if(data.updated) document.getElementById('upd').textContent='更新: '+data.updated;

    let html='';
    // News panels
    TOPICS.forEach(t=>{{
      const arts=(data.news||{{}})[t.key]||[];
      html+=`<div class="panel">
        <div class="ph">
          <span class="ph-dot" style="background:${{t.color}};box-shadow:0 0 5px ${{t.color}}"></span>
          <span class="ph-label" style="color:${{t.color}}">${{esc(t.label)}}</span>
        </div>
        <div class="pb">
          ${{arts.length?arts.map(a=>`<div class="art">
            <a class="at" href="${{esc(a.link||'#')}}" target="_blank">${{esc(a.title)}}</a>
            <div class="am">${{esc(a.source)}}${{a.published?' · '+esc(a.published):''}}
            </div></div>`).join(''):'<div style="padding:8px;color:var(--dim)">取得中...</div>'}}
        </div>
      </div>`;
    }});

    // Price sections
    const mkTable=(items,title)=>{{
      const rows=items.map(i=>{{
        const ok=i.data&&i.data.price!=null;
        const cls=ok?(i.data.change>=0?'up':'dn'):'na';
        const arr=ok?(i.data.change>=0?'▲':'▼'):'';
        return `<tr>
          <td>${{esc(i.name)}}&nbsp;<span style="font-size:9px;color:var(--dim)">${{esc(i.ticker)}}</span></td>
          <td class="${{cls}}" style="font-weight:700;font-family:monospace">${{ok?arr+' $'+i.data.price.toFixed(2):'N/A'}}</td>
          <td>${{chg(i)}}</td>
        </tr>`;
      }}).join('');
      return `<div class="panel">
        <div class="ph"><span class="ph-label" style="color:#ffc840">${{title}}</span></div>
        <div class="pb"><table class="ptbl">
          <thead><tr><th style="text-align:left">銘柄</th><th>価格 (USD)</th><th>前日比</th></tr></thead>
          <tbody>${{rows}}</tbody>
        </table></div>
      </div>`;
    }};

    html+=`<div class="price-section">
      ${{mkTable(data.energy||[],'⚡ エネルギー価格 — Energy Prices')}}
      ${{mkTable(data.rare||[],'⚛ レアアース関連指標 — Rare Earth Proxies')}}
    </div>`;

    document.getElementById('main').innerHTML=html;
  }}catch(e){{console.error(e)}}
}}

refresh();
setInterval(refresh, REFRESH*1000);
</script>
</body>
</html>"""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    # 起動直後に1回データ取得してからサーバーを開始
    logging.info("初回データ取得中...")
    fetch_all()
    # 以降は6時間ごとにバックグラウンドで更新
    threading.Thread(target=bg_loop, daemon=True).start()
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
