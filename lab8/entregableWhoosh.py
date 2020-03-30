#encoding:utf-8
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser

# Método para crear el esquema que me piden en el enunciado

def get_schema():
    return Schema(jornada=TEXT(stored=True), equipoLocal=TEXT(stored=True), equipoVisitante=TEXT(stored=True), resultado=TEXT(stored=True), 
        fechaCronica=TEXT(stored=True), autorCronica=TEXT(stored=True), tituloCronica=TEXT(stored=True), textoResumenCronica=TEXT(stored=True))

# Apartado a):

# a) Para este apartado he creado el método extraerJornadas donde accedo y saco los datos de la url del enunciado, y el método 
# apartado_a_a al que le paso como parámetro el directorio donde voy a almacenar los partidos y almaceno los partidos del número
# de jornadas que me digan en el enunciado

def extraerJornadas():
    res = []
    url="https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    res += s.find_all("div", class_=["cont-modulo", "resultados"])
    res2 = res[0:3]
    return res2

def apartado_a_a(dirjornadas):
    ls = extraerJornadas()
    if not os.path.exists(dirjornadas):
        os.mkdir(dirjornadas)
    jornadas = create_in(dirjornadas, schema=get_schema())
    writer = jornadas.writer()
    cabeceraUrl = "https://resultados.as.com"
    cont = 0
    for jornada in ls:
        jorn = jornada.find("h2").find("a").text
        resultadosPartidos = jornada.find("div", class_=["cont-resultados", "cf"]).find("table", class_="tabla-datos").find("tbody").find_all("tr")
        
        for partido in resultadosPartidos:
            equipoLocal = partido.find("td", class_="col-equipo-local").find("a").find("span", class_="nombre-equipo").text
            equipoVisitante = partido.find("td", class_="col-equipo-visitante").find("a").find("span", class_="nombre-equipo").text
            resultado = partido.find("td", class_=["col-resultado", "finalizado"]).find("a").text.strip()
            
            urlCronica = cabeceraUrl + partido.find("td", class_=["col-resultado", "finalizado"]).find("a")["href"]
            ficheroCronica = urllib.request.urlopen(urlCronica)
            sCronica = BeautifulSoup(ficheroCronica, "lxml")
            infoCronica = sCronica.find("div", class_=["cont-cuerpo-noticia", "principal"])
            
            if(infoCronica is not None):
                fechaCronica = infoCronica.find("div", class_="ntc-info").find("time").find("span", class_="s-inb-sm").find("a").text
                autorCronica = infoCronica.find("div", class_="ntc-info").find("p", class_=["ntc-autor", "s-inb"]).find("a").text
                tituloCronica = infoCronica.find("h2", class_="live-title").find("a").text
                textoResumenCronica = infoCronica.find("div", class_="cf").find("p").text
            
                writer.add_document(jornada=jorn, equipoLocal=equipoLocal, equipoVisitante=equipoVisitante, resultado=resultado, 
                    fechaCronica=fechaCronica, autorCronica=autorCronica, tituloCronica=tituloCronica, textoResumenCronica=textoResumenCronica)
                cont += 1

    writer.commit()
    messagebox.showinfo("Información", "Se han cargado un total de " + str(cont) + " partidos con éxito")

# b) Para este apartado he creado el método apartado_a_b al que le paso como parámetro la ventana que deseo cerrar y la cierro

def apartado_a_b(ventanaACerrar):
    ventanaACerrar.destroy()

# Apartado b):

# a) Para este apartado he creado el método apartado_b_a donde creo la ventana con las especificaciones del enunciado y lo que hago
# es buscar, con lo que ha introducido el usuario, texto resumen de las crónicas que son semejantes. Después muestro en una 
# nueva ventana con las especificaciones del enunciado los datos de la crónica que me piden

def apartado_b_a(dirjornadas):
    ventanaBuscarNoticia = tk.Toplevel()
    ventanaBuscarNoticia.title("Buscar noticia")
    ventanaBuscarNoticia.geometry("500x50")
    frame = tk.Frame(ventanaBuscarNoticia)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca la frase de la noticia que desea buscar: ")
    etiqueta.pack(side=tk.LEFT)
    entradaNoticia = tk.Entry(frame)
    entradaNoticia.pack(side=tk.LEFT)

    def metodoBuscar(event):
        fraseABuscar = entradaNoticia.get()
        ventanaResultados = tk.Toplevel()
        ventanaResultados.title("Resultados para " + fraseABuscar)
        ventanaResultados.geometry("600x165")
        barraScroll = tk.Scrollbar(ventanaResultados)
        barraScroll.pack(side=tk.RIGHT, fill=tk.Y)
        listBox = tk.Listbox(ventanaResultados, yscrollcommand=barraScroll.set)
        listBox.pack(side=tk.TOP, fill = tk.BOTH)
        barraScroll.config(command = listBox.yview)
        listBox.delete(0,tk.END)
        jornadas = open_dir(dirjornadas)
        with jornadas.searcher() as searcher:
            query = QueryParser("textoResumenCronica", jornadas.schema).parse(fraseABuscar)
            partidos = searcher.search(query, terms=True)
            for p in partidos:
                listBox.insert(tk.END, p['fechaCronica'])
                listBox.insert(tk.END, p['tituloCronica'])
                listBox.insert(tk.END, p['autorCronica'])
                listBox.insert(tk.END,'')

    entradaNoticia.bind("<Return>", metodoBuscar)

# b) Para este apartado he creado el método apartado_b_b donde creo la ventana con las especificaciones del enunciado y lo que hago
# es buscar, con el equipo que ha introducido el usuario, los partidos en los que ha jugado como local y después como visitante. 
# Después muestro en una nueva ventana con las especificaciones del enunciado los datos del partido que me piden

def apartado_b_b(dirjornadas):
    ventanaBuscarEquipo = tk.Toplevel()
    ventanaBuscarEquipo.title("Buscar equipo")
    ventanaBuscarEquipo.geometry("500x50")
    frame = tk.Frame(ventanaBuscarEquipo)
    frame.pack(side=tk.TOP)
    etiqueta = tk.Label(frame, text="Introduzca el equipo que desea buscar: ")
    etiqueta.pack(side=tk.LEFT)
    entradaEquipo = tk.Entry(frame)
    entradaEquipo.pack(side=tk.LEFT)

    def metodoBuscar(event):
        equipoABuscar = entradaEquipo.get()
        ventanaResultados = tk.Toplevel()
        ventanaResultados.title("Resultados para " + equipoABuscar)
        ventanaResultados.geometry("600x165")
        barraScroll = tk.Scrollbar(ventanaResultados)
        barraScroll.pack(side=tk.RIGHT, fill=tk.Y)
        listBox = tk.Listbox(ventanaResultados, yscrollcommand=barraScroll.set)
        listBox.pack(side=tk.TOP, fill = tk.BOTH)
        barraScroll.config(command = listBox.yview)
        listBox.delete(0,tk.END)
        jornadas = open_dir(dirjornadas)
        with jornadas.searcher() as searcher:
            queryLocal = QueryParser("equipoLocal", jornadas.schema).parse(equipoABuscar)
            partidosLocal = searcher.search(queryLocal, terms=True)
            for p in partidosLocal:
                listBox.insert(tk.END, p['jornada'])
                listBox.insert(tk.END, p['equipoLocal'])
                listBox.insert(tk.END, p['equipoVisitante'])
                listBox.insert(tk.END, p['resultado'])
                listBox.insert(tk.END,'')
            queryVisitante = QueryParser("equipoVisitante", jornadas.schema).parse(equipoABuscar)
            partidosVisitante = searcher.search(queryVisitante, terms=True)
            for p in partidosVisitante:
                listBox.insert(tk.END, p['jornada'])
                listBox.insert(tk.END, p['equipoLocal'])
                listBox.insert(tk.END, p['equipoVisitante'])
                listBox.insert(tk.END, p['resultado'])
                listBox.insert(tk.END,'')

    entradaEquipo.bind("<Return>", metodoBuscar)

# Método para crear la interfaz gráfica

def interfazGrafica():
    # Directorio en el que almacenar los partidos

    dirjornadas="Jornadas"

    ventana = tk.Tk()
    ventana.title("Diario AS")
    ventana.geometry("250x250")

    # Creamos la barra del menú como piden en el enuniciado

    barraMenu = tk.Menu(ventana)

    # Creamos la opción de "Datos" con las opciones que va a tener, que son cargar y salir del apartado a

    datosMenu = tk.Menu(barraMenu, tearoff=0)
    datosMenu.add_command(label="Cargar", command= lambda: apartado_a_a(dirjornadas))
    datosMenu.add_command(label = "Salir", command= lambda: apartado_a_b(ventana))

    # Añadimos la opción "Datos" a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Datos", menu=datosMenu)

    # Creamos la opción de "Buscar" con las opciones que va a tener, que son noticia y equipo del apartado b

    buscarMenu = tk.Menu(barraMenu, tearoff=0)
    buscarMenu.add_command(label="Noticia", command= lambda: apartado_b_a(dirjornadas))
    buscarMenu.add_command(label = "Equipo", command= lambda: apartado_b_b(dirjornadas))

    # Añadimos la opción de "Buscar" a la barra del menú con las opciones anteriores

    barraMenu.add_cascade(label="Buscar", menu=buscarMenu)

    # Usamos el método "config" para añadir el menú a la ventana, abrimos la interfaz y cerramos la conexión

    ventana.config(menu=barraMenu)
    ventana.mainloop()

interfazGrafica()