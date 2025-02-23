import os
import pickle
import random
import tkinter as tk
from tkinter import messagebox
import socket

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.tablero = [0] * 9  # Tablero vacío
        self.datos = self.cargar_datos()  # Cargar datos previos
        self.jugador_actual = 1  # El jugador 1 empieza por defecto (máquina o humano)
        self.humano = None  # Será asignado cuando el jugador seleccione modo
        self.maquina = None  # Será asignado cuando el jugador seleccione modo
        self.estado_jugadas = []  # Lista de estados del juego
        self.botones = []  # Botones del tablero
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Crear los botones del tablero
        for i in range(9):
            boton = tk.Button(self.root, text=" ", font=("Arial", 20), width=5, height=2,
                              command=lambda i=i: self.jugar_turno_humano(i))
            boton.grid(row=i // 3, column=i % 3)
            self.botones.append(boton)
        
        # Botón para reiniciar el juego
        self.boton_reiniciar = tk.Button(self.root, text="Reiniciar", font=("Arial", 12),
                                         command=self.reiniciar_juego)
        self.boton_reiniciar.grid(row=3, column=0, columnspan=3)
        
        # Selector de turno inicial
        self.label_turno = tk.Label(self.root, text="Selecciona el turno", font=("Arial", 12))
        self.label_turno.grid(row=4, column=0, columnspan=3)
        
        self.boton_maquina = tk.Button(self.root, text="Iniciar IA", font=("Arial", 12),
                                       command=lambda: self.iniciar_juego(1))
        self.boton_maquina.grid(row=5, column=0, columnspan=3)
        
        self.boton_humano = tk.Button(self.root, text="Iniciar Prob-Bloq", font=("Arial", 12),
                                      command=lambda: self.iniciar_juego(2))
        self.boton_humano.grid(row=6, column=0, columnspan=3)
        
        #self.boton_servidor = tk.Button(self.root,text = )
    def reiniciar_juego(self):
        self.tablero = [0] * 9
        self.estado_jugadas = []
        self.actualizar_interfaz()
        
    def iniciar_juego(self, turno):
        self.reiniciar_juego()
        if turno == 1:
            self.iniciar_servidor(turno)
            self.humano = 2
            self.maquina = 1
            self.jugador_actual = self.maquina
            self.jugar_turno_maquina()  # La máquina inicia
        elif turno == 2:
            self.iniciar_servidor(turno)
            self.humano = 1
            self.maquina = 2
            self.jugador_actual = self.humano  # El humano inicia
            self.jugar_turno_humano()
            
    def actualizar_interfaz(self):
        simbolos = [' ', 'X', 'O']
        for i in range(9):
            self.botones[i].config(text=simbolos[self.tablero[i]])
        
    def solicitar_posicion(self, indice):
        if self.tablero[indice] == 0:
            return indice
        else:
            return None
    
    def verificar_victoria(self):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)              # Diagonales
        ]
        for combo in combinaciones:
            a, b, c = combo
            if self.tablero[a] == self.tablero[b] == self.tablero[c] != 0:
                return self.tablero[a]
        if all(pos != 0 for pos in self.tablero):
            return 0  # Empate
        return -1  # Juego en curso

    def cargar_datos(self):
        if os.path.exists('datos_gato_refuerzo_03.pkl'):
            with open('datos_gato_refuerzo_03.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return {'casos': {}}

    def guardar_datos(self):
        with open('datos_gato_refuerzo_03.pkl', 'wb') as f:
            pickle.dump(self.datos, f)

    def obtener_valor_estado(self):
        estado = tuple(self.tablero)
        if estado not in self.datos['casos']:
            self.datos['casos'][estado] = 0.5  # Valor neutral para estados nuevos
        return self.datos['casos'][estado]

    def escoger_mejor_movimiento(self):
        posibles_movimientos = [i for i, pos in enumerate(self.tablero) if pos == 0]
        if not posibles_movimientos:
            return None
        
        mejor_movimiento = None
        mejor_valor = -float('inf')

        for movimiento in posibles_movimientos:
            self.tablero[movimiento] = self.jugador_actual
            valor_estado = self.obtener_valor_estado()
            self.tablero[movimiento] = 0  # Deshacer el movimiento

            if valor_estado > mejor_valor:
                mejor_valor = valor_estado
                mejor_movimiento = movimiento

        return mejor_movimiento if mejor_movimiento is not None else random.choice(posibles_movimientos)

    def actualizar_valores(self, resultado):
        if resultado == self.maquina:
            recompensa = 1
        elif resultado == self.humano:
            recompensa = -1
        else:
            recompensa = 0  # Empate
        for estado in reversed(self.estado_jugadas):
            if estado not in self.datos['casos']:
                self.datos['casos'][estado] = 0.5  # Valor neutral para nuevos estados
            self.datos['casos'][estado] += 0.1 * (recompensa - self.datos['casos'][estado])
            recompensa = self.datos['casos'][estado]  # El valor de este estado es la recompensa para el anterior

    def jugar_turno_humano(self):
        indice = self.recibir_movimiento()
        if self.tablero[indice] == 0 and self.jugador_actual == self.humano:
            self.tablero[indice] = self.humano
            self.estado_jugadas.append(tuple(self.tablero))  # Guardar el estado
            self.actualizar_interfaz()
            self.jugador_actual = self.maquina
            self.verificar_estado()
            # if self.verificar_estado() == -1:
                # self.root.after(500,self.jugar_turno_maquina)

    def jugar_turno_maquina(self):
        posicion = self.escoger_mejor_movimiento()
        
        if posicion is not None:
            self.enviar_movimiento(posicion)
            self.tablero[posicion] = self.maquina
            self.estado_jugadas.append(tuple(self.tablero))  # Guardar el estado
            self.actualizar_interfaz()
            self.jugador_actual = self.humano
            self.verificar_estado()

    def verificar_estado(self):
        resultado = self.verificar_victoria()
        self.guardar_datos()
        if resultado != -1:
            ganador = 'Empate' if resultado == 0 else ('IA' if resultado == self.maquina else 'Prob-Bloq') #('Humano' if resultado == self.humano else 'Máquina')
            messagebox.showinfo("Juego Terminado", f"El ganador es: {ganador}")
            self.actualizar_valores(resultado)
            self.guardar_datos()
            self.reiniciar_juego()
        elif self.jugador_actual == self.humano:#self.maquina:
            self.root.after(500, self.jugar_turno_humano)#self.jugar_turno_maquina)  # Pausa de 500ms para la jugada de la máquina
        elif self.jugador_actual == self.maquina:
            self.root.after(500, self.jugar_turno_maquina)
        return resultado
    
    def iniciar_servidor(self,turno, host = '10.87.14.5', puerto = 49671):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host,puerto))
        self.sock.listen(1)
        print("Esperando conexión ...")
        self.conn,_ = self.sock.accept()
        self.jugador_actual =  turno
        print("Conexión exitosa, Inicia el juego")
    
    def enviar_movimiento(self,indice):
        #self.conn.sendall(str(indice).encode())
        self.conn.sendall(f"mov:{indice}".encode())
        print(f"{indice}")
    def recibir_movimiento(self):
        print("Esperando Datos")
        data = self.conn.recv(1024).decode()
        if data.startswith("mov:"):
            print(f"{data.split(":")[1]}")
            return int(data.split(":")[1])
        return None

# Inicializar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Juego del Gato con Aprendizaje")
    juego = TicTacToe(root)
    root.mainloop()