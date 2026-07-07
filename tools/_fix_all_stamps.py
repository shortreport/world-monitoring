"""3枚のスタンプを正しく設定し直す"""
import os, re, base64

base = os.path.dirname(__file__)

def load_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

b64_0 = load_b64(r"C:\Users\shondo\Desktop\trial\2_関係者外秘R.jpg")
b64_1 = load_b64(r"C:\Users\shondo\Desktop\trial\1_秘R.jpg")
b64_2 = load_b64(r"C:\Users\shondo\Desktop\trial\1_極秘R.jpg")

print(f"stamp0: {b64_0[:10]}... ({len(b64_0)} chars)")
print(f"stamp1: {b64_1[:10]}... ({len(b64_1)} chars)")
print(f"stamp2: {b64_2[:10]}... ({len(b64_2)} chars)")

new_stamps = f"""// スタンプのsrcプロパティ: 実画像をBase64で埋め込み
const STAMPS = [
  {{ name: '関係者外秘', src: 'data:image/jpeg;base64,{b64_0}' }},
  {{ name: '秘',       src: 'data:image/jpeg;base64,{b64_1}' }},
  {{ name: '極秘',     src: 'data:image/jpeg;base64,{b64_2}' }}
];"""

py_path = os.path.join(base, '_build.py')
with open(py_path, encoding='utf-8') as f:
    code = f.read()

# STAMPS ブロック全体を正規表現で置換
pattern = r'// スタンプのsrcプロパティ.*?const STAMPS = \[.*?\];'
new_code, n = re.subn(pattern, new_stamps, code, flags=re.DOTALL)

if n == 1:
    print("STAMPS block replaced OK")
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
else:
    print(f"ERROR: {n} matches. Trying fallback...")
    # fallback: const STAMPS = [ から ]; まで
    pattern2 = r'const STAMPS = \[.*?\];'
    new_code2, n2 = re.subn(pattern2, new_stamps, code, flags=re.DOTALL)
    if n2 == 1:
        print("Fallback OK")
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(new_code2)
    else:
        print(f"Fallback also failed: {n2} matches")
