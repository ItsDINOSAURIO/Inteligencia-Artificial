import numpy as np
import matplotlib.pyplot as plt 
from skimage import data

imagen = data.camera()

#inicializar una lisat para almacenar los valores del histograma
histograma = [0]*256
#Recorrer cada píxel de la imagen para calcular el histograma
for fila in range(imagen.shape[0]):
    for columna in range(imagen.shape[1]):
        valor_pixel = imagen[fila,columna]
        histograma[valor_pixel] += 1

plt.figure(figsize = (12,5))
#Mostrar en el primer subgráfico la imagen original 
plt.close('all')
plt.subplot(1,2,1)
plt.imshow(imagen, cmap = 'gray')
plt.title('Imagen Original')
plt.axis('off')

#Mostrar el histograma en el segundo subgráfico
plt.subplot(1, 2, 2)
plt.bar(range(256), histograma)
plt.xlabel('Valor de intensidad')
plt.ylabel('Frecuencia')
plt.title('Histograma de la Imagen')

# Mostrar el gráfico
plt.tight_layout()
#plt.show()

data = imagen.reshape(-1,1)#convierte en vector columna
#--------------------------------------------------------------
#función para calcular las distancias 
#--------------------------------------------------------------
#Esta función regresa una matriz de filas = número de datos x 3 columnas
#en cada columna está la distancia del dato al centro de la clase
def calc_distancias(data,centros,num_clases):
    #Calcula la distancia euclidiana entre cada dato y cada centro
    distancias = np.zeros((data.shape[0],num_clases))
    for k in range(num_clases):
        #calcula la distancia entre cada punto y cada centro
        #la distancia se guarda en un vector de tres columnas
        distancias[:,k] = np.linalg.norm(data - centros[k],axis = 1)
    #for k in range(num_clases):
     #   for filas in range(data.shape[0]):
      #      distancias[filas,k] = np.sqrt((data[filas]-centros[k])**2)    
    #Evitar divisiones por cero reemplazando ceros con un valor muy pequeño
    distancias = np.fmax(distancias, np.finfo(np.float64).eps)
    


    return distancias
#---------------------------------------------------------------
#           función para calcular WCSS para método del codo
#---------------------------------------------------------------
def calc_wcss(data,labels,centros):
    wcss = 0
    for k in range(len(centros)):
        #asigna los puntos que pertenezcan a una clase de acuerdo con labels
        cluster_puntos = data[labels == k]
        #suma de las distancias entre los puntos y los centros
        wcss += np.sum((cluster_puntos - centros[k])**2)
    return wcss
#--------------------------------------------------------------
#                       ALGORITMO KMEANS
#--------------------------------------------------------------
np.random.seed(42)  # Para reproducibilidad
iter_max = 100
def calc_kmeans(data,max_clusters):
    #lista para guardar la suma de las distancias al cuadrado
    distancias_codo = []
    
    #Se realizan calculos desde 1 hasta el número clases solicitado por el usuario
    for num_clases in range(1,max_clusters+1):
        #Inicializa los centros de manera aleatoria dentro del rango de intensidades
        centros = np.random.uniform(low = data.min(), high = data.max(), size = (num_clases,1))
        #arreglo para etiquetar datos de acuerdo con la distancia a los centros
        labels = np.zeros(data.shape[0])

        for iteration in range(iter_max):
            #Guarda una copia de los centros anteriores para verificar convergencia
            centros_previos = centros.copy()
            #Calcular las distancias
            distancias = calc_distancias(data,centros,num_clases)
            #Asignar cada punto al centroide más cercano
            labels = np.argmin(distancias, axis = 1)
            #recalcular los centroides promediando los datos asignados
            for k in range(num_clases):
                centros[k] = data[labels == k].mean(axis = 0)#obtiene promedio de cada clase
            if np.allclose(centros,centros_previos):
                print(f"convergencia alcanzada en la iteracion {iteration}")
                break
        #calcula la suma de las distancias al cuadrado para EM
        wcss = calc_wcss(data,labels,centros)
        distancias_codo.append(wcss)#guarda wcss de todos los números de clases
    return centros, distancias_codo,labels

#----------------------------------------------------------------------
centrosF, codo,labelsCodo = calc_kmeans(data,10)

# Graficar el método del codo
plt.figure(figsize=(8, 6))
plt.plot(range(1,11), codo, marker='o')
plt.xlabel('Número de clusters')
plt.ylabel('Inercia (WCSS)')
plt.title('Método del codo para determinar el número óptimo de clusters')
#plt.show()

#-----------------------------------------------------------------------

num_clases = 3
centros3C,codo3C,labels = calc_kmeans(data,num_clases)

#Calcula los valores máximos y mínimos de cada clase
minimos = np.zeros([1,num_clases])
maximos = np.zeros([1,num_clases])
for k in range(num_clases):

    minimos[0,k] = np.min(data[labels == k])
    maximos[0,k] = np.max(data[labels == k])
    
# minC1 = np.min(data[labels == 0])
# maxC1 = np.max(data[labels == 0])
# minC2 = np.min(data[labels == 1])
# maxC2 = np.max(data[labels == 1])
# minC3 = np.min(data[labels == 2])
# maxC3 = np.max(data[labels == 2])

segmentada = np.zeros([imagen.shape[0],imagen.shape[1]])

for filas in range(imagen.shape[0]):
    for columnas in range(imagen.shape[1]):
        for k in range(num_clases):
            if imagen[filas,columnas]>=minimos[0,k] and imagen[filas,columnas]<=maximos[0,k]:
                segmentada[filas,columnas] = int(255*(k+1)/num_clases) 
                break
            else:
                continue
 
          
plt.figure(figsize = (10,5))
plt.imshow(segmentada, cmap = 'gray')
plt.tight_layout()
plt.show()