"""
Outlook の特定フォルダーの未読メールを PDF 化するスクリプト
  - 各メールを1 PDF（要点 + 原文）
  - Claude API で要点を日本語要約
  - 処理後に既読へ変更
出力先: C:\\Users\\shondo\\Desktop\\agent_project\\files
"""
import os
import re
import html
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Windows コンソールの文字化け防止
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import win32com.client
import pythoncom
import anthropic

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 設定 ─────────────────────────────────────────────────────────────────────
CLAUDE_API_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
DEFAULT_FOLDERS  = ["*Politico", "JETRO", "EG"]   # 引数なしで処理するフォルダー一覧
FILES_DIR        = Path(r"C:\Users\shondo\Desktop\agent_project\mail_files")
CLAUDE_MODEL     = "claude-haiku-4-5-20251001"   # 高速・低コスト


# ── フォント登録 ──────────────────────────────────────────────────────────────
def register_fonts():
    candidates = [
        (r"C:\Windows\Fonts\meiryo.ttc",   0, "JP"),
        (r"C:\Windows\Fonts\meiryo.ttc",   1, "JPB"),
        (r"C:\Windows\Fonts\YuGothR.ttc",  0, "JP"),
        (r"C:\Windows\Fonts\msgothic.ttc", 0, "JP"),
        (r"C:\Windows\Fonts\msgothic.ttc", 0, "JPB"),
    ]
    registered = set()
    for path, idx, name in candidates:
        if name in registered:
            continue
        if Path(path).exists():
            try:
                pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
                registered.add(name)
            except Exception:
                pass
    if "JP" not in registered:
        raise RuntimeError("日本語フォントを登録できませんでした。")
    if "JPB" not in registered:
        pdfmetrics.registerFont(TTFont("JPB", candidates[0][0], subfontIndex=0))


# ── HTML → プレーンテキスト変換 ──────────────────────────────────────────────
def strip_html(text: str) -> str:
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


# ── 自動車関連キーワード判定 ──────────────────────────────────────────────────
_TOYOTA_KW = [
    "toyota", "トヨタ", "自動車", "automotive", "auto sector",
    "electric vehicle", "ev tariff", "ev policy", "ev market",
    "automobile", "car tariff", "car industry", "car maker",
    "iaa", "industrial accelerator act",
    "porsche", "volkswagen", "vw ", "stellantis", "bmw",
    "nissan", "honda motor", "ford motor", "general motors",
    "自動車産業", "自動車メーカー", "自動車業界",
    "catl", "usmca",
]

def is_toyota_relevant(subject: str, body: str) -> bool:
    text = (subject + " " + body[:2000]).lower()
    return any(kw in text for kw in _TOYOTA_KW)


# ── Claude で要点要約 ─────────────────────────────────────────────────────────
def summarize(subject: str, body: str) -> str:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    prompt = (
        "以下のメールを読み、日本語で要点を3〜5箇条にまとめてください。\n"
        "各箇条は「・」で始め、簡潔に1〜2文でまとめてください。\n"
        "要点のみを出力し、前置きや見出しは不要です。\n\n"
        f"件名: {subject}\n\n"
        f"本文（先頭3000字）:\n{body[:3000]}"
    )
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


# ── PDF 生成 ──────────────────────────────────────────────────────────────────
def make_pdf(subject: str, sender: str, date_str: str,
             summary: str, body: str, out_path: Path):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    # スタイル定義
    s_title = ParagraphStyle(
        "title", fontName="JPB", fontSize=14, leading=22,
        spaceAfter=3, textColor=HexColor("#1a1a2e"),
    )
    s_meta = ParagraphStyle(
        "meta", fontName="JP", fontSize=9, leading=14,
        textColor=HexColor("#666688"),
    )
    s_sec = ParagraphStyle(
        "sec", fontName="JPB", fontSize=11, leading=18,
        spaceBefore=6, spaceAfter=3,
        textColor=HexColor("#003399"),
    )
    s_bullet = ParagraphStyle(
        "bullet", fontName="JP", fontSize=10, leading=18,
        leftIndent=8, spaceAfter=2,
    )
    s_body = ParagraphStyle(
        "body", fontName="JP", fontSize=9, leading=15,
        spaceAfter=1,
    )

    story = []

    # ── ヘッダー：件名・送信者・日時 ─────────────
    story.append(Paragraph(_esc(subject), s_title))
    story.append(Paragraph(
        f"送信者: {_esc(sender)}　　受信日時: {_esc(date_str)}", s_meta
    ))
    story.append(Spacer(1, 5 * mm))

    # ── 要点セクション（自動車関連のみ）────────────
    if summary:
        story.append(Paragraph("【要点】", s_sec))
        for line in summary.splitlines():
            line = line.strip()
            if line:
                story.append(Paragraph(_esc(line), s_bullet))
        story.append(Spacer(1, 5 * mm))
        story.append(HRFlowable(
            width="100%", thickness=0.8,
            color=HexColor("#aaaacc"), spaceAfter=4 * mm,
        ))

    # ── 原文セクション ────────────────────────────
    story.append(Paragraph("【メール原文】", s_sec))
    story.append(Spacer(1, 2 * mm))
    for line in body.splitlines():
        if line.strip():
            story.append(Paragraph(_esc(line), s_body))
        else:
            story.append(Spacer(1, 3 * mm))

    doc.build(story)


def _esc(text: str) -> str:
    """reportlab Paragraph 用の特殊文字エスケープ"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


# ── ファイル名サニタイズ ──────────────────────────────────────────────────────
def safe_fname(s: str, max_len: int = 50) -> str:
    s = re.sub(r'[\\/:*?"<>|\r\n\t]', '_', s)
    s = re.sub(r'\s+', '_', s.strip())
    return s[:max_len]


# ── Outlook フォルダー検索（再帰） ────────────────────────────────────────────
def find_folder(parent, name: str):
    for folder in parent.Folders:
        if folder.Name == name:
            return folder
        found = find_folder(folder, name)
        if found:
            return found
    return None


# ── メイン ────────────────────────────────────────────────────────────────────
def process_folder(ns, folder_name: str) -> int:
    """指定フォルダーの未読メールをPDF化し、処理件数を返す"""
    inbox = ns.GetDefaultFolder(6)  # 6 = Inbox
    target = find_folder(inbox, folder_name)
    if not target:
        for store in ns.Stores:
            try:
                root = store.GetRootFolder()
                target = find_folder(root, folder_name)
                if target:
                    break
            except Exception:
                pass

    if not target:
        print(f"ERROR: フォルダー '{folder_name}' が見つかりませんでした。")
        return 0

    print(f"\n{'='*50}")
    print(f"フォルダー '{target.Name}' を処理中...")

    items = target.Items
    items.Sort("[ReceivedTime]", True)
    unread_items = [m for m in items
                    if getattr(m, "UnRead", False) and getattr(m, "Class", 0) == 43]

    print(f"未読メール: {len(unread_items)} 件")
    if not unread_items:
        print("未読メールはありません。")
        return 0

    processed = []
    for i, mail in enumerate(unread_items, 1):
        subject  = getattr(mail, "Subject",    "") or "(件名なし)"
        sender   = getattr(mail, "SenderName", "") or ""
        recv     = getattr(mail, "ReceivedTime", None)
        date_str = str(recv)[:16] if recv else ""
        body_raw = getattr(mail, "Body", "") or ""
        body     = strip_html(body_raw)

        print(f"\n[{i}/{len(unread_items)}] {subject}")
        print(f"  送信者: {sender}  /  受信: {date_str}")

        if is_toyota_relevant(subject, body):
            print("  → 🚗 自動車関連 — Claude で要約中...")
            try:
                summary = summarize(subject, body)
            except Exception as e:
                print(f"  ⚠ 要約エラー: {e}")
                summary = ""
        else:
            print("  → スキップ（自動車無関連）")
            summary = ""

        date_tag = str(recv)[:16].replace(":", "").replace("-", "").replace(" ", "_") if recv else "00000000_0000"
        fname    = f"{date_tag}_{safe_fname(subject)}.pdf"
        out_path = FILES_DIR / fname

        print(f"  → PDF 生成: {fname}")
        try:
            make_pdf(subject, sender, date_str, summary, body, out_path)
            print(f"  → 保存完了: {out_path}")
            processed.append(mail)
        except Exception as e:
            print(f"  ⚠ PDF 生成エラー: {e}")

    print(f"\n{len(processed)} 件を既読に変更中...")
    for mail in processed:
        try:
            mail.UnRead = False
        except Exception as e:
            print(f"  ⚠ 既読変更エラー: {e}")

    return len(processed)


def connect_outlook():
    """
    Outlook COM オブジェクトを取得する。
    タスクスケジューラ等（画面ロック中）での実行を考慮し、
    まず GetActiveObject（既存インスタンスへの接続）を試み、
    失敗した場合のみ Dispatch（新規起動）にフォールバックする。
    """
    print("Outlook に接続中...")
    try:
        outlook = win32com.client.GetActiveObject("Outlook.Application")
        print("  [OK] 既存の Outlook インスタンスに接続しました。")
        return outlook
    except Exception as e_get:
        print(f"  [INFO] GetActiveObject 失敗: {e_get}")
        print("  [INFO] Dispatch で新規接続を試みます...")

    try:
        pythoncom.CoInitialize()
    except Exception:
        pass

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        import time
        time.sleep(3)  # 起動待機
        print("  [OK] Outlook を Dispatch で起動しました。")
        return outlook
    except Exception as e_disp:
        print(f"  [ERROR] Outlook の接続に失敗しました: {e_disp}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Outlook未読メールをPDF化")
    parser.add_argument("folders", nargs="*", default=DEFAULT_FOLDERS,
                        help=f"対象フォルダー名（省略時: {', '.join(DEFAULT_FOLDERS)}）")
    args = parser.parse_args()
    folder_names = args.folders

    FILES_DIR.mkdir(exist_ok=True)
    register_fonts()
    print("フォントを登録しました。")

    try:
        outlook = connect_outlook()
    except Exception as e:
        print(f"FATAL: Outlook に接続できませんでした: {e}")
        sys.exit(1)

    ns = outlook.GetNamespace("MAPI")

    total = 0
    for folder_name in folder_names:
        total += process_folder(ns, folder_name)

    print(f"\n{'='*50}")
    print(f"全フォルダー処理完了。")
    print(f"  総処理件数: {total} 件")
    print(f"  PDF 保存先: {FILES_DIR}")


if __name__ == "__main__":
    main()
