import os
import pickle
import random
 
class TicTacToe:
    def __init__(self):
        self.tablero = [0] * 9  # Tablero vacío
        self.datos = self.cargar_datos()  # Cargar datos previos (aprendizaje)
        self.jugador_actual = 1  # El jugador 1 empieza por defecto
        self.humano = None  # Será asignado en el método jugar
        self.maquina = None  # Será asignado en el método jugar
        self.estado_jugadas = []  # Lista de estados por los que pasa en el juego
 
    def mostrar_tablero(self):
        simbolos = [' ', 'X', 'O']
        print('\nTablero:')
        for i in range(3):
            fila = ''
            for j in range(3):
                valor = self.tablero[i * 3 + j]
                fila += f' {simbolos[valor]} '
                if j < 2:
                    fila += '|'
            print(fila)
            if i < 2:
                print('---+---+---')
 
    def solicitar_posicion(self):
        posicion = int(input('Ingresa una posición (1-9): ')) - 1
        while posicion < 0 or posicion > 8 or self.tablero[posicion] != 0:
            posicion = int(input('Posición inválida. Ingresa una posición (1-9): ')) - 1
        return posicion
 
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
        if os.path.exists('datos_gato_refuerzo_02.pkl'):
            with open('datos_gato_refuerzo_02.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return {
                'casos': {},  # Mapeo de estado a valor
            }
 
    def guardar_datos(self):
        with open('datos_gato_refuerzo_02.pkl', 'wb') as f:
            pickle.dump(self.datos, f)
 
    def obtener_valor_estado(self):
        estado = tuple(self.tablero)
        if estado not in self.datos['casos']:
            self.datos['casos'][estado] = 0.5  # Valor neutral para estados nuevos
        return self.datos['casos'][estado]
 
    def escoger_mejor_movimiento(self):
        posibles_movimientos = [i for i, pos in enumerate(self.tablero) if pos == 0]
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
        posicion = self.solicitar_posicion()
        self.tablero[posicion] = self.jugador_actual
 
    def jugar_turno_maquina(self):
        posicion = self.escoger_mejor_movimiento()
        print(f'Máquina juega en la posición {posicion + 1}')
        self.tablero[posicion] = self.jugador_actual
 
    def jugar(self):
        turno = int(input('TURNO: (0 reinicia) (1 Máquina) (2 Humano) (3 Terminar): '))
        if turno == 0:
            print('Reiniciando juego...')
            return True  # Reinicia el juego
        elif turno == 3:
            print('Terminando el juego. ¡Hasta la próxima!')
            return False  # Termina el juego
 
        self.estado_jugadas = []  # Resetear jugadas del estado
        self.tablero = [0] * 9  # Tablero vacío
 
        if turno == 1:
            self.humano = 2
            self.maquina = 1
            self.jugador_actual = self.maquina
        elif turno == 2:
            self.humano = 1
            self.maquina = 2
            self.jugador_actual = self.humano
        else:
            print("Opción inválida. Selecciona 1 (Máquina) o 2 (Humano).")
            return True  # Reinicia el juego
 
        juego_en_curso = True
 
        while juego_en_curso:
            self.mostrar_tablero()
            if self.jugador_actual == self.humano:
                self.jugar_turno_humano()
            else:
                self.jugar_turno_maquina()
 
            self.estado_jugadas.append(tuple(self.tablero))  # Guardar el estado actual
 
            resultado = self.verificar_victoria()
            if resultado != -1:
                self.mostrar_tablero()
                if resultado == 0:
                    print('El juego terminó en empate.')
                else:
                    ganador = 'Humano' if resultado == self.humano else 'Máquina'
                    print(f'El ganador es: {ganador}')
                self.actualizar_valores(resultado)
                juego_en_curso = False
 
            self.jugador_actual = self.humano if self.jugador_actual == self.maquina else self.maquina
 
        self.guardar_datos()
        return True
 
# Ejecutar el juego
if __name__ == "__main__":
    juego = TicTacToe()
    while juego.jugar():
        pass