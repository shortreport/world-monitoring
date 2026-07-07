"""
板取り図（ネスティング）
455×455mm 板 1枚から4部品を切り出す配置図
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
#  部品寸法
# ════════════════════════════════════════════
SHEET_W = 455
SHEET_H = 455
GAP = 2   # 部品間隔 mm

# pitts_01: 箱 底面展開図  (BF=13, W=90, L=130)
P01_W = 13 + 90 + 13   # 116mm
P01_H = 13 + 130 + 13  # 156mm

# pitts_04: 箱 側面4連展開図
P04_W = 443   # 130+1+90+1+130+1+90
P04_H = 79    # POCKET(33)+壁(40)+BA+HEM(5)

# lid_01: 蓋 天面展開図  (BF=11, W=93, L=133)
L01_W = 11 + 93 + 11   # 115mm
L01_H = 11 + 133 + 11  # 155mm

# lid_02: 蓋 側面4連展開図
L02_W = 133+1+93+1+133+1+93  # 455mm
L02_H = 55    # POCKET(29)+壁(20)+BA+HEM(5)

# ── 配置座標（左下原点、y上方向） ──
# Row1: pitts_04（上）
p04_x, p04_y = 0, SHEET_H - P04_H
# Row2: lid_02（Row1の下）
l02_x, l02_y = 0, p04_y - GAP - L02_H
# Row3a: pitts_01（左下）
p01_x, p01_y = 0, l02_y - GAP - P01_H
# Row3b: lid_01（pitts_01の右）
l01_x, l01_y = P01_W + GAP, l02_y - GAP - L01_H

print("=" * 55)
print(f"板サイズ     : {SHEET_W} × {SHEET_H} mm")
print(f"pitts_01 配置: ({p01_x},{p01_y}) {P01_W}×{P01_H}mm")
print(f"pitts_04 配置: ({p04_x},{p04_y}) {P04_W}×{P04_H}mm")
print(f"lid_01   配置: ({l01_x},{l01_y}) {L01_W}×{L01_H}mm")
print(f"lid_02   配置: ({l02_x},{l02_y}) {L02_W}×{L02_H}mm")

# 干渉チェック
max_x = max(p04_x+P04_W, l02_x+L02_W, p01_x+P01_W, l01_x+L01_W)
min_y = min(p04_y, l02_y, p01_y, l01_y)
print(f"使用範囲     : X={max_x}mm / Y最小={min_y}mm (下端 板底面から{min_y}mm)")
area_parts = P01_W*P01_H + P04_W*P04_H + L01_W*L01_H + L02_W*L02_H
area_sheet = SHEET_W * SHEET_H
print(f"材料利用率   : {area_parts/area_sheet*100:.1f}%")
print("=" * 55)

# ════════════════════════════════════════════
#  描画
# ════════════════════════════════════════════
sc = 1.05
OX, OY = 70, 60

fig, ax = plt.subplots(figsize=(10, 10))

def T(x, y): return OX + x*sc, OY + y*sc

ax.set_xlim(-30, OX + SHEET_W*sc + 130)
ax.set_ylim(-60, OY + SHEET_H*sc + 100)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(
    f'【板取り図】  {SHEET_W}×{SHEET_H}mm 板 1枚  板厚 0.5mm\n'
    f'材料利用率 {area_parts/area_sheet*100:.1f}%  '
    f'（部品間隔 {GAP}mm）',
    fontsize=13, fontweight='bold', pad=14)

# ── 板（素材）──
ax.add_patch(patches.Rectangle(
    T(0, 0), SHEET_W*sc, SHEET_H*sc,
    edgecolor='#444', facecolor='#F5F5F5', lw=2.5, zorder=1))

# ── 部品描画関数 ──
def draw_part(x, y, w, h, fc, ec, name, size_str, rot=False):
    ax.add_patch(patches.Rectangle(
        T(x, y), w*sc, h*sc,
        edgecolor=ec, facecolor=fc, lw=1.8, zorder=3, alpha=0.88))
    # 部品名
    cx, cy = T(x + w/2, y + h/2)
    ax.text(cx, cy + 6, name, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=ec, zorder=5)
    # サイズ
    ax.text(cx, cy - 8, size_str, ha='center', va='center',
            fontsize=8, color='#444', zorder=5)

# ── 4部品 ──
draw_part(p04_x, p04_y, P04_W, P04_H,
          '#BBDEFB', '#1565C0',
          'pitts_04  箱 側面', f'{P04_W}×{P04_H}mm')

draw_part(l02_x, l02_y, L02_W, L02_H,
          '#E1BEE7', '#6A1B9A',
          'lid_02  蓋 側面', f'{L02_W}×{L02_H}mm')

draw_part(p01_x, p01_y, P01_W, P01_H,
          '#C8E6C9', '#2E7D32',
          'pitts_01\n箱 底面', f'{P01_W}×{P01_H}mm')

draw_part(l01_x, l01_y, L01_W, L01_H,
          '#FFE0B2', '#E65100',
          'lid_01\n蓋 天面', f'{L01_W}×{L01_H}mm')

# ── 余白部（網掛け） ──
waste_regions = [
    # pitts_04 右の余白
    (P04_W+GAP, p04_y, SHEET_W-P04_W-GAP, P04_H),
    # lid_01 右の余白
    (l01_x+L01_W+GAP, l01_y, SHEET_W-l01_x-L01_W-GAP, L01_H),
    # pitts_01・lid_01 下の余白（板底まで）
    (0, 0, SHEET_W, p01_y - GAP),
]
for (wx, wy, ww, wh) in waste_regions:
    if ww > 0 and wh > 0:
        ax.add_patch(patches.Rectangle(
            T(wx, wy), ww*sc, wh*sc,
            hatch='....', facecolor='none', edgecolor='#BDBDBD',
            lw=0.3, alpha=0.5, zorder=2))

# ── 板の寸法線 ──
def dim_arrow(ax, x1, y1, x2, y2, text, side='right', fontsize=9, color='#333'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    mx, my = (x1+x2)/2, (y1+y2)/2
    if x1 == x2:
        dx = 5 if side == 'right' else -5
        ax.text(mx+dx, my, text, ha='left' if side=='right' else 'right',
                va='center', fontsize=fontsize, color=color)
    else:
        dy = -6 if side == 'bottom' else 6
        ax.text(mx, my+dy, text, ha='center',
                va='top' if side == 'bottom' else 'bottom', fontsize=fontsize, color=color)

# 板幅（上）
dim_arrow(ax, *T(0, SHEET_H+10), *T(SHEET_W, SHEET_H+10),
          f'{SHEET_W}mm', 'top', 10, '#333')
# 板高（右）
dim_arrow(ax, *T(SHEET_W+10, 0), *T(SHEET_W+10, SHEET_H),
          f'{SHEET_H}mm', 'right', 10, '#333')

# 各部品の配置寸法（右側に積み上げ高さ）
annotations = [
    (SHEET_W+40, p04_y,         SHEET_W+40, p04_y+P04_H,   f'{P04_H}mm', '#1565C0'),
    (SHEET_W+40, l02_y,         SHEET_W+40, l02_y+L02_H,   f'{L02_H}mm', '#6A1B9A'),
    (SHEET_W+40, p01_y,         SHEET_W+40, p01_y+P01_H,   f'{P01_H}mm', '#2E7D32'),
]
for x1, y1, x2, y2, txt, clr in annotations:
    dim_arrow(ax, *T(x1/sc, y1/sc + (y2-y1)/(2*sc) - 0.5), # hack to use T properly
              *T(x1/sc, y1/sc + (y2-y1)/(2*sc) + 0.5), '', 'right', 8, clr)

# シンプルに右側ラベル
for (py, ph, lbl, clr) in [
    (p04_y, P04_H, f'{P04_H}mm', '#1565C0'),
    (l02_y, L02_H, f'{L02_H}mm', '#6A1B9A'),
    (p01_y, P01_H, f'{P01_H}mm', '#2E7D32'),
]:
    tx, ty = T(SHEET_W + 12, py + ph/2)
    ax.annotate('', xy=T(SHEET_W+8, py+ph), xytext=T(SHEET_W+8, py),
                arrowprops=dict(arrowstyle='<->', color=clr, lw=1.0))
    ax.text(tx, ty, lbl, ha='left', va='center', fontsize=8, color=clr)

# 下幅ラベル
for (px, pw, lbl, clr) in [
    (p04_x, P04_W, f'{P04_W}mm', '#1565C0'),
    (l02_x, L02_W, f'{L02_W}mm', '#6A1B9A'),
    (p01_x, P01_W, f'{P01_W}mm', '#2E7D32'),
    (l01_x, L01_W, f'{L01_W}mm', '#E65100'),
]:
    bx1, by1 = T(px, -12)
    bx2, by2 = T(px+pw, -12)
    ax.annotate('', xy=(bx2, by1), xytext=(bx1, by1),
                arrowprops=dict(arrowstyle='<->', color=clr, lw=1.0))
    ax.text((bx1+bx2)/2, by1-5, lbl, ha='center', va='top', fontsize=8, color=clr)

# ── 凡例 ──
LX = OX
LY = OY - 42
items = [
    ('#BBDEFB', '#1565C0', f'pitts_04  箱 側面  {P04_W}×{P04_H}mm'),
    ('#E1BEE7', '#6A1B9A', f'lid_02    蓋 側面  {L02_W}×{L02_H}mm'),
    ('#C8E6C9', '#2E7D32', f'pitts_01  箱 底面  {P01_W}×{P01_H}mm'),
    ('#FFE0B2', '#E65100', f'lid_01    蓋 天面  {L01_W}×{L01_H}mm'),
]
for i, (fc, ec, lbl) in enumerate(items):
    ax.add_patch(patches.Rectangle((LX + i*130, LY), 14, 10,
                                    facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(LX + i*130 + 18, LY+5, lbl, fontsize=8, va='center', color='#333')

plt.savefig('nesting_90x130.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("nesting_90x130.png  完了")
