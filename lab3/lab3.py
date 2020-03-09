import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
from tkinter import messagebox
from datetime import datetime
import time


conexion = sqlite3.connect('diarioAS.db')

conexion.execute('''DROP TABLE IF EXISTS JORNADA;''')

conexion.execute('''CREATE TABLE JORNADA
            (JORNADA INTEGER NOT NULL,
            LOCAL TEXT NOT NULL,
            VISITANTE TEXT NOT NULL,
            GOLES_L INTEGER NOT NULL,
            GOLES_V INTEGER NOT NULL,
            LINK TEXT);''')


def extraerJornadas():
    res = []
    url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    res += s.find_all("div", class_=["cont-modulo", "resultados"])
    return res

def cargarBD():
    jornadas = extraerJornadas()
    prefijoUrl = "https://resultados.as.com"
    for jornada in jornadas:
        jorn = jornada.find("h2").find("a").text
        jornadaFinal = int(jorn.split()[1])
        resultadosPartidos = jornada.find("div", class_=["cont-resultados", "cf"]).find("table", class_="tabla-datos").find("tbody").find_all("tr")
        for partido in resultadosPartidos:
            equipoLocal = partido.find("td", class_="col-equipo-local").find("a").find("span", class_="nombre-equipo").text
            resultado = partido.find("td", class_="col-resultado").find("a").text
            golesLocal = int(resultado.split("-")[0])
            golesVisitante = int(resultado.split("-")[1])
            equipoVisitante = partido.find("td", class_="col-equipo-visitante").find("a").find("span", class_="nombre-equipo").text
            link = prefijoUrl + partido.find("td", class_="col-resultado").find("a")["href"]
            conexion.execute("INSERT INTO JORNADA (JORNADA, LOCAL, VISITANTE, GOLES_L, GOLES_V, LINK) VALUES (?, ?, ?, ?, ?, ?)", (jornadaFinal, equipoLocal, equipoVisitante, golesLocal, golesVisitante, link))
    conexion.commit()

def interfazGrafica():

    ventana = tk.Tk()
    ventana.title("Jornadas")

    bBuscarJornadas = tk.Button(ventana, text="Buscar Jornadas")
    bBuscarJornadas.place(x=0, y=0)
    bBuscarJornadas.update()
    largoBotonBuscarJornadas = bBuscarJornadas.winfo_width()

    bBuscarGoles = tk.Button(ventana, text="Buscar Goles")
    bBuscarGoles.place(x=largoBotonBuscarJornadas+1, y=0)

    ventana.mainloop()

cargarBD()
interfazGrafica()

conexion.execute('''DROP TABLE IF EXISTS JORNADA;''')
conexion.close()