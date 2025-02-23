# import tkinter as tk
# import numpy as np
# import random
# from collections import defaultdict
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class metro:
#     def __init__(self):

#         self.coords = {}
#         self.nodos = {}
#         self.conexiones = {}
#         self.estaciones = {}
#         self.feromonas = {}
#         self.nodo_in = 0 
#         self.nodo_out = 0
#         self.lista_inicio = []
#         self.lista_fin = []
#         self.nodo_inhibido = set()  # Nodos que se desactivarán

        
#         self.root = tk.Tk()
#         self.root.title("Metro de la CDMX por ACO")
#         self.root.configure(bg = "black" )

        
#         #crea el frame principal
#         self.main_frame = tk.Frame(self.root,bg = "black")
#         self.main_frame.pack(fill = tk.BOTH, expand = True)
        
#         # crea canvas para dibujar mapa
#         self.canvas = tk.Canvas(self.main_frame, bg = "black", width = 1200 , height = 800, highlightthickness = 0)
#         self.canvas.grid(row = 0, column = 0, rowspan = 2, sticky = "nsew")
        

#     def mapa(self):
#         self.nodos={
#             0:(19.50467,-99.20010),1:(19.48949,-99.14473),2:(19.48533,-99.12547),
#             3:(19.48514,-99.10437),4:(19.46991,-99.13657),5:(19.45952,-99.18752),
#             6:(19.45823,-99.11391),7:(19.44498,-99.08688),8:(19.44493,-99.14525),
#             9:(19.44393,-99.13862),10:(19.43965,-99.11818),
#             11:(19.43751,-99.14715),   
#             12:(19.43639,-99.14161),13:(19.43009,-99.11432),14:(19.42956,-99.12097),
#             15:(19.42435,-99.13285),16:(19.42725,-99.14901), 17:(19.42721,-99.14210),
#             18:(19.41510,-99.07436),19:(19.40198,-99.18732),20:(19.40659,-99.15520),
#             21:(19.40918,-99.13563),22:(19.41097,-99.12176),23:(19.40417,-99.12067),
#             24:(19.37609,-99.18778),25:(19.37068,-99.16505),26:(19.36113,-99.14308),
#             27:(19.35626,-99.10118)
#         }
#         self.coords = {}
#         for nodo, (lat, lon) in self.nodos.items():
#             x = 111 * (lat - list(self.nodos.values())[0][0])
#             y = 111 * np.cos(np.radians((lat + list(self.nodos.values())[0][0]) / 2)) * (lon - list(self.nodos.values())[0][1])
#             self.coords[nodo] = (y, x)
        
#         self.estaciones={    
#             0: "Rosario",1: "Instituto del Petróleo", 2: "Deportivo 18 de Marzo",
#             3: "Martín Carrera", 4: "La Raza",5: "Tacuba",
#             6: "Consulado", 7: "Oceanía", 8: "Guerrero",
#             9: "Garibaldí/Lagunilla",10: "Morelos",11: "Hidalgo",
#             12: "Bellas Artes",13: "San Lázaro",14: "Candelaria",
#             15: "Pino Suárez",16: "Balderas",17: "Salto del Agua",
#             18: "Pantitlán",19: "Tacubaya", 20: "Centro Médico",
#             21: "Chabacano",22: "Jamaica",23: "Santa Anita",
#             24: "Mixcoac",25: "Zapata",26: "Ermita",27: "Atlalilco"}

        
#         self.conexiones={}
#         for (nodo1,nodo2) in [
#             (0,1),(0,5),(1,2),(1,4),(2,3),(2,4),(3,6),(4,6),(4,8),(5,11),(5,19),(6,7),(6,10),
#             (7,13),(7,18),(8,9),(8,11),(9,10),(9,12),(10,13),(10,14),(11,12),(11,16),(12,15),
#             (12,17),(13,14),(13,18),(14,15),(14,22),(15,17),(15,21),(16,17),(16,19),(16,20),
#             (17,21),(18,22),(19,20),(19,24),(20,21),(20,25),(21,22),(21,26),(23,21),(22,23),(23,27),
#             (24,25),(25,26),(26,27)
#             ]:
#             dist=self.calcular_distancia(nodo1,nodo2)
#             self.conexiones[(min(nodo1,nodo2),max(nodo1,nodo2))]=dist
        
#         self.coords_norm = self.coords.copy()
#         self.normalizar_coordenadas(self.coords_norm, 700, 700)
#         self.feromonas={arista:0.1 for arista in self.conexiones}
        
        
#         self.canvas.create_text(700,80, text = "Metro de la CDMX", fill = "white", font=("Arial", 20))
    
        
#         # Dibujar conexiones (excluyendo nodos inhibidos)
#         for (nodo1, nodo2) in self.conexiones:
#             if nodo1 in self.nodo_inhibido or nodo2 in self.nodo_inhibido:
#                 continue
#             x1, y1 = self.coords_norm[nodo1]
#             x2, y2 = self.coords_norm[nodo2]
#             self.canvas.create_line(x1, y1, x2, y2, fill="cyan", dash=(10, 4), width=2)

        
        
#         # Dibujar estaciones (resaltar nodos inhibidos)
#         for nodo, (x, y) in self.coords_norm.items():
#             color = "red" if nodo in self.nodo_inhibido else "purple"
#             self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="white")
#             self.canvas.create_text(x+10, y-10, text=self.estaciones[nodo], fill="white", font=("Arial", 8))

        
#         self.label1 = tk.Label(self.main_frame,text = "ORIGEN",font=("Arial", 10), bg="black", fg="white" )
#         self.label1.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#         self.label2 = tk.Label(self.main_frame,text = "DESTINO",font=("Arial", 10), bg="black", fg="white" )
        
#         self.lista_inicio = list(self.estaciones.values())  
#         self.lista1 = tk.Listbox(self.main_frame, selectmode = tk.SINGLE, bg = "black", fg = "white", highlightbackground ="gray", highlightthickness = 0)
#         # Llena la lista 1 con las estaciones disponibles
#         self.lista1.delete(0, tk.END)  
#         for estacion in self.lista_inicio:
#             self.lista1.insert(tk.END, estacion) 

        
        
#         self.lista1.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
#         self.lista1.bind("<<ListboxSelect>>",self.lista1_evento)
        
#         self.lista2 = tk.Listbox(self.main_frame, selectmode = tk.SINGLE, bg = "black", fg = "white", highlightbackground ="gray", highlightcolor="white", highlightthickness=0)
#         self.lista2.bind("<<ListboxSelect>>",self.lista2_evento)
        

#         self.main_frame.columnconfigure(0, weight=3) 
#         self.main_frame.columnconfigure(1, weight=1)  
#         self.main_frame.rowconfigure(0, weight=1)
#         self.main_frame.rowconfigure(1, weight=7)
#         self.main_frame.rowconfigure(2, weight=1)
        
#         button = tk.Button(self.main_frame, text="Cerrar", command=self.root.quit)
#         button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
#         # button.pack(pady=10)

#         btn_inhibir = tk.Button(self.main_frame, text="Inhibir Estacion", command=self.ventana_inhibir, bg="red", fg="white")
#         btn_inhibir.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        
#         btn_reset = tk.Button(self.main_frame, text="Reset", command=self.reset)
#         btn_reset.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        
#         self.canvas.update()
#         self.root.mainloop()
        
      

        
#     def calcular_distancia(self,nodo1,nodo2):
#         x1,y1=self.coords[nodo1]
#         x2,y2=self.coords[nodo2]
#         distancia=np.sqrt((x2-x1)**2+(y2-y1)**2)
#         return distancia
#     def lista1_evento(self, event):
#         if self.lista2.winfo_ismapped():
#             return
#         seleccion = self.lista1.curselection()
#         if seleccion:
#             estacion = self.lista1.get(seleccion)
#             for nodo, nombre in self.estaciones.items():
#                 if nombre == estacion:
#                     self.nodo_in = nodo
#                     break
    
#             print(f"Estación seleccionada como inicio: {estacion} ({self.nodo_in})")
            
#             self.lista_fin = self.lista_inicio[:]
#             self.lista_fin.remove(estacion)
#             for elemento in self.lista_fin:
#                 self.lista2.insert(tk.END, elemento)
#             self.label2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")    
#             self.lista2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


#     def lista2_evento(self, event):
#         seleccion = self.lista2.curselection()
#         if seleccion:
#             # Obtén el índice seleccionado en lista2 y conviértelo en el nodo correspondiente.
#             estacion = self.lista2.get(seleccion)
#             for nodo, nombre in self.estaciones.items():
#                 if nombre == estacion:
#                     self.nodo_out = nodo
#                     break
            
#             print(f"Estación seleccionada como destino: {estacion} ({self.nodo_out})") 
#             self.find_best_ruta()
#     def find_best_ruta(self):

#         rho = 0.9
#         alpha = 1
#         beta = 1
#         Q = 1
#         num_hormigas = 100
#         num_iteraciones = 200#323
#         heuristica = {arista:1.0/self.conexiones[arista] for arista in self.conexiones} #Visibilidad
        
#         mejor_camino = None
#         mejor_longitud = float('inf')
        
#         for iteraciones in range(num_iteraciones):
#             caminos_todos = []
#             longitudes_todos = []
#             for hormiga in range(num_hormigas):
#                 # print("{hormiga}")
#                 nodo_actual = self.nodo_in
#                 nodos_visitados = [nodo_actual]
#                 camino = []
#                 longitud_total = 0
        
#                 while nodo_actual != self.nodo_out:
#                     nodos_vecinos = [
#                     nodo for nodo in self.nodos if nodo != nodo_actual
#                     and nodo not in nodos_visitados
#                     and nodo not in self.nodo_inhibido  # Excluir nodos inhibidos
#                     and (min(nodo_actual, nodo), max(nodo_actual, nodo)) in self.conexiones
#                 ]

        
#                     if not nodos_vecinos:
#                         break
        
#                     probabilidades = []
#                     for vecino in nodos_vecinos:
#                         arista = (min(nodo_actual, vecino), max(nodo_actual, vecino))
#                         tau = self.feromonas[arista] ** alpha
#                         eta = heuristica[arista] ** beta
#                         probabilidades.append(tau * eta)
        
#                     suma_probabilidades = sum(probabilidades)
#                     probabilidades = [p / suma_probabilidades for p in probabilidades]
#                     # print(probabilidades)
        
#                     valor_random = random.random()
#                     suma_acumulada = 0
#                     proximo_nodo = None
#                     for i, nodo in enumerate(nodos_vecinos):
#                         suma_acumulada += probabilidades[i]
#                         if suma_acumulada >= valor_random:
#                             proximo_nodo = nodo
#                             # print(proximo_nodo)
#                             break
        
#                     camino.append(proximo_nodo)
#                     nodos_visitados.append(proximo_nodo)
#                     distancia = self.calcular_distancia(nodo_actual, proximo_nodo)
#                     longitud_total += distancia
#                     nodo_actual = proximo_nodo
        
#                 if nodo_actual == self.nodo_out:
#                     caminos_todos.append(camino)
#                     longitudes_todos.append(longitud_total)
                
#                     if longitud_total < mejor_longitud:
#                         mejor_longitud = longitud_total
#                         mejor_camino = [self.nodo_in]+camino
        
#             # Evaporación y refuerzo de feromonas
#             for arista in self.feromonas:
#                 self.feromonas[arista] *= (1-rho) 
        
#             # print(feromonas)
        
#             for camino, longitud in zip(caminos_todos, longitudes_todos):
#                 for i in range(len(camino) - 1):
#                     arista = (min(camino[i], camino[i + 1]), max(camino[i], camino[i + 1]))
#                     self.feromonas[arista] += Q / longitud
#             # print(feromonas)
        
#         # print(f"El mejor camino encontrado desde {nodo_in} es {mejor_camino} con longitud {mejor_longitud} km")
#         print('Mejor camino:')
#         for nodo in mejor_camino:
#             print(self.estaciones[nodo],end="->")
#         print(f"\nLongitud total: {mejor_longitud}")
        
#         self.muestra_best_ruta(mejor_camino)
       
#         return None
#     def normalizar_coordenadas(self, coords, canvas_width, canvas_height):
#         """Escala las coordenadas al tamaño del canvas y corrige el eje Y."""
#         # Encontrar valores mínimos y máximos de las coordenadas
#         x_values = [x for x, y in coords.values()]
#         y_values = [y for x, y in coords.values()]
#         x_min, x_max = min(x_values), max(x_values)
#         y_min, y_max = min(y_values), max(y_values)
    
#         # Escalar las coordenadas
#         for nodo in coords:
#             x, y = coords[nodo]
#             x_normalizado = (x - x_min) / (x_max - x_min) * canvas_width + 100
#             y_normalizado = canvas_height - (y - y_min) / (y_max - y_min) * canvas_height +  80#Invertir el eje Y
#             coords[nodo] = (x_normalizado, y_normalizado)
   
#     def muestra_best_ruta(self,mejor_camino):
#         print(mejor_camino)
#         ancho = self.canvas.winfo_height()
#         num_estaciones = len(mejor_camino)
#         step = ancho/(num_estaciones+2)
#         y = 0
#         for i,nodo in enumerate(mejor_camino):
#             y += step
#             self.canvas.create_text(1000,y, text = self.estaciones[nodo], fill = "white", font = ("Arial",10),tags = "texto")
#             if i < (len(mejor_camino)-1):
#                 self.canvas.create_line(1000, y+10, 1000, y + step - 10, fill = "cyan", dash = (10,4), width = 2,tags = "linea")
#                 self.canvas.create_oval(995,y+10,1005,y+20,fill = "purple", outline = "white", tags = "circulo")
#                 self.canvas.create_oval(995,y+step-20,1005,y+step-10,fill = "purple", outline = "white",tags = "circulo")
#         #formar tuplas de conexiones 
#         conexion = []
#         for i in range(len(mejor_camino)):
#             if i < len(mejor_camino)-1:
#                 conexion.append((mejor_camino[i],mejor_camino[i+1]))
#         #Resaltar ruta en el mapa
#         for (nodo1,nodo2) in conexion:
#             x1,y1 = self.coords_norm[nodo1]
#             x2,y2 = self.coords_norm[nodo2]
#             self.canvas.create_line(x1, y1, x2, y2, fill = "red", dash = (10,4), width = 4,tags = "linea")

#     def ventana_inhibir(self):
#         ventana = tk.Toplevel(self.root)
#         ventana.title("Inhibir Estacion")
#         ventana.configure(bg="black")

#         label = tk.Label(ventana, text="Selecciona un nodo para inhibir:", bg="black", fg="white", font=("Arial", 10))
#         label.pack(pady=10)

#         lista_nodos = tk.Listbox(ventana, selectmode=tk.SINGLE, bg="black", fg="white", highlightbackground="gray", highlightthickness=0)
#         for nodo, estacion in self.estaciones.items():
#             lista_nodos.insert(tk.END, f"{nodo} - {estacion}")
#         lista_nodos.pack(pady=10)

#         def inhibir():
#             seleccion = lista_nodos.curselection()
#             if seleccion:
#                 nodo = int(lista_nodos.get(seleccion).split(" - ")[0])
#                 self.nodo_inhibido.add(nodo)  # Añadir nodo a la lista de nodos inhibidos
#                 ventana.destroy()
#                 self.actualizar_mapa()  # Redibujar el mapa excluyendo nodos inhibidos

#         boton_inhibir = tk.Button(ventana, text="Ihnibir Estacion", command=inhibir, bg="red", fg="white")
#         boton_inhibir.pack(pady=10)

            
        
#     def reset(self):
#         self.canvas.delete("linea")
#         self.canvas.delete("circulo")
#         self.canvas.delete("texto")
#         # self.root.delete("btn_cerrar")
        
#         self.mapa()
        
        
#     def run(self):
#         self.mapa()
    
    

# if __name__ == "__main__":
#       juego = metro()
#       juego.run()

import tkinter as tk
import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class metro:
    def __init__(self):
        # Inicialización de atributos
        self.estados_nodos = {nodo: "habilitado" for nodo in range(28)}  # Todos los nodos habilitados al inicio
        self.coords = {}
        self.nodos = {}
        self.conexiones = {}
        self.estaciones = {}
        self.feromonas = {}
        self.nodo_in = 0 
        self.nodo_out = 0
        self.lista_inicio = []
        self.lista_fin = []

        # Inicialización de la raíz principal
        self.root = tk.Tk()
        #self.root.withdraw()  # Ocultar la ventana principal hasta que sea necesario
        self.root.title("Metro de la CDMX por ACO")
        self.root.configure(bg="black")

        # Crear el frame principal (se mostrará después de la ventana de nodos)
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear canvas para dibujar mapa
        self.canvas = tk.Canvas(self.main_frame, bg="black", width=1200, height=800, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Abrir la ventana de gestión de nodos como primer paso

    def mapa(self):
        self.nodos={
            0:(19.50467,-99.20010),1:(19.48949,-99.14473),2:(19.48533,-99.12547),
            3:(19.48514,-99.10437),4:(19.46991,-99.13657),5:(19.45952,-99.18752),
            6:(19.45823,-99.11391),7:(19.44498,-99.08688),8:(19.44493,-99.14525),
            9:(19.44393,-99.13862),10:(19.43965,-99.11818),11:(19.43751,-99.14715),   
            12:(19.43639,-99.14161),13:(19.43009,-99.11432),14:(19.42956,-99.12097),
            15:(19.42435,-99.13285),16:(19.42725,-99.14901), 17:(19.42721,-99.14210),
            18:(19.41510,-99.07436),19:(19.40198,-99.18732),20:(19.40659,-99.15520),
            21:(19.40918,-99.13563),22:(19.41097,-99.12176),23:(19.40417,-99.12067),
            24:(19.37609,-99.18778),25:(19.37068,-99.16505),26:(19.36113,-99.14308),
            27:(19.35626,-99.10118)
        }
        self.coords = {}
        for nodo, (lat, lon) in self.nodos.items():
            x = 111 * (lat - list(self.nodos.values())[0][0])
            y = 111 * np.cos(np.radians((lat + list(self.nodos.values())[0][0]) / 2)) * (lon - list(self.nodos.values())[0][1])
            self.coords[nodo] = (y, x)
        
        self.estaciones={    
            0: "Rosario",1: "Instituto del Petróleo", 2: "Deportivo 18 de Marzo",
            3: "Martín Carrera", 4: "La Raza",5: "Tacuba",
            6: "Consulado", 7: "Oceanía", 8: "Guerrero",
            9: "Garibaldí/Lagunilla",10: "Morelos",11: "Hidalgo",
            12: "Bellas Artes",13: "San Lázaro",14: "Candelaria",
            15: "Pino Suárez",16: "Balderas",17: "Salto del Agua",
            18: "Pantitlán",19: "Tacubaya", 20: "Centro Médico",
            21: "Chabacano",22: "Jamaica",23: "Santa Anita",
            24: "Mixcoac",25: "Zapata",26: "Ermita",27: "Atlalilco"}
        
        self.ventana_habilitar_nodos()
        
        self.conexiones={}
        for (nodo1,nodo2) in [
            (0,1),(0,5),(1,2),(1,4),(2,3),(2,4),(3,6),(4,6),(4,8),(5,11),(5,19),(6,7),(6,10),
            (7,13),(7,18),(8,9),(8,11),(9,10),(9,12),(10,13),(10,14),(11,12),(11,16),(12,15),
            (12,17),(13,14),(13,18),(14,15),(14,22),(15,17),(15,21),(16,17),(16,19),(16,20),
            (17,21),(18,22),(19,20),(19,24),(20,21),(20,25),(21,22),(21,26),(23,21),(22,23),
            (23,27),(24,25),(25,26),(26,27)
            ]:
            dist=self.calcular_distancia(nodo1,nodo2)
            self.conexiones[(min(nodo1,nodo2),max(nodo1,nodo2))]=dist
        
        self.coords_norm = self.coords.copy()
        self.normalizar_coordenadas(self.coords_norm, 700, 700)
        self.feromonas={arista:0.1 for arista in self.conexiones}
        
        
        self.canvas.create_text(700,80, text = "Metro de la CDMX", fill = "white", font=("Arial", 20))
        self.actualizar_listas()

        #Dibujar conexiones 
        for (nodo1,nodo2) in self.conexiones:
            x1,y1 = self.coords_norm[nodo1]
            x2,y2 = self.coords_norm[nodo2]
            self.canvas.create_line(x1, y1, x2, y2, fill = "cyan", dash = (10,4), width = 2)
        
        #Dibujar estaciones
        for nodo,(x,y) in self.coords_norm.items():
            color="red" if nodo in self.lista_fin else "purple"
            self.canvas.create_oval(x-5,y-5,x+5,y+5,fill = color, outline = "white")
            self.canvas.create_text(x+10, y-10, text = self.estaciones[nodo], fill = "white", font=("Arial", 8))
        
        self.label1 = tk.Label(self.main_frame,text = "ORIGEN",font=("Arial", 10), bg="black", fg="white" )
        self.label1.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.label2 = tk.Label(self.main_frame,text = "DESTINO",font=("Arial", 10), bg="black", fg="white" )
        
        self.lista_inicio = [self.estaciones[nodo] for nodo in self.estaciones if nodo not in self.lista_fin]
        self.lista1 = tk.Listbox(self.main_frame, selectmode = tk.SINGLE, bg = "black", fg = "white", highlightbackground ="gray", highlightthickness = 0)

        # Llena la lista 1 con las estaciones disponibles
        self.lista1.delete(0, tk.END)  
        for estacion in self.lista_inicio:
            self.lista1.insert(tk.END, estacion) 

        self.lista1.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.lista1.bind("<<ListboxSelect>>",self.lista1_evento)
        
        self.lista2 = tk.Listbox(self.main_frame, selectmode = tk.SINGLE, bg = "black", fg = "white", highlightbackground ="gray", highlightcolor="white", highlightthickness=0)
        self.lista2.bind("<<ListboxSelect>>",self.lista2_evento)
        
        self.main_frame.columnconfigure(0, weight=3) 
        self.main_frame.columnconfigure(1, weight=1)  
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=7)
        self.main_frame.rowconfigure(2, weight=1)
        
        button = tk.Button(self.main_frame, text="Cerrar", command=self.root.quit)
        button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        btn_reset = tk.Button(self.main_frame, text="Reset", command=self.reset)
        btn_reset.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.canvas.update()
        self.root.mainloop()
        
      
    def ventana_habilitar_nodos(self):
        """Ventana para habilitar o inhibir nodos (estaciones)."""

        # Crear ventana de nodos
        self.ventana_nodos = tk.Toplevel()
        self.ventana_nodos.title("Habilitar/Inhabilitar Estaciones")
        self.ventana_nodos.geometry("1200x800")
        self.ventana_nodos.configure(bg="black")

        # Etiqueta inicial
        label = tk.Label(
            self.ventana_nodos,
            text="Selecciona la opción de habilitar o inhabilitar estaciones:",
            font=("Arial", 12),
            bg="black",
            fg="white",
        )
        label.pack(pady=10)

        # Botón para habilitar nodos
        boton_habilitar = tk.Button(
            self.ventana_nodos,
            text="Habilitar Estaciones",
            command=lambda: self.mostrar_lista_nodos(accion="habilitar"),
            bg="purple",
            fg="white",
            font=("Arial", 20),
        )
        boton_habilitar.pack(pady=20)

        # Botón para inhabilitar nodos
        boton_inhabilitar = tk.Button(
            self.ventana_nodos,
            text="Inhabilitar Estaciones",
            command=lambda: self.mostrar_lista_nodos(accion="inhabilitar"),
            bg="purple",
            fg="white",
            font=("Arial", 20),
        )
        boton_inhabilitar.pack(pady=20)

        # Frame para la lista de nodos y los botones de acción
        self.frame_lista = tk.Frame(self.ventana_nodos, bg="black")
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def mostrar_lista_nodos(self, accion):
        """Muestra la lista de nodos y permite seleccionarlos según la acción."""

        # Limpiar el frame antes de mostrar contenido nuevo
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Crear lista de nodos
        self.lista_nodos = tk.Listbox(
            self.frame_lista,
            selectmode=tk.MULTIPLE,
            bg="black",
            fg="white",
            highlightbackground="gray",
            highlightthickness=1,
            selectbackground="purple",
            font=("Arial", 10),
        )
        self.lista_nodos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Rellenar la lista según la acción seleccionada
        if accion == "habilitar":
            estaciones_para_mostrar = {
                nodo: estacion for nodo, estacion in self.estaciones.items() if nodo in self.lista_fin
            }
            titulo = "Estaciones inhabilitadas:"
        else:  # accion == "inhabilitar"
            estaciones_para_mostrar = {
                nodo: estacion for nodo, estacion in self.estaciones.items() if nodo not in self.lista_fin
            }
            titulo = "Estaciones habilitadas:"

        # Etiqueta de título
        label = tk.Label(
            self.frame_lista,
            text=titulo,
            font=("Arial", 12),
            bg="black",
            fg="white",
        )
        label.pack(pady=5)

        # Agregar estaciones al Listbox
        for nodo, estacion in estaciones_para_mostrar.items():
            self.lista_nodos.insert(tk.END, estacion)

        # Botón para aplicar cambios y continuar
        boton_aplicar = tk.Button(
            self.frame_lista,
            text="Aplicar y Continuar",
            command=lambda: self.actualizar_estaciones(accion),
            bg="purple",
            fg="white",
            font=("Arial", 10),
        )
        boton_aplicar.pack(pady=10)

        # Botón para cerrar sin cambios
        boton_cerrar = tk.Button(
            self.frame_lista,
            text="Cerrar sin cambios",
            command=self.ventana_nodos.destroy,
            bg="gray",
            fg="white",
            font=("Arial", 10),
        )
        boton_cerrar.pack(pady=5)

    #__________________________
    def actualizar_lista_principal(self):
        """Actualiza la lista de estaciones mostrada en la ventana principal."""
        self.lista_nodos.delete(0, tk.END)  # Limpiar la lista actual
        estaciones_habilitadas = [
            estacion for estacion in self.estaciones.keys() if estacion not in self.lista_fin
        ]
        for estacion in estaciones_habilitadas:
            self.lista_nodos.insert(tk.END, estacion)  # Insertar las estaciones habilitadas



    def actualizar_estaciones(self, accion):
        # """Actualiza las estaciones habilitadas/inhabilitadas según la selección."""
        # seleccionados = self.lista_nodos.curselection()
        # estaciones_seleccionadas = [
        #     list(self.estaciones.keys())[indice] for indice in seleccionados
        # ]

        # if accion == "habilitar":
        #     # Mover nodos de la lista de inhabilitados a habilitados
        #     self.lista_fin = [nodo for nodo in self.lista_fin if nodo not in estaciones_seleccionadas]
        # elif accion == "inhabilitar":
        #     # Mover nodos a la lista de inhabilitados
        #     self.lista_fin.extend(nodo for nodo in estaciones_seleccionadas if nodo not in self.lista_fin)
        # # Actualizar inmediatamente la ventana del metro         
        # self.actualizar_lista_principal()   

        # if hasattr(self, "ventana_nodos") and self.ventana_nodos.winfo_exists():
        #     self.ventana_nodos.destroy()
        seleccionados = self.lista_nodos.curselection()
        estaciones_seleccionadas = [
            list(self.estaciones.keys())[indice] for indice in seleccionados
        ]
        for nodo in estaciones_seleccionadas:
                self.estados_nodos[nodo] = "habilitado" if accion == "habilitar" else "inhabilitado"

        # print(f"Estados de nodos actualizados: {self.estados_nodos}")
        self.actualizar_listas()
        self.actualizar_lista_principal()
        self.ventana_nodos.destroy()

    def actualizar_ventana_metro(self):
        """Actualiza la lista de estaciones en la ventana del metro según su estado."""
        if hasattr(self, "lista_metro") and isinstance(self.lista_nodos, tk.Listbox):
            # Primero, limpiamos el contenido actual
            self.lista_nodos.delete(0, tk.END)

            # Agregar nodos habilitados a la lista del metro
            for nodo in self.estaciones.keys():
                if nodo not in self.lista_fin:  # Solo nodos habilitados
                    self.lista_nodos.insert(tk.END, nodo)
    def actualizar_listas(self):
        self.lista_inicio = [
            self.estaciones[nodo] for nodo, estado in self.estados_nodos.items() if estado == "habilitado"
        ]
        self.lista_fin = [
            nodo for nodo, estado in self.estados_nodos.items() if estado == "inhabilitado"
        ]
    def calcular_distancia(self,nodo1,nodo2):
        x1,y1=self.coords[nodo1]
        x2,y2=self.coords[nodo2]
        distancia=np.sqrt((x2-x1)**2+(y2-y1)**2)
        return distancia
    def lista1_evento(self, event):
        # if self.lista2.winfo_ismapped():
        #     return
        # seleccion = self.lista1.curselection()
        # if seleccion:
        #     estacion = self.lista1.get(seleccion)
        #     for nodo, nombre in self.estaciones.items():
        #         if nombre == estacion:
        #             self.nodo_in = nodo
        #             break
    
        #     print(f"Estación seleccionada como inicio: {estacion} ({self.nodo_in})")
            
        #     # self.lista_fin = self.lista_inicio[:]
        #     # self.lista_fin.remove(estacion)
        #     if estacion in self.lista_inicio:
        #         self.lista_inicio.remove(estacion)
        #     self.lista_fin = [nodo for nodo in self.estaciones if self.estaciones[nodo] in self.lista_inicio]
        #     for elemento in self.lista_fin:
        #         self.lista2.insert(tk.END, elemento)
        #     self.label2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")    
        #     self.lista2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        if self.lista2.winfo_ismapped():
            return
        seleccion = self.lista1.curselection()
        if seleccion:
            estacion = self.lista1.get(seleccion)
            for nodo, nombre in self.estaciones.items():
                if nombre == estacion:
                    self.nodo_in = nodo
                    break

            print(f"Estación seleccionada como inicio: {estacion} ({self.nodo_in})")

            self.lista2.delete(0, tk.END)
            for estacion in self.lista_inicio:
                if estacion != self.estaciones[self.nodo_in]:
                    self.lista2.insert(tk.END, estacion) 
        # Muestra `self.lista2` y su etiqueta "DESTINO".
        self.label2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.lista2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")       


    def lista2_evento(self, event):
        seleccion = self.lista2.curselection()
        if seleccion:
            # Obtén el índice seleccionado en lista2 y conviértelo en el nodo correspondiente.
            estacion = self.lista2.get(seleccion)
            for nodo, nombre in self.estaciones.items():
                if nombre == estacion:
                    self.nodo_out = nodo
                    break
            
            print(f"Estación seleccionada como destino: {estacion} ({self.nodo_out})") 
            self.find_best_ruta()
    def find_best_ruta(self):

        rho = 0.9
        alpha = 1
        beta = 1
        Q = 1
        num_hormigas = 100
        num_iteraciones = 200#323
        heuristica = {arista:1.0/self.conexiones[arista] for arista in self.conexiones} #Visibilidad
        
        mejor_camino = None
        mejor_longitud = float('inf')
        
        for iteraciones in range(num_iteraciones):
            caminos_todos = []
            longitudes_todos = []
            for hormiga in range(num_hormigas):
                # print("{hormiga}")
                nodo_actual = self.nodo_in
                nodos_visitados = [nodo_actual]
                camino = []
                longitud_total = 0
        
                while nodo_actual != self.nodo_out:
                    nodos_vecinos = [
                        nodo for nodo in self.nodos if nodo != nodo_actual
                        and nodo not in nodos_visitados
                        and (min(nodo_actual, nodo), max(nodo_actual, nodo)) in self.conexiones
                    ]
        
                    if not nodos_vecinos:
                        break
        
                    probabilidades = []
                    for vecino in nodos_vecinos:
                        arista = (min(nodo_actual, vecino), max(nodo_actual, vecino))
                        tau = self.feromonas[arista] ** alpha
                        eta = heuristica[arista] ** beta
                        probabilidades.append(tau * eta)
        
                    suma_probabilidades = sum(probabilidades)
                    probabilidades = [p / suma_probabilidades for p in probabilidades]
                    # print(probabilidades)
        
                    valor_random = random.random()
                    suma_acumulada = 0
                    proximo_nodo = None
                    for i, nodo in enumerate(nodos_vecinos):
                        suma_acumulada += probabilidades[i]
                        if suma_acumulada >= valor_random:
                            proximo_nodo = nodo
                            # print(proximo_nodo)
                            break
        
                    camino.append(proximo_nodo)
                    nodos_visitados.append(proximo_nodo)
                    distancia = self.calcular_distancia(nodo_actual, proximo_nodo)
                    longitud_total += distancia
                    nodo_actual = proximo_nodo
        
                if nodo_actual == self.nodo_out:
                    caminos_todos.append(camino)
                    longitudes_todos.append(longitud_total)
                
                    if longitud_total < mejor_longitud:
                        mejor_longitud = longitud_total
                        mejor_camino = [self.nodo_in]+camino
        
            # Evaporación y refuerzo de feromonas
            for arista in self.feromonas:
                self.feromonas[arista] *= (1-rho) 
        
            # print(feromonas)
        
            for camino, longitud in zip(caminos_todos, longitudes_todos):
                for i in range(len(camino) - 1):
                    arista = (min(camino[i], camino[i + 1]), max(camino[i], camino[i + 1]))
                    self.feromonas[arista] += Q / longitud
            # print(feromonas)
        
        # print(f"El mejor camino encontrado desde {nodo_in} es {mejor_camino} con longitud {mejor_longitud} km")
        print('Mejor camino:')
        for nodo in mejor_camino:
            print(self.estaciones[nodo],end="->")
        print(f"\nLongitud total: {mejor_longitud}")
        
        self.muestra_best_ruta(mejor_camino)
       
        return None
    def normalizar_coordenadas(self, coords, canvas_width, canvas_height):
        """Escala las coordenadas al tamaño del canvas y corrige el eje Y."""
        # Encontrar valores mínimos y máximos de las coordenadas
        x_values = [x for x, y in coords.values()]
        y_values = [y for x, y in coords.values()]
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
    
        # Escalar las coordenadas
        for nodo in coords:
            x, y = coords[nodo]
            x_normalizado = (x - x_min) / (x_max - x_min) * canvas_width + 100
            y_normalizado = canvas_height - (y - y_min) / (y_max - y_min) * canvas_height +  80#Invertir el eje Y
            coords[nodo] = (x_normalizado, y_normalizado)
   
    def muestra_best_ruta(self,mejor_camino):
        print(mejor_camino)
        ancho = self.canvas.winfo_height()
        num_estaciones = len(mejor_camino)
        step = ancho/(num_estaciones+2)
        y = 0
        for i,nodo in enumerate(mejor_camino):
            y += step
            self.canvas.create_text(1000,y, text = self.estaciones[nodo], fill = "white", font = ("Arial",10),tags = "texto")
            if i < (len(mejor_camino)-1):
                self.canvas.create_line(1000, y+10, 1000, y + step - 10, fill = "cyan", dash = (10,4), width = 2,tags = "linea")
                self.canvas.create_oval(995,y+10,1005,y+20,fill = "purple", outline = "white", tags = "circulo")
                self.canvas.create_oval(995,y+step-20,1005,y+step-10,fill = "purple", outline = "white",tags = "circulo")
        #formar tuplas de conexiones 
        conexion = []
        for i in range(len(mejor_camino)):
            if i < len(mejor_camino)-1:
                conexion.append((mejor_camino[i],mejor_camino[i+1]))
        #Resaltar ruta en el mapa
        for (nodo1,nodo2) in conexion:
            x1,y1 = self.coords_norm[nodo1]
            x2,y2 = self.coords_norm[nodo2]
            self.canvas.create_line(x1, y1, x2, y2, fill = "red", dash = (10,4), width = 4,tags = "linea")
            
        
    def reset(self):
        # self.canvas.delete("linea")
        # self.canvas.delete("circulo")
        # self.canvas.delete("texto")
        # # self.root.delete("btn_cerrar")
        
        # self.mapa()
        self.canvas.delete("linea")
        self.canvas.delete("circulo")
        self.canvas.delete("texto")
        self.mapa()
        
        
    def run(self):
        self.mapa()
    
    

if __name__ == "__main__":
      app = metro()
      app.run()
