"""縦横比修正を文字列置換で正しく適用"""
import os, re

base = os.path.dirname(__file__)
py_path = os.path.join(base, '_build.py')

with open(py_path, encoding='utf-8') as f:
    code = f.read()

# --- imgToPngBase64 を修正 ---
old_fn = '''function imgToPngBase64(src, size) {
  return new Promise(resolve => {
    const canvas = document.createElement('canvas');
    canvas.width = size; canvas.height = size;
    const img = new Image();
    img.onload = () => { canvas.getContext('2d').drawImage(img, 0, 0, size, size); resolve(canvas.toDataURL('image/png')); };
    img.src = src;
  });
}'''

new_fn = '''function imgToPngBase64(src) {
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
      canvas.getContext('2d').drawImage(img, 0, 0);
      resolve(canvas.toDataURL('image/png'));
    };
    img.src = src;
  });
}'''

if old_fn in code:
    code = code.replace(old_fn, new_fn)
    print("imgToPngBase64: OK")
else:
    # すでに修正済みかチェック
    if 'function imgToPngBase64(src)' in code:
        print("imgToPngBase64: already fixed")
    else:
        print("imgToPngBase64: NOT FOUND - checking...")
        idx = code.find('function imgToPngBase64')
        print(code[idx:idx+200] if idx >= 0 else "not found at all")

# --- showStamp を修正 ---
old_show = '''function showStamp() {
  confirmed = false;
  stampEl.classList.remove('confirmed');
  document.getElementById('btn-confirm').disabled = false;
  document.getElementById('btn-edit').disabled    = true;
  document.getElementById('btn-save').disabled    = true;
  document.getElementById('stamp-img').src = STAMPS[selectedIdx].src;

  const main    = document.getElementById('main');
  const docWrap = document.getElementById('doc-wrap');
  const mainR   = main.getBoundingClientRect();
  const wrapR   = docWrap.getBoundingClientRect();
  const startX  = Math.max(0, (mainR.left + 20) - wrapR.left) + scale * 0.8;
  const startY  = Math.max(0, (mainR.top  + 20) - wrapR.top)  + scale * 0.8;
  const size    = 3.0 * scale;

  stampEl.style.left   = startX + 'px';
  stampEl.style.top    = startY + 'px';
  stampEl.style.width  = size + 'px';
  stampEl.style.height = size + 'px';
  stampEl.style.display = 'block';
  updateCoords();
}'''

new_show = '''function showStamp() {
  confirmed = false;
  stampEl.classList.remove('confirmed');
  document.getElementById('btn-confirm').disabled = false;
  document.getElementById('btn-edit').disabled    = true;
  document.getElementById('btn-save').disabled    = true;
  const src = STAMPS[selectedIdx].src;
  const tmpImg = new Image();
  tmpImg.onload = () => {
    const aspect = tmpImg.naturalHeight / tmpImg.naturalWidth;
    const main  = document.getElementById('main');
    const wrapR = document.getElementById('doc-wrap').getBoundingClientRect();
    const mainR = main.getBoundingClientRect();
    const startX = Math.max(0, (mainR.left + 20) - wrapR.left) + scale * 0.8;
    const startY = Math.max(0, (mainR.top  + 20) - wrapR.top)  + scale * 0.8;
    const w = 4.0 * scale;
    const h = w * aspect;
    document.getElementById('stamp-img').src = src;
    stampEl.style.left   = startX + 'px';
    stampEl.style.top    = startY + 'px';
    stampEl.style.width  = w + 'px';
    stampEl.style.height = h + 'px';
    stampEl.style.display = 'block';
    updateCoords();
  };
  tmpImg.src = src;
}'''

if old_show in code:
    code = code.replace(old_show, new_show)
    print("showStamp: OK")
else:
    if 'tmpImg.onload' in code:
        print("showStamp: already fixed")
    else:
        print("showStamp: NOT FOUND")
        idx = code.find('function showStamp')
        print(code[idx:idx+400] if idx >= 0 else "not found")

# --- imgToPngBase64 呼び出しの引数修正 ---
code = re.sub(r'imgToPngBase64\(([^,)]+),\s*300\)', r'imgToPngBase64(\1)', code)

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved.")
