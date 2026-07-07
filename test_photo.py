# -*- coding: utf-8 -*-
"""
fetch_ambassador_photo フルフロー テスト
"""
import sys, pathlib, importlib.util

spec = importlib.util.spec_from_file_location("mcp", "make_cv_plus.py")
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

import anthropic
client = anthropic.Anthropic(api_key=mod.CLAUDE_API_KEY)

save_path = pathlib.Path("cv/photo/test_klucar_full.jpg")
save_path.parent.mkdir(parents=True, exist_ok=True)
if save_path.exists():
    save_path.unlink()

info = {
    "full_name_ja": "マルチン・クルチャル",
    "nationality": "チェコ共和国",
    "current_position": "駐日チェコ共和国特命全権大使",
    "wikipedia_title_en": "Martin Klucar",
}

print("=== Step: get_embassy_pages ===")
embassy_pages = mod.get_embassy_pages("駐日大使", "チェコ", "マルチン・クルチャル", client)
print("embassy_pages:", embassy_pages)

print("\n=== Step: fetch_ambassador_photo ===")
result = mod.fetch_ambassador_photo(
    info, "駐日大使", "チェコ", client, save_path,
    embassy_pages=embassy_pages
)
print("結果:", result)
if save_path.exists():
    print("ファイルサイズ:", save_path.stat().st_size, "bytes")
else:
    print("ファイルが作成されませんでした")
