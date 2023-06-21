import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils.union_find import UnionFind

def kruskal(G):
    print("Iniciando Kruskal...")
    edges = list(G.edges.data('weight'))
    edges.sort(key=lambda x: x[2])  # Ordenar las aristas por peso en orden ascendente
    mst = nx.Graph()  # Grafo para almacenar el árbol de expansión mínimo (Minimum Spanning Tree)
    uf = UnionFind()

    for edge in edges:
        u, v, weight = edge
        if not uf[u] == uf[v]:
            mst.add_edge(u, v, weight=weight)
            uf.union(u, v)

    return mst