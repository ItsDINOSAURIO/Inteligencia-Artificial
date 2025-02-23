import socket
from tkinter import *
from tkinter import messagebox
import random
import time
import math

def blq():
    for i in range(0, 9):
        lB[i].config(state="disable")

def selec():
    global selec_mod
    selec_mod = Toplevel(v)
    selec_mod.geometry("300x200")
    selec_mod.title("Selecciona Modo de Juego")
    
    Label(selec_mod, text="Selecciona el modo de juego:").pack(pady=20)
    
    Button(selec_mod, text="Probabilístico", command=lambda: IJ0(1)).pack(pady=10)
    Button(selec_mod, text="Bloqueador", command=lambda: IJ0(2)).pack(pady=10)

def IJ0(modo):
    global tipo
    tipo = modo
    selec_mod.destroy()
    IJ()

def IJ():
    global turno, Tabla, Sec, FJ, cliente, t
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('10.87.14.5', 49671))
    turno = 2  # random.randint(1, 2)
    Tabla = [0] * 9
    t = ["N"] * 9  # Reinicializar el tablero
    Sec = [

        [4, 0, 2, 6, 8, 1, 3, 5, 7],
        [4, 6, 0, 8, 2, 3, 7, 1, 5],
        [4, 2, 0, 8, 6, 1, 5, 3, 7],
        [4, 8, 2, 6, 0, 5, 7, 3, 1]
    ]
    Sec = random.choice(Sec).copy()  # Usar copy() para evitar referencias
    FJ = False

    # Reiniciar la interfaz gráfica
    for i in range(9):
        lB[i].config(state="normal", bg="lightgray", text="")

    if turno == 2:
        tJ.set("Turno Prob-Bloq")
        v.after(500, Decide)
    else:
        tJ.set("Turno IA")
        v.after(500, recibir_movimiento)

def Decide():
    global turno, Sec, FJ
    if FJ:
        return

    if tipo == 1:
        num = Sec[0]
        Sec.remove(num)
    elif tipo == 2:
        num = 0
        i = 1
        j = 2
        time.sleep(0.2)
        while num == 0:
            if i == 1:
                s = [0, 1, 2]
            elif i == 2:
                s = [3, 4, 5]
            elif i == 3:
                s = [6, 7, 8]
            elif i == 4:
                s = [0, 3, 6]
            elif i == 5:
                s = [1, 4, 7]
            elif i == 6:
                s = [2, 5, 8]
            elif i == 7:
                s = [0, 4, 8]
            elif i == 8:
                s = [2, 4, 6]
            elif i == 9 and j == 2:
                j = 1
                i = 1
            elif i == 9 and j == 1:
                num = Sec[math.ceil(random.random() * len(Sec)) - 1]
            
            if Tabla[s[0]] == j and Tabla[s[1]] == j and Tabla[s[2]] == 0:
                num = s[2]
            elif Tabla[s[0]] == j and Tabla[s[1]] == 0 and Tabla[s[2]] == j:
                num = s[1]
            elif Tabla[s[0]] == 0 and Tabla[s[1]] == j and Tabla[s[2]] == j:
                num = s[0]
            i += 1
    
    # if num is not None and 0 <= num < 9 and t[num] == "N":
    cliente.sendall(f"mov:{num}".encode())
    v.after(500, lambda: val(num))  # Usar after para evitar problemas de sincronización

    

def val(num):
    global turno, Tabla, FJ
    
    if FJ or num is None or num < 0 or num >= 9 or t[num] != "N":
        return

    # Actualizar el tablero lógico
    t[num] = "O" if turno == 1 else "X"
    Tabla[num] = turno

    # Actualizar la interfaz gráfica
    if turno == 2:
        lB[num].config(text="X", bg="white")
        turno = 1
        tJ.set("Turno: " + J2)
    else:
        lB[num].config(text="O", bg="lightblue")
        turno = 2
        tJ.set("Turno: " + J1)

    lB[num].config(state="disable")
    print(f"Turno: {turno}")
    print(f"Tablero: {t}")
    print(f"Num Selec:{num}")
    
    verif()
    
    if not FJ and turno == 2:
        v.after(500, Decide)
    elif not FJ and turno == 1:
        v.after(500, recibir_movimiento)

def recibir_movimiento():
    global turno, cliente
    print(f"Recibiendo Datos")
    data = cliente.recv(1024).decode()
    if data.startswith("mov:"):
        num = int(data.split(":")[1])
        Sec.remove(num)
        v.after(500, lambda: val(num))
        
    

def verif():
    global FJ
    ganador = None

    lineas_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for linea in lineas_ganadoras:
        if all(t[i] == "O" for i in linea):
            ganador = J1
            break
        elif all(t[i] == "X" for i in linea):
            ganador = J2
            break

    if ganador:
        blq()
        messagebox.showinfo("Ganador", "Ganó " + ganador)
        FJ = True
    elif all(c != "N" for c in t):
        blq()
        messagebox.showinfo("Empate", "¡Es un empate!")
        FJ = True

# Configuración inicial de la ventana
v = Tk()
v.geometry("380x500")
v.title("Juego del Gato")

J1 = "IA"
J2 = "Prob-Bloq"
lB = []
t = ["N"] * 9
tJ = StringVar()
FJ = False
tipo = 0

# Crear botones del tablero
k = 0
n = 0
for i in range(3):
    m = 0
    for j in range(3):
        b = Button(v, width=9, height=3)
        lB.append(b)
        b.place(x=50 + m, y=50 + n)
        m += 100
        k += 1
    n += 100

Et = Label(v, textvariable=tJ).place(x=120, y=20)
I = Button(v, bg='#006', fg='white', text='Iniciar Juego', width=15, height=3, command=selec).place(x=130, y=350)
blq()

v.mainloop()