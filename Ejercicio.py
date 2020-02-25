import tkinter
import tkinter as tk
import sqlite3
from tkinter import messagebox

# Base de datos
import re
import urllib.request
import os.path

#Creacion de la BD
conn = sqlite3.connect('test.db')
conn.execute('''DROP TABLE IF EXISTS NOTICIA''')

# Insercion de datos
conn.execute('''CREATE TABLE NOTICIA
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         LINK           TEXT    NOT NULL,
         DATE           TEXT);''')


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


def abrir_url(url,file):
    try:
        if os.path.exists(file):
            recarga = input("La pagina ya ha sido cargada. Desea recargarla (s/n)?")
            if recarga == "s":
                urllib.request.urlretrieve(url,file)
        else:
            urllib.request.urlretrieve(url,file)
        return file
    except:
        print  ("Error al conectarse a la pagina")
        return None
    





def rellenaBD():
    file = abrir_url("https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml","noticias.txt")
    lista = extraer_lista(file)
    for x in range(len(lista)):
        noticia = lista[x]
        nombre = noticia[0]
        fecha = noticia[1]
        link = noticia[2]
        conn.execute("INSERT INTO NOTICIA(ID,NAME,LINK,DATE)  VALUES (?,?,?,?)",(x,nombre,fecha,link));
    conn.commit()  
    mensaje = messagebox.showinfo("Info BD","BD creada correctamente")

def listaBD():
    elemBD = conn.execute("SELECT ID,NAME,LINK,DATE FROM NOTICIA")
    cadena = ""
    for fila in elemBD:
        nombre = fila[1]
        link =   fila[2] 
        fecha =  fila[3]
        cadena +=  nombre + "\n"+ link + "\n"+ fecha + "\n\n"
    mensaje = messagebox.showinfo("Elementos Base Datos", cadena)

#Creacion de la interfaz   
top = tkinter.Tk();     
    
A = tk.Button(top, text = "Almacenar",command = rellenaBD)
B = tk.Button(top, text = "Listar",command = listaBD)
C = tk.Button(top, text = "Buscar")

A.place(x = 0,y = 0)
A.update()
largoal= A.winfo_width()

B.place(x =largoal+1,y =0)
B.update()
largolis = B.winfo_width()
C.place(x = largolis + largoal +1 ,y =0)



top.mainloop()

conn.close() 