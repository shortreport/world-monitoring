"""stamp0のBase64をBOMなしで差し替え"""
import os

base = os.path.dirname(__file__)

with open(os.path.join(base, '_stamp0_b64.txt'), encoding='ascii') as f:
    b64 = f.read().strip()

assert b64.startswith('/9j/'), f"BOM混入: {b64[:10]}"

py_path = os.path.join(base, '_build.py')
with open(py_path, encoding='utf-8') as f:
    code = f.read()

# 既存のstamp0のsrcを置換（BOM付きを正常なものに）
import re
pattern = r"(\{ name: '関係者外秘', src: 'data:image/jpeg;base64,)[^']+(' \})"
new_val = f"\\g<1>{b64}\\g<2>"
new_code, n = re.subn(pattern, new_val, code)

if n == 1:
    print("stamp0 fixed OK")
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
else:
    print(f"ERROR: {n} matches found")
