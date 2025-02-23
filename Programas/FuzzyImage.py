# Sistema difuso para segmentado de imágenes. El programa esta completo
# Puedes modificar la cantidad de clases, pero esta optimizado para imágenes
# en escala de grises
import numpy as np
import matplotlib.pyplot as plt
from skimage import data

# -----------------------------------------
# Lectura y preprocesamiento de la imagen
# -----------------------------------------
# Leer la imagen
imagen = data.camera()

# Inicializar una lista para almacenar los valores del histograma
histograma = [0] * 256

# Recorrer cada píxel de la imagen para calcular el histograma
for fila in range(imagen.shape[0]):
    for columna in range(imagen.shape[1]):
        valor_pixel = imagen[fila, columna]
        histograma[valor_pixel] += 1

# Convertir la imagen en un vector columna
datos = imagen.reshape(-1, 1)

# Crear una figura con dos subgráficos
plt.figure(figsize=(12, 5))

# Mostrar la imagen original en el primer subgráfico
plt.close('all')
plt.subplot(1, 2, 1)
plt.imshow(imagen, cmap='gray')
plt.title('Imagen Original')
plt.axis('off')  # Ocultar los ejes

# Mostrar el histograma en el segundo subgráfico
plt.subplot(1, 2, 2)
plt.bar(range(256), histograma)
plt.xlabel('Valor de intensidad')
plt.ylabel('Frecuencia')
plt.title('Histograma de la Imagen')

# Mostrar el gráfico
plt.tight_layout()
#plt.show()


# # Leer la imagen 'camera' de skimage
# imagen = data.camera()

# # Mostrar la imagen original
# plt.close('all')
# plt.figure(figsize=(6, 6))
# plt.imshow(imagen, cmap='gray')
# plt.title('Imagen Original')
# plt.axis('off')
# plt.show()

# Convertir la imagen en un vector columna de datos
datos = imagen.reshape(-1, 1).astype(np.float32)

# Imprimir información básica sobre los datos
print(f"Tamaño del vector de datos: {datos.shape}")
print(f"Valor mínimo y máximo de los datos: {datos.min()}, {datos.max()}")

# ---------------------------------------
# Parámetros del algoritmo Fuzzy C-Means
# ---------------------------------------

num_clases = 10  # Número de clústeres deseados
m = 2.0  # Parámetro de fuzziness
epsilon = 0.01  # Criterio de convergencia
max_iter = 300  # Número máximo de iteraciones

# ---------------------------------------------------------
# Inicialización de los centros y la matriz de pertenencia
# ---------------------------------------------------------

# Inicializar los centros de manera aleatoria dentro del rango de intensidades
np.random.seed(42)  # Para reproducibilidad
centros = np.random.uniform(low=datos.min(), high=datos.max(), size=(num_clases, 1))

# Inicializar la matriz de pertenencia con ceros
pertenencia = np.zeros((datos.shape[0], num_clases))

# Mostrar los centros iniciales
print(f"Centros iniciales:\n{centros}")

# --------------------------------------
# Función para calcular las distancias
# --------------------------------------

def calcular_distancias(datos, centros):
    """
    Calcula la distancia euclidiana entre cada dato y cada centro.
    """
    distancias = np.zeros((datos.shape[0], num_clases))
    for k in range(num_clases):
        distancias[:, k] = np.linalg.norm(datos - centros[k], axis=1)
    # Evitar divisiones por cero reemplazando ceros con un valor muy pequeño
    distancias = np.fmax(distancias, np.finfo(np.float64).eps)
    return distancias

# ------------------------------------------
# Iteraciones del algoritmo Fuzzy C-Means
# -----------------------------------------

for iteration in range(max_iter):
    # Guardar copia de los centros anteriores para verificar convergencia
    centros_previos = centros.copy()
    
    # Paso 1: Calcular distancias
    distancias = calcular_distancias(datos, centros)
    
    # Paso 2: Actualizar matriz de pertenencia
    exponent = 2 / (m - 1)
    inv_distancias = 1.0 / distancias ** exponent
    suma_inv = np.sum(inv_distancias, axis=1, keepdims=True)
    pertenencia = inv_distancias / suma_inv
    
    # Paso 3: Actualizar centros
    numerador = np.dot(pertenencia.T ** m, datos)
    denominador = np.sum(pertenencia.T ** m, axis=1, keepdims=True)
    centros = numerador / denominador
    
    # Paso 4: Verificar convergencia
    max_cambio = np.max(np.abs(centros - centros_previos))
    print(f"Iteración {iteration + 1}: cambio máximo en centros = {max_cambio}")
    if max_cambio < epsilon:
        print("Criterio de convergencia alcanzado.")
        break

# ---------------------
# Resultados finales
# ----------------------

print(f"Centros finales:\n{centros}")

# Asignar cada pixel al clúster con mayor pertenencia
labels = np.argmax(pertenencia, axis=1)
imagen_segmentada = labels.reshape(imagen.shape)

# Mostrar la imagen segmentada
plt.figure(figsize=(6, 6))
plt.imshow(imagen_segmentada, cmap='gray')
plt.title('Imagen Segmentada por Fuzzy C-Means')
plt.axis('off')
#plt.show()

# -----------------------------------------------
# Gráfico de conjuntos difusos y centros finales
# -----------------------------------------------

# Gráfico de membresías
plt.figure(figsize=(10, 6))
for j in range(num_clases):
    plt.plot(datos, pertenencia[:, j], '.', label=f'Clase {j + 1} (Centro: {centros[j][0]:.2f})')

# Graficar los centros finales
plt.scatter(centros, np.ones(num_clases), c='red', marker='x', s=100, label='Centros finales')

plt.title('Distribución de Conjuntos Difusos y Centros Finales')
plt.xlabel('Valor de Intensidad del Pixel')
plt.ylabel('Grado de Pertenencia')
plt.legend()
plt.show()

# ----------------------------------------------
# Cálculo de las métricas de Validity Cluster
# ----------------------------------------------

# Coeficiente de Partición (Partition Coefficient)
PC = np.sum(pertenencia ** 2) / datos.shape[0]
print(f"Coeficiente de Partición (PC): {PC:.4f}")

# Separabilidad Promedio de Particiones (Average Partition Separability)
APS = np.mean([np.sum(pertenencia[:, j] / np.sum(pertenencia, axis=1)) / datos.shape[0] for j in range(num_clases)])
print(f"Separabilidad Promedio de Particiones (APS): {APS:.4f}")

# Entropía de Partición (Partition Entropy)
PE = -np.sum(pertenencia * np.log(pertenencia)) / datos.shape[0]
print(f"Entropía de Partición (PE): {PE:.4f}")




