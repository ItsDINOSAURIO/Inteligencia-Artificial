# import numpy as np
# import matplotlib.pyplot as plt

# plt.close()
# plt.ion()
# fig,ax=plt.subplots()

# tamano_mapa=10 #red 10x10 : 100 neuronas
# epocas=1000
# tasa_aprendizaje_inicial=0.8
# vecindad_inicial=5

# entradas=np.random.rand(300,2) #bidimensional
# w=np.random.uniform(0.8,0.2,(tamano_mapa,tamano_mapa,2)) #máximo valor de la w es .8 y el mínimo .2

# for epoca in range(epocas):
#     tasa_aprendizaje=tasa_aprendizaje_inicial*(1-epoca/epocas)
#     vecindad=max(1,int(vecindad_inicial*(1-epoca/epocas))) #Reducción del vecindario evitando la indeterminación de 0 por lo que el mínimo será 1
#     for x in entradas:
#         distancias=np.sum((w-x)**2,axis=-1) #Suma de distancias cuadradas: se evita la raíz cuadrada pues finalmente el más cercano será siempre el más cercano axis=0 fila, axis=1 columna axis=-1 todo el arreglo
#         ganadora=np.unravel_index(np.argmin(distancias),distancias.shape) #Ravel==Flatten por lo tanto unravel, agarra un vector y lo transforma en una matriz; Se saca la posición de la neurona ganadora
#         filas_g,columnas_g=ganadora
#         i_min,i_max=max(0,filas_g-vecindad),min(tamano_mapa,filas_g+vecindad+1)
#         j_min,j_max=max(0,columnas_g-vecindad),min(tamano_mapa,columnas_g+vecindad+1)

#         #Actualiza las neuronas de un vecindarioc
#         for i in range(i_min,i_max):
#             for j in range(j_min,j_max):
#                 distancia_cuadrada=(i-filas_g)**2+(j-columnas_g)**2
#                 influencia=(np.exp(-distancia_cuadrada/(2*(vecindad**2)))) #Función de vecindad
#                 w[i,j]+=tasa_aprendizaje*influencia*(x-w[i,j])

#         if (epoca+1)%5==0 or epoca ==epocas-1:
#             ax.clear()
#             ax.plot(entradas[:,0],entradas[:,1],'.b')
#             ax.plot(w[:,:,0],w[:,:,1],'or')
#             ax.plot(w[:,:,0],w[:,:,1],'k',linewidth=2)
#             ax.plot(w[:,:,0].T,w[:,:,1].T,'k',linewidth=2)
#             ax.set_title(f'Tiempo = {epoca+1}')
#             plt.pause(0.1)




# plt.show()

import numpy as np
import matplotlib.pyplot as plt
#--------------
tamano_mapa = 10  # red de 10x10= 100 neuronas
num_epocas = 1000
tasa_aprendizaje_inicial = 0.8
vecindad_inicial = 5  #----> 1
#--------------
# datos iniciales aleatorios
entradas = np.random.rand (300,2)  #Patrones de entrada, 300 patrones,y 2 por bidimensional
#pesos sinapticos iniciales
w = np.random.uniform(0.8, 0.2,(tamano_mapa, tamano_mapa,2))
#-------------------

plt.close('all')
plt.ion() 
fig,ax = plt.subplots()

for epoca in range(num_epocas):
    tasa_aprendizaje = tasa_aprendizaje_inicial * (1-epoca/num_epocas)
    vecindad = max(1, int(vecindad_inicial * (1-epoca/num_epocas)))
    for x in entradas:
        distancias = np.sum((w-x)**2,axis=-1) # axis-1 es todo el arreglo
        ganadora = np.unravel_index(np.argmin(distancias),distancias.shape)  # unravel: recibe un vector y lo convierte en matriz

        filas_g,columnas_g = ganadora
        i_min, i_max = max(0,filas_g - vecindad), min(tamano_mapa,filas_g + vecindad + 1)
        j_min, j_max = max(0,columnas_g - vecindad), min(tamano_mapa,columnas_g + vecindad + 1)

        for i in range (i_min, i_max):
            for j in range (j_min, j_max):
                distancia_cuadrada = (i-filas_g)*2 + (j-columnas_g)*2
                influencia =np.exp(-distancia_cuadrada/(2*(vecindad**2)))
                w[i,j] += tasa_aprendizaje*influencia*(x-w[i,j])

    if (epoca+1) % 5 == 0 or epoca == num_epocas-1:
        ax.clear()
        ax.plot(entradas[:,0],entradas[:,1],'.b')
        ax.plot(w[:,:,0], w[:,:,1], 'or')
        ax.plot(w[:,:,0], w[:,:,1], 'k',linewidth=2)
        ax.plot(w[:,:,0].T, w[:,:,1].T, 'k',linewidth=2)
        ax.set_title(f'Tiempo = {epoca+1}')
        plt.pause(0.1)

plt.ioff()
plt.show()