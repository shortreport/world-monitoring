"""
板金箱 展開図・作成手順図 生成スクリプト
溶接なし・ハゼ折り構造（タブは長辺側板に付く）
材料: 455mm × 455mm
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
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

# ═══════════════════════════════════════════════
#  寸法定義
# ═══════════════════════════════════════════════
W  = 130   # 幅（短辺）mm
L  = 190   # 長さ（長辺）mm
H  = 55    # 高さ mm

SHEET    = 455
T_PLATE  = 0.5   # 板厚 mm

# ── ハゼ構造寸法 ──
# 長辺タブ側 (y方向加算): T板厚+T板厚+9mm有効タブ = 10mm
S_tab   = 9                       # 長辺タブ有効長さ mm
S_long  = T_PLATE*2 + S_tab       # = 10mm  長辺ハゼしろ合計
# 短辺受け側 (x方向加算): T板厚+T板厚+11mm受け = 12mm
R_lock  = 11                      # 短辺受け有効長さ mm
S_short = T_PLATE*2 + R_lock      # = 12mm  短辺受け合計

# 本体ブランク
# x方向: 短辺側板(H+S_short)×2 + 底板幅W  → 受けあり
# y方向: 長辺側板(H+S_long)×2  + 底板長L  → タブあり
BW = W + 2*(H + S_short)          # 130 + 2*67 = 264 mm
BH = L + 2*(H + S_long)           # 190 + 2*65 = 320 mm

# 折り曲げ位置
xs = [0, H+S_short, H+S_short+W, 2*(H+S_short)+W]   # [0, 67, 197, 264]
ys = [0, H+S_long,  H+S_long+L,  2*(H+S_long)+L]    # [0, 65, 255, 320]

# 蓋寸法（同構造）
W_lid = W + 4     # 134 mm
L_lid = L + 4     # 194 mm
H_lid = 18

S_tab_lid   = 7
S_long_lid  = T_PLATE*2 + S_tab_lid    # = 8mm
R_lock_lid  = 9
S_short_lid = T_PLATE*2 + R_lock_lid   # = 10mm

LW = W_lid + 2*(H_lid + S_short_lid)    # 134 + 2*28 = 190 mm
LH = L_lid + 2*(H_lid + S_long_lid)     # 194 + 2*26 = 246 mm
lxs = [0, H_lid+S_short_lid, H_lid+S_short_lid+W_lid, 2*(H_lid+S_short_lid)+W_lid]
      # [0, 28, 162, 190]
lys = [0, H_lid+S_long_lid, H_lid+S_long_lid+L_lid, 2*(H_lid+S_long_lid)+L_lid]
      # [0, 26, 220, 246]

print("="*50)
print(f"本体内寸  : W{W} x L{L} x H{H} mm  板厚{T_PLATE}mm")
print(f"  長辺タブ: T+T+{S_tab}={S_long}mm  短辺受け: T+T+{R_lock}={S_short}mm")
print(f"本体ブランク: {BW} x {BH} mm")
print(f"  xs={xs}  ys={ys}")
print(f"蓋内寸    : W{W_lid} x L{L_lid} x H{H_lid} mm")
print(f"蓋ブランク  : {LW} x {LH} mm")
print(f"  lxs={lxs}")
print(f"板取り配置  : 本体{BW}+蓋{LW}={BW+LW}mm (< {SHEET}mm {'+OK' if BW+LW<=SHEET else 'NG!'})")
print("="*50)

# ── ヘルパー関数 ──
def dim_arrow(ax, x1, y1, x2, y2, text, side='bottom', fontsize=8.5, color='#333333'):
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    mx, my = (x1+x2)/2, (y1+y2)/2
    if x1 == x2:
        ax.text(mx+6, my, text, ha='left', va='center', fontsize=fontsize, color=color)
    else:
        dy = -6 if side=='bottom' else 6
        ax.text(mx, my+dy, text, ha='center',
                va='top' if side=='bottom' else 'bottom', fontsize=fontsize, color=color)

def fold_line(ax, x1, y1, x2, y2, color='#0066CC', ls='--', lw=1.2):
    ax.plot([x1,x2],[y1,y2], linestyle=ls, color=color, lw=lw, zorder=4)

# ═══════════════════════════════════════════════
#  図1: 板取り図（横並び配置）
# ═══════════════════════════════════════════════
fig1, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(-40, 500); ax.set_ylim(-50, 500)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('【板取り図】455mm x 455mm 一枚板からの切り出し', fontsize=13, fontweight='bold', pad=12)

ax.add_patch(patches.Rectangle((0,0), SHEET, SHEET,
             linewidth=2.5, edgecolor='#333333', facecolor='#FAFAF0', zorder=1))

bx0, by0 = 0, (SHEET-BH)//2
lx0, ly0 = bx0+BW+1, (SHEET-LH)//2

ax.add_patch(patches.Rectangle((bx0,by0), BW, BH,
             linewidth=2, edgecolor='#1565C0', facecolor='#BBDEFB', alpha=0.85, zorder=2))
ax.text(bx0+BW/2, by0+BH*0.55, '本体ブランク', ha='center', fontsize=11,
        fontweight='bold', color='#1565C0', zorder=3)
ax.text(bx0+BW/2, by0+BH*0.45, f'{BW} x {BH} mm', ha='center', fontsize=10,
        color='#1565C0', zorder=3)

ax.add_patch(patches.Rectangle((lx0,ly0), LW, LH,
             linewidth=2, edgecolor='#B71C1C', facecolor='#FFCDD2', alpha=0.85, zorder=2))
ax.text(lx0+LW/2, ly0+LH*0.55, '蓋ブランク', ha='center', fontsize=11,
        fontweight='bold', color='#B71C1C', zorder=3)
ax.text(lx0+LW/2, ly0+LH*0.45, f'{LW} x {LH} mm', ha='center', fontsize=10,
        color='#B71C1C', zorder=3)

# 端材
for rx,ry,rw,rh in [
    (lx0+LW, 0, SHEET-lx0-LW, SHEET),
    (bx0, by0+BH, BW, SHEET-by0-BH),
    (bx0, 0, BW, by0),
    (lx0, ly0+LH, LW, SHEET-ly0-LH),
    (lx0, 0, LW, ly0),
]:
    if rw > 3 and rh > 3:
        ax.add_patch(patches.Rectangle((rx,ry), rw, rh, linewidth=1, edgecolor='gray',
                     facecolor='#EEEEEE', alpha=0.5, linestyle=':', zorder=2))
        ax.text(rx+rw/2, ry+rh/2, '端材', ha='center', va='center',
                fontsize=8, color='#999999', zorder=3)

dim_arrow(ax, 0,-20, SHEET,-20, f'{SHEET}mm', 'bottom', 10, '#333333')
dim_arrow(ax, -30,0, -30,SHEET, f'{SHEET}mm', 'bottom', 10, '#333333')
dim_arrow(ax, bx0,by0-12, bx0+BW,by0-12, f'{BW}mm', 'bottom', 8.5, '#1565C0')
dim_arrow(ax, -15,by0, -15,by0+BH, f'{BH}mm', 'bottom', 8.5, '#1565C0')
dim_arrow(ax, lx0,ly0-12, lx0+LW,ly0-12, f'{LW}mm', 'bottom', 8.5, '#B71C1C')
dim_arrow(ax, lx0+LW+8,ly0, lx0+LW+8,ly0+LH, f'{LH}mm', 'bottom', 8.5, '#B71C1C')

ax.text(SHEET/2, -45,
        f'本体({BW}x{BH}) + 蓋({LW}x{LH})  使用幅:{bx0+BW+1+LW}mm  最大高:{max(BH,LH)}mm  <- 455x455に収まる',
        ha='center', fontsize=8.5, color='#333333',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFDE7', edgecolor='#FFA000'))

# 板厚・材質仕様
ax.text(SHEET-5, SHEET-5,
        f'【材料仕様】\n板厚: {T_PLATE}mm\n板サイズ: {SHEET}x{SHEET}mm\n材質: 鋼板（ガルバ等）',
        ha='right', va='top', fontsize=9, color='#333333',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', edgecolor='#F57F17', lw=1.5))

plt.savefig('box_01_itatorie.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("box_01_itatorie.png")

# ═══════════════════════════════════════════════
#  図2: 本体展開図（詳細）
# ═══════════════════════════════════════════════
fig2, ax = plt.subplots(figsize=(10, 13))
OX, OY = 70, 60
sc = 0.92

ax.set_xlim(-10, OX + BW*sc + 90)
ax.set_ylim(-80, OY + BH*sc + 100)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title(
    f'【本体 展開図】  内寸 W{W}×L{L}×H{H}mm  板厚{T_PLATE}mm\n'
    f'長辺タブ {S_long}mm(T+T+{S_tab})  短辺受け {S_short}mm(T+T+{R_lock})',
    fontsize=12, fontweight='bold', pad=12)

def T2(x, y): return OX + x*sc, OY + y*sc

zc = {
    'bottom': '#C8E6C9',
    'long':   '#BBDEFB',
    'short':  '#FFE0B2',
    'tab':    '#FF8A65',
    'recv':   '#E1BEE7',   # 受け部（紫系）
}

# 底板
ax.add_patch(patches.Rectangle(T2(xs[1],ys[1]), (xs[2]-xs[1])*sc, (ys[2]-ys[1])*sc,
             edgecolor='#2E7D32', facecolor=zc['bottom'], lw=1.5, zorder=3))
ax.text(*T2((xs[1]+xs[2])/2, (ys[1]+ys[2])/2), f'底板\n{W}×{L}mm',
        ha='center', va='center', fontsize=10, fontweight='bold', color='#2E7D32', zorder=5)

# 長辺側板（y方向上下）壁 + タブ 別色で描画
for is_bottom in [True, False]:
    name = '前面' if is_bottom else '後面'
    if is_bottom:
        wall_y0, wall_y1 = ys[0]+S_long, ys[1]
        tab_y0,  tab_y1  = ys[0],        ys[0]+S_long
    else:
        wall_y0, wall_y1 = ys[2],        ys[3]-S_long
        tab_y0,  tab_y1  = ys[3]-S_long, ys[3]
    # 壁部分（青）
    ax.add_patch(patches.Rectangle(T2(xs[1], wall_y0), (xs[2]-xs[1])*sc, (wall_y1-wall_y0)*sc,
                 edgecolor='#1565C0', facecolor=zc['long'], lw=1.5, zorder=3))
    ax.text(*T2((xs[1]+xs[2])/2, (wall_y0+wall_y1)/2),
            f'長辺壁({name})\n{W}×{H}mm',
            ha='center', va='center', fontsize=8, color='#1565C0', zorder=5)
    # タブ部分（橙 = コーナータブと同色）
    ax.add_patch(patches.Rectangle(T2(xs[1], tab_y0), (xs[2]-xs[1])*sc, (tab_y1-tab_y0)*sc,
                 edgecolor='#BF360C', facecolor=zc['tab'], lw=1.5, zorder=3))
    ax.text(*T2((xs[1]+xs[2])/2, (tab_y0+tab_y1)/2),
            f'タブ {S_long}mm',
            ha='center', va='center', fontsize=6.5, color='white', fontweight='bold', zorder=5)

# 短辺側板（x方向左右）壁部分 + 受け部分
for xi, xj in [(0, 1), (2, 3)]:
    if xi == 0:
        wx0, wx1 = xs[0]+S_short, xs[1]     # 壁: x=[12, 67]
        rx0, rx1 = xs[0],         xs[0]+S_short  # 受け: x=[0, 12]
    else:
        wx0, wx1 = xs[2],         xs[3]-S_short  # 壁: x=[197, 252]
        rx0, rx1 = xs[3]-S_short, xs[3]     # 受け: x=[252, 264]
    # 壁部分（橙色）
    ax.add_patch(patches.Rectangle(T2(wx0, ys[1]), (wx1-wx0)*sc, (ys[2]-ys[1])*sc,
                 edgecolor='#E65100', facecolor=zc['short'], lw=1.5, zorder=3))
    ax.text(*T2((wx0+wx1)/2, (ys[1]+ys[2])/2), f'短辺壁\n{H}×{L}mm',
            ha='center', va='center', fontsize=7.5, color='#E65100', zorder=5)
    # 受け部分（紫色）
    ax.add_patch(patches.Rectangle(T2(rx0, ys[1]), (rx1-rx0)*sc, (ys[2]-ys[1])*sc,
                 edgecolor='#7B1FA2', facecolor=zc['recv'], lw=1.5, zorder=3))
    ax.text(*T2((rx0+rx1)/2, (ys[1]+ys[2])/2),
            f'受け\n{S_short}mm\n(T+T+{R_lock})',
            ha='center', va='center', fontsize=5.5, color='#7B1FA2', zorder=5)

# ── コーナー処理（4隅）──
# 下側2隅
for xi0, xi1 in [(xs[0],xs[1]), (xs[2],xs[3])]:
    cx = (xi0+xi1)/2
    # タブ（y=0〜S_long = 10mm）
    ax.add_patch(patches.Rectangle(T2(xi0, ys[0]), (xi1-xi0)*sc, S_long*sc,
                 edgecolor='#BF360C', facecolor=zc['tab'], lw=1.5, zorder=4))
    ax.text(*T2(cx, S_long/2), f'タブ\n{S_long}mm', ha='center', va='center',
            fontsize=6.5, color='white', fontweight='bold', zorder=6)
    # 切取り（y=S_long〜H+S_long = 55mm）
    ax.add_patch(patches.Rectangle(T2(xi0, ys[0]+S_long), (xi1-xi0)*sc, H*sc,
                 edgecolor='red', facecolor='#FFCDD2', lw=1.5, linestyle='--', alpha=0.7, zorder=4))
    ax.text(*T2(cx, S_long+H/2), 'x\n切取', ha='center', va='center',
            fontsize=7, color='red', zorder=6)

# 上側2隅
for xi0, xi1 in [(xs[0],xs[1]), (xs[2],xs[3])]:
    cx = (xi0+xi1)/2
    # タブ
    ax.add_patch(patches.Rectangle(T2(xi0, ys[3]-S_long), (xi1-xi0)*sc, S_long*sc,
                 edgecolor='#BF360C', facecolor=zc['tab'], lw=1.5, zorder=4))
    ax.text(*T2(cx, ys[3]-S_long/2), f'タブ\n{S_long}mm', ha='center', va='center',
            fontsize=6.5, color='white', fontweight='bold', zorder=6)
    # 切取り
    ax.add_patch(patches.Rectangle(T2(xi0, ys[2]), (xi1-xi0)*sc, H*sc,
                 edgecolor='red', facecolor='#FFCDD2', lw=1.5, linestyle='--', alpha=0.7, zorder=4))
    ax.text(*T2(cx, ys[2]+H/2), 'x\n切取', ha='center', va='center',
            fontsize=7, color='red', zorder=6)

# ── 外形線（正しい輪郭）──
outline_pts = [
    T2(xs[0], ys[0]),             # (0,0)
    T2(xs[3], ys[0]),             # (264,0)    下辺全幅
    T2(xs[3], ys[0]+S_long),      # (264,10)   右タブ上端
    T2(xs[2], ys[0]+S_long),      # (197,10)   右下ノッチ内角
    T2(xs[2], ys[1]),             # (197,65)   右短辺折り線（下）
    T2(xs[3], ys[1]),             # (264,65)   右辺
    T2(xs[3], ys[2]),             # (264,255)  右辺上
    T2(xs[2], ys[2]),             # (197,255)  右短辺折り線（上）
    T2(xs[2], ys[3]-S_long),      # (197,310)  右上ノッチ内角
    T2(xs[3], ys[3]-S_long),      # (264,310)  右タブ下端
    T2(xs[3], ys[3]),             # (264,320)  右上
    T2(xs[0], ys[3]),             # (0,320)    上辺全幅
    T2(xs[0], ys[3]-S_long),      # (0,310)    左タブ下端
    T2(xs[1], ys[3]-S_long),      # (67,310)   左上ノッチ内角
    T2(xs[1], ys[2]),             # (67,255)   左短辺折り線（上）
    T2(xs[0], ys[2]),             # (0,255)    左辺上
    T2(xs[0], ys[1]),             # (0,65)     左辺下
    T2(xs[1], ys[1]),             # (67,65)    左短辺折り線（下）
    T2(xs[1], ys[0]+S_long),      # (67,10)    左下ノッチ内角
    T2(xs[0], ys[0]+S_long),      # (0,10)     左タブ上端
    T2(xs[0], ys[0]),             # (0,0)      閉じる
]
ax.plot([p[0] for p in outline_pts], [p[1] for p in outline_pts],
        color='#333333', lw=2.5, zorder=7)

# ── 折り曲げ線 ──
CLR_MAIN = '#0066CC'  # 青：パネル境界折り線
CLR_BEND = '#E65100'  # 橙：谷折り線（ハゼ構造内部）

# 底板↔短辺側板の折り線（縦）
for x in [xs[1], xs[2]]:
    fold_line(ax, *T2(x, ys[1]), *T2(x, ys[2]), color=CLR_MAIN)
# 底板↔長辺側板の折り線（横）
for y in [ys[1], ys[2]]:
    fold_line(ax, *T2(xs[1], y), *T2(xs[2], y), color=CLR_MAIN)

# ── 長辺タブ 谷折り線（ブランク全幅） ──
# ① 壁/折りしろ境界：y = S_long(10mm) から外辺
fold_line(ax, *T2(xs[0], ys[0]+S_long), *T2(xs[3], ys[0]+S_long), color=CLR_BEND, ls='-.')
fold_line(ax, *T2(xs[0], ys[3]-S_long), *T2(xs[3], ys[3]-S_long), color=CLR_BEND, ls='-.')
# ② 折りしろ/タブ境界：y = S_tab(9mm) から外辺
fold_line(ax, *T2(xs[0], ys[0]+S_tab),  *T2(xs[3], ys[0]+S_tab),  color=CLR_BEND, ls='-.')
fold_line(ax, *T2(xs[0], ys[3]-S_tab),  *T2(xs[3], ys[3]-S_tab),  color=CLR_BEND, ls='-.')

# ── 短辺受け 谷折り線（短辺帯: y=[ys[1],ys[2]]） ──
# ① 壁/折りしろ境界：x = S_short(12mm) から外辺
fold_line(ax, *T2(xs[0]+S_short, ys[1]), *T2(xs[0]+S_short, ys[2]), color=CLR_BEND, ls='-.')
fold_line(ax, *T2(xs[3]-S_short, ys[1]), *T2(xs[3]-S_short, ys[2]), color=CLR_BEND, ls='-.')
# ② 折りしろ/受け境界：x = R_lock(11mm) から外辺
fold_line(ax, *T2(xs[0]+R_lock,  ys[1]), *T2(xs[0]+R_lock,  ys[2]), color=CLR_BEND, ls='-.')
fold_line(ax, *T2(xs[3]-R_lock,  ys[1]), *T2(xs[3]-R_lock,  ys[2]), color=CLR_BEND, ls='-.')

# ── 谷折り寸法ラベル（長辺パネル下側） ──
_lx = T2(xs[1]-2/sc, 0)[0]  # 長辺パネル左端の少し左
_sc = sc
# 9mm タブ区間
ax.annotate('', xy=T2(xs[1]-4/sc, ys[0]+S_tab),
            xytext=T2(xs[1]-4/sc, ys[0]),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T2(xs[1]-3/sc, ys[0]+S_tab/2), f'{S_tab}', ha='right', va='center',
        fontsize=7, color=CLR_BEND)
# 1mm 折りしろ区間
ax.annotate('', xy=T2(xs[1]-4/sc, ys[0]+S_long),
            xytext=T2(xs[1]-4/sc, ys[0]+S_tab),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T2(xs[1]-3/sc, ys[0]+S_tab+T_PLATE), f'1', ha='right', va='center',
        fontsize=6, color=CLR_BEND)
# 55mm 壁区間
ax.annotate('', xy=T2(xs[1]-4/sc, ys[1]),
            xytext=T2(xs[1]-4/sc, ys[0]+S_long),
            arrowprops=dict(arrowstyle='<->', color=CLR_MAIN, lw=1.0))
ax.text(*T2(xs[1]-3/sc, ys[0]+S_long+H/2), f'{H}', ha='right', va='center',
        fontsize=7, color=CLR_MAIN)

# ── 谷折り寸法ラベル（短辺パネル左側） ──
_by = T2(0, ys[1]-3/sc)[1]
# 11mm 受け区間
ax.annotate('', xy=T2(xs[0]+R_lock,  ys[1]-4/sc),
            xytext=T2(xs[0],         ys[1]-4/sc),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T2(xs[0]+R_lock/2, ys[1]-3/sc), f'{R_lock}', ha='center', va='top',
        fontsize=7, color=CLR_BEND)
# 1mm 折りしろ区間
ax.annotate('', xy=T2(xs[0]+S_short, ys[1]-4/sc),
            xytext=T2(xs[0]+R_lock,  ys[1]-4/sc),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T2(xs[0]+R_lock+T_PLATE, ys[1]-3/sc), '1', ha='center', va='top',
        fontsize=6, color=CLR_BEND)
# 55mm 壁区間
ax.annotate('', xy=T2(xs[1],        ys[1]-4/sc),
            xytext=T2(xs[0]+S_short, ys[1]-4/sc),
            arrowprops=dict(arrowstyle='<->', color=CLR_MAIN, lw=1.0))
ax.text(*T2(xs[0]+S_short+H/2, ys[1]-3/sc), f'{H}', ha='center', va='top',
        fontsize=7, color=CLR_MAIN)

# ── 寸法線 ──
off = 28
# 横方向（上辺）
dim_arrow(ax, *T2(xs[0], ys[3]+off/sc),   *T2(xs[1], ys[3]+off/sc),
          f'H+受={H+S_short}mm', 'top', 7.5, '#E65100')
dim_arrow(ax, *T2(xs[1], ys[3]+off/sc),   *T2(xs[2], ys[3]+off/sc),
          f'W={W}mm', 'top', 9, '#2E7D32')
dim_arrow(ax, *T2(xs[2], ys[3]+off/sc),   *T2(xs[3], ys[3]+off/sc),
          f'H+受={H+S_short}mm', 'top', 7.5, '#E65100')
dim_arrow(ax, *T2(xs[0], ys[3]+off*2/sc), *T2(xs[3], ys[3]+off*2/sc),
          f'全幅 {BW}mm', 'top', 9.5, '#333333')
# 縦方向（右辺）
ox2 = xs[3]+12
dim_arrow(ax, *T2(ox2, ys[0]), *T2(ox2, ys[1]),
          f'H+タブ\n{H+S_long}mm', 'bottom', 8, '#1565C0')
dim_arrow(ax, *T2(ox2, ys[1]), *T2(ox2, ys[2]),
          f'L={L}mm', 'bottom', 9, '#2E7D32')
dim_arrow(ax, *T2(ox2, ys[2]), *T2(ox2, ys[3]),
          f'H+タブ\n{H+S_long}mm', 'bottom', 8, '#1565C0')
dim_arrow(ax, *T2(ox2+28/sc, ys[0]), *T2(ox2+28/sc, ys[3]),
          f'全長 {BH}mm', 'bottom', 9.5, '#333333')
# タブ幅注記
ax.annotate(f'ハゼタブ\n{S_long}mm', xy=T2(xs[1]/2, S_long/2),
            xytext=T2(-18/sc, S_long/2),
            fontsize=8, color='#BF360C', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#BF360C', lw=1),
            ha='right', va='center')

# 凡例
legend_items = [
    (zc['bottom'], '#2E7D32', '底板'),
    (zc['long'],   '#1565C0', f'長辺壁（前後）{W}×{H}mm'),
    (zc['short'],  '#E65100', f'短辺壁（左右）{H}×{L}mm'),
    (zc['recv'],   '#7B1FA2', f'短辺受け {S_short}mm（T+T+{R_lock}mm）← タブを押さえる'),
    (zc['tab'],    '#BF360C', f'タブ部分 {S_long}mm（T+T+{S_tab}mm）← 長辺パネル外縁 ＋ コーナー共通'),
    ('#FFCDD2',    'red',     f'切り取り部（{H+S_short}×{H}mm）'),
]
for i, (fc, ec, lbl) in enumerate(legend_items):
    lx = T2(xs[0], 0)[0]
    ly = T2(0, 0)[1] - 18 - i*17
    ax.add_patch(patches.Rectangle((lx, ly), 18, 11, facecolor=fc, edgecolor=ec, lw=1))
    ax.text(lx+22, ly+5.5, lbl, fontsize=8, va='center', color='#333333')

# 折り線凡例
lx = T2(xs[0], 0)[0]
ly_line = T2(0, 0)[1] - 18 - len(legend_items)*17
ax.plot([lx, lx+18], [ly_line+5.5, ly_line+5.5], ls='--', color=CLR_MAIN, lw=1.5)
ax.text(lx+22, ly_line+5.5, '折り曲げ線（パネル境界）', fontsize=8, va='center', color='#333333')
ly_line2 = ly_line - 17
ax.plot([lx, lx+18], [ly_line2+5.5, ly_line2+5.5], ls='-.', color=CLR_BEND, lw=1.5)
ax.text(lx+22, ly_line2+5.5,
        f'２回谷折りする（ハゼ構造）: タブ{S_tab}mm ＋ 折りしろ1mm / 受け{R_lock}mm ＋ 折りしろ1mm',
        fontsize=8, va='center', color='#333333')

# 板厚注記（右下）
note_x = T2(xs[3], 0)[0] + 40
note_y = T2(0, 0)[1] - 10
ax.text(note_x, note_y,
        f'板厚: {T_PLATE}mm\n（溶融亜鉛めっき鋼板等）',
        ha='left', va='top', fontsize=9, color='#5D4037',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', edgecolor='#F57F17', lw=1.5))

plt.savefig('box_02_honkaitenzu.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("box_02_honkaitenzu.png")

# ═══════════════════════════════════════════════
#  図3: 蓋展開図（詳細）
# ═══════════════════════════════════════════════
fig3, ax = plt.subplots(figsize=(8, 11))
OX3, OY3 = 70, 60
sc3 = 0.92

ax.set_xlim(-10, OX3 + LW*sc3 + 90)
ax.set_ylim(-60, OY3 + LH*sc3 + 90)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title(
    f'【蓋 展開図】  内寸 W{W_lid}×L{L_lid}×H{H_lid}mm  板厚{T_PLATE}mm\n'
    f'長辺タブ {S_long_lid}mm(T+T+{S_tab_lid})  短辺受け {S_short_lid}mm(T+T+{R_lock_lid})',
    fontsize=12, fontweight='bold', pad=12)

def T3(x, y): return OX3 + x*sc3, OY3 + y*sc3

zc3 = {
    'top':   '#E8F5E9',
    'long':  '#E3F2FD',
    'short': '#FFF3E0',
    'tab':   '#FF8A65',
    'recv':  '#F3E5F5',
}

# 天面
ax.add_patch(patches.Rectangle(T3(lxs[1],lys[1]), (lxs[2]-lxs[1])*sc3, (lys[2]-lys[1])*sc3,
             edgecolor='#2E7D32', facecolor=zc3['top'], lw=1.5, zorder=3))
ax.text(*T3((lxs[1]+lxs[2])/2, (lys[1]+lys[2])/2), f'蓋天面\n{W_lid}×{L_lid}mm',
        ha='center', va='center', fontsize=9, fontweight='bold', color='#2E7D32', zorder=5)

# 長辺側板（y方向）壁 + タブ 別色で描画
for is_bottom in [True, False]:
    if is_bottom:
        wall_y0, wall_y1 = lys[0]+S_long_lid, lys[1]
        tab_y0,  tab_y1  = lys[0],            lys[0]+S_long_lid
    else:
        wall_y0, wall_y1 = lys[2],            lys[3]-S_long_lid
        tab_y0,  tab_y1  = lys[3]-S_long_lid, lys[3]
    name3 = '前面' if is_bottom else '後面'
    # 壁部分（青）
    ax.add_patch(patches.Rectangle(T3(lxs[1], wall_y0), (lxs[2]-lxs[1])*sc3, (wall_y1-wall_y0)*sc3,
                 edgecolor='#1565C0', facecolor=zc3['long'], lw=1.5, zorder=3))
    ax.text(*T3((lxs[1]+lxs[2])/2, (wall_y0+wall_y1)/2),
            f'長辺壁({name3})\n{W_lid}×{H_lid}mm',
            ha='center', va='center', fontsize=7.5, color='#1565C0', zorder=5)
    # タブ部分（橙 = コーナータブと同色）
    ax.add_patch(patches.Rectangle(T3(lxs[1], tab_y0), (lxs[2]-lxs[1])*sc3, (tab_y1-tab_y0)*sc3,
                 edgecolor='#BF360C', facecolor=zc3['tab'], lw=1.5, zorder=3))
    ax.text(*T3((lxs[1]+lxs[2])/2, (tab_y0+tab_y1)/2),
            f'タブ {S_long_lid}mm',
            ha='center', va='center', fontsize=6, color='white', fontweight='bold', zorder=5)

# 短辺側板（x方向）壁部分 + 受け部分
for xi, xj in [(0, 1), (2, 3)]:
    if xi == 0:
        wx0, wx1 = lxs[0]+S_short_lid, lxs[1]
        rx0, rx1 = lxs[0],             lxs[0]+S_short_lid
    else:
        wx0, wx1 = lxs[2],             lxs[3]-S_short_lid
        rx0, rx1 = lxs[3]-S_short_lid, lxs[3]
    # 壁部分
    ax.add_patch(patches.Rectangle(T3(wx0, lys[1]), (wx1-wx0)*sc3, (lys[2]-lys[1])*sc3,
                 edgecolor='#E65100', facecolor=zc3['short'], lw=1.5, zorder=3))
    ax.text(*T3((wx0+wx1)/2, (lys[1]+lys[2])/2), f'短辺壁\n{H_lid}×{L_lid}mm',
            ha='center', va='center', fontsize=7, color='#E65100', zorder=5)
    # 受け部分
    ax.add_patch(patches.Rectangle(T3(rx0, lys[1]), (rx1-rx0)*sc3, (lys[2]-lys[1])*sc3,
                 edgecolor='#7B1FA2', facecolor=zc3['recv'], lw=1.5, zorder=3))
    ax.text(*T3((rx0+rx1)/2, (lys[1]+lys[2])/2), f'受け\n{S_short_lid}mm',
            ha='center', va='center', fontsize=6, color='#7B1FA2', zorder=5)

# コーナー処理
for xi0, xi1 in [(lxs[0],lxs[1]), (lxs[2],lxs[3])]:
    cx = (xi0+xi1)/2
    # 下側タブ
    ax.add_patch(patches.Rectangle(T3(xi0, lys[0]), (xi1-xi0)*sc3, S_long_lid*sc3,
                 edgecolor='#BF360C', facecolor=zc3['tab'], lw=1, zorder=4))
    ax.text(*T3(cx, S_long_lid/2), f'T\n{S_long_lid}', ha='center', va='center',
            fontsize=6, color='white', fontweight='bold', zorder=6)
    # 下側切取り
    ax.add_patch(patches.Rectangle(T3(xi0, lys[0]+S_long_lid), (xi1-xi0)*sc3, H_lid*sc3,
                 edgecolor='red', facecolor='#FFCDD2', lw=1, linestyle='--', alpha=0.7, zorder=4))
    ax.text(*T3(cx, S_long_lid+H_lid/2), 'x', ha='center', va='center',
            fontsize=8, color='red', zorder=6)
    # 上側タブ
    ax.add_patch(patches.Rectangle(T3(xi0, lys[3]-S_long_lid), (xi1-xi0)*sc3, S_long_lid*sc3,
                 edgecolor='#BF360C', facecolor=zc3['tab'], lw=1, zorder=4))
    ax.text(*T3(cx, lys[3]-S_long_lid/2), f'T\n{S_long_lid}', ha='center', va='center',
            fontsize=6, color='white', fontweight='bold', zorder=6)
    # 上側切取り
    ax.add_patch(patches.Rectangle(T3(xi0, lys[2]), (xi1-xi0)*sc3, H_lid*sc3,
                 edgecolor='red', facecolor='#FFCDD2', lw=1, linestyle='--', alpha=0.7, zorder=4))
    ax.text(*T3(cx, lys[2]+H_lid/2), 'x', ha='center', va='center',
            fontsize=8, color='red', zorder=6)

# 外形線
lid_outline = [
    T3(lxs[0], lys[0]),
    T3(lxs[3], lys[0]),
    T3(lxs[3], lys[0]+S_long_lid),
    T3(lxs[2], lys[0]+S_long_lid),
    T3(lxs[2], lys[1]),
    T3(lxs[3], lys[1]),
    T3(lxs[3], lys[2]),
    T3(lxs[2], lys[2]),
    T3(lxs[2], lys[3]-S_long_lid),
    T3(lxs[3], lys[3]-S_long_lid),
    T3(lxs[3], lys[3]),
    T3(lxs[0], lys[3]),
    T3(lxs[0], lys[3]-S_long_lid),
    T3(lxs[1], lys[3]-S_long_lid),
    T3(lxs[1], lys[2]),
    T3(lxs[0], lys[2]),
    T3(lxs[0], lys[1]),
    T3(lxs[1], lys[1]),
    T3(lxs[1], lys[0]+S_long_lid),
    T3(lxs[0], lys[0]+S_long_lid),
    T3(lxs[0], lys[0]),
]
ax.plot([p[0] for p in lid_outline], [p[1] for p in lid_outline], color='#333333', lw=2, zorder=7)

# ── 折り曲げ線 ──
# 主要折り線（青破線）
for x in [lxs[1], lxs[2]]:
    fold_line(ax, *T3(x, lys[1]), *T3(x, lys[2]), color=CLR_MAIN)
for y in [lys[1], lys[2]]:
    fold_line(ax, *T3(lxs[1], y), *T3(lxs[2], y), color=CLR_MAIN)

# 長辺タブ ２回谷折り線（ブランク全幅）
fold_line(ax, *T3(lxs[0], lys[0]+S_long_lid), *T3(lxs[3], lys[0]+S_long_lid), color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[0], lys[3]-S_long_lid), *T3(lxs[3], lys[3]-S_long_lid), color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[0], lys[0]+S_tab_lid),  *T3(lxs[3], lys[0]+S_tab_lid),  color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[0], lys[3]-S_tab_lid),  *T3(lxs[3], lys[3]-S_tab_lid),  color=CLR_BEND, ls='-.')

# 短辺受け ２回谷折り線（短辺帯）
fold_line(ax, *T3(lxs[0]+S_short_lid, lys[1]), *T3(lxs[0]+S_short_lid, lys[2]), color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[3]-S_short_lid, lys[1]), *T3(lxs[3]-S_short_lid, lys[2]), color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[0]+R_lock_lid,  lys[1]), *T3(lxs[0]+R_lock_lid,  lys[2]), color=CLR_BEND, ls='-.')
fold_line(ax, *T3(lxs[3]-R_lock_lid,  lys[1]), *T3(lxs[3]-R_lock_lid,  lys[2]), color=CLR_BEND, ls='-.')

# 谷折り寸法ラベル（長辺パネル下側）
ax.annotate('', xy=T3(lxs[1]-4/sc3, lys[0]+S_tab_lid),
            xytext=T3(lxs[1]-4/sc3, lys[0]),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T3(lxs[1]-3/sc3, lys[0]+S_tab_lid/2), f'{S_tab_lid}', ha='right', va='center',
        fontsize=7, color=CLR_BEND)
ax.annotate('', xy=T3(lxs[1]-4/sc3, lys[0]+S_long_lid),
            xytext=T3(lxs[1]-4/sc3, lys[0]+S_tab_lid),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T3(lxs[1]-3/sc3, lys[0]+S_tab_lid+T_PLATE), '1', ha='right', va='center',
        fontsize=6, color=CLR_BEND)
ax.annotate('', xy=T3(lxs[1]-4/sc3, lys[1]),
            xytext=T3(lxs[1]-4/sc3, lys[0]+S_long_lid),
            arrowprops=dict(arrowstyle='<->', color=CLR_MAIN, lw=1.0))
ax.text(*T3(lxs[1]-3/sc3, lys[0]+S_long_lid+H_lid/2), f'{H_lid}', ha='right', va='center',
        fontsize=7, color=CLR_MAIN)

# 谷折り寸法ラベル（短辺パネル左側）
ax.annotate('', xy=T3(lxs[0]+R_lock_lid,  lys[1]-4/sc3),
            xytext=T3(lxs[0],             lys[1]-4/sc3),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T3(lxs[0]+R_lock_lid/2, lys[1]-3/sc3), f'{R_lock_lid}', ha='center', va='top',
        fontsize=7, color=CLR_BEND)
ax.annotate('', xy=T3(lxs[0]+S_short_lid, lys[1]-4/sc3),
            xytext=T3(lxs[0]+R_lock_lid,  lys[1]-4/sc3),
            arrowprops=dict(arrowstyle='<->', color=CLR_BEND, lw=1.0))
ax.text(*T3(lxs[0]+R_lock_lid+T_PLATE, lys[1]-3/sc3), '1', ha='center', va='top',
        fontsize=6, color=CLR_BEND)
ax.annotate('', xy=T3(lxs[1],            lys[1]-4/sc3),
            xytext=T3(lxs[0]+S_short_lid, lys[1]-4/sc3),
            arrowprops=dict(arrowstyle='<->', color=CLR_MAIN, lw=1.0))
ax.text(*T3(lxs[0]+S_short_lid+H_lid/2, lys[1]-3/sc3), f'{H_lid}', ha='center', va='top',
        fontsize=7, color=CLR_MAIN)

off3 = 22
dim_arrow(ax, *T3(lxs[0],lys[3]+off3/sc3), *T3(lxs[1],lys[3]+off3/sc3),
          f'{H_lid+S_short_lid}mm', 'top', 8, '#E65100')
dim_arrow(ax, *T3(lxs[1],lys[3]+off3/sc3), *T3(lxs[2],lys[3]+off3/sc3),
          f'W={W_lid}mm', 'top', 9, '#2E7D32')
dim_arrow(ax, *T3(lxs[2],lys[3]+off3/sc3), *T3(lxs[3],lys[3]+off3/sc3),
          f'{H_lid+S_short_lid}mm', 'top', 8, '#E65100')
dim_arrow(ax, *T3(lxs[0],lys[3]+off3*2/sc3), *T3(lxs[3],lys[3]+off3*2/sc3),
          f'全幅 {LW}mm', 'top', 9.5, '#333333')
ox3 = lxs[3]+12
dim_arrow(ax, *T3(ox3,lys[0]), *T3(ox3,lys[1]),
          f'H+タブ\n{H_lid+S_long_lid}mm', 'bottom', 8, '#1565C0')
dim_arrow(ax, *T3(ox3,lys[1]), *T3(ox3,lys[2]),
          f'L={L_lid}mm', 'bottom', 9, '#2E7D32')
dim_arrow(ax, *T3(ox3,lys[2]), *T3(ox3,lys[3]),
          f'H+タブ\n{H_lid+S_long_lid}mm', 'bottom', 8, '#1565C0')
dim_arrow(ax, *T3(ox3+25/sc3,lys[0]), *T3(ox3+25/sc3,lys[3]),
          f'全長 {LH}mm', 'bottom', 9.5, '#333333')

# 折り線凡例
lx3  = T3(lxs[0], 0)[0]
ly3a = T3(0, 0)[1] - 18
ly3b = ly3a - 17
ax.plot([lx3, lx3+18], [ly3a+5.5, ly3a+5.5], ls='--', color=CLR_MAIN, lw=1.5)
ax.text(lx3+22, ly3a+5.5, '折り曲げ線（パネル境界）', fontsize=8, va='center', color='#333333')
ax.plot([lx3, lx3+18], [ly3b+5.5, ly3b+5.5], ls='-.', color=CLR_BEND, lw=1.5)
ax.text(lx3+22, ly3b+5.5,
        f'２回谷折りする（ハゼ構造）: タブ{S_tab_lid}mm ＋ 折りしろ1mm / 受け{R_lock_lid}mm ＋ 折りしろ1mm',
        fontsize=8, va='center', color='#333333')

# 板厚注記（右下）
note3_x = T3(lxs[3], 0)[0] + 42
note3_y = T3(0, 0)[1] - 10
ax.text(note3_x, note3_y,
        f'板厚: {T_PLATE}mm',
        ha='left', va='top', fontsize=9, color='#5D4037',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1', edgecolor='#F57F17', lw=1.5))

plt.savefig('box_03_futakaitenzu.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("box_03_futakaitenzu.png")

# ═══════════════════════════════════════════════
#  図4: 作成手順図（8ステップ）
# ═══════════════════════════════════════════════
fig4, axes = plt.subplots(2, 4, figsize=(20, 10))
fig4.suptitle('【作成手順】 溶接なし・ハゼ折り工法（長辺タブ式）',
              fontsize=15, fontweight='bold', y=1.01)
fig4.patch.set_facecolor('#FAFAFA')

steps = [
    ('① 板取り・切断',         '#E3F2FD'),
    ('② コーナー切取り',       '#FFF8E1'),
    ('③ 長辺を90°折り上げ',   '#E8F5E9'),
    ('④ 長辺タブを外側へ90°折る', '#FCE4EC'),
    ('⑤ 短辺を90°折り上げ',       '#FFF3E0'),
    ('⑥ 受けをタブに被せて固定',   '#F3E5F5'),
    ('⑦ 蓋を同様に作成',       '#E0F7FA'),
    ('⑧ 完成（蓋を載せる）',   '#F9FBE7'),
]

for idx, (ax, (title, bg)) in enumerate(zip(axes.flat, steps)):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_facecolor(bg)
    ax.text(5, 9.5, title, ha='center', va='top', fontsize=10, fontweight='bold', color='#333333')

    if idx == 0:  # ① 板取り
        ax.add_patch(patches.Rectangle((0.5,0.5),9,8, edgecolor='#333',facecolor='#FAFAF0',lw=2))
        ax.add_patch(patches.Rectangle((0.7,1.5),5.2,6.8, edgecolor='#1565C0',facecolor='#BBDEFB',lw=1.5))
        ax.text(3.3,5.0,f'本体ブランク\n{BW}x{BH}mm',ha='center',fontsize=7.5,color='#1565C0',fontweight='bold')
        ax.add_patch(patches.Rectangle((6.2,2.5),3.2,5.1, edgecolor='#B71C1C',facecolor='#FFCDD2',lw=1.5))
        ax.text(7.8,5.0,f'蓋ブランク\n{LW}x{LH}mm',ha='center',fontsize=7.5,color='#B71C1C',fontweight='bold')
        ax.text(5,0.2,'455x455mm 一枚板 → 横並び切り出し',ha='center',fontsize=7.5,color='#333')

    elif idx == 1:  # ② コーナー切取り（全ゾーン色分け）
        # ブランクを縮小して全体を表示
        bx, bw = 0.4, 9.2
        by, bh = 0.3, 8.8
        scx = bw / BW
        scy = bh / BH
        def bpt(rx, ry): return (bx + rx*scx, by + ry*scy)
        def bsz(rw, rh): return (rw*scx, rh*scy)
        def brect(rx, ry, rw, rh, fc, ec='none', lw=0, zo=2, **kw):
            ax.add_patch(patches.Rectangle(bpt(rx,ry), *bsz(rw,rh),
                         facecolor=fc, edgecolor=ec, lw=lw, zorder=zo, **kw))

        # ── Strip 1/5: 長辺タブ帯（橙・全幅 S_long mm）──
        brect(0,           0,        BW, S_long, '#FF8A65')
        brect(0,  BH-S_long,         BW, S_long, '#FF8A65')
        # ── Strip 2/4: 長辺壁（青・中央列）＋ 切り取り（赤・左右コーナー）──
        brect(xs[1], S_long,    W, H, '#BBDEFB')          # 長辺壁 下
        brect(xs[1], ys[2],     W, H, '#BBDEFB')          # 長辺壁 上
        brect(0,     S_long, xs[1], H, '#FFCDD2', ec='#E53935', lw=1.2, zo=3, ls='--')  # 切取り 下左
        brect(xs[2], S_long, xs[1], H, '#FFCDD2', ec='#E53935', lw=1.2, zo=3, ls='--')  # 切取り 下右
        brect(0,     ys[2],  xs[1], H, '#FFCDD2', ec='#E53935', lw=1.2, zo=3, ls='--')  # 切取り 上左
        brect(xs[2], ys[2],  xs[1], H, '#FFCDD2', ec='#E53935', lw=1.2, zo=3, ls='--')  # 切取り 上右
        # ── Strip 3: 底板・短辺壁・受け ──
        brect(xs[1],      ys[1], W, L, '#C8E6C9')          # 底板（緑）
        brect(S_short,    ys[1], H, L, '#FFE0B2')          # 短辺壁 左（橙）
        brect(xs[2],      ys[1], H, L, '#FFE0B2')          # 短辺壁 右（橙）
        brect(0,          ys[1], S_short, L, '#CE93D8', zo=4)   # 受け 左（紫）
        brect(xs[2]+H,    ys[1], S_short, L, '#CE93D8', zo=4)   # 受け 右（紫）

        # ── 切り取りマーク ──
        for cx0 in [0, xs[2]]:
            for cy0 in [S_long, ys[2]]:
                tx, ty = bpt(cx0 + xs[1]*0.5, cy0 + H*0.5)
                ax.text(tx, ty, '✂\n切取り', ha='center', va='center',
                        fontsize=7.5, color='#B71C1C', fontweight='bold', zorder=6)

        # ── 境界線 ──
        for rx in [xs[1], xs[2]]:
            xp = bpt(rx, 0)[0]
            ax.plot([xp]*2, [by, by+bh], '--', color='#0066CC', lw=1.2, zorder=7)
        for ry in [ys[1], ys[2]]:
            yp = bpt(0, ry)[1]
            ax.plot([bx, bx+bw], [yp]*2, '--', color='#0066CC', lw=1.2, zorder=7)
        for ry in [S_long, BH-S_long]:
            yp = bpt(0, ry)[1]
            ax.plot([bx, bx+bw], [yp]*2, '-.', color='#E65100', lw=1.0, zorder=7)
        for rx in [S_short, xs[2]+H]:
            xp = bpt(rx, 0)[0]
            ax.plot([xp]*2, [bpt(0,ys[1])[1], bpt(0,ys[2])[1]], '-.', color='#7B1FA2', lw=1.0, zorder=7)

        # ── 外枠（再描画）──
        ax.add_patch(patches.Rectangle((bx,by), bw, bh,
                     facecolor='none', edgecolor='#333', lw=2, zorder=8))

        # ── ゾーンラベル ──
        ax.text(*bpt(xs[1]+W*0.5, ys[1]+L*0.5),
                '底板', ha='center', va='center',
                fontsize=8, color='#2E7D32', fontweight='bold', zorder=9)
        ax.text(*bpt(xs[1]+W*0.5, S_long+H*0.5),
                f'長辺壁\n{W}×{H}mm', ha='center', va='center',
                fontsize=6.5, color='#1565C0', fontweight='bold', zorder=9)
        ax.text(*bpt(xs[1]+W*0.5, ys[2]+H*0.5),
                f'長辺壁\n{W}×{H}mm', ha='center', va='center',
                fontsize=6.5, color='#1565C0', fontweight='bold', zorder=9)
        ax.text(*bpt(S_short+H*0.5, ys[1]+L*0.5),
                f'短辺壁\n{H}×{L}', ha='center', va='center',
                fontsize=6, color='#BF360C', fontweight='bold', zorder=9)
        ax.text(*bpt(S_short*0.5, ys[1]+L*0.5),
                f'受け\n{S_short}', ha='center', va='center',
                fontsize=6, color='#6A1B9A', fontweight='bold', zorder=9)
        # タブラベル（下）
        ax.text(*bpt(BW*0.5, S_long*0.5),
                f'タブ帯 {S_long}mm（全幅）', ha='center', va='center',
                fontsize=6.5, color='white', fontweight='bold', zorder=9)
        # 切取りサイズ注記（左下コーナー）
        ax.text(*bpt(xs[1]*0.5, S_long + H*0.5),
                f'{int(xs[1])}×{H}\nmm', ha='center', va='center',
                fontsize=6.5, color='#B71C1C', fontweight='bold', zorder=9)
        # タブコーナーサイズ注記（左下タブ）
        ax.text(*bpt(xs[1]*0.5, S_long*0.5),
                f'{int(xs[1])}×{S_long}mm', ha='center', va='center',
                fontsize=6, color='white', fontweight='bold', zorder=9)

        ax.text(5, 0.05,
                f'4隅の赤部を切取り（{int(xs[1])}×{H}mm）　タブ（橙 {int(xs[1])}×{S_long}mm）は残す',
                ha='center', fontsize=8, color='#333',
                bbox=dict(facecolor='#FFF8E1', edgecolor='#FFA000', boxstyle='round'))

    elif idx == 2:  # ③ 長辺を90°折り上げ（断面図）
        y0 = 3.0
        H_s = 3.0
        S_s = H_s * S_long/H  # タブ高さ相当
        ax.add_patch(patches.Rectangle((1.0,y0-0.4),8,0.4,facecolor='#C8E6C9',edgecolor='#2E7D32',lw=2))
        ax.text(5,y0-0.2,'底板',ha='center',va='center',fontsize=8,fontweight='bold',color='#2E7D32')
        ax.add_patch(patches.Rectangle((1.0,y0),0.6,H_s,facecolor='#BBDEFB',edgecolor='#1565C0',lw=2))
        ax.text(1.3,y0+H_s*0.5,'長辺\n壁',ha='center',va='center',fontsize=7.5,color='#1565C0',fontweight='bold')
        ax.add_patch(patches.Rectangle((8.4,y0),0.6,H_s,facecolor='#BBDEFB',edgecolor='#1565C0',lw=2))
        ax.text(8.7,y0+H_s*0.5,'長辺\n壁',ha='center',va='center',fontsize=7.5,color='#1565C0',fontweight='bold')
        ax.add_patch(patches.Rectangle((1.0,y0+H_s),0.6,S_s,facecolor='#E53935',edgecolor='#B71C1C',lw=2.5,zorder=5))
        ax.text(1.3,y0+H_s+S_s*0.5,'T',ha='center',va='center',fontsize=9,color='white',fontweight='bold')
        ax.add_patch(patches.Rectangle((8.4,y0+H_s),0.6,S_s,facecolor='#E53935',edgecolor='#B71C1C',lw=2.5,zorder=5))
        ax.text(8.7,y0+H_s+S_s*0.5,'T',ha='center',va='center',fontsize=9,color='white',fontweight='bold')
        ax.annotate('',xy=(1.6,y0+H_s*0.5),xytext=(3.5,y0-0.2),
                    arrowprops=dict(arrowstyle='->',color='#1565C0',lw=2.0))
        ax.annotate('',xy=(8.4,y0+H_s*0.5),xytext=(6.5,y0-0.2),
                    arrowprops=dict(arrowstyle='->',color='#1565C0',lw=2.0))
        ax.annotate('',xy=(9.5,y0+H_s+S_s),xytext=(9.5,y0),
                    arrowprops=dict(arrowstyle='<->',color='#1565C0',lw=1.5))
        ax.text(9.7,y0+H_s*0.5,f'H+タブ\n={H+S_long}mm',ha='left',va='center',fontsize=7.5,color='#1565C0')
        ax.text(5,1.0,f'長辺側板を折り上げる\nT=タブ{S_long}mmが上に突き出る（4隅）',
                ha='center',fontsize=8.5,color='#333',
                bbox=dict(facecolor='#E8F5E9',edgecolor='#2E7D32',boxstyle='round'))

    elif idx == 3:  # ④ 長辺タブを外側へ90°折る（3D立体図）
        # ── 等角投影：長辺壁のみ、タブの90°折りを示す ──
        ox_c=4.8; oy_c=1.3; di_x=0.62; di_y=0.40
        H_u=3.0; tu=H_u*S_long/H   # タブ高さ（等角単位）
        Lu=4.0
        def p3(x,y,z): return (ox_c-x+z*di_x, oy_c+y+z*di_y)
        ax.text(5,9.65,'【④ 3D図：長辺タブを外側へ90°折る】',
                ha='center',va='top',fontsize=9,fontweight='bold',color='#333')
        # 底板（一部）
        ax.add_patch(patches.Polygon(
            [p3(0,0,0),p3(Lu,0,0),p3(Lu,0,0.45),p3(0,0,0.45)],
            facecolor='#C8E6C9',edgecolor='#2E7D32',lw=2,zorder=1,closed=True))
        ax.text(*p3(Lu*0.5,-0.22,0.2),'底板',ha='center',va='center',
                fontsize=7.5,color='#2E7D32',fontweight='bold')
        # 長辺壁（青）
        ax.add_patch(patches.Polygon(
            [p3(0,0,0),p3(Lu,0,0),p3(Lu,H_u,0),p3(0,H_u,0)],
            facecolor='#BBDEFB',edgecolor='#1565C0',lw=2.5,zorder=4,closed=True))
        ax.text(*p3(Lu*0.5,H_u*0.44,0),f'長辺壁\nH={H}mm',
                ha='center',va='center',fontsize=9,color='#1565C0',fontweight='bold')
        # タブ「折る前」= 垂直（薄い・点線）
        ax.add_patch(patches.Polygon(
            [p3(0,H_u,0),p3(Lu,H_u,0),p3(Lu,H_u+tu,0),p3(0,H_u+tu,0)],
            facecolor='#FFCDD2',edgecolor='#E53935',lw=1.8,zorder=3,
            closed=True,linestyle='--',alpha=0.75))
        bx0,by0 = p3(Lu*0.5,H_u+tu*0.52,0)
        ax.text(bx0,by0,'折る前\n(垂直)',ha='center',va='center',
                fontsize=8,color='#C62828',style='italic')
        # タブ「折った後」= 水平（濃い赤・実線）
        ax.add_patch(patches.Polygon(
            [p3(0,H_u,0),p3(Lu,H_u,0),p3(Lu,H_u,tu),p3(0,H_u,tu)],
            facecolor='#E53935',edgecolor='#B71C1C',lw=2.5,zorder=6,closed=True))
        bx1,by1 = p3(Lu*0.5,H_u+0.18,tu*0.5)
        ax.text(bx1,by1,f'折った後\n(水平 {S_long}mm)',
                ha='center',va='center',fontsize=8,color='white',fontweight='bold')
        # タブ先端の側面エッジ
        ax.add_patch(patches.Polygon(
            [p3(0,H_u-0.06,tu),p3(Lu,H_u-0.06,tu),p3(Lu,H_u,tu),p3(0,H_u,tu)],
            facecolor='#C62828',edgecolor='#B71C1C',lw=1.5,zorder=5,closed=True))
        # 90°カーブ矢印（垂直→水平）
        tip_x,tip_y = p3(Lu*0.2, H_u+0.1, tu)
        src_x,src_y = p3(Lu*0.2, H_u+tu,  0.05)
        ax.annotate('', xy=(tip_x,tip_y), xytext=(src_x,src_y),
                    arrowprops=dict(arrowstyle='->,head_width=0.32,head_length=0.27',
                                   color='#B71C1C',lw=3.5,
                                   connectionstyle='arc3,rad=-0.42'))
        ax.text((tip_x+src_x)*0.5-0.7,(tip_y+src_y)*0.5+0.15,
                '90°\n外側へ！',ha='center',va='center',
                fontsize=11,color='#B71C1C',fontweight='bold')
        ax.text(5,0.38,
                f'長辺壁の上端タブ({S_long}mm)を外側へ90°折り曲げる\n★ 短辺壁を立てる前に折る（4か所）',
                ha='center',fontsize=8.5,color='#333',
                bbox=dict(facecolor='#FCE4EC',edgecolor='#B71C1C',boxstyle='round'))

    elif idx == 4:  # ⑤ 短辺を90°折り上げ（受けはまだ平ら）
        # ── 等角投影：タブ完成＋短辺折り上げ、受けはストレートのまま ──
        ox_c=5.6; oy_c=1.2; di_x=0.62; di_y=0.40
        H_u=2.8; tu=H_u*S_long/H; ru=H_u*S_short/H
        Lu=3.2; Wu=2.0
        def p3(x,y,z): return (ox_c-x+z*di_x, oy_c+y+z*di_y)
        def f3(pts,fc,ec='#333',lw=1.5,zo=2):
            ax.add_patch(patches.Polygon(pts,facecolor=fc,edgecolor=ec,lw=lw,zorder=zo,closed=True))
        ax.text(5,9.65,'【⑤ 3D図：短辺を折り上げ（受けはまだ平ら）】',
                ha='center',va='top',fontsize=8.5,fontweight='bold',color='#333')
        # 底板
        f3([p3(0,0,0),p3(Lu,0,0),p3(Lu,0,Wu),p3(0,0,Wu)],'#C8E6C9','#2E7D32',lw=2,zo=1)
        ax.text(*p3(Lu*0.5,-0.22,Wu*0.4),'底板',ha='center',va='center',
                fontsize=7.5,color='#2E7D32',fontweight='bold')
        # 短辺壁（橙）：受けより下の部分
        f3([p3(0,0,0),p3(0,0,Wu),p3(0,H_u,Wu),p3(0,H_u,0)],'#FFE0B2','#E65100',lw=2,zo=2)
        ax.text(*p3(0,H_u*0.42,Wu*0.5),'短辺壁\n(橙)',ha='center',va='center',
                fontsize=7.5,color='#BF360C',fontweight='bold')
        # 受け帯（紫）：まだ平ら＝短辺壁の上端から真上に伸びたまま
        f3([p3(0,H_u,0),p3(0,H_u,Wu),p3(0,H_u+ru,Wu),p3(0,H_u+ru,0)],'#E1BEE7','#7B1FA2',lw=2.5,zo=3)
        ax.text(*p3(0,H_u+ru*0.5,Wu*0.5),f'受け帯\n{S_short}mm\n（まだ平ら！）',
                ha='center',va='center',fontsize=6.5,color='#4A148C',fontweight='bold')
        # 長辺壁（青）
        f3([p3(0,0,0),p3(Lu,0,0),p3(Lu,H_u,0),p3(0,H_u,0)],'#BBDEFB','#1565C0',lw=2.5,zo=4)
        ax.text(*p3(Lu*0.5,H_u*0.4,0),f'長辺壁\nH={H}mm',
                ha='center',va='center',fontsize=8,color='#1565C0',fontweight='bold')
        # タブ（水平・既に折り済み）上面
        f3([p3(0,H_u,0),p3(Lu,H_u,0),p3(Lu,H_u,tu),p3(0,H_u,tu)],'#E53935','#B71C1C',lw=2.5,zo=6)
        ax.text(*p3(Lu*0.5,H_u+0.15,tu*0.5),f'タブ{S_long}mm\n(水平・折り済み)',
                ha='center',va='center',fontsize=7.5,color='white',fontweight='bold')
        # タブ先端エッジ
        f3([p3(0,H_u-0.06,tu),p3(Lu,H_u-0.06,tu),p3(Lu,H_u,tu),p3(0,H_u,tu)],'#C62828','#B71C1C',lw=1.5,zo=5)
        # 受けがまだ平らで「次に曲げる」を示す注記＋矢印
        rx,ry = p3(0,H_u+ru*0.6,Wu*0.55)
        ax.annotate('この帯を\n次ステップで\nタブに被せる\n↓',
                    xy=(rx,ry), xytext=(3.2,8.6),fontsize=8,ha='center',
                    color='#4A148C',fontweight='bold',
                    arrowprops=dict(arrowstyle='->',color='#7B1FA2',lw=2.2))
        ax.text(5,0.38,
                f'短辺壁({H}mm)を折り上げる　※受け帯({S_short}mm)はまだ真っすぐ\n次ステップでこの受け帯をタブの上に折り曲げてロック',
                ha='center',fontsize=8.5,color='#333',
                bbox=dict(facecolor='#FFF3E0',edgecolor='#E65100',boxstyle='round'))

    elif idx == 5:  # ⑥ 受けをタブに被せて固定（3D立体図）
        # ── 等角投影：受け帯がタブを上から被さってロック ──
        ox_c=5.6; oy_c=1.2; di_x=0.62; di_y=0.40
        H_u=2.8; tu=H_u*S_long/H; ru=H_u*S_short/H
        Lu=3.2; Wu=2.0
        def p3(x,y,z): return (ox_c-x+z*di_x, oy_c+y+z*di_y)
        def f3(pts,fc,ec='#333',lw=1.5,zo=2):
            ax.add_patch(patches.Polygon(pts,facecolor=fc,edgecolor=ec,lw=lw,zorder=zo,closed=True))
        ax.text(5,9.65,'【⑥ 3D図：受けをタブに被せて固定！】',
                ha='center',va='top',fontsize=9,fontweight='bold',color='#1B5E20')
        # 底板
        f3([p3(0,0,0),p3(Lu,0,0),p3(Lu,0,Wu),p3(0,0,Wu)],'#C8E6C9','#2E7D32',lw=2,zo=1)
        # 短辺壁（橙）
        f3([p3(0,0,0),p3(0,0,Wu),p3(0,H_u,Wu),p3(0,H_u,0)],'#FFE0B2','#E65100',lw=2,zo=2)
        ax.text(*p3(0,H_u*0.38,Wu*0.5),'短辺壁',ha='center',va='center',
                fontsize=7.5,color='#BF360C',fontweight='bold')
        # 長辺壁（青）
        f3([p3(0,0,0),p3(Lu,0,0),p3(Lu,H_u,0),p3(0,H_u,0)],'#BBDEFB','#1565C0',lw=2.5,zo=4)
        ax.text(*p3(Lu*0.5,H_u*0.42,0),f'長辺壁\nH={H}mm',
                ha='center',va='center',fontsize=8,color='#1565C0',fontweight='bold')
        # タブ（水平・折り済み）上面
        f3([p3(0,H_u,0),p3(Lu,H_u,0),p3(Lu,H_u,tu),p3(0,H_u,tu)],'#E53935','#B71C1C',lw=2.5,zo=5)
        ax.text(*p3(Lu*0.5,H_u+0.13,tu*0.5),f'タブ\n{S_long}mm',
                ha='center',va='center',fontsize=7,color='white',fontweight='bold')
        # タブ先端エッジ
        f3([p3(0,H_u-0.06,tu),p3(Lu,H_u-0.06,tu),p3(Lu,H_u,tu),p3(0,H_u,tu)],'#C62828','#B71C1C',lw=1.5,zo=4)
        # ★ 受け帯（紫）：タブを上から被せてロック
        #   上面：y3=H_u平面で z3=0..ru に水平展開（タブ{tu}より wide な ru で覆う）
        f3([p3(0,H_u,0),p3(Lu,H_u,0),p3(Lu,H_u,ru),p3(0,H_u,ru)],'#CE93D8','#7B1FA2',lw=2.5,zo=7)
        ax.text(*p3(Lu*0.5,H_u+0.14,ru*0.55),f'受け帯{S_short}mm\n（タブを被さる）',
                ha='center',va='center',fontsize=7,color='#4A148C',fontweight='bold')
        # 受け帯の外側エッジ（ru端で折り返して下に向く腕）
        edge_drop = 0.18
        f3([p3(0,H_u-edge_drop,ru),p3(Lu,H_u-edge_drop,ru),p3(Lu,H_u,ru),p3(0,H_u,ru)],
           '#AB47BC','#7B1FA2',lw=2,zo=6)
        # 断面イメージ（右下に小さなコ字断面を示す）
        sc=0.85; cx=8.2; cy=2.8
        ax.plot([cx,cx+sc*0.15,cx+sc*0.15],[cy,cy,cy+sc*0.55],'#7B1FA2',lw=3.5)  # 受け内腕
        ax.plot([cx,cx+sc*ru/tu*1.1],[cy+sc*0.55,cy+sc*0.55],'#7B1FA2',lw=3.5)  # 受け上面
        ax.plot([cx+sc*ru/tu*1.1,cx+sc*ru/tu*1.1],[cy+sc*0.55,cy+sc*0.55-edge_drop*sc*2],
                '#7B1FA2',lw=3.5)  # 受け外腕
        ax.fill_between([cx+sc*0.1,cx+sc*0.1+sc*tu/tu*0.85],[cy,cy],[cy+sc*0.55,cy+sc*0.55],
                        color='#E53935',alpha=0.85)  # タブ断面
        ax.text(cx-0.15,cy+sc*0.7,'断面',ha='center',fontsize=7.5,color='#555',style='italic')
        ax.text(cx+sc*0.5,cy-0.22,'受けがタブを\n包んで固定',ha='center',fontsize=7.5,color='#7B1FA2',fontweight='bold')
        # ロック完了バッジ
        bx,by = p3(Lu*0.5, H_u*0.5, -0.6)
        ax.text(bx,by,'✓ ハゼ固定完成！\n   溶接なし',
                ha='center',va='center',fontsize=9,color='white',fontweight='bold',
                bbox=dict(facecolor='#1B5E20',edgecolor='#2E7D32',boxstyle='round,pad=0.3'))
        ax.annotate('受け帯がタブを\n上から覆い\n外れない！',
                    xy=p3(Lu*0.4,H_u+0.1,ru*0.6), xytext=(1.5,8.5),fontsize=8.5,ha='center',
                    color='#7B1FA2',fontweight='bold',
                    arrowprops=dict(arrowstyle='->',color='#7B1FA2',lw=2.2))
        ax.text(5,0.38,
                f'受け帯({S_short}mm)をタブ({S_long}mm)に被せて木槌で叩き曲げる\n受けがタブを包んで固定 ＝ 溶接なし（4隅）',
                ha='center',fontsize=8.5,color='#333',
                bbox=dict(facecolor='#F3E5F5',edgecolor='#7B1FA2',boxstyle='round'))

    elif idx == 6:  # ⑦ 本体完成・蓋を同様に作成
        def box3d(ax, ox, oy, bL, bW, bH, fc_top, fc_front, fc_side, ec):
            dx, dy = 0.9, 0.55
            top   = np.array([[ox,oy+bH],[ox+bL,oy+bH],[ox+bL+dx,oy+bH+dy],[ox+dx,oy+bH+dy]])
            front = np.array([[ox,oy],[ox+bL,oy],[ox+bL,oy+bH],[ox,oy+bH]])
            side  = np.array([[ox+bL,oy],[ox+bL+dx,oy+dy],[ox+bL+dx,oy+bH+dy],[ox+bL,oy+bH]])
            ax.add_patch(patches.Polygon(top,   facecolor=fc_top,   edgecolor=ec, lw=1.5))
            ax.add_patch(patches.Polygon(front, facecolor=fc_front, edgecolor=ec, lw=1.5))
            ax.add_patch(patches.Polygon(side,  facecolor=fc_side,  edgecolor=ec, lw=1.5))
        box3d(ax,0.5,2.5,5.5,1.5,2.8,'#C8E6C9','#A5D6A7','#81C784','#2E7D32')
        ax.text(3.5,4.1,'本体完成',ha='center',va='center',fontsize=9,fontweight='bold',color='#1B5E20')
        ax.text(3.5,3.0,'ハゼ4隅固定済み',ha='center',va='center',fontsize=7.5,color='#2E7D32')
        for cx2,cy2 in [(0.5,5.3),(6.0,5.3),(0.5,2.5),(6.0,2.5)]:
            ax.text(cx2,cy2,'H',ha='center',va='center',fontsize=9,color='#B71C1C',fontweight='bold')
        ax.text(3.5,1.8,'H=ハゼ固定（4隅）',ha='center',fontsize=7.5,color='#B71C1C')
        box3d(ax,5.8,1.5,3.3,1.0,0.7,'#E0F7FA','#B2EBF2','#80DEEA','#006064')
        ax.text(7.9,2.5,'蓋',ha='center',fontsize=9,fontweight='bold',color='#006064')
        ax.text(7.9,1.8,f'{LW}x{LH}mm',ha='center',fontsize=7,color='#006064')
        ax.text(7.9,1.3,'同手順で作成',ha='center',fontsize=7.5,color='#006064')
        ax.text(5,0.5,'本体と同じ工程で蓋（高さ18mm）を作成',
                ha='center',fontsize=8.5,color='#333',
                bbox=dict(facecolor='#E0F7FA',edgecolor='#006064',boxstyle='round'))

    elif idx == 7:  # ⑧ 完成
        def box3d2(ax, ox, oy, bL, bW, bH, fc_top, fc_front, fc_side, ec):
            dx, dy = 1.0, 0.65
            top   = np.array([[ox,oy+bH],[ox+bL,oy+bH],[ox+bL+dx,oy+bH+dy],[ox+dx,oy+bH+dy]])
            front = np.array([[ox,oy],[ox+bL,oy],[ox+bL,oy+bH],[ox,oy+bH]])
            side  = np.array([[ox+bL,oy],[ox+bL+dx,oy+dy],[ox+bL+dx,oy+bH+dy],[ox+bL,oy+bH]])
            ax.add_patch(patches.Polygon(top,   facecolor=fc_top,   edgecolor=ec, lw=1.5))
            ax.add_patch(patches.Polygon(front, facecolor=fc_front, edgecolor=ec, lw=1.5))
            ax.add_patch(patches.Polygon(side,  facecolor=fc_side,  edgecolor=ec, lw=1.5))
        box3d2(ax,0.8,1.2,6.2,1.5,3.0,'#C8E6C9','#A5D6A7','#81C784','#2E7D32')
        box3d2(ax,0.8,5.5,6.2,1.5,0.65,'#E0F7FA','#B2EBF2','#80DEEA','#006064')
        ax.annotate('',xy=(3.0,8.5),xytext=(3.0,6.3),
                    arrowprops=dict(arrowstyle='->',color='#006064',lw=2.5))
        ax.text(4.5,9.0,'蓋が上に開く',ha='center',fontsize=9,color='#006064',fontweight='bold')
        ax.text(5,0.7,f'本体内寸 W{W}xL{L}xH{H}mm',ha='center',fontsize=8,color='#2E7D32')
        ax.text(5,0.1,'溶接なし・ハゼ折り 完成！',ha='center',fontsize=9,color='white',fontweight='bold',
                bbox=dict(facecolor='#388E3C',boxstyle='round,pad=0.3'))

fig4.tight_layout(pad=1.0)
plt.savefig('box_04_tejun.png', dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print("box_04_tejun.png")

# ═══════════════════════════════════════════════
#  図5: ハゼ接合 詳細断面図（タブ＋受け構造）
# ═══════════════════════════════════════════════
fig5, axes5 = plt.subplots(1, 3, figsize=(15, 7))
fig5.suptitle(f'【ハゼ接合 詳細断面図】長辺タブ({S_long}mm)＋短辺受け({S_short}mm)でロック',
              fontsize=13, fontweight='bold')

titles5 = [f'STEP A: 展開状態（板厚{T_PLATE}mm）',
           'STEP B: コーナー立面（折り上げ後）',
           'STEP C: ハゼ完成 断面ズームアップ']
for ax5, t5 in zip(axes5, titles5):
    ax5.set_xlim(0,10); ax5.set_ylim(0,10)
    ax5.set_aspect('equal'); ax5.axis('off')
    ax5.set_title(t5, fontsize=10, fontweight='bold', color='#333333')

# ─── STEP A: 長辺タブと短辺受けの展開状態 ───
ax5 = axes5[0]
ax5.set_facecolor('#F5F5F5')
ax5.text(5,9.5,'【展開状態の断面（1コーナー分）】',ha='center',va='top',
         fontsize=8,color='#555')

# 縮尺：全長を10unitに収める
sc_a = 9.0 / (H + S_short + S_long + H)   # ≈ 9/(55+12+10+55)=0.068

def draw_flat_profile(ax5, cx, y_base, label_above=True):
    """1コーナー断面を横に並べる（左から：受け | 短辺 | ＜隙間＞ | 長辺 | タブ）"""
    # 左側の短辺壁 + 受け（受けは最も外側）
    recv_w = S_short * sc_a * 9
    short_w = H * sc_a * 9
    long_w  = H * sc_a * 9
    tab_w   = S_long * sc_a * 9
    h_bar   = 0.5                      # 断面の厚み（模式）
    gap     = 0.4                      # 短辺・長辺の隙間（折り目位置）

    x0 = cx
    # 受け（紫）
    ax5.add_patch(patches.Rectangle((x0,y_base),recv_w,h_bar,
                  facecolor='#CE93D8',edgecolor='#7B1FA2',lw=2))
    ax5.text(x0+recv_w*0.5,y_base+h_bar+0.15,f'{S_short}mm\n受け',
             ha='center',va='bottom',fontsize=6.5,color='#7B1FA2',fontweight='bold')
    # 短辺壁（橙）
    ax5.add_patch(patches.Rectangle((x0+recv_w,y_base),short_w,h_bar,
                  facecolor='#FFE0B2',edgecolor='#E65100',lw=2))
    ax5.text(x0+recv_w+short_w*0.5,y_base+h_bar*0.5,f'短辺H={H}',
             ha='center',va='center',fontsize=7,color='#E65100',fontweight='bold')
    # 谷折り線（受け）
    for ox in [recv_w*T_PLATE*2/S_short, recv_w*R_lock/S_short]:
        ax5.plot([x0+ox,x0+ox],[y_base-0.15,y_base+h_bar+0.15],
                 color='#E65100',lw=1.5,ls='-.')
    # 折り目（長辺|底板の境）
    ax5.plot([x0+recv_w+short_w,x0+recv_w+short_w],[y_base-0.15,y_base+h_bar+0.15],
             color='#1565C0',lw=2,ls='--')
    # 長辺壁（青）
    ax5.add_patch(patches.Rectangle((x0+recv_w+short_w+gap,y_base),long_w,h_bar,
                  facecolor='#BBDEFB',edgecolor='#1565C0',lw=2))
    ax5.text(x0+recv_w+short_w+gap+long_w*0.5,y_base+h_bar*0.5,f'長辺H={H}',
             ha='center',va='center',fontsize=7,color='#1565C0',fontweight='bold')
    # 折り目（長辺|タブの境）
    ax5.plot([x0+recv_w+short_w+gap+long_w]*2,[y_base-0.15,y_base+h_bar+0.15],
             color='#E65100',lw=2,ls='-.')
    # タブ（赤橙）
    ax5.add_patch(patches.Rectangle((x0+recv_w+short_w+gap+long_w,y_base),tab_w,h_bar,
                  facecolor='#FF8A65',edgecolor='#BF360C',lw=2))
    ax5.text(x0+recv_w+short_w+gap+long_w+tab_w*0.5,y_base+h_bar+0.15,f'{S_long}mm\nタブ',
             ha='center',va='bottom',fontsize=6.5,color='#BF360C',fontweight='bold')
    # 谷折り線（タブ）
    for ox2 in [tab_w*T_PLATE*2/S_long, tab_w*S_tab/S_long]:
        ax5.plot([x0+recv_w+short_w+gap+long_w+ox2]*2,[y_base-0.15,y_base+h_bar+0.15],
                 color='#E65100',lw=1.5,ls='-.')

draw_flat_profile(ax5, 0.3, 5.5)

ax5.text(5,4.6,'──── 折り目 ────',ha='center',fontsize=7,color='#888')
ax5.plot([0.3,0.3],[4.8,5.4],color='#E65100',lw=1.5,ls='-.')
ax5.text(0.6,4.65,'谷折り線（２回）',ha='left',fontsize=7,color='#E65100')
ax5.plot([2.2,2.5],[4.8,5.4],color='#1565C0',lw=2,ls='--')
ax5.text(2.7,4.65,'パネル境界折り',ha='left',fontsize=7,color='#1565C0')

ax5.text(5,2.2,
         f'長辺タブ: {S_tab}mm有効＋折りしろ{int(T_PLATE*2)}mm = {S_long}mm\n'
         f'短辺受け: {R_lock}mm有効＋折りしろ{int(T_PLATE*2)}mm = {S_short}mm\n'
         f'板厚T = {T_PLATE}mm',
         ha='center',fontsize=8.5,color='#333',
         bbox=dict(facecolor='white',edgecolor='#999',boxstyle='round'))

# ─── STEP B: 折り上げ後コーナー立面 ───
ax5 = axes5[1]
ax5.set_facecolor('#F5F5F5')
ax5.text(5,9.5,'【コーナー立面：外側から見た図】',ha='center',va='top',
         fontsize=8,color='#555')

H_s  = 3.6
S_s  = H_s * S_long  / H
R_s  = H_s * S_short / H
y0b  = 1.5
# 長辺壁
lx0 = 0.6; lw2 = 3.8
ax5.add_patch(patches.Rectangle((lx0,y0b),lw2,H_s,
              facecolor='#BBDEFB',edgecolor='#1565C0',lw=2))
ax5.text(lx0+lw2*0.5,y0b+H_s*0.4,f'長辺壁\nH={H}mm',
         ha='center',va='center',fontsize=8,color='#1565C0',fontweight='bold')
# 長辺タブ
ax5.add_patch(patches.Rectangle((lx0,y0b+H_s),lw2,S_s,
              facecolor='#E53935',edgecolor='#B71C1C',lw=2.5))
ax5.text(lx0+lw2*0.5,y0b+H_s+S_s*0.5,f'タブ {S_long}mm',
         ha='center',va='center',fontsize=8,color='white',fontweight='bold')
# 2回谷折り線（タブ内）
fold1y = y0b+H_s+S_s*T_PLATE*2/S_long
fold2y = y0b+H_s+S_s*S_tab/S_long
ax5.plot([lx0,lx0+lw2],[fold1y]*2,color='#E65100',lw=1.5,ls='-.',zorder=5)
ax5.plot([lx0,lx0+lw2],[fold2y]*2,color='#E65100',lw=1.5,ls='-.',zorder=5)
# 短辺壁（受けより下）
sx0 = lx0+lw2; sw2 = 2.8
ax5.add_patch(patches.Rectangle((sx0,y0b),sw2,H_s-R_s,
              facecolor='#FFE0B2',edgecolor='#E65100',lw=2))
ax5.text(sx0+sw2*0.5,y0b+(H_s-R_s)*0.45,'短辺壁',
         ha='center',va='center',fontsize=8,color='#E65100',fontweight='bold')
# 受け（紫）
ax5.add_patch(patches.Rectangle((sx0,y0b+H_s-R_s),sw2,R_s,
              facecolor='#CE93D8',edgecolor='#7B1FA2',lw=2))
ax5.text(sx0+sw2*0.5,y0b+H_s-R_s/2,f'受け\n{S_short}mm',
         ha='center',va='center',fontsize=7.5,color='#7B1FA2',fontweight='bold')
# 2回谷折り線（受け内）
rlock_y = y0b+H_s-R_s+R_s*R_lock/S_short
rfold_y = y0b+H_s-R_s+R_s*T_PLATE*2/S_short
ax5.plot([sx0,sx0+sw2],[rlock_y]*2,color='#E65100',lw=1.5,ls='-.',zorder=5)
ax5.plot([sx0,sx0+sw2],[rfold_y]*2,color='#E65100',lw=1.5,ls='-.',zorder=5)
# 底板
ax5.add_patch(patches.Rectangle((lx0-0.2,y0b-0.35),lw2+sw2+0.4,0.35,
              facecolor='#C8E6C9',edgecolor='#2E7D32',lw=1.5))
# 寸法
ax5.plot([sx0+sw2+0.1]*2,[y0b,y0b+H_s+S_s],color='#1565C0',lw=1.5,ls=':')
ax5.annotate('',xy=(sx0+sw2+0.5,y0b+H_s+S_s),xytext=(sx0+sw2+0.5,y0b),
             arrowprops=dict(arrowstyle='<->',color='#1565C0',lw=1.5))
ax5.text(sx0+sw2+0.7,y0b+H_s*0.5,f'H+T\n={H+S_long}mm',ha='left',va='center',fontsize=7,color='#1565C0')
ax5.text(5,0.6,f'タブ({S_long}mm)が受け上端から突き出た状態\n次ステップで木槌で叩き込む',
         ha='center',fontsize=8.5,color='#333',
         bbox=dict(facecolor='#FFF3E0',edgecolor='#E65100',boxstyle='round'))

# ─── STEP C: ハゼ完成 断面ズームアップ ───
ax5 = axes5[2]
ax5.set_facecolor('#F0FFF0')
ax5.text(5,9.5,'【ズームアップ断面：1コーナー】',ha='center',va='top',
         fontsize=8,color='#333',fontweight='bold')

# 断面パラメータ（拡大表示）
Hc  = 4.0                      # 55mmウォール高さ(plot)
Sc  = Hc * S_long  / H         # タブ高さ
Rc  = Hc * S_short / H         # 受け高さ
Rl  = Hc * R_lock  / H         # 有効受け深さ
tc  = 0.28                     # 板厚
y0c = 1.2
# 長辺壁（青：左）
lwall_x = 1.0; lwall_w = 3.0
ax5.add_patch(patches.Rectangle((lwall_x,y0c),lwall_w,Hc,
              facecolor='#BBDEFB',edgecolor='#1565C0',lw=2,zorder=2))
ax5.text(lwall_x+lwall_w*0.5,y0c+Hc*0.35,f'長辺壁\nH={H}mm',
         ha='center',va='center',fontsize=8,color='#1565C0',fontweight='bold')
# 短辺壁 edge-on（橙：右）
swall_x = lwall_x+lwall_w
ax5.add_patch(patches.Rectangle((swall_x,y0c),tc,Hc-Rc,
              facecolor='#FFE0B2',edgecolor='#E65100',lw=2,zorder=3))
# 受け（紫 Cポケット）
#  ポケットは内側(=長辺方向)に開く
ax5.add_patch(patches.Rectangle((swall_x,y0c+Hc-Rc),tc,Rc,       # 外壁
              facecolor='#CE93D8',edgecolor='#7B1FA2',lw=2,zorder=4))
ax5.add_patch(patches.Rectangle((swall_x-Rl,y0c+Hc-Rc),Rl,tc,   # ポケット底
              facecolor='#CE93D8',edgecolor='#7B1FA2',lw=2,zorder=4))
ax5.add_patch(patches.Rectangle((swall_x-Rl,y0c+Hc-Rc),tc,Rc,   # 内壁
              facecolor='#CE93D8',edgecolor='#7B1FA2',lw=2,zorder=4))
# ── タブ（コ字：受けポケットに噛み合わせた状態）──
#  天板：受けをまたぐ（swall_x方向）
ax5.add_patch(patches.Rectangle((swall_x-Sc,y0c+Hc),Sc+tc,tc,
              facecolor='#E53935',edgecolor='#B71C1C',lw=2.5,zorder=7))
#  外垂直腕：ポケット内壁の外側を抱える
ax5.add_patch(patches.Rectangle((swall_x-Sc,y0c+Hc-Rc-tc),tc,Rc+tc,
              facecolor='#E53935',edgecolor='#B71C1C',lw=2.5,zorder=7))
# 短辺壁ラベル
ax5.text(swall_x+tc+0.15,y0c+(Hc-Rc)*0.5,'短辺\n壁',
         ha='left',va='center',fontsize=7,color='#E65100',fontweight='bold')
ax5.text(swall_x+tc+0.15,y0c+Hc-Rc*0.5,'受け\n→',
         ha='left',va='center',fontsize=7,color='#7B1FA2',fontweight='bold')
# タブ寸法注記
ax5.annotate('',xy=(swall_x-Sc,y0c+Hc+tc*1.5),xytext=(swall_x,y0c+Hc+tc*1.5),
             arrowprops=dict(arrowstyle='<->',color='#B71C1C',lw=1.5))
ax5.text(swall_x-Sc*0.5,y0c+Hc+tc*3.5,f'タブ\n{S_long}mm',
         ha='center',fontsize=7,color='#B71C1C',fontweight='bold')
# 受け寸法注記
ax5.annotate('',xy=(swall_x-Rl,y0c+Hc-Rc-tc-0.15),xytext=(swall_x,y0c+Hc-Rc-tc-0.15),
             arrowprops=dict(arrowstyle='<->',color='#7B1FA2',lw=1.5))
ax5.text(swall_x-Rl*0.5,y0c+Hc-Rc-tc-0.4,f'受け{S_short}mm',
         ha='center',fontsize=7,color='#7B1FA2',fontweight='bold')
# ロック注記
ax5.annotate('タブが\nポケットに\nはまり\nロック！',
             xy=(swall_x-Sc*0.5,y0c+Hc-Rc*0.5),
             xytext=(swall_x-Sc*0.5-1.8,y0c+Hc-Rc*0.5+1.0),
             fontsize=8,ha='center',color='#B71C1C',fontweight='bold',
             arrowprops=dict(arrowstyle='->',color='#B71C1C',lw=1.8))
# 底板
ax5.add_patch(patches.Rectangle((lwall_x-0.15,y0c-0.3),lwall_w+tc+0.3,0.3,
              facecolor='#C8E6C9',edgecolor='#2E7D32',lw=1.5))
ax5.text(lwall_x+lwall_w*0.5,y0c-0.15,'底板',
         ha='center',va='center',fontsize=7.5,color='#2E7D32')
ax5.text(5,0.4,f'ハゼ完成：溶接不要・板厚{T_PLATE}mm・4隅すべて同処理',
         ha='center',fontsize=8.5,color='white',fontweight='bold',
         bbox=dict(facecolor='#388E3C',boxstyle='round,pad=0.3'))

fig5.tight_layout()
plt.savefig('box_05_haze_detail.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("box_05_haze_detail.png")

print("\n=== 全図完成 ===")
print("box_01_itatorie.png    : 板取り図（横並び配置）")
print("box_02_honkaitenzu.png : 本体展開図（タブ=長辺）")
print("box_03_futakaitenzu.png: 蓋展開図（タブ=長辺）")
print("box_04_tejun.png       : 作成手順図（8ステップ）")
print("box_05_haze_detail.png : ハゼ接合詳細断面図")
print(f"\n【本体内寸】W{W} x L{L} x H{H} mm  板厚{T_PLATE}mm")
print(f"【ブランク】本体: {BW}x{BH}mm  蓋: {LW}x{LH}mm")
print(f"【ハゼしろ】本体タブ: {S_long}mm(長辺T+T+{S_tab})  受け: {S_short}mm(短辺T+T+{R_lock})")
print(f"           蓋タブ: {S_long_lid}mm(長辺)  蓋受け: {S_short_lid}mm(短辺)")
print(f"【コーナー切取り】本体: {H+S_short}x{H}mm x4  蓋: {H_lid+S_short_lid}x{H_lid}mm x4")
print(f"【コーナータブ】  本体: {H+S_short}x{S_long}mm x4  蓋: {H_lid+S_short_lid}x{S_long_lid}mm x4")
