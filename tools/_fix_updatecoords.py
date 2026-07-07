"""updateCoords の関数宣言を修復"""
import os

base = os.path.dirname(__file__)
py_path = os.path.join(base, '_build.py')

with open(py_path, encoding='utf-8') as f:
    code = f.read()

# 壊れた状態: showStamp の閉じ } の直後に val-w, val-h の行が続いている
broken = """  tmpImg.src = src;
}
  document.getElementById('val-w').textContent = (parseFloat(stampEl.style.width)  / scale).toFixed(2);
  document.getElementById('val-h').textContent = (parseFloat(stampEl.style.height) / scale).toFixed(2);
}"""

fixed = """  tmpImg.src = src;
}

function updateCoords() {
  document.getElementById('val-x').textContent = (parseFloat(stampEl.style.left)   / scale).toFixed(2);
  document.getElementById('val-y').textContent = (parseFloat(stampEl.style.top)    / scale).toFixed(2);
  document.getElementById('val-w').textContent = (parseFloat(stampEl.style.width)  / scale).toFixed(2);
  document.getElementById('val-h').textContent = (parseFloat(stampEl.style.height) / scale).toFixed(2);
}"""

if broken in code:
    code = code.replace(broken, fixed)
    print("Fixed OK")
else:
    # val-x がどこかに残っているか確認
    idx = code.find("val-w').textContent")
    print(f"broken pattern not found. val-w at: {idx}")
    if idx > 0:
        print(repr(code[idx-100:idx+200]))

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(code)
