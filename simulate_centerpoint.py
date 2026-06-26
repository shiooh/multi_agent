import os
import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
from enum import IntEnum, auto
from depth.model.DepthEucl import DepthEucl

from utils.graph_generator import generate_random_adjacency_list
from utils.visualizer import visualizer

class AgentType(IntEnum):
    NOMAL = auto()
    ADVERSAL = auto()


class Agent:
    def __init__(self, initial_position, agent_type, F, dimension):
        self.position_history = [initial_position]
        self.agent_type = agent_type
        self.F = F
        self.dimension = dimension
    
    def _move_as_adversal(self, other_agents_positions):
        ## 静止
        self.position_history.append(self.position_history[-1].copy())

    def _move_as_nomal(self, other_agents_positions):
        other_agents_positions.append(self.position_history[-1])
        other_agents_positions = np.array(other_agents_positions)

        model=DepthEucl().load_dataset(other_agents_positions)
        depths = model.halfspace(other_agents_positions, exact=True)

        center_idx = depths.argmax()
        centerpoint = other_agents_positions[center_idx]
         
        self.position_history.append(centerpoint.copy())

    def update_position(self, other_agents_positions):
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
       self.visible_graph = generate_random_adjacency_list(self.N, self.N *2)

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
    def _has_got_agreement(self):
        almost_zero = 10**(-3)
        for agent_i in self.agents:
            if agent_i.agent_type == AgentType.NOMAL:
                for agent_j in self.agents:
                    if agent_j.agent_type == AgentType.NOMAL:
                        diff = agent_i.position_history[-1] - agent_j.position_history[-1]
                        if np.linalg.norm(diff) > almost_zero:
                            return False
        return True

    # agents の移動の様子を可視化. 2次元にのみ対応している
    def _visualize(self):
        ##TODO: グラフがなんか変
        assert self.dimension == 2
        visualizer()

    def simulate(self, update_times):
        for t in range(update_times):
            self._update_agents(t)
            if self._has_got_agreement():
                break
        
        self._visualize()


if __name__ == "__main__":
    simulation_platform = SimulationPlatform(dimension=2, N=10, F=2)
    simulation_platform.simulate(update_times=50)