"""
make_en_intelligence.py  v2
英語版インテリジェンスページ (docs/en/intelligence.html) 生成スクリプト

処理方針:
- 全メール: HTMLをそのまま html ファイルとして保存（PDF化・翻訳なし）
- Jetro のみ: 件名だけ英訳（1 API call/件）
- 自動車関連のみ: EN+JA 要約段落生成 → 要約 PDF 作成
- カード: HTML リンク（全件）＋ Summary PDF ボタン（自動車関連のみ）
"""

import os, re, sys, io, json, html as _html, subprocess, urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Windowsのユーザー環境変数から APIキーを自動ロード
if not os.environ.get("ANTHROPIC_API_KEY"):
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as _k:
            _v, _ = winreg.QueryValueEx(_k, "ANTHROPIC_API_KEY")
            if _v: os.environ["ANTHROPIC_API_KEY"] = _v
    except Exception:
        pass

def _get_gh_token() -> str:
    try:
        import subprocess, winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
            v, _ = winreg.QueryValueEx(k, "GH_TOKEN")
            if v: return v
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import win32com.client, pythoncom
import anthropic
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Config ────────────────────────────────────────────────────────────────────
BASE         = Path(__file__).parent
ROLLING_JSON = BASE / "docs" / "data" / "mail_rolling.json"
HTML_DIR     = BASE / "docs" / "data" / "pdfs"   # html/pdf 両方ここに置く
EN_HTML      = BASE / "docs" / "en" / "intelligence.html"
MODEL        = "claude-haiku-4-5-20251001"
JST          = timezone(timedelta(hours=9))
GH_TOKEN     = os.environ.get("GH_TOKEN") or _get_gh_token()

MAIL_FOLDERS = ["*Politico", "EG", "JETRO"]
JA_SENDERS   = {"Jetro"}

_TOYOTA_KW = [
    "toyota","トヨタ","自動車","automotive","auto sector","electric vehicle",
    "ev tariff","ev policy","ev market","automobile","car tariff","car industry",
    "car maker","porsche","volkswagen","vw ","stellantis","bmw","nissan",
    "honda motor","ford motor","general motors","自動車産業","自動車メーカー",
    "自動車業界","catl","usmca","industrial accelerator act",
]
_MONTH_ABBR = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
_SENDER_CODE = {
    "Eurasia Group": ("EG",  "#8a6200"),
    "POLITICO":      ("POL", "#a8121e"),
    "Jetro":         ("JET", "#007838"),
}


# ── Utilities ─────────────────────────────────────────────────────────────────
def _e(s: str) -> str:
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def _url_path(p: str) -> str:
    """onclick内パス用: & ' ; をURLエンコード（ブラウザのHTML→JSデコードで壊れない）"""
    return str(p).replace('&', '%26').replace("'", '%27').replace(';', '%3B')

def _js_str(s: str) -> str:
    """onclick内タイトル用: シングルクォートをJSエスケープ"""
    return str(s).replace('\\', '\\\\').replace("'", "\\'")

def strip_html_tags(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>",  "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>",   "",   text)
    text = _html.unescape(text)
    return re.sub(r"\n{4,}", "\n\n\n", text).strip()

def safe_fname(s: str, n: int = 50) -> str:
    return re.sub(r"\s+", "_", re.sub(r'[\\/:*?"<>|\r\n\t]', "_", s.strip()))[:n]

def is_toyota(subject: str, body: str) -> bool:
    return any(kw in (subject + " " + body[:2000]).lower() for kw in _TOYOTA_KW)

def normalize_sender(name: str) -> str:
    n = name.upper()
    if "EURASIA" in n or n.startswith("EG"):  return "Eurasia Group"
    if "POLITICO" in n:                        return "POLITICO"
    if "JETRO" in n or "ジェトロ" in name or "ビジネス短信" in name: return "Jetro"
    return name

def estimate_read_min(text: str) -> int:
    return max(1, min(round(len(text.split()) / 200), 15))

def sender_code(s: str):
    return _SENDER_CODE.get(s, ("OTH", "#444488"))

def parse_json_safe(text: str) -> dict:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())

def clean_cid(html_text: str) -> str:
    html_text = re.sub(r'src="cid:[^"]+"', 'src=""', html_text)
    html_text = re.sub(r"src='cid:[^']+'", "src=''", html_text)
    return html_text

def extract_and_replace_cid(mail, html_body: str, img_dir: Path, prefix: str = "") -> str:
    """Outlookインライン添付画像をファイル保存し、cid:参照を相対パスに置換"""
    try:
        attachments = getattr(mail, "Attachments", None)
        if not attachments or attachments.Count == 0:
            return clean_cid(html_body)

        cid_map = {}
        for i in range(1, attachments.Count + 1):
            att = attachments.Item(i)
            try:
                content_id = att.PropertyAccessor.GetProperty(
                    "http://schemas.microsoft.com/mapi/proptag/0x3712001E"
                )
            except Exception:
                content_id = None
            if not content_id:
                continue
            ext = Path(getattr(att, "FileName", "") or "").suffix or ".dat"
            safe_name = f"{prefix}_img{i}{ext}" if prefix else re.sub(r'[^\w\-.]', '_', getattr(att, "FileName", f"img{i}.dat"))
            img_path = img_dir / safe_name
            try:
                att.SaveAsFile(str(img_path))
                cid_map[content_id] = safe_name
                cid_map[content_id.strip('<>')] = safe_name
            except Exception as ex:
                print(f"  [WARN] 画像保存失敗: {ex}")

        if not cid_map:
            return clean_cid(html_body)

        def _replace(m):
            cid = m.group(1)
            fname = cid_map.get(cid) or cid_map.get(cid.strip('<>')) or cid_map.get(f'<{cid}>')
            return f'src="{fname}"' if fname else 'src=""'

        html_body = re.sub(r'src="cid:([^"]+)"', _replace, html_body)
        html_body = re.sub(r"src='cid:([^']+)'",
                           lambda m: _replace(m).replace('"', "'"), html_body)
        html_body = re.sub(r'src="cid:[^"]+"', 'src=""', html_body)
        html_body = re.sub(r"src='cid:[^']+'", "src=''", html_body)
        return html_body
    except Exception as ex:
        print(f"  [WARN] CID置換失敗: {ex}")
        return clean_cid(html_body)


# ── Font ──────────────────────────────────────────────────────────────────────
def register_fonts():
    for path, idx, name in [
        (r"C:\Windows\Fonts\meiryo.ttc", 0, "JP"),
        (r"C:\Windows\Fonts\meiryo.ttc", 1, "JPB"),
    ]:
        if Path(path).exists():
            try: pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
            except: pass


# ── 最近N日のメール全件取得（再処理用）────────────────────────────────────────
def get_all_recent(ns, folder_name: str, days: int = 3) -> list:
    inbox  = ns.GetDefaultFolder(6)
    target = find_folder(inbox, folder_name)
    if not target:
        for store in ns.Stores:
            try:
                target = find_folder(store.GetRootFolder(), folder_name)
                if target: break
            except: pass
    if not target:
        return []
    items = target.Items
    items.Sort("[ReceivedTime]", True)
    result = []
    for item in items:
        try:
            recv = getattr(item, "ReceivedTime", None)
            if not recv: continue
            recv_naive = datetime(recv.year, recv.month, recv.day, recv.hour, recv.minute)
            if (datetime.now() - recv_naive).days > days:
                break
            if getattr(item, "Class", 0) == 43:
                result.append(item)
        except Exception:
            pass
    return result


# ── Summary PDF（自動車関連のみ）────────────────────────────────────────────
def make_summary_pdf(subject_en: str, sender: str, date_str: str,
                     summary_en: str, summary_ja: str, out_path: Path):
    def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    doc  = SimpleDocTemplate(str(out_path), pagesize=A4,
                             leftMargin=24*mm, rightMargin=24*mm,
                             topMargin=22*mm, bottomMargin=22*mm)
    st   = ParagraphStyle("t",  fontName="JPB", fontSize=14, leading=22, textColor=HexColor("#1a1a2e"))
    sm   = ParagraphStyle("m",  fontName="JP",  fontSize=9,  leading=14, textColor=HexColor("#666688"))
    sh   = ParagraphStyle("h",  fontName="JPB", fontSize=11, leading=18, spaceBefore=8, textColor=HexColor("#003399"))
    sb   = ParagraphStyle("b",  fontName="JP",  fontSize=10, leading=18, leftIndent=4)
    story = [
        Paragraph(esc(subject_en), st),
        Paragraph(f"From: {esc(sender)}  &nbsp; {esc(date_str)}", sm),
        Spacer(1, 6*mm),
        HRFlowable(width="100%", thickness=0.8, color=HexColor("#aaaacc"), spaceAfter=4*mm),
        Paragraph("English Summary", sh),
        Spacer(1, 2*mm),
    ]
    for line in summary_en.splitlines():
        story.append(Paragraph(esc(line), sb) if line.strip() else Spacer(1, 3*mm))
    story += [
        Spacer(1, 6*mm),
        HRFlowable(width="100%", thickness=0.8, color=HexColor("#ccccaa"), spaceAfter=4*mm),
        Paragraph("日本語要約", sh),
        Spacer(1, 2*mm),
    ]
    for line in summary_ja.splitlines():
        story.append(Paragraph(esc(line), sb) if line.strip() else Spacer(1, 3*mm))
    doc.build(story)


# ── Outlook ───────────────────────────────────────────────────────────────────
def connect_outlook():
    try:    return win32com.client.GetActiveObject("Outlook.Application")
    except: pass
    pythoncom.CoInitialize()
    return win32com.client.Dispatch("Outlook.Application")

def find_folder(parent, name: str):
    for f in parent.Folders:
        if f.Name == name: return f
        found = find_folder(f, name)
        if found: return found
    return None

def get_unread(ns, folder_name: str) -> list:
    inbox  = ns.GetDefaultFolder(6)
    target = find_folder(inbox, folder_name)
    if not target:
        for store in ns.Stores:
            try:
                target = find_folder(store.GetRootFolder(), folder_name)
                if target: break
            except: pass
    if not target:
        print(f"  [WARN] フォルダー未発見: {folder_name}")
        return []
    items = target.Items
    items.Sort("[ReceivedTime]", True)
    return [m for m in items if getattr(m, "UnRead", False) and getattr(m, "Class", 0) == 43]


# ── HTML 抽出・保存 ───────────────────────────────────────────────────────────
_EG_ANALYST_RE = re.compile(
    r'https://library\.eurasiagroup\.net//tag/analystimage/([^/\s"\']+)/([^/\s"\']+)'
)

def _download_analyst_photo(url: str, img_dir: Path) -> str:
    """外部アナリスト写真URLをローカルJPEGにDLしてファイル名を返す。失敗時は元URLを返す。"""
    try:
        analyst_id = url.rstrip("/").split("/")[-1]
        safe_id = re.sub(r'[^a-zA-Z0-9._@-]', '_', analyst_id)
        local_name = f"eg_analyst_{safe_id}.jpg"
        local_path = img_dir / local_name
        if not local_path.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            # PIL で正規 JPEG に変換・圧縮
            try:
                from PIL import Image
                import io as _io
                img = Image.open(_io.BytesIO(data)).convert("RGB")
                img.thumbnail((320, 320))
                buf = _io.BytesIO()
                img.save(buf, "JPEG", quality=85)
                local_path.write_bytes(buf.getvalue())
            except Exception:
                local_path.write_bytes(data)
            print(f"  [DL] analyst photo: {local_name}")
        return local_name
    except Exception as ex:
        print(f"  [WARN] analyst photo DL失敗 {url}: {ex}")
        return url

def _localize_analyst_photos(html_body: str, img_dir: Path) -> str:
    """HTMLのアナリスト写真URLをローカルファイル参照に置換"""
    def _replace(m):
        return _download_analyst_photo(m.group(0), img_dir)
    return _EG_ANALYST_RE.sub(_replace, html_body)

def save_mail_html(mail, out_path: Path, base_name: str = "") -> bool:
    try:
        html_body = getattr(mail, "HTMLBody", "") or ""
        if not html_body:
            text = getattr(mail, "Body", "") or ""
            html_body = (
                "<!DOCTYPE html><html><body style='font-family:sans-serif;padding:20px'>"
                + "".join(f"<p>{_e(l)}</p>" for l in text.splitlines())
                + "</body></html>"
            )
        html_body = extract_and_replace_cid(mail, html_body, out_path.parent, prefix=base_name)
        html_body = _localize_analyst_photos(html_body, out_path.parent)
        out_path.write_text(html_body, encoding="utf-8")
        return True
    except Exception as ex:
        print(f"  [WARN] HTML保存失敗: {ex}")
        return False


# ── Claude API ────────────────────────────────────────────────────────────────
def translate_subject(subject: str, client) -> str:
    """Jetro件名を英訳（短いので1 call）"""
    try:
        resp = client.messages.create(
            model=MODEL, max_tokens=80,
            messages=[{"role": "user", "content":
                f'Translate this Japanese email subject to English. Return the translation only, no quotes.\n\n{subject}'}]
        )
        return resp.content[0].text.strip()
    except Exception as ex:
        print(f"  [WARN] 件名翻訳失敗: {ex}")
        return subject


def generate_bilingual_summary(subject: str, body_text: str, is_ja: bool, client) -> dict:
    """自動車関連メールの EN+JA 要約を 1 call で生成"""
    lang_note = "The source is in Japanese." if is_ja else "The source is in English."
    try:
        resp = client.messages.create(
            model=MODEL, max_tokens=500,
            messages=[{"role": "user", "content":
                f"{lang_note} Write a concise automotive-industry summary.\n"
                "Return JSON only:\n"
                '{"summary_en": "2-3 sentences in plain English, WSJ style, no heading",\n'
                ' "summary_ja": "same in natural Japanese, 2-3 sentences, no heading"}\n\n'
                f"Subject: {subject}\n{body_text[:2500]}"}]
        )
        d = parse_json_safe(resp.content[0].text)
        return {
            "summary_en": d.get("summary_en", ""),
            "summary_ja": d.get("summary_ja", ""),
        }
    except Exception as ex:
        print(f"  [WARN] 要約生成失敗: {ex}")
        return {"summary_en": "", "summary_ja": ""}


def generate_sidebar_summary(toyota_entries: list, client) -> str:
    """自動車関連エントリからサイドバー用英語要約を生成"""
    items = "\n".join(
        f'- [{em["sender_norm"]}] {em.get("subject_en") or em["subject"]}: {em.get("summary_en","")}'
        for em in toyota_entries[:6] if em.get("summary_en")
    )
    if not items:
        return ""
    try:
        resp = client.messages.create(
            model=MODEL, max_tokens=400,
            messages=[{"role": "user", "content":
                "You are writing the sidebar of an intelligence dashboard for a global automaker.\n\n"
                "Write 2-3 short paragraphs in plain, direct English — WSJ reporter style, not consultant. "
                "No heading, no bullets, no markdown.\n\n"
                "Structure: (1) What happened today — specific and concrete. "
                "(2) Why it matters for the auto industry. "
                "(3) What to watch next — one sentence.\n\n"
                "No jargon. No filler phrases. Do NOT name specific automakers. No title.\n\n"
                f"Source material:\n{items}"}]
        )
        raw = re.sub(r"^#+[^\n]*\n+", "", resp.content[0].text.strip())
        return raw.strip()
    except Exception as ex:
        print(f"  [WARN] サイドバー生成失敗: {ex}")
        return ""


def translate_to_ja(en_text: str, client) -> str:
    if not en_text:
        return ""
    try:
        resp = client.messages.create(
            model=MODEL, max_tokens=500,
            messages=[{"role": "user", "content":
                "以下の英語を自然な日本語に翻訳してください。段落の区切りはそのまま保持し、前置き不要。\n\n"
                + en_text}]
        )
        return resp.content[0].text.strip()
    except Exception as ex:
        print(f"  [WARN] translate_to_ja 失敗: {ex}")
        return ""


# ── rolling JSON 更新 ─────────────────────────────────────────────────────────
def update_rolling(emails_all: list, toyota_summary_en: str, toyota_summary_ja: str):
    data = json.loads(ROLLING_JSON.read_text(encoding="utf-8"))
    existing = {em["ts"]: i for i, em in enumerate(data["emails"])}

    for ne in emails_all:
        ts = ne["ts"]
        if ts in existing:
            data["emails"][existing[ts]].update({
                k: ne[k] for k in
                ("subject_en","html","summary_en","summary_ja","summary_pdf","toyota")
                if k in ne
            })
        else:
            data["emails"].append(ne)

    data["emails"].sort(key=lambda x: x["ts"], reverse=True)
    data["emails"] = data["emails"][:50]

    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    data["updated_at"]        = now_str
    data["toyota_summary_en"] = toyota_summary_en
    data["toyota_summary"]    = toyota_summary_ja
    ROLLING_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Rolling] 合計 {len(data['emails'])} 件")
    return data


# ── HTML 生成（英語版ページ）────────────────────────────────────────────────
_MAIL_V2_CSS = """
    :root { --primary:#16163e; --surface:#ffffff; --surface-2:#edeef1; --border:#d8dae0; --text:#1a1a2e; --text-sub:#6b6f7a; --accent:#0096c8; }
    .v2-wrap { max-width:1280px; margin:28px auto; padding:0 20px; display:grid; grid-template-columns:1fr 300px; gap:28px; align-items:start; }
    .v2-left { position:sticky; top:112px; max-height:calc(100vh - 140px); overflow-y:auto; padding-right:4px; }
    .v2-left::-webkit-scrollbar { width:5px; } .v2-left::-webkit-scrollbar-thumb { background:rgba(0,0,0,.18); border-radius:3px; }
    .v2-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; align-items:start; }
    .v2-card { border-radius:4px; padding:14px 16px 12px; display:flex; flex-direction:column; gap:7px; box-shadow:2px 3px 8px rgba(0,0,0,.10),0 1px 2px rgba(0,0,0,.06); transition:transform .15s,box-shadow .15s; position:relative; }
    .v2-card:hover { transform:translateY(-3px); box-shadow:3px 6px 16px rgba(0,0,0,.15); }
    .v2-card[data-s="EG"]  { background:#fffaed; }
    .v2-card[data-s="POL"] { background:#fff0f1; }
    .v2-card[data-s="JET"] { background:#edfff4; }
    .v2-card[data-s="OTH"] { background:#f5f5ff; }
    .v2-sender { font-size:10px; font-weight:700; letter-spacing:.8px; text-transform:uppercase; }
    .v2-card[data-s="EG"]  .v2-sender { color:#8a6200; }
    .v2-card[data-s="POL"] .v2-sender { color:#a8121e; }
    .v2-card[data-s="JET"] .v2-sender { color:#007838; }
    .v2-card[data-s="OTH"] .v2-sender { color:#444488; }
    .v2-title   { font-size:15px; font-weight:700; line-height:1.45; color:#1a1a2e; flex:1; cursor:pointer; }
    .v2-title:hover { color:#0096c8; }
    .v2-summary { font-size:13px; color:#3a3a50; line-height:1.6; border-top:1px solid rgba(0,0,0,.08); padding-top:7px; }
    .v2-dot     { position:absolute; top:8px; right:10px; font-size:18px; opacity:.9; }
    .v2-meta    { font-size:10.5px; color:var(--text-sub); border-top:1px solid rgba(0,0,0,.07); padding-top:6px; display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
    .v2-pdf-btn { font-size:10px; font-weight:600; color:#fff; background:#555599; border:none; border-radius:3px; padding:2px 8px; cursor:pointer; white-space:nowrap; }
    .v2-pdf-btn:hover { background:#333377; }
    .v2-sidebar { position:sticky; top:112px; max-height:calc(100vh - 140px); overflow-y:auto; background:var(--surface); border:1px solid var(--border); border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,.07); }
    .v2-sidebar::-webkit-scrollbar { width:5px; } .v2-sidebar::-webkit-scrollbar-thumb { background:rgba(0,0,0,.18); border-radius:3px; }
    .v2-sb-head { background:#f5f6f8; border-bottom:1px solid var(--border); padding:12px 18px; }
    .v2-sb-ttl  { font-size:15px; font-weight:700; color:var(--primary); }
    .v2-sb-sub  { font-size:12px; color:var(--text-sub); margin-top:2px; }
    .v2-sb-body { padding:16px 18px; }
    .v2-summary-block p { font-size:14px; line-height:1.75; color:#2a2a3e; margin-bottom:10px; }
    .v2-summary-block p:last-child { margin-bottom:0; }
    .v2-hr      { border:none; border-top:1px solid var(--border); margin:14px 0; }
    .v2-src-lbl { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-sub); margin-bottom:8px; }
    .v2-src     { display:flex; align-items:flex-start; gap:8px; padding:7px 0; border-bottom:1px solid var(--border); cursor:pointer; font-size:13px; line-height:1.4; color:var(--text); transition:color .15s; }
    .v2-src:last-child { border-bottom:none; }
    .v2-src:hover { color:var(--accent); }
    .v2-badge   { font-size:9.5px; font-weight:700; color:#fff; padding:2px 5px; border-radius:3px; white-space:nowrap; flex-shrink:0; margin-top:1px; }
    .v2-rt      { font-size:10.5px; color:var(--text-sub); margin-top:10px; }
    .v2-modal   { display:none; position:fixed; inset:0; z-index:999; background:rgba(0,0,0,.65); align-items:center; justify-content:center; }
    .v2-modal-box { background:#fff; border-radius:10px; overflow:hidden; width:90vw; max-width:940px; height:88vh; display:flex; flex-direction:column; box-shadow:0 12px 48px rgba(0,0,0,.4); animation:mIn .16s ease; }
    @keyframes mIn { from{transform:scale(.94);opacity:0} to{transform:scale(1);opacity:1} }
    .v2-mh { display:flex; align-items:center; gap:12px; padding:10px 18px; background:var(--primary); color:#fff; flex-shrink:0; }
    .v2-mt { font-size:13px; font-weight:600; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .v2-mc { background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.3); color:#fff; border-radius:6px; padding:4px 12px; cursor:pointer; font-size:12px; }
    .v2-mc:hover { background:rgba(255,255,255,.28); }
    .v2-mf { flex:1; border:none; width:100%; }
    @media(max-width:960px){ .v2-wrap{grid-template-columns:1fr;} .v2-left{position:static;max-height:none;} .v2-sidebar{position:static;max-height:none;} }
    @media(max-width:640px){ .v2-grid{grid-template-columns:1fr;} }
"""

_BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif; background: #f4f5f7; color: #1a1a2e; font-size: 16px; line-height: 1.7; }
.site-header { background: #1a1a2e; color: #fff; padding: 0 24px; height: 58px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 300; box-shadow: 0 2px 8px rgba(0,0,0,.25); }
.logo { font-size: 20px; font-weight: 700; letter-spacing: .5px; white-space: nowrap; cursor: pointer; }
.logo em { color: #5bc8f5; font-style: normal; }
.header-date { font-size: 12px; color: rgba(255,255,255,.5); white-space: nowrap; }
.header-spacer { flex: 1; }
.live-badge { background: #e63946; color: #fff; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: 1px; }
.update-time { font-size: 11px; color: rgba(255,255,255,.4); white-space: nowrap; }
.lang-toggle { display: flex; gap: 6px; font-size: 12px; }
.lang-toggle a { color: rgba(255,255,255,.6); text-decoration: none; padding: 3px 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,.3); transition: all .15s; font-weight: 600; }
.lang-toggle a.active { color: #fff; background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.7); }
.lang-toggle a:hover { color: #fff; background: rgba(255,255,255,.12); }
.page-nav { background: #fff; border-bottom: 1px solid #e5e7eb; padding: 0 24px; display: flex; align-items: stretch; position: sticky; top: 58px; z-index: 200; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.page-nav a { display: flex; align-items: center; gap: 6px; padding: 0 18px; height: 44px; font-size: 14px; font-weight: 500; color: #6b7280; text-decoration: none; border-bottom: 3px solid transparent; white-space: nowrap; transition: color .15s, border-color .15s; }
.page-nav a:hover { color: #1a1a2e; }
.page-nav a.active { color: #1a1a2e; border-bottom-color: #1a1a2e; font-weight: 700; }
.page-nav a .nav-icon { font-size: 15px; }
.page-nav a.dim { opacity: .45; pointer-events: none; }
.page-nav a:last-child { margin-left: auto; border-left: 1px solid #e5e7eb; }
.site-footer { text-align: center; padding: 28px 20px; font-size: 11px; color: #9ca3af; margin-top: 32px; border-top: 1px solid #e5e7eb; }
@media (max-width: 640px) { .site-header { padding: 0 14px; } .update-time { display: none; } .page-nav { padding: 0 8px; } .page-nav a { padding: 0 12px; font-size: 13px; } }
"""


def render_card(em: dict) -> str:
    code, _     = sender_code(em.get("sender_norm", ""))
    title       = em.get("subject_en") or em.get("subject", "")
    html_path   = em.get("html", "") or em.get("pdf", "")
    summary_pdf = em.get("summary_pdf", "")
    # docs/data/... → ../data/... (intelligence.html は en/ 下にある)
    def to_rel(p):
        return ("../" + p) if p.startswith("data/") else p
    html_rel    = to_rel(html_path)
    pdf_rel     = to_rel(summary_pdf)
    summary_en  = em.get("summary_en", "")
    date_lbl    = em.get("date_label", "")
    read_min    = em.get("read_min", 1)
    dot         = '<span class="v2-dot">🚗</span>' if em.get("toyota") else ""
    summary_html = (
        f'\n  <div class="v2-summary">{_e(summary_en[:160])}…</div>'
        if summary_en else ""
    )
    pdf_btn = (
        f'<button class="v2-pdf-btn" onclick="event.stopPropagation();openFile(\'{_url_path(pdf_rel)}\',\'{_js_str(title[:60])} — Summary\')">📄 Summary</button>'
        if summary_pdf else ""
    )
    return (
        f'<div class="v2-card" data-s="{code}" onclick="openFile(\'{_url_path(html_rel)}\',\'{_js_str(title[:60])}\')">\n'
        f'  {dot}\n'
        f'  <div class="v2-sender">{_e(em.get("sender_norm",""))}</div>\n'
        f'  <div class="v2-title">{_e(title)}</div>'
        f'{summary_html}\n'
        f'  <div class="v2-meta">{_e(date_lbl)} &nbsp;·&nbsp; {read_min} MIN &nbsp;{pdf_btn}</div>\n'
        f'</div>'
    )


def render_sidebar(toyota_entries: list, updated_at: str, summary_en: str) -> str:
    if summary_en:
        paras = [p.strip() for p in summary_en.split("\n\n") if p.strip()]
        body  = "\n".join(f"<p>{_e(p)}</p>" for p in paras)
    elif toyota_entries:
        body  = "\n".join(
            f'<p><strong>{_e((em.get("subject_en") or em["subject"])[:55])}.</strong> '
            f'{_e(em.get("summary_en","")[:120])}</p>'
            for em in toyota_entries[:4] if em.get("summary_en")
        ) or "<p>No automotive-relevant emails today.</p>"
    else:
        body = "<p>No automotive-relevant emails today.</p>"

    src_items = ""
    for em in toyota_entries[:6]:
        _, col   = sender_code(em.get("sender_norm",""))
        html_path = em.get("html","")
        rel      = ("../" + html_path) if html_path.startswith("data/") else html_path
        subj     = em.get("subject_en") or em.get("subject","")
        src_items += (
            f'<div class="v2-src" onclick="openFile(\'{_url_path(rel)}\',\'{_js_str(subj[:60])}\')">'
            f'<span class="v2-badge" style="background:{col};">{_e(em.get("sender_norm",""))}</span>'
            f'<span>{_e(subj)}</span></div>\n'
        )
    total_min = sum(em.get("read_min", 0) for em in toyota_entries[:6])
    sources_html = (
        f'<hr class="v2-hr"><div class="v2-src-lbl">Source Emails</div>\n{src_items}'
        if src_items else ""
    )
    return f"""<div class="v2-sidebar">
  <div class="v2-sb-head">
    <div class="v2-sb-ttl">Key Takeaways</div>
    <div class="v2-sb-sub">{_e(updated_at)} &nbsp;·&nbsp; ~1 min read</div>
  </div>
  <div class="v2-sb-body">
    <div class="v2-summary-block">{body}</div>
    {sources_html}
    <div class="v2-rt">⏱ Full sources: ~{total_min} min total</div>
  </div>
</div>"""


def build_html(emails_all: list, sidebar_html: str, updated_at: str) -> str:
    now_jst    = datetime.now(JST)
    date_en    = now_jst.strftime("%B %d, %Y")
    cards_html = "\n".join(render_card(em) for em in emails_all)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intelligence | World Intelligence Monitor</title>
<style>
{_BASE_CSS}
{_MAIL_V2_CSS}
</style>
</head>
<body>
<header class="site-header">
  <div class="logo" onclick="location.href='index.html'">World<em>News</em></div>
  <div class="header-date">{date_en}</div>
  <div class="header-spacer"></div>
  <div class="update-time">Updated: {_e(updated_at)}</div>
  <div class="lang-toggle">
    <a href="../jp/intelligence.html">JP</a>
    <a href="intelligence.html" class="active">EN</a>
  </div>
  <div class="live-badge">LIVE</div>
</header>
<nav class="page-nav">
  <a href="index.html"><span class="nav-icon">🏠</span>Home</a>
  <a href="intelligence.html" class="active"><span class="nav-icon">📋</span>Intelligence</a>
  <a href="trump.html"><span class="nav-icon">🇺🇸</span>US / Trump</a>
  <a href="theme.html"><span class="nav-icon">🔎</span>Themes</a>
  <a href="midterm.html"><span class="nav-icon">🗳️</span>US Midterms</a>
  <a href="summary.html"><span class="nav-icon">📋</span>Exec Summary</a>
</nav>
<div class="v2-wrap">
  <div class="v2-left">
    <div class="v2-grid">
{cards_html}
    </div>
  </div>
  {sidebar_html}
</div>
<footer class="site-footer">
  Sources: EG (Eurasia Group) &nbsp;|&nbsp; POLITICO &nbsp;|&nbsp; JETRO &nbsp;|&nbsp;
  Updated: {_e(updated_at)}
</footer>
<div id="v2-modal" class="v2-modal">
  <div class="v2-modal-box">
    <div class="v2-mh">
      <span id="v2-mt" class="v2-mt">—</span>
      <button onclick="closeModal()" class="v2-mc">✕ Close</button>
    </div>
    <iframe id="v2-mf" class="v2-mf" src="about:blank"></iframe>
  </div>
</div>
<script>
var modal=document.getElementById('v2-modal'),frame=document.getElementById('v2-mf'),ttl=document.getElementById('v2-mt');
function openFile(u,t){{ttl.textContent=t||'';frame.src=u;modal.style.display='flex';}}
function closeModal(){{modal.style.display='none';frame.src='about:blank';}}
modal.addEventListener('click',function(e){{if(e.target===modal)closeModal();}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeModal();}});
</script>
</body>
</html>"""


# ── git + deploy ──────────────────────────────────────────────────────────────
def git_push_and_deploy(msg: str):
    def run(cmd): subprocess.run(cmd, cwd=str(BASE))
    run(["git", "add",
         "docs/en/intelligence.html",
         "docs/en/index.html",
         "docs/data/mail_rolling.json",
         "docs/data/pdfs"])
    diff = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=str(BASE))
    if diff.returncode == 0:
        print("[Git] 変更なし。スキップ。")
        return
    run(["git", "commit", "-m", msg])
    push = subprocess.run(["git", "push"], cwd=str(BASE))
    if push.returncode != 0:
        run(["git", "fetch", "origin", "main"])
        run(["git", "merge", "-X", "ours", "origin/main", "--no-edit"])
        subprocess.run(["git", "push"], cwd=str(BASE))
    req = urllib.request.Request(
        "https://api.github.com/repos/shortreport/world-monitoring/actions/workflows/update.yml/dispatches",
        data=b'{"ref":"main"}',
        headers={"Authorization": f"token {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req)
        print("[Deploy] GitHub Actions トリガー完了。約5分で反映されます。")
    except Exception as ex:
        print(f"[Deploy] WARN: Actions トリガー失敗 — {ex}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--reprocess", action="store_true",
                        help="最近3日分のHTMLを画像付きで強制再生成（rolling JSON更新なし）")
    args = parser.parse_args()

    register_fonts()
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()

    print("Outlook に接続中...")
    outlook = connect_outlook()
    ns      = outlook.GetNamespace("MAPI")

    new_entries  = []
    mark_as_read = []

    for folder_name in MAIL_FOLDERS:
        print(f"\n{'='*50}\nフォルダー: {folder_name}")
        if args.reprocess:
            mails = get_all_recent(ns, folder_name, days=3)
            print(f"再処理対象: {len(mails)} 件")
        else:
            mails = get_unread(ns, folder_name)
            print(f"未読: {len(mails)} 件")

        for i, mail in enumerate(mails, 1):
            subject  = getattr(mail, "Subject",    "") or "(no subject)"
            sender   = getattr(mail, "SenderName", "") or ""
            recv     = getattr(mail, "ReceivedTime", None)
            date_str = str(recv)[:16] if recv else ""
            body_raw = getattr(mail, "Body", "") or ""
            body_txt = strip_html_tags(body_raw)[:3000]

            print(f"  [{i}] {subject[:65]}")

            sender_norm = normalize_sender(sender)
            is_ja       = sender_norm in JA_SENDERS
            auto        = is_toyota(subject, body_txt)

            # タイムスタンプ
            if recv:
                date_tag = str(recv)[:16].replace(":","").replace("-","").replace(" ","_")
            else:
                date_tag = "00000000_0000"
            ts         = date_tag[:8] + "_" + date_tag[9:13]
            month      = int(date_tag[4:6])
            day        = int(date_tag[6:8])
            date_label = f"{_MONTH_ABBR[month-1]} {day}  {date_tag[9:11]}:{date_tag[11:13]}"

            base_name  = f"{date_tag}_{safe_fname(subject)}"
            html_fname = f"{base_name}.html"
            html_path  = f"data/pdfs/{html_fname}"
            html_out   = HTML_DIR / html_fname

            # ── HTML 保存（再処理時は強制上書き）───────────────────────────
            if not html_out.exists() or args.reprocess:
                save_mail_html(mail, html_out, base_name=base_name)
                print(f"    → HTML: {html_fname}")

            # ── Jetro: 件名だけ翻訳 ─────────────────────────────────────────
            subject_en = subject
            if is_ja:
                print(f"    → 件名翻訳中...")
                subject_en = translate_subject(subject, client)
                print(f"    → EN subject: {subject_en[:60]}")

            # ── 自動車関連: EN+JA 要約 → Summary PDF ────────────────────────
            summary_en = summary_ja = ""
            summary_pdf_path = ""
            if auto:
                print(f"    → 自動車関連: EN+JA 要約生成中...")
                sums       = generate_bilingual_summary(subject, body_txt, is_ja, client)
                summary_en = sums["summary_en"]
                summary_ja = sums["summary_ja"]
                if summary_en:
                    pdf_fname        = f"{base_name}_summary.pdf"
                    pdf_out          = HTML_DIR / pdf_fname
                    summary_pdf_path = f"data/pdfs/{pdf_fname}"
                    make_summary_pdf(subject_en, sender, date_str,
                                     summary_en, summary_ja, pdf_out)
                    print(f"    → Summary PDF: {pdf_fname}")

            new_entries.append({
                "ts":          ts,
                "sender_norm": sender_norm,
                "subject":     subject,
                "subject_en":  subject_en,
                "html":        html_path,
                "pdf":         html_path,        # 後方互換：JPページの pdf フィールドにも使う
                "summary_en":  summary_en,
                "summary_ja":  summary_ja,
                "summary_pdf": summary_pdf_path,
                "date_label":  date_label,
                "read_min":    estimate_read_min(body_raw),
                "toyota":      auto,
                "excerpt":     summary_ja[:130] if summary_ja else "",
            })
            if not args.reprocess:
                mark_as_read.append(mail)

    if args.reprocess:
        # 再処理モード: HTMLファイルを画像付きで再生成してpushするだけ
        print(f"\n[再処理] HTML再生成完了。rolling JSON更新・既読変更はスキップ。")
        print("\n[Git] コミット＆プッシュ中...")
        git_push_and_deploy(f"Reprocess HTML with images: {datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')}")
        return

    print(f"\n{len(mark_as_read)} 件を既読に変更...")
    for mail in mark_as_read:
        try: mail.UnRead = False
        except: pass

    # ── rolling JSON に統合 ───────────────────────────────────────────────────
    data = update_rolling(new_entries,
                          toyota_summary_en="", toyota_summary_ja="")
    emails_all    = data["emails"]
    toyota_entries = [em for em in emails_all if em.get("toyota") and em.get("summary_en")]

    # ── サイドバー要約 ────────────────────────────────────────────────────────
    if toyota_entries:
        print("\n英語サイドバー要約を生成中...")
        sidebar_en = generate_sidebar_summary(toyota_entries, client)
        print("日本語に翻訳中...")
        sidebar_ja = translate_to_ja(sidebar_en, client)
        update_rolling([], sidebar_en, sidebar_ja)
        data["toyota_summary_en"] = sidebar_en
        data["toyota_summary"]    = sidebar_ja
    else:
        sidebar_en = data.get("toyota_summary_en", "")

    # ── HTML 生成 ─────────────────────────────────────────────────────────────
    now_str      = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    toyota_entries = [em for em in emails_all if em.get("toyota") and em.get("summary_en")]
    sidebar_html  = render_sidebar(toyota_entries, now_str, sidebar_en)
    html_content  = build_html(emails_all, sidebar_html, now_str)
    EN_HTML.write_text(html_content, encoding="utf-8")
    print(f"[OK] EN Intelligence -> {EN_HTML}")

    # EN Home nav のグレーアウトを解除
    en_index = BASE / "docs" / "en" / "index.html"
    if en_index.exists():
        txt = en_index.read_text(encoding="utf-8")
        new = txt.replace('<a href="intelligence.html" class="dim">', '<a href="intelligence.html">')
        if new != txt:
            en_index.write_text(new, encoding="utf-8")
            print("[OK] EN Home nav: intelligence.html リンクを有効化")

    # ── git + deploy ──────────────────────────────────────────────────────────
    print("\n[Git] コミット＆プッシュ中...")
    git_push_and_deploy(f"EN Intelligence: {now_str}")


if __name__ == "__main__":
    main()
