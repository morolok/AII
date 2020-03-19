import tkinter as tk
from tkinter import messagebox
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser




def indexar(dirdocs,dirindex):
    if not os.path.exists(dirdocs):
        print ("Error: no existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)

    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    i=0
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            add_doc(writer, dirdocs, docname)
            i+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " correos")     
    writer.commit()

    
def buscarRemitente(dirindex):
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser("remitente", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['destinatarios'])
                lb.insert(END,r['asunto'])
                lb.insert(END,'')
    v = tk.Toplevel()
    v.title("Busqueda por rttes")
    f = tk.Frame(v)
    f.pack(side=tk.TOP)
    l = tk.Label(f, text="Introduzca el correo del rtte:")
    l.pack(side=tk.LEFT)
    en = tk.Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=tk.LEFT)
    sc = tk.Scrollbar(v)
    sc.pack(side=tk.RIGHT, fill=tk.Y)
    lb = tk.Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=tk.BOTTOM, fill = tk.BOTH)
    sc.config(command = lb.yview)    
   
            
def get_schema():
    return Schema(remitente=TEXT(stored=True), destinatarios=KEYWORD(stored=True), asunto=TEXT(stored=True), contenido=TEXT(stored=True))


def add_doc(writer, path, docname):
    fileobj=open(path+'\\'+docname, "r")
    rte=fileobj.readline().strip()
    dtos=fileobj.readline().strip()
    ast=fileobj.readline().strip()
    ctdo=fileobj.read()
    fileobj.close()
    writer.add_document(remitente=rte, destinatarios=dtos, asunto=ast, contenido=ctdo)


def interfazGrafica():

    dirdocs="Correos"
    dirindex="Index"

    ventana = tk.Tk()
    ventana.title("Whoosh")

    bIndexar = tk.Button(ventana, text="Indexar", command = lambda: indexar(dirdocs,dirindex))
    bIndexar.place(x=0, y=0)
    bIndexar.update()
    largoIndexar = bIndexar.winfo_width()

    bBuscarRemitente = tk.Button(ventana, text="Buscar Remitente", command = lambda: buscarRemitente(dirindex))
    bBuscarRemitente.place(x=largoIndexar+1, y=0)

    ventana.mainloop()

interfazGrafica()