import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from tkinter import messagebox
from datetime import datetime
import time


conexion = sqlite3.connect("elseptimoarte.db")

conexion.execute("DROP TABLE IF EXISTS PELICULA;")

conexion.execute('''CREATE TABLE PELICULA
         (TITULO           TEXT    NOT NULL,
         TITULO_ORIGINAL            TEXT     NOT NULL,
         PAISES        TEXT   NOT NULL,
         FECHA_ESTRENO        TEXT   NOT NULL,
         DIRECTOR        TEXT   NOT NULL,    
         GENEROS  TEXT     NOT NULL);''')


def extraerEnlacesPeliculas():
    aux = []
    paginas = ["1", "2"]
    for i in paginas:
        url = "https://www.elseptimoarte.net/estrenos/" + i + "/"
        fichero = urllib.request.urlopen(url)
        s = BeautifulSoup(fichero, "lxml")
        aux += s.find("ul", class_="elements").find_all("li")
    res = []
    for p in aux:
        enlace = "https://www.elseptimoarte.net" + p.find("h3").find("a")["href"]
        enlace = enlace.replace(" ", "%20")
        res.append(enlace)
    return res

def cargar():
    enlaces = extraerEnlacesPeliculas()
    info_peli = []
    
    for enl in enlaces:
        fichero = urllib.request.urlopen(enl)
        s = BeautifulSoup(fichero, "lxml")
        generos = s.find("p", class_="categorias")
        informacion = s.find("section", class_="highlight").find("div")
        tup = (generos, informacion)
        info_peli.append(tup)
    
    for p in info_peli:
        p1 = p[0]
        p2 = p[1]
        gen = p1.find_all("a")


cargar()




def salir(ventanaACerrar):
    ventanaACerrar.destroy()

def interfazGrafica():
    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Películas")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar")
    datosMenu.add_command(label = "Salir", command= lambda: salir(ventana))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Título")
    buscarMenu.add_command(label = "Fecha")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

#interfazGrafica()

conexion.execute("DROP TABLE IF EXISTS PELICULA;")
conexion.close