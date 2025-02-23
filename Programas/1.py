from skimage import data
import matplotlib.pyplot as plt
import numpy as np

gris = data.camera()
x=gris.reshape(-1,1)
plt.figure(0)
plt.imshow(gris,cmap='gray')
plt.show

fil,col=gris.shape

X=gris
#x1=pixel(0,0)
car=1
n=fil*col
cla=4
pen=2
#cen = np.array([[39.0], [201.0], [125.0]])
cen=np.random.rand(cla,car)*255

dist = np.zeros([cla,n])

for epocas in range(1):
        
    for i in range(cla):
        for k in range(n):
            suma0 = 0
            for j in range(car):
                suma0 = (x[k, j] - cen[i, j])**2 + suma0
            dist[i, k] = suma0**(1/2)

    mu = np.zeros([cla, n])
    for i in range(cla):
        for k in range(n):
            suma1 = 1e-10  # Para evitar indeterminaciones
            for j in range(cla):
                suma1 = ((dist[i, k] / (dist[j, k] + 1e-10))**(2/(pen-1))) + suma1
            mu[i, k] = 1 / suma1

    for i in range(cla):
        for j in range(car):
            suma2 = 1e-6
            suma3 = 1e-6
            for k in range(n):
                suma2 = (mu[i, k]**pen) * x[k, j] + suma2
                suma3 = (mu[i, k]**pen) + suma3
            cen[i, j] = suma2 / suma3
    '''
    suma5 = 0
    for k in range(n):
        suma4 = 0
        for i in range(cla):
            suma4 = (mu[i, k]**2) + suma4
        suma5 = suma4 + suma5

    Pc = (1/n) * suma5 #Partition Coefficient

    print(Pc) 
    '''

    suma8=0
    for i in range(cla-1):
        suma7=0
        for j in range(i+1,cla,1):
            suma6=0
            for k in range(n):
                suma6=(mu[i,k]-mu[j,k])**2+suma6
            suma7=(1/n)*suma6+suma7
        suma8=suma7+suma8
    aps=(1/cla-1)*suma8 #average partition separability

    print(aps)