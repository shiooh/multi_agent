import random
import networkx as nx
import numpy as np

## NOTE: 自身のノードは含まないグラフの, 隣接リストを作成する helper 関数

# 正常ノード nomal_agents_id, 故障ノード adversal_agents_id を頂点として 辺数 n_edges の(i), (ii) を満たすグラフをランダムに生成する
# (i) 正常ノード i の近傍の数 N_i が N_i >= F_i * (dimension + 1)
# (ii) 正常ノードの 接続グラフは repeatedly reachable
def generate_random_graph_with_spanning_arborescence(nomal_agents_id, adversal_agents_id, n_edges, min_neighbour):

    adj_list = [[] for _ in nomal_agents_id + adversal_agents_id]
    
    # 条件(ii)を満たす
    generate_spanning_arborescence_of_nomal_agents(nomal_agents_id, adj_list)

    # 条件(i)を満たす
    candidate_edges = []
    for i in nomal_agents_id:
        if min_neighbour >= len(adj_list[i]):
            not_adj_of_i = set(nomal_agents_id + adversal_agents_id)
            not_adj_of_i.remove(i)
            for j in adj_list[i]:
                not_adj_of_i.remove(j)
            chosen = random.sample(list(not_adj_of_i), min_neighbour - len(adj_list[i]))
            adj_list[i].extend(chosen)
            for j in chosen:
                not_adj_of_i.remove(j)
            candidate_edges.extend([(i, j) for j in list(not_adj_of_i)])
            n_edges -= min_neighbour
        else:
            n_edges -= len(adj_list[i])

    # 足りない辺の数を肉付け
    if n_edges < 0:
        print("Overed intended edge size")
    elif n_edges > 0:
        if n_edges <= len(candidate_edges):
            random.sample(candidate_edges, n_edges)
        else:
            print("Intended edge size is too much")

    # print_graph(adj_list)

    return adj_list

def generate_spanning_arborescence_of_nomal_agents(nomal_agents_id, adj_list):

    parents = [0] * len(nomal_agents_id)
    parents_size = 0
    children = nomal_agents_id.copy()
    children_size = len(nomal_agents_id)

    def pop_from_children():
        nonlocal children, children_size
        random_id = random.randint(0, children_size-1)
        chosen = children[random_id]
        children[children_size-1], children[random_id] = children[random_id], children[children_size-1]
        children_size -= 1
        return chosen
    def add_to_parents(added):
        nonlocal parents, parents_size
        parents[parents_size] = added
        parents_size += 1

    random_parent = pop_from_children()
    add_to_parents(random_parent)
    for i in range(len(nomal_agents_id)-1):
        random_child = pop_from_children()
        random_parent = parents[random.randint(0, parents_size-1)]
        adj_list[random_parent].append(random_child)
        add_to_parents(random_child)
    

# 頂点数 n_vertices の完全グラフを生成
def generate_complite_graph(nomal_agents_id, adversal_agents_id):
    visible_graph =  [[] for _ in (nomal_agents_id + adversal_agents_id)]
    for i in (nomal_agents_id + adversal_agents_id):
        for j in (nomal_agents_id + adversal_agents_id):
            if i is not j:
                visible_graph[i].append(j)
    return visible_graph


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def print_graph(adj_list):
    adj_dict = {i: neighbors for i, neighbors in enumerate(adj_list)}

    G = nx.from_dict_of_lists(adj_dict)
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold')
    plt.savefig("out/network_graph.png", format="PNG", dpi=300)
