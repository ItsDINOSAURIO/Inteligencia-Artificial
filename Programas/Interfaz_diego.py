from tkinter import *
from tkinter import messagebox
import random
import time
import math

def blq():
    """Deshabilita todos los botones del tablero."""
    for i in range(0, 9):
        lB[i].config(state="disable")

def selec():
    """Crea una pantalla para seleccionar el modo de juego."""
    global selec_mod
    selec_mod = Toplevel(v)
    selec_mod.geometry("300x200")
    selec_mod.title("Selecciona Modo de Juego")
    selec_mod.config(bg="#2b2b2b")
    
    Label(selec_mod, text="Selecciona el modo de juego:", font=("Helvetica", 12), bg="#2b2b2b", fg="white").pack(pady=20)
    
    Button(selec_mod, text="Probabilístico", command=lambda: IJ0(1), bg='#4a4a4a', fg='white', font=("Helvetica", 10), width=20).pack(pady=10)
    Button(selec_mod, text="Bloqueador", command=lambda: IJ0(2), bg='#4a4a4a', fg='white', font=("Helvetica", 10), width=20).pack(pady=10)

def IJ0(modo):
    """Inicia el juego con el modo seleccionado."""
    global tipo
    tipo = modo
    selec_mod.destroy()
    IJ()

def IJ():
    """Inicia el juego, define el turno y limpia el tablero."""
    global turno, Tabla, Sec, FJ
    turno = random.randint(1, 2)
    Tabla = [0] * 9
    Sec = [
        [4, 0, 2, 6, 8, 1, 3, 5, 7],
        [4, 6, 0, 8, 2, 3, 7, 1, 5],
        [4, 2, 0, 8, 6, 1, 5, 3, 7],
        [4, 8, 2, 6, 0, 5, 7, 3, 1]
    ]
    Sec = random.choice(Sec)
    FJ = False

    if turno == 2:
        tJ.set("Turno Compu")
        v.after(700, Decide)
    else:
        tJ.set("Turno Humano")

    for i in range(0, 9):
        lB[i].config(state="normal", bg="#2b2b2b", text="", width=5, height=2, relief="raised", bd=3)  # Tamaño ajustado
        t[i] = "N"

def Decide():
    """Turno de la computadora, elige un movimiento según el modo."""
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

    val(num)

def val(num):
    """Valida el movimiento de los jugadores."""
    global turno, J1, J2, Sec, Tabla, FJ
    if FJ:
        return

    if num in Sec:
        Sec.remove(num)
    Tabla[num] = turno

    if t[num] == "N" and turno == 1:
        lB[num].config(text="X", bg="#373b44", fg="#cabbe9", font=("Helvetica", 16, "bold"), relief="solid", bd=6)  # Tamaño de fuente reducido
        t[num] = "X"
        turno = 2
        tJ.set("Turno: " + J2)
        verif()
        if not FJ:
            v.after(700, Decide)
    elif t[num] == "N" and turno == 2:
        lB[num].config(text="O", bg="#2e3b3f", fg="#f8c552", font=("Helvetica", 16, "bold"), relief="solid", bd=6)  # Tamaño de fuente reducido
        t[num] = "O"
        turno = 1
        tJ.set("Turno: " + J1)
    
    lB[num].config(state="disable")
    verif()

def verif():
    """Verifica si hay un ganador o un empate."""
    global FJ
    ganador = None

    lineas_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]

    for linea in lineas_ganadoras:
        if all(t[i] == "X" for i in linea):
            ganador = J1
        elif all(t[i] == "O" for i in linea):
            ganador = J2

    if ganador:
        blq()
        messagebox.showinfo("Ganador", "Ganó " + ganador)
        FJ = True
    elif all(c != "N" for c in t):  
        blq()
        messagebox.showinfo("Empate", "¡Es un empate!")
        FJ = True

# Inicialización de la ventana principal
v = Tk()
v.geometry("250x350")  # Ajuste del tamaño general de la ventana
v.title("Juego del Gato")
v.configure(bg="#2b2b2b")

J1 = "Humano"
J2 = "Computadora"
lB = []
t = []
tJ = StringVar()
FJ = False
tipo = 0

for i in range(0, 9):
    t.append("N")

# Crear botones usando grid y fijar el tamaño
for i in range(0, 3):
    for j in range(0, 3):
        b = Button(v, width=5, height=2, command=lambda k=3*i+j: val(k), bg='#4a4a4a', font=("Helvetica", 12), relief="raised", bd=6)  # Tamaño reducido
        lB.append(b)
        b.grid(row=i, column=j, padx=5, pady=5)

Et = Label(v, textvariable=tJ, bg="#2b2b2b", fg="white", font=("Helvetica", 14, "bold")).grid(row=3, column=0, columnspan=3, pady=10)
I = Button(v, bg='#645394', fg='white', text='Iniciar Juego', width=15, height=2, font=("Helvetica", 12), command=selec).grid(row=4, column=0, columnspan=3)

blq()
v.mainloop()
