import numpy as np
patrones=[np.array([-0.1961, 0.9806]),
          np.array([ 0.1961, 0.9806]),
          np.array([ 0.9806, 0.1961]),
          np.array([ 0.9806,-0.1961]),
          np.array([-0.5812,-0.8137]),
          np.array([-0.8137,-0.5812])]

pesos=[np.array([-0.1961, 0.9806]),
       np.array([ 0.1961, 0.9806]),
       np.array([ 0.9806, 0.1961]),
       np.array([ 0.9806,-0.1961]),
       np.array([-0.5812,-0.8137]),
       np.array([-0.8137,-0.5812])]

W1=np.array(pesos) #6x2
R=len(patrones[0])
b1=R
epsilon=0.1 #Cantidad de información "falsa" que se le da al resto de neuronas
iteracion=10 #el # de iteraciones para la capa recursiva
for idx , patron in enumerate(patrones): #patron: 2x1
    a1=np.dot(W1,patron)+b1
    a2=a1.copy()
    #Ecuación 16.7 inhibicion lateral
    for _ in range(iteracion): #el _ significa omitir, al no ser dependiente de una variable en específico, solo se iterará el bloque de código
        new_a2=np.zeros_like(a2)
        for i in range(len(a2)):
            ini=epsilon*(np.sum(a2)-a2[i]) #inhibicion
            new_a2[i]=max(0,a2[i]-ini) #poslin: si valor es menor que 0, entonces la salida será 0, sino será el mismo valor
        a2=new_a2
    winner_ind=np.argmax(a2)
    print(f"Patron de entrada {idx+1} : {patron}")
    print(f"Neurona ganadora {winner_ind+1} : {patron}")
    print(f"Salida final: {a2}\n")
    