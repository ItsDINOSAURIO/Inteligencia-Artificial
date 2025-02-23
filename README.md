# Proyectos-Intelligencia Artificial

## Proyectos realizados para la materia Inteligencia Artificial

## Requisitos

- Python 3.7+

## Instalación

1. Clona este repositorio en local:
    1. Clic derecho en la carpeta a trabajar
    2. Mas opciones
    3. Abrir git bash aqui
    
    ```bash
    git clone https://github.com/ItsDINOSAURIO/Proyectos_Patrones.git
    cd Proyecto 
    ```
**cd mueve a bash a la carpeta específica donde se trabajará**

2. En caso de no ser aceptado por git bash
    ```bash
    git config --global user.name "Nombre_de_Usuario"
    git config --global user.email "Correo"
    ```
3. Comprobar que bash reconoce al usuario
    ```bash
    git config --global user.name
    git config --global user.email
    ```

## Primeros pasos con git para hacer commits al repositorio desde local una vez instalado (los comandos pueden realizarse desde una terminal de VSC)

1. Agregar carpetas o todas las carpetas necesarias
   
    ```bash
    git add . 
    ```

    ***El punto indica todas las carpetas en caso contrario mencionar que carpeta se desea agregar***

2. Realizar el commit/actualización al repositorio
    
    ```bash
    git commit -m "[Nombre]" 
    ```

3. Finalizar el push al origin

    ```bash
    git push origin main 
    ```

## Actualizar repositorio local

1. Revisar el status del repositorio
   
    ```bash
    git status
    ```
2. Realizar el pull del repositorio en github
    
    ```bash
    git pull 
    ```
***Una vez se verifica que el status del contenido local no está en riesgo conforme a lo que se menciona en la nube se puede hacer el pull sin ningún problema***
