import random
import networkx as nx

def generate_random_adjacency_list(n_vertices, n_edges):
    if n_edges < n_vertices - 1:
        raise ValueError("辺の数は (頂点数 - 1) 以上である必要があります。")
        
    G = nx.DiGraph()
    G.add_nodes_from(range(n_vertices))
    
    # 1. 骨組みとなる全域木
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
    
def generate_random_complite_graph(n_vertices):
    visible_graph =  [[] for _ in range(n_vertices)]
    for i in range(n_vertices):
        for j in range(n_vertices):
            if i is not j:
                visible_graph[i].append(j)
