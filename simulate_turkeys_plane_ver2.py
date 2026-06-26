import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from enum import IntEnum, auto

class AgentType(IntEnum):
    NOMAL = auto()
    ADVERSAL = auto()

class Agent:
    def __init__(self, initial_position, agent_type, F, dimension):
        self.position_history = [initial_position]
        self.agent_type = agent_type
        self.F = F
        self.dimension = dimension

    def _is_valid_positions(self, other_agents_positions):
        ## TODO: validation した方が理想的
        return True
    
    def _move_as_adversal(self, other_agents_positions):
        ## 静止
        self.position_history.append(self.position_history[-1].copy())

    def _move_as_nomal(self, other_agents_positions):
        best_nomal_vector_set = {'nomal_vector': None, 'diff_of_sides': 0}

        for counter in range(100):
            # hyperplane の単位法線ベクトル (nomal_vector) をランダムに生成
            rng = np.random.default_rng()
            v = rng.standard_normal(self.dimension)
            norm = np.linalg.norm(v)
            nomal_vector = v / norm
            
            nodes_on_positive_side = 0  # hyperplane の nomal_vector 側にある agent の数
            nodes_on_negative_side = 0  # hyperplane の nomal_vector と逆側にある agent の数
            for other_position in other_agents_positions:
                if nomal_vector @ (other_position - self.position_history[-1]) > 0:
                    nodes_on_positive_side += 1
                else:
                    nodes_on_negative_side += 1
            diff_of_sides = nodes_on_positive_side - nodes_on_negative_side
            if diff_of_sides > self.F:
                if diff_of_sides > best_nomal_vector_set['diff_of_sides']:
                    best_nomal_vector_set['nomal_vector'] = nomal_vector                    
                    best_nomal_vector_set['diff_of_sides'] = diff_of_sides
            elif - diff_of_sides >  self.F:
                if -diff_of_sides > best_nomal_vector_set['diff_of_sides']:
                    best_nomal_vector_set['nomal_vector'] = - nomal_vector                    
                    best_nomal_vector_set['diff_of_sides'] = - diff_of_sides
        
        if best_nomal_vector_set['nomal_vector'] is None:
            self.position_history.append(self.position_history[-1].copy())
            print("not found good hyperplane")

        else:   
            self.position_history.append(self.position_history[-1].copy() + best_nomal_vector_set['nomal_vector'] * 10)

    def update_position(self, other_agents_positions):
        assert self._is_valid_positions(other_agents_positions)
        if self.agent_type == AgentType.ADVERSAL:
            self._move_as_adversal(other_agents_positions)
        else:
            self._move_as_nomal(other_agents_positions)
        
class SimulationPlatform:
    def __init__(self, dimension, N, F):
        self.dimension = dimension
        self.N = N
        self.F = F
        self.agents = []
        self._initialize_agents()
        self.visible_graph = [[] for _ in range(N)]
        self._initialize_visible_graph()

    def _initialize_visible_graph(self):
        ## NOTE: 一旦可視グラフは完全グラフと仮定する
        for i in range(self.N):
            for j in range(self.N):
                if i is not j:
                    self.visible_graph[i].append(j)

    def _initialize_agents(self):
        adversal_index = random.sample(list(range(self.N)), self.F)
        for i in range(self.N):
            position = np.array([random.uniform(0, 50) for _ in range(self.dimension)])
            if i in adversal_index:
                agent_type = AgentType.ADVERSAL
            else:
                agent_type = AgentType.NOMAL
            self.agents.append(Agent(initial_position=position, agent_type=agent_type, F=self.F, dimension=self.dimension))

    def _update_agents(self, cur_time):
        for i in range(self.N):
            other_agents_positions = []
            for j in self.visible_graph[i]:
                other_agents_positions.append(self.agents[j].position_history[cur_time])
            self.agents[i].update_position(other_agents_positions)

    # agents が合意に達しているか評価
    def _has_got_agreement():
        almost_zero = 10**(-5)
        for i in range(N):
            for j in range(self.N):
                if np.abs(self.agents[i] - self.agents[j]) > almost_zero:
                    return False
        return True

    # agents の移動の様子を可視化. 2次元にのみ対応している
    def _visualize(self, update_times):
        assert self.dimension == 2
        fig, ax = plt.subplots(figsize=(6, 6))

        scat_nomal = ax.scatter([], [], c='blue', label='Nomal Agents')
        scat_adversal = ax.scatter([], [], c='red', label='Adversal Agents')
        x = [agent.position_history[t][0] for t in range(update_times) for agent in self.agents]
        y = [agent.position_history[t][1] for t in range(update_times) for agent in self.agents]
        ax.set_xlim(min(x),max(x))
        ax.set_ylim(min(y),max(y))
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
            time_text.set_text(f'Time: {t}')
            
            return scat_nomal, scat_adversal, leg, time_text

        base_interval = 50 
        durations = [base_interval] * update_times
        durations[-1] = 3000

        ani = animation.FuncAnimation(
            fig, animate, frames=update_times, interval=50, blit=True, repeat=False
        )
        ani.save(
            f'out/visualizer.mp4'
        )
        plt.close()
        return

    def simulate(self, update_times):
        for t in range(update_times):
            self._update_agents(t)
        
        self._visualize(update_times)


if __name__ == "__main__":
    simulation_platform = SimulationPlatform(dimension=2, N=10, F=1)
    simulation_platform.simulate(update_times=100)