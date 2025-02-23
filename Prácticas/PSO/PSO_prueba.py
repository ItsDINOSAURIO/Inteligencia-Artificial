import numpy as np
import matplotlib.pyplot as plt
#--------------
# Ecuación Fitness a la que se provee solución
def purelin(n):
    return n
def logsig(n):
#    return 1 / (1 + np.exp(-n))
   return (2 / (1 + np.exp(-2*n)))-1

def neurona(x,pattern):
    n1 = logsig(pattern*x[0]+x[2])
    n2 = logsig(pattern*x[1]+x[3])
    n3 = purelin(n1*x[4] + n2*x[5] + x[6])
    error = (1+np.sin((np.pi/4)*pattern))-n3
    # print(error)
    return error,n3

def fitness(pattern,particula):
    # error=0
    # for i in range(len(pattern)):
    #     x=neurona(particula,pattern[i])
    #     error=x+error
    # dato=error/len(pattern)
    # return(dato)
    error_cuadrado = 0
    for i in range(len(pattern)):
        error,_ = neurona(particula, pattern[i])
        error_cuadrado += error ** 2  # Elevar al cuadrado el error y acumular
    
    mse = error_cuadrado / len(pattern)
    return mse

#---------------
particula={ 'posicion': None,
            'velocidad':None,
            'costo':None,
            'best_posicion':None,
            'best_costo':np.inf}

_global={'posicion': None,
         'costo':np.inf}
#-----------------

num_variables=7  #caracteristica 1 y caracteristica 2
pattern = np.arange(0,8,0.1)
var_min,var_max=-3,3
max_iterar=650
# poblacion=170
poblacion=200
c1,c2=1.5,1.5
w=1    #coeficinete de inercia
disminu=0.5
error=[]


individuo=[]
for i in range(0,poblacion):
    individuo.append(particula.copy())
    individuo[i]['posicion']=np.random.uniform(var_min,var_max,num_variables)
    individuo[i]['velocidad']=np.zeros(num_variables)
    individuo[i]['costo']=fitness(pattern,individuo[i]['posicion'])#Eggholder(individuo[i]['posicion'])
    individuo[i]['best_posicion']=individuo[i]['posicion'].copy()
    individuo[i]['best_costo']=individuo[i]['costo'].copy()
    if individuo[i]['best_costo']<_global['costo']:
        _global['posicion']=individuo[i]['best_posicion'].copy()
        _global['costo']=individuo[i]['best_costo'].copy()

for iterar in range(0,max_iterar):
    for i in range(0,poblacion):
        individuo[i]['velocidad']= w*individuo[i]['velocidad'] + np.random.rand(num_variables)*c1*(individuo[i]['best_posicion']-individuo[i]['posicion']) + np.random.rand(num_variables)*c2*(_global['posicion']-individuo[i]['posicion'])
        individuo[i]['posicion']=individuo[i]['posicion']+individuo[i]['velocidad']
        individuo[i]['posicion']=np.maximum(individuo[i]['posicion'],var_min)
        individuo[i]['posicion']=np.minimum(individuo[i]['posicion'],var_max)
        individuo[i]['costo']=fitness(pattern,individuo[i]['posicion'])

        if individuo[i]['costo'] < individuo[i]['best_costo']:
            individuo[i]['best_posicion'] = individuo[i]['posicion'].copy()
            individuo[i]['best_costo']= individuo[i]['costo'].copy()
            if individuo[i]['best_costo'] < _global['costo']:
                _global['posicion']=individuo[i]['best_posicion'].copy()
                _global['costo']=individuo[i]['best_costo'].copy()
    w*=disminu
    print('Iteracion {}: error más bajo={} y parámetros={}'.format(iterar+1,_global['costo'],_global['posicion']))
    error.append(_global['costo'])

plt.figure()
grafica_costo=np.array(error)
plt.semilogy(abs(grafica_costo))
plt.xlabel('Iteraciones')
plt.ylabel('Costo')

resultado = [] 
target = []      
plt.figure()

for i in range(len(pattern)):
    r1,r2=neurona(_global['posicion'],pattern[i])
    resultado.append(r2)
    target.append(1+np.sin((np.pi/4)*pattern[i]))
plt.plot(pattern,resultado)
plt.plot(pattern,target)
plt.show()