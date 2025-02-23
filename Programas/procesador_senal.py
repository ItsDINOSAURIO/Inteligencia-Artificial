import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter,filtfilt,correlate
plt.close('all')

mat=scipy.io.loadmat(r"D:\Upiita\6to\IA\Fotos\complejo.mat")
ecg_signal=mat["ECG"].flatten()
fs=360 #frecuencia de muestreo
indices_inicio=[70,175,280,385,490]#[175,280,385]
N=50 #Numero de muestras después de cada complejo

complejos=[]
for idx in indices_inicio:
    complejo=ecg_signal[idx:idx+N]
    complejos.append(complejo)

def bandpass_filter(signal,lowcut,highcut,fs,order=6):
    nyq=0.5*fs
    low=lowcut/nyq
    high=highcut/nyq
    b,a=butter(order,[low,high],btype='band')
    y=filtfilt(b,a,signal)
    return y

lowcut=0.5
highcut=40.0

complejos_preprocessed=[]
for complejo in complejos:
    complejo_filtrado=bandpass_filter(complejo,lowcut,highcut,fs)
    complejo_corrected=complejo_filtrado-np.mean(complejo_filtrado)
    complejos_preprocessed.append(complejo_corrected)

def shift_signal(signal,lag):
    if lag>0:
        shifted_signal=np.concatenate((np.zeros(lag),signal[:-lag])) #ajusta con ceros la señal tanto por delante como por detras para que todas queden del mismo tamaño
    elif lag<0:
        shifted_signal=np.concatenate((signal[-lag:],np.zeros(-lag)))
    else: 
        shifted_signal=signal
    return shifted_signal

reference=complejos_preprocessed[0] #usar el primer complejo como referencia
aligned_complexes=[reference]
for i in range(1,len(complejos_preprocessed)):
    signal=complejos_preprocessed[i]
    corr=correlate(reference,signal,mode='full')
    lag=np.argmax(corr)-(len(signal)-1)
    aligned_signal=shift_signal(signal,lag)
    aligned_complexes.append(aligned_signal)

unified_signal=np.mean(aligned_complexes,axis=0)
signal_normal=(unified_signal-np.mean(unified_signal))/np.std(unified_signal)

plt.figure(figsize=(12,8))
plt.subplot(3,1,1)
for i,complejo in enumerate(complejos):
    plt.plot(complejo)
    plt.title('Señal original')
plt.subplot(3,1,2)
for i,aligned_signal in enumerate(aligned_complexes):
    plt.plot(aligned_signal)
    plt.title('Señal alineada')
plt.subplot(3,1,3)
plt.plot(signal_normal)
plt.title('Señal normalizada')

plt.show()

# Hacer seguidor de señal con base radial
#Con 20 se podrá adaptar bien, probar desde de 10, la señal normalizada es la señal de "control"
#Señal de partida
#Distribución de conjuntos 
#Comparación entre señal original y la salida de la neurona
#Recortar imagen y guardar como DelgadoHernandez.jpg