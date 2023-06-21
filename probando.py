import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.utils.union_find import UnionFind

def read_graph_from_csv(filename):
    G = nx.Graph()

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la primera fila (encabezado)

        for row in reader:
            Sid, Svillage,Sprovince,Sdepartment,Slatitud,Slongitud,Saltitude,Did,Dvillage,Dprovince,Ddepartment,Dlongitud,Dlatitud,Daltitude,  distance, = row
            G.add_edge(Sid, Did, weight=float(distance))

    return G

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

# Ejemplo de uso
filename = 'grafo.csv'
G = read_graph_from_csv(filename)
MST = kruskal(G)

# Mostrar el grafo original
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.title('Grafo original')

# Mostrar el árbol de expansión mínimo
plt.subplot(122)
nx.draw(MST, with_labels=True, font_weight='bold')
plt.title('Árbol de Expansión Mínimo')

plt.show()