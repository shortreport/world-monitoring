"""
query_claude.py
===============
フォルダー内の全ファイルを読み込み、ユーザーが入力した質問・テーマに対して
Claude API が関連情報を抜き出して回答するインタラクティブツール。

質問内容から検索先フォルダーを自動判定します:
  - 米国・北米に関する質問 → db/north america
  - 中国に関する質問       → db/china
  - 欧州・EUに関する質問   → db/europe
  - 不明・その他           → db/（ルート）

【使い方】
  # 1回だけ質問する
  python query_claude.py --query "米国の金利動向は"

  # 対話モード（質問を繰り返せる）
  python query_claude.py

  # 結果をファイルに保存
  python query_claude.py --query "支払い条件" --output ./result.md
"""

import argparse
import datetime
import os
import sys

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

SUPPORTED      = {".docx", ".pdf", ".txt", ".md"}
CHARS_PER_FILE = 4000
CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"


def extract_text(path: str) -> str:
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
    result = []
    for root, _, files in os.walk(folder):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() in SUPPORTED:
                result.append(os.path.join(root, name))
    return result


def build_files_block(file_contents: list[dict]) -> str:
    blocks = []
    for fc in file_contents:
        text = fc["text"][:CHARS_PER_FILE]
        if len(fc["text"]) > CHARS_PER_FILE:
            text += "\n[以下省略]"
        blocks.append(f"=== ファイル: {fc['filename']} ===\n{text}")
    return "\n\n".join(blocks)


# ═══════════════════════════════════════════════════════════
# 2. 質問内容からフォルダーを自動選択
# ═══════════════════════════════════════════════════════════

DB_ROOT     = r"C:\Users\shondo\Desktop\agent_project\db"
DB_NORTH_AM = r"C:\Users\shondo\Desktop\agent_project\db\north america"
DB_CHINA    = r"C:\Users\shondo\Desktop\agent_project\db\china"
DB_EUROPE   = r"C:\Users\shondo\Desktop\agent_project\db\europe"

KEYWORDS_NA     = ["米国", "アメリカ", "USA", "US", "北米", "ニューヨーク", "ワシントン", "FRB", "Fed"]
KEYWORDS_CHINA  = ["中国", "チャイナ", "China", "北京", "上海", "香港", "人民元", "中銀"]
KEYWORDS_EUROPE = ["欧州", "ヨーロッパ", "Europe", "EU", "ECB", "ユーロ", "ドイツ", "フランス",
                   "イギリス", "英国", "イタリア", "スペイン", "ブリュッセル", "欧州連合",
                   "ユーロ圏", "産業加速法", "European"]

REGION_PROMPT = """以下の質問が「米国・北米」「中国」「欧州・EU」のいずれかに関するものか、
それとも「その他・不明」かを判定してください。

【質問】
{query}

以下の4つのうち1つだけを返してください（他の文字は一切出力しないこと）:
north_america
china
europe
unknown"""


def detect_region(query: str, client: anthropic.Anthropic) -> str:
    """質問テキストから検索対象地域を返す: 'north_america' / 'china' / 'europe' / 'unknown'"""
    for kw in KEYWORDS_NA:
        if kw in query:
            return "north_america"
    for kw in KEYWORDS_CHINA:
        if kw in query:
            return "china"
    for kw in KEYWORDS_EUROPE:
        if kw in query:
            return "europe"
    # キーワードで判定できない場合は Claude に問い合わせ
    prompt = REGION_PROMPT.format(query=query)
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip().lower()
    if "north_america" in raw:
        return "north_america"
    if "china" in raw:
        return "china"
    if "europe" in raw:
        return "europe"
    return "unknown"


def resolve_folder(query: str, client: anthropic.Anthropic) -> tuple[str, str]:
    region = detect_region(query, client)
    candidates = {
        "north_america": (DB_NORTH_AM, "North America"),
        "china":         (DB_CHINA,    "China"),
        "europe":        (DB_EUROPE,   "Europe"),
        "unknown":       (DB_ROOT,     "全DB"),
    }
    folder, label = candidates[region]
    if not os.path.isdir(folder):
        print(f"  ⚠️  [{label}] フォルダーが見つかりません。DB ルートを使用します: {DB_ROOT}")
        folder, label = DB_ROOT, "全DB（フォールバック）"
    return folder, label


def load_folder(query_text: str, client: anthropic.Anthropic) -> tuple[list[dict], str]:
    folder, label = resolve_folder(query_text, client)
    print(f"  🗂️  検索先: [{label}] {folder}")
    files = collect_files(folder)
    if not files:
        print(f"  ⚠️  ファイルが見つかりません: {folder}")
        return [], folder
    file_contents = []
    for path in files:
        filename = os.path.relpath(path, folder)
        text = extract_text(path)
        if not text.strip():
            print(f"  ⚠️  スキップ: {filename}")
            continue
        file_contents.append({"filename": filename, "text": text})
        print(f"  ✅ {filename}")
    return file_contents, folder


# ═══════════════════════════════════════════════════════════
# 3. Claude API で質問に回答
# ═══════════════════════════════════════════════════════════

QUERY_PROMPT = """あなたは文書検索アシスタントです。
以下の複数のファイルの内容をすべて読んだうえで、ユーザーの質問に答えてください。

{files_block}

---

【ユーザーの質問】
{query}

---

【回答フォーマットのルール】
1. 回答は必ず箇条書き（「・」）で要点ごとに1行にまとめること
2. 各箇条書きの末尾に、情報の出典ファイルを *1 *2 のような注釈番号で示すこと
   例:  ・契約期間は2026年4月1日〜2027年3月31日です *1
3. 回答の最後に空行を入れ、「【情報ソース】」という見出しのあとに
   注釈番号とファイル名の対応を列挙すること
   例:
   【情報ソース】
   *1 contract.pdf
   *2 schedule.docx
4. 複数のファイルに同じ情報がある場合は *1 *2 のように両方示すこと
5. 該当する情報がない場合は「・該当する情報が見つかりませんでした」とだけ回答すること
6. 情報を捏造しないこと
7. 回答はすべて日本語で書くこと
8. 文末は必ず「です」「ます」調で統一すること"""


def ask_claude(query: str, file_contents: list[dict], client: anthropic.Anthropic) -> str:
    files_block = build_files_block(file_contents)
    prompt = QUERY_PROMPT.format(files_block=files_block, query=query)
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


# ═══════════════════════════════════════════════════════════
# 4. 結果をMarkdownに保存
# ═══════════════════════════════════════════════════════════

def save_result(query: str, answer: str, output_path: str, folder: str):
    now = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
    if "【情報ソース】" in answer:
        body, sources = answer.split("【情報ソース】", 1)
        sources_block = "## 📎 情報ソース\n\n" + sources.strip()
    else:
        body = answer
        sources_block = ""

    content = "\n".join([
        "# 📄 ドキュメント検索結果",
        "",
        f"- **検索先フォルダー:** `{folder}`",
        f"- **作成日時:** {now}",
        "",
        "---",
        "",
        "## 🔍 質問",
        "",
        f"> {query}",
        "",
        "## 💬 回答",
        "",
        body.strip(),
        "",
        *(["---", "", sources_block, ""] if sources_block else []),
        "---",
        "",
        "*本レポートは Claude API (Anthropic) により自動生成されました。*",
    ])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n💾 結果を保存しました: {output_path}")


# ═══════════════════════════════════════════════════════════
# 5. メイン
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="質問内容から検索先DBフォルダーを自動判定して回答するツール（Claude版）"
    )
    parser.add_argument("--query",   default="", help="質問内容（省略時は対話モード）")
    parser.add_argument("--output",  default="", help="結果を保存するMarkdownファイルのパス")
    parser.add_argument("--api-key", default="", help="Anthropic APIキー（省略時はスクリプト内のキーを使用）")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "") or CLAUDE_API_KEY
    client = anthropic.Anthropic(api_key=api_key)

    # ── 1回質問モード ──────────────────────────────────────
    if args.query:
        print(f"🔍 質問: {args.query}\n")
        file_contents, folder = load_folder(args.query, client)
        if not file_contents:
            sys.exit("❌ テキストを抽出できたファイルがありません。")
        answer = ask_claude(args.query, file_contents, client)
        print("💬 回答:\n")
        print(answer)
        if args.output:
            save_result(args.query, answer, args.output, folder)
        return

    # ── 対話モード ─────────────────────────────────────────
    print("=" * 50)
    print("  対話モード — 質問を入力してください")
    print("  終了するには「exit」または「quit」と入力")
    print("=" * 50)

    session_log = []

    while True:
        print()
        try:
            query = input("❓ 質問 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 終了します。")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit", "終了"):
            print("👋 終了します。")
            break

        print("\n🤖 検索先を判定中...\n")
        try:
            file_contents, folder = load_folder(query, client)
            if not file_contents:
                print("⚠️  該当ファイルがありませんでした。")
                continue
            answer = ask_claude(query, file_contents, client)
            print("💬 回答:\n")
            print(answer)
            session_log.append({"query": query, "answer": answer, "folder": folder})
        except Exception as e:
            print(f"❌ エラー: {e}")

    # 対話終了後、--output 指定があれば全ログを保存
    if args.output and session_log:
        now = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
        lines = [
            "# 📄 ドキュメント検索ログ",
            "",
            f"- **作成日時:** {now}",
            f"- **質問数:** {len(session_log)} 件",
            "",
            "---",
            "",
        ]
        for i, entry in enumerate(session_log, 1):
            ans = entry["answer"]
            if "【情報ソース】" in ans:
                body, sources = ans.split("【情報ソース】", 1)
                ans_block = body.strip() + "\n\n**情報ソース:**\n" + sources.strip()
            else:
                ans_block = ans
            lines += [
                f"## Q{i}. {entry['query']}",
                f"*(検索先: {entry['folder']})*",
                "",
                ans_block,
                "",
                "---",
                "",
            ]
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\n💾 ログを保存しました: {args.output}")


if __name__ == "__main__":
    main()
