import numpy as np
import random
from collections import defaultdict
nodos={
    0:(1,1),
    1:(1.5,3.5),
    2:(4,3),
    3:(5,1.5),
    4:(4,6),
    5:(6,3.5),
    6:(7,6)
}

def calcular_distancia(nodo1,nodo2):
    x1,y1=nodos[nodo1]
    x2,y2=nodos[nodo2]
    distancia=np.sqrt((x2-x1)**2+(y2-y1)**2)
    return distancia

conexiones={}
for (nodo1,nodo2) in [
    (0,1),
    (0,2),
    (0,3),
    (1,2),
    (1,4),
    (2,3),
    (2,4),
    (3,5),
    (4,6),
    (5,6)
    ]:
    dist=calcular_distancia(nodo1,nodo2)
    conexiones[(min(nodo1,nodo2),max(nodo1,nodo2))]=dist

print(conexiones)
feromonas={arista:0.1 for arista in conexiones}
rho=0.9
alpha=1
beta=1
Q=1
num_hormigas=2
num_iteraciones=323
heuristica={arista:1.0/conexiones[arista] for arista in conexiones} #Visibilidad

mejor_camino=None
mejor_longitud=float('inf')

# print(conexiones)

for iteraciones in range(num_iteraciones):
    caminos_todos=[]
    longitudes_todos=[]
    for hormiga in range(num_hormigas):
        # print("{hormiga}")
        nodo_actual=0
        nodos_visitados=[nodo_actual]
        camino=[]
        longitud_total=0

        while nodo_actual != 6:
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

        if nodo_actual==6:
            caminos_todos.append(camino)
            longitudes_todos.append(longitud_total)
        
            if longitud_total < mejor_longitud:
                mejor_longitud = longitud_total
                mejor_camino = camino

    # Evaporación y refuerzo de feromonas
    for arista in feromonas:
        feromonas[arista] *= (1-rho) 

    # print(feromonas)

    for camino, longitud in zip(caminos_todos, longitudes_todos):
        for i in range(len(camino) - 1):
            arista = (min(camino[i], camino[i + 1]), max(camino[i], camino[i + 1]))
            feromonas[arista] += Q / longitud
    # print(feromonas)

print(f"Mejor camino encontrado: {mejor_camino} con longitud {mejor_longitud}")


    #Tomar todo el mapa de la ciudad de mexico de las lineas dle metro y buscar cuales nodos comparten más de 1 línea, resolver con ACO
    #Proporcionar un destino y un inicio, para determinar las conexiones necesarias para llegar al destino, solo tomar conexiones, no todas las estaciones con interfaz gráfica
    #El usuario tiene que decir donde es el "nido" y donde es la "comida" si se pide la misma ruta, no recalcular, considerando horas pico o accidentes, de la misma forma algún nodo podría desaoarece momentaneamente
    #Listado de conexiones, hacer calculo en el momento, considerar latitud y longitud para estaciones
    #Hacer un nuevo plano con la latitud y longitud, considerando las distancias reales, generando nuevo mapa, transbordes tomarlos como un solo punto
    #Considerar el que desaparezca una conexión o nodo para reformular