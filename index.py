from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from Kruskal import kruskal
import networkx as nx
#import Graph as gp 
import Graph_data as gp

app = Flask(__name__)

#ahora
grafo = nx.Graph()
grafo, villages = gp.initGraph()
mapaKruskal = gp.cleanMap()

# Ruta principal del servidor
@app.route('/', methods=['GET', 'POST'])
def index():
    caminokruskal = 'Pendiente'
    if request.method == 'POST':   
        arbol_expansion_minimo = kruskal(grafo)
        print("Árbol de expansión mínimo:", arbol_expansion_minimo.nodes)
        print("Aristas del árbol de expansión mínimo:", arbol_expansion_minimo.edges)
        print("Peso total del árbol de expansión mínimo:", sum(arbol_expansion_minimo[u][v]['weight'] for u, v in arbol_expansion_minimo.edges))
        print("Número de nodos del árbol de expansión mínimo:", arbol_expansion_minimo.number_of_nodes())
        print("Número de aristas del árbol de expansión mínimo:", arbol_expansion_minimo.number_of_edges())
        print("Número de componentes conexas del árbol de expansión mínimo:", nx.number_connected_components(arbol_expansion_minimo))
        print("Componentes conexas del árbol de expansión mínimo:", list(nx.connected_components(arbol_expansion_minimo)))
        print("latitud de la ciudad 1:", villages[0][0].getPosition())
        if not arbol_expansion_minimo:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapaKruskal.html')
            print("No se encontró un árbol de expansión mínimo")
        else:
            # Se crea el mapa con el árbol de expansión mínimo
            folium_map = gp.drawMap(arbol_expansion_minimo, arbol_expansion_minimo.edges, villages)
            mapaKruskal = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapaKruskal.html')
            print("Se encontró un árbol de expansión mínimo")

        # return render_template('index.html', caminobfs=caminobfs, caminodijkstra=caminodijkstra)
        return redirect(url_for('index'))
    else:
        response = make_response(render_template("index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

# Ruta para calcular el camino más corto entre dos pueblos
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapaKruskal')
def mapaKruskal():
    
    return send_from_directory('templates', 'mapaKruskal.html')


@app.context_processor
def inject_version():
    import time
    return {'version': int(time.time())}

if __name__ == "__main__":
    app.run(debug=True)