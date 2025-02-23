import numpy as np
import matplotlib.pyplot as plt
#--------------
# Ecuación Fitness a la que se provee solución
def Eggcrate(x): #equis es una particula
    return x[0]**2+x[1]**2+25*(np.sin(x[0])**2+np.sin(x[1])**2)

def Eggholder(x): 
    return -(x[1]+47)*np.sin(np.sqrt(np.abs(x[1]+(x[0]/2)+47)))-x[0]*np.sin(np.sqrt(np.abs(x[0]-(x[1]+47))))
def purelin(n):
    return n
def logsig(n):
   return 1 / (1 + np.exp(-n))

def neurona(x,pattern):
    n1 = logsig(pattern*x[0]+x[2])
    n2 = logsig(pattern*x[1]+x[3])
    n3 = purelin(n1*x[4] + n2*x[5] + x[6])
    error = (1+np.sin((np.pi/4)*pattern))-n3
    # print(error)
    return error

def fitness(pattern,particula):
    error=0
    for i in range(len(pattern)):
        x=neurona(particula,pattern[i])
        error=x+error
    dato=error/len(pattern)
    return(dato)

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
pattern = np.arange(-2,10,0.1)
# var_min=-5.5
# var_max=5.5
# var_min=-512
# var_max=512
var_min,var_max=-3,3
max_iterar=300
poblacion=50
# c1=2   #coeficiente de aceleracion (cognitivo) <----PERSONAL
# c2=2   #coeficiente de aceleracion (poblacional) <-----GRUPAL
c1,c2=1.5,1.5
w=1    #coeficinete de inercia
disminu=0.9
error=[]

# X=np.arange(-5.5,5.5,0.1)
# Y=np.arange(-5.5,5.5,0.1)
# X=np.arange(-512,512,1)
# Y=np.arange(-512,512,1)
# X,Y=np.meshgrid(X,Y)

#Función Benchmark Eggcrate
# Z=X**2 + Y**2 +25*(np.sin(X)**2+np.sin(Y)**2)
# Z=-(Y+47)*np.sin(np.sqrt(np.abs(Y+(X/2)+47)))-X*np.sin(np.sqrt(np.abs(X-(Y+47))))
#--------------

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
        individuo[i]['costo']=fitness(pattern,individuo[i]['posicion'])#Eggholder(individuo[i]['posicion'])

        if individuo[i]['costo'] < individuo[i]['best_costo']:
            individuo[i]['best_posicion'] = individuo[i]['posicion'].copy()
            individuo[i]['best_costo']= individuo[i]['costo'].copy()
            if individuo[i]['best_costo'] < _global['costo']:
                _global['posicion']=individuo[i]['best_posicion'].copy()
                _global['costo']=individuo[i]['best_costo'].copy()
    w*=disminu
    print('Iteracion {}:mejor costo={} y posicion={}'.format(iterar+1,_global['costo'],_global['posicion']))
    # plt.gcf().clear()
    # plt.contour(X,Y,Z,cmap='gray')
    # x_pso=[]
    # y_pso=[]
    # for m in range(poblacion):
    #     x_pso.append(individuo[m]['posicion'][0])
    #     y_pso.append(individuo[m]['posicion'][1])
    # plt.scatter(x_pso,y_pso,c='r')
    # plt.pause(0.5)
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
    resultado.append(neurona(_global['posicion'],pattern[i]))
    target.append(1+np.sin((np.pi/4)*pattern[i]))
plt.plot(pattern,resultado)
plt.plot(pattern,target)
plt.show()