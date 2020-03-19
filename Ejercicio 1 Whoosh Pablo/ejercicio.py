#encoding:utf-8
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from numpy import ix_


#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en el directorio dirindexa


def indexar(dirdocu,dirindexa):
    if not os.path.exists(dirdocu):
        print("Error no existe el directorio con los documentos" + dirdocu)
    else:
        if not os.path.exists(dirindexa):
            os.mkdir(dirindexa)
    ix = create_in(dirindexa, schema=get_schema())
    writer = ix.writer()
    j=0
    for docname in os.listdir(dirdocu):
        if not os.path.isdir(dirdocu+docname):
            add_doc(writer, dirdocu, docname)
            j+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(j)+ " correos") 
    writer.commit()

def get_schema():
    return Schema(remitente=TEXT(stored=True),destinatarios=KEYWORD(stored=True),asunto=TEXT(stored=True),cuerpo_correo=TEXT(stored=True))


def add_doc(writer,path,docname):
    fileobj = open(path+'\\'+docname,"r")
    remiten = fileobj.readline().strip()
    destinat = fileobj.readline().strip()
    asun = fileobj.readline().strip()
    cont = fileobj.read()
    fileobj.close()
    writer.add_document(remitente=remiten,destinatarios= destinat,asunto=asun,cuerpo_correo=cont)
  
def busqueda_remitente(dirindexa): 
    def mostrar_lista(event):
        lb.delete(0,END)
        ix=open_dir(dirindexa)
        with ix.searcher() as searcher:
            query = QueryParser("remitente",ix.schema).parse(str(en.get()))
            resultados = searcher.search(query)
            for x in resultados:
                lb.insert(END,x['destinatarios'])
                lb.insert(END,x['asunto'])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por remitentes")
    f = Frame(v)
    f.pack(side = TOP)
    lista = Label(f, text="Introducir correo del remitente")
    lista.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    barra = Scrollbar(v)
    barra.pack(side=RIGHT ,fill=Y)
    lb = Listbox(v,yscrollcommand=barra.set)
    lb.pack(side=BOTTOM,fill=BOTH)
    barra.config(command = lb.yview)
                
        



#Configuracion menu
dirdocu="Correos"
dirindexa="Index"

top = tk.Tk()

top.title("Ejercicio Whoosh")

A = tk.Button(top,text ="Indexar",command = lambda:indexar(dirdocu,dirindexa))
A.place(x=0,y=0)
A.update()
largoind = A.winfo_width()

B = tk.Button(top,text="Buscar Remitente",command = lambda:busqueda_remitente(dirindexa))
B.place(x=largoind+1,y=0)

top.mainloop()