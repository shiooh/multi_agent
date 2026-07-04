import os
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch

def visualizer(all_agents_history, nomal_agents_history, adversal_agents_history, visible_graph, show_arrow=True):
    print("Visualizing ...")
    
    all_history = np.array(all_agents_history)       # N × update_times × 2
    normal_history = np.array(nomal_agents_history)   # N-F × update_times × 2
    advers_history = np.array(adversal_agents_history) # F × update_times × 2
    
    N = all_history.shape[0]
    update_times = all_history.shape[1]
    
    fig, ax = plt.subplots(figsize=(7, 7))

    # 初期化
    scat_nomal = ax.scatter([], [], c='blue', label='Nomal Agents', s=70)
    scat_adversal = ax.scatter([], [], c='red', label='Adversal Agents', s=70)
    edge_indices = [(i, j) for i in range(N) for j in visible_graph[i]]
    
    # 矢印のビジュアル設定
    if show_arrow:
        arrow_patches = [
            FancyArrowPatch(
                (0, 0), (0, 0),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=1.6,
                color='gray',
                alpha=0.45,
            )
            for _ in edge_indices
        ]
        for patch in arrow_patches:
            ax.add_patch(patch)

    # テキストオブジェクトをあらかじめ作っておく
    text_labels = [
        ax.text(
            0, 0, '', fontsize=8, color='black', ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.2),
            visible=False
        )
        for _ in range(N)
    ]

    # プロットの表示範囲の設定
    x_min, x_max = all_history[:, :, 0].min(), all_history[:, :, 0].max()
    y_min, y_max = all_history[:, :, 1].min(), all_history[:, :, 1].max()
    
    x_range = max(x_max - x_min, 1e-6)
    y_range = max(y_max - y_min, 1e-6)
    x_padding = max(x_range * 0.08, 1.0)
    y_padding = max(y_range * 0.08, 1.0)

    ax.set_xlim(x_min - x_padding, x_max + x_padding)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_title("Agents Simulation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=True)
    fig.subplots_adjust(bottom=0.2)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, weight='bold')

    # 時刻 t のプロットを行う
    def _animate(t):
        scat_nomal.set_offsets(normal_history[:, t, :])
        if advers_history.size > 0:
            scat_adversal.set_offsets(advers_history[:, t, :])

        current_positions = all_history[:, t, :]
        grouped_positions = []
        
        for idx in range(N):
            pos = current_positions[idx]
            matched_group = None

            for group in grouped_positions:
                if np.allclose(pos, group['position'], atol=1e-3, rtol=0.0):
                    matched_group = group
                    break
            if matched_group is None:
                grouped_positions.append({'position': pos, 'indices': [idx]})
            else:
                matched_group['indices'].append(idx)

        for label in text_labels:
            label.set_visible(False)

        num_groups = len(grouped_positions)
        for group_idx, group in enumerate(grouped_positions):
            label = text_labels[group_idx]
            label.set_visible(True)
            
            x_pos, y_pos = group['position']
            offset_radius = 0.8
            offset_x = offset_radius * np.cos(2 * np.pi * group_idx / max(1, num_groups))
            offset_y = offset_radius * np.sin(2 * np.pi * group_idx / max(1, num_groups))
            label.set_position((x_pos + offset_x, y_pos + offset_y))

            indices = group['indices']
            if len(indices) == 1:
                label_text = str(indices[0])
            else:
                label_text = '[' + ','.join(map(str, indices)) + ']'
            label.set_text(label_text)

        # 有向辺をプロット
        if show_arrow:
            for patch, (i, j) in zip(arrow_patches, edge_indices):
                start_pos = current_positions[j]
                end_pos = current_positions[i]
                patch.set_positions((start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))

        # 現在時刻を表示
        time_text.set_text(f'Time: {t}')

        if show_arrow:
            return scat_nomal, scat_adversal, *arrow_patches, leg, time_text, *text_labels

        return scat_nomal, scat_adversal, leg, time_text, *text_labels

    # 全時刻のプロットを集めてアニメーションにする
    os.makedirs('out', exist_ok=True)
    ani = animation.FuncAnimation(
        fig, _animate, frames=update_times, interval=100, blit=True, repeat=False
    )
    ani.save('out/visualizer.mp4')
    print("Saved animation to out/visualizer.mp4")
    plt.close()
    return