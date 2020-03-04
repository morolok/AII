import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from tkinter import messagebox
from datetime import datetime


conexion = sqlite3.connect('meneame.db')

conexion.execute('''DROP TABLE IF EXISTS NOTICIA;''')

conexion.execute('''CREATE TABLE NOTICIA
         (TITULO           TEXT    NOT NULL,
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
    return res

def cargar():
    conexion.text_factory = str
    ls = extraerNoticias()
    for n in ls:
        titulo = n.find("h2").text
        link = n.find("h2").find("a")['href']
        nombre_autor = n.find("div", class_="news-submitted").find_all("a")[1].text
        fecha = n.find_all("span", class_=["ts","visible"])[1]["data-ts"]
        conexion.execute("INSERT INTO NOTICIA (TITULO,LINK,NOMBRE_AUTOR,FECHA) VALUES (?, ?, ?, ?)", (titulo, link, nombre_autor, fecha))
    conexion.commit()
    msg = messagebox.showinfo("Información BD", "BD creada correctamente con " + str(len(ls)) + " elementos")

def mostrar():
    ventanaMostrar = tk.Tk()
    ventanaMostrar.title("Elementos de la BD")
    noticiasBD = conexion.execute("SELECT TITULO, NOMBRE_AUTOR, FECHA FROM NOTICIA;")
    subventana = tk.Frame(ventanaMostrar)
    subventana.pack()
    listboxMostrar = tk.Listbox(subventana, width=150, height=20)
    barraScroll = tk.Scrollbar(subventana, orient="vertical")
    barraScroll.pack(side="right", fill="y")
    barraScroll.config(command=listboxMostrar.yview)
    listboxMostrar.config(yscrollcommand=barraScroll.set)
    contador = 1
    for n in noticiasBD:
        titulo = n[0]
        nombre_autor = n[1]
        fecha = n[2]
        fechaFormateada = datetime.fromtimestamp(int(fecha))
        texto = titulo + " " + nombre_autor + " " + str(fechaFormateada)
        listboxMostrar.insert(contador, texto)
        contador += 1
    listboxMostrar.pack()    
    ventanaMostrar.mainloop()

def salir(ventanaACerrar):
    ventanaACerrar.destroy()

def buscarAutor():
    ventanaBuscarAutor = tk.Tk()
    ventanaBuscarAutor.title("Buscar noticia por autor")
    noticiasBD = conexion.execute("SELECT TITULO, NOMBRE_AUTOR, FECHA FROM NOTICIA;")
    autores = list({n[1] for n in noticiasBD})
    spinboxVentana = tk.Spinbox(ventanaBuscarAutor, values = autores)
    spinboxVentana.place(x=0,y=0)
    spinboxVentana.update()
    spinboxVentana.pack()

    def buscarNoticiasAutor():
        conexion.text_factory = str
        ventanaMostrar = tk.Tk()
        ventanaMostrar.title("Noticias del autor")
        autorSeleccionado = spinboxVentana.get()
        subventana = tk.Frame(ventanaMostrar)
        subventana.pack()
        listboxMostrar = tk.Listbox(subventana, width=150, height=20)
        autorBuscar = "%" + autorSeleccionado + "%"
        noticasBuscadas = conexion.execute("SELECT TITULO, NOMBRE_AUTOR, FECHA FROM NOTICIA WHERE NOMBRE_AUTOR LIKE ?",(autorBuscar,))
        barraScroll = tk.Scrollbar(subventana, orient="vertical")
        barraScroll.pack(side="right", fill="y")
        barraScroll.config(command=listboxMostrar.yview)
        listboxMostrar.config(yscrollcommand=barraScroll.set)
        contador = 1
        for n in noticasBuscadas:
            titulo = n[0]
            nombre_autor = n[1]
            fecha = n[2]
            fechaFormateada = datetime.fromtimestamp(int(fecha))
            texto = titulo + " " + nombre_autor + " " + str(fechaFormateada)
            listboxMostrar.insert(contador, texto)
            contador += 1
        listboxMostrar.pack()
        ventanaMostrar.mainloop()
    
    largoSpinbox = spinboxVentana.winfo_width()
    botonBuscar = tk.Button(ventanaBuscarAutor, text="Buscar", command=buscarNoticiasAutor)
    botonBuscar.place(x=7*largoSpinbox, y=0)

def interfazGrafica():
    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Práctica 1")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar", command=cargar)
    datosMenu.add_command(label = "Mostrar", command=mostrar)
    datosMenu.add_command(label = "Salir", command= lambda: salir(ventana))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Autor", command=buscarAutor)
    buscarMenu.add_command(label = "Fecha")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()

conexion.execute('''DROP TABLE IF EXISTS NOTICIA;''')
conexion.close()