def calcular_promedio_edades(encuestas, zona):
    edades = []
    for encuesta in encuestas:
        if encuesta[2] == zona:
            edades.append(encuesta[1])
    if len(edades) > 0:
        promedio = sum(edades) / len(edades)
        return promedio
    else:
        return 0

def calcular_porcentaje_hombres_mayores(encuestas):
    hombres_mayores = 0
    hombres_mayores_supervisan = 0
    for encuesta in encuestas:
        if encuesta[0] == 0 and encuesta[1] > 50:
            hombres_mayores += 1
            if encuesta[4] > 4:
                hombres_mayores_supervisan += 1
    if hombres_mayores > 0:
        porcentaje = (hombres_mayores_supervisan / hombres_mayores) * 100
        return porcentaje
    else:
        return 0

def calcular_promedio_tiempo_mujeres(encuestas, edad):
    tiempos = []
    for encuesta in encuestas:
        if encuesta[0] == 1 and encuesta[1] == edad:
            tiempos.append(encuesta[4])
    if len(tiempos) > 0:
        promedio = sum(tiempos) / len(tiempos)
        return promedio
    else:
        return 0

encuestas = []
num_encuestas = int(input("Ingrese el número de encuestas: "))

for i in range(num_encuestas):
    respuesta = input("Ingrese la respuesta del colaborador (sexo / edad / labor / inicio_fin): ")
    datos = respuesta.split(" / ")
    sexo = int(datos[0])
    edad = int(datos[1])
    labor = int(datos[2])
    inicio_fin = datos[3].split(" ")
    inicio = int(inicio_fin[0])
    fin = int(inicio_fin[1])
    encuestas.append((sexo, edad, labor, inicio, fin))

promedio_edades_zona1 = calcular_promedio_edades(encuestas, 1)
promedio_edades_zona2 = calcular_promedio_edades(encuestas, 2)
porcentaje_hombres_mayores = calcular_porcentaje_hombres_mayores(encuestas)
promedio_tiempo_mujeres = calcular_promedio_tiempo_mujeres(encuestas, 45)

print("Promedio de edades en zona 1:", promedio_edades_zona1)
print("Promedio de edades en zona 2:", promedio_edades_zona2)
print("Porcentaje de hombres mayores de 50 años que supervisan por más de 4 horas:", porcentaje_hombres_mayores)
print("Promedio de tiempo que pasan supervisando las mujeres de 45 años:", promedio_tiempo_mujeres)
