"""
World News ニュース番組 .mp4 自動生成スクリプト
依存: moviepy pillow gTTS imageio-ffmpeg (インストール済み)
使用法: python make_news_video.py
出力:  world_news_20260516.mp4
"""
import os, sys, time, textwrap, subprocess
from pathlib import Path
import numpy as np

BASE      = Path(__file__).parent
TMPDIR    = BASE / "_news_tmp"
VIDEO_DIR = BASE / "news program"
FILES_DIR = BASE / "files"
TMPDIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
FILES_DIR.mkdir(exist_ok=True)
OUTPUT    = str(VIDEO_DIR / "world_news_20260516.mp4")

W, H  = 1280, 720
FPS   = 24
SPEED = 1.68  # 音声速度

# ── 色定義 ────────────────────────────────────────────────────────────────────
BG    = (4,   4,  12)
WHITE = (255, 255, 255)
CYAN  = (0,   200, 255)
YEL   = (255, 215,   0)
RED   = (255,  48,  80)
ORG   = (255, 144,  64)
GRN   = ( 48, 255, 128)
DIM   = ( 80,  80, 120)

# ── 台本 ─────────────────────────────────────────────────────────────────────
SEGMENTS = [
    dict(
        badge="OPENING", color=CYAN, cover=True,
        title="World News",
        subtitle="2026年5月16日　主要ニュース",
        bullets=[], risk="", context="",
        narration=(
            "ワールドニュース。"
            "2026年5月16日の世界主要ニュースをお伝えします。"
        ),
    ),
    dict(
        badge="① 米中首脳会談", color=YEL, cover=False,
        title="「G2」の衝撃と台湾への最強警告",
        subtitle="習主席「対応誤れば衝突・非常に危険」/ トランプ「台湾武器売却は暫定保留」",
        bullets=[
            "5/14〜15 北京で米中首脳会談── トランプ大統領2017年以来の初訪中",
            "習主席「対応誤れば両国衝突・非常に危険」── 近年最も強硬な台湾警告",
            "トランプ「台湾武器売却140億ドルは暫定保留」── いかなる約束もしなかった",
            "貿易合意：ボーイング200機・大豆2500万トン・LNG・農産物購入に合意",
            "「測定された競争に基づく戦略的安定の米中関係」の枠組みを合意",
            "産経「G2時代の予感」── 日本の安保・同盟体制への影響を強く懸念",
        ],
        risk="▲リスク：数週間以内に台湾武器売却の可否が判明。米中G2合意が深化すれば日本が蚊帳の外に。",
        context="背景：米中が「管理可能な競争」を演出しつつ経済的相互依存を維持。台湾は最大の未解決事項。",
        narration=(
            "第1のニュースです。"
            "トランプ大統領が2017年以来となる北京訪問を終えました。"
            "貿易面では、ボーイング200機の購入や大豆2500万トン、"
            "LNGなど農産物の追加購入で合意しました。"
            "一方、習近平主席は台湾について、"
            "対応を誤れば両国は衝突し、非常に危険な状況に陥ると最強レベルの警告を発しました。"
            "トランプ大統領は140億ドル規模の台湾への武器売却について、"
            "暫定保留とし、いかなる約束もしなかったと述べました。"
            "両首脳は測定された競争に基づく戦略的安定の米中関係という枠組みに合意しましたが、"
            "産経新聞はこれをG2時代の予感と形容し、"
            "日本が米中合意から蚊帳の外に置かれるリスクを指摘しています。"
        ),
    ),
    dict(
        badge="② 米イラン戦争", color=RED, cover=False,
        title="交渉崩壊リスクとホルムズ長期封鎖",
        subtitle="トランプ「我慢の限界」/ 原油ピーク120ドル / 日本エネルギー危機",
        bullets=[
            "2/28 米・イスラエルが「エピック・フューリー作戦」開始。ハメネイ師死亡",
            "3/4 イランがホルムズ海峡「閉鎖」宣言── 3/8迄に船舶10隻以上が攻撃被害",
            "4/8 停戦合意も再エスカレート── 5/15現在トランプ「我慢の限界」と戦闘再開示唆",
            "原油：開戦時67ドル→ピーク120ドル（+79%）── 5月初 114ドルで依然高値圏",
            "グローバル原油供給の約20%が影響── IEA「史上最大のエネルギー安全保障の挑戦」",
            "日本：原油輸入の90%がホルムズ経由── 高市首相「6月に7割確保の見通し」",
        ],
        risk="▲リスク【最緊急】：数日〜数週間内に戦闘再開の可能性。長期封鎖で日本エネルギー危機・物価急騰。",
        context="背景：ホルムズ封鎖が長期化すれば原油150ドル超も予測。日本はLNGの代替調達ルート確保を急ぐ。",
        narration=(
            "第2のニュースです。"
            "2月28日、米国とイスラエルはエピック・フューリー作戦と呼ばれる軍事作戦を開始し、"
            "イランのハメネイ最高指導者が死亡しました。"
            "3月4日にイランはホルムズ海峡の閉鎖を宣言し、"
            "8日までに10隻以上の船舶が攻撃を受けました。"
            "4月8日に停戦が合意されましたが再エスカレートし、"
            "トランプ大統領はもう我慢の限界だと発言し、戦闘再開を示唆しています。"
            "原油価格は開戦前の67ドルからピーク時120ドルまで急騰し、"
            "5月初旬も114ドルと高値圏が続いています。"
            "世界の原油供給の約20%が影響を受けており、"
            "IEAは史上最大のエネルギー安全保障の挑戦と形容しました。"
            "日本は原油輸入の90%をホルムズ海峡に依存しており、"
            "高市首相は6月に7割以上確保の見通しと説明しています。"
        ),
    ),
    dict(
        badge="③ 日米関係", color=CYAN, cover=False,
        title="ベッセント来日とG2への強い懸念",
        subtitle="高市首相・上田日銀総裁と会談。レアアース・エネルギーで連携強化",
        bullets=[
            "ベッセント財務長官来日（5/11〜13）── 高市首相・片山財務相・上田日銀総裁と会談",
            "主要議題：レアアース代替調達・イラン対応・円安・通貨政策を協議",
            "中国がレアアース輸出規制を強化── 日本の半導体・防衛産業に直撃",
            "G7が2026年1月にレアアース代替サプライチェーン構築で合意済み",
            "米中会談後、トランプ大統領が高市首相と電話── 会談内容を詳細に共有",
            "レアアースETF（REMX）-3.6%急落── 台湾武器売却保留で供給不安が継続",
        ],
        risk="▲リスク：150日関税暫定措置期限（2026年夏）と台湾武器売却保留が日米関係の試金石に。",
        context="背景：日本の半導体・EV・防衛装備はレアアースに依存。中国の輸出規制が国家安全保障に直結。",
        narration=(
            "第3のニュースです。"
            "ベッセント米財務長官が5月11日から13日まで来日し、"
            "高市首相、片山財務大臣、上田日銀総裁と相次いで会談しました。"
            "主要議題はレアアースの代替調達、イラン情勢への対応、"
            "そして円安と通貨政策をめぐる協議です。"
            "中国がレアアースの輸出規制を強化しており、"
            "日本の半導体や防衛産業への打撃が深刻化しています。"
            "G7はすでに2026年1月にレアアース代替サプライチェーンの構築で合意しています。"
            "米中首脳会談の終了後、トランプ大統領は高市首相と電話会談を行い、"
            "会談内容を詳細に共有しました。"
            "しかし産経新聞は、米中がG2として世界を管理する構造の中で、"
            "日本が取り残されるリスクを指摘しています。"
        ),
    ),
    dict(
        badge="④ 台湾問題", color=ORG, cover=False,
        title="習主席の最強警告と武器売却の行方",
        subtitle="140億ドル保留・12月承認分110億ドルは維持── 数週間〜数ヶ月が分岐点",
        bullets=[
            "習主席「対応誤れば衝突・非常に危険」── 近年最も強硬な台湾警告を公開発表",
            "トランプ「140億ドル武器売却は暫定保留」── 交渉カードとして活用の構え",
            "中国：農産物・石油の購入増加を条件に、武器売却停止を強く要求",
            "2025年12月承認済みの110億ドル武器パッケージは現時点で維持",
            "台湾：防衛費250億ドル可決済み── 独自抑止力の強化と徴兵制延長を継続",
            "高市「台湾有事」答弁後── 黄川田大臣が日本閣僚として初めて中国を訪問",
        ],
        risk="▲リスク：武器売却凍結→台湾の抑止力低下→中国の圧力増大。数週間〜数ヶ月が重要な分岐点。",
        context="背景：習主席の発言は北京サミット前に中国側が公開。米側の沈黙と対照的で、圧力戦略の一環とみられる。",
        narration=(
            "第4のニュースです。"
            "米中首脳会談において台湾問題が最大の焦点となりました。"
            "習主席はトランプ大統領に対し、"
            "対応を誤れば両国は衝突し、非常に危険な状況に陥ると、"
            "近年で最も強硬なレベルの警告を発し、これを公開の声明として発表しました。"
            "中国側は農産物や石油の購入増加を条件に武器売却の停止を強く求めています。"
            "トランプ大統領は140億ドル規模の武器売却を暫定保留とし、"
            "交渉カードとして活用する構えです。"
            "2025年12月に承認済みの110億ドル分のパッケージは現時点で維持されています。"
            "台湾は防衛費250億ドルを可決し、独自の抑止力強化を継続しています。"
        ),
    ),
    dict(
        badge="⑤ 自動車産業", color=GRN, cover=False,
        title="ホンダ上場来初赤字・EV撤退加速",
        subtitle="1.45兆円EV損失 / 脱ガソリン撤回 / 日産とホンダが統合検討",
        bullets=[
            "ホンダ26年3月期：1.45兆円のEV関連損失── 上場来初の赤字4239億円",
            "ホンダ0シリーズSUV・セダン、オンタリオ州工場（1.5兆円規模）を無期限停止",
            "日産：3400億円超の損失── 工場閉鎖・大規模リストラ。ホンダと統合を検討",
            "トヨタ：EV＋ハイブリッド両軸で米工場に1600億円投資。純利益22%減を予測",
            "日本郵船：ホルムズ封鎖で中東向け自動車輸送の代替ルートを緊急検討中",
            "トヨタがインドに新工場建設発表（2029年稼働）── BYDの世界シェア拡大に対抗",
        ],
        risk="▲リスク：EV撤退の間にBYDが市場獲得加速。ホルムズ長期封鎖で輸送コストの恒常的上昇が懸念。",
        context="背景：日本メーカーはEV移行に乗り遅れた一方、中国BYDが2025年に世界販売台数1位に浮上済み。",
        narration=(
            "第5のニュースです。"
            "ホンダが2026年3月期決算で上場以来初となる4239億円の赤字に転落しました。"
            "EV関連の損失は1.45兆円に上り、"
            "ホンダ0シリーズのSUVとセダン、"
            "そして1.5兆円規模のカナダ・オンタリオ州工場計画を無期限停止しました。"
            "日産も3400億円を超える損失を計上し、工場閉鎖と大規模リストラを進めており、"
            "ホンダとの経営統合も検討されています。"
            "トヨタはEVとハイブリッドの両軸戦略で米工場に1600億円を投資しますが、"
            "純利益は22%の減益が予測されています。"
            "ホルムズ海峡の封鎖が続く中、"
            "日本郵船は中東向け自動車輸送の代替ルートを緊急検討しています。"
            "トヨタはインドへの新工場建設を発表し、"
            "BYDが世界シェアを拡大する中、成長市場へのシフトを加速させています。"
        ),
    ),
    dict(
        badge="END", color=CYAN, cover=True,
        title="World News",
        subtitle="以上、本日の主要ニュースをお伝えしました",
        bullets=[], risk="", context="",
        narration=(
            "以上、2026年5月16日の世界主要ニュースでした。"
            "また明日お会いしましょう。"
        ),
    ),
]

# ── フォント取得 ──────────────────────────────────────────────────────────────
def get_font(size, bold=False):
    from PIL import ImageFont
    candidates = [
        (r"C:\Windows\Fonts\meiryo.ttc",  1 if bold else 0),
        (r"C:\Windows\Fonts\YuGothM.ttc", 0),
        (r"C:\Windows\Fonts\msgothic.ttc", 0),
    ]
    for path, idx in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size, index=idx)
            except Exception:
                pass
    return ImageFont.load_default()


# ── スライド画像生成 ───────────────────────────────────────────────────────────
def make_frame(seg):
    from PIL import Image, ImageDraw
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    color = seg["color"]

    # グリッド背景
    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(0, 18, 36), width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(0, 18, 36), width=1)

    # ヘッダーバー
    draw.rectangle([(0, 0), (W, 58)], fill=(6, 6, 20))
    draw.line([(0, 58), (W, 58)], fill=color, width=2)
    draw.text((16, 14), "[ World News ]", font=get_font(24, bold=True), fill=WHITE)
    draw.text((W - 310, 20), "2026.05.16  LIVE", font=get_font(16), fill=DIM)

    # バッジ
    f_badge = get_font(16, bold=True)
    btext   = seg["badge"]
    bw      = min(len(btext) * 15 + 28, 400)
    draw.rounded_rectangle([(16, 66), (16 + bw, 96)],
                            radius=4, outline=color, width=1, fill=(4, 4, 20))
    draw.text((28, 70), btext, font=f_badge, fill=color)

    if seg["cover"]:
        # ── カバースライド ──────────────────────────
        f_big = get_font(76, bold=True)
        f_sub = get_font(28)
        tw  = draw.textlength(seg["title"],    font=f_big)
        tw2 = draw.textlength(seg["subtitle"], font=f_sub)
        draw.text(((W - tw)  / 2, 200), seg["title"],    font=f_big, fill=WHITE)
        draw.text(((W - tw2) / 2, 310), seg["subtitle"], font=f_sub, fill=color)
        draw.rectangle([(W//2 - 200, 370), (W//2 + 200, 373)], fill=color)
    else:
        # ── ニュースライド（2カラムレイアウト） ────────
        # 左カラム：タイトル・サブタイトル・箇条書き
        # 右カラム：リスク・背景（同じフォントサイズで統一）
        LCOL_W = 840   # 左カラム幅
        RDIV_X = 852   # 縦区切り線X
        RCOL_X = 864   # 右カラム本文開始X
        RCOL_W = W - RCOL_X - 12  # 右カラム幅 ≈ 404px

        f_t   = get_font(38, bold=True)  # タイトル
        f_s   = get_font(19)             # サブタイトル
        f_b   = get_font(17)             # 箇条書き
        f_lbl = get_font(17, bold=True)  # セクションラベル
        f_txt = get_font(17)             # リスク・背景（箇条書きと同サイズ）

        # ── 左カラム ──────────────────────────────────
        y = 104

        # タイトル（折り返し22文字）
        for line in textwrap.wrap(seg["title"], 22)[:2]:
            draw.text((16, y), line, font=f_t, fill=WHITE)
            y += 48

        # サブタイトル（折り返し44文字）
        for line in textwrap.wrap(seg["subtitle"], 44)[:2]:
            draw.text((16, y), line, font=f_s, fill=color)
            y += 27
        y += 8

        # 左カラム区切り線
        draw.rectangle([(16, y), (LCOL_W, y + 2)], fill=color)
        y += 12

        # 箇条書き（最大6項目、折り返し44文字・最大2行）
        for bullet in seg["bullets"][:6]:
            lines = textwrap.wrap("● " + bullet, 44)
            draw.text((16, y), lines[0], font=f_b, fill=(190, 190, 230))
            y += 28
            if len(lines) > 1:
                draw.text((30, y), lines[1], font=f_b, fill=(165, 165, 205))
                y += 26
            y += 5

        # ── 右カラム縦区切り線 ─────────────────────────
        draw.line([(RDIV_X, 66), (RDIV_X, H - 22)], fill=(50, 50, 90), width=1)
        draw.line([(RDIV_X + 1, 66), (RDIV_X + 1, H - 22)], fill=color, width=1)

        # ── 右カラム：リスク ──────────────────────────
        ry = 104

        # リスクラベル
        draw.rectangle([(RCOL_X, ry), (W - 12, ry + 28)],
                        fill=(40, 8, 12), outline=RED, width=1)
        draw.text((RCOL_X + 8, ry + 4), "◆ リスク", font=f_lbl, fill=RED)
        ry += 36

        # リスク本文（"▲リスク：" プレフィックスを除去して表示）
        risk_raw = (seg.get("risk", "")
                    .replace("▲リスク【最緊急】：", "")
                    .replace("▲リスク：", ""))
        for rl in textwrap.wrap(risk_raw, 22):
            draw.text((RCOL_X + 4, ry), rl, font=f_txt, fill=(255, 145, 145))
            ry += 28
        ry += 14

        # ── 右カラム：背景 ────────────────────────────
        draw.line([(RCOL_X, ry), (W - 12, ry)], fill=(45, 45, 85), width=1)
        ry += 12

        draw.rectangle([(RCOL_X, ry), (W - 12, ry + 28)],
                        fill=(10, 12, 36), outline=(80, 90, 140), width=1)
        draw.text((RCOL_X + 8, ry + 4), "◆ 背景", font=f_lbl, fill=(160, 175, 230))
        ry += 36

        ctx_raw = seg.get("context", "").replace("背景：", "")
        for cl in textwrap.wrap(ctx_raw, 22):
            draw.text((RCOL_X + 4, ry), cl, font=f_txt, fill=(150, 158, 210))
            ry += 28

    # フッター
    draw.rectangle([(0, H - 22), (W, H)], fill=(6, 6, 20))
    draw.text((16, H - 17),
              "ソース: NHK・産経・日経・CNBC・FT・BBC・NYT・Reuters・Al Jazeera ほか",
              font=get_font(10), fill=DIM)

    return np.array(img)


# ── gTTS 音声生成 ─────────────────────────────────────────────────────────────
def make_audio(text, path):
    from gtts import gTTS
    tts = gTTS(text=text, lang="ja", slow=False)
    tts.save(str(path))
    time.sleep(0.8)


def speed_audio(src, dst, factor):
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_exe = "ffmpeg"
    result = subprocess.run(
        [ffmpeg_exe, "-y", "-i", str(src),
         "-filter:a", f"atempo={factor}", str(dst)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg atempo error:\n{result.stderr}")


def audio_duration(path):
    try:
        from moviepy import AudioFileClip
        clip = AudioFileClip(str(path))
        d = clip.duration
        clip.close()
        return d
    except Exception:
        return 10.0


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

    print("=" * 60)
    print("World News 動画生成を開始します")
    print(f"音声速度: {SPEED}x")
    print(f"出力先: {OUTPUT}")
    print("=" * 60)

    clips = []
    for i, seg in enumerate(SEGMENTS):
        label = seg["badge"]
        print(f"\n[{i+1}/{len(SEGMENTS)}] {label}")

        mp3_raw  = TMPDIR / f"nar_{i:02d}_raw.mp3"
        mp3_fast = TMPDIR / f"nar_{i:02d}_fast.mp3"

        if not mp3_fast.exists():
            if not mp3_raw.exists():
                print("  → 音声生成中 (gTTS)...")
                make_audio(seg["narration"], mp3_raw)
            if SPEED != 1.0:
                print(f"  → {SPEED}倍速に変換中 (ffmpeg)...")
                speed_audio(mp3_raw, mp3_fast, SPEED)
            else:
                import shutil
                shutil.copy(mp3_raw, mp3_fast)
        else:
            print("  → 音声キャッシュ使用")

        audio_dur = audio_duration(mp3_fast)
        slide_dur = max(audio_dur + 0.6, 4.0)
        print(f"  → スライド長: {slide_dur:.1f}秒 (音声: {audio_dur:.1f}秒)")

        frame = make_frame(seg)

        # スライド画像を files/ に保存
        from PIL import Image
        slide_name = f"slide_{i:02d}_{seg['badge'].replace('/', '-')}.png"
        Image.fromarray(frame).save(str(FILES_DIR / slide_name))
        print(f"  → スライド保存: files/{slide_name}")

        img_clip   = ImageClip(frame).with_duration(slide_dur)
        audio_clip = AudioFileClip(str(mp3_fast))
        clip       = img_clip.with_audio(audio_clip)
        clips.append(clip)

    total = sum(c.duration for c in clips)
    print(f"\n合計尺: {total:.1f}秒 ({total/60:.1f}分)")
    print("動画を書き出し中...")

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(TMPDIR / "tmp_audio.m4a"),
        remove_temp=True,
        logger="bar",
    )

    for f in TMPDIR.glob("nar_*.mp3"):
        f.unlink(missing_ok=True)

    # 原稿テキストを files/ に保存
    script_path = FILES_DIR / "script_20260516.txt"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("World News 2026年5月16日　放送原稿\n")
        f.write("=" * 60 + "\n\n")
        for i, seg in enumerate(SEGMENTS):
            f.write(f"【{seg['badge']}】\n")
            if not seg["cover"]:
                f.write(f"タイトル: {seg['title']}\n")
                f.write(f"サブタイトル: {seg['subtitle']}\n")
                f.write("箇条書き:\n")
                for b in seg["bullets"]:
                    f.write(f"  ● {b}\n")
                if seg.get("risk"):
                    f.write(f"リスク: {seg['risk']}\n")
                if seg.get("context"):
                    f.write(f"背景: {seg['context']}\n")
            f.write(f"ナレーション:\n  {seg['narration']}\n\n")
    print(f"[完了] 原稿保存: {script_path}")

    print(f"\n[完了] 動画: {OUTPUT}")
    print(f"   総尺: {total:.0f}秒 ({total/60:.1f}分)")
    print(f"[完了] スライド画像: {FILES_DIR} ({len(SEGMENTS)}枚)")
    print(f"[完了] 原稿: {script_path}")


if __name__ == "__main__":
    main()
