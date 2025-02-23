import scipy.io
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

mat1=scipy.io.loadmat(r"D:\Upiita\6to\IA\Fotos\complejo.mat")
corazon=mat1["ECG"].flatten()
plt.figure(figsize=(10,6))
plt.plot(corazon,label='Senal Original',linewidth=2)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.legend()

indices_inicio=[70,175,280,385,490]
pat_list=[] #Patrones
tar_list=[] #Targets
largo=50
for inicio in indices_inicio:
    fin=inicio+largo
    complejo=corazon[inicio:fin]
    maximo=np.max(np.abs(complejo))
    complejo_norm=complejo/maximo
    if complejo_norm.ndim==1:
        complejo_norm=complejo_norm[:,np.newaxis]
        pat=np.linspace(0,1,largo)
        pat=pat[:,np.newaxis]
        pat_list.append(pat)
        tar_list.append(complejo_norm)
        # plt.figure()
        plt.plot(complejo)
        plt.pause(3)
pat=np.vstack(pat_list)
tar=np.vstack(tar_list)

plt.show()