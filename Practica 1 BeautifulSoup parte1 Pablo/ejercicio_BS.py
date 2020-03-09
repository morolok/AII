import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox



#Creacion Base de Datos
conexion = sqlite3.connect('basedatos.db')

conexion.execute('''DROP TABLE IF EXISTS LIGA;''')

conexion.execute('''CREATE TABLE LIGA
         (JORNADA INTEGER     NOT NULL,
         EQLOCAL           TEXT    NOT NULL,
         EQVISITANTE        TEXT NOT NULL,
         GOLESlOCAL         INTEGER NOT NULL,
         GOLESVISITANTE         INTEGER NOT NULL,
         LINK               TEXT);''')
print("Table created succesfully")





#BeatifulSoup
def extrae_jornadas():
    res = []
    url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"  
    fichero = urllib.request.urlopen(url)
    result = BeautifulSoup(fichero,"lxml")
    res += result.find_all("div", class_= ["cont-modulo","resultados"])
    return res



def almacena_bd():
    #Obtenemos la  lista con las jornadas
    lista = extrae_jornadas()
    url = "https://resultados.as.com"
    for x in lista:
        jorn = x.find("h2").find("a").text
        jornfinal = int(jorn.split()[1])
        resulPar = x.find("div",class_=["cont-resultados","cf"]).find("table", class_="tabla-datos").find("tbody").find_all("tr")
        for partido in resulPar:
            equipoLocal = partido.find("td", class_="col-equipo-local").find("a").find("span", class_="nombre-equipo").text
            resultado = partido.find("td", class_="col-resultado").find("a").text
            golesLocal = int(resultado.split("-")[0])
            golesVisitante = int(resultado.split("-")[1])
            equipoVisitante = partido.find("td", class_="col-equipo-visitante").find("a").find("span", class_="nombre-equipo").text
            link = url + partido.find("td", class_="col-resultado").find("a")["href"]
            conexion.execute("INSERT INTO LIGA (JORNADA, EQLOCAL,EQVISITANTE,GOLESLOCAL,GOLESVISITANTE,LINK) VALUES (?, ?, ?, ?, ?, ?)", (jornfinal, equipoLocal, equipoVisitante, golesLocal, golesVisitante, link))
    conexion.commit()
    cursor = conexion.execute("SELECT COUNT(*) FROM LIGA")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conexion.close()



def listar_bd():
    conexion = sqlite3.connect('basedatos.db')
    conexion.text_factory = str  
    cursor = conexion.execute("SELECT * FROM LIGA ORDER BY JORNADA")
    imprimir_lista(cursor)
    conexion.close()
                                               

def imprimir_lista(cursor):
    v = Toplevel()
    v.title("TEMPORADA "+"2018_2019")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    jornada=0
    for row in cursor:
        if row[0] != jornada:
            jornada=row[0]
            lb.insert(END,"\n")
            s = 'JORNADA '+ str(jornada)
            lb.insert(END,s)
            lb.insert(END,"-----------------------------------------------------")
        s = "     " + row[1] +' '+ str(row[3]) +'-'+ str(row[4]) +' '+  row[2]
        lb.insert(END,s)
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

#Creacion interfaz  



top = tk.Tk()    

A = tk.Button(top,text ="Almacenar_Resultados",command = almacena_bd)
A.place(x = 0,y = 0)
A.update()
largoal= A.winfo_width()


B = tk.Button(top,text ="Listar_Jornadas",command = listar_bd)
B.place(x =largoal+1,y =0)
B.update()
largoLj = B.winfo_width()


top.mainloop()

