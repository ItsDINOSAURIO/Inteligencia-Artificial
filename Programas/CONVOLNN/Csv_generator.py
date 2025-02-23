#Marcar en un csv cada clase para realizar base de datos
import csv
import numpy as np
import matplotlib.pyplot as plt
import os



myData=[["Nombre","Categoria"]]
contenido = 'D:/01 Escuela/01 UPIITA/Semestre 2023-1/IA/Base/'
with os.scandir(contenido) as ficheros:
    print(ficheros)
    for fichero in ficheros:
        fich=fichero.name
        fich1=fich.replace('.jpg','').upper()
        if  ('DOG'in fich1) or ('P' in fich1):
            list1=[fich, '1']
        else:
            list1=[fich, '0']
        myData.append(list1)
        print(list1)

myFile = open('dataFiles.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(myData)

print(type(myData))
print("Writing complete")
