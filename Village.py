import csv

class Village:
    def __init__(self, id, village, province, department, latitude, longitude, altitude):
        self.id = id
        self.village = village
        self.province = province
        self.department = department
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
    
    def __str__(self):
        return f"Village Name:{self.village} -> Provincia: {self.province} -> Latitud: {self.latitude} -> Longitud: {self.longitude} -> Altitud: {self.altitude}"
    
    def getPosition(self):
        return (self.latitude, self.longitude)
    
class ListVillages:
    def __init__(self):
        self.dict = {}
    
    def __str__(self):
        return f"{self.dict}"
    
    def getList(self):
        return self.dict
    
    def addVillage(self, id, info):
        self.dict[id] = info

    def getVillageById(self, id):
        if id in self.dict:
            return self.dict[id]
        return None
    
    def getVillageByProvince(self, sel):
        villages = ListVillages()
        for id in self.dict:
            if self.dict[id]['department'] == sel:
                villages.addVillage(id, self.dict[id])
        return villages
    
    
    def addFromCSV(self, filename):
        indice = 0
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if indice == 0:
                    indice += 1
                    continue

                # village = Village(
                #     row[0],         # id
                #     row[1],         # village
                #     row[2],         # province
                #     row[3],         # latitude
                #     row[4],         # longitude
                #     row[5]          # altitude
                # )
                # self.addVillage(row[0], village)
                village = {
                    'village': row[1],
                    'province': row[2],
                    'department': row[3],
                    'latitude': row[4],
                    'longitude': row[5],
                    'altitude': row[6]
                }

                self.dict[row[0]] = village 
                indice += 1
        print(f"Se han cargado {indice} pueblos")