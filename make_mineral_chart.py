import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = ['Meiryo', 'MS Gothic', 'Yu Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(13, 5))
fig.patch.set_facecolor('#F8F8F8')
ax.set_facecolor('#F8F8F8')

minerals_labels = [
    'ボーキサイト\n（世界計 約444百万t）',
    'アルミニウム\n（世界計 約72百万t）',
    'ガリウム\n（世界計 約600t）',
]

data_list = [
    {'countries': ['オーストラリア', '中国', 'ギニア', 'その他'],
     'values': [18.7, 15.3, 10.1, 55.9]},
    {'countries': ['中国', 'インド', 'ロシア', 'その他'],
     'values': [59.7, 5.8, 5.3, 29.2]},
    {'countries': ['中国', 'ロシア', '日本', 'その他'],
     'values': [98.0, 0.8, 0.7, 0.5]},
]

# 1位=赤, 2位=青, 3位=緑, その他=グレー
colors = ['#C62828', '#1565C0', '#2E7D32', '#BDBDBD']
y_pos = np.arange(len(minerals_labels))
bar_height = 0.55

for i, d in enumerate(data_list):
    left = 0
    for j, (country, val) in enumerate(zip(d['countries'], d['values'])):
        ax.barh(i, val, left=left, height=bar_height,
                color=colors[j], edgecolor='white', linewidth=1.5)
        if val >= 7:
            ax.text(left + val / 2, i,
                    f'{country}\n{val:.1f}%',
                    ha='center', va='center', fontsize=10,
                    color='white', fontweight='bold')
        left += val

# ガリウムの2・3位は棒が細すぎるため注記
ax.text(0.5, -0.08,
        '※ ガリウム: 2位 ロシア 0.8% / 3位 日本 0.7%（棒が細すぎるため表示省略）',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=9, color='#666666', style='italic')

ax.set_xlim(0, 100)
ax.set_ylim(-0.5, len(minerals_labels) - 0.45)
ax.set_yticks(y_pos)
ax.set_yticklabels(minerals_labels, fontsize=11)
ax.set_xlabel('生産シェア (%)', fontsize=11)
ax.set_title('主要鉱物の生産国シェア比較（2024年）\n上位3カ国＋その他',
             fontsize=14, fontweight='bold', pad=14)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3, linestyle='--', color='gray')

legend_patches = [mpatches.Patch(color=c, label=l)
                  for c, l in zip(colors, ['1位', '2位', '3位', 'その他'])]
ax.legend(handles=legend_patches, loc='lower right', fontsize=10,
          title='順位', title_fontsize=10, framealpha=0.9, edgecolor='#CCCCCC')

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
output_path = r'C:\Users\shondo\Desktop\agent_project\mineral_production_share.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#F8F8F8')
print(f'保存完了: {output_path}')
