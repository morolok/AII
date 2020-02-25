import tkinter
import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import urllib.request
import os.path
from nt import link

conection = sqlite3.connect('test.db')

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
        print("Error al conectarse a la pagina")
        return None

def almacenar():
    conection.execute("DROP TABLE IF EXISTS NOTICIA")
    print("Opened database successfully");

    conection.execute('''CREATE TABLE NOTICIA
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         DATE            TEXT     NOT NULL,
         LINK         TEXT        NOT NULL);''')

    print("Table created successfully");

    lista_noticias = abrir_url("https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml", "noticias.txt")
    listN = extraer_lista(lista_noticias)
    for i in range(len(listN)):
        noticia = listN[i]
        nombre_not = noticia[0]
        link_not = noticia[1]
        date_not = noticia[2]
        conection.execute("INSERT INTO NOTICIA(ID,NAME,DATE,LINK) VALUES (?,?,?,?)", (i,nombre_not,date_not, link_not))
    
    conection.commit()
    msg = messagebox.showinfo("Informacion BD", "BD creada correctamente")
    
def listar():
    elementosBD = conection.execute("SELECT ID, NAME, DATE, LINK FROM NOTICIA")
    cadenaListar = ""
    for fila in elementosBD:
        nombre = fila[1]
        link = fila[2]
        fecha = fila[3]
        cadenaListar += nombre + "\n" + link + "\n" + fecha + "\n\n"
    msg = messagebox.showinfo("Elementos BD", cadenaListar)

top = tkinter.Tk()

ButtonAlm = tk.Button(top, text = "Almacenar", command = almacenar)
ButtonList = tk.Button(top, text = "Listar", command = listar)
ButtonBusc = tk.Button(top, text = "Buscar")

ButtonAlm.place(x = 0,y = 0)
ButtonList.place(x = 70,y = 0)
ButtonBusc.place(x = 110,y = 0)

top.mainloop()

conection.execute('''DROP TABLE NOTICIA;''')
conection.close()


