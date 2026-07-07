"""
Gemini Web検索スケジューラー
----------------------------
使い方:
  pip install google-genai schedule
  python gemini_search_scheduler.py

設定は config.json で行います（初回起動時に自動生成）。
"""

import json
import os
import time
import schedule
import datetime
import pathlib
from google import genai
from google.genai import types

# ── 設定ファイルのパス ────────────────────────────────────────────
CONFIG_FILE = "config.json"
OUTPUT_DIR  = "search_results"

DEFAULT_CONFIG = {
    "api_key": "YOUR_GEMINI_API_KEY",
    "keywords": ["AIニュース", "Python最新情報"],
    "target_urls": [],
    "schedule": {
        "type": "interval_hours",
        "interval": 24,
        "daily_time": "09:00"
    },
    "output_format": "both",
    "max_results_per_keyword": 5
}

# 無料枠対策パラメータ
WAIT_BETWEEN_KEYWORDS = 10   # キーワード間の待機秒数
MAX_RETRY             = 3    # 429エラー時の最大リトライ回数
RETRY_WAIT            = 65   # リトライ前の待機秒数（1分+余裕）

# ── 設定の読み込み / 初期化 ────────────────────────────────────────
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        print(f"[設定ファイルを生成しました: {CONFIG_FILE}]")
        print("api_key を設定してから再実行してください。")
        exit(0)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)

# ── Gemini クライアント初期化 ──────────────────────────────────────
def init_client(api_key: str):
    return genai.Client(api_key=api_key)

# ── 1キーワードの検索 ─────────────────────────────────────────────
def search_keyword(client, keyword: str, target_urls: list) -> dict:
    site_hint = ""
    if target_urls:
        site_hint = "以下のサイトを優先して検索してください:\n"
        site_hint += "\n".join(f"  - {u}" for u in target_urls)
        site_hint += "\n\n"

    prompt = (
        f"{site_hint}"
        f"キーワード「{keyword}」についてWebで検索し、"
        f"最新情報を日本語で400字程度に要約してください。"
        f"情報の鮮度・重要度が高いものを優先してください。"
        f"情報源のURLも含めてください。"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        summary = response.text

        sources = []
        try:
            meta = response.candidates[0].grounding_metadata
            for chunk in meta.grounding_chunks:
                if hasattr(chunk, "web") and chunk.web.uri:
                    sources.append(chunk.web.uri)
        except Exception:
            pass

        return {"keyword": keyword, "summary": summary, "sources": sources, "error": None}

    except Exception as e:
        return {"keyword": keyword, "summary": "", "sources": [], "error": str(e)}

# ── リトライ付き検索 ──────────────────────────────────────────────
def search_keyword_with_retry(client, kw, urls):
    for attempt in range(1, MAX_RETRY + 1):
        result = search_keyword(client, kw, urls)
        if result["error"] and "429" in str(result["error"]):
            if attempt < MAX_RETRY:
                print(f"\n    レート制限検知 → {RETRY_WAIT}秒待機してリトライ ({attempt}/{MAX_RETRY})...")
                time.sleep(RETRY_WAIT)
            else:
                print(f"\n    リトライ上限({MAX_RETRY}回)に達しました。スキップします。")
        else:
            return result
    return result

# ── 全キーワードの一括検索 ────────────────────────────────────────
def run_all_searches(config: dict):
    print(f"\n[{now_str()}] 検索開始")
    client   = init_client(config["api_key"])
    keywords = config.get("keywords", [])
    urls     = config.get("target_urls", [])
    results  = []

    for i, kw in enumerate(keywords):
        print(f"  検索中: 「{kw}」...", end=" ", flush=True)
        result = search_keyword_with_retry(client, kw, urls)
        if result["error"]:
            print(f"エラー: {result['error']}")
        else:
            print(f"完了 ({len(result['sources'])} ソース)")
        results.append(result)
        if i < len(keywords) - 1:
            print(f"    ({WAIT_BETWEEN_KEYWORDS}秒待機中...)")
            time.sleep(WAIT_BETWEEN_KEYWORDS)

    save_results(results, config)
    print(f"[{now_str()}] 保存完了\n")

# ── 結果の保存 ────────────────────────────────────────────────────
def save_results(results: list, config: dict):
    pathlib.Path(OUTPUT_DIR).mkdir(exist_ok=True)
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fmt = config.get("output_format", "markdown")

    if fmt in ("markdown", "both"):
        save_markdown(results, ts, config)
    if fmt in ("json", "both"):
        save_json(results, ts)

def save_markdown(results, ts, config):
    path = os.path.join(OUTPUT_DIR, f"report_{ts}.md")
    urls = config.get("target_urls", [])
    lines = [
        "# Gemini Web検索レポート",
        f"生成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
    ]
    if urls:
        lines += ["", "## 検索対象サイト", ""] + [f"- {u}" for u in urls]
    lines += ["", "---", ""]

    for r in results:
        lines += [f"## キーワード: {r['keyword']}", ""]
        if r["error"]:
            lines += [f"> エラー: {r['error']}", ""]
        else:
            lines += [r["summary"], ""]
            if r["sources"]:
                lines += ["### 参照ソース", ""] + [f"- {s}" for s in r["sources"]] + [""]
        lines.append("---\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  → Markdown保存: {path}")

def save_json(results, ts):
    path = os.path.join(OUTPUT_DIR, f"report_{ts}.json")
    data = {
        "generated_at": datetime.datetime.now().isoformat(),
        "results": results
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  → JSON保存: {path}")

# ── ユーティリティ ────────────────────────────────────────────────
def now_str():
    return datetime.datetime.now().strftime("%H:%M:%S")

# ── スケジューリング ──────────────────────────────────────────────
def setup_schedule(config: dict):
    sched      = config.get("schedule", {})
    stype      = sched.get("type", "interval_hours")
    interval   = sched.get("interval", 24)
    daily_time = sched.get("daily_time", "09:00")

    def job():
        run_all_searches(config)

    if stype == "interval_minutes":
        schedule.every(interval).minutes.do(job)
        print(f"スケジュール: {interval}分ごとに実行")
    elif stype == "interval_hours":
        schedule.every(interval).hours.do(job)
        print(f"スケジュール: {interval}時間ごとに実行")
    elif stype == "daily":
        schedule.every().day.at(daily_time).do(job)
        print(f"スケジュール: 毎日 {daily_time} に実行")
    else:
        print(f"不明なスケジュールタイプ: {stype}")
        exit(1)

# ── メイン ────────────────────────────────────────────────────────
if __name__ == "__main__":
    config = load_config()

    if config["api_key"] == "YOUR_GEMINI_API_KEY":
        print("config.json の api_key を設定してください。")
        exit(1)

    print("=" * 50)
    print("  Gemini Web検索スケジューラー")
    print("=" * 50)
    print(f"キーワード: {config['keywords']}")
    if config["target_urls"]:
        print(f"検索対象サイト: {config['target_urls']}")
    print(f"出力ディレクトリ: {OUTPUT_DIR}/")
    print()

    run_all_searches(config)
    setup_schedule(config)

    print("スケジューラー起動中 (Ctrl+C で終了)\n")
    while True:
        schedule.run_pending()
        time.sleep(30)
