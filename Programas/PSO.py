import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
plt.close('all')

X=np.arange(-5.5,5.5,0.1)
Y=np.arange(-5.5,5.5,0.1)
X,Y=np.meshgrid(X,Y)

#Función Benchmark Eggcrate

Z=X**2 + Y**2 +25*(np.sin(X)**2+np.sin(Y)**2)
#EL mejor de todos los Z, es el conocimiento global g(t) para todas las x, en la actualización, todas las partículas se dirigen hacia el mejor global, hasta que converge

fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.plot_surface(X,Y,Z,cmap=cm.coolwarm)
#Etiquetas y limites
ax.set_xlabel('X')
ax.set_xlim(-5.5,5.5)
ax.set_ylabel('Y')
ax.set_ylim(-5.5,5.5)
ax.set_zlabel('Z')
ax.set_zlim(0,150)

plt.show()