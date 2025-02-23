# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm

# #Función Fitness
# def eggcrate(x):
#     out=np.sum(x**2+25*np.sin(x)**2,axis=1)
#     return out

# def purelin(n):
#     a = n
#     return a
# def logsig(n):
#     f = 1 / (1 + np.exp(-n))
#     return f
# def neurona(x,pattern):
#     n1 = logsig(pattern*x[0]+x[2])
#     n2 = logsig(pattern*x[1]+x[3])
#     n3 = purelin(n1*x[4] + n2*x[5] + x[6])
#     # error = (1+np.sin((np.pi/4)*pattern))-n3
#     error=np.mean(((1+np.sin((np.pi/4)*pattern))-n3)**2)
#     return error,n3

# def fitness(pattern, particulas):  # Fitness ahora recibe todas las partículas
#     errores = []
#     for particula in particulas:
#         error = 0
#         for i in range(len(pattern)):
#             err,_ = neurona(particula, pattern[i])
#         dato = np.mean(err**2)
#         errores.append(dato)
#     return np.array(errores)

# # def neurona(x,pattern):
# #     n1 = logsig(pattern*x[0]+x[2])
# #     n2 = logsig(pattern*x[1]+x[3])
# #     n3 = purelin(n1*x[4] + n2*x[5] + x[6])
# #     #error = (1+np.sin((np.pi/4)*pattern))-n3
# #     error = np.mean(((1+np.sin((np.pi/4)*pattern))-n3)**2)
       
# #     return error,n3
# # resultado = []
# # def fitness(pattern, particula):
# #     errores = []
# #     for p in pattern:  # Iterar sobre cada valor de pattern
# #         error, _ = neurona(particula, p)
# #         errores.append(error)
# #     mse = np.mean(errores)  # Promediar los errores
# #     return mse

# #Clase dedicada al Algoritmo
# class GWO:
#     #Función para inicializar el sistema 
#     def __init__(self,funcion,n_dim,n_pop,max_iter,var_min,var_max):
#         self.funcion=funcion
#         self.n_dim=n_dim
#         self.n_pop=n_pop
#         self.max_iter=max_iter
#         self.var_min=var_min
#         self.var_max=var_max
#         self.positions=np.random.uniform(self.var_min,self.var_max,(self.n_pop,self.n_dim))
#         self.costs=self.funcion(pattern,self.positions)
#         # self.costs = np.array([self.funcion(pattern, particula) for particula in self.positions])
#         sort_indices=np.argsort(self.costs)
#         self.alpha_pos=self.positions[sort_indices[0].copy()]
#         self.alpha_score=self.costs[sort_indices[0]]
#         self.beta_pos=self.positions[sort_indices[1].copy()]
#         self.beta_score=self.costs[sort_indices[1]]
#         self.delta_pos=self.positions[sort_indices[2].copy()]
#         self.delta_score=self.costs[sort_indices[2]]
#         self.converge_curve=np.zeros(self.max_iter)
    
#     #Ciclo de optimización
#     def optimize(self):
#         for t in range(self.max_iter):
#             a=2-t*(2/self.max_iter)#Decrese de 2 a 0
#             r1=np.random.rand(self.n_pop,self.n_dim)
#             r2=np.random.rand(self.n_pop,self.n_dim)
#             A1=2*a*r1-a
#             C1=2*r2
#             D_alpha=np.abs(C1*self.alpha_pos-self.positions)
#             x1=self.alpha_pos-A1*D_alpha
#             r1=np.random.rand(self.n_pop,self.n_dim)
#             r2=np.random.rand(self.n_pop,self.n_dim)
#             A1=2*a*r1-a
#             C1=2*r2
#             D_beta=np.abs(C1*self.beta_pos-self.positions)
#             x2=self.beta_pos-A1*D_beta
#             r1=np.random.rand(self.n_pop,self.n_dim)
#             r2=np.random.rand(self.n_pop,self.n_dim)
#             A1=2*a*r1-a
#             C1=2*r2
#             D_delta=np.abs(C1*self.delta_pos-self.positions)
#             x3=self.delta_pos-A1*D_delta

#             self.positions=(x1+x2+x3)/3.0
#             self.positions=np.clip(self.positions,self.var_min,self.var_max)
#             self.costs=self.funcion(pattern,self.positions)
#             for i in range(self.n_pop):
#                 if self.costs[i]<self.alpha_score:
#                     self.alpha_score=self.costs[i]
#                     self.alpha_pos=self.positions[i].copy()                
#                 elif self.costs[i]<self.beta_score:
#                     self.beta_score=self.costs[i]
#                     self.beta_pos=self.positions[i].copy()                
#                 elif self.costs[i]<self.delta_score:
#                     self.delta_score=self.costs[i]
#                     self.delta_pos=self.positions[i].copy()
#                 self.converge_curve[t]=self.alpha_score
#             errorg.append(self.alpha_score)
#             if(t+1)%10==0 or t==0:
#                 print(f"Iteracón{t+1}/{self.max_iter}, Mejor Costo={self.alpha_score}, Mejor posicion= {self.alpha_pos} ")
#         print("Optimización Completada")

# n_dim = 7
# var_min,var_max=-3,3
# n_pop=250
# max_iter=900
# pattern = np.arange(-2,2,0.1)
# errorg=[]

# lobos=GWO(funcion=fitness,n_dim=n_dim,n_pop=n_pop,max_iter=max_iter,var_min=var_min,var_max=var_max)
# lobos.optimize()

# plt.figure()
# grafica_costo = np.array(errorg)
# plt.semilogy(abs(grafica_costo))

# plt.figure()
# resultado=[]
# target=[]
# for i in range(len(pattern)):
#     _,r1=neurona(lobos.alpha_pos,pattern[i])
#     resultado.append(r1)
#     target.append(1+np.sin((np.pi/4)*pattern[i]))
# plt.plot(pattern,resultado,'c--')
# plt.plot(pattern,target,'r')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

def eggcrate(x):
    out = np.sum(x**2 + 25*np.sin(x)**2, axis=1)
    return out

def purelin(n):
    return n

def logsig(n):
    return 1 / (1 + np.exp(-n))

def neurona(x, pattern):
    n1 = logsig(pattern*x[0] + x[2])
    n2 = logsig(pattern*x[1] + x[3])
    n3 = purelin(n1*x[4] + n2*x[5] + x[6])
    error = np.mean(((1 + np.sin((np.pi/4)*pattern)) - n3)**2)
    return error, n3

def fitness(pattern, particulas):
    errores = []
    for particula in particulas:
        errors = []
        for p in pattern:
            err, _ = neurona(particula, p)
            errors.append(err)
        errores.append(np.mean(errors))
    return np.array(errores)

class GWO:
    def __init__(self, funcion, n_dim, n_pop, max_iter, var_min, var_max, pattern):
        self.funcion = funcion
        self.n_dim = n_dim
        self.n_pop = n_pop
        self.max_iter = max_iter
        self.var_min = var_min
        self.var_max = var_max
        self.pattern = pattern
        
        # Initialize population
        self.positions = np.random.uniform(self.var_min, self.var_max, (self.n_pop, self.n_dim))
        self.costs = self.funcion(self.pattern, self.positions)
        
        # Sort and initialize best wolves
        sort_indices = np.argsort(self.costs)
        self.alpha_pos = self.positions[sort_indices[0]].copy()
        self.alpha_score = self.costs[sort_indices[0]]
        self.beta_pos = self.positions[sort_indices[1]].copy()
        self.beta_score = self.costs[sort_indices[1]]
        self.delta_pos = self.positions[sort_indices[2]].copy()
        self.delta_score = self.costs[sort_indices[2]]
        
        # Track convergence
        self.converge_curve = np.zeros(self.max_iter)
        self.errorg = []
    
    def optimize(self):
        for t in range(self.max_iter):
            a = 2 - t * (2 / self.max_iter)  # Decreases from 2 to 0
            
            for i in range(self.n_pop):
                r1 = np.random.rand(self.n_dim)
                r2 = np.random.rand(self.n_dim)
                
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                
                # Calculate distances and new positions for alpha, beta, delta wolves
                D_alpha = np.abs(C1 * self.alpha_pos - self.positions[i])
                D_beta = np.abs(C1 * self.beta_pos - self.positions[i])
                D_delta = np.abs(C1 * self.delta_pos - self.positions[i])
                
                x1 = self.alpha_pos - A1 * D_alpha
                x2 = self.beta_pos - A1 * D_beta
                x3 = self.delta_pos - A1 * D_delta
                
                self.positions[i] = (x1 + x2 + x3) / 3.0
            
            # Clip positions to bounds
            self.positions = np.clip(self.positions, self.var_min, self.var_max)
            
            # Recalculate costs
            self.costs = self.funcion(self.pattern, self.positions)
            
            # Update best wolves
            for i in range(self.n_pop):
                if self.costs[i] < self.alpha_score:
                    self.delta_score = self.beta_score
                    self.delta_pos = self.beta_pos.copy()
                    self.beta_score = self.alpha_score
                    self.beta_pos = self.alpha_pos.copy()
                    self.alpha_score = self.costs[i]
                    self.alpha_pos = self.positions[i].copy()
                elif self.costs[i] < self.beta_score:
                    self.delta_score = self.beta_score
                    self.delta_pos = self.beta_pos.copy()
                    self.beta_score = self.costs[i]
                    self.beta_pos = self.positions[i].copy()
                elif self.costs[i] < self.delta_score:
                    self.delta_score = self.costs[i]
                    self.delta_pos = self.positions[i].copy()
            
            # Track best score
            self.converge_curve[t] = self.alpha_score
            self.errorg.append(self.alpha_score)
            
            # Print progress
            if (t + 1) % 10 == 0 or t == 0:
                print(f"Iteration {t+1}/{self.max_iter}, Best Cost={self.alpha_score}, Mejor Posicion={self.alpha_pos}")
        
        print("Optimization Completed")
        return self.alpha_pos

def main():
    # Parameters
    n_dim = 7
    var_min, var_max = -3, 3
    n_pop = 15
    max_iter = 100
    pattern = np.arange(-2, 2, 0.1)

    # Run optimization
    lobos = GWO(funcion=fitness, n_dim=n_dim, n_pop=n_pop, 
                max_iter=max_iter, var_min=var_min, var_max=var_max, 
                pattern=pattern)
    best_solution = lobos.optimize()

    # Plotting
    plt.figure()
    grafica_costo = np.array(lobos.errorg)
    plt.semilogy(abs(grafica_costo))
    plt.title('Convergence Curve')
    plt.xlabel('Iterations')
    plt.ylabel('Best Cost')

    plt.figure()
    resultado = []
    target = []
    for p in pattern:
        _, r1 = neurona(best_solution, p)
        resultado.append(r1)
        target.append(1 + np.sin((np.pi/4)*p))
    
    plt.plot(pattern, resultado, 'c--', label='Predicted')
    plt.plot(pattern, target, 'r', label='Target')
    plt.title('Neural Network Output vs Target')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()