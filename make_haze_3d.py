#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ハゼ折り 3D解説図  ステップ⑤・⑥  (box_06_haze_3d.py)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# フォント設定
for fn in ['MS Gothic','IPAGothic','TakaoGothic','Noto Sans CJK JP']:
    try:
        matplotlib.font_manager.findfont(fn, fallback_to_default=False)
        matplotlib.rcParams['font.family'] = fn
        print(f"font: {fn}"); break
    except: pass

# ── 斜投影関数 ──────────────────────────────
def ob(x, y, z, ang=32, sc=0.52):
    a = math.radians(ang)
    return x + z*sc*math.cos(a), y + z*sc*math.sin(a)

def poly(ax, pts3d, **kw):
    ax.add_patch(patches.Polygon(np.array([ob(*p) for p in pts3d]), **kw))

# ── 寸法（画面単位、55mm≒4.0）────────────────
H  = 4.0    # 側板高さ H=55mm
S  = 0.87   # タブ高さ  S=12mm
Lw = 5.5    # 長辺表示幅（見やすく短縮）
Wd = 3.2    # 短辺表示奥行
Th = 0.17   # 板厚

# ── 全体レイアウト ────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(24, 13))
fig.patch.set_facecolor('#F7F7F7')
fig.suptitle('ハゼ折り コーナー固定の仕組み  ⑤タブ折り → ⑥ハゼ完成',
             fontsize=21, fontweight='bold', color='#1A1A1A', y=0.99)

# ════════════════════════════════════════════════
#   左パネル：ステップ⑤  タブを90°外側へ折る
# ════════════════════════════════════════════════
ax = axes[0]
ax.set_facecolor('#EEF0FF')
ax.set_xlim(-2.5, 12.5)
ax.set_ylim(-2.0, 11.5)
ax.set_aspect('equal')
ax.axis('off')

ax.text(5.0, 11.1,
        '⑤  タブを 90° 外側へ折り曲げる',
        ha='center', va='top', fontsize=17, fontweight='bold', color='#1A237E',
        bbox=dict(facecolor='#C5CAE9', edgecolor='#3F51B5', boxstyle='round,pad=0.4'))

# ── 底板 ──
poly(ax, [(0,0,0),(Lw,0,0),(Lw,0,Wd),(0,0,Wd)],
     fc='#A5D6A7', ec='#388E3C', lw=1.5, alpha=0.85, zorder=1)
ax.text(*ob(Lw*0.5, 0.07, Wd*0.5), '底  板',
        ha='center', fontsize=10, color='#1B5E20', zorder=2)

# ── 長辺側板 前面 ──
poly(ax, [(0,0,0),(Lw,0,0),(Lw,H,0),(0,H,0)],
     fc='#BBDEFB', ec='#1565C0', lw=3, zorder=3)
ax.text(*ob(Lw*0.42, H*0.46, 0),
        '長辺側板\nH = 55 mm',
        ha='center', va='center', fontsize=12, color='#0D47A1',
        fontweight='bold', zorder=10)

# 長辺 上面（板厚）
poly(ax, [(0,H,0),(Lw,H,0),(Lw,H,Th),(0,H,Th)],
     fc='#64B5F6', ec='#1565C0', lw=1.5, zorder=4)

# ── 短辺側板 本体（高さH） ──
poly(ax, [(Lw,0,0),(Lw,0,Wd),(Lw,H,Wd),(Lw,H,0)],
     fc='#FFE0B2', ec='#E65100', lw=3, zorder=5)
ax.text(*ob(Lw, H*0.42, Wd*0.58),
        '短辺側板\nH = 55 mm',
        ha='left', va='center', fontsize=12, color='#BF360C',
        fontweight='bold', zorder=10)

# ── タブ（短辺上端12mm、まだ上向き） ──
poly(ax, [(Lw,H,0),(Lw,H,Wd),(Lw,H+S,Wd),(Lw,H+S,0)],
     fc='#EF5350', ec='#B71C1C', lw=3, zorder=6)
ax.text(*ob(Lw, H + S*0.5, Wd*0.55),
        'タブ  12mm',
        ha='left', va='center', fontsize=13, color='#B71C1C',
        fontweight='bold', zorder=10)

# ── 長辺上端ライン（破線） ──
p1 = ob(0, H, 0);  p2 = ob(Lw, H, 0)
ax.plot([p1[0],p2[0]], [p1[1],p2[1]],
        color='#1565C0', lw=2.5, ls='--', zorder=7, label='長辺上端')
ax.text(p1[0]-0.2, p1[1]+0.05, '長辺上端',
        ha='right', va='bottom', fontsize=10.5, color='#1565C0', fontweight='bold')

# ── 寸法 ──
qa = ob(Lw+0.5, 0, 0)
qb = ob(Lw+0.5, H, 0)
qc = ob(Lw+0.5, H+S, 0)
ax.annotate('', xy=qb, xytext=qa,
            arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=1.8))
ax.text(qb[0]+0.18, (qa[1]+qb[1])/2, 'H=55mm',
        ha='left', va='center', fontsize=10.5, color='#1565C0')
ax.annotate('', xy=qc, xytext=qb,
            arrowprops=dict(arrowstyle='<->', color='#B71C1C', lw=2.2))
ax.text(qb[0]+0.18, (qb[1]+qc[1])/2, 'T=12mm\n(タブ)',
        ha='left', va='center', fontsize=11, color='#B71C1C', fontweight='bold')

# ── タブ折り曲げ矢印（弧） ──
pf = ob(Lw, H+S*0.5, 0)
pe = ob(Lw-0.05, H+0.05, 0)
ax.annotate('', xy=(pe[0]-0.55, pe[1]-0.08),
            xytext=(pf[0]-0.3, pf[1]+0.12),
            arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=4.5,
                           connectionstyle='arc3,rad=0.52'), zorder=11)
ax.text(pf[0]-3.8, pf[1]+1.4,
        '← 外側へ\n   90° 折る！',
        ha='center', fontsize=15, color='#B71C1C', fontweight='bold',
        bbox=dict(facecolor='#FFEBEE', edgecolor='#B71C1C',
                  boxstyle='round,pad=0.5'), zorder=12)

# ── 補足説明 ──
ax.text(4.8, -1.5,
        '短辺の上端タブ（赤）は長辺より12mm高く突き出している\n'
        'このタブを「外側＝長辺の正面方向」へ 90° 折り倒す',
        ha='center', fontsize=12, color='#222',
        bbox=dict(facecolor='#FFF9C4', edgecolor='#F9A825',
                  boxstyle='round,pad=0.45'))


# ════════════════════════════════════════════════
#   右パネル：ステップ⑥  タブ叩き → ハゼ完成
# ════════════════════════════════════════════════
ax = axes[1]
ax.set_facecolor('#E8F5E9')
ax.set_xlim(-2.5, 12.5)
ax.set_ylim(-2.0, 11.5)
ax.set_aspect('equal')
ax.axis('off')

ax.text(5.0, 11.1,
        '⑥  タブを叩いて長辺外面に密着 → ハゼ完成',
        ha='center', va='top', fontsize=17, fontweight='bold', color='#1B5E20',
        bbox=dict(facecolor='#C8E6C9', edgecolor='#388E3C', boxstyle='round,pad=0.4'))

# ── 底板 ──
poly(ax, [(0,0,0),(Lw,0,0),(Lw,0,Wd),(0,0,Wd)],
     fc='#A5D6A7', ec='#388E3C', lw=1.5, alpha=0.85, zorder=1)
ax.text(*ob(Lw*0.5, 0.07, Wd*0.5), '底  板',
        ha='center', fontsize=10, color='#1B5E20', zorder=2)

# ── 長辺側板 前面 ──
poly(ax, [(0,0,0),(Lw,0,0),(Lw,H,0),(0,H,0)],
     fc='#BBDEFB', ec='#1565C0', lw=3, zorder=3)
ax.text(*ob(Lw*0.38, H*0.4, 0),
        '長辺側板\nH = 55 mm',
        ha='center', va='center', fontsize=12, color='#0D47A1',
        fontweight='bold', zorder=10)

# ── 長辺 上面 ──
poly(ax, [(0,H,0),(Lw,H,0),(Lw,H,Th),(0,H,Th)],
     fc='#90CAF9', ec='#1565C0', lw=1.5, zorder=4)

# ── 短辺側板 ──
poly(ax, [(Lw,0,0),(Lw,0,Wd),(Lw,H,Wd),(Lw,H,0)],
     fc='#FFE0B2', ec='#E65100', lw=3, zorder=5)
ax.text(*ob(Lw, H*0.42, Wd*0.58),
        '短辺側板', ha='left', va='center',
        fontsize=12, color='#BF360C', fontweight='bold', zorder=10)

# ── タブ「コ」字 ──
# ① 長辺正面に密着した垂直部（y=H-S〜H, z=0の面）
poly(ax, [(0,H-S,0),(Lw,H-S,0),(Lw,H,0),(0,H,0)],
     fc='#E53935', ec='#B71C1C', lw=2.5, zorder=7)
ax.text(*ob(Lw*0.48, H-S*0.5, 0),
        'タブ密着（垂直部）', ha='center', va='center',
        fontsize=11, color='white', fontweight='bold', zorder=11)

# ② 長辺上端をまたぐ水平部（y=H, z=0〜Th）
poly(ax, [(0,H,0),(Lw,H,0),(Lw,H,Th),(0,H,Th)],
     fc='#EF5350', ec='#B71C1C', lw=2, zorder=8)

# ── ハゼ完成マーク ──
ax.text(*ob(Lw+0.25, H, 0),
        ' ◎ ハゼ完成！',
        ha='left', va='center', fontsize=13, color='#1B5E20', fontweight='bold')

# ── 「コ」字の説明矢印 ──
cpx, cpy = ob(Lw*0.5, H, 0)
ax.annotate('「コ」字タブが\n長辺の上端を\nクリップのように\n抱え込む！\n→ 外れない！',
            xy=(cpx, cpy),
            xytext=(cpx - 4.8, cpy + 2.8),
            fontsize=13, ha='center', color='#B71C1C', fontweight='bold',
            bbox=dict(facecolor='#FFEBEE', edgecolor='#B71C1C',
                      boxstyle='round,pad=0.5'),
            arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=3),
            zorder=12)

# ══════════════════════════════════════
#   断面インセット（右下に大きく配置）
# ══════════════════════════════════════
# 「コ」字断面を誰でも分かる大きさで描く
ix, iy = 7.2, -0.2
iH  = 4.2    # 長辺高さ（断面）
iS  = 0.92   # タブ高さ
iT2 = 0.52   # 板厚（断面）

# 背景
ax.add_patch(patches.FancyBboxPatch((ix-1.1, iy-0.3), 4.8, iH+iS+1.8,
             boxstyle='round,pad=0.15',
             fc='#FFFDE7', ec='#F57F17', lw=2, zorder=11))
ax.text(ix+1.25, iy+iH+iS+1.3,
        'コーナー断面図\n（横から切って見た図）',
        ha='center', fontsize=11, color='#555', zorder=12)

# 長辺断面（青ブロック）
ax.add_patch(patches.Rectangle((ix, iy), iT2, iH,
             fc='#1565C0', ec='#0D47A1', lw=2.5, zorder=12))
ax.text(ix+iT2*0.5, iy+iH*0.5, '長\n辺',
        ha='center', va='center', fontsize=10, color='white',
        fontweight='bold', zorder=13)
ax.text(ix-0.7, iy-0.18, '長辺の\n外面↓', ha='center', fontsize=9, color='#1565C0')

# 短辺断面（橙ブロック）
ax.add_patch(patches.Rectangle((ix+iT2, iy), iT2, iH,
             fc='#E65100', ec='#BF360C', lw=2.5, zorder=12))
ax.text(ix+iT2*1.5, iy+iH*0.5, '短\n辺',
        ha='center', va='center', fontsize=10, color='white',
        fontweight='bold', zorder=13)

# タブ水平部（赤、長辺上端をまたぐ）
ax.add_patch(patches.Rectangle((ix - iS, iy+iH),
             iS + iT2*2 + 0.05, iT2*0.9,
             fc='#E53935', ec='#B71C1C', lw=2.5, zorder=12))

# タブ垂直部（赤、長辺外面を押さえる）
ax.add_patch(patches.Rectangle((ix - iS, iy+iH - iS),
             iT2*0.9, iS + iT2*0.9,
             fc='#E53935', ec='#B71C1C', lw=2.5, zorder=12))

# 「コ」字ラベル
ax.text(ix - iS*0.45, iy+iH+iT2*1.2,
        'タブ水平部\n（上端を越える）',
        ha='center', va='bottom', fontsize=9, color='#B71C1C', fontweight='bold')
ax.text(ix - iS - 0.05, iy+iH - iS*0.5,
        'タブ\n垂直部\n（外面\nに密着）',
        ha='right', va='center', fontsize=9, color='#B71C1C', fontweight='bold')

# フック矢印（なぜ外れないか）
ax.annotate('この「角」が\n引き抜きを防ぐ\n（フック効果）',
            xy=(ix, iy+iH),
            xytext=(ix+1.5, iy+iH+0.8),
            fontsize=10, ha='left', color='#7B1FA2', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2),
            zorder=14)

# ── 補足説明 ──
ax.text(4.8, -1.5,
        '木槌でタブを叩くと「コ」字クリップになる\n'
        '→ タブが長辺の上端に引っ掛かり、引いても外れない！（4隅同じ）',
        ha='center', fontsize=12, color='#222',
        bbox=dict(facecolor='#E8F5E9', edgecolor='#388E3C',
                  boxstyle='round,pad=0.45'))

# ════════════════════════════════════════
plt.tight_layout(pad=2.5)
out = 'box_06_haze_3d.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#F7F7F7')
print(f'✓ {out}')
