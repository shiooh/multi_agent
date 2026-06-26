import os
import numpy as np
import itertools

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch

def visualizer(all_agents_history, nomal_agents_history, adversal_agents_history, visible_graph):
    print("Visualizing ...")
    ## all_agents_history : N × update_times × dimension
    ## nomal_agents_history : N-F × update_times × dimension
    ## adversal_agents_history : F × update_times × dimension
    N = len(all_agents_history)
    update_times = len(all_agents_history[0])
    fig, ax = plt.subplots(figsize=(7, 7))

    # 初期化
    scat_nomal = ax.scatter([], [], c='blue', label='Nomal Agents', s=70)
    scat_adversal = ax.scatter([], [], c='red', label='Adversal Agents', s=70)
    edge_indices = [(i, j) for i in range(N) for j in visible_graph[i]]
    
    # 矢印のビジュアル設定
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

    # Agent番号のラベルづけの設定
    text_labels = []

    # プロットの設定
    x = [agent_history[t][0] for t in range(update_times) for agent_history in itertools.chain(nomal_agents_history, adversal_agents_history)]
    y = [agent_history[t][1] for t in range(update_times) for agent_history in itertools.chain(nomal_agents_history, adversal_agents_history)]

    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
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
        x_nomal = [agent_history[t][0] for agent_history in nomal_agents_history]
        y_nomal = [agent_history[t][1] for agent_history in nomal_agents_history]
        x_adversal = [agent_history[t][0] for agent_history in adversal_agents_history]
        y_adversal = [agent_history[t][1] for agent_history in adversal_agents_history]

        scat_nomal.set_offsets(np.c_[x_nomal, y_nomal])
        scat_adversal.set_offsets(np.c_[x_adversal, y_adversal])

        # 点とAgent番号のプロット
        grouped_positions = []
        for idx, agent_history in enumerate(all_agents_history):
            x_pos = agent_history[t][0]
            y_pos = agent_history[t][1]
            pos = np.array([x_pos, y_pos])
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

        for group_idx, group in enumerate(grouped_positions):
            if group_idx >= len(text_labels):
                text_labels.append(
                    ax.text(
                        0, 0, '', fontsize=8, color='black', ha='left', va='bottom',
                        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.2)
                    )
                )

            label = text_labels[group_idx]
            label.set_visible(True)
            x_pos = group['position'][0]
            y_pos = group['position'][1]
            offset_radius = 0.8
            offset_x = offset_radius * np.cos(2 * np.pi * group_idx / max(1, len(grouped_positions)))
            offset_y = offset_radius * np.sin(2 * np.pi * group_idx / max(1, len(grouped_positions)))
            label.set_position((x_pos + offset_x, y_pos + offset_y))

            indices = group['indices']
            if len(indices) == 1:
                label_text = str(indices[0])
            else:
                label_text = '[' + ','.join(map(str, indices)) + ']'
            label.set_text(label_text)

        # 有向辺をプロット
        for patch, (i, j) in zip(arrow_patches, edge_indices):
            start_pos = all_agents_history[j][t]
            end_pos = all_agents_history[i][t]
            patch.set_positions((start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
        time_text.set_text(f'Time: {t}')

        return scat_nomal, scat_adversal, *arrow_patches, leg, time_text, *text_labels


    # 全時刻のプロットを集めてアニメーションにする
    os.makedirs('out', exist_ok=True)
    ani = animation.FuncAnimation(
        fig, _animate, frames=update_times, interval=100, blit=True, repeat=False
    )
    ani.save('out/visualizer.mp4')
    print("Saved animation to out/visualizer.mp4")
    plt.close()
    return