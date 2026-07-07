"""
risk_analyzer/analyze_claude.py
================================
指定フォルダー内の .docx / .pdf / .txt / .md を1件ずつ読み込み、
ファイルごとに Claude API でリスク分析し Markdown レポートを出力する。
レポートは元ファイルと同じ振り分け先フォルダーに保存される。

使い方:
    python analyze_claude.py --folder ./docs

APIキーの設定:
    環境変数 ANTHROPIC_API_KEY を設定するか、--api-key オプションで指定する。
    https://console.anthropic.com でキーを取得できる。
"""

import argparse
import datetime
import json
import os
import re
import shutil
import sys
import time

# ── サードパーティ ──────────────────────────────────────────
try:
    import anthropic
except ImportError:
    sys.exit(
        "❌ anthropic がインストールされていません。\n"
        "   `pip install anthropic` を実行してください。"
    )

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None


# ═══════════════════════════════════════════════════════════
# 1. テキスト抽出
# ═══════════════════════════════════════════════════════════

SUPPORTED = {".docx", ".pdf", ".txt", ".md"}

# 1ファイルあたり文字数上限（Claude は大容量コンテキストに対応）
CHARS_PER_FILE = 20000

MODEL = "claude-haiku-4-5"


def extract_text(path: str) -> str:
    """ファイル種別に応じてテキストを抽出する。失敗時は空文字を返す。"""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        if fitz is None:
            print(f"  ⚠️  PyMuPDF 未インストール。PDF をスキップ: {path}")
            return ""
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)

    if ext == ".docx":
        if DocxDocument is None:
            print(f"  ⚠️  python-docx 未インストール。DOCX をスキップ: {path}")
            return ""
        doc = DocxDocument(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext in (".txt", ".md"):
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()

    return ""


def collect_files(folder: str) -> list[str]:
    """フォルダー配下のサポート対象ファイルを再帰的に収集する。"""
    result = []
    for root, _, files in os.walk(folder):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() in SUPPORTED:
                result.append(os.path.join(root, name))
    return result


# ═══════════════════════════════════════════════════════════
# 2. Claude API でリスク分析
# ═══════════════════════════════════════════════════════════

# システムプロンプト（全リクエスト共通 → プロンプトキャッシュ対象）
SYSTEM_PROMPT = """あなたはリスク分析の専門家です。提供されたファイルの内容を分析し、JSONのみを返してください。他の文字・説明文は一切出力しないでください。

返すJSONの形式:
{"overall_summary":"ファイルの総合的な概要（3〜5文）","risks":[{"title":"リスクのタイトル（20字以内）","description":"リスクの詳細説明（最大100字程度）","severity":"高|中|低","schedule":"顕在化しうる日程・時期（不明なら要確認）","source_files":["関連するファイル名"]}]}

ルール:
- risksは重要度の高い順に最大5件。
- 日程情報が文書中にある場合は必ず抽出すること。
- 存在しないリスクを捏造しないこと。"""

USER_PROMPT_TEMPLATE = """以下のファイルを分析してください。

=== ファイル: {filename} ===
{file_text}"""

MAX_RETRIES = 5
RETRY_WAIT_DEFAULT = 60


def analyze_one_with_claude(fc: dict, client: anthropic.Anthropic) -> dict:
    """1ファイルをClaude APIに送り、リスク情報を返す。レート制限時はリトライする。"""
    text = fc["text"][:CHARS_PER_FILE]
    if len(fc["text"]) > CHARS_PER_FILE:
        text += "\n[以下省略]"

    user_prompt = USER_PROMPT_TEMPLATE.format(filename=fc["filename"], file_text=text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                # システムプロンプトにキャッシュを適用してコスト削減
                system=[{
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": user_prompt}],
            )
            raw = response.content[0].text.strip()

            # JSON 抽出（```json ... ``` ブロックに包まれている場合も対応）
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not json_match:
                raise ValueError(f"JSONが見つかりません。レスポンス: {raw[:300]}")
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError as je:
                raise ValueError(f"JSON解析エラー: {je}\n--- レスポンス先頭300字 ---\n{raw[:300]}") from je

        except anthropic.RateLimitError as e:
            retry_after = int(e.response.headers.get("retry-after", RETRY_WAIT_DEFAULT))
            wait_sec = retry_after + 5

            if attempt < MAX_RETRIES:
                print(f"  ⏳ レート制限（429）。{wait_sec} 秒待機後にリトライします... "
                      f"（{attempt}/{MAX_RETRIES}）")
                time.sleep(wait_sec)
            else:
                raise RuntimeError(
                    f"レート制限により {MAX_RETRIES} 回リトライしましたが失敗しました。"
                    f"しばらく時間をおいて再試行してください。"
                ) from e

        except (anthropic.APIConnectionError, anthropic.InternalServerError) as e:
            if attempt < MAX_RETRIES:
                wait_sec = 30 * attempt
                print(f"  ⏳ 一時的なAPIエラー。{wait_sec} 秒待機後にリトライします... "
                      f"（{attempt}/{MAX_RETRIES}）")
                time.sleep(wait_sec)
            else:
                raise

        except Exception:
            raise


# ═══════════════════════════════════════════════════════════
# 3. Markdown レポート生成
# ═══════════════════════════════════════════════════════════

SEVERITY_ICON = {"高": "🔴", "中": "🟡", "低": "🟢"}


def build_report(data: dict, fc: dict, folder: str) -> str:
    now = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
    risks = data.get("risks", [])

    lines = [
        "# 📋 リスク分析レポート",
        "",
        f"- **対象ファイル:** `{fc['filename']}`",
        f"- **対象フォルダー:** `{folder}`",
        f"- **作成日時:** {now}",
        f"- **使用モデル:** Claude Haiku 4.5 (Anthropic)",
        "",
        "---",
        "",
    ]

    # ── 総合概要 ─────────────────────────────────────────
    lines += ["## 📌 総合概要", ""]
    summary = data.get("overall_summary", "（概要なし）")
    for sentence in re.split(r"。", summary):
        sentence = sentence.strip()
        if sentence:
            lines.append(f"- {sentence}。")
    lines += ["", "---", ""]

    # ── リスク詳細 ────────────────────────────────────────
    lines += ["## 🔍 検出されたリスク", ""]

    if not risks:
        lines.append("リスクは検出されませんでした。")
        lines.append("")
    else:
        for i, risk in enumerate(risks, 1):
            sev = risk.get("severity", "不明")
            icon = SEVERITY_ICON.get(sev, "⚪")
            lines.append(f"### {i}. {icon} {risk.get('title', '（無題）')} `[{sev}]`")
            lines.append("")
            lines.append(f"- **詳細:** {risk.get('description', '')}")
            lines.append(f"- **顕在化しうる日程:** {risk.get('schedule', '要確認')}")
            src = risk.get("source_files", [])
            if src:
                lines.append(f"- **関連ファイル:** {', '.join(src)}")
            lines.append("")

    # ── 日程別早見表 ──────────────────────────────────────
    lines += ["---", "", "## 📅 顕在化しうる日程別リスク一覧", ""]
    lines.append("| 日程 | リスクタイトル | 深刻度 |")
    lines.append("|------|--------------|--------|")
    for risk in risks:
        sev = risk.get("severity", "不明")
        icon = SEVERITY_ICON.get(sev, "⚪")
        lines.append(f"| {risk.get('schedule', '要確認')} | {risk.get('title', '')} | {icon} {sev} |")

    lines += [
        "",
        "---",
        "",
        "*本レポートは Claude API (Anthropic) により自動生成されました。内容の最終確認は担当者が行ってください。*",
        "",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 4. APIリクエストカウンター
# ═══════════════════════════════════════════════════════════

COUNTER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".api_counter.json")
FREE_LIMIT_PER_DAY = 1000  # 目安（プランにより異なる）


def load_counter() -> dict:
    """カウンターファイルを読み込む。存在しない・日付が変わった場合はリセット。"""
    today = datetime.date.today().isoformat()
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("date") == today:
                return data
        except Exception:
            pass
    return {"date": today, "count": 0}


def save_counter(counter: dict) -> None:
    """カウンターをファイルに保存する。"""
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(counter, f, ensure_ascii=False)


def increment_counter() -> tuple[int, int]:
    """カウンターを1増やして保存し、(本日の使用回数, 残り回数) を返す。"""
    counter = load_counter()
    counter["count"] += 1
    save_counter(counter)
    used = counter["count"]
    remaining = max(0, FREE_LIMIT_PER_DAY - used)
    return used, remaining


# ═══════════════════════════════════════════════════════════
# 5. 要約内容によるファイル振り分け
# ═══════════════════════════════════════════════════════════

ROUTE_RULES = [
    {
        "keywords": ["タイ", "インドネシア", "ベトナム", "フィリピン", "シンガポール", "マレーシア", "ミャンマー", "アセアン", "Thai", "Indonesia", "Vietnam", "Philippines", "Singapore", "Malaysia", "Myanmar", "ASEAN"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\asean_oceania",
        "label": "ASEAN Oceania",
    },
    {
        "keywords": ["中国", "習近平", "China"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\china",
        "label": "China",
    },
    {
        "keywords": ["イギリス", "英国", "フランス", "ドイツ", "イタリア", "スペイン", "欧州", "トルコ", "ウクライナ", "ロシア", "UK", "France", "Germany", "Italy", "Spain", "EU", "Ukraine", "Russia", "Turkey"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\europe",
        "label": "Europe",
    },
    {
        "keywords": ["地政学", "地経学", "geopolitics", "半導体", "鉱物", "Semiconductors", "Minerals"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\geopolitics",
        "label": "Geopolitics",
    },
    {
        "keywords": ["インド", "サウジ", "イスラエル", "イラン", "ホルムズ", "シリア", "UAE", "カタール", "エジプト", "ケニア", "ナイジェリア", "OPEC", "India", "Saudi", "Israel", "Iran", "Hormuz", "Syria", "Qatar", "Eygpt", "Kenya", "Nigeria"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\india_mena",
        "label": "India MENA",
    },
    {
        "keywords": ["日本", "高市", "Japan", "Takaichi"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\japan",
        "label": "Japan",
    },
    {
        "keywords": ["鉱物", "ニッケル", "リチウム", "レアアース", "Minerals", "黒鉛", "レアミネラル", "Rare Minerals", "Nickel", "Lithium", "Rare Earths", "Graphite"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\minerals",
        "label": "Minerals",
    },
    {
        "keywords": ["米国", "トランプ", "カナダ", "メキシコ", "キューバ", "USA", "Trump", "Canada", "Mexico", "Cuba", "NAFTA", "USMCA"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\north america",
        "label": "North America",
    },
    {
        "keywords": ["ブラジル", "アルゼンチン", "ベネズエラ", "メルコスール", "Brazil", "Argentina", "Venezuela", "Mercosur"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\south america",
        "label": "South America",
    },
    {
        "keywords": ["台湾", "Taiwan"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\taiwan",
        "label": "Taiwan",
    },
    {
        "keywords": ["通商", "WTO", "関税", "FTA", "trade", "tariff", "人権", "human rights", "環境", "environment", "AI"],
        "dest": r"C:\Users\shondo\Desktop\agent_project\db\trade_tariff_ai",
        "label": "Trade Tariff AI",
    },
]


def keyword_match(text: str, keywords: list[str]) -> bool:
    """
    キーワードがテキストに含まれるか判定する。
    英数字のみのキーワードは単語境界でマッチさせ誤検知を防ぐ。
    """
    for kw in keywords:
        if re.match(r'^[A-Za-z0-9]+$', kw):
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text):
                return True
        else:
            if kw in text:
                return True
    return False


def route_files(raw_text: str, source_files: list[str], report_path: str) -> None:
    """
    原文テキストにキーワードが含まれる場合、対象フォルダーへファイルとレポートをコピーし、
    全コピー完了後に元ファイルを削除する。
    キーワードが合致しなかった場合は others フォルダーへコピーする。
    """
    matched_rules = [
        rule for rule in ROUTE_RULES
        if keyword_match(raw_text, rule["keywords"])
    ]

    if not matched_rules:
        others_dir = r"C:\Users\shondo\Desktop\agent_project\db\others"
        others_report_dir = os.path.join(others_dir, "report")
        os.makedirs(others_dir, exist_ok=True)
        os.makedirs(others_report_dir, exist_ok=True)
        for src in source_files:
            if not os.path.isfile(src):
                print(f"  ⚠️  振り分けスキップ（ファイルが見つかりません）: {src}")
                continue
            dest_path = os.path.join(others_dir, os.path.basename(src))
            shutil.copy2(src, dest_path)
            print(f"  📁 [Others] コピー: {src} → {dest_path}")
        if os.path.isfile(report_path):
            dest_report = os.path.join(others_report_dir, os.path.basename(report_path))
            shutil.copy2(report_path, dest_report)
            print(f"  📄 [Others] レポートをコピー: {report_path} → {dest_report}")
        for src in source_files:
            if os.path.isfile(src):
                os.remove(src)
                print(f"  🗑️  元ファイルを削除しました: {src}")
        return

    # ── Step1: 全コピーを先に完了させる ──────────────────
    for rule in matched_rules:
        dest_dir = rule["dest"]
        dest_report_dir = os.path.join(dest_dir, "report")
        os.makedirs(dest_dir, exist_ok=True)
        os.makedirs(dest_report_dir, exist_ok=True)
        for src in source_files:
            if not os.path.isfile(src):
                print(f"  ⚠️  振り分けスキップ（ファイルが見つかりません）: {src}")
                continue
            dest_path = os.path.join(dest_dir, os.path.basename(src))
            shutil.copy2(src, dest_path)
            print(f"  📁 [{rule['label']}] コピー: {src} → {dest_path}")
        if os.path.isfile(report_path):
            dest_report = os.path.join(dest_report_dir, os.path.basename(report_path))
            shutil.copy2(report_path, dest_report)
            print(f"  📄 [{rule['label']}] レポートをコピー: {report_path} → {dest_report}")

    # ── Step2: 全コピー完了後に元ファイルを削除 ──────────
    for src in source_files:
        if os.path.isfile(src):
            os.remove(src)
            print(f"  🗑️  元ファイルを削除しました: {src}")


# ═══════════════════════════════════════════════════════════
# 6. メイン
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Claude APIでフォルダー内の全ファイルをまとめてリスク分析します")
    parser.add_argument("--folder", required=True, help="分析対象フォルダーのパス")
    parser.add_argument("--output", default="", help="出力Markdownファイルのパス（省略時は自動命名）")
    parser.add_argument("--api-key", default="", help="Anthropic APIキー（省略時は環境変数 ANTHROPIC_API_KEY を使用）")
    args = parser.parse_args()

    # API キー設定（環境変数を優先。ハードコードは行わない）
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit(
            "❌ APIキーが見つかりません。\n"
            "   https://console.anthropic.com でキーを取得し、\n"
            "   --api-key オプションか環境変数 ANTHROPIC_API_KEY を設定してください。"
        )

    # Claude クライアント初期化
    client = anthropic.Anthropic(api_key=api_key)

    # ファイル収集
    files = collect_files(args.folder)
    if not files:
        sys.exit(f"❌ 対象ファイルが見つかりませんでした: {args.folder}")

    print(f"📂 {len(files)} 件のファイルを検出しました。1件ずつ分析します...\n")

    total_used = 0

    # ── ファイルごとにAPI呼び出し・レポート生成・振り分けを実行 ──
    for path in files:
        filename = os.path.relpath(path, args.folder)
        print(f"{'='*60}")
        print(f"📄 処理中: {filename}")

        # テキスト抽出
        text = extract_text(path)
        if not text.strip():
            print(f"  ⚠️  スキップ: テキストを抽出できませんでした。")
            continue
        fc = {"filename": filename, "text": text}
        print(f"  ✅ テキスト抽出完了")

        # Claude API で分析
        print(f"  🤖 Claude API で分析中...")
        try:
            data = analyze_one_with_claude(fc, client)
            print(f"  ✅ 分析完了 — リスク {len(data.get('risks', []))} 件を検出")
        except Exception as e:
            print(f"  ❌ API呼び出しエラー: {e} — スキップします")
            continue

        # カウンター更新
        used, remaining = increment_counter()
        total_used += 1
        print(f"  📊 本日のAPIリクエスト使用数: {used} 回（残り目安: {remaining:,} / {FREE_LIMIT_PER_DAY:,}）")

        # レポートをいったん一時ファイルとして保存
        stem = os.path.splitext(os.path.basename(path))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{stem}_{timestamp}.md"
        tmp_report_path = os.path.join(args.folder, report_filename)
        report_md = build_report(data, fc, args.folder)
        with open(tmp_report_path, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"  📝 レポート一時保存: {report_filename}")

        # 振り分け（原文テキストでキーワード判定）・レポートも同じ振り分け先へ保存
        absolute_file = [os.path.abspath(path)]
        route_files(text, absolute_file, os.path.abspath(tmp_report_path))

        # 振り分け完了後、filesフォルダーの一時レポートを削除
        if os.path.isfile(tmp_report_path):
            os.remove(tmp_report_path)
            print(f"  🗑️  一時レポートを削除しました: {report_filename}")

    print(f"\n{'='*60}")
    print(f"✅ 全処理完了。合計 {total_used} 回のAPIリクエストを使用しました。")


if __name__ == "__main__":
    main()
