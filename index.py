from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from Algorithms import kruskal, prim
import networkx as nx
import Graph_data as gp

app = Flask(__name__)
grafo = nx.Graph()
#grafo, villages = gp.initGraph()
mapaKruskal = gp.cleanMap()
mapaPrim = gp.cleanMap()
mapa = gp.cleanMap()



# Ruta principal del servidor
@app.route('/', methods=['GET', 'POST'])
def index():
    peso_kruskal=0
    peso_grafo=0
    peso_prim=0
    costoKruskal=0
    costoPrim=0
    costoGrafo=0
    kmTotal=0  
    caminokruskal = 'Pendiente'
    if request.method == 'POST': 
        seleccion = request.form['provincias']
        # Aquí puedes realizar cualquier operación con el valor seleccionado
        # Por ejemplo, puedes imprimirlo en la consola
        print("Provincia seleccionada:", seleccion)
        grafo, villages = gp.initGraph(seleccion)
        #print("Grafo:", grafo.nodes)
        #print("Aristas del grafo:", grafo.edges)
        #print("village:", villages)
        
        arbol_expansion_minimo = kruskal(grafo) 
        #print("Árbol de expansión mínimo:", arbol_expansion_minimo.nodes)
        #print("Aristas del árbol de expansión mínimo:", arbol_expansion_minimo.edges)
        #print("Peso total del árbol de expansión mínimo:", sum(arbol_expansion_minimo[u][v]['weight'] for u, v in arbol_expansion_minimo.edges))
        #print("Número de nodos del árbol de expansión mínimo:", arbol_expansion_minimo.number_of_nodes())
        #print("Número de aristas del árbol de expansión mínimo:", arbol_expansion_minimo.number_of_edges())
        #print("Número de componentes conexas del árbol de expansión mínimo:", nx.number_connected_components(arbol_expansion_minimo))
        #print("Componentes conexas del árbol de expansión mínimo:", list(nx.connected_components(arbol_expansion_minimo)))
        #print("latitud de la ciudad 1:", villages.getList()['1']['latitude'])    
        #villages=villages.getVillageByProvince(seleccion)

        #print("latitud de la ciudad 1:", villages)
        if not arbol_expansion_minimo:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapaKruskal.html')
        else:
            folium_map = gp.drawMap(arbol_expansion_minimo, arbol_expansion_minimo.edges, villages, seleccion)
            mapaKruskal = folium_map
            if arbol_expansion_minimo:
                peso_kruskal = sum(arbol_expansion_minimo[u][v]['weight'] for u, v in arbol_expansion_minimo.edges)
            costoKruskal = peso_kruskal * 5000
            folium_map.save('templates/mapaKruskal.html')
            
        if not grafo:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapa.html')
        else:
            folium_map = gp.drawMap(grafo, grafo.edges, villages, seleccion)
            mapa = folium_map
            if grafo:
                peso_grafo = sum(grafo[u][v]['weight'] for u, v in grafo.edges)
            costoGrafo = peso_grafo * 5000
            folium_map.save('templates/mapa.html')

        arbol_expansion_minimo_prim = prim(grafo)
        if not arbol_expansion_minimo_prim:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapaPrim.html')
        else:
            folium_map = gp.drawMap(arbol_expansion_minimo_prim, arbol_expansion_minimo_prim.edges, villages, seleccion)
            mapa = folium_map
            if arbol_expansion_minimo_prim:
                peso_prim = sum(arbol_expansion_minimo_prim[u][v]['weight'] for u, v in arbol_expansion_minimo_prim.edges)
            costoPrim = peso_prim * 5000
            folium_map.save('templates/mapaPrim.html')

        
        return render_template('index.html',peso_kruskal=peso_kruskal, costoKruskal=costoKruskal, peso_grafo=peso_grafo, costoGrafo=costoGrafo, peso_prim=peso_prim, costoPrim=costoPrim)
    else:
        response = make_response(render_template("index.html", peso_kruskal=peso_kruskal, costoKruskal=costoKruskal, peso_grafo=peso_grafo, costoGrafo=costoGrafo, peso_prim=peso_prim, costoPrim=costoPrim))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


@app.route('/mapa')
def mapa():
    return send_from_directory('templates', 'mapa.html')

@app.route('/mapaKruskal')
def mapaKruskal():
    return send_from_directory('templates', 'mapaKruskal.html')

@app.route('/mapaPrim')
def mapaPrim():
    return send_from_directory('templates', 'mapaPrim.html')

@app.context_processor
def inject_version():
    import time
    return {'version': int(time.time())}

if __name__ == "__main__":
    app.run(debug=True)