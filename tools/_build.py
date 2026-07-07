"""stamp_tool.html build script"""
import os, base64

base = os.path.dirname(__file__)

with open(os.path.join(base, '_lib_jszip.js'), encoding='utf-8') as f:
    jszip = f.read()
with open(os.path.join(base, '_lib_docxpreview.js'), encoding='utf-8') as f:
    docxpreview = f.read()

def img_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

s0 = img_b64(r"C:\Users\shondo\Desktop\trial\2_関係者外秘R.jpg")
s1 = img_b64(r"C:\Users\shondo\Desktop\trial\1_秘R.jpg")
s2 = img_b64(r"C:\Users\shondo\Desktop\trial\1_極秘R.jpg")
print(f"stamps: {len(s0)}, {len(s1)}, {len(s2)}")

STAMPS_JS = (
    "const STAMPS = [\n"
    "  { name: '関係者外秘', src: 'data:image/jpeg;base64," + s0 + "' },\n"
    "  { name: '秘',       src: 'data:image/jpeg;base64," + s1 + "' },\n"
    "  { name: '極秘',     src: 'data:image/jpeg;base64," + s2 + "' }\n"
    "];"
)

# HTMLテンプレートを読み込む
with open(os.path.join(base, '_template.html'), encoding='utf-8') as f:
    html = f.read()

html = html.replace('%%JSZIP%%',      '<script>' + jszip + '</script>')
html = html.replace('%%DOCXPREVIEW%%','<script>' + docxpreview + '</script>')
html = html.replace('%%STAMPS%%',     STAMPS_JS)

out_path = os.path.join(base, '🔴スタンプ貼り付けツール.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built: {os.path.getsize(out_path):,} bytes")