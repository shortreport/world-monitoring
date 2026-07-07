"""
手動更新スクリプト: python update_now.py [モード]

モード:
  (引数なし)  → 時刻で自動判定
  news        → ニュースのみ更新
  full        → ニュース + Economist（Outlook必要）
  briefing    → ブリーフィングPDF生成のみ
  trump       → Trumpデータ収集のみ
  all         → trump → full → briefing の順で全更新

使い方:
  python update_now.py          # 朝6-9時なら full、それ以外は news
  python update_now.py full     # Economist含む全更新
  python update_now.py all      # 全タスクを順番に実行
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

BASE    = Path(__file__).parent
PYTHON  = BASE / "venv" / "Scripts" / "python.exe"
SCRIPTS = BASE / "scripts"

os.environ["PYTHONUTF8"] = "1"


def run(cmd, label):
    print(f"\n{'='*50}")
    print(f"[{label}] 開始: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, cwd=str(BASE))
    code = result.returncode
    status = "完了" if code == 0 else f"失敗 (exit={code})"
    print(f"\n[{label}] {status}: {datetime.now().strftime('%H:%M:%S')}")
    return code


def do_news():
    return run([str(PYTHON), "update_home.py"], "ニュース更新")

def do_full():
    return run([str(PYTHON), "update_home.py", "--with-economist"], "ニュース+Economist更新")

def do_briefing():
    return run(["cmd", "/c", str(SCRIPTS / "update_briefing.bat")], "ブリーフィング生成")

def do_trump():
    return run([str(PYTHON), "trump_monitor.py"], "Trump収集")


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "auto"

    if mode == "auto":
        hour = datetime.now().hour
        if 5 <= hour < 10:
            print("→ 時刻判定: 朝の時間帯 → full モード（ニュース + Economist）")
            mode = "full"
        else:
            print(f"→ 時刻判定: {hour}時 → news モード（ニュースのみ）")
            mode = "news"

    if mode == "news":
        do_news()
    elif mode == "full":
        do_full()
    elif mode == "briefing":
        do_briefing()
    elif mode == "trump":
        do_trump()
    elif mode == "all":
        do_trump()
        do_full()
        do_briefing()
    else:
        print(f"不明なモード: {mode}")
        print("使用可能: news / full / briefing / trump / all")
        sys.exit(1)


if __name__ == "__main__":
    main()
