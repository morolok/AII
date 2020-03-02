import tkinter as tk
from bs4 import BeautifulSoup
import urllib.request
import sqlite3

conexion = sqlite3.connect('jornadasAS.db')

TEMPORADA = "2018_2019"

def extraer_jornadas():
    url = "https://resultados.as.com/resultados/futbol/primera/"+TEMPORADA+"/calendario/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    ls = s.find_all("div", class_=["cont-modulo","resultados"])
    return ls

print(extraer_jornadas())

# Ventana gráfica

ventana = tk.Tk()

bAlmacenarResultados = tk.Button(ventana, text="Almacenar Resultados")
bAlmacenarResultados.place(x=0, y=0)
bAlmacenarResultados.update()
largoAlmacenar = bAlmacenarResultados.winfo_width()

bListarJornadas = tk.Button(ventana, text="Listar Jornadas")
bListarJornadas.place(x=largoAlmacenar+1, y=0)

ventana.mainloop()

conexion.close()