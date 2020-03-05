#encoding:utf-8
import tkinter as tk
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
import tkinter
from datetime import datetime
import time





    # Cargamos y almacenamos los datos de la pagina web 

conn = sqlite3.connect('noticias.db')

conn.execute("DROP TABLE IF EXISTS NOTICIAS") 
conn.execute('''CREATE TABLE NOTICIAS
    (TITULO       TEXT NOT NULL,
    LINK          TEXT    NOT NULL,
    AUTOR      TEXT    NOT NULL,
    FECHA       TEXT);''')
print("Table created succesfully")



def extraernoticias():
    l=[]
    url= "https://www.meneame.net/?page="
    for i in range(1,4):
        url1 = url + str(i) 
        f = urllib.request.urlopen(url1)
        s = BeautifulSoup(f,"lxml")
        l += s.find_all("div", class_= ["center-content","no-padding"])
    return l





def almacenar_bd():
    conn.text_factory=str
    l = extraernoticias()
    for x in l:
      titulo = x.find("h2").text
      link = x.find("h2").find("a")['href']
      autor = x.find("div", class_= "news-submitted").find_all("a")[1].text
      fecha = x.find_all("span", class_= ["ts","visible"])[1]["data-ts"]
      conn.execute("INSERT INTO NOTICIAS (TITULO,LINK,AUTOR,FECHA) VALUES (?, ?, ?, ?)", (titulo, link,autor, fecha))
    conn.commit()




#Este metodo nos permite mostrar cada una de las noticias almacenadas en la  base de datos
def mostrar_noticias():
    muestra = tk.Tk();
    #Esto nos permitira ver las noticias almacenadas en la base de datos
    muestra.title("Elementos Base de Datos")
    noticias = conn.execute("SELECT TITULO,AUTOR,FECHA FROM NOTICIAS;")
    subventana = tk.Frame(muestra)
    subventana.pack() 
    boxMostrar= tk.Listbox(subventana, width = 150, height = 20)
    scroll = tk.Scrollbar(subventana,orient ="vertical")
    scroll.pack(side ="right",fill ="y")
    scroll.config(command=boxMostrar.yview)
    boxMostrar.config(yscrollcommand=scroll.set)
    cont = 1
    for j in noticias:
        titulo = j[0]
        autor =  j[1]
        fecha =  j[2]
        fechaformateada = datetime.fromtimestamp(int(fecha))
        cadena = titulo + " " + autor + " " + str(fechaformateada)
        boxMostrar.insert(cont,cadena)
        cont += 1
    boxMostrar.pack()
    muestra.mainloop()

#Con este metodo podemos cerrar la ventana que muestra las noticias

def cierra_ventana(cierre):
    cierre.destroy()


def busquedaporAutor():
    ventanabusqAutor=tk.Tk()
    ventanabusqAutor.title("Busqueda por autor")
    noticias = conn.execute("SELECT TITULO,AUTOR,FECHA FROM NOTICIAS;")
    autores = list({i[1] for i in noticias})
    ventanaSpinbox = tk.Spinbox(ventanabusqAutor, values = autores)
    ventanaSpinbox.place(x=0,y=0)
    ventanaSpinbox.update()
    ventanaSpinbox.pack()
    #Creamos una función auxiliar que nos permita  buscar las noticias asociadas al autor
    def obtennoticias_Autor():
        conn.text_factory=str
        muestra =tk.Tk()
        muestra.title("Noticias asociadas al autor")
        autor_sel = ventanaSpinbox.get()
        subventana = tk.Frame(muestra)
        subventana.pack()
        mostListbox=tk.Listbox(subventana, width=150, height = 20)
        autorBuscado = "%" + autor_sel + "%"
        noticias_asociadas = conn.execute("SELECT TITULO,AUTOR,FECHA FROM NOTICIAS WHERE AUTOR LIKE ? " , (autorBuscado,))
        scroll = tk.Scrollbar(subventana,orient= "vertical")
        scroll.pack(side="right" , fill="y")
        scroll.config(command=mostListbox.yview)
        mostListbox.config(yscrollcommand=scroll.set)
        cont=1
        for j in noticias_asociadas:
            titulo = j[0]
            autor =  j[1]
            fecha =  j[2]
            fechaformateada = datetime.fromtimestamp(int(fecha))
            cadena = titulo + " " + autor + " " + str(fechaformateada)
            mostListbox.insert(cont,cadena)
            cont += 1
        mostListbox.pack()
        muestra.mainloop()
    largSpinbox = ventanaSpinbox.winfo_width()
    botonBuscar = tk.Button(ventanabusqAutor,text="Buscar",command = obtennoticias_Autor)
    botonBuscar.place(x= 7*largSpinbox, y=0)
        
    
#Método Buscar fecha
def buscarFecha():
    ventanaBuscarFecha = tk.Tk()
    ventanaBuscarFecha.title("Buscar noticias por fecha")
    tk.Label(ventanaBuscarFecha, text="Introduzca la fecha dd/mm/aaaa").grid(row=0)
    entradaFecha = tk.Entry(ventanaBuscarFecha)
    entradaFecha.grid(row=0, column=1)
    def metodoBuscar():
        muestra = tk.Tk()
        muestra.title("Noticias a partir de la fecha")
        subventana = tk.Frame(muestra)
        subventana.pack()
        listboxMostrar = tk.Listbox(subventana, width=150, height=20)
        barraScroll = tk.Scrollbar(subventana, orient="vertical")
        barraScroll.pack(side="right", fill="y")
        barraScroll.config(command=listboxMostrar.yview)
        listboxMostrar.config(yscrollcommand=barraScroll.set)
        fechaABuscar = entradaFecha.get()
        fechaFormateada = str(time.mktime(datetime.strptime(fechaABuscar, "%d/%m/%Y").timetuple()))
        conexionBuscarFecha = sqlite3.connect('noticias.db')
        conexionBuscarFecha.text_factory = str
        noticiasBuscadas = conexionBuscarFecha.execute("SELECT TITULO, NOMBRE_AUTOR, FECHA FROM NOTICIA;")
        contador = 1
        for n in noticiasBuscadas:
            if (float(n[2]) > float(fechaFormateada)):
                titulo = n[0]
                nombre_autor = n[1]
                fecha = n[2]
                fechaForm = datetime.fromtimestamp(int(fecha))
                texto = titulo + " " + nombre_autor + " " + str(fechaForm)
                listboxMostrar.insert(contador, texto)
                contador += 1
        listboxMostrar.pack()
        muestra.mainloop()
    
    entradaFecha.bind("<Return>", metodoBuscar)
    ventanaBuscarFecha.mainloop()


#Creación Interfaz gráfica

top = tkinter.Tk()

# Creamos la barra del menu
barmenu = tk.Menu(top)
top.title( "Practica 1")

# Creamos  los subapartados de Buscar
filemenu = tk.Menu(barmenu, tearoff = 0)
filemenu.add_command(label="Cargar" ,command = almacenar_bd)
filemenu.add_command(label = "Mostrar",command = mostrar_noticias)
filemenu.add_command(label = "Salir", command = lambda: cierra_ventana(top))

#Creamos el bot�n Buscar
barmenu.add_cascade(label = "Datos", menu = filemenu)

filemenu.add_separator()


findmenu = tk.Menu(barmenu, tearoff = 0)

findmenu.add_command(label="Autor",command = busquedaporAutor)
findmenu.add_command(label = "Fecha", command = buscarFecha)

barmenu.add_cascade(label = "Buscar", menu = findmenu)

#Permite añadir el menú a la ventana , abrimos la interfaz y cerramos la conexión
top.config(menu= barmenu)
top.mainloop()

conn.close()

