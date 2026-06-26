        
def visualizer():
    update_times = len(self.agents[0].position_history)
    fig, ax = plt.subplots(figsize=(6, 6))

    scat_nomal = ax.scatter([], [], c='blue', label='Nomal Agents', s=70)
    scat_adversal = ax.scatter([], [], c='red', label='Adversal Agents', s=70)
    edge_indices = [(i, j) for i in range(self.N) for j in self.visible_graph[i]]
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
    label_offsets = [
        (
            0.8 * np.cos(2 * np.pi * i / max(1, self.N)),
            0.8 * np.sin(2 * np.pi * i / max(1, self.N)),
        )
        for i in range(self.N)
    ]
    text_labels = [
        ax.text(
            0, 0, str(i), fontsize=8, color='black', ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.2)
        )
        for i in range(self.N)
    ]

    x = [agent.position_history[t][0] for t in range(update_times) for agent in self.agents]
    y = [agent.position_history[t][1] for t in range(update_times) for agent in self.agents]
    padding = 2.0
    ax.set_xlim(min(x) - padding, max(x) + padding)
    ax.set_ylim(min(y) - padding, max(y) + padding)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_title("Agents Simulation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    leg = ax.legend(loc='upper right')
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, weight='bold')

    def animate(t):
        x_nomal = [agent.position_history[t][0] for agent in self.agents if agent.agent_type == AgentType.NOMAL]
        y_nomal = [agent.position_history[t][1] for agent in self.agents if agent.agent_type == AgentType.NOMAL]
        x_adversal = [agent.position_history[t][0] for agent in self.agents if agent.agent_type == AgentType.ADVERSAL]
        y_adversal = [agent.position_history[t][1] for agent in self.agents if agent.agent_type == AgentType.ADVERSAL]

        scat_nomal.set_offsets(np.c_[x_nomal, y_nomal])
        scat_adversal.set_offsets(np.c_[x_adversal, y_adversal])

        for idx, agent in enumerate(self.agents):
            x_pos = agent.position_history[t][0]
            y_pos = agent.position_history[t][1]
            offset_x, offset_y = label_offsets[idx]
            text_labels[idx].set_position((x_pos + offset_x, y_pos + offset_y))
            text_labels[idx].set_text(str(idx))

        for patch, (i, j) in zip(arrow_patches, edge_indices):
            start_pos = self.agents[i].position_history[t]
            end_pos = self.agents[j].position_history[t]
            patch.set_positions((start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
        time_text.set_text(f'Time: {t}')

        return scat_nomal, scat_adversal, *arrow_patches, leg, time_text, *text_labels

    print(self.visible_graph)
    os.makedirs('out', exist_ok=True)
    ani = animation.FuncAnimation(
        fig, animate, frames=update_times, interval=100, blit=True, repeat=False
    )
    ani.save('out/visualizer.mp4')
    plt.close()
    return