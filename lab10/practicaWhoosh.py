#encoding:utf-8

import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import re, os, shutil
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from datetime import datetime


def get_schema():
    return Schema(categoria=TEXT(stored=True), titulo=TEXT(stored=True), enlace=TEXT(stored=True), descripcion=TEXT(stored=True), 
        fecha=DATETIME(stored=True))

def extraerNoticias():
    url = "http://www.sensacine.com/noticias/?page="
    paginas = ["1", "2"]
    res = []
    for i in paginas:
        urlFinal = url + i
        fichero = urllib.request.urlopen(urlFinal)
        s = BeautifulSoup(fichero, "lxml")
        res += s.find("div", class_="col-left").find_all("div", class_=["card", "news-card"])
        #res += s.find("div", class_="col-left").find_all("div", class_=["card", "news-card", "news-card-full", "mdl", "cf"])
        #res += s.find("div", class_="col-left").find_all("div", class_=["card", "news-card", "news-card-row", "mdl", "cf"])
        #res += s.find("div", class_="col-left").find_all("div", class_=["card", "news-card", "news-card-col", "mdl", "cf"])
    return res

def apartado_a_a(dirnoticias):
    ls = extraerNoticias()
    meses = {"enero":"01", "febrero":"02", "marzo":"03", "abril":"04", "mayo":"05", "junio":"06", "julio":"07", "agosto":"08", "septiembre":"09", "octubre":"10", "noviembre":"11", "diciembre":"12"}
    prefijo = "http://www.sensacine.com"
    if not os.path.exists(dirnoticias):
        os.mkdir(dirnoticias)
    noticias = create_in(dirnoticias, schema=get_schema())
    writer = noticias.writer()
    cont = 0
    for n in ls:
        infoNoticia = n.find("div", class_="meta")
        categoria = infoNoticia.find("div", class_="meta-category").text.strip()
        titulo = infoNoticia.find("h2", class_="meta-title").find("a", class_="meta-title-link").text.strip()
        enlace = prefijo + infoNoticia.find("h2", class_="meta-title").find("a", class_="meta-title-link")['href']
        divDescripcion = infoNoticia.find("div", class_="meta-body")
        if(divDescripcion == None):
            descripcion = ""
        else:
            descripcion = divDescripcion.text.strip()
        fecha = infoNoticia.find("div", class_="meta-date").text.strip().split(" ")
        dia = fecha[1]
        mes = meses[fecha[3]]
        year = fecha[5]
        auxFecha = dia+"/"+mes+"/"+year
        fechaFormateada = datetime.strptime(auxFecha, '%d/%m/%Y')
        writer.add_document(categoria=categoria, titulo=titulo, enlace=enlace, descripcion=descripcion, fecha=fechaFormateada)
        cont += 1
    writer.commit()
    messagebox.showinfo("Información", "Se han cargado un total de " + str(cont) + " noticas con éxito")

def apartado_a_b(ventanaACerrar, dirnoticias):
    
    def eliminarDirectorioCreado():
        if(os.path.exists(dirnoticias)):
            shutil.rmtree(dirnoticias)
    
    eliminarDirectorioCreado()
    ventanaACerrar.destroy()

def apartado_b_a(dirnoticias):
    ventanaBuscarTyD = tk.Toplevel()
    ventanaBuscarTyD.title("Buscar título y descripción")
    ventanaBuscarTyD.geometry("600x50")
    frame = tk.Frame(ventanaBuscarTyD)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca la palabra o palabras de la noticia que desea buscar: ")
    etiqueta.pack(side=tk.LEFT)
    entradaTyD = tk.Entry(frame)
    entradaTyD.pack(side=tk.LEFT)

    def metodoBuscar(event):
        palabrasABuscar = entradaTyD.get().split(" ")
        ventanaResultados = tk.Toplevel()
        ventanaResultados.title("Resultados para " + entradaTyD.get())
        ventanaResultados.geometry("800x165")
        barraScroll = tk.Scrollbar(ventanaResultados)
        barraScroll.pack(side=tk.RIGHT, fill=tk.Y)
        listBox = tk.Listbox(ventanaResultados, yscrollcommand=barraScroll.set)
        listBox.pack(side=tk.TOP, fill = tk.BOTH)
        barraScroll.config(command = listBox.yview)
        listBox.delete(0,tk.END)
        noticias = open_dir(dirnoticias)
        with noticias.searcher() as searcher:
            notis = []
            for p in palabrasABuscar:
                query = MultifieldParser(["titulo", "descripcion"], noticias.schema).parse(p)
                notis += searcher.search(query, terms=True)
            for n in notis:
                listBox.insert(tk.END, n['categoria'])
                listBox.insert(tk.END, n['titulo'])
                listBox.insert(tk.END, n['fecha'])
                listBox.insert(tk.END,'')

    entradaTyD.bind("<Return>", metodoBuscar)

def apartado_b_b(dirnoticias):
    ventanaBuscarFecha = tk.Toplevel()
    ventanaBuscarFecha.title("Buscar Fecha")
    ventanaBuscarFecha.geometry("600x50")
    frame = tk.Frame(ventanaBuscarFecha)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca el rango de fechas en formato DD/MM/AAAA DD/MM/AAAA: ")
    etiqueta.pack(side=tk.LEFT)
    entradaFecha = tk.Entry(frame)
    entradaFecha.pack(side=tk.LEFT)

    def metodoBuscar(event):
        fechas = entradaFecha.get().split(" ")
        fechaInicio = fechas[0].split("/")
        fechaFin = fechas[1].split("/")
        fechaInicioFormateada = fechaInicio[2]+fechaInicio[1]+fechaInicio[0]
        fechaFinFormateada = fechaFin[2]+fechaFin[1]+fechaFin[0]
        fechaComprobarFormato = fechaInicioFormateada + " " + fechaFinFormateada
        if(not re.match("\d{8} \d{8}", fechaComprobarFormato)):
            messagebox.showinfo("Error", "Formato del rango de fecha incorrecto")
            return
        rango_fecha = '[' + fechaInicioFormateada + ' TO ' + fechaFinFormateada + ']'
        ventanaResultados = tk.Toplevel()
        ventanaResultados.title("Resultados para el rango de fechas dado")
        ventanaResultados.geometry("800x165")
        barraScroll = tk.Scrollbar(ventanaResultados)
        barraScroll.pack(side=tk.RIGHT, fill=tk.Y)
        listBox = tk.Listbox(ventanaResultados, yscrollcommand=barraScroll.set)
        listBox.pack(side=tk.TOP, fill = tk.BOTH)
        barraScroll.config(command = listBox.yview)
        listBox.delete(0,tk.END)
        noticias = open_dir(dirnoticias)
        with noticias.searcher() as searcher:
            query = QueryParser("fecha", noticias.schema).parse(rango_fecha)
            notis = searcher.search(query)
            for n in notis:
                listBox.insert(tk.END, n['categoria'])
                listBox.insert(tk.END, n['titulo'])
                listBox.insert(tk.END, n['fecha'])
                listBox.insert(tk.END,'')

    entradaFecha.bind("<Return>", metodoBuscar)

def apartado_b_c(dirnoticias):
    ventanaBuscarDescripcion = tk.Toplevel()
    ventanaBuscarDescripcion.title("Buscar título y descripción")
    ventanaBuscarDescripcion.geometry("600x50")
    frame = tk.Frame(ventanaBuscarDescripcion)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca la frase de la noticia que desea buscar: ")
    etiqueta.pack(side=tk.LEFT)
    entradaDescripcion = tk.Entry(frame)
    entradaDescripcion.pack(side=tk.LEFT)

    def metodoBuscar(event):
        fraseABuscar = entradaDescripcion.get()
        ventanaResultados = tk.Toplevel()
        ventanaResultados.title("Resultados para " + fraseABuscar)
        ventanaResultados.geometry("800x165")
        barraScroll = tk.Scrollbar(ventanaResultados)
        barraScroll.pack(side=tk.RIGHT, fill=tk.Y)
        listBox = tk.Listbox(ventanaResultados, yscrollcommand=barraScroll.set)
        listBox.pack(side=tk.TOP, fill = tk.BOTH)
        barraScroll.config(command = listBox.yview)
        listBox.delete(0,tk.END)
        noticias = open_dir(dirnoticias)
        with noticias.searcher() as searcher:
            query = QueryParser("descripcion", noticias.schema).parse(fraseABuscar)
            notis = searcher.search(query)
            for n in notis:
                listBox.insert(tk.END, n['titulo'])
                listBox.insert(tk.END, n['enlace'])
                listBox.insert(tk.END, n['descripcion'])
                listBox.insert(tk.END,'')

    entradaDescripcion.bind("<Return>", metodoBuscar)

def interfazGrafica():
    
    dirnoticias = "Noticias"

    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Sensacine")
    ventana.geometry("250x250")

    # Creamos la barra del menú

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar", command= lambda: apartado_a_a(dirnoticias))
    datosMenu.add_command(label = "Salir", command= lambda: apartado_a_b(ventana, dirnoticias))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Titulo y Descripción", command= lambda: apartado_b_a(dirnoticias))
    buscarMenu.add_command(label = "Fecha", command= lambda: apartado_b_b(dirnoticias))
    buscarMenu.add_command(label = "Descripción", command= lambda: apartado_b_c(dirnoticias))

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()