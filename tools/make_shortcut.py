"""
stamp_tool.html のショートカットをカスタムアイコン付きで作成する
実行: python tools/make_shortcut.py
"""
import os
from PIL import Image
import win32com.client

base     = os.path.dirname(os.path.abspath(__file__))
html     = os.path.join(base, 'stamp_tool.html')
ico_path = os.path.join(base, 'stamp_icon.ico')
lnk_path = os.path.join(base, 'スタンプ貼り付けツール.lnk')

# --- ICOファイルを作成 ---
img = Image.open(r"C:\Users\shondo\Desktop\trial\1_極秘R.jpg").convert('RGBA')
# 正方形にリサイズ（中央クロップ）
w, h = img.size
side = min(w, h)
img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
img.save(ico_path, format='ICO', sizes=[(256,256),(64,64),(32,32),(16,16)])
print(f"ICO: {ico_path}")

# --- ショートカット作成 ---
shell = win32com.client.Dispatch("WScript.Shell")
sc = shell.CreateShortCut(lnk_path)
sc.TargetPath    = html
sc.IconLocation  = ico_path
sc.Description   = 'スタンプ貼り付けツール'
sc.Save()
print(f"Shortcut: {lnk_path}")
print("完了！ 'スタンプ貼り付けツール.lnk' を配布してください。")
