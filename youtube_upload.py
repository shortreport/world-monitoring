"""
YouTube アップロードスクリプト
  - news program/ フォルダーの最新 MP4 を YouTube にアップロード
  - 初回は OAuth2 ブラウザ認証 → token.json に保存（以降は自動更新）
  - 使用法: python youtube_upload.py [--file <path>] [--title "タイトル"] [--private]

事前準備:
  1. Google Cloud Console で "YouTube Data API v3" を有効化
  2. OAuth 2.0 クライアント ID を作成（種類: デスクトップ アプリ）
  3. client_secrets.json をこのスクリプトと同じフォルダーに配置
  4. pip install google-api-python-client google-auth-oauthlib
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

VIDEO_DIR = Path(__file__).parent / "news program"
SECRETS   = Path(__file__).parent / "client_secrets.json"
TOKEN     = Path(__file__).parent / "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CATEGORY_NEWS = "25"   # YouTube カテゴリID: News & Politics


# ── 認証 ─────────────────────────────────────────────────────────────────────
def get_credentials():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not SECRETS.exists():
                print(f"ERROR: {SECRETS} が見つかりません。")
                print("Google Cloud Console から OAuth クライアント ID をダウンロードし、")
                print(f"  {SECRETS}")
                print("として配置してください。")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN.write_text(creds.to_json(), encoding="utf-8")
        print(f"認証情報を保存しました: {TOKEN}")

    return creds


# ── 最新 MP4 を検索 ───────────────────────────────────────────────────────────
def find_latest_mp4() -> Path | None:
    mp4s = sorted(VIDEO_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    return mp4s[0] if mp4s else None


# ── アップロード ──────────────────────────────────────────────────────────────
def upload(video_path: Path, title: str, description: str, privacy: str):
    import googleapiclient.discovery
    import googleapiclient.http

    creds = get_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": CATEGORY_NEWS,
            "defaultLanguage": "ja",
        },
        "status": {
            "privacyStatus": privacy,      # "public" | "unlisted" | "private"
            "selfDeclaredMadeForKids": False,
        },
    }

    media = googleapiclient.http.MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024 * 8,   # 8 MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    print(f"アップロード開始: {video_path.name}")
    print(f"  タイトル   : {title}")
    print(f"  公開設定   : {privacy}")
    print(f"  ファイルサイズ: {video_path.stat().st_size / 1024 / 1024:.1f} MB")
    print()

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r  [{bar}] {pct}%", end="", flush=True)

    print(f"\n\nアップロード完了！")
    video_id = response.get("id", "")
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"  動画 ID  : {video_id}")
    print(f"  URL      : {url}")
    return url


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    today = datetime.now()
    default_title = f"World News ニュース番組 {today.strftime('%Y年%m月%d日')}"
    default_desc = (
        f"World News 自動生成ニュース番組\n"
        f"収録日: {today.strftime('%Y-%m-%d')}\n\n"
        "※ このビデオはスクリプトにより自動生成されました。"
    )

    parser = argparse.ArgumentParser(description="YouTube へ MP4 をアップロード")
    parser.add_argument("--file",    default=None,          help="アップロードするMP4ファイルパス（省略時: 最新ファイル）")
    parser.add_argument("--title",   default=default_title, help="動画タイトル")
    parser.add_argument("--desc",    default=default_desc,  help="動画説明文")
    parser.add_argument("--private", action="store_true",   help="非公開でアップロード（省略時: 限定公開）")
    parser.add_argument("--public",  action="store_true",   help="公開でアップロード")
    args = parser.parse_args()

    # ファイル選択
    if args.file:
        video_path = Path(args.file)
        if not video_path.exists():
            print(f"ERROR: ファイルが見つかりません: {video_path}")
            sys.exit(1)
    else:
        video_path = find_latest_mp4()
        if video_path is None:
            print(f"ERROR: {VIDEO_DIR} に MP4 ファイルが見つかりません。")
            sys.exit(1)
        print(f"最新ファイルを選択: {video_path.name}")

    # 公開設定
    if args.public:
        privacy = "public"
    elif args.private:
        privacy = "private"
    else:
        privacy = "unlisted"   # デフォルト: 限定公開（URLを知っている人のみ）

    # 確認プロンプト
    print()
    print("=" * 50)
    print(f"  ファイル: {video_path}")
    print(f"  タイトル: {args.title}")
    print(f"  公開設定: {privacy}")
    print("=" * 50)
    ans = input("\nこの内容でアップロードしますか？ [y/N]: ").strip().lower()
    if ans != "y":
        print("キャンセルしました。")
        sys.exit(0)

    print()
    url = upload(video_path, args.title, args.desc, privacy)

    # URL をテキストファイルに保存
    url_file = Path(__file__).parent / "youtube_url.txt"
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with url_file.open("a", encoding="utf-8") as f:
        f.write(f"{today_str}\t{video_path.name}\t{url}\n")
    print(f"\nURL を保存しました: {url_file}")


if __name__ == "__main__":
    main()
