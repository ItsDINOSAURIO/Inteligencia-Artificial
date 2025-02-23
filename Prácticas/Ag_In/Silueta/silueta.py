import numpy as np
import matplotlib.pyplot as plt
from skimage import color, io
from sklearn.metrics import pairwise_distances, silhouette_score

# Cargar la imagen y convertirla a escala de grises
imagen = io.imread(r'D:\Upiita\6to\IA\Fotos\rauw_100.jpg')
imagen_gris = color.rgb2gray(imagen)

# Convertir la imagen en un vector de píxeles (vector columna)
X = imagen_gris.reshape(-1, 1)

# Función para calcular distancias
def calc_distancias(data, centros, num_clases):
    distancias = np.zeros((data.shape[0], num_clases))
    for k in range(num_clases):
        distancias[:, k] = np.linalg.norm(data - centros[k], axis=1)
    distancias = np.fmax(distancias, np.finfo(np.float64).eps)
    return distancias

# Función para ejecutar KMeans con convergencia
def kmeans_converge(data, num_clases, iter_max=100):
    centros = np.random.uniform(low=data.min(), high=data.max(), size=(num_clases, 1))
    labels = np.zeros(data.shape[0])

    for iteration in range(iter_max):
        centros_previos = centros.copy()
        distancias = calc_distancias(data, centros, num_clases)
        labels = np.argmin(distancias, axis=1)
        for k in range(num_clases):
            if np.any(labels == k):
                centros[k] = data[labels == k].mean(axis=0)

        # Checar convergencia
        if np.allclose(centros, centros_previos):
            print(f"Convergencia alcanzada en la iteración {iteration} para {num_clases} clases.")
            break

    return labels, centros

# Evaluar el número de clusters óptimo usando el coeficiente de silueta
silhouette_scores = []
labels_dict = {} 
cluster_range = range(2, 11)  # Evaluar entre 2 y 10 clusters

#K means y Silueta
for num_clusters in cluster_range:
    cluster_labels, _ = kmeans_converge(X, num_clusters)
    labels_dict[num_clusters] = cluster_labels
    if len(np.unique(cluster_labels)) > 1:
        score = silhouette_score(X, cluster_labels)
        silhouette_scores.append(score)
    else:
        silhouette_scores.append(-1) 

# Encontrar el número de clusters con el mejor coeficiente de silueta
best_num_clusters = cluster_range[np.argmax(silhouette_scores)]
print(f"El mejor número de clusters según el coeficiente de silueta es: {best_num_clusters}")
# Crear gráficos de silueta para los mejores números de clusters
fig, ax = plt.subplots(3, 3, figsize=(20, 20))  

for idx, num_clusters in enumerate(cluster_range):
    cluster_labels = labels_dict[num_clusters] 
    
    # Calcular la matriz de distancias entre todos los puntos
    D = pairwise_distances(X)

    # Inicializar las listas para los coeficientes de silueta
    a = np.zeros(X.shape[0])  # Distancia promedio dentro del mismo clúster
    b = np.zeros(X.shape[0])  # Distancia promedio al clúster más cercano
    s = np.zeros(X.shape[0])  # Coeficiente de silueta

    for j in range(X.shape[0]):
        own_cluster = cluster_labels[j]

        # Distancias dentro del mismo clúster
        same_cluster = (cluster_labels == own_cluster)
        same_cluster[j] = False
        if np.sum(same_cluster) > 0:
            a[j] = np.mean(D[j, same_cluster]) 
        else:
            a[j] = 0 

        # Distancias al clúster más cercano
        other_clusters = np.unique(cluster_labels[cluster_labels != own_cluster])
        b[j] = np.min([np.mean(D[j, cluster_labels == other]) for other in other_clusters])

        # Calcular el coeficiente de silueta
        if max(a[j], b[j]) > 0:
            s[j] = (b[j] - a[j]) / max(a[j], b[j])

    # Crear el gráfico de silueta
    q, mod = divmod(idx, 3)
    ax[q][mod].set_xlim([-0.1, 1])
    ax[q][mod].set_ylim([0, len(s) + (num_clusters + 1) * 10])

    # Organizar las siluetas por valor
    y_lower = 10
    for k in range(num_clusters):
        
        cluster_silhouette_values = s[cluster_labels == k]
        cluster_silhouette_values.sort()

        size_cluster_k = cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_k

        
        ax[q][mod].fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_silhouette_values, alpha=0.7)

        
        ax[q][mod].text(-0.05, y_lower + 0.5 * size_cluster_k, str(k))

        y_lower = y_upper + 10 

    # Línea del promedio general de silueta 
    silhouette_avg = np.mean(s)
    ax[q][mod].axvline(x=silhouette_avg, color="red", linestyle="--")

    ax[q][mod].set_title(f"Clusters = {num_clusters}")
    ax[q][mod].set_xlabel("Coeficiente de Silueta")
    ax[q][mod].set_ylabel("ID de muestra")

plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.tight_layout()

# Mostrar la imagen original y su histograma
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(imagen_gris, cmap='gray')
plt.title('Imagen Original a grises')
plt.axis('off')

# Calcular el histograma de la imagen
histograma, bins = np.histogram(imagen_gris, bins=256, range=(0, 1))
bins = (bins[:-1] + bins[1:]) / 2  # Bin centers

plt.subplot(1, 2, 2)
plt.bar(bins, histograma, width=0.01)
plt.xlabel('Valor de Intensidad')
plt.ylabel('Frecuencia')
plt.title('Histograma de la Imagen')
plt.tight_layout()

# Segmentación
num_clusters= 2 

cluster_labels_manual = labels_dict[num_clusters] 
# Reconstruir la imagen segmentada
imagen_segmentada_manual = cluster_labels_manual.reshape(imagen_gris.shape)

# Mostrar la imagen segmentada
plt.figure(figsize=(8, 6))
plt.imshow(imagen_segmentada_manual, cmap='gray')
plt.title(f'Imagen Segmentada con {num_clusters} Clusters')
plt.axis('off')
plt.show()