import sys
import io
import networkx as nx
import folium as fl
from Village import Village, ListVillages
import Route_village as rts

# Configurar la salida estándar con una codificación adecuada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def initGraph(seleccion):
    grafo = nx.Graph()
    listWeightedNodes = []

    routes_village = rts.ListRoutesVillages()
    routes_village.addFromCSV('data/distance_village.csv')
    routes_village = routes_village.getRoutesVillagesBySourceDepartment(seleccion)
    
    villages = ListVillages()
    villages.addFromCSV("data/village.csv")
    newVillages = villages.getVillageByProvince(seleccion)

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
    return grafo, newVillages

def calcular_peso(grafo, village1, village2):
    return nx.shortest_path_length(grafo, village1, village2, weight='weight')

def cleanMap():
    map = fl.Map(location=[0, 0], zoom_start=3)
    return map

def drawMap(grafo, camino, listVillages: ListVillages, seleccion):

    nuevoCamino = []

    for item in camino:
        tmp = [item[0], item[1]]
        nuevoCamino.append(tmp)   

    #print("LA SELECCION",listVillages.getVillageByProvince(seleccion))
    print("EL CAMINO", nuevoCamino)
    
    map = fl.Map(location=[listVillages.getVillageById(nuevoCamino[0][0])['latitude'],
                           listVillages.getVillageById(nuevoCamino[0][0])['longitude']], 
                           zoom_start=10)
    
    villageAdded = []
    routesPositions = []

    # Agregar los nodos al mapa
    for vllgs in nuevoCamino:
        village1, village2 = vllgs
        if village1 not in villageAdded:
            if village1 == nuevoCamino[0][0]:
                _color = 'green'
            elif village1 == nuevoCamino[-1][0]:
                _color = 'red'
            else:
                _color = 'blue'
            
            villageAdded.append(village1)

            village = listVillages.getVillageById(village1)
            villagePosition = (village['latitude'], village['longitude'])
            routesPositions.append(villagePosition)
            map.add_child(
                fl.Marker(location=villagePosition, 
                          popup=village1 +' - '+ village['village'], #village['village'], 
                          icon=fl.Icon(prefix="fa",
                                       icon="location",
                                       color=_color)))
        
        if village2 not in villageAdded:
            _color = 'blue'
            
            villageAdded.append(village2)

            village = listVillages.getVillageById(village2)
            villagePosition = (village['latitude'], village['longitude'])
            routesPositions.append(villagePosition)
            map.add_child(
                fl.Marker(location=villagePosition, 
                          popup=village2 +' - '+ village['village'],  #village['village'], 
                          icon=fl.Icon(prefix="fa",
                                       icon="location",
                                       color=_color)))
            
    # Agregar las rutas al mapa con los pesos como popup
    for vllgs in nuevoCamino:
        print("VILLAGES: " ,vllgs)
        village1, village2 = vllgs
        position1 = (
        float(listVillages.getVillageById(village1)['latitude']), 
        float(listVillages.getVillageById(village1)['longitude']))

        position2 = (
        float(listVillages.getVillageById(village2)['latitude']), 
        float(listVillages.getVillageById(village2)['longitude']))

        print("position 1: ", position1)
        print("Position 2: ", position2)

        if position1 and position2:
            peso = calcular_peso(grafo, village1, village2)

            #crear la arista y agregar el popup con el peso
            fl.PolyLine([position1, position2], color='blue', weight=2, 
                        popup=f'Distancia: {peso} Km').add_to(map)
            
            print("Arista agregada: ", position1, position2)
    
    return map


    