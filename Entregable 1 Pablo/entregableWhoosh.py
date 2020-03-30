#encoding:utf-8
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import re, os
from datetime import date
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser


#Apartado a Método cargar
def extraer_jornadas():
    resultado = []
    url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
    fichero = urllib.request.urlopen(url)
    string = BeautifulSoup(fichero, "lxml")
    resultado += string.find_all("div", class_=["cont-modulo", "resultados"])
    resultado2=resultado[0:3]
    return resultado2



def apartado_a(directorio):
    schem = Schema(jornada=TEXT(stored=True), eqlocal=TEXT(stored=True), eqvisitante=TEXT(stored=True), resultado=TEXT(stored=True), fecha=TEXT(stored=True),autor=TEXT(stored=True),titulo=TEXT(stored=True), resumen=TEXT(stored=True))
    if not os.path.exists(directorio):
        os.mkdir(directorio)
    ix = create_in(directorio, schema=schem)
    writer = ix.writer()
    lista =extraer_jornadas()
    prefijo = "https://resultados.as.com"
    contador=0
    for x in lista:
        jornada =x.find("h2",class_="tit-modulo").find("a").text
        resulPartidos = x.find("div", class_=["cont-resultados", "cf"]).find("table", class_="tabla-datos").find("tbody").find_all("tr")
        for j in resulPartidos:
            eqlocal=j.find("td", class_="col-equipo-local").find("a").find("span", class_="nombre-equipo").text
            eqvisitante = j.find("td", class_="col-equipo-visitante").find("a").find("span", class_="nombre-equipo").text
            resultado = j.find("td", class_=["col-resultado","finalizado"]).find("a").text.strip()
            
            link = prefijo + j.find("td", class_=["col-resultado","finalizado"]).find("a")["href"]
            fich=urllib.request.urlopen(link)
            string2 = BeautifulSoup(fich, "lxml")
            cronica= string2.find("div",class_=["cont-cuerpo-noticia","principal"])
            if (cronica is not None):
                fecha=cronica.find("div",class_="ntc-info").find("time").find("span",class_="s-inb-sm").find("a").text
                autor=cronica.find("div",class_="ntc-info").find("p",class_=["ntc-autor","s-inb"]).find("a").text
                titulo = cronica.find("h2",class_="live-title").find("a").text
                resumen = cronica.find("div",class_="cf").find("p").text
                writer.add_document(jornada=jornada, eqlocal=eqlocal, eqvisitante=eqvisitante, resultado=resultado, fecha=fecha,autor=autor,titulo=titulo,resumen=resumen)    
                contador+=1 
    writer.commit()
    messagebox.showinfo("Información" ,"Se han indexado "+str(contador)+ " partidos de forma exitosa")

directorio ="DiarioAS"


#Método búsqueda por noticia
def apartado_b_a():
    def mostrar_lista_noticias(event):
        #abrimos el �ndice
        ix=open_dir("DiarioAS")
        #creamos un searcher en el �ndice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "contenido" la palabra que hay en el Entry "en"
            query = QueryParser("resumen", ix.schema).parse(str(en.get()))
            #llamamos a la funci�n search del searcher, pas�ndole como par�metro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            listb = Listbox(v, yscrollcommand=sc.set)
            listb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = listb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                listb.insert(END,r['fecha'])
                listb.insert(END,r['titulo'])
                listb.insert(END,r['autor'])
                listb.insert(END,'')
    
    ve = Toplevel()
    ve.title("Busqueda por Noticia")
    l = Label(ve, text="Introduzca frase a buscar:")
    l.pack(side=LEFT)
    en = Entry(ve)
    en.bind("<Return>", mostrar_lista_noticias)
    en.pack(side=LEFT)
   
    
#Método búsqueda por equipo

def apartado_b_b():
    def mostrar_lista_equipo(event):
        #abrimos el �ndice
        ix=open_dir("DiarioAS")
        #creamos un searcher en el �ndice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "contenido" la palabra que hay en el Entry "en"
            query = QueryParser("eqlocal", ix.schema).parse(str(en.get()))
            query2 =QueryParser("eqvisitante",ix.schema).parse(str(en.get()))
            #llamamos a la funci�n search del searcher, pas�ndole como par�metro la consulta creada
            results = searcher.search(query)
            results2= searcher.search(query2)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            listb = Listbox(v, yscrollcommand=sc.set)
            listb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = listb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                listb.insert(END,r['jornada'])
                listb.insert(END,r['eqlocal'])
                listb.insert(END,r['eqvisitante'])
                listb.insert(END,r['resultado'])
            for w in results2:
                listb.insert(END,w['jornada'])
                listb.insert(END,w['eqlocal'])
                listb.insert(END,w['eqvisitante'])
                listb.insert(END,w['resultado'])
                listb.insert(END,'')
                
    
    ve = Toplevel()
    ve.title("Busqueda por Equipo")
    l = Label(ve, text="Introduzca equipo:")
    l.pack(side=LEFT)
    en = Entry(ve)
    en.bind("<Return>", mostrar_lista_equipo)
    en.pack(side=LEFT)
    
#Configuración Menú Principal

root = Tk()
menubar = Menu(root)

#Apartado a "Datos con 2 opciones

 
datosmenu = Menu(menubar, tearoff=0)
datosmenu.add_command(label="Cargar",command =lambda:apartado_a(directorio))
datosmenu.add_separator()   
datosmenu.add_command(label="Salir", command=root.quit)
    
menubar.add_cascade(label="Datos", menu=datosmenu)

#Apartado b “Buscar”, con dos opciones:
    
buscarmenu = Menu(menubar, tearoff=0)

# apartado a Noticia
buscarmenu.add_command(label="Noticia",command=lambda:apartado_b_a())

#apartado b Equipo
buscarmenu.add_command(label="Equipo",command=lambda:apartado_b_b())
    
menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
root.config(menu=menubar)
root.mainloop()

    
