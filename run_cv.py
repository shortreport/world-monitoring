"""
CV生成ツール（コマンドライン実行用）
使い方:
  python run_cv.py "Franck Leroy" --nationality "フランス" --position "グラン・テスト州知事"
"""
import os, sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "web_app"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="人物名（現地語または日本語）")
    parser.add_argument("--nationality",   default="", help="国籍ヒント")
    parser.add_argument("--position",      default="", help="役職ヒント")
    parser.add_argument("--official-url",  default="", help="公式プロフィールページURL（写真取得に使用）")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY が設定されていません。")

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        print("[警告] GEMINI_API_KEY が未設定です。Google検索なしで実行します。")

    from tools.cv_generator import generate_cv_document
    official_url = args.official_url
    print(f"CV生成開始: {args.name} / 国籍={args.nationality or '自動'} / 役職={args.position or '自動'}")
    if official_url:
        print(f"公式URL指定: {official_url}")

    buf, filename = generate_cv_document(
        args.name, api_key,
        nationality_hint=args.nationality,
        position_hint=args.position,
        official_url=official_url,
    )

    out_dir = Path(__file__).parent / "cv"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / filename
    out_path.write_bytes(buf.getvalue())
    print(f"完了: {out_path}")

if __name__ == "__main__":
    main()
