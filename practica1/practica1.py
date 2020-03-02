import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request


conexion = sqlite3.connect('meneame.db')

#conexion.execute('''DROP TABLE NOTICIA;''')

conexion.execute('''CREATE TABLE NOTICIA
         (ID INT PRIMARY KEY     NOT NULL,
         TITULO           TEXT    NOT NULL,
         LINK            TEXT     NOT NULL,
         NOMBRE_AUTOR        TEXT   NOT NULL,
         FECHA  TEXT);''')

def extraerNoticias():
    res = []
    url="https://www.meneame.net/?page="
    for i in range(1,4):
        url2 = url + str(i)
        fichero = urllib.request.urlopen(url2)
        s = BeautifulSoup(fichero, "lxml")
        res += s.find_all("div", class_=["center-content","no-padding"])
    #print(res[0])
    return res

extraerNoticias()

def cargar():
    conexion.text_factory = str
    ls = extraerNoticias()
    for n in ls:
        titulo = n.find("h2").text
        link = n.find("h2").find("a")['href']
        nombre_autor = n.find("div", class_="news-submitted").find_all("a")[1].text
        fecha = n.find_all("span", class_=["ts","visible"])[1]["data-ts"]
        print(fecha)
        

cargar()

def interfazGrafica():
    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Práctica 1")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar")
    datosMenu.add_command(label = "Mostrar")
    datosMenu.add_command(label = "Salir")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Autor")
    buscarMenu.add_command(label = "Fecha")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()

conexion.execute('''DROP TABLE NOTICIA;''')
conexion.close()