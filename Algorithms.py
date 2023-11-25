import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.utils.union_find import UnionFind
import heapq

def kruskal(G):
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



def prim(G):
    start_node = next(iter(G))  # Seleccionar cualquier nodo como inicio
    mst = nx.Graph()  # Grafo para almacenar el árbol de expansión mínimo (Minimum Spanning Tree)
    visited = set([start_node])  # Conjunto de nodos visitados
    heap = []  # Montículo para seleccionar la siguiente arista de menor peso

    # Agregar las aristas del nodo inicial al montículo
    for neighbor in G.neighbors(start_node):
        weight = G[start_node][neighbor]['weight']
        heapq.heappush(heap, (weight, start_node, neighbor))

    while heap:
        weight, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst.add_edge(u, v, weight=weight)

            # Agregar las aristas del nodo visitado al montículo
            for neighbor in G.neighbors(v):
                if neighbor not in visited:
                    weight = G[v][neighbor]['weight']
                    heapq.heappush(heap, (weight, v, neighbor))

    return mst