import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import urllib.request
import os.path
import dateutil.parser
#from tkinter import *


#Creacion de la BD y metodos para poblarla

conexion = sqlite3.connect('rssABC.db')

#conexion.execute('''DROP TABLE NOTICIA;''')

conexion.execute('''CREATE TABLE NOTICIA
         (ID INT PRIMARY KEY     NOT NULL,
         NOMBRE           TEXT    NOT NULL,
         LINK            TEXT     NOT NULL,
         FECHA        TEXT);''')


def extraer_lista(file):
    f = open (file, "r",encoding='utf-8')
    s = f.read()
    l1 = re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>', s)
    l2 = re.findall(r'<pubDate>(.*)</pubDate>', s)
    l=[]
    l = [list(e1) for e1 in l1]
    for e1,e2 in zip(l,l2):
        e1.append(e2)
    f.close()
    return l[1:]

def abrir_url(url, file):
    try:
        urllib.request.urlretrieve(url, file)
        return file
    except:
        print ("Error al conectarse a la página")
        return None

def almacenarBD():
    ficheroNoticias = abrir_url("https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml", "Noticias.txt")
    ls = extraer_lista(ficheroNoticias)
    for i in range(len(ls)):
        noticia = ls[i]
        nombreN = noticia[0]
        linkN = noticia[1]
        fechaN = noticia[2]
        conexion.execute("INSERT INTO NOTICIA (ID,NOMBRE,LINK,FECHA) VALUES (?, ?, ?, ?)", (i, nombreN, linkN, fechaN))
    conexion.commit()
    msg = messagebox.showinfo("Información BD", "BD creada correctamente")
    #print(fila)

def listarBD():
    elementosBD = conexion.execute("SELECT ID, NOMBRE, LINK, FECHA FROM NOTICIA")
    cadenaListar = ""
    for fila in elementosBD:
        nombre = fila[1]
        link = fila[2]
        fecha = fila[3]
        cadenaListar += nombre + "\n" + link + "\n" + fecha + "\n\n"
    msg = messagebox.showinfo("Elementos BD", cadenaListar)

def buscarMes():
    ventanaBuscarMes = tk.Tk()
    tk.Label(ventanaBuscarMes, text="Introduzca el mes (Xxx)").grid(row=0)
    entradaMes = tk.Entry(ventanaBuscarMes)
    entradaMes.grid(row=0, column=1)

    def metodoDeBuscar(event):
        mesABuscar = entradaMes.get()
        conexionBuscarMes = sqlite3.connect('rssABC.db')
        conexionBuscarMes.text_factory = str
        sBuscar = "%" + mesABuscar + "%"
        elementosBuscados = conexionBuscarMes.execute("SELECT ID, NOMBRE, LINK, FECHA FROM NOTICIA WHERE FECHA LIKE ?",(sBuscar,))
        resultados = ""
        for fila in elementosBuscados:
            nombre = fila[1]
            link = fila[2]
            fecha = fila[3]
            resultados += nombre + "\n" + link + "\n" + fecha + "\n\n"
        conexionBuscarMes.close()
        msg = messagebox.showinfo("Elementos BD por mes dado", resultados)

    entradaMes.bind("<Return>", metodoDeBuscar)
    ventanaBuscarMes.mainloop()

def buscarDia():
    ventanaBuscarDia = tk.Tk()
    tk.Label(ventanaBuscarDia, text="Introduzca la fecha dd/mm/aaaa").grid(row=0)
    entradaDia = tk.Entry(ventanaBuscarDia)
    entradaDia.grid(row=0, column=1)

    def metodoDeBuscar(event):
        diaABuscar = entradaDia.get()
        conexionBuscarDia = sqlite3.connect('rssABC.db')
        conexionBuscarDia.text_factory = str
        elementosBuscados = conexionBuscarDia.execute("SELECT ID, NOMBRE, LINK, FECHA FROM NOTICIA")
        resultados = ""
        for fila in elementosBuscados:
            if dateutil.parser.parse(diaABuscar).date() == dateutil.parser.parse(fila[3]).date():
                nombre = fila[1]
                link = fila[2]
                fecha = fila[3]
                resultados += nombre + "\n" + link + "\n" + fecha + "\n\n"
        conexionBuscarDia.close()
        msg = messagebox.showinfo("Elementos BD por fecha dada", resultados)
    
    entradaDia.bind("<Return>", metodoDeBuscar)
    ventanaBuscarDia.mainloop()



#Creacion de la interfaz
ventana = tk.Tk()

bAlmacenar = tk.Button(ventana, text="Almacenar", command = almacenarBD)
bAlmacenar.place(x=0, y=0)
bAlmacenar.update()
largoAlmacenar = bAlmacenar.winfo_width()

bListar = tk.Button(ventana, text="Listar", command = listarBD)
bListar.place(x=largoAlmacenar+1, y=0)
bListar.update()
largoListar = bListar.winfo_width()

bBuscarMes = tk.Button(ventana, text="Buscar mes", command = buscarMes)
bBuscarMes.place(x=largoAlmacenar+largoListar+1, y=0)
bBuscarMes.update()
largoBuscarMes = bBuscarMes.winfo_width()

bBuscarDia = tk.Button(ventana, text="Buscar día", command = buscarDia)
bBuscarDia.place(x=largoAlmacenar+largoListar+largoBuscarMes+1, y=0)


#Abrir la interfaz y cerrar la BD

ventana.mainloop()
conexion.execute('''DROP TABLE NOTICIA;''')
conexion.close()