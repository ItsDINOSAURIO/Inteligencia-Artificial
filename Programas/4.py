import numpy as np
import matplotlib.pyplot as plt
alpha=0.1 #Razón de aprendizaje
epsilon=0.1 #inhibición
patrones=np.array([[-0.1961, 0.9806],
          [ 0.1961, 0.9806],
          [ 0.9806, 0.1961],
          [ 0.9806,-0.1961],
          [-0.5812,-0.8137],
          [-0.8137,-0.5812]])

pesos1=np.array([[-0.17071, 0.17071],
                 [-0.17071, 0.17071],
                 [-0.17071, 0.17071]]) #En el caso de tener 2 neuronas iguales, gana la primera que se evalúa puesto que el programa está planteado de forma secuencial

pesos2=np.array([[1,-epsilon,-epsilon],
                [-epsilon,1,-epsilon],
                [-epsilon,-epsilon,1]])

bias=np.zeros((len(pesos1),1))

plt.close('all')
plt.ion()
fig,ax=plt.subplots()
for i in range (patrones.shape[0]):
    ax.arrow(0,0,patrones[i,0],patrones[i,1],head_width=0.05,head_length=0.1,color='b')

for i in range(pesos1.shape[0]):
    ax.arrow(0,0,pesos1[i,0],pesos1[i,1],head_width=0.05,head_length=0.1,color='r')

ax.plot(0,0,'ok')
ax.set_aspect('equal')
ax.set_xlim([-1.5,1.5])
ax.set_ylim([-1.5,1.5])
ax.grid(True,which='major')#Evita que se mueva el grid a pesar de ser interactivo


for epocas in range(100):
    for i in range (patrones.shape[0]):
        a1=pesos1.dot(patrones[i,:].T)+bias.flatten()
        #a2=np.where(pesos2.dot(a1)<=0,0,pesos2.dot(a1)) #Se busca en pesos2,y se hace producto . por a1, donde sea <= a 0, se le asignará 0, donde no, se pondrá el valor de la multiplicación
        ganador=np.argmax(a1)
        #Ganador Toma todo (COMPET) a diferencia que en Self-organizing map (SOM) activa además más neuronas que se encuentren a cierto radio de vecindad
        #PAra el self organizing map se calcula la distancia entre w y p
        for j in range(pesos1.shape[0]):
            if j==ganador:
                pesos1[j,:]+=alpha*(patrones[i,:]-pesos1[j,:])
        bias[ganador]-=0.2*(1+bias[ganador])
        # for _ in range(6):
        #     a2=np.where(pesos2.dot(a2)<=0,0,pesos2.dot(a2))
        # for j in range (pesos1.shape[0]):
        #     pesos1[j,:]+=alpha*a2[j]*(patrones[i,:]-pesos1[j,:]) #Regla de aprendizaje de kohonnen
        # ganador=np.argmax(a1)
        # bias=bias*0.9
        # bias[ganador]-=0.1 #Variación para la impedancia del bias, así acelerando la propagación de patrones

        ax.cla() #Clear axes

        ax.plot(0,0,'ok')
        ax.set_aspect('equal')
        ax.set_xlim([-1.5,1.5])
        ax.set_ylim([-1.5,1.5])
        ax.grid(True,which='major')
        for i in range (patrones.shape[0]):
            ax.arrow(0,0,patrones[i,0],patrones[i,1],head_width=0.05,head_length=0.1,color='b')

        for i in range(pesos1.shape[0]):
            ax.arrow(0,0,pesos1[i,0],pesos1[i,1],head_width=0.05,head_length=0.1,color='r')

        plt.pause(0.1)


plt.show()