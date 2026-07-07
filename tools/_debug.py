import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# _build.pyを実際にimportしてAPP_HTMLの中身を確認
with open('tools/_build.py', encoding='utf-8') as f:
    code = f.read()

# APP_HTML の中のSTAMPS部分
idx = code.find('const STAMPS')
end = code.find('];', idx)
block = code[idx:end+2]
names = re.findall("name: '([^']+)'", block)
print('names found:', names)
print('block length:', len(block))

# ビルドを実行してHTMLのSTAMPS部分も確認
exec(compile(code, '_build.py', 'exec'))
# APP_HTMLが定義されているはず
html_idx = APP_HTML.find('const STAMPS')
html_end = APP_HTML.find('];', html_idx)
html_block = APP_HTML[html_idx:html_end+2]
html_names = re.findall("name: '([^']+)'", html_block)
print('HTML names:', html_names)
