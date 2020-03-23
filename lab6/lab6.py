import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from datetime import datetime

def get_schema():
    return Schema(titulo=TEXT(stored=True), autor=TEXT(stored=True), fuente=KEYWORD(stored=True), enlace=TEXT(stored=True), fecha=TEXT(stored=True), contenido=TEXT(stored=True))

def extraerNoticias():
    res = []
    url="https://www.meneame.net/?page="
    for i in range(1,4):
        url2 = url + str(i)
        fichero = urllib.request.urlopen(url2)
        s = BeautifulSoup(fichero, "lxml")
        res += s.find_all("div", class_=["center-content","no-padding"])
    return res

def cargar(dirindex):
    ls = extraerNoticias()
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    index = create_in(dirindex, schema=get_schema())
    writer = index.writer()
    cont = 0
    for n in ls:
        posibleFuente = n.find("div", class_="news-submitted").find("span", class_="showmytitle")
        if (posibleFuente is not None):
            titulo = n.find("h2").text.strip()
            autor = n.find("div", class_="news-submitted").find_all("a")[1].text.strip()
            fuente = posibleFuente.text.strip()
            enlace = n.find("h2").find("a")['href'].strip()
            fecha = n.find_all("span", class_=["ts","visible"])[1]["data-ts"]
            fechaFormateada = datetime.fromtimestamp(int(fecha)).strftime("%d/%m/%Y, %H:%M:%S")
            contenido = n.find("div", class_="news-content").text.strip()
            writer.add_document(titulo=titulo, autor=autor, fuente=fuente, enlace=enlace, fecha=fechaFormateada, contenido=contenido)
            cont += 1
    msg = messagebox.showinfo("Información BD", "BD creada correctamente con " + str(cont) + " elementos")
    writer.commit()

def salir(ventanaACerrar):
    ventanaACerrar.destroy()

def buscarNoticia(dirindex):
    ventanaBuscarNoticia = tk.Toplevel()
    ventanaBuscarNoticia.title("Buscar noticia")
    frame = tk.Frame(ventanaBuscarNoticia)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca la noticia que quiere buscar: ")
    etiqueta.pack(side=tk.LEFT)
    entradaNoticia = tk.Entry(frame)
    entradaNoticia.pack(side=tk.LEFT)

    def metodoBuscar(event):
        lb.delete(0,tk.END)   #borra toda la lista
        index = open_dir(dirindex)
        with index.searcher() as searcher:
            query = QueryParser("contenido", index.schema).parse(entradaNoticia.get())
            noticias = searcher.search(query)
            for n in noticias:
                lb.insert(tk.END, n['titulo'])
                lb.insert(tk.END, n['autor'])
                lb.insert(tk.END, n['enlace'])
                lb.insert(tk.END,'')
    
    entradaNoticia.bind("<Return>", metodoBuscar)
    sc = tk.Scrollbar(ventanaBuscarNoticia)
    sc.pack(side=tk.RIGHT, fill=tk.Y)
    lb = tk.Listbox(ventanaBuscarNoticia, yscrollcommand=sc.set)
    lb.pack(side=tk.BOTTOM, fill = tk.BOTH)
    sc.config(command = lb.yview)



def interfazGrafica():
    # Interfaz gráfica

    dirindex="Index"

    ventana = tk.Tk()
    ventana.title("Menéame")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar", command= lambda: cargar(dirindex))
    datosMenu.add_command(label = "Salir", command= lambda: salir(ventana))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Noticia", command= lambda: buscarNoticia(dirindex))
    buscarMenu.add_command(label = "Fuente")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()