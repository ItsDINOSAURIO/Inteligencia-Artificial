# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.spatial.distance import cdist
# from scipy.signal import butter,filtfilt,correlate
# import scipy.io



# # Paso 1: Preprocesamiento de la señal (utilizando tu código anterior)
# # Este es el punto en el que "signal_normal" representa la señal procesada final
# # Supongamos que "signal_normal" es la salida de tu preprocesador de señal

# mat=scipy.io.loadmat(r"D:\Upiita\6to\IA\Fotos\complejo.mat")
# ecg_signal=mat["ECG"].flatten()
# fs=360 #frecuencia de muestreo
# indices_inicio=[70,175,280,385,490]#[175,280,385]
# N=50 #Numero de muestras después de cada complejo

# complejos=[]
# for idx in indices_inicio:
#     complejo=ecg_signal[idx:idx+N]
#     complejos.append(complejo)

# def bandpass_filter(signal,lowcut,highcut,fs,order=6):
#     nyq=0.5*fs
#     low=lowcut/nyq
#     high=highcut/nyq
#     b,a=butter(order,[low,high],btype='band')
#     y=filtfilt(b,a,signal)
#     return y

# lowcut=0.5
# highcut=40.0

# complejos_preprocessed=[]
# for complejo in complejos:
#     complejo_filtrado=bandpass_filter(complejo,lowcut,highcut,fs)
#     complejo_corrected=complejo_filtrado-np.mean(complejo_filtrado)
#     complejos_preprocessed.append(complejo_corrected)

# def shift_signal(signal,lag):
#     if lag>0:
#         shifted_signal=np.concatenate((np.zeros(lag),signal[:-lag])) #ajusta con ceros la señal tanto por delante como por detras para que todas queden del mismo tamaño
#     elif lag<0:
#         shifted_signal=np.concatenate((signal[-lag:],np.zeros(-lag)))
#     else: 
#         shifted_signal=signal
#     return shifted_signal

# reference=complejos_preprocessed[0] #usar el primer complejo como referencia
# aligned_complexes=[reference]
# for i in range(1,len(complejos_preprocessed)):
#     signal=complejos_preprocessed[i]
#     corr=correlate(reference,signal,mode='full')
#     lag=np.argmax(corr)-(len(signal)-1)
#     aligned_signal=shift_signal(signal,lag)
#     aligned_complexes.append(aligned_signal)

# unified_signal=np.mean(aligned_complexes,axis=0)
# signal_normal=(unified_signal-np.mean(unified_signal))/np.std(unified_signal)

# # Paso 2: Configuración de la red neuronal de base radial (RBF)
# n_neurons = 40  # Más de 20 neuronas
# centers = np.linspace(0, len(signal_normal) - 1, n_neurons, dtype=int)
# centers = signal_normal[centers]  # Usamos valores de la señal como centros
# centers = np.linspace(np.min(signal_normal), np.max(signal_normal), n_neurons)
# spread = 1.0 / np.sqrt(2 * n_neurons)  # Parámetro que controla la amplitud de las Gaussianas

# def rbf(x, center, spread):
#     return np.exp(-cdist(x[:, None], center[:, None]) ** 2 / (2 * spread ** 2))

# # Generación de las salidas de la capa RBF
# rbf_outputs = rbf(np.arange(len(signal_normal)), centers, spread)

# # Paso 3: Ajuste de los pesos (Entrenamiento)
# # Usamos la salida deseada que es la misma señal
# weights = np.linalg.pinv(rbf_outputs).dot(signal_normal)

# # Salida de la red
# signal_output = rbf_outputs.dot(weights)

# # Paso 4: Visualización de resultados
# plt.figure(figsize=(12, 8))

# # Subplot 1: Señal Inicial (señal preprocesada)
# plt.subplot(3, 1, 1)
# plt.plot(signal_normal, label='Señal Inicial')
# plt.title('Señal Inicial (Normalizada)')
# plt.legend()
# plt.grid()

# # Subplot 2: Distribución de Señales de Entrenamiento
# for center in centers:
#     plt.subplot(3, 1, 2)
#     plt.plot(np.arange(len(signal_normal)), rbf(np.arange(len(signal_normal)), np.array([center]), spread)[:, 0])
# plt.title('Distribución de Señales de Entrenamiento (Centros Gaussianos)')
# plt.grid()

# # Subplot 3: Señal de Salida de la RBF
# plt.subplot(3, 1, 3)
# plt.plot(signal_output, label='Señal de Salida RBF', color='orange')
# plt.title('Señal de Salida de la Red Neuronal RBF')
# plt.legend()
# plt.grid()

# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.signal import butter, filtfilt, correlate
import scipy.io

# Paso 1: Preprocesamiento de la señal
mat = scipy.io.loadmat(r"D:\Upiita\6to\IA\Fotos\complejo.mat")
ecg_signal = mat["ECG"].flatten()
fs = 360  # frecuencia de muestreo
indices_inicio = [70, 175, 280, 385, 490]
N = 50  # Numero de muestras después de cada complejo

def bandpass_filter(signal, lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, signal)
    return y

def shift_signal(signal, lag):
    if lag > 0:
        shifted_signal = np.concatenate((np.zeros(lag), signal[:-lag]))
    elif lag < 0:
        shifted_signal = np.concatenate((signal[-lag:], np.zeros(-lag)))
    else:
        shifted_signal = signal
    return shifted_signal

def preprocess_signal(ecg_signal, indices_inicio, N, fs, lowcut=0.5, highcut=40.0):
    # Extraer complejos
    complejos = [ecg_signal[idx:idx+N] for idx in indices_inicio]
    
    # Filtrar y normalizar complejos
    complejos_preprocessed = []
    for complejo in complejos:
        complejo_filtrado = bandpass_filter(complejo, lowcut, highcut, fs)
        complejo_corrected = complejo_filtrado - np.mean(complejo_filtrado)
        complejos_preprocessed.append(complejo_corrected)
    
    # Alinear complejos
    reference = complejos_preprocessed[0]
    aligned_complexes = [reference]
    
    for signal in complejos_preprocessed[1:]:
        corr = correlate(reference, signal, mode='full')
        lag = np.argmax(corr) - (len(signal) - 1)
        aligned_signal = shift_signal(signal, lag)
        aligned_complexes.append(aligned_signal)
    
    # Unificar y normalizar señal
    unified_signal = np.mean(aligned_complexes, axis=0)
    signal_normal = (unified_signal - np.mean(unified_signal)) / np.std(unified_signal)
    
    return signal_normal

class RBFNetwork:
    def __init__(self, n_neurons, spread_factor=1.0):
        self.n_neurons = n_neurons
        self.spread_factor = spread_factor
        self.centers = None
        self.spread = None
        self.weights = None
    
    def _rbf_function(self, x, centers, spread):
        """Función de base radial gaussiana"""
        x_matrix = x.reshape(-1, 1)
        distances = cdist(x_matrix, centers.reshape(-1, 1))
        return np.exp(-distances**2 / (2 * spread**2))
    
    def fit(self, X, y):
        """Entrenamiento de la red RBF"""
        self.centers = np.linspace(np.min(X), np.max(X), self.n_neurons)
        avg_distance = np.mean(np.diff(self.centers))
        self.spread = self.spread_factor * avg_distance
        rbf_outputs = self._rbf_function(X, self.centers, self.spread)
        self.weights = np.linalg.pinv(rbf_outputs).dot(y)
        return self
    
    def predict(self, X):
        """Predicción usando la red RBF"""
        if self.centers is None or self.weights is None:
            raise ValueError("La red debe ser entrenada antes de hacer predicciones")
        rbf_outputs = self._rbf_function(X, self.centers, self.spread)
        return rbf_outputs.dot(self.weights)
    
    def get_weighted_rbfs(self, X):
        """Obtener las funciones RBF individuales multiplicadas por sus pesos"""
        rbf_outputs = self._rbf_function(X, self.centers, self.spread)
        weighted_rbfs = np.zeros((len(X), len(self.centers)))
        for i in range(len(self.centers)):
            weighted_rbfs[:, i] = rbf_outputs[:, i] * self.weights[i]
        return weighted_rbfs

# Preprocesamiento de la señal [código anterior]
signal_normal = preprocess_signal(ecg_signal, indices_inicio, N, fs)
X = np.arange(len(signal_normal))

# Crear y entrenar la red RBF
rbf_net = RBFNetwork(n_neurons=25, spread_factor=1)
rbf_net.fit(X, signal_normal)
signal_output = rbf_net.predict(X)

# Obtener las funciones RBF ponderadas
weighted_rbfs = rbf_net.get_weighted_rbfs(X)

# Visualización de resultados
plt.figure(figsize=(15, 12))

# Señal Original
plt.subplot(3, 1, 1)
plt.plot(signal_normal, label='Señal Original', linewidth=2)
plt.title('Señal Original (Normalizada)')
plt.legend()
plt.grid(True)

# Funciones de Base Radial sin ponderar
# plt.subplot(4, 1, 2)
# rbf_outputs = rbf_net._rbf_function(X, rbf_net.centers, rbf_net.spread)
# for i in range(len(rbf_net.centers)):
#     plt.plot(X, rbf_outputs[:, i], alpha=0.5, linestyle='--')
# plt.title('Funciones de Base Radial (Sin ponderar)')
# plt.grid(True)

# Funciones de Base Radial ponderadas
plt.subplot(3, 1, 2)
for i in range(len(rbf_net.centers)):
    plt.plot(X, weighted_rbfs[:, i], alpha=0.7)
plt.title('Funciones de Base Radial Ponderadas')
plt.grid(True)

# Comparación de señales
plt.subplot(3, 1, 3)
plt.plot(signal_normal, label='Señal Original', alpha=0.7, linewidth=2)
plt.plot(signal_output, label='Señal Reconstruida', color='orange', linewidth=2, linestyle='--')
for i in range(len(rbf_net.centers)):
    plt.plot(X, weighted_rbfs[:, i], alpha=0.3, color='gray', linestyle='--')
plt.title('Señal Original, Reconstruida y Contribuciones Individuales')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Calcular y mostrar el error
mse = np.mean((signal_normal - signal_output)**2)
print(f"Error cuadrático medio: {mse:.6f}")

# Mostrar información sobre los pesos
print("\nEstadísticas de los pesos:")
print(f"Peso máximo: {np.max(rbf_net.weights):.4f}")
print(f"Peso mínimo: {np.min(rbf_net.weights):.4f}")
print(f"Peso promedio: {np.mean(rbf_net.weights):.4f}")
print(f"Desviación estándar de los pesos: {np.std(rbf_net.weights):.4f}")