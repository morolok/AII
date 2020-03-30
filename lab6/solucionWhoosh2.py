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

#extrae todas las noticias de las tres primeras pÃ¡ginas de "meneame"
def extraer_noticias():
    #devuelve una lista de tuplas. Cada tupla tiene la informaciÃ³n requerida de una noticia
    lista_noticias = []
    
    for i in range(1,4):
        lista_pagina = extraer_pagina("https://www.meneame.net/?page="+str(i))
        lista_noticias.extend(lista_pagina)
        
    return lista_noticias
    
    
#extrae todas las noticias que hay en una pÃ¡gina (url) y devuelve una lista    
def extraer_pagina(url):
    
    lista =[]
    
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")    
    l = s.find_all("div", class_= "center-content") #lista de noticias de la pagina
    for i in l:
        titulo = i.h2.a.string
        aux = i.find("div",class_="news-submitted")
        autor = aux.find_all("a")[1].string      
        fuentelink = aux.find("span",class_="showmytitle")
        if fuentelink:
            fuente = fuentelink.string
            link = fuentelink['title']
        else: #porque hay algunos casos que no tienen fuente y link
            fuente = "Anonima"
            link = "Desconocido"
        if aux.find("span",{'data-ts':True,'title':re.compile("publicado")}): 
            fecha_ts = aux.find("span",{'data-ts':True,'title':re.compile("publicado")})['data-ts']
        else: #porque hay algunos casos que no tienen fecha de publiacacion, solo de enviado
            fecha_ts = aux.find("span",{'data-ts':True,'title':re.compile("enviado")})['data-ts']
        fecha = datetime.fromtimestamp(int(fecha_ts))
        contenido = i.find("div",class_="news-content").get_text()  #se usa get_text porque hay algunos casos que tienen otras eqtiquetas en su interior
        lista.append((titulo,autor,fuente,link,fecha,contenido))
        
    return lista


#almacena cada noticia en un documento de un Ã­ndice. Usa la funciÃ³n extraer_noticias() para obtener la lista de noticias 
def almacenar_datos():
    
    #define el esquema de la informaciÃ³n
    schem = Schema(titulo=TEXT(stored=True), autor=TEXT(stored=True), fuente=TEXT(stored=True), link=ID(stored=True), fechahora=DATETIME(stored=True), contenido=TEXT)
    
    #eliminamos el directorio del Ã­ndice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el Ã­ndice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder aÃ±adir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_noticias()
    for noticia in lista:
        #aÃ±ade cada noticia de la lista al Ã­ndice
        writer.add_document(titulo=str(noticia[0]), autor=str(noticia[1]), fuente=str(noticia[2]), link=str(noticia[3]), fechahora=noticia[4], contenido=str(noticia[5]))    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " noticias")          


# permite buscar palabras en el "contenido" de las noticias 
def buscar_noticia():
    def mostrar_lista(event):
        #abrimos el Ã­ndice
        ix=open_dir("Index")
        #creamos un searcher en el Ã­ndice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "contenido" la palabra que hay en el Entry "en"
            query = QueryParser("contenido", ix.schema).parse(str(en.get()))
            #llamamos a la funciÃ³n search del searcher, pasÃ¡ndole como parÃ¡metro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Noticias")
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
                lb.insert(END,r['link'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Noticia")
    l = Label(v, text="Introduzca palabra a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
        


# permite buscar las noticias de una "fuente". FunciÃ³n similar a buscar_noticia
def buscar_fuente():
    def mostrar_lista(event):
        ix=open_dir("Index")      
        with ix.searcher() as searcher:

            query = QueryParser("fuente", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            v = Toplevel()
            v.title("Listado de Noticias")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results:
                lb.insert(END,r['titulo'])
                lb.insert(END,r['autor'])
                lb.insert(END,r['fuente'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Fuente")
    l = Label(v, text="Introduzca fuente a buscar:")
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
    buscarmenu.add_command(label="Noticia", command=buscar_noticia)
    buscarmenu.add_command(label="Fuente", command=buscar_fuente)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()