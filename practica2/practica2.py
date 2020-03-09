import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from tkinter import messagebox
from datetime import datetime
import time


conexion = sqlite3.connect("vinissimus.db")

conexion.execute("DROP TABLE IF EXISTS VINO;")

conexion.execute('''CREATE TABLE VINO
         (NOMBRE_VINO           TEXT    NOT NULL,
         PRECIO            TEXT     NOT NULL,
         DENOMINACION_ORIGEN        TEXT   NOT NULL,
         BODEGA        TEXT   NOT NULL,    
         UVAS  TEXT     NOT NULL);''')


def extraerVinos():
    res = []
    vinos = ["0", "50"]
    for i in vinos:
        url = "https://www.vinissimus.com/es/vinos/tinto/index.html?start=" + i
        fichero = urllib.request.urlopen(url)
        s = BeautifulSoup(fichero, "lxml")
        res += s.find_all("tr", class_="warning")
    #print(res[0])
    return res

def cargar():
    conexion.text_factory = str
    vinos = extraerVinos()
    for v in vinos:
        info_vino = v.find("div", class_="info")
        nombre_vino = info_vino.find("h3").find("a").text
        precio = info_vino.find("p").find("span", class_ = ["price", "clearfix"]).text.split()[2] + " " + info_vino.find("p").find("span", class_ = ["price", "clearfix"]).text.split()[3]
        denominacion_origen = info_vino.find("p").find("span", class_="type").text.strip()
        bodega = info_vino.find("p").find("span", class_="owner").text
        lsUvas = info_vino.find("p").find("span", class_="grape").text.split(",")
        uvas = ""
        for i in range(0, len(lsUvas)):
            if(i==(len(lsUvas)-1)):
                u = lsUvas[i].strip()
                uvas += u
            else:
                u = lsUvas[i].strip()
                uvas += u + ", "
        conexion.execute("INSERT INTO VINO (NOMBRE_VINO, PRECIO, DENOMINACION_ORIGEN, BODEGA, UVAS) VALUES (?, ?, ?, ?, ?)", (nombre_vino, precio, denominacion_origen, bodega, uvas))
    conexion.commit()
    msg = messagebox.showinfo("Información BD", "BD creada correctamente con " + str(len(vinos)) + " elementos")

def salir(ventanaACerrar):
    ventanaACerrar.destroy()


def buscarDenominacion():
    ventanaBuscarDenominacion = tk.Tk()
    ventanaBuscarDenominacion.title("Buscar vino por denominación de origen")
    tk.Label(ventanaBuscarDenominacion, text="Introduzca la denominación de origen").grid(row=0)
    entradaDO = tk.Entry(ventanaBuscarDenominacion)
    entradaDO.grid(row=0, column=1)

    def metodoDeBuscar(event):
        denominacionABuscar = entradaDO.get()
        conexionBuscarDO = sqlite3.connect("vinissimus.db")
        conexionBuscarDO.text_factory = str
        doABuscar = "%" + denominacionABuscar + "%"
        elementosBuscados = conexionBuscarDO.execute("SELEC NOMBRE_VINO, PRECIO, DENOMINACION_ORIGEN, BODEGA, UVAS FROM VINO WHERE DENOMINACION_ORIGEN LIKE ?", (doABuscar,))

    entradaDO.bind("<Return>", metodoDeBuscar)
    ventanaBuscarDenominacion.mainloop()




def interfazGrafica():
    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Práctica 2")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar", command=cargar)
    datosMenu.add_command(label = "Salir", command= lambda: salir(ventana))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Denominación", command=buscarDenominacion)
    buscarMenu.add_command(label = "Bodega")
    buscarMenu.add_command(label = "Uvas")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()

conexion.execute("DROP TABLE IF EXISTS VINO;")
conexion.close