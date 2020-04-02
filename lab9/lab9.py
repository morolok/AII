import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from datetime import datetime

dirindex = "Index"

def get_schema():
    return Schema(titulo=TEXT(stored=True), tituloOriginal=TEXT(stored=True), fechaEstrenoSpain=DATETIME(stored=True), 
        paises=TEXT(stored=True), generos=TEXT(stored=True), director=TEXT(stored=True), sinopsis=TEXT(stored=True))

def extraerEnlacesPeliculas():
    url = "https://www.elseptimoarte.net/estrenos/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    aux = s.find("ul", class_="elements").find_all("li")
    res = []
    for p in aux:
        enlace = "https://www.elseptimoarte.net" + p.find("h3").find("a")["href"]
        enlace = enlace.replace(" ", "%20")
        res.append(enlace)
    return res

def cargar():
    enlaces = extraerEnlacesPeliculas()

    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    index = create_in(dirindex, schema=get_schema())
    writer = index.writer()

    cont = 0
    for enlace in enlaces:

        fichero = urllib.request.urlopen(enlace)
        s = BeautifulSoup(fichero, "lxml")

        titulo = ""
        tituloOriginal = ""
        auxFecha = ""
        paises = ""
        generos = ""
        director = ""
        sinopsis = s.find("div", class_="info", itemprop="description").text.strip()

        lsGeneros = s.find("p", class_="categorias").find_all("a")
        for i in range(0, len(lsGeneros)):
            if(i!=0):
                generos += ", " + lsGeneros[i].text.strip()
            else:
                generos += lsGeneros[i].text.strip()
        
        ficha = s.find("section", class_="highlight").find("div").find("dl").find_all()
        
        for i in range(0, len(ficha)):
            elemento = ficha[i]
            if(elemento.text.strip() == "Título"):
                titulo = ficha[i+1].text.strip()
            if(elemento.text.strip() == "Título original"):
                tituloOriginal = ficha[i+1].text.strip().replace("#", "")
            if(elemento.text.strip() == "País"):
                todosPaises = ficha[i+1].find_all("a")
                for j in range(0, len(todosPaises)):
                    if(j!=0):
                        paises += ", " + todosPaises[j].text.strip()
                    else:
                        paises += todosPaises[j].text.strip()
            if(elemento.text.strip() == "Director"):
                todosDirectores = ficha[i+1].find_all("a")
                for j in range(0, len(todosDirectores)):
                    if(j!=0):
                        director += ", " + todosDirectores[j].text.strip()
                    else:
                        director += todosDirectores[j].text.strip()
            if(elemento.text.strip() == "Estreno en España"):
                auxFecha = ficha[i+1].text.strip()
                #auxFecha = ficha[i+1].text.strip().split("/")
        
        if(titulo == ""):
            titulo = tituloOriginal
        #fechaEstrenoSpain = datetime.datetime(int(auxFecha[2]), int(auxFecha[1]), int(auxFecha[0]))
        todoBien = titulo != "" and tituloOriginal != "" and auxFecha != "" and paises != "" and generos != "" and director != ""  and sinopsis != ""
        if(todoBien):
            fechaEstrenoSpain = datetime.strptime(auxFecha, '%d/%m/%Y')
            writer.add_document(titulo=titulo, tituloOriginal=tituloOriginal, fechaEstrenoSpain=fechaEstrenoSpain, paises=paises, 
                director=director, sinopsis=sinopsis)
            cont += 1
    
    writer.commit()
    messagebox.showinfo("Información BD", "BD creada correctamente con " + str(cont) + " películas")

def salir(ventanaACerrar):
    ventanaACerrar.destroy()




def interfazGrafica():
    # Interfaz gráfica

    ventana = tk.Tk()
    ventana.title("Séptimo Arte")
    ventana.geometry("250x250")

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
    buscarMenu.add_command(label="Título y Sinopsis")
    buscarMenu.add_command(label = "Géneros")
    buscarMenu.add_command(label = "Fecha")

    # Añadimos la opción a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()