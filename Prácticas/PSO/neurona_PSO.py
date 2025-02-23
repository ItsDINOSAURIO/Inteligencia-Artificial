import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm

num_variables = 7 
c1 = 1.5 #coeficiente de aceleración
c2 = 1.5 #coeficiente poblacional 
w = 1 #coeficiente de inercia
max_iter = 1000
poblacion = 250
var_min,var_max = -3,3
pattern = np.arange(-2,2,0.1)
disminu = 0.5
error = [] 

def purelin(n):
    a = 1 * n
    return a
def logsig(n):
    f = 1 / (1 + np.exp(-n))
    return f
def neurona(x,pattern):
    n1 = logsig(pattern*x[0]+x[2])
    n2 = logsig(pattern*x[1]+x[3])
    n3 = purelin(n1*x[4] + n2*x[5] + x[6])
    #error = (1+np.sin((np.pi/4)*pattern))-n3
    error = np.mean(((1+np.sin((np.pi/4)*pattern))-n3)**2)
       
    return error,n3
resultado = []
def fitness(pattern, particula):
    errores,_ = neurona(particula, pattern)
    mse = np.mean(errores**2)  # Error cuadrático medio
    return mse
# def fitness(pattern,particula):#fitness
#     resultado = []
#     error = 0
#     for i in range(len(pattern)):
#         x,_ = neurona(particula,pattern[i])
#         error = x + error
#     dato = error/len(pattern)
#     resultado.append(dato)
#     return dato 

particula = {'posicion': None,
             'velocidad': None,
             'costo': None,
             'best_posicion' : None,
             'best_costo' : np.inf
             }
_global = {'posicion': None,
           'costo':np.inf}

individuo = []

for i in range(0,poblacion):
    individuo.append(particula.copy())
    individuo[i]['posicion'] = np.random.uniform(var_min,var_max,num_variables)
    individuo[i]['velocidad'] = np.zeros(num_variables)
    individuo[i]['costo'] = fitness(pattern,individuo[i]['posicion'])# Eggcrate(individuo[i]['posicion'])
    individuo[i]['best_posicion'] = individuo[i]['posicion'].copy() #guarda el valor apuntando a la dirección 
    individuo[i]['best_costo'] = individuo[i]['costo'].copy()
    
    if individuo [i]['best_costo'] < _global['costo']:
        _global['posicion'] = individuo[i]['best_posicion'].copy()
        _global['costo'] = individuo[i]['best_costo'].copy()

for iter in range(0,max_iter):
    for i in range(0,poblacion):
        #x(t+1) = x(t)+v(t+1)
        individuo[i]['velocidad'] = w*individuo[i]['velocidad']\
                                    +np.random.rand(num_variables)*c1*(individuo[i]['best_posicion']-individuo[i]['posicion'])\
                                    +np.random.rand(num_variables)*c2*(_global['posicion']-individuo[i]['posicion'])
        individuo[i]['posicion'] = individuo[i]['posicion'] + individuo[i]['velocidad']
        individuo[i]['posicion'] = np.maximum(individuo[i]['posicion'],var_min)
        individuo[i]['posicion'] = np.minimum(individuo[i]['posicion'],var_max)#acota la región entre las condiciones de frontera
        
        individuo[i]['costo'] = fitness(pattern,individuo[i]['posicion'])#Eggcrate(individuo[i]['posicion'])
        
        if individuo[i]['costo'] < individuo[i]['best_costo']:
            individuo[i]['best_posicion'] = individuo[i]['posicion'].copy()
            individuo[i]['best_costo'] = individuo[i]['costo'].copy()
            if individuo[i]['best_costo'] < _global['costo']:
                _global['posicion'] = individuo[i]['best_posicion'].copy()
                _global['costo'] = individuo[i]['best_costo'].copy()
        
    w*= disminu
    print('Iteración{}: mejor costo = {} y posicion = {}'.format(iter,_global['costo'],_global['posicion']))
    error.append(_global['costo'])
  
plt.close('all')
plt.figure()
grafica_costo = np.array(error)
plt.semilogy(abs(grafica_costo))
plt.xlabel('Iteraciones')
plt.ylabel('Costo')

resultado = [] 
resultado2 = [] 

target = []      
plt.figure()

for i in range(len(pattern)):
    r1,r2 = neurona(_global['posicion'],pattern[i])  
    resultado.append(r1)
    resultado2.append(r2)
    target.append(1+np.sin((np.pi/4)*pattern[i]))

#fitness(pattern,_global['posicion'])
plt.plot(pattern,resultado)
plt.plot(pattern,target)
plt.plot(pattern,resultado2,'--')

plt.show()