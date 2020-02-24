import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import urllib.request
import os.path
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
        if os.path.exists(file):
            recarga = input("La página ya ha sido cargada. Desea recargarla (s/n)?")
            if recarga == "s":
                urllib.request.urlretrieve(url, file)
        else:
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

bBuscar = tk.Button(ventana, text="Buscar")
bBuscar.place(x=largoAlmacenar+largoListar+1, y=0)


#Abrir la interfaz y cerrar la BD

ventana.mainloop()
conexion.execute('''DROP TABLE NOTICIA;''')
conexion.close()