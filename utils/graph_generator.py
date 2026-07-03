import random
import networkx as nx
import numpy as np

## NOTE: 自身のノードは含まないグラフの, 隣接リストを作成する helper 関数

def generate_random_strongly_connected_graph(n_vertices, n_edges):
    ## TODO: 未完成

    G = nx.DiGraph()
    G.add_nodes_from(range(n_vertices))

    # 有向サイクルをグラフに追加
    arr = np.arange(n_vertices)
    np.random.shuffle(arr)
    G.add_cycle(arr)

    # 残りの辺はランダムに追加
    all_possible_edges = [(u, v) for u in range(n_vertices) for v in range(n_vertices) if u != v]
    current_edges = set(G.edges())
    candidate_edges = [edge for edge in all_possible_edges if edge not in current_edges]
    choosen_edges = random.sample(candidate_edges, 3)
    G.add_edges_from(choosen_edges)

    # TODO: 一旦可視化、そのあと、強連結性を保証しながらランダムに入れ替える


# 頂点数 n_vertices, 辺の数 n_edges の、全域有向木を含む有向グラフをランダムに生成 計算量: O(V^2)
def generate_random_graph_with_spanning_arborescence(n_vertices, n_edges):
    if n_edges < n_vertices - 1:
        raise ValueError("|E| have to be more than (|V| - 1)")
        
    G = nx.DiGraph()
    G.add_nodes_from(range(n_vertices))
    
    # 1. 骨組みとなる全域木を生成
    for i in range(1, n_vertices):
        parent = random.randint(0, i - 1)
        G.add_edge(parent, i)
        
    # 2. ランダムな辺の肉付け
    all_possible_edges = [(u, v) for u in range(n_vertices) for v in range(n_vertices) if u != v]
    current_edges = set(G.edges())
    candidate_edges = [edge for edge in all_possible_edges if edge not in current_edges]
    random.shuffle(candidate_edges)
    
    edges_to_add = n_edges - (n_vertices - 1)
    for _ in range(min(edges_to_add, len(candidate_edges))):
        G.add_edge(*candidate_edges.pop())
        
    # 3. シャッフル
    mapping = list(range(n_vertices))
    random.shuffle(mapping)
    mapping_dict = {i: mapping[i] for i in range(n_vertices)}
    final_graph = nx.relabel_nodes(G, mapping_dict)
    
    adj_dict = nx.to_dict_of_lists(final_graph)
    
    return adj_dict

# 頂点数 n_vertices の完全グラフを生成
def generate_complite_graph(n_vertices):
    visible_graph =  [[] for _ in range(n_vertices)]
    for i in range(n_vertices):
        for j in range(n_vertices):
            if i is not j:
                visible_graph[i].append(j)
    return visible_graph
