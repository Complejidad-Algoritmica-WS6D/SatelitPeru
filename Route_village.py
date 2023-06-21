import csv
from Village import Village

class Route_village(object):
    def __init__(self, 
                 sourceId,
                 sourceVillage,
                 sourceProvince,
                 sourceDepartament,
                 sourceLatitude,
                 sourceLongitude,
                 sourceAltitude,
                 destinationId,
                 destinationVillage,
                 destinationProvince,
                 destinationDepartament,
                 destinationLatitude,
                 destinationLongitude,
                 destinationAltitude,
                 distance
                 ):
        self.source = Village(
            sourceId, 
            sourceVillage, 
            sourceProvince,
            sourceDepartament, 
            sourceLatitude, 
            sourceLongitude,
            sourceAltitude
        )
        self.destination = Village(
            destinationId,
            destinationVillage,
            destinationProvince,
            destinationDepartament,
            destinationLatitude,
            destinationLongitude,
            destinationAltitude
        )
        self.distance = distance

    def __str__(self):
        return f"Origen: {self.source} -> Destino: {self.destination} : Distancia: {self.distance}"

    def getRouteVillage(self):
        return (self.source, self.destination, self.distance)
    
    def getSourceId(self):
        return self.source.id
    
    def getSourceVillage(self):
        return self.source.village
    
    def getSourceProvince(self):
        return self.source.province
    
    def getSourceDepartament(self):
        return self.source.department
    
    def getSourceLatitude(self):
        return self.source.latitude
    
    def getSourceLongitude(self):
        return self.source.longitude
    
    def getSourceAltitude(self):
        return self.source.altitude
    
    def getDestinationId(self):
        return self.destination.id

    def getDestinationVillage(self):
        return self.destination.village
    
    def getDestinationProvince(self):
        return self.destination.province
    
    def getDestinationDepartament(self):
        return self.destination.department
    
    def getDestinationLatitude(self):
        return self.destination.latitude
    
    def getDestinationLongitude(self):
        return self.destination.longitude
    
    def getDestinationAltitude(self):
        return self.destination.altitude
    
    def getDistance(self):
        return self.distance
    
class ListRoutesVillages:
    def __init__(self):
        self.list = []
    def __str__(self):
        return f"{self.list}"
    
    def getList(self):
        return self.list
    
    def addRouteVillage(self, route_village):
        self.list.append(route_village)
    def addFromCSV(self, filename):
        indice = 0
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if indice == 0:
                    indice += 1
                    continue
                
                routeVillage = Route_village(
                    row[0],         # sourceId
                    row[1],         # sourceVillage
                    row[2],         # sourceProvince
                    row[3],         # sourceDepartament
                    float(row[4]),  # sourceLatitude
                    float(row[5]),  # sourceLongitude
                    float(row[6]),  # sourceAltitude
                    row[7],         # destinationId
                    row[8],         # destinationVillage
                    row[9],         # destinationProvince
                    row[10],         # destinationDepartament
                    float(row[11]),  # destinationLatitude
                    float(row[12]), # destinationLongitude
                    float(row[13]), # destinationAltitude
                    float(row[14])  # distance
                    )
                self.addRouteVillage(routeVillage)
                indice += 1
        
        print(f"Se han cargado {indice} rutas de pueblos")
