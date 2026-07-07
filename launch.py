import subprocess
import time
import os

brave_paths = [
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    os.path.join(os.environ.get("LOCALAPPDATA",""), r"BraveSoftware\Brave-Browser\Application\brave.exe"),
]
brave = next((p for p in brave_paths if os.path.exists(p)), None)

base = os.path.dirname(os.path.abspath(__file__))
python = os.path.join(base, r"venv\Scripts\python.exe")

# 1) World Monitor 公式サイトを新しいウィンドウで開く
if brave:
    subprocess.Popen([brave, "--new-window", "https://www.worldmonitor.app/"])
else:
    import webbrowser
    webbrowser.open("https://www.worldmonitor.app/")

# 2) ダッシュボードサーバー (port 5001) を起動
subprocess.Popen(
    [python, "dashboard_app.py"],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    cwd=base,
)

# 3) World News サーバー (port 5002) を起動
subprocess.Popen(
    [python, "news_app.py"],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
    cwd=base,
)

# サーバー起動を待つ
time.sleep(4)

# 4) ダッシュボードを新しいウィンドウで開く
if brave:
    subprocess.Popen([brave, "--new-window", "http://localhost:5001"])
else:
    import webbrowser
    webbrowser.open("http://localhost:5001")

# 5) World News タブを同じウィンドウに追加
time.sleep(1)
if brave:
    subprocess.Popen([brave, "--new-tab", "http://localhost:5002"])
else:
    import webbrowser
    webbrowser.open("http://localhost:5002")
