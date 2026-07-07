"""
ピッツバーグハゼ箱 展開図 生成スクリプト  Step 1/4
底板90x130mm、高さ40mm、板厚0.5mm
パーツ：底板1枚(フランジ付) + 長辺側板2枚 + 短辺側板2枚
コーナー：溶接なし（隙間あり）
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import warnings
warnings.filterwarnings('ignore')

for font in ['MS Gothic', 'Meiryo', 'Yu Gothic', 'BIZ UDGothic', 'TakaoPGothic', 'DejaVu Sans']:
    try:
        matplotlib.rcParams['font.family'] = font
        fig_test = plt.figure()
        plt.text(0, 0, 'テスト')
        plt.close(fig_test)
        print(f"Using font: {font}")
        break
    except:
        plt.close('all')
        continue

matplotlib.rcParams['axes.unicode_minus'] = False

# ════════════════════════════════════════════
#  基本寸法
# ════════════════════════════════════════════
W  = 90    # 底板 幅（短辺）mm
L  = 130   # 底板 長さ（長辺）mm
H  = 40    # 側面 高さ mm
T  = 0.5   # 板厚 mm

# ── ピッツバーグハゼ寸法 ──
# 底板側：立ち上がりフランジ（オス/クリップ）
F   = 12   # フランジ高さ mm
BA  = 1    # 曲げ代（90°、板厚0.5mm） mm

# 側板側：ピッツバーグポケット（メス、3回折り）
P1  = 4    # ポケット外脚 mm（カシメ端）
P2  = 14   # ポケット屋根 mm（フランジ幅を包む）
P3  = 12   # ポケット内脚 mm（≒フランジ高さ）
# 側板底辺のポケット折り代合計
POCKET_FLAT = P1 + BA + P2 + BA + P3 + BA  # = 33mm

# 安全ヘム（側板上端）
HEM = 5    # ヘム幅 mm

# ── ブランク寸法計算 ──
BF       = F + BA            # 底板片側の展開量 = 13mm（フランジ12mm + 曲げ代1mm）
BW_blank = W + BF * 2       # 底板ブランク幅  = 90 + 26 = 116mm
BL_blank = L + BF * 2       # 底板ブランク長  = 130 + 26 = 156mm
NOTCH    = BF                # コーナー切り欠き辺長 = 13mm

# 長辺側板ブランク（×2）
LONG_W  = L                              # 130mm
LONG_H  = POCKET_FLAT + H + HEM + BA    # 33+40+5+1 = 79mm

# 短辺側板ブランク（×2）
SHORT_W = W                              # 90mm
SHORT_H = LONG_H                         # 79mm（同じ）

print("=" * 55)
print(f"底板内寸    : {W} × {L} mm  板厚 {T}mm")
print(f"側面高さ    : {H} mm")
print(f"底板ブランク: {BW_blank} × {BL_blank} mm")
print(f"  コーナー切り欠き: {NOTCH} × {NOTCH} mm × 4隅")
print(f"長辺側板    : {LONG_W} × {LONG_H} mm  ×2枚")
print(f"短辺側板    : {SHORT_W} × {SHORT_H} mm  ×2枚")
print(f"ポケット折り代: {POCKET_FLAT}mm  "
      f"（外脚{P1}+曲{BA}+屋根{P2}+曲{BA}+内脚{P3}+曲{BA}）")
print("=" * 55)

# ── ヘルパー関数 ──
def dim_arrow(ax, x1, y1, x2, y2, text, side='bottom', fontsize=8.5, color='#333333'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    mx, my = (x1+x2)/2, (y1+y2)/2
    if x1 == x2:
        ax.text(mx+4, my, text, ha='left', va='center', fontsize=fontsize, color=color)
    else:
        dy = -6 if side == 'bottom' else 6
        ax.text(mx, my+dy, text, ha='center',
                va='top' if side == 'bottom' else 'bottom', fontsize=fontsize, color=color)

def fold_line(ax, x1, y1, x2, y2, color='#0066CC', ls='--', lw=1.2):
    ax.plot([x1, x2], [y1, y2], linestyle=ls, color=color, lw=lw, zorder=4)

CLR_MAIN = '#0066CC'   # 青：主折り曲げ線
CLR_BEND = '#E65100'   # 橙：ハゼ構造折り線
CLR_CUT  = '#B71C1C'   # 赤：切り取り部

# ════════════════════════════════════════════
#  図1：底板 展開図
# ════════════════════════════════════════════
fig1, ax = plt.subplots(figsize=(9, 8))
OX, OY = 65, 55
sc = 1.4   # 表示スケール（mm→画面座標）

ax.set_xlim(-35, OX + BW_blank*sc + 90)
ax.set_ylim(-65, OY + BL_blank*sc + 80)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    '【図1】底板 展開図   内寸 90×130mm  板厚 0.5mm\n'
    'フランジ 12mm（4辺）— 90°立ち上げてポケットに差し込む（オス側）',
    fontsize=11, fontweight='bold', pad=12)

def T1(x, y): return OX + x*sc, OY + y*sc

# ── 底板エリア（内側）──
ax.add_patch(patches.Rectangle(
    T1(BF, BF), W*sc, L*sc,
    edgecolor='#2E7D32', facecolor='#C8E6C9', lw=2, zorder=3))
ax.text(*T1(BF + W/2, BF + L/2),
        f'底板\n{W} × {L} mm',
        ha='center', va='center', fontsize=12, fontweight='bold', color='#2E7D32', zorder=5)

# ── フランジエリア（4辺）──
FC = '#BBDEFB'
EC_F = '#1565C0'

def draw_flange(rx, ry, rw, rh, label):
    ax.add_patch(patches.Rectangle(
        T1(rx, ry), rw*sc, rh*sc,
        edgecolor=EC_F, facecolor=FC, lw=1.5, zorder=3))
    ax.text(*T1(rx + rw/2, ry + rh/2), label,
            ha='center', va='center', fontsize=8, color=EC_F, fontweight='bold', zorder=5)

draw_flange(BF, 0,       W,  F,  f'フランジ\n{F}mm')   # 下（手前）
draw_flange(BF, BF+L,    W,  F,  f'フランジ\n{F}mm')   # 上（奥）
draw_flange(0,  BF,      F,  L,  f'フ\nラ\nン\nジ\n{F}mm')  # 左
draw_flange(BF+W, BF,    F,  L,  f'フ\nラ\nン\nジ\n{F}mm')  # 右

# ── コーナー切り欠き（4隅）──
for cx, cy in [(0, 0), (BF+W, 0), (0, BF+L), (BF+W, BF+L)]:
    ax.add_patch(patches.Rectangle(
        T1(cx, cy), BF*sc, BF*sc,
        edgecolor=CLR_CUT, facecolor='#FFCDD2', lw=1.5, linestyle='--',
        alpha=0.85, zorder=6))
    ax.text(*T1(cx + BF/2, cy + BF/2),
            f'✂\n{NOTCH}×{NOTCH}',
            ha='center', va='center', fontsize=6, color=CLR_CUT, fontweight='bold', zorder=7)

# ── 外形輪郭（切り欠き後の正しい輪郭）──
outline = [
    T1(BF,        0),           # 下辺 左端
    T1(BF+W,      0),           # 下辺 右端
    T1(BF+W,      BF),          # 右下コーナー内折
    T1(BW_blank,  BF),          # 右辺 下端
    T1(BW_blank,  BF+L),        # 右辺 上端
    T1(BF+W,      BF+L),        # 右上コーナー内折
    T1(BF+W,      BL_blank),    # 上辺 右端
    T1(BF,        BL_blank),    # 上辺 左端
    T1(BF,        BF+L),        # 左上コーナー内折
    T1(0,         BF+L),        # 左辺 上端
    T1(0,         BF),          # 左辺 下端
    T1(BF,        BF),          # 左下コーナー内折
    T1(BF,        0),           # 閉じる
]
ax.plot([p[0] for p in outline], [p[1] for p in outline],
        color='#333333', lw=2.5, zorder=8)

# ── フランジ先端 V字切り込み（半幅 NW=5mm、深さ=F=12mm） ──
NW = 5  # V字切り込み半幅 mm

def flange_vnotch(tri_pts, cut_line):
    ax.add_patch(patches.Polygon(tri_pts, closed=True,
                                  facecolor='white', edgecolor=CLR_CUT, lw=1.5, zorder=9))
    ax.plot([cut_line[0][0], cut_line[1][0]],
            [cut_line[0][1], cut_line[1][1]],
            color=CLR_CUT, lw=1.8, zorder=10)
    # 切り込み幅ラベル（切断線の中点）
    mx = (cut_line[0][0] + cut_line[1][0]) / 2
    my = (cut_line[0][1] + cut_line[1][1]) / 2
    ax.text(mx, my, f'{NW}mm', ha='center', va='center', fontsize=6,
            color=CLR_CUT, fontweight='bold', zorder=11,
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.8))

# 底フランジ（y: 0→F、自由端=y0、折り線=yBF）
# 左端（半V：右半分）
flange_vnotch([T1(BF, 0), T1(BF+NW, 0), T1(BF, F)],
              [T1(BF+NW, 0), T1(BF, F)])
# 右端（半V：左半分）
flange_vnotch([T1(BF+W-NW, 0), T1(BF+W, 0), T1(BF+W, F)],
              [T1(BF+W-NW, 0), T1(BF+W, F)])

# 上フランジ（y: BF+L→BL_blank、自由端=yBL_blank）
# 左端
flange_vnotch([T1(BF, BL_blank), T1(BF+NW, BL_blank), T1(BF, BF+L)],
              [T1(BF+NW, BL_blank), T1(BF, BF+L)])
# 右端
flange_vnotch([T1(BF+W-NW, BL_blank), T1(BF+W, BL_blank), T1(BF+W, BF+L)],
              [T1(BF+W-NW, BL_blank), T1(BF+W, BF+L)])

# 左フランジ（x: 0→BF、自由端=x0）
# 下端（半V：上半分）
flange_vnotch([T1(0, BF), T1(0, BF+NW), T1(BF, BF)],
              [T1(0, BF+NW), T1(BF, BF)])
# 上端（半V：下半分）
flange_vnotch([T1(0, BF+L-NW), T1(0, BF+L), T1(BF, BF+L)],
              [T1(0, BF+L-NW), T1(BF, BF+L)])

# 右フランジ（x: BF+W→BW_blank、自由端=xBW_blank）
# 下端
flange_vnotch([T1(BW_blank, BF), T1(BW_blank, BF+NW), T1(BF+W, BF)],
              [T1(BW_blank, BF+NW), T1(BF+W, BF)])
# 上端
flange_vnotch([T1(BW_blank, BF+L-NW), T1(BW_blank, BF+L), T1(BF+W, BF+L)],
              [T1(BW_blank, BF+L-NW), T1(BF+W, BF+L)])

# ── 折り曲げ線（4辺のフランジ境界）──
for x in [BF, BF+W]:
    fold_line(ax, *T1(x, BF), *T1(x, BF+L), color=CLR_MAIN)
for y in [BF, BF+L]:
    fold_line(ax, *T1(BF, y), *T1(BF+W, y), color=CLR_MAIN)

# ── 山折り / 谷折り ラベル ──
# 底板フランジ4辺はすべて「山折り」
# （外面（底面）を上にして置き、フランジを内側へ折り上げる方向）
mk = dict(fontsize=8, color=CLR_MAIN, fontweight='bold', zorder=10,
          bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                    edgecolor=CLR_MAIN, alpha=0.95, lw=0.8))

# 下横折り線（y=BF）
ax.text(*T1(BF + W*0.5, BF), '▲ 山折り', ha='center', va='center', **mk)
# 上横折り線（y=BF+L）
ax.text(*T1(BF + W*0.5, BF+L), '▲ 山折り', ha='center', va='center', **mk)
# 左縦折り線（x=BF）
ax.text(*T1(BF, BF + L*0.5), '▲ 山折り', ha='center', va='center', rotation=90, **mk)
# 右縦折り線（x=BF+W）
ax.text(*T1(BF+W, BF + L*0.5), '▲ 山折り', ha='center', va='center', rotation=90, **mk)

# ── 寸法線 ──
off = 16
# 横（下側）
dim_arrow(ax, *T1(BF, -off/sc), *T1(BF+W, -off/sc), f'{W}mm', 'bottom', 8.5, '#2E7D32')
dim_arrow(ax, *T1(0,  -off*2.2/sc), *T1(BW_blank, -off*2.2/sc),
          f'全幅 {BW_blank}mm', 'bottom', 9, '#333')
# 縦（右側）
ox = BW_blank + 8
dim_arrow(ax, *T1(ox, 0),    *T1(ox, BF),       f'{BF}mm', 'bottom', 7.5, EC_F)
dim_arrow(ax, *T1(ox, BF),   *T1(ox, BF+L),     f'{L}mm',  'bottom', 9,   '#2E7D32')
dim_arrow(ax, *T1(ox, BF+L), *T1(ox, BL_blank), f'{BF}mm', 'bottom', 7.5, EC_F)
dim_arrow(ax, *T1(ox+22/sc, 0), *T1(ox+22/sc, BL_blank),
          f'全長 {BL_blank}mm', 'bottom', 9, '#333')
# フランジ幅注釈（左辺）
dim_arrow(ax, *T1(-8/sc, BF), *T1(-8/sc, BF+L), f'{L}mm', 'bottom', 8, '#2E7D32')

# ── 凡例 ──
LX = OX
LY = OY - 30
legends = [
    ('#C8E6C9', '#2E7D32', f'底板  {W}×{L}mm（内寸）'),
    (FC,        EC_F,      f'フランジ  F={F}mm、曲げ代{BA}mm含む → 4辺を90°内側へ折り上げる'),
    ('#FFCDD2', CLR_CUT,   f'切り欠き  {NOTCH}×{NOTCH}mm × 4隅（切り取る）'),
]
for i, (fc, ec, lbl) in enumerate(legends):
    ax.add_patch(patches.Rectangle((LX, LY - i*17), 18, 11, facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(LX+23, LY+5.5 - i*17, lbl, fontsize=8.5, va='center', color='#333')

# 折り曲げ線凡例
ax.plot([LX, LX+18], [LY+5.5 - len(legends)*17]*2, ls='--', color=CLR_MAIN, lw=1.5)
ax.text(LX+23, LY+5.5 - len(legends)*17,
        '90°折り曲げ線（フランジ根元）', fontsize=8.5, va='center', color='#333')

# 板厚注記
ax.text(OX + BW_blank*sc + 85, OY - 28,
        f'板厚: {T}mm', ha='right', va='top', fontsize=9, color='#5D4037',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1', edgecolor='#F57F17', lw=1.2))

plt.savefig('pitts_01_bottomplate.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("pitts_01_bottomplate.png  完了")

# ════════════════════════════════════════════
#  図2：長辺側板 展開図（×2枚）
# ════════════════════════════════════════════
fig2, ax = plt.subplots(figsize=(10, 8))
OX2, OY2 = 70, 55
sc2 = 1.4

ax.set_xlim(-45, OX2 + LONG_W*sc2 + 110)
ax.set_ylim(-30, OY2 + LONG_H*sc2 + 75)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【図2】長辺側板 展開図（×2枚）  ブランク {LONG_W}×{LONG_H}mm  板厚 {T}mm\n'
    f'底部：ピッツバーグポケット {POCKET_FLAT}mm（3回折り）  上端：安全ヘム {HEM}mm',
    fontsize=11, fontweight='bold', pad=12)

def T2(x, y): return OX2 + x*sc2, OY2 + y*sc2

# ── ゾーン境界 y 座標 ──
z_ba1_top  = P1 + BA           # 15
z_p2_top   = P1 + BA + P2     # 19
z_ba2_top  = P1 + BA + P2 + BA        # 20
z_p3_top   = P1 + BA + P2 + BA + P3   # 32
z_wall_bot = POCKET_FLAT               # 33
z_wall_top = POCKET_FLAT + H           # 73
z_hem_bot  = z_wall_top + BA           # 74
z_hem_top  = LONG_H                    # 79

POCKET_CLR = '#FF8A65'
WALL_CLR   = '#BBDEFB'
HEM_CLR    = '#E0E0E0'
BA_CLR     = '#FFF9C4'

def draw_zone(rx, ry, rw, rh, fc, ec, label, lsize=9, lcolor='#333'):
    ax.add_patch(patches.Rectangle(
        T2(rx, ry), rw*sc2, rh*sc2,
        edgecolor=ec, facecolor=fc, lw=1.2, zorder=3))
    if label:
        ax.text(*T2(rx + rw/2, ry + rh/2), label,
                ha='center', va='center', fontsize=lsize,
                color=lcolor, fontweight='bold', zorder=5)

# P1（外脚）
draw_zone(0, 0,          LONG_W, P1,   POCKET_CLR, '#BF360C',
          f'ポケット外脚  P1={P1}mm\n（フランジの外側を包む）', 8.5, 'white')
# BA1
draw_zone(0, P1,         LONG_W, BA,   BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# P2（屋根）
draw_zone(0, z_ba1_top,  LONG_W, P2,   POCKET_CLR, '#BF360C',
          f'屋根  P2={P2}mm', 7.5, 'white')
# BA2
draw_zone(0, z_p2_top,   LONG_W, BA,   BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# P3（内脚）
draw_zone(0, z_ba2_top,  LONG_W, P3,   POCKET_CLR, '#BF360C',
          f'ポケット内脚  P3={P3}mm\n（フランジの内側に沿う）', 8, 'white')
# BA3（ポケット→壁）
draw_zone(0, z_p3_top,   LONG_W, BA,   BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# 壁
draw_zone(0, z_wall_bot, LONG_W, H,    WALL_CLR, '#1565C0',
          f'側板壁\n{LONG_W} × {H}mm', 12, '#1565C0')
# BA4（壁→ヘム）
draw_zone(0, z_wall_top, LONG_W, BA,   BA_CLR, '#F9A825', '', 6, '#795548')
# ヘム
draw_zone(0, z_hem_bot,  LONG_W, HEM,  HEM_CLR, '#616161',
          f'安全ヘム {HEM}mm', 8.5, '#333')

# 外形線
ax.add_patch(patches.Rectangle(
    T2(0, 0), LONG_W*sc2, LONG_H*sc2,
    edgecolor='#333', facecolor='none', lw=2.5, zorder=7))

# 折り線
fold_data = [
    (P1,         CLR_BEND, '-.'),   # P1→BA1
    (z_ba1_top,  CLR_BEND, '-.'),   # BA1→P2
    (z_p2_top,   CLR_BEND, '-.'),   # P2→BA2
    (z_ba2_top,  CLR_BEND, '-.'),   # BA2→P3
    (z_p3_top,   CLR_BEND, '-.'),   # P3→BA3
    (z_wall_bot, CLR_MAIN, '--'),   # 主折り（ポケット→壁）
    (z_wall_top, CLR_MAIN, '--'),   # ヘム折り
]
for y, clr, ls in fold_data:
    fold_line(ax, *T2(0, y), *T2(LONG_W, y), color=clr, ls=ls)

# ── 山折り / 谷折り ラベル ──
# 基準：内面（箱の内側になる面）を上にして作業
# ▲ 山折り = 折り目が内面側に盛り上がる
# ▽ 谷折り = 折り目が外面側（作業台側）に向かう
fold_dir = [
    # (y座標,  ラベル,         文字色,    背景枠色)
    (P1,         '▽ 谷折り', '#BF360C', '#BF360C'),  # y=14 P1外脚：谷折り
    (z_p2_top,   '▽ 谷折り', '#BF360C', '#BF360C'),  # y=19 P2屋根：谷折り
    (z_wall_bot, '▲ 山折り', CLR_MAIN,  CLR_MAIN),   # y=33 ポケット主折り：山折り
    (z_wall_top, '▽ 谷折り', CLR_MAIN,  CLR_MAIN),   # y=73 ヘム：谷折り
]
for y, label, txt_clr, box_clr in fold_dir:
    ax.text(*T2(LONG_W * 0.5, y), label,
            ha='center', va='center',
            fontsize=8, color=txt_clr, fontweight='bold', zorder=10,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=box_clr, alpha=0.95, lw=0.8))

# 凡例注記（折り方向の基準説明）
ax.text(OX2, OY2 + LONG_H*sc2 + 10,
        '※ 折り方向の基準：内面（箱の内側になる面）を上にして置いた状態',
        fontsize=8, color='#555', style='italic')

# 寸法線（右側）
ox2r = LONG_W + 8
for y0, y1, lbl, clr in [
    (0,          P1,         f'P1={P1}',   '#BF360C'),
    (z_ba1_top,  z_p2_top,   f'P2={P2}',   '#BF360C'),
    (z_ba2_top,  z_p3_top,   f'P3={P3}',   '#BF360C'),
    (z_wall_bot, z_wall_top, f'H={H}',     '#1565C0'),
    (z_hem_bot,  z_hem_top,  f'HEM={HEM}', '#616161'),
]:
    dim_arrow(ax, *T2(ox2r, y0), *T2(ox2r, y1), f'{lbl}mm', 'bottom', 8, clr)

dim_arrow(ax, *T2(-12/sc2, 0), *T2(-12/sc2, LONG_H),
          f'全高 {LONG_H}mm', 'bottom', 9, '#333')
dim_arrow(ax, *T2(0, -10/sc2), *T2(LONG_W, -10/sc2),
          f'全幅 {LONG_W}mm', 'bottom', 9, '#333')

# 凡例
L2X = OX2
L2Y = OY2 - 25
leg2 = [
    (POCKET_CLR, '#BF360C', f'ピッツバーグポケット部  計 {POCKET_FLAT}mm（3回折り）'),
    (WALL_CLR,   '#1565C0', f'側板壁  {H}mm'),
    (HEM_CLR,    '#616161', f'安全ヘム  {HEM}mm（上端を折り返す：怪我防止）'),
    (BA_CLR,     '#F9A825', f'曲げ代  各 {BA}mm × 4か所'),
]
for i, (fc, ec, lbl) in enumerate(leg2):
    ax.add_patch(patches.Rectangle((L2X, L2Y - i*16), 16, 10, facecolor=fc, edgecolor=ec, lw=1))
    ax.text(L2X+20, L2Y+5 - i*16, lbl, fontsize=8.5, va='center', color='#333')

ax.plot([L2X, L2X+16], [L2Y+5 - len(leg2)*16]*2, ls='--', color=CLR_MAIN, lw=1.5)
ax.text(L2X+20, L2Y+5 - len(leg2)*16,
        '主折り曲げ線（ポケット→壁 / 壁→ヘム）', fontsize=8.5, va='center', color='#333')
ax.plot([L2X, L2X+16], [L2Y+5 - (len(leg2)+1)*16]*2, ls='-.', color=CLR_BEND, lw=1.5)
ax.text(L2X+20, L2Y+5 - (len(leg2)+1)*16,
        'ポケット内折り線（3本）', fontsize=8.5, va='center', color='#333')

plt.savefig('pitts_02_longpanel.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("pitts_02_longpanel.png  完了")

# ════════════════════════════════════════════
#  図3：短辺側板 展開図（×2枚）
# ════════════════════════════════════════════
fig3, ax = plt.subplots(figsize=(8, 8))
OX3, OY3 = 70, 55
sc3 = 1.4

ax.set_xlim(-45, OX3 + SHORT_W*sc3 + 110)
ax.set_ylim(-30, OY3 + SHORT_H*sc3 + 75)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【図3】短辺側板 展開図（×2枚）  ブランク {SHORT_W}×{SHORT_H}mm  板厚 {T}mm\n'
    f'底部：ピッツバーグポケット {POCKET_FLAT}mm（3回折り）  上端：安全ヘム {HEM}mm',
    fontsize=11, fontweight='bold', pad=12)

def T3(x, y): return OX3 + x*sc3, OY3 + y*sc3

def draw_zone(rx, ry, rw, rh, fc, ec, label, lsize=9, lcolor='#333'):
    ax.add_patch(patches.Rectangle(
        T3(rx, ry), rw*sc3, rh*sc3,
        edgecolor=ec, facecolor=fc, lw=1.2, zorder=3))
    if label:
        ax.text(*T3(rx + rw/2, ry + rh/2), label,
                ha='center', va='center', fontsize=lsize,
                color=lcolor, fontweight='bold', zorder=5)

# P1（外脚）
draw_zone(0, 0,          SHORT_W, P1,  POCKET_CLR, '#BF360C',
          f'ポケット外脚  P1={P1}mm\n（フランジの外側を包む）', 8.5, 'white')
# BA1
draw_zone(0, P1,         SHORT_W, BA,  BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# P2（屋根）
draw_zone(0, z_ba1_top,  SHORT_W, P2,  POCKET_CLR, '#BF360C',
          f'屋根  P2={P2}mm', 7.5, 'white')
# BA2
draw_zone(0, z_p2_top,   SHORT_W, BA,  BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# P3（内脚）
draw_zone(0, z_ba2_top,  SHORT_W, P3,  POCKET_CLR, '#BF360C',
          f'ポケット内脚  P3={P3}mm\n（フランジの内側に沿う）', 8, 'white')
# BA3（ポケット→壁）
draw_zone(0, z_p3_top,   SHORT_W, BA,  BA_CLR, '#F9A825', f'曲げ代{BA}', 6, '#795548')
# 壁
draw_zone(0, z_wall_bot, SHORT_W, H,   WALL_CLR, '#1565C0',
          f'側板壁\n{SHORT_W} × {H}mm', 12, '#1565C0')
# BA4（壁→ヘム）
draw_zone(0, z_wall_top, SHORT_W, BA,  BA_CLR, '#F9A825', '', 6, '#795548')
# ヘム
draw_zone(0, z_hem_bot,  SHORT_W, HEM, HEM_CLR, '#616161',
          f'安全ヘム {HEM}mm', 8.5, '#333')

# 外形線
ax.add_patch(patches.Rectangle(
    T3(0, 0), SHORT_W*sc3, SHORT_H*sc3,
    edgecolor='#333', facecolor='none', lw=2.5, zorder=7))

# 折り線
for y, clr, ls in [
    (P1,         CLR_BEND, '-.'),
    (z_ba1_top,  CLR_BEND, '-.'),
    (z_p2_top,   CLR_BEND, '-.'),
    (z_ba2_top,  CLR_BEND, '-.'),
    (z_p3_top,   CLR_BEND, '-.'),
    (z_wall_bot, CLR_MAIN, '--'),
    (z_wall_top, CLR_MAIN, '--'),
]:
    fold_line(ax, *T3(0, y), *T3(SHORT_W, y), color=clr, ls=ls)

# 山折り / 谷折り ラベル
fold_dir3 = [
    (P1,         '▽ 谷折り', '#BF360C', '#BF360C'),
    (z_p2_top,   '▽ 谷折り', '#BF360C', '#BF360C'),
    (z_wall_bot, '▲ 山折り', CLR_MAIN,  CLR_MAIN),
    (z_wall_top, '▽ 谷折り', CLR_MAIN,  CLR_MAIN),
]
for y, label, txt_clr, box_clr in fold_dir3:
    ax.text(*T3(SHORT_W * 0.5, y), label,
            ha='center', va='center',
            fontsize=8, color=txt_clr, fontweight='bold', zorder=10,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=box_clr, alpha=0.95, lw=0.8))

# 凡例注記
ax.text(OX3, OY3 + SHORT_H*sc3 + 10,
        '※ 折り方向の基準：内面（箱の内側になる面）を上にして置いた状態',
        fontsize=8, color='#555', style='italic')

# 寸法線（右側）
ox3r = SHORT_W + 8
for y0, y1, lbl, clr in [
    (0,          P1,         f'P1={P1}',   '#BF360C'),
    (z_ba1_top,  z_p2_top,   f'P2={P2}',   '#BF360C'),
    (z_ba2_top,  z_p3_top,   f'P3={P3}',   '#BF360C'),
    (z_wall_bot, z_wall_top, f'H={H}',     '#1565C0'),
    (z_hem_bot,  z_hem_top,  f'HEM={HEM}', '#616161'),
]:
    dim_arrow(ax, *T3(ox3r, y0), *T3(ox3r, y1), f'{lbl}mm', 'bottom', 8, clr)

dim_arrow(ax, *T3(-12/sc3, 0), *T3(-12/sc3, SHORT_H),
          f'全高 {SHORT_H}mm', 'bottom', 9, '#333')
dim_arrow(ax, *T3(0, -10/sc3), *T3(SHORT_W, -10/sc3),
          f'全幅 {SHORT_W}mm', 'bottom', 9, '#333')

# 凡例
L3X = OX3
L3Y = OY3 - 25
leg3 = [
    (POCKET_CLR, '#BF360C', f'ピッツバーグポケット部  計 {POCKET_FLAT}mm（3回折り）'),
    (WALL_CLR,   '#1565C0', f'側板壁  {H}mm'),
    (HEM_CLR,    '#616161', f'安全ヘム  {HEM}mm（上端を折り返す：怪我防止）'),
    (BA_CLR,     '#F9A825', f'曲げ代  各 {BA}mm × 4か所'),
]
for i, (fc, ec, lbl) in enumerate(leg3):
    ax.add_patch(patches.Rectangle((L3X, L3Y - i*16), 16, 10, facecolor=fc, edgecolor=ec, lw=1))
    ax.text(L3X+20, L3Y+5 - i*16, lbl, fontsize=8.5, va='center', color='#333')

ax.plot([L3X, L3X+16], [L3Y+5 - len(leg3)*16]*2, ls='--', color=CLR_MAIN, lw=1.5)
ax.text(L3X+20, L3Y+5 - len(leg3)*16,
        '主折り曲げ線（ポケット→壁 / 壁→ヘム）', fontsize=8.5, va='center', color='#333')
ax.plot([L3X, L3X+16], [L3Y+5 - (len(leg3)+1)*16]*2, ls='-.', color=CLR_BEND, lw=1.5)
ax.text(L3X+20, L3Y+5 - (len(leg3)+1)*16,
        'ポケット内折り線（3本）', fontsize=8.5, va='center', color='#333')

plt.savefig('pitts_03_shortpanel.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("pitts_03_shortpanel.png  完了")

print("Step 3 完了 ─ 図1（底板）＋ 図2（長辺側板）＋ 図3（短辺側板）出力")

# ════════════════════════════════════════════
#  図4：4面連続展開図（長辺-短辺-長辺-短辺 1枚取り）
# ════════════════════════════════════════════
BA_C = BA   # コーナー折り代 1mm

# x 座標（左端基点）
x_L1_st  = 0
x_L1_en  = LONG_W                              # 130
x_C1_en  = x_L1_en + BA_C                     # 131
x_S1_en  = x_C1_en + SHORT_W                  # 221
x_C2_en  = x_S1_en + BA_C                     # 222
x_L2_en  = x_C2_en + LONG_W                   # 352
x_C3_en  = x_L2_en + BA_C                     # 353
x_S2_en  = x_C3_en + SHORT_W                  # 443
STRIP_W  = x_S2_en                            # 443mm
STRIP_H  = SHORT_H                             # 79mm

fig4, ax = plt.subplots(figsize=(17, 5))
sc4 = 0.88
OX4, OY4 = 75, 65

ax.set_xlim(-80, OX4 + STRIP_W*sc4 + 110)
ax.set_ylim(-50, OY4 + STRIP_H*sc4 + 95)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【図4】4面連続展開図（長辺-短辺-長辺-短辺、1枚取り）  板厚 {T}mm\n'
    f'ストリップ全幅 {STRIP_W}mm × 全高 {STRIP_H}mm\n'
    f'長辺{LONG_W}×2 + 短辺{SHORT_W}×2 + コーナー折り代{BA_C}mm×3',
    fontsize=10.5, fontweight='bold', pad=12)

def T4(x, y): return OX4 + x*sc4, OY4 + y*sc4

def draw_zone4(rx, ry, rw, rh, fc, ec, label='', lsize=8, lcolor='#333'):
    ax.add_patch(patches.Rectangle(
        T4(rx, ry), rw*sc4, rh*sc4,
        edgecolor=ec, facecolor=fc, lw=0.9, zorder=3))
    if label:
        ax.text(*T4(rx + rw/2, ry + rh/2), label,
                ha='center', va='center', fontsize=lsize,
                color=lcolor, fontweight='bold', zorder=5)

# ── 水平ゾーン帯（全幅） ──
for y0, rh, fc, ec in [
    (0,          P1,  POCKET_CLR, '#BF360C'),
    (P1,         BA,  BA_CLR,     '#F9A825'),
    (z_ba1_top,  P2,  POCKET_CLR, '#BF360C'),
    (z_p2_top,   BA,  BA_CLR,     '#F9A825'),
    (z_ba2_top,  P3,  POCKET_CLR, '#BF360C'),
    (z_p3_top,   BA,  BA_CLR,     '#F9A825'),
    (z_wall_bot, H,   WALL_CLR,   '#1565C0'),
    (z_wall_top, BA,  BA_CLR,     '#F9A825'),
    (z_hem_bot,  HEM, HEM_CLR,    '#616161'),
]:
    draw_zone4(0, y0, STRIP_W, rh, fc, ec)

# ── コーナー折り代ゾーン（薄紫でハイライト、全高） ──
CORNER_CLR = '#EDE7F6'
for cx in [x_L1_en, x_S1_en, x_L2_en]:
    draw_zone4(cx, 0, BA_C, STRIP_H, CORNER_CLR, '#5C6BC0')

# ── コーナーV字切り込み（底辺、鋭角V字） ──
NOTCH_D = z_wall_bot   # 切り込み深さ = 33mm（主折り線まで）
NOTCH_W = 8            # 切り込み半幅 = 8mm（頂角≈27°）

for cx_start in [x_L1_en, x_S1_en, x_L2_en]:
    cx = cx_start + BA_C / 2
    tri = [T4(cx - NOTCH_W, 0), T4(cx + NOTCH_W, 0), T4(cx, NOTCH_D)]
    ax.add_patch(patches.Polygon(tri, closed=True,
                                  facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
    ax.plot([T4(cx - NOTCH_W, 0)[0], T4(cx, NOTCH_D)[0]],
            [T4(cx - NOTCH_W, 0)[1], T4(cx, NOTCH_D)[1]],
            color=CLR_CUT, lw=2.0, zorder=10)
    ax.plot([T4(cx + NOTCH_W, 0)[0], T4(cx, NOTCH_D)[0]],
            [T4(cx + NOTCH_W, 0)[1], T4(cx, NOTCH_D)[1]],
            color=CLR_CUT, lw=2.0, zorder=10)
    dim_arrow(ax, *T4(cx, 0), *T4(cx, NOTCH_D),
              f'{NOTCH_D}mm', 'bottom', 7, CLR_CUT)
    dim_arrow(ax, *T4(cx, -8/sc4), *T4(cx + NOTCH_W, -8/sc4),
              f'{NOTCH_W}mm', 'bottom', 7, CLR_CUT)
    ax.text(*T4(cx, NOTCH_D * 0.35), '切り込み\n（V字）',
            ha='center', va='center', fontsize=6.5,
            color=CLR_CUT, fontweight='bold', zorder=11)

# ── 両端の半V字切り込み（4隅目） ──
# 左端
tri_left = [T4(0, 0), T4(NOTCH_W, 0), T4(0, NOTCH_D)]
ax.add_patch(patches.Polygon(tri_left, closed=True,
                              facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
ax.plot([T4(NOTCH_W, 0)[0], T4(0, NOTCH_D)[0]],
        [T4(NOTCH_W, 0)[1], T4(0, NOTCH_D)[1]],
        color=CLR_CUT, lw=2.0, zorder=10)
dim_arrow(ax, *T4(0, -8/sc4), *T4(NOTCH_W, -8/sc4),
          f'{NOTCH_W}mm', 'bottom', 7, CLR_CUT)
ax.text(*T4(NOTCH_W * 0.25, NOTCH_D * 0.35), '半\nV字',
        ha='center', va='center', fontsize=6.5,
        color=CLR_CUT, fontweight='bold', zorder=11)

# 右端
tri_right = [T4(STRIP_W - NOTCH_W, 0), T4(STRIP_W, 0), T4(STRIP_W, NOTCH_D)]
ax.add_patch(patches.Polygon(tri_right, closed=True,
                              facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
ax.plot([T4(STRIP_W - NOTCH_W, 0)[0], T4(STRIP_W, NOTCH_D)[0]],
        [T4(STRIP_W - NOTCH_W, 0)[1], T4(STRIP_W, NOTCH_D)[1]],
        color=CLR_CUT, lw=2.0, zorder=10)
dim_arrow(ax, *T4(STRIP_W - NOTCH_W, -8/sc4), *T4(STRIP_W, -8/sc4),
          f'{NOTCH_W}mm', 'bottom', 7, CLR_CUT)
ax.text(*T4(STRIP_W - NOTCH_W * 0.25, NOTCH_D * 0.35), '半\nV字',
        ha='center', va='center', fontsize=6.5,
        color=CLR_CUT, fontweight='bold', zorder=11)

# ── 上辺V字切り込み（ヘム折り用、深さ=HEM=5mm） ──
NOTCH_T = HEM   # 5mm：ヘム幅分だけ切り込む（鋭角V字）

# 内部3コーナー（上辺から下向きV字）
for cx_start in [x_L1_en, x_S1_en, x_L2_en]:
    cx = cx_start + BA_C / 2
    tri_top = [T4(cx - NOTCH_T, STRIP_H),
               T4(cx + NOTCH_T, STRIP_H),
               T4(cx, STRIP_H - NOTCH_T)]
    ax.add_patch(patches.Polygon(tri_top, closed=True,
                                  facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
    ax.plot([T4(cx - NOTCH_T, STRIP_H)[0], T4(cx, STRIP_H - NOTCH_T)[0]],
            [T4(cx - NOTCH_T, STRIP_H)[1], T4(cx, STRIP_H - NOTCH_T)[1]],
            color=CLR_CUT, lw=2.0, zorder=10)
    ax.plot([T4(cx + NOTCH_T, STRIP_H)[0], T4(cx, STRIP_H - NOTCH_T)[0]],
            [T4(cx + NOTCH_T, STRIP_H)[1], T4(cx, STRIP_H - NOTCH_T)[1]],
            color=CLR_CUT, lw=2.0, zorder=10)

# 左端（上辺・半V字）
tri_top_left = [T4(0, STRIP_H), T4(NOTCH_T, STRIP_H), T4(0, STRIP_H - NOTCH_T)]
ax.add_patch(patches.Polygon(tri_top_left, closed=True,
                              facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
ax.plot([T4(NOTCH_T, STRIP_H)[0], T4(0, STRIP_H - NOTCH_T)[0]],
        [T4(NOTCH_T, STRIP_H)[1], T4(0, STRIP_H - NOTCH_T)[1]],
        color=CLR_CUT, lw=2.0, zorder=10)

# 右端（上辺・半V字）
tri_top_right = [T4(STRIP_W - NOTCH_T, STRIP_H),
                 T4(STRIP_W, STRIP_H),
                 T4(STRIP_W, STRIP_H - NOTCH_T)]
ax.add_patch(patches.Polygon(tri_top_right, closed=True,
                              facecolor='white', edgecolor=CLR_CUT, lw=2.0, zorder=9))
ax.plot([T4(STRIP_W - NOTCH_T, STRIP_H)[0], T4(STRIP_W, STRIP_H - NOTCH_T)[0]],
        [T4(STRIP_W - NOTCH_T, STRIP_H)[1], T4(STRIP_W, STRIP_H - NOTCH_T)[1]],
        color=CLR_CUT, lw=2.0, zorder=10)

# ── 外形線 ──
ax.add_patch(patches.Rectangle(
    T4(0, 0), STRIP_W*sc4, STRIP_H*sc4,
    edgecolor='#222', facecolor='none', lw=2.2, zorder=8))

# ── 水平折り線 ──
for y, clr, ls in [
    (P1,         CLR_BEND, '-.'),
    (z_ba1_top,  CLR_BEND, '-.'),
    (z_p2_top,   CLR_BEND, '-.'),
    (z_ba2_top,  CLR_BEND, '-.'),
    (z_p3_top,   CLR_BEND, '-.'),
    (z_wall_bot, CLR_MAIN, '--'),
    (z_wall_top, CLR_MAIN, '--'),
]:
    fold_line(ax, *T4(0, y), *T4(STRIP_W, y), color=clr, ls=ls)

# ── 垂直コーナー折り線（BA帯の両端） ──
for cx in [x_L1_en, x_C1_en, x_S1_en, x_C2_en, x_L2_en, x_C3_en]:
    ax.plot([T4(cx, 0)[0], T4(cx, STRIP_H)[0]],
            [T4(cx, 0)[1], T4(cx, STRIP_H)[1]],
            color='#5C6BC0', lw=1.2, ls='--', zorder=6)

# ── 山折り/谷折りラベル（水平） ──
for y, label, txt_clr, box_clr in [
    (P1,         '▽ 谷折り', '#BF360C', '#BF360C'),
    (z_p2_top,   '▽ 谷折り', '#BF360C', '#BF360C'),
    (z_wall_bot, '▲ 山折り', CLR_MAIN,  CLR_MAIN),
    (z_wall_top, '▽ 谷折り', CLR_MAIN,  CLR_MAIN),
]:
    ax.text(*T4(STRIP_W * 0.5, y), label,
            ha='center', va='center',
            fontsize=7.5, color=txt_clr, fontweight='bold', zorder=10,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=box_clr, alpha=0.95, lw=0.8))

# ── パネルラベル（壁ゾーン内） ──
for name, x_st, pw, clr in [
    ('長辺①\n130mm', x_L1_st,  LONG_W,  '#1565C0'),
    ('短辺①\n 90mm', x_C1_en, SHORT_W, '#E65100'),
    ('長辺②\n130mm', x_C2_en,  LONG_W,  '#1565C0'),
    ('短辺②\n 90mm', x_C3_en, SHORT_W, '#E65100'),
]:
    ax.text(*T4(x_st + pw/2, z_wall_bot + H/2), name,
            ha='center', va='center', fontsize=9.5,
            color=clr, fontweight='bold', zorder=6)

# ── コーナーラベル（帯中央上） ──
for i, cx in enumerate([x_L1_en, x_S1_en, x_L2_en], 1):
    ax.text(*T4(cx + BA_C/2, STRIP_H + 3/sc4),
            f'C{i}', ha='center', va='bottom',
            fontsize=8, color='#5C6BC0', fontweight='bold')

# ── 寸法線（上部 各パネル幅） ──
DY = STRIP_H + 10/sc4
for x0, x1, lbl, clr in [
    (x_L1_st, x_L1_en, f'{LONG_W}mm',  '#1565C0'),
    (x_C1_en, x_S1_en, f'{SHORT_W}mm', '#E65100'),
    (x_C2_en, x_L2_en, f'{LONG_W}mm',  '#1565C0'),
    (x_C3_en, x_S2_en, f'{SHORT_W}mm', '#E65100'),
]:
    dim_arrow(ax, *T4(x0, DY), *T4(x1, DY), lbl, 'bottom', 8, clr)

# 全幅寸法
dim_arrow(ax, *T4(0, STRIP_H + 26/sc4), *T4(STRIP_W, STRIP_H + 26/sc4),
          f'全幅 {STRIP_W}mm', 'bottom', 9.5, '#333')

# 全高寸法（左側）
dim_arrow(ax, *T4(-18/sc4, 0), *T4(-18/sc4, STRIP_H),
          f'全高 {STRIP_H}mm', 'bottom', 9, '#333')

# 右端寸法（ポケット・壁・ヘム）
rx4 = STRIP_W + 8
for y0, y1, lbl, clr in [
    (0,          P1,         f'P1={P1}',   '#BF360C'),
    (z_ba1_top,  z_p2_top,   f'P2={P2}',  '#BF360C'),
    (z_ba2_top,  z_p3_top,   f'P3={P3}',  '#BF360C'),
    (z_wall_bot, z_wall_top, f'H={H}',    '#1565C0'),
    (z_hem_bot,  STRIP_H,    f'HEM={HEM}','#616161'),
]:
    dim_arrow(ax, *T4(rx4, y0), *T4(rx4, y1), f'{lbl}mm', 'bottom', 7.5, clr)

# ── 接合部マーク（両端） ──
seam_kw = dict(fontsize=8, color='#C62828',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE',
                         edgecolor='#C62828', lw=1))
ax.text(*T4(STRIP_W + 3/sc4, STRIP_H/2), '→ 接合部\n（4隅目）',
        ha='left', va='center', **seam_kw)
ax.text(*T4(-3/sc4, STRIP_H/2), '接合部 ←\n（4隅目）',
        ha='right', va='center', **seam_kw)

# ── 注記 ──
ax.text(OX4, OY4 - 38,
        f'【折り手順】 ① 底部ポケット折り（4本・水平）→ ② コーナー折り C1・C2・C3（3本・垂直 各90°内折り）→ ③ ヘム折り（水平）\n'
        f'【接合部】 左右端（C4隅）をリベット・両面テープ等で固定\n'
        f'【V字切り込み（赤）】 各コーナーで深さ{z_wall_bot}mm・底辺{NOTCH_W*2}mmの三角形を切り取る → 折り時の重なりを防ぎ直角コーナーを形成',
        fontsize=7.5, color='#444', style='italic')

plt.savefig('pitts_04_4panels.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("pitts_04_4panels.png  完了")

print("Step 4 完了 ─ 図1-4 すべて出力")
