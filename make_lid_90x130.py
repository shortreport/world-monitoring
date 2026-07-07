"""
蓋 天面 展開図
内寸 W94×L134×H20mm  板厚0.5mm
底面（pitts_01）と同じ構造：天面＋4辺フランジ
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import warnings
warnings.filterwarnings('ignore')

for font in ['MS Gothic', 'Meiryo', 'Yu Gothic', 'BIZ UDGothic', 'TakaoPGothic', 'DejaVu Sans']:
    try:
        matplotlib.rcParams['font.family'] = font
        fig_test = plt.figure(); plt.text(0, 0, 'テスト'); plt.close(fig_test)
        print(f"Using font: {font}"); break
    except:
        plt.close('all'); continue

matplotlib.rcParams['axes.unicode_minus'] = False

# ════════════════════════════════════════════
#  基本寸法
# ════════════════════════════════════════════
W  = 93     # 蓋天面 内寸 幅（短辺）mm
L  = 133    # 蓋天面 内寸 長さ（長辺）mm
H  = 10     # 蓋壁高さ mm（フランジ高さ）
T  = 0.5    # 板厚 mm
BA = 1      # 曲げ代 mm
BF = H + BA # フランジ込み展開幅 = 21mm

BW_blank = BF + W + BF   # ブランク全幅 = 21+94+21 = 136mm
BL_blank = BF + L + BF   # ブランク全長 = 21+134+21 = 176mm

print("=" * 55)
print(f"蓋天面内寸  : W{W} × L{L} × H{H} mm  板厚 {T}mm")
print(f"フランジ展開: {H}mm + BA{BA}mm = BF{BF}mm")
print(f"ブランク全幅: {BW_blank}mm")
print(f"ブランク全長: {BL_blank}mm")
print(f"コーナー切り欠き: {BF}×{BF}mm × 4箇所")
print("=" * 55)

# ── 色 ──
CLR_MAIN = '#0066CC'
CLR_CUT  = '#B71C1C'
CLR_TOP  = '#C8E6C9'   # 天面：緑
CLR_FL   = '#BBDEFB'   # フランジ：青

# ── ヘルパー ──
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

def fold_line(ax, x1, y1, x2, y2, color=CLR_MAIN, ls='--', lw=1.2):
    ax.plot([x1, x2], [y1, y2], linestyle=ls, color=color, lw=lw, zorder=4)

# ════════════════════════════════════════════
#  図：蓋 天面 展開図
# ════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 9))
sc = 1.4
OX, OY = 65, 55

def T1(x, y): return OX + x*sc, OY + y*sc

ax.set_xlim(-20, OX + BW_blank*sc + 130)
ax.set_ylim(-50, OY + BL_blank*sc + 110)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【蓋 天面 展開図】  内寸 W{W}×L{L}×H{H}mm  板厚 {T}mm\n'
    f'フランジ {H}mm（▲山折り）  曲げ代 {BA}mm  BF={BF}mm',
    fontsize=12, fontweight='bold', pad=14)

# ── 天面（緑） ──
ax.add_patch(patches.Rectangle(
    T1(BF, BF), W*sc, L*sc,
    edgecolor='#2E7D32', facecolor=CLR_TOP, lw=1.5, zorder=3))
ax.text(*T1(BF + W/2, BF + L/2), f'蓋 天面\n{W}×{L}mm',
        ha='center', va='center', fontsize=13, color='#2E7D32',
        fontweight='bold', zorder=5)

# ── 4辺フランジ（青） ──
def draw_flange(rx, ry, rw, rh):
    ax.add_patch(patches.Rectangle(
        T1(rx, ry), rw*sc, rh*sc,
        edgecolor='#1565C0', facecolor=CLR_FL, lw=1.2, zorder=3))

draw_flange(BF, 0,      W,  H)    # 前面フランジ（下）
draw_flange(BF, BF+L,   W,  H)    # 後面フランジ（上）
draw_flange(0,  BF,     H,  L)    # 左フランジ
draw_flange(BF+W, BF,   H,  L)    # 右フランジ

# フランジラベル
ax.text(*T1(BF + W/2, H/2),        f'フランジ {H}mm', ha='center', va='center', fontsize=8, color='#1565C0', zorder=5)
ax.text(*T1(BF + W/2, BF+L+H/2),   f'フランジ {H}mm', ha='center', va='center', fontsize=8, color='#1565C0', zorder=5)
ax.text(*T1(H/2,      BF + L/2),    f'フランジ\n{H}mm', ha='center', va='center', fontsize=8, color='#1565C0', zorder=5)
ax.text(*T1(BF+W+H/2, BF + L/2),   f'フランジ\n{H}mm', ha='center', va='center', fontsize=8, color='#1565C0', zorder=5)

# ── コーナー切り欠き（BF×BF = 21×21mm） ──
for cx, cy in [(0, 0), (BF+W, 0), (0, BF+L), (BF+W, BF+L)]:
    ax.add_patch(patches.Rectangle(
        T1(cx, cy), BF*sc, BF*sc,
        edgecolor=CLR_CUT, facecolor='white', lw=1.5, zorder=6))
    ax.add_patch(patches.Rectangle(
        T1(cx, cy), BF*sc, BF*sc,
        hatch='////', facecolor='none', edgecolor=CLR_CUT,
        lw=0.5, alpha=0.6, zorder=7))

# コーナー寸法注記（左下のみ）
ax.text(*T1(BF/2, BF/2), f'{BF}×{BF}\n切り欠き',
        ha='center', va='center', fontsize=6.5, color=CLR_CUT, zorder=8,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))

# ── 外形輪郭 ──
outline = [
    T1(BF, 0), T1(BF+W, 0),
    T1(BF+W, BF), T1(BW_blank, BF),
    T1(BW_blank, BF+L), T1(BF+W, BF+L),
    T1(BF+W, BL_blank), T1(BF, BL_blank),
    T1(BF, BF+L), T1(0, BF+L),
    T1(0, BF), T1(BF, BF),
    T1(BF, 0),
]
ax.plot([p[0] for p in outline], [p[1] for p in outline],
        color='#222', lw=2.0, zorder=8)

# ── 折り曲げ線（天面とフランジの境界） ──
for x in [BF, BF+W]:
    fold_line(ax, *T1(x, BF), *T1(x, BF+L))
for y in [BF, BF+L]:
    fold_line(ax, *T1(BF, y), *T1(BF+W, y))

# ── フランジ先端 V字切り込み（半幅 NW=5mm、深さ=H=12mm） ──
NW = 5

def flange_vnotch(tri_pts, cut_line):
    ax.add_patch(patches.Polygon(tri_pts, closed=True,
                                  facecolor='white', edgecolor=CLR_CUT, lw=1.5, zorder=9))
    ax.plot([cut_line[0][0], cut_line[1][0]],
            [cut_line[0][1], cut_line[1][1]],
            color=CLR_CUT, lw=1.8, zorder=10)
    mx = (cut_line[0][0] + cut_line[1][0]) / 2
    my = (cut_line[0][1] + cut_line[1][1]) / 2
    ax.text(mx, my, f'{NW}mm', ha='center', va='center', fontsize=6,
            color=CLR_CUT, fontweight='bold', zorder=11,
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.8))

# 前面フランジ（y:0→H、自由端=y0）
flange_vnotch([T1(BF, 0), T1(BF+NW, 0), T1(BF, H)],
              [T1(BF+NW, 0), T1(BF, H)])
flange_vnotch([T1(BF+W-NW, 0), T1(BF+W, 0), T1(BF+W, H)],
              [T1(BF+W-NW, 0), T1(BF+W, H)])
# 後面フランジ（y:BF+L→BL_blank、自由端=BL_blank）
flange_vnotch([T1(BF, BL_blank), T1(BF+NW, BL_blank), T1(BF, BF+L)],
              [T1(BF+NW, BL_blank), T1(BF, BF+L)])
flange_vnotch([T1(BF+W-NW, BL_blank), T1(BF+W, BL_blank), T1(BF+W, BF+L)],
              [T1(BF+W-NW, BL_blank), T1(BF+W, BF+L)])
# 左フランジ（x:0→BF、自由端=x0）
flange_vnotch([T1(0, BF), T1(0, BF+NW), T1(BF, BF)],
              [T1(0, BF+NW), T1(BF, BF)])
flange_vnotch([T1(0, BF+L-NW), T1(0, BF+L), T1(BF, BF+L)],
              [T1(0, BF+L-NW), T1(BF, BF+L)])
# 右フランジ（x:BF+W→BW_blank、自由端=BW_blank）
flange_vnotch([T1(BW_blank, BF), T1(BW_blank, BF+NW), T1(BF+W, BF)],
              [T1(BW_blank, BF+NW), T1(BF+W, BF)])
flange_vnotch([T1(BW_blank, BF+L-NW), T1(BW_blank, BF+L), T1(BF+W, BF+L)],
              [T1(BW_blank, BF+L-NW), T1(BF+W, BF+L)])

# ── 折り方向ラベル（▲山折り × 4辺） ──
mk = dict(fontsize=8, fontweight='bold', zorder=10,
          bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, lw=0.8))

ax.text(*T1(BF + W/2, BF),      '▲ 山折り', ha='center', va='center', color=CLR_MAIN, **mk)
ax.text(*T1(BF + W/2, BF+L),    '▲ 山折り', ha='center', va='center', color=CLR_MAIN, **mk)
ax.text(*T1(BF,       BF + L/2), '▲ 山折り', ha='center', va='center', color=CLR_MAIN, rotation=90, **mk)
ax.text(*T1(BF+W,     BF + L/2), '▲ 山折り', ha='center', va='center', color=CLR_MAIN, rotation=90, **mk)

# ── 寸法線 ──
DY_TOP = BL_blank + 10
dim_arrow(ax, *T1(BF,   DY_TOP), *T1(BF+W, DY_TOP), f'W={W}mm', 'top', 9.5, '#2E7D32')
dim_arrow(ax, *T1(0,    DY_top := DY_TOP+18), *T1(BW_blank, DY_top),
          f'全幅 {BW_blank}mm', 'top', 9.5, '#333')

DX_R = BW_blank + 9
dim_arrow(ax, *T1(DX_R, BF),    *T1(DX_R, BF+L),    f'L={L}mm', 'bottom', 9.5, '#2E7D32')
dim_arrow(ax, *T1(DX_R+18, 0),  *T1(DX_R+18, BL_blank),
          f'全長 {BL_blank}mm', 'bottom', 9.5, '#333')

# フランジ幅寸法
dim_arrow(ax, *T1(0, BF/2), *T1(BF, BF/2), f'BF={BF}mm', 'top', 8, '#1565C0')
dim_arrow(ax, *T1(0, BF + L/2 - 3), *T1(0, BF + L/2 + H),
          f'{H}mm', 'bottom', 8, '#1565C0')

# ── 凡例 ──
LX = OX
LY = OY - 38
leg = [
    (CLR_TOP,  '#2E7D32', f'蓋 天面  {W}×{L}mm'),
    (CLR_FL,   '#1565C0', f'フランジ  {H}mm（▲山折り）× 4辺'),
    ('white',  CLR_CUT,   f'コーナー切り欠き  {BF}×{BF}mm × 4箇所'),
]
for i, (fc, ec, lbl) in enumerate(leg):
    ax.add_patch(patches.Rectangle((LX, LY - i*16), 16, 10,
                                    facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(LX+21, LY+5 - i*16, lbl, fontsize=8.5, va='center', color='#333')

ax.plot([LX, LX+16], [LY+5 - len(leg)*16]*2, ls='--', color=CLR_MAIN, lw=1.5)
ax.text(LX+21, LY+5 - len(leg)*16, '▲ 山折り（フランジ折り曲げ線）', fontsize=8.5, va='center', color='#333')

# 板厚注記
ax.text(OX + BW_blank*sc + 125, OY - 28,
        f'板厚: {T}mm', ha='right', va='top', fontsize=9, color='#5D4037',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                  edgecolor='#F57F17', lw=1.2))

plt.savefig('lid_01_topplate.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("lid_01_topplate.png  完了")

# ════════════════════════════════════════════
#  図2：蓋 側面4連展開図（pitts_04準拠）
# ════════════════════════════════════════════
# ── 側面パラメータ ──
P1 = 4;  P2 = 12;  P3 = 10   # ポケット寸法（蓋用：P2=12, P3=10）
HEM    = 5                     # ヘム mm
H_WALL = 20                    # 蓋壁高さ mm
BA_C   = BA                    # コーナー曲げ代 1mm

POCKET_FLAT = P1+BA+P2+BA+P3+BA   # = 33mm

# y座標（y=0: ポケット外端、下方向に増加）
y_p1      = P1                      # 4
y_ba1     = P1 + BA                 # 5
y_p2      = P1 + BA + P2            # 19
y_ba2     = P1 + BA + P2 + BA       # 20
y_p3      = P1 + BA + P2 + BA + P3  # 32
y_wbot    = POCKET_FLAT              # 33  壁上端（主折り線）
y_wtop    = y_wbot + H_WALL          # 53  壁下端
y_hembot  = y_wtop + BA              # 54  ヘム折り線
y_hemtop  = y_hembot + HEM           # 59  自由端

STRIP_H = y_hemtop   # 59mm

# x座標（パネル境界）
LONG_W  = L    # 134mm
SHORT_W = W    # 94mm

x_L1_en = LONG_W                              # 134
x_C1_en = x_L1_en + BA_C                     # 135
x_S1_en = x_C1_en + SHORT_W                  # 229
x_C2_en = x_S1_en + BA_C                     # 230
x_L2_en = x_C2_en + LONG_W                   # 364
x_C3_en = x_L2_en + BA_C                     # 365
x_S2_en = x_C3_en + SHORT_W                  # 459

STRIP_W = x_S2_en   # 459mm

print(f"蓋側面ストリップ: {STRIP_W}mm × {STRIP_H}mm")
print(f"  L(長辺)={LONG_W}mm × 2 + S(短辺)={SHORT_W}mm × 2 + BA×3")
print(f"  ポケット={POCKET_FLAT}mm + 壁={H_WALL}mm + BA + ヘム={HEM}mm = {STRIP_H}mm")

# ── 色（pitts_04準拠） ──
C_P1   = '#FF8A65'; C_P2 = '#FFCC80'; C_P3 = '#FFF176'
C_WALL = '#B3E5FC'; C_HEM = '#E1BEE7'; C_BA = '#CFD8DC'
C_LONG = '#E8F5E9'; C_SHORT = '#FFF3E0'; C_CORNER = '#EDE7F6'

fig4, ax = plt.subplots(figsize=(17, 5))
sc4 = 0.88
OX4, OY4 = 75, 65

def T4(x, y): return OX4 + x*sc4, OY4 + y*sc4

ax.set_xlim(-20, OX4 + STRIP_W*sc4 + 130)
ax.set_ylim(-55, OY4 + STRIP_H*sc4 + 100)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【蓋 側面4連展開図】  '
    f'L(長辺){LONG_W}mm × S(短辺){SHORT_W}mm  壁高{H_WALL}mm  板厚{T}mm\n'
    f'ポケット={POCKET_FLAT}mm（P1={P1}+BA+P2={P2}+BA+P3={P3}+BA）'
    f'  ヘム={HEM}mm  全幅={STRIP_W}mm',
    fontsize=10, fontweight='bold', pad=12)

def draw_zone4(rx, ry, rw, rh, fc, ec, label='', lsize=8, lcolor='#333'):
    ax.add_patch(patches.Rectangle(
        T4(rx, ry), rw*sc4, rh*sc4,
        edgecolor=ec, facecolor=fc, lw=1.0, zorder=3))
    if label:
        ax.text(*T4(rx+rw/2, ry+rh/2), label,
                ha='center', va='center', fontsize=lsize,
                color=lcolor, fontweight='bold', zorder=5)

# ── ゾーン描画（左から L1 → C1 → S1 → C2 → L2 → C3 → S2） ──
for x_st, x_en, color, name in [
    (0,       x_L1_en, C_LONG,   f'長辺壁\n{LONG_W}mm'),
    (x_C1_en, x_S1_en, C_SHORT,  f'短辺壁\n{SHORT_W}mm'),
    (x_C2_en, x_L2_en, C_LONG,   f'長辺壁\n{LONG_W}mm'),
    (x_C3_en, x_S2_en, C_SHORT,  f'短辺壁\n{SHORT_W}mm'),
]:
    w = x_en - x_st
    draw_zone4(x_st, y_wbot,  w, H_WALL, color, '#555', name, 8.5, '#333')
    draw_zone4(x_st, 0,       w, P1,     C_P1,  '#BF360C', f'P1={P1}', 7, 'white')
    draw_zone4(x_st, y_p1,    w, BA,     C_BA,  '#607D8B', '', 6, '#333')
    draw_zone4(x_st, y_ba1,   w, P2,     C_P2,  '#E65100', f'P2={P2}', 7.5, '#5D4037')
    draw_zone4(x_st, y_p2,    w, BA,     C_BA,  '#607D8B', '', 6, '#333')
    draw_zone4(x_st, y_ba2,   w, P3,     C_P3,  '#F9A825', f'P3={P3}', 7, '#5D4037')
    draw_zone4(x_st, y_p3,    w, BA,     C_BA,  '#607D8B', '', 6, '#333')
    draw_zone4(x_st, y_wtop,  w, BA,     C_BA,  '#607D8B', '', 6, '#333')
    draw_zone4(x_st, y_hembot,w, HEM,    C_HEM, '#7B1FA2', f'ヘム{HEM}', 7, '#4A148C')

# コーナーBA帯
for x_st, x_en in [(x_L1_en, x_C1_en), (x_S1_en, x_C2_en), (x_L2_en, x_C3_en)]:
    draw_zone4(x_st, 0, BA_C, STRIP_H, C_CORNER, '#7E57C2', '', 5)

# ── 外形輪郭 ──
ax.plot([T4(0,0)[0], T4(STRIP_W,0)[0]], [T4(0,0)[1], T4(STRIP_W,0)[1]],
        color='#222', lw=2.0, zorder=8)
ax.plot([T4(0,STRIP_H)[0], T4(STRIP_W,STRIP_H)[0]],
        [T4(0,STRIP_H)[1], T4(STRIP_W,STRIP_H)[1]], color='#222', lw=2.0, zorder=8)
ax.plot([T4(0,0)[0], T4(0,STRIP_H)[0]], [T4(0,0)[1], T4(0,STRIP_H)[1]],
        color='#222', lw=2.0, zorder=8)
ax.plot([T4(STRIP_W,0)[0], T4(STRIP_W,STRIP_H)[0]],
        [T4(STRIP_W,0)[1], T4(STRIP_W,STRIP_H)[1]], color='#222', lw=2.0, zorder=8)

# ── 折り曲げ線 ──
def fold4(y, color=CLR_MAIN, ls='--'):
    ax.plot([T4(0,y)[0], T4(STRIP_W,y)[0]], [T4(0,y)[1], T4(STRIP_W,y)[1]],
            ls=ls, color=color, lw=1.2, zorder=4)

fold4(y_p1,    CLR_CUT,  '-.')   # P1折り（谷折り①）
fold4(y_p2,    CLR_CUT,  '-.')   # P2折り（谷折り②）
fold4(y_wbot,  CLR_MAIN, '--')   # 主折り（山折り）
fold4(y_wtop,  CLR_MAIN, '--')   # ヘム折り（谷折り）
fold4(y_hembot,CLR_MAIN, '--')   # ヘム折り

# コーナー折り線（垂直）
for x in [x_L1_en, x_C1_en, x_S1_en, x_C2_en, x_L2_en, x_C3_en]:
    ax.plot([T4(x,0)[0], T4(x,STRIP_H)[0]], [T4(x,0)[1], T4(x,STRIP_H)[1]],
            ls='--', color='#7E57C2', lw=1.0, zorder=4)

# ── 折り方向ラベル ──
fold_labels = [
    (P1/2,      '▽ 谷折り', CLR_CUT),    # P1
    (y_ba1+P2/2,'▽ 谷折り', CLR_CUT),    # P2
    (y_wbot,    '▲ 山折り', CLR_MAIN),   # 主折り
    (y_wtop,    '▽ 谷折り', CLR_MAIN),   # 壁/ヘム
]
mk4 = dict(fontsize=7, fontweight='bold', zorder=10,
           bbox=dict(boxstyle='round,pad=0.15', facecolor='white', alpha=0.9, lw=0.5))
for y, lbl, clr in fold_labels:
    ax.text(*T4(STRIP_W/2, y), lbl, ha='center', va='center', color=clr, **mk4)

# ── V字切り込み（底辺・頂辺） ──
NOTCH_D = POCKET_FLAT   # 33mm（ポケット深さまで）
NOTCH_W = 8             # 半幅 8mm

def add_vnotch(cx, top=False):
    """底辺(top=False)または頂辺(top=True)にV字を追加"""
    if top:
        y_base, y_apex = STRIP_H, STRIP_H - HEM
        tri = [T4(cx-NOTCH_W, y_base), T4(cx+NOTCH_W, y_base), T4(cx, y_apex)]
    else:
        y_base, y_apex = 0, NOTCH_D
        tri = [T4(cx-NOTCH_W, y_base), T4(cx+NOTCH_W, y_base), T4(cx, y_apex)]
    ax.add_patch(patches.Polygon(tri, closed=True,
                                  facecolor='white', edgecolor=CLR_CUT, lw=1.8, zorder=9))

# 底辺：内部3コーナー
for cx in [x_L1_en + BA_C/2, x_S1_en + BA_C/2, x_L2_en + BA_C/2]:
    add_vnotch(cx, top=False)
    # 寸法
    ax.text(*T4(cx, NOTCH_D/2), f'{NOTCH_D}×\n{NOTCH_W*2}mm',
            ha='center', va='center', fontsize=5.5, color=CLR_CUT, zorder=11)
# 底辺：左右端（半V）
ax.add_patch(patches.Polygon(
    [T4(0,0), T4(NOTCH_W,0), T4(0,NOTCH_D)],
    closed=True, facecolor='white', edgecolor=CLR_CUT, lw=1.8, zorder=9))
ax.add_patch(patches.Polygon(
    [T4(STRIP_W-NOTCH_W,0), T4(STRIP_W,0), T4(STRIP_W,NOTCH_D)],
    closed=True, facecolor='white', edgecolor=CLR_CUT, lw=1.8, zorder=9))

# 頂辺（ヘム）：内部3コーナー＋左右端
for cx in [x_L1_en + BA_C/2, x_S1_en + BA_C/2, x_L2_en + BA_C/2]:
    add_vnotch(cx, top=True)
ax.add_patch(patches.Polygon(
    [T4(0,STRIP_H), T4(HEM,STRIP_H), T4(0,STRIP_H-HEM)],
    closed=True, facecolor='white', edgecolor=CLR_CUT, lw=1.5, zorder=9))
ax.add_patch(patches.Polygon(
    [T4(STRIP_W-HEM,STRIP_H), T4(STRIP_W,STRIP_H), T4(STRIP_W,STRIP_H-HEM)],
    closed=True, facecolor='white', edgecolor=CLR_CUT, lw=1.5, zorder=9))

# ── 寸法線 ──
DY4 = -12
dim_arrow(ax, *T4(0, DY4),        *T4(x_L1_en, DY4), f'L={LONG_W}mm', 'bottom', 7.5, '#2E7D32')
dim_arrow(ax, *T4(x_C1_en, DY4),  *T4(x_S1_en, DY4), f'S={SHORT_W}mm','bottom', 7.5, '#E65100')
dim_arrow(ax, *T4(x_C2_en, DY4),  *T4(x_L2_en, DY4), f'L={LONG_W}mm', 'bottom', 7.5, '#2E7D32')
dim_arrow(ax, *T4(x_C3_en, DY4),  *T4(x_S2_en, DY4), f'S={SHORT_W}mm','bottom', 7.5, '#E65100')
dim_arrow(ax, *T4(0, DY4-14),     *T4(STRIP_W, DY4-14), f'全幅 {STRIP_W}mm', 'bottom', 8.5, '#333')

DX4_R = STRIP_W + 8
dim_arrow(ax, *T4(DX4_R, 0),       *T4(DX4_R, y_wbot),   f'{POCKET_FLAT}mm', 'bottom', 7, '#E65100')
dim_arrow(ax, *T4(DX4_R, y_wbot),  *T4(DX4_R, y_wtop),   f'壁{H_WALL}mm',    'bottom', 7, '#1565C0')
dim_arrow(ax, *T4(DX4_R, y_wtop),  *T4(DX4_R, STRIP_H),  f'{BA+HEM}mm',      'bottom', 7, '#7B1FA2')
dim_arrow(ax, *T4(DX4_R+18, 0),    *T4(DX4_R+18, STRIP_H),f'全高 {STRIP_H}mm','bottom', 8.5, '#333')

# ── 凡例 ──
LX4 = OX4
LY4 = OY4 - 40
items4 = [
    (C_P1,  '#BF360C', f'P1={P1}mm（カシメ端・外脚）'),
    (C_P2,  '#E65100', f'P2={P2}mm（屋根）'),
    (C_P3,  '#F9A825', f'P3={P3}mm（内脚）= 蓋フランジ {H}mm + BA'),
    (C_WALL,'#1565C0', f'壁 {H_WALL}mm'),
    (C_HEM, '#7B1FA2', f'ヘム {HEM}mm'),
    (C_CORNER,'#7E57C2',f'コーナーBA {BA_C}mm（▽谷折り）'),
]
for i, (fc, ec, lbl) in enumerate(items4):
    ax.add_patch(patches.Rectangle((LX4, LY4 - i*14), 14, 9, facecolor=fc, edgecolor=ec, lw=1.0))
    ax.text(LX4+18, LY4+4.5 - i*14, lbl, fontsize=7.5, va='center', color='#333')

ax.text(OX4 + STRIP_W*sc4 + 125, OY4 - 28,
        f'板厚: {T}mm', ha='right', va='top', fontsize=9, color='#5D4037',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1', edgecolor='#F57F17', lw=1.2))

plt.savefig('lid_02_4panels.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("lid_02_4panels.png  完了")
