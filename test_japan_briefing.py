"""
test_japan_briefing.py
関心事項・注意点（japan_briefing）セクションの動作確認テスト。
Franck Leroyで実行し、docxに同セクションが出力されることを検証する。
"""
import sys, os, winreg, io
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

# ── APIキーをレジストリから取得 ─────────────────────────────────────────────
def _get_reg(name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
        val = winreg.QueryValueEx(key, name)[0]
        winreg.CloseKey(key)
        return val
    except Exception:
        return ""

# setdefault は既存（空）キーを上書きしないため、レジストリ値がある場合は強制上書き
for _var in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
    _v = _get_reg(_var)
    if _v:
        os.environ[_var] = _v

# ── パス設定 ─────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "web_app"))
from tools.cv_generator import generate_cv_document

# ── テスト実行 ────────────────────────────────────────────────────────────────
print("=== Franck Leroy 略歴書生成テスト ===")
print("（数分かかります）\n")

buf, filename = generate_cv_document(
    name="Franck Leroy",
    api_key=os.environ["ANTHROPIC_API_KEY"],
    nationality_hint="フランス共和国",
    position_hint="グラン・テスト地域圏議長",
)

out_path = Path(__file__).parent / filename
out_path.write_bytes(buf.read())
print(f"\n[OK] 生成完了: {filename}")
print(f"   保存先: {out_path}")

# ── docx から japan_briefing の内容を確認 ─────────────────────────────────
from docx import Document
doc = Document(str(out_path))
in_section = False
items = []
for para in doc.paragraphs:
    text = para.text.strip()
    if "関　心　事　項　・　注　意　点" in text:
        in_section = True
        print("\n--- 関心事項・注意点 セクション ---")
        continue
    if in_section:
        if text.startswith("◆"):
            items.append(text)
            print(" ", text)
        elif text and not text.startswith("◆") and len(text) > 5:
            # 別セクション開始
            break

if items:
    print(f"\n[OK] {len(items)}件の項目が出力されました。")
else:
    print("\n[NG] 関心事項・注意点セクションに項目が見つかりませんでした。")
    print("   docxファイルを直接開いて確認してください。")
