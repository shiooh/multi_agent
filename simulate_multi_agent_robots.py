import numpy as np
import random

from enum import IntEnum, auto
from utils.graph_generator import *
from utils.visualizer import visualizer
from utils.robust_update_functions import *

class AgentType(IntEnum):
    NOMAL = auto()
    ADVERSAL = auto()

class Agent:
    def __init__(self, initial_position, agent_type, F, dimension):
        self.position_history = [initial_position]
        self.agent_type = agent_type
        self.F = F
        self.dimension = dimension
        self.cur_time = 0
    
    def _move_as_adversal(self, other_agents_positions):
        ## 静止
        self.position_history.append(self.position_history[-1].copy())

    def _move_as_nomal(self, other_agents_positions):

        ## Tukey's Hyperplane に基づく更新
        # next_position = update_by_tukeys_hyperplane(
        #     self_position = self.position_history[-1],
        #     other_agents_positions = other_agents_positions,
        #     cur_time = self.cur_time,
        #     F = self.F,
        #     dimension = self.dimension,
        #     find_best = True,     # ver1: False, ver2~ : True
        #     diminish_step_length = True    # ver1,2: False, ver3: True
        # )

        # Centerpoint に基づく更新
        next_position = update_by_center_point(
            weight = 0.7,
            self_position = self.position_history[-1],
            other_agents_positions = other_agents_positions,
            F = self.F,
            dimension = self.dimension
        )
        
        self.position_history.append(next_position)
        

    def update_position(self, other_agents_positions):
        self.cur_time += 1
        if self.agent_type == AgentType.ADVERSAL:
            self._move_as_adversal(other_agents_positions)
        elif self.agent_type == AgentType.NOMAL:
            self._move_as_nomal(other_agents_positions)
        else:
            raise ValueError("Unexpected Agent Type")


class SimulationPlatform:
    def __init__(self, dimension, N, F, epsilon, max_delay=0):
        self.dimension = dimension
        self.N = N
        self.F = F
        self.epsilon = epsilon
        self.max_delay = max_delay
        self.agents = []
        self._initialize_agents()
        self.visible_graph = [[] for _ in range(N)]
        self._initialize_visible_graph()

    # 可視グラフをランダムに生成
    def _initialize_visible_graph(self):
        nomal_agents_id = [i for i in range(self.N) if self.agents[i].agent_type == AgentType.NOMAL]
        adversal_agents_id = [i for i in range(self.N) if self.agents[i].agent_type == AgentType.ADVERSAL]
        ## 完全グラフ
        # self.visible_graph = generate_complite_graph(nomal_agents_id, adversal_agents_id)

        ## Safe Point アルゴリズムの条件を満たすグラフ
        self.visible_graph = generate_random_graph_with_spanning_arborescence(nomal_agents_id, adversal_agents_id, 100, self.F*(self.dimension+1))

    # Agent の位置をランダムに決定
    def _initialize_agents(self):
        for i in range(self.N):
            position = np.array([random.uniform(0, 50) for _ in range(self.dimension)])
            # agent 1 ~ N-F を故障ロボットとしても一般性を失わない
            if i in range(self.N - self.F):
                agent_type = AgentType.NOMAL
            else:
                agent_type = AgentType.ADVERSAL
            self.agents.append(Agent(initial_position=position, agent_type=agent_type, F=self.F, dimension=self.dimension))

    # 各Agent の位置を更新
    def _update_agents(self, cur_time):
        for i in range(self.N):
            other_agents_positions = []
            for j in self.visible_graph[i]:
                delay = random.randint(0, min(self.max_delay, cur_time))
                other_agents_positions.append(self.agents[j].position_history[cur_time - delay])
            self.agents[i].update_position(other_agents_positions)

    # agents が合意に達しているか評価
    def _has_got_agreement(self):
        for agent_i in self.agents:
            if agent_i.agent_type == AgentType.NOMAL:
                for agent_j in self.agents:
                    if agent_j.agent_type == AgentType.NOMAL:
                        diff = agent_i.position_history[-1] - agent_j.position_history[-1]
                        if np.linalg.norm(diff) >= self.epsilon:
                            return False
        return True

    # agents の移動の様子を可視化. 2次元にのみ対応している
    def _visualize(self):
        if self.dimension != 2:
            raise ValueError("Dimension has to be 2 to visualize")
        all_agents_history = [agent.position_history for agent in self.agents]
        nomal_agents_history = [agent.position_history for agent in self.agents if agent.agent_type == AgentType.NOMAL]
        adversal_agents_history = [agent.position_history for agent in self.agents if agent.agent_type == AgentType.ADVERSAL]

        visualizer(
            all_agents_history = all_agents_history,
            nomal_agents_history = nomal_agents_history,
            adversal_agents_history = adversal_agents_history,
            visible_graph = self.visible_graph,
            show_arrow = False
        )

    # 全体の流れ
    def simulate(self, update_times):
        for t in range(update_times):
            print("Update time: ", t)
            self._update_agents(t)
            if self._has_got_agreement():
                print("Acheaved agreement!")
                break
        
        self._visualize()
        pass


if __name__ == "__main__":
    print("Simulating ... ")
    simulation_platform = SimulationPlatform(dimension=2, N=15, F=1, epsilon=10**(-3), max_delay=5)
    simulation_platform.simulate(update_times=500)