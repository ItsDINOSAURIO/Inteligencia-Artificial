import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt

nodos={
    0:(19.50467,-99.20010),
    1:(19.48949,-99.14473),
    2:(19.48533,-99.12547),
    3:(19.48514,-99.10437),
    4:(19.46991,-99.13657),
    5:(19.45952,-99.18752),
    6:(19.45823,-99.11391),
    7:(19.44498,-99.08688),
    8:(19.44493,-99.14525),
    9:(19.44393,-99.13862),
    10:(19.43965,-99.11818),
    11:(19.43751,-99.14715),
    12:(19.43639,-99.14161),
    13:(19.43009,-99.11432),
    14:(19.42956,-99.12097),
    15:(19.42435,-99.13285),
    16:(19.42725,-99.14901),
    17:(19.42721,-99.14210),
    18:(19.41510,-99.07436),
    19:(19.40198,-99.18732),
    20:(19.40659,-99.15520),
    21:(19.40918,-99.13563),
    22:(19.41097,-99.12176),
    23:(19.40417,-99.12067),
    24:(19.37609,-99.18778),
    25:(19.37068,-99.16505),
    26:(19.36113,-99.14308),
    27:(19.35626,-99.10118)
}
coords = {}
for nodo, (lat, lon) in nodos.items():
    x = 111 * (lat - list(nodos.values())[0][0])
    y = 111 * np.cos(np.radians((lat + list(nodos.values())[0][0]) / 2)) * (lon - list(nodos.values())[0][1])
    coords[nodo] = (y, x)

estaciones={    
    0: "Rosario",
    1: "Instituto del Petróleo",
    2: "Deportivo 18 de Marzo",
    3: "Martín Carrera",
    4: "La Raza",
    5: "Tacuba",
    6: "Consulado",
    7: "Oceanía",
    8: "Guerrero",
    9: "Garibaldí/Lagunilla",
    10: "Morelos",
    11: "Hidalgo",
    12: "Bellas Artes",
    13: "San Lázaro",
    14: "Candelaria",
    15: "Pino Suárez",
    16: "Balderas",
    17: "Salto del Agua",
    18: "Pantitlán",
    19: "Tacubaya",
    20: "Centro Médico",
    21: "Chabacano",
    22: "Jamaica",
    23: "Santa Anita",
    24: "Mixcoac",
    25: "Zapata",
    26: "Ermita",
    27: "Atlalilco"}

def calcular_distancia(nodo1,nodo2):
    x1,y1=coords[nodo1]
    x2,y2=coords[nodo2]

    distancia=np.sqrt((x2-x1)**2+(y2-y1)**2)
    return distancia

conexiones={}
for (nodo1,nodo2) in [
    (0,1),(0,5),(1,2),(1,4),(2,3),(2,4),(3,6),(4,6),(4,8),(5,11),(5,19),(6,7),(6,10),
    (7,13),(7,18),(8,9),(8,11),(9,10),(9,12),(10,13),(10,14),(11,12),(11,16),(12,15),
    (12,17),(13,14),(13,18),(14,15),(14,22),(15,17),(15,21),(16,17),(16,19),(16,20),
    (17,21),(18,22),(19,20),(19,24),(20,21),(20,25),(21,22),(21,26),(22,23),(23,27),
    (24,25),(25,26),(26,27)
    ]:
    dist=calcular_distancia(nodo1,nodo2)
    conexiones[(min(nodo1,nodo2),max(nodo1,nodo2))]=dist

feromonas={arista:0.1 for arista in conexiones}
rho=0.9
alpha=1
beta=1
Q=1
num_hormigas=50
num_iteraciones=100#323
heuristica={arista:1.0/conexiones[arista] for arista in conexiones} #Visibilidad

mejor_camino=None
mejor_longitud=float('inf')

# print(conexiones)

print("Estaciones disponibles:")
for indice, nombre in estaciones.items():
    print(f"{indice}: {nombre}")

estaciones_res=estaciones.copy()

while True:
    try:
        nodo_in=int(input('¿Dónde Quiere Iniciar el Trayecto? '))
        if nodo_in not in estaciones:
            raise ValueError("Has seleccionado un nodo inválido.")
        break
    except ValueError as e:
        print(f'Error:{e}.  Por favor, inténtalo de nuevo.\n')

estacion_in=estaciones_res.pop(nodo_in)
print(f"Estación Inicial: {estacion_in}")

while True:
    try:
        print("Estaciones disponibles:")
        for indice, nombre in estaciones_res.items():
            print(f"{indice}: {nombre}")
        nodo_out=int(input('¿Dónde Quiere Terminar el Trayecto? '))
        if nodo_out not in estaciones_res:
            raise ValueError("Has seleccionado un nodo inválido.")
        break
    except ValueError as e:
        print(f'Error:{e}. Por favor, inténtalo de nuevo.') 

print(f"Estación Final: {estaciones_res[nodo_out]}")

print(f"Trayecto seleccionado: De {estaciones[nodo_in]} a {estaciones[nodo_out]}")


for iteraciones in range(num_iteraciones):
    caminos_todos=[]
    longitudes_todos=[]
    for hormiga in range(num_hormigas):
        # print("{hormiga}")
        nodo_actual=nodo_in
        nodos_visitados=[nodo_actual]
        camino=[]
        longitud_total=0

        while nodo_actual != nodo_out:
            nodos_vecinos = [
                nodo for nodo in nodos if nodo != nodo_actual
                and nodo not in nodos_visitados
                and (min(nodo_actual, nodo), max(nodo_actual, nodo)) in conexiones
            ]

            if not nodos_vecinos:
                break

            probabilidades = []
            for vecino in nodos_vecinos:
                arista = (min(nodo_actual, vecino), max(nodo_actual, vecino))
                tau = feromonas[arista] ** alpha
                eta = heuristica[arista] ** beta
                probabilidades.append(tau * eta)

            suma_probabilidades = sum(probabilidades)
            probabilidades = [p / suma_probabilidades for p in probabilidades]
            # print(probabilidades)

            valor_random = random.random()
            suma_acumulada = 0
            proximo_nodo = None
            for i, nodo in enumerate(nodos_vecinos):
                suma_acumulada += probabilidades[i]
                if suma_acumulada >= valor_random:
                    proximo_nodo = nodo
                    # print(proximo_nodo)
                    break

            camino.append(proximo_nodo)
            nodos_visitados.append(proximo_nodo)
            distancia = calcular_distancia(nodo_actual, proximo_nodo)
            longitud_total += distancia
            nodo_actual = proximo_nodo

        if nodo_actual==nodo_out:
            caminos_todos.append(camino)
            longitudes_todos.append(longitud_total)
        
            if longitud_total < mejor_longitud:
                mejor_longitud = longitud_total
                mejor_camino = [nodo_in]+camino

    # Evaporación y refuerzo de feromonas
    for arista in feromonas:
        feromonas[arista] *= (1-rho) 

    # print(feromonas)

    for camino, longitud in zip(caminos_todos, longitudes_todos):
        for i in range(len(camino) - 1):
            arista = (min(camino[i], camino[i + 1]), max(camino[i], camino[i + 1]))
            feromonas[arista] += Q / longitud
    # print(feromonas)

# print(f"El mejor camino encontrado desde {nodo_in} es {mejor_camino} con longitud {mejor_longitud} km")
print('Mejor camino:')
for nodo in mejor_camino:
    print(estaciones[nodo],end="->")
print(f"\nLongitud total: {mejor_longitud}")

plt.figure(figsize=(10, 8))

for (nodo1, nodo2) in conexiones:
    x1, y1 = coords[nodo1]
    x2, y2 = coords[nodo2]
    plt.plot([x1, x2], [y1, y2], 'cyan', linestyle='--', alpha=0.3)

for nodo, (x, y) in coords.items():
    plt.scatter(x, y, c='purple', s=50, label=estaciones[nodo] if nodo < len(estaciones) else None)
    plt.text(x +0.1, y + 0.3, estaciones[nodo], fontsize=8)

plt.title("Mapa de Estaciones")
plt.xlabel("Distancia X (km)")
plt.ylabel("Distancia Y (km)")
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')

plt.show()

    #Tomar todo el mapa de la ciudad de mexico de las lineas dle metro y buscar cuales nodos comparten más de 1 línea, resolver con ACO
    #Proporcionar un destino y un inicio, para determinar las conexiones necesarias para llegar al destino, solo tomar conexiones, no todas las estaciones con interfaz gráfica
    #El usuario tiene que decir donde es el "nido" y donde es la "comida" si se pide la misma ruta, no recalcular, considerando horas pico o accidentes, de la misma forma algún nodo podría desaoarece momentaneamente
    #Listado de conexiones, hacer calculo en el momento, considerar latitud y longitud para estaciones
    #Hacer un nuevo plano con la latitud y longitud, considerando las distancias reales, generando nuevo mapa, transbordes tomarlos como un solo punto
    #Considerar el que desaparezca una conexión o nodo para reformular


