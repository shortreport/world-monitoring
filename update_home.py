#!/usr/bin/env python3
"""
update_home.py  —  ホームページ用データ収集スクリプト

処理の流れ:
  1. dashboard_app.py (5001) / news_app.py (5002) を自動起動
  2. 5001/5002 から記事を収集し Claude で5大事象を選定
  3. docs/data/home_latest.json に保存
  4. --with-economist 時: Outlook の Economist フォルダーを取得し
     Claude で要約 → docs/data/economist_latest.json に保存
  5. generate_site.py を実行して docs/ を再生成
  6. git add / commit / push でサイトを更新

使用法:
  python update_home.py                    # ニュースのみ
  python update_home.py --with-economist   # ニュース + Economist

タスクスケジューラ登録:
  06:30  → scripts/update_home_full.bat   (--with-economist)
  12:30  → scripts/update_home_news.bat
  18:30  → scripts/update_home_news.bat
  00:30  → scripts/update_home_news.bat
"""

import os, sys, json, socket, subprocess, time, re, argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ── 定数 ─────────────────────────────────────────────────────────────────────
JST       = timezone(timedelta(hours=9))
TODAY     = datetime.now(JST)
DATE_JP   = TODAY.strftime("%Y年%m月%d日")
NOW_STR   = TODAY.strftime("%Y-%m-%d %H:%M JST")

BASE          = Path(__file__).parent
DOCS_DATA_DIR = BASE / "docs" / "data"
HOME_JSON     = DOCS_DATA_DIR / "home_latest.json"
ECONOMIST_JSON = DOCS_DATA_DIR / "economist_latest.json"

CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# ── API キー読み込み ──────────────────────────────────────────────────────────
def _get_api_key() -> str:
    """優先順位: 環境変数 > api_config.py"""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    try:
        sys.path.insert(0, str(BASE))
        import api_config
        return api_config.ANTHROPIC_API_KEY
    except Exception:
        pass
    raise RuntimeError(
        "ANTHROPIC_API_KEY が見つかりません。"
        "環境変数 ANTHROPIC_API_KEY または api_config.py に設定してください。"
    )


# ── ポート確認 / サーバー起動 ─────────────────────────────────────────────────
def _is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("localhost", port)) == 0


def _start_server(script: str, port: int):
    """サーバーが未起動なら起動して Popen を返す。起動済みなら None を返す。"""
    if _is_port_open(port):
        print(f"  :{port} はすでに起動中")
        return None
    print(f"  :{port} 起動中 ({script}) ...")
    proc = subprocess.Popen(
        [sys.executable, str(BASE / script)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(BASE),
    )
    # 最大 45 秒待機
    for i in range(45):
        time.sleep(1)
        if _is_port_open(port):
            print(f"  :{port} 起動完了 ({i+1}秒)")
            return proc
    print(f"  [WARN] :{port} が {45}秒経っても応答しません")
    return proc


# ── ニュース収集 + Claude 分析 ────────────────────────────────────────────────
def fetch_home_segments(api_key: str) -> list | None:
    """
    5001/5002 から記事を取得し Claude で5大事象を選定。
    docs/data/home_latest.json に保存して返す。
    失敗時は None を返す。
    """
    import requests as _req
    import anthropic

    print("\n[ニュース収集] サーバーから記事を取得中...")

    def _pick_date(a: dict) -> str:
        for key in ("date", "published", "published_at", "publishedAt", "pubDate",
                    "pub_date", "created_at", "timestamp"):
            v = a.get(key)
            if v:
                return str(v)[:16]
        return ""

    # ── 5001: refresh → /api/data ────────────────────────────────────────
    try:
        print("  5001: リフレッシュ中（30〜60秒かかります）...")
        _req.post("http://localhost:5001/api/refresh", timeout=120)
        print("  5001: リフレッシュ完了")
    except Exception as e:
        print(f"  5001: リフレッシュ失敗（キャッシュ使用）: {e}")

    articles_5001 = []
    try:
        r = _req.get("http://localhost:5001/api/data", timeout=10)
        r.raise_for_status()
        for topic, arts in r.json().get("news", {}).items():
            for a in arts:
                articles_5001.append({
                    "topic":   topic,
                    "title":   a.get("title", ""),
                    "source":  a.get("source", ""),
                    "url":     a.get("link", ""),
                    "date":    _pick_date(a),
                    "summary": "",
                })
        print(f"  5001: {len(articles_5001)} 件取得")
    except Exception as e:
        print(f"  5001 取得失敗（サーバー未応答？）: {e}")

    # ── 5002: refresh → /api/news ────────────────────────────────────────
    try:
        print("  5002: リフレッシュ中（30〜60秒かかります）...")
        _req.post("http://localhost:5002/api/refresh", timeout=120)
        print("  5002: リフレッシュ完了")
    except Exception as e:
        print(f"  5002: リフレッシュ失敗（キャッシュ使用）: {e}")

    articles_5002 = []
    try:
        r = _req.get("http://localhost:5002/api/news", timeout=10)
        r.raise_for_status()
        for topic, arts in r.json().get("articles", {}).items():
            for a in arts:
                bullets = a.get("bullets", [])
                summary = "; ".join(bullets[:3]) if bullets else a.get("summary", "")[:150]
                articles_5002.append({
                    "topic":   topic,
                    "title":   a.get("title", ""),
                    "source":  a.get("source", ""),
                    "url":     a.get("url", ""),
                    "date":    _pick_date(a),
                    "summary": summary,
                })
        print(f"  5002: {len(articles_5002)} 件取得")
    except Exception as e:
        print(f"  5002 取得失敗（サーバー未応答？）: {e}")

    all_articles = articles_5001 + articles_5002
    if not all_articles:
        print("  両サーバー未応答 — home_latest.json の更新をスキップします。")
        return None

    # ── 48時間以内の記事のみ使用（古いニュース混入防止） ─────────────────
    def _parse_pub(s: str):
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
            try:
                return datetime.strptime(s[:16], fmt)
            except ValueError:
                pass
        return None

    cutoff_48h = TODAY.replace(tzinfo=None) - timedelta(hours=48)
    recent, skipped = [], 0
    for a in all_articles:
        dt = _parse_pub(a.get("date", ""))
        if dt is None or dt >= cutoff_48h:
            recent.append(a)
        else:
            skipped += 1
    all_articles = recent
    print(f"  日付フィルタ: {len(all_articles)} 件使用 / {skipped} 件除外（48時間超）")
    if not all_articles:
        print("  フィルタ後に記事がゼロ — home_latest.json の更新をスキップします。")
        return None

    # ── 記事に連番を振り、Claude に渡すテキストを構築 ────────────────────
    lines = []
    for idx, a in enumerate(all_articles, 1):
        a["_ref_id"] = idx
        date_tag = f"[{a['date']}]" if a.get("date") else ""
        line = f"[{idx}] {date_tag}[{a['topic']}] ({a['source']}) {a['title']}"
        if a.get("summary"):
            line += f" / {a['summary']}"
        lines.append(line)
    articles_text = "\n".join(lines)

    prompt = f"""\
今日の日付: {DATE_JP}

以下は{DATE_JP}時点で収集した世界ニュース記事リストです（日本語・英語メディア横断）。
すべての記事は48時間（2日）以内に発行されたものです。
公開日が分かる記事には[日付]を付記しています。

{articles_text}

この記事群のみを根拠として、現在最も大きく報道されている重要な国際ニュース事象を最大5つ選定してください。
**重要**: 必ず直近48時間以内の記事を根拠とすること。[日付]が2日以上前の記事は選ばないこと。
各事象について5W2H（誰が・何を・いつ・どこで・なぜ・どのように・いくら）を意識してまとめ、
以下のJSON配列のみを出力してください（前置き・コードブロック不要）。

ルール:
・文末は体言止めを最優先（例:「〜を発表」「〜で合意」「〜が急騰」「〜を警告」）。体言止めで自然に表現できない場合のみ「です」「ます」を使用。「だ」「である」「した」「します」は使わない
・badge: 「① テーマ名」形式（テーマ名は8文字以内）
・title: 20文字以内
・subtitle: 40文字以内
・bullets: 5〜6項目、各40文字以内（記事に記載のある情報のみ、最新の動向を先に書く）
・risk: 「▲リスク：」で始め、リスクが顕在化しうるタイムラインも記載
・context: 「背景：」で始める
・color: YEL（米中・貿易）RED（戦争・危機）CYAN（日米・外交）ORG（台湾・安保）GRN（産業・技術）から選択
・search_en: このセグメントをGoogle Newsで検索するための英語キーワード（5〜8語の名詞句、例: "US Iran ceasefire Hormuz strait 2026"）
・source_refs: このセグメントの各bullet（1〜5番目）に最も関連する記事番号のリスト（上記 [1]〜[N] から選ぶ。bulletと同数か、最大5つ）

[
  {{
    "badge": "① テーマ名",
    "color": "YEL",
    "title": "タイトル",
    "subtitle": "サブタイトル",
    "search_en": "English search keywords 5 to 8 words",
    "source_refs": [1, 5, 12, 23, 30],
    "bullets": ["箇条1", "箇条2", "箇条3", "箇条4", "箇条5"],
    "risk": "▲リスク：内容とタイムライン",
    "context": "背景：内容"
  }}
]"""

    print("  Claude で5大事象を分析・選定中...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*", "", raw)
        segments_data = json.loads(raw)
    except Exception as e:
        print(f"  [WARN] Claude 分析失敗: {e}")
        return None

    # ── JSON 形式に整形して保存 ───────────────────────────────────────────
    # 記事番号 → (url, source) の逆引きテーブル
    id_to_art = {a["_ref_id"]: a for a in all_articles if a.get("_ref_id")}

    valid_colors = {"YEL", "RED", "CYAN", "ORG", "GRN"}
    result = []
    for item in segments_data[:5]:
        color = item.get("color", "CYAN")
        if color not in valid_colors:
            color = "CYAN"

        bullets_text = item.get("bullets", [])
        source_refs  = item.get("source_refs", [])

        # 各 bullet に対応する記事URLを解決
        bullet_sources = []
        for i, bt in enumerate(bullets_text):
            ref_id = (source_refs[i] if i < len(source_refs)
                      else (source_refs[-1] if source_refs else None))
            art    = id_to_art.get(ref_id) if ref_id else None
            bullet_sources.append({
                "text":   bt,
                "url":    art.get("url", "") if art else "",
                "source": art.get("source", "News") if art else "News",
            })

        result.append({
            "badge":     item.get("badge", "① ニュース"),
            "color":     color,
            "title":     item.get("title", ""),
            "subtitle":  item.get("subtitle", ""),
            "search_en": item.get("search_en", ""),
            "bullets":   bullet_sources if bullet_sources else bullets_text,
            "risk":      item.get("risk", ""),
            "context":   item.get("context", ""),
        })

    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at":  NOW_STR,
        "article_count": len(all_articles),
        "segments":      result,
    }
    HOME_JSON.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  [OK] home_latest.json に {len(result)} 件保存 ({HOME_JSON})")
    return result


# ── Economist メール処理（テキスト + 画像URL のみ） ───────────────────────────
def _find_folder(parent, name):
    for folder in parent.Folders:
        if folder.Name == name:
            return folder
        found = _find_folder(folder, name)
        if found:
            return found
    return None


def _parse_economist_html(html_body: str) -> dict:
    """Economist HTML から Today's top stories / The day ahead のテキストと画像URLを抽出"""
    from bs4 import BeautifulSoup

    soup     = BeautifulSoup(html_body, "html.parser")
    html_low = html_body.lower()

    # 画像URL一覧（ロゴ・スペーサーを除外）
    img_positions = []
    for tag in soup.find_all("img"):
        src = tag.get("src", "")
        if not src.startswith("http"):
            continue
        try:
            if int(tag.get("width", 999)) < 200:
                continue
        except Exception:
            pass
        pos = html_body.find(src)
        if pos != -1:
            img_positions.append((pos, src))
    img_positions.sort(key=lambda x: x[0])

    TOP_KWS = ["today's top stories", "today&#39;s top stories",
               "today&rsquo;s top stories", "today’s top stories"]
    DAY_KWS = ["the day ahead"]

    def _html_pos(kws):
        for kw in kws:
            idx = html_low.find(kw.lower())
            if idx != -1:
                return idx
        return -1

    full_text    = soup.get_text("\n")
    full_low     = full_text.lower()
    top_html_pos = _html_pos(TOP_KWS)
    day_html_pos = _html_pos(DAY_KWS)

    def _text_pos(kws):
        for kw in kws:
            idx = full_low.find(kw.lower())
            if idx != -1:
                return idx
        return -1

    top_text_pos = _text_pos(TOP_KWS)
    day_text_pos = _text_pos(DAY_KWS)

    result = {"top_text": "", "top_img_url": None,
              "day_text": "", "day_img_url": None}

    if top_text_pos != -1:
        end = (day_text_pos if (day_text_pos != -1 and day_text_pos > top_text_pos)
               else top_text_pos + 4000)
        result["top_text"] = full_text[top_text_pos:end].strip()
    if day_text_pos != -1:
        result["day_text"] = full_text[day_text_pos:day_text_pos + 4000].strip()

    # スライド2 画像: "Today's top stories" の直前の最も近い画像
    if top_html_pos != -1:
        before = [(p, s) for p, s in img_positions if p < top_html_pos]
        if before:
            result["top_img_url"] = before[-1][1]
    if not result["top_img_url"] and img_positions:
        result["top_img_url"] = img_positions[0][1]

    # スライド3 画像: "The day ahead" の直後の最も近い画像
    if day_html_pos != -1:
        after = [(p, s) for p, s in img_positions if p > day_html_pos]
        if after:
            result["day_img_url"] = after[0][1]
    if not result["day_img_url"] and img_positions:
        result["day_img_url"] = img_positions[-1][1]

    return result


def _summarize_economist(section_name: str, text: str, api_key: str) -> list:
    """Claude で Economist メールのセクションを箇条書き要約して返す"""
    import anthropic
    prompt = (
        f"以下はThe Economistのメールの「{section_name}」セクションの内容です。\n"
        "日本語で要点を5〜7箇条にまとめてください。\n"
        "各箇条は「●」で始め、簡潔に1〜2文でまとめてください。\n"
        "文末は体言止めを最優先（例:「〜を発表」「〜で合意」「〜が急騰」「〜と警告」）。"
        "体言止めで自然に表現できない場合のみ「です」「ます」を使用。"
        "「だ」「である」「した」「します」は使わない。\n"
        "【固有名詞】国名・地名・人名は正確なカタカナで表記すること。"
        "漢字とカタカナを混在させない（例: ウクライナ ○ / 烏クライナ ×、ロシア ○ / 露シア ×）。\n"
        "要点のみを出力し、前置きや見出しは不要です。\n\n"
        f"内容:\n{text[:4000]}"
    )
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=900,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _download_image(url: str, save_path: Path) -> bool:
    """画像URLをダウンロードして save_path に保存する。成功時 True を返す。"""
    import requests as _req
    try:
        r = _req.get(url, timeout=20,
                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        r.raise_for_status()
        save_path.write_bytes(r.content)
        print(f"  [OK] 画像保存: {save_path.name} ({len(r.content)//1024} KB)")
        return True
    except Exception as e:
        print(f"  [WARN] 画像ダウンロード失敗: {e}")
        return False


OUTLOOK_EXE = r"C:\Program Files\Microsoft Office\Root\Office16\OUTLOOK.EXE"

def _get_outlook_app():
    """
    Outlook COM オブジェクトを取得する。
    既に起動済みの場合のみ接続する（バックグラウンド実行時に自動起動しない）。
    """
    import win32com.client, subprocess

    # ① 既に起動済みか試みる
    try:
        app = win32com.client.GetActiveObject("Outlook.Application")
        print("  既存の Outlook に接続しました")
        return app
    except Exception:
        pass

    # ② Outlook プロセスが存在しない場合はスキップ（自動起動しない）
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq OUTLOOK.EXE", "/NH"],
        capture_output=True, text=True
    )
    if "OUTLOOK.EXE" not in result.stdout:
        raise RuntimeError("Outlook が起動していません（スキップ）")

    # ③ プロセスはあるが GetActiveObject に失敗した場合（起動直後など）
    import pythoncom, time
    try:
        pythoncom.CoInitialize()
    except Exception:
        pass
    try:
        app = win32com.client.Dispatch("Outlook.Application")
        time.sleep(3)
        print("  Outlook を Dispatch で起動しました")
        return app
    except Exception as e:
        raise RuntimeError(f"Outlook の接続に失敗しました: {e}")


def fetch_economist_for_web(api_key: str) -> dict | None:
    """
    Outlook の Economist フォルダーから最新メールを取得し要約する。
    （未読・既読問わず最新1件を使用）
    docs/data/economist_latest.json と economist_cover.jpg に保存して返す。
    失敗時 → None を返す。
    """
    print("\n[Economist] Outlook に接続中...")
    try:
        import win32com.client
    except ImportError:
        print("  [WARN] win32com が利用できません（Outlook 未インストール？）")
        return None

    try:
        outlook = _get_outlook_app()
        ns = outlook.GetNamespace("MAPI")
    except Exception as e:
        print(f"  [WARN] Outlook 接続失敗: {e}")
        return None

    folder = None
    for store in ns.Stores:
        try:
            root = store.GetRootFolder()
            folder = _find_folder(root, "Economist")
            if folder:
                break
        except Exception:
            pass

    if not folder:
        print("  [WARN] 'Economist' フォルダーが見つかりません。スキップ。")
        return None

    items = folder.Items
    items.Sort("[ReceivedTime]", True)

    # 未読・既読問わず最新1件のメールを取得
    mail = None
    for m in items:
        if getattr(m, "Class", 0) == 43:  # olMail = 43
            mail = m
            break

    if mail is None:
        print("  Economist: メールなし — スキップ")
        return None

    subject   = getattr(mail, "Subject", "") or ""
    html_body = getattr(mail, "HTMLBody", "") or ""
    is_unread = getattr(mail, "UnRead", False)
    received  = getattr(mail, "ReceivedTime", None)
    recv_str  = str(received)[:16] if received else ""
    print(f"  件名: {subject}  受信: {recv_str}  未読: {is_unread}")

    if not html_body:
        print("  [WARN] HTMLBody が空。スキップ。")
        return None

    print("  HTML 解析中...")
    parsed = _parse_economist_html(html_body)

    top_bullets = []
    if parsed["top_text"]:
        print("  Today's top stories を要約中 (Claude)...")
        try:
            top_bullets = _summarize_economist(
                "Today's top stories", parsed["top_text"], api_key
            )
        except Exception as e:
            print(f"  [WARN] 要約エラー: {e}")

    day_bullets = []
    if parsed["day_text"]:
        print("  The day ahead を要約中 (Claude)...")
        try:
            day_bullets = _summarize_economist(
                "The day ahead", parsed["day_text"], api_key
            )
        except Exception as e:
            print(f"  [WARN] 要約エラー: {e}")

    if not top_bullets and not day_bullets:
        print("  [WARN] 要約結果が空。保存をスキップ。")
        return None

    # ── カバー画像をダウンロード ────────────────────────────────────────
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cover_local = None
    top_img_url = parsed.get("top_img_url")
    if top_img_url:
        print(f"  カバー画像をダウンロード中...")
        cover_path = DOCS_DATA_DIR / "economist_cover.jpg"
        if _download_image(top_img_url, cover_path):
            cover_local = "data/economist_cover.jpg"  # HTML から見た相対パス

    # 未読だった場合のみ既読に変更（make_news_video2.py との整合性を保つ）
    if is_unread:
        try:
            mail.UnRead = False
            print("  未読メールを既読に変更")
        except Exception:
            pass

    output = {
        "generated_at": NOW_STR,
        "subject":      subject,
        "received":     recv_str,
        "top_bullets":  top_bullets,
        "top_img_url":  top_img_url,
        "cover_local":  cover_local,
        "day_bullets":  day_bullets,
        "day_img_url":  parsed.get("day_img_url"),
    }
    ECONOMIST_JSON.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"  [OK] economist_latest.json に保存 "
        f"(top: {len(top_bullets)} 件, day: {len(day_bullets)} 件)"
    )
    return output


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Home page data updater")
    parser.add_argument(
        "--with-economist", action="store_true",
        help="Economist メールも処理する（毎朝 6:30 専用）",
    )
    parser.add_argument(
        "--no-generate", action="store_true",
        help="generate_site.py の呼び出しと git push をスキップ（B/C 生成用）",
    )
    args = parser.parse_args()

    print("=" * 60)
    print(f"update_home.py  {NOW_STR}")
    if args.with_economist:
        print("  モード: ニュース + Economist")
    else:
        print("  モード: ニュースのみ")
    print("=" * 60)

    # ── API キー取得 ─────────────────────────────────────────────────────
    try:
        api_key = _get_api_key()
    except RuntimeError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    # ── サーバー起動 ────────────────────────────────────────────────────
    print("\n[サーバー起動]")
    proc5001 = _start_server("dashboard_app.py", 5001)
    proc5002 = _start_server("news_app.py",      5002)

    # ── ニュース収集 ────────────────────────────────────────────────────
    fetch_home_segments(api_key)

    # ── Economist 処理（--with-economist のみ）─────────────────────────
    if args.with_economist:
        fetch_economist_for_web(api_key)

    # ── サーバーは停止しない ────────────────────────────────────────────
    # make_news_video2.py や他のスクリプトも同じ 5001/5002 を使うため、
    # 起動したサーバーはそのまま稼働させておく（PC再起動まで継続）
    print("\n[サーバー] 起動したまま継続（make_news_video2.py でも使用可能）")

    # ── GitHub Actions との競合を避けるため fetch + 選択チェックアウト ──────
    # git pull --rebase は GitHub Actions が生成した docs/index.html 等と
    # 衝突して REBASE_MERGE 状態に陥り、以降の実行も連鎖的に失敗するため使わない。
    print("\n[Git Sync] リモートの最新データを取り込み中...")
    # 前回失敗でリベース中状態が残っていれば中断
    subprocess.run(["git", "rebase", "--abort"], cwd=str(BASE), capture_output=True)
    # リモートの最新コミットを取得
    subprocess.run(["git", "fetch", "origin", "main"], cwd=str(BASE))
    # GitHub Actions が更新するデータファイルだけを最新化（ローカル生成 JSON は保持）
    for _remote_file in ["docs/data/trump_latest.json", "docs/data/theme_latest.json"]:
        subprocess.run(
            ["git", "checkout", "origin/main", "--", _remote_file],
            cwd=str(BASE), capture_output=True,
        )

    if args.no_generate:
        print("\n[サイト生成 / Git Push] --no-generate のためスキップ（bat ファイル側で処理）")
    else:
        # ── サイト HTML 再生成 ────────────────────────────────────────────
        print("\n[サイト生成]")
        result = subprocess.run(
            [sys.executable, str(BASE / "generate_site.py")],
            cwd=str(BASE),
        )
        if result.returncode != 0:
            print("  [WARN] generate_site.py が失敗しました")

        # ── git add / commit / push ───────────────────────────────────────
        print("\n[Git Push]")
        subprocess.run(["git", "add", "docs/"], cwd=str(BASE))
        diff = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            cwd=str(BASE),
        )
        if diff.returncode != 0:
            commit_msg = f"Home update: {NOW_STR}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE))
            push = subprocess.run(["git", "push"], cwd=str(BASE))
            if push.returncode != 0:
                print("  [WARN] push 失敗（リモート更新あり）、merge でリトライ...")
                subprocess.run(["git", "fetch", "origin", "main"], cwd=str(BASE))
                subprocess.run(
                    ["git", "merge", "-X", "ours", "origin/main", "--no-edit"],
                    cwd=str(BASE),
                )
                push = subprocess.run(["git", "push"], cwd=str(BASE))
            if push.returncode == 0:
                print("  [OK] push 完了。約1〜2分でサイトに反映されます。")
            else:
                print("  [WARN] push 失敗。git push を手動で実行してください。")
        else:
            print("  変更なし。スキップ。")

    print("\n[完了]")


if __name__ == "__main__":
    main()
