import numpy as np
import matplotlib.pyplot as plt
from skimage import io
# Función para seleccionar puntos de la imagen manualmente
def seleccionar_puntos_manual(imagen, num_puntos):
    plt.imshow(imagen)
    plt.title(f'Selecciona {num_puntos} puntos de la imagen')
    puntos = plt.ginput(num_puntos)
    plt.close()
    # Convertir las coordenadas a valores RGB de la imagen
    seleccionados = [imagen[int(y), int(x), :] for x, y in puntos]
    return np.array(seleccionados)
# Cargar la primera imagen y permitir al usuario seleccionar 15 puntos manualmente
imagen1 = io.imread(r"D:\Upiita\6to\IA\Fotos\Multimedia.jpg") / 255.0
puntos_seleccionados = seleccionar_puntos_manual(imagen1, 20)



#Parámetros de la Red
nfil=30
ncol=30
nras=3

som=np.random.rand(nfil,ncol,nras)
# Datos=np.random.rand(30,nras)
Datos=puntos_seleccionados

fix,ax=plt.subplots(1,2,figsize=(10,5))
ax[0].imshow(som,aspect='auto')
ax[0].axis('off')

#Crear sistema coordenado para red SOM

x,y=np.meshgrid(np.arange(nfil),np.arange(ncol))

#Parametros de entrenamiento
epocas=100
alpha=0.5
decay=0.05
smg0=10 #Vecindarios gaussiano

#Entrenamiento

for t in range(epocas):
    alpha=alpha*np.exp(-t*decay) #Reducción de alpha
    smg=smg0*np.exp(-t*decay)
    ven=int(np.ceil(smg*3)) #Radio del Vecindario
    for vector in Datos:
        colum=som.reshape(nfil*ncol,nras)
        dista=np.linalg.norm(colum-vector,axis=1)
        #Encontrar neurona ganadora
        bmu_index=np.argmin(dista)
        bmfil,bmcol=np.unravel_index(bmu_index,(nfil,ncol))
        #Generar la función gaussiana
        g=np.exp(-((x-bmcol)**2+(y-bmfil)**2)/(2*smg0**2))
        #Limitar indices del vecindario
        ffil=max(0,bmfil-ven)
        tfil=min(bmfil+ven,nfil-1)
        fcol=max(0,bmcol-ven)
        tcol=min(bmcol+ven,ncol-1)
        #Actualizar valores de las neuronas 
        vecindad=som[ffil:tfil+1,fcol:tcol+1,:]
        G=g[ffil:tfil+1,fcol:tcol+1][...,np.newaxis]
        som[ffil:tfil+1,fcol:tcol+1]+=alpha*G*vector*(vector-vecindad)

    ax[1].imshow(som,aspect='auto')
    ax[1].axis('off')
    ax[1].set_title(f'som en la epoca {t+1}')
    # plt.pause(0.1)

# Cargar la segunda imagen
imagen2 = io.imread(r"D:\Upiita\6to\IA\Fotos\rauw.jpg") / 255.0
# Crear una nueva imagen para almacenar el resultado
salida = np.zeros_like(imagen2)
# Asignar a cada píxel de la segunda imagen un color basado en los pesos de la SOM
for i in range(imagen2.shape[0]):
    for j in range(imagen2.shape[1]):
        pixel = imagen2[i, j, :]
        # Calcular la distancia euclidiana entre el píxel y los pesos de las neuronas
        COLUM = som.reshape(nfil * ncol, nras)
        dista = np.linalg.norm(COLUM - pixel, axis=1)
        # Encontrar la neurona más cercana (BMU)
        bmu_index = np.argmin(dista)
        # Asignar el color de la neurona más cercana al píxel de salida
        salida[i, j, :] = COLUM[bmu_index, :]
# Mostrar la imagen original y la imagen resultante
plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(imagen2)
plt.title("Imagen Original")
plt.subplot(1, 2, 2)
plt.imshow(salida)
plt.title("Imagen Repintada")

plt.show()