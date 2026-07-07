"""スタンプ定義を実画像に差し替えるパッチスクリプト"""
import os, re

base = os.path.dirname(__file__)

# stamp0 の Base64 を読み込む
with open(os.path.join(base, '_stamp0_b64.txt'), encoding='utf-8') as f:
    b64_0 = f.read().strip()

src_0 = f'data:image/jpeg;base64,{b64_0}'

py_path = os.path.join(base, '_build.py')
with open(py_path, encoding='utf-8') as f:
    code = f.read()

# STAMPS 配列の定義を差し替え
# 旧: SVGベースの3スタンプ
# 新: stamp0 だけ実画像に差し替え

old_stamps = """const STAMPS = [
  { name: '社外秘',    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 110"><circle cx="50" cy="55" r="46" fill="none" stroke="#cc0000" stroke-width="5"/><text x="50" y="38" text-anchor="middle" font-family="serif" font-size="23" fill="#cc0000" font-weight="bold">社外</text><text x="50" y="72" text-anchor="middle" font-family="serif" font-size="28" fill="#cc0000" font-weight="bold">秘</text></svg>` },
  { name: '秘（黒丸）', svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#111" stroke-width="6"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="#111" font-weight="bold">秘</text></svg>` },
  { name: '秘（赤丸）', svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#cc0000"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="white" font-weight="bold">秘</text></svg>` }
];"""

new_stamps = f"""// スタンプのsrcプロパティ: SVGはsvgUrl()でdataURL化、実画像はそのまま使用
const STAMPS = [
  {{ name: '関係者外秘', src: '{src_0}' }},
  {{ name: '秘（黒丸）', src: svgUrl(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#111" stroke-width="6"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="#111" font-weight="bold">秘</text></svg>`) }},
  {{ name: '秘（赤丸）', src: svgUrl(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#cc0000"/><text x="50" y="62" text-anchor="middle" font-family="serif" font-size="44" fill="white" font-weight="bold">秘</text></svg>`) }}
];"""

if old_stamps in code:
    code = code.replace(old_stamps, new_stamps)
    print("STAMPS replaced OK")
else:
    print("ERROR: STAMPS block not found")
    exit(1)

# svgUrl() の呼び出しを src プロパティに対応させる
# 旧: svgUrl(s.svg) → 新: s.src（既にdataURLになっている）
code = code.replace("svgUrl(s.svg)", "s.src")
code = code.replace("svgUrl(STAMPS[i].svg)", "STAMPS[i].src")
code = code.replace("svgUrl(STAMPS[selectedIdx].svg)", "STAMPS[selectedIdx].src")
code = code.replace("svgUrl(STAMPS[s.stampIdx].svg)", "STAMPS[s.stampIdx].src")
code = code.replace("svgUrl(STAMPS[idx].svg)", "STAMPS[idx].src")

# svgToPngBase64 → imgToPngBase64 に変更（JPEG/PNG/SVGに対応）
old_fn = """function svgToPngBase64(svg, size) {
  return new Promise(resolve => {
    const canvas = document.createElement('canvas');
    canvas.width = size; canvas.height = size;
    const img = new Image();
    img.onload = () => { canvas.getContext('2d').drawImage(img, 0, 0, size, size); resolve(canvas.toDataURL('image/png')); };
    img.src = svgUrl(svg);
  });
}"""

new_fn = """function imgToPngBase64(src, size) {
  return new Promise(resolve => {
    const canvas = document.createElement('canvas');
    canvas.width = size; canvas.height = size;
    const img = new Image();
    img.onload = () => { canvas.getContext('2d').drawImage(img, 0, 0, size, size); resolve(canvas.toDataURL('image/png')); };
    img.src = src;
  });
}"""

code = code.replace(old_fn, new_fn)
code = code.replace("svgToPngBase64(STAMPS[idx].svg, 300)", "imgToPngBase64(STAMPS[idx].src, 300)")
code = code.replace("svgToPngBase64(STAMPS[stampIdx].svg, 300)", "imgToPngBase64(STAMPS[stampIdx].src, 300)")

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied successfully")
