import numpy as np
import matplotlib.pyplot as plt

def hardlim(x):
    if x>0:
        y=1
    else: 
        y=0
    return y

p0=0
w0=1
p=0
w=0
b=-0.5
alpha=0.1
gamma=0.1
plt.close('all')
plt.ion() #i:interaction, on:aprender la interacción; una vez termine sería ioff
for epocas in range (150):
    n=(w0*p0)+(w*p)+(1*b)
    output=hardlim(n)
    # w=w+(alpha*output*p)#sin decaemiento
    # w=((1-gamma)*w)+(alpha*output*p)#con decaemiento
    w=((1-gamma*output)*w)+(alpha*output*p)#con memoria, pues el aprendizaje se ve anclado al una salida=0, por lo que se tiene una neurona que recuerda 
    #w=w+(alpha*output*p)-(gamma*w)#olvido 
    

    if epocas>10:
        p0=1
        p=1
        if epocas>100:
            p0=0
            p=1
    # elif epocas>30:
    #     p0=0
    plt.plot(epocas,w,'.')
    plt.pause(0.25)

plt.ioff()
plt.show()