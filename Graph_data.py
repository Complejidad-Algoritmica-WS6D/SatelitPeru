import sys
import io
import networkx as nx
import folium as fl
from Village import Village, ListVillages
import Route_village as rts

# Configurar la salida estándar con una codificación adecuada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def initGraph():
    grafo = nx.Graph()
    listWeightedNodes = []

    routes_village = rts.ListRoutesVillages()
    routes_village.addFromCSV('static/distance_village.csv')

    villages = ListVillages()
    villages.addFromCSV("static/village.csv")

    # Recorrer la lista de rutas de pueblos y agregar los nodos al grafo
    for route in routes_village.getList():

        origen = route.getSourceId()
        destino = route.getDestinationId()

        try:
            latitud_origen = float(route.getSourceLatitude())
            longitud_origen = float(route.getSourceLongitude())
            latitud_destino = float(route.getDestinationLatitude())
            longitud_destino = float(route.getDestinationLongitude())
        except:
            continue

        distancia = route.getDistance()

        if not grafo.has_node(origen):
            grafo.add_node(origen)
        
        if not grafo.has_node(destino):
            grafo.add_node(destino)
        
        nodo = (origen, destino, distancia)
        listWeightedNodes.append(nodo)

    grafo.add_weighted_edges_from(listWeightedNodes)
    return grafo, villages

def calcular_peso(grafo, village1, village2):
    return nx.shortest_path_length(grafo, village1, village2, weight='weight')

def cleanMap():
    map = fl.Map(location=[0, 0], zoom_start=3)
    return map

def drawMap(grafo, camino, listVillages: ListVillages):
    map = fl.Map(location=[listVillages.getVillageById(camino[0][0])['latitude'],
                           listVillages.getVillageById(camino[0][0])['longitude']], 
                           zoom_start=3)
    
    villageAdded = []
    routesPositions = []

    # Agregar los nodos al mapa
    for vllgs in camino:
        village1, village2 = vllgs
        if village1 not in villageAdded:
            if village1 == camino[0][0]:
                _color = 'green'
            elif village1 == camino[-1][0]:
                _color = 'red'
            else:
                _color = 'blue'
            
            villageAdded.append(village1)

            village = listVillages.getVillageById(village1)
            villagePosition = (village['latitude'], village['longitude'])
            routesPositions.append(villagePosition)
            map.add_child(
                fl.Marker(location=villagePosition, 
                          popup=village['village'], 
                          icon=fl.Icon(prefix="fa",
                                       icon="location-arrow",
                                       color=_color)))
        
        if village2 not in villageAdded:
            if village2 == camino[0][0]:
                _color = 'green'
            elif village2 == camino[-1][0]:
                _color = 'red'
            else:
                _color = 'blue'
            
            villageAdded.append(village2)

            village = listVillages.getVillageById(village2)
            villagePosition = (village['latitude'], village['longitude'])
            routesPositions.append(villagePosition)
            map.add_child(
                fl.Marker(location=villagePosition, 
                          popup=village['village'], 
                          icon=fl.Icon(prefix="fa",
                                       icon="location-arrow",
                                       color=_color)))
            
    # Agregar las rutas al mapa con los pesos como popup
    for vllgs in camino:
        village1, village2 = vllgs
        position1 = (
        listVillages.getVillageById(village1)['latitude'], listVillages.getVillageById(village1)['longitude'])
        position2 = (
        listVillages.getVillageById(village2)['latitude'], listVillages.getVillageById(village2)['longitude'])

        if position1 and position2:
            peso = calcular_peso(grafo, village1, village2)

            #crear la arista y agregar el popup con el peso
            fl.PolyLine([position1, position2], color='blue', weight=2, 
                        popup=f'Distancia: {peso}Km').add_to(map)
    
    return map


    