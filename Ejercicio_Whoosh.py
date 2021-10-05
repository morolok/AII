#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser
#extrae todos los partidos de las 3 primreas jornadas del AS
def extraer_partidos():
    #devuelve una lista de tuplas. Cada tupla tiene la informacion requerida de una partido
    lista_partidos = []
    
    for i in range(1,4):
        for u in range(0,9):
            lista_partido = extraer_pagina("https://resultados.as.com/resultados/futbol/primera/2018_2019/directo/regular_a_"+str(i)+"_2482"+str(i)+str(u)+"/",i)
            lista_partidos.extend(lista_partido) 
    return lista_partidos
    
    
#extrae todos los partidos que hay en una pagina (url) y devuelve una lista    
def extraer_pagina(url,j):
    
    lista =[]
    
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")    
    jornada = j
    """--------------------------------------------------------------------------------------------------------------------------"""
    l = s.find("div", class_= "cont-info partido") #Crónica de la página
    if l:
        aux1 = l.find("div",class_="cont-cuerpo partido principal")
        titulo = aux1.h2.a.title                                                                                    
        """--------------------------------------------------------------------------------------------------------------------------"""
        aux2 = aux1.find("div",class_="ntc-info")
        autor = aux2.p.a.get_text
        fecha_aux = aux2.time.datetime.a.string
        fecha = fecha_aux.strftime('%d/%m/%y')
        """--------------------------------------------------------------------------------------------------------------------------"""
        aux3 = aux1.find("div",class_="cf")
        resumen = aux3.p.string
    else:
        titulo = "null"
        autor = "null"
        fecha = datetime.now
        resumen = "null"
    """--------------------------------------------------------------------------------------------------------------------------"""
    lo = s.find("div",class_="eq-local")
    local = lo.find("span",class_="nom")
    vi = s.find("div",class_="eq-visit")
    visitante = vi.find("span",class_="nom")
    tanteo = s.find("div",class_="marcador cf")
    tlocal = tanteo.find("span",class_="tanteo-local").get_text
    tvisit = tanteo.find("span",class_="tanteo-visit").get_text
    resultado = str(tlocal)+"-"+str(tvisit)

    lista.append((jornada,local,visitante,resultado,fecha,autor,titulo,resumen))    
        
    return lista


#almacena cada partido en un documento de un Ã­ndice. Usa la funciÃ³n extraer_partidos() para obtener la lista de partidos 
def almacenar_datos():
    
    #define el esquema de la informaciÃ³n
    schem = Schema(jornada=TEXT(stored=True), local=TEXT(stored=True), visitante=TEXT(stored=True), 
                    resultado=TEXT(stored=True), fecha=DATETIME(stored=True), autor=TEXT(stored=True),titulo=TEXT(stored=True),resumen=TEXT(stored=True))
    
    #eliminamos el directorio del Ã­ndice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el i­ndice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder anadir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_partidos()
    for partido in lista:
        #aÃ±ade cada partido de la lista al Ã­ndice
        writer.add_document(jornada=str(partido[0]), local=str(partido[1]), visitante=str(partido[2]), resultado=str(partido[3]), fecha=partido[4], autor=str(partido[5]), titulo=str(partido[6]),
        resumen=str(partido[7]))
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " partidos")          


# permite buscar palabras en el "resumen" de los partidos 
def buscar_cronica():
    def mostrar_lista(event):
        #abrimos el Ã­ndice
        ix=open_dir("Index")
        #creamos un searcher en el Ã­ndice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "resumen" la palabra que hay en el Entry "en"
            query = QueryParser("resumen", ix.schema).parse(str(en.get()))
            #llamamos a la funciÃ³n search del searcher, pasÃ¡ndole como parÃ¡metro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de crónicas")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                lb.insert(END,r['titulo'])
                lb.insert(END,r['autor'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por crónica")
    l = Label(v, text="Introduzca palabra a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
        


# permite buscar las partidos de una "Equipo". FunciÃ³n similar a buscar partido
def buscar_Equipo():
    def mostrar_lista(event):
        ix=open_dir("Index")      
        with ix.searcher() as searcher:

            query = QueryParser("local", ix.schema).parse(str(en.get())) + QueryParser("visitante", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            v = Toplevel()
            v.title("Listado de partidos")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results:
                lb.insert(END,r['jornada'])
                lb.insert(END,r['local'])
                lb.insert(END,r['visitante'])
                lb.insert(END,r['resultado'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Equipo")
    l = Label(v, text="Introduzca Equipo a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)


def ventana_principal():
        
    root = Tk()
    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_datos)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label= "Crónica", command=buscar_cronica)
    buscarmenu.add_command(label="Equipo", command=buscar_Equipo)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()