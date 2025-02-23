import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import disk, skeletonize, dilation, remove_small_objects,closing,opening,convex_hull_image
from skimage import io, measure, color
from skimage.transform import resize
from skimage.segmentation import clear_border
from skimage.filters import threshold_otsu

imagendb=io.imread(r'D:\Upiita\6to\IA\Fotos\Abecedario.jpg')
# imagenp=io.imread(r'D:\Upiita\6to\IA\Fotos\Poema_T.jpg')
imagenp=io.imread(r'D:\Upiita\6to\IA\Fotos\poema_T1.bmp')

abecedario = (
    'A','B', 'C', 'D','E',  'F','G',  'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'Ñ' , 'O','P', 'Q', 'R','S','T','U','V','W','X','Y', 'Z',
    'a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','ñ',
    'o','p','q','r','s','t','u','v','w','x','y','z',
    'á', 'é', 'í', 'ó','ú',
    'Á', 'É', 'Í','Ó','Ú'
)

def gbf(imagen,im):
    if im == 'w':
        gris = color.rgb2gray(imagen)
        binario = (gris < 0.5)
        estructura = disk(1.8)
        binario = dilation(binario, estructura) 
        binario = closing(binario, estructura) 
    elif im == 'pv':
        gris = color.rgb2gray(imagen)
        binario = (gris < 0.5)
    elif im == 'p':
        binario=imagen
        estructura = disk(.9)
        binario = dilation(binario, estructura) 
        binario = closing(binario, estructura) 
    return binario

def recorta_lineas(imagen):
    # imagen = gbf(imagen)
    puntosY = []
    imagenes = []
    while np.any(imagen == 1):
        for fila in range(0, imagen.shape[0]):
            if np.any(imagen[fila, :] == 1):
                puntosY.insert(0, fila)
                break
        for fila in range(puntosY[0], imagen.shape[0]):
            if np.all(imagen[fila, :] == 0):
                puntosY.append(fila)
                break
        if len(puntosY) == 2:
            recorte = imagen[puntosY[0]-4:puntosY[1]+2, :]
            imagen = imagen[puntosY[1]:imagen.shape[0], :]
            imagenes.append(recorte)
            puntosY = []
    return None, imagen, imagenes

def extrae_letras(recorte):
    puntosX = []
    puntosY = []
    recortes = []
    recorte_letra = None  # Inicialización para evitar UnboundLocalError
    coordenadas=[]

    # Cambiar la condición de búsqueda de letras a buscar valores 1
    while np.any(recorte == 1):  # Cambia de np.any(recorte == 0) a np.any(recorte == 1)
        if np.any(recorte == 1):
            # Detecta el primer píxel de la primera letra de izquierda a derecha
            for columna in range(recorte.shape[1]):
                if np.any(recorte[:, columna] == 1):  # Cambia de == 0 a == 1
                    puntosX.insert(0, columna)
                    break

            # Detecta la primera columna sin letras después de la letra
            for columna in range(puntosX[0], recorte.shape[1]):
                if np.all(recorte[:, columna] == 0):  # Cambia de == 1 a == 0
                    puntosX.append(columna)
                    break

            # Encontrar límites de recorte vertical
            for fila in range(0, recorte.shape[0]):
                for columna in range(puntosX[0], puntosX[1]):
                    if recorte[fila, columna] == 1:  # Cambia de == 0 a == 1
                        puntosY.insert(0, fila)
                        break
                if puntosY:
                    break

            recorte_letra = recorte[:, puntosX[0]:puntosX[1]]

            if puntosY:
                for fila in range(puntosY[0], recorte_letra.shape[0]):
                    if np.all(recorte_letra[fila, :] == 0):  # Cambia de == 1 a == 0
                        puntosY.append(fila)
                        break

                recorte_letra = recorte[puntosY[0]-3:puntosY[1]+3, puntosX[0]-3:puntosX[1]+3]
                recortes.append(recorte_letra)
                coordenadas.append((puntosX[0]-3, puntosY[0]-3, puntosX[1]+3, puntosY[1]+3))  # Almacenar coordenadas


            # Actualiza el recorte eliminando la letra procesada
            recorte = recorte[:, puntosX[1]:recorte.shape[1]]
            puntosX = []
            puntosY = []

            # # Mostrar la letra recortada
            # plt.imshow(recorte_letra, cmap='gray')
            # plt.title("Letra recortada")
            # plt.show()
        else:
            break

    # Asegurarse de que recorte_letra tenga algún valor
    if recorte_letra is None:
        recorte_letra = np.zeros((1, 1))  # Valor por defecto si no hay letras

    return recortes, recorte_letra, coordenadas

def guarda_letras(s,wp):
    # Iterar sobre cada línea recortada para extraer sus letras
    coordenadas_letras = []
    for idx, linea in enumerate(s):
        # print(f"Procesando línea {idx + 1}:")
        
        # Aplicar la función extrae_letras a la línea actual
        recortes, _, coords  = extrae_letras(np.array(linea))  
        coordenadas_letras.extend(coords)
        
        # Redimensionar cada letra a 28x28 y almacenarlas en una lista
        if wp=='w':
            recortes_resized = [resize(letra, (28, 28), anti_aliasing=True) for letra in recortes]
        elif wp=='p':
            recortes_resized = [resize(gbf(letra,'p'), (28, 28), anti_aliasing=True) for letra in recortes]
        recortes.extend(recortes_resized)
        for recorte in recortes_resized:
            # Normaliza el recorte
            recorte[recorte > 0] = 1  # Cambia todos los valores mayores que 0 a 1
            vectores.append(recorte.flatten())
    # # Mostrar la imagen original del poema y dibujar rectángulos alrededor de las letras
    # plt.figure(figsize=(10, 6))
    # plt.imshow(imagendb, cmap='gray')
    # plt.axis('off')  # Ocultar los ejes

    # # Dibujar rectángulos alrededor de cada letra
    # for (x0, y0, x1, y1) in coordenadas_letras:
    #     plt.gca().add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, linewidth=1, edgecolor='r', facecolor='none'))

    # plt.title("Imagen del Poema con Recortes de Letras")
    # plt.show()
        
        # Mostrar todas las letras redimensionadas de esta línea
        fig, axes = plt.subplots(1, len(recortes_resized), figsize=(15, 5))
        
        # Asegurar que axes sea iterable incluso si hay una sola letra
        if len(recortes_resized) == 1:
            axes = [axes]
        
        for i, recorte_letra in enumerate(recortes_resized):
            axes[i].imshow(recorte_letra, cmap='gray')
            axes[i].axis('off')  # Ocultar los ejes para mayor claridad
            axes[i].set_title(f"Línea {idx + 1}, Letra {i + 1}")

        plt.tight_layout()
        plt.show()
    return vectores
    

def concatena_letras(letras_recortes, coordenadas, umbral_espacio=10):

    texto = ""  # Inicializa el texto concatenado
    
    # Ordenar las letras y sus coordenadas según la posición x0 (columna inicial)
    letras_con_coords = sorted(zip(letras_recortes, coordenadas), key=lambda x: x[1][0])
    
    for i in range(len(letras_con_coords) - 1):
        letra_actual, (x0_actual, _, x1_actual, _) = letras_con_coords[i]
        letra_siguiente, (x0_siguiente, _, _, _) = letras_con_coords[i + 1]
        
        # Agrega la letra actual al texto
        texto += letra_actual

        # Si la distancia entre letras es mayor que el umbral, añade un espacio
        if x0_siguiente - x1_actual > umbral_espacio:
            texto += " "
    
    # Agrega la última letra
    texto += letras_con_coords[-1][0]
    
    return texto

abc =  imagendb
abc = gbf(abc,'w')*1
vectores=[]
recortes=[]
_,_, s  = recorta_lineas(abc)
vectoresw=guarda_letras(s,'w')

##Red Instar-Compet##
epsilon=0.0153 #Cantidad de información "falsa" que se le da al resto de neuronas
alpha=0.01
W=np.array(vectoresw,dtype=np.float64)
print(f"Dimensión de la matriz de pesos: {W.shape}")

patrones=W

R=len(patrones[0])
b1=R
b1=np.ones(W.shape[0])
epsilon=0.0153
alpha=0.01
iteracion=30
# for epoca in range(10):
#     for idx , patron in enumerate(patrones): 
#         a1=np.dot(W,patron)+b1
#         a2=a1.copy()
#         for _ in range(iteracion): 
#             new_a2=np.zeros_like(a2)
#             for i in range(len(a2)):
#                 ini=epsilon*(np.sum(a2)-a2[i]) 
#                 new_a2[i]=max(0,a2[i]-ini) 
#             a2=new_a2
#         winner_ind=np.argmax(a2)
#         W[winner_ind]+=alpha*(patron-W[winner_ind])
#         b1[winner_ind]-=0.02*(1+b1[winner_ind])


poema =  imagenp
poema = gbf(poema,'pv')*1
vectores=[]
recortes=[]
Salida=[]
_,_, s  = recorta_lineas(poema)
vectoresp=guarda_letras(s,'p')
patrones=np.array(vectoresp,dtype=np.float64)

for idx , patron in enumerate(patrones):
    a1=np.dot(W,patron)+b1
    a2=a1.copy()
    for _ in range(iteracion): 
        new_a2=np.zeros_like(a2)
        for i in range(len(a2)):
            ini=epsilon*(np.sum(a2)-a2[i]) 
            new_a2[i]=max(0,a2[i]-ini) 
        a2=new_a2
    winner_ind=np.argmax(a2)
    # print(f"Patron de entrada {idx+1} : {patron}")
    # print(f"Neurona ganadora {winner_ind+1} : {patron}")
    print(f"Salida final: {a2}\n")
    print(f"Letra: {abecedario[winner_ind]}\n")
    Salida.append(abecedario[winner_ind])

    texto=concatena_letras(Salida,,umbral=10)