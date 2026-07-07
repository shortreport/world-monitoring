"""スタンプ2・3を実画像に差し替え"""
import os, re

base = os.path.dirname(__file__)

with open(os.path.join(base, '_stamp1_b64.txt'), encoding='utf-8') as f:
    b64_1 = f.read().strip()
with open(os.path.join(base, '_stamp2_b64.txt'), encoding='utf-8') as f:
    b64_2 = f.read().strip()

py_path = os.path.join(base, '_build.py')
with open(py_path, encoding='utf-8') as f:
    code = f.read()

# stamp1（秘・黒丸）のSVGを実画像に差し替え
old1 = """  { name: '秘（黒丸）', src: svgUrl(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#111" stroke-width="6"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="#111" font-weight="bold">秘</text></svg>`) },"""
new1 = f"""  {{ name: '秘', src: 'data:image/jpeg;base64,{b64_1}' }},"""

# stamp2（秘・赤丸）のSVGを実画像に差し替え
old2 = """  { name: '秘（赤丸）', src: svgUrl(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#cc0000"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="white" font-weight="bold">秘</text></svg>`) }"""
new2 = f"""  {{ name: '極秘', src: 'data:image/jpeg;base64,{b64_2}' }}"""

if old1 in code:
    code = code.replace(old1, new1)
    print("stamp1 replaced OK")
else:
    print("ERROR: stamp1 not found")

if old2 in code:
    code = code.replace(old2, new2)
    print("stamp2 replaced OK")
else:
    print("ERROR: stamp2 not found")

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(code)
