from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from gestionPeliculas.models import Pais, Director, Genero, Pelicula
#import gestionPeliculas.models as modelos
from django.shortcuts import render

# Create your views here.


def poblarBD():
    url = "https://www.elseptimoarte.net/estrenos/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    aux = s.find("ul", class_="elements").find_all("li")
    enlaces = []
    
    for p in aux:
        enlace = "https://www.elseptimoarte.net" + p.find("h3").find("a")["href"]
        enlace = enlace.replace(" ", "%20")
        enlaces.append(enlace)
    
    for link in enlaces:
        fichero = urllib.request.urlopen(link)
        s = BeautifulSoup(fichero, "lxml")
        ficha = s.find("section", class_="highlight").find("div").find("dl").find_all()

        titulo = ""
        tituloOriginal = ""
        pais = ""
        director = ""

        for i in range(0, len(ficha)):
            elemento = ficha[i]
            if(elemento.text.strip() == "Título"):
                titulo = ficha[i+1].text.strip()
            if(elemento.text.strip() == "Título original"):
                tituloOriginal = ficha[i+1].text.strip().replace("#", "")
            if(elemento.text.strip() == "País"):
                todosPaises = ficha[i+1].find_all("a")
                if(len(todosPaises) > 0):
                    pais = todosPaises[0].text.strip()
                else:
                    pais = ficha[i+1].text.strip()
            if(elemento.text.strip() == "Director"):
                todosDirectores = ficha[i+1].find_all("a")
                if(len(todosDirectores) > 0):
                    director = todosDirectores[0].text.strip()
                else:
                    director = ficha[i+1].text.strip()
            if(elemento.text.strip() == "Estreno en España"):
                auxFecha = ficha[i+1].text.strip()
                fechaEstreno = datetime.strptime(auxFecha, '%d/%m/%Y')
    
        lsGeneros = s.find("p", class_="categorias").find_all("a")
        todosGeneros = [lsGeneros[i].text.strip() for i in range(0, len(lsGeneros))]
        
        for genero in todosGeneros:
            Genero.objects.create(nombre = genero)

        Pais.objects.create(nombre = pais)
        Director.objects.create(nombre = director)
        Genero.objects.create(nombre = genero)
        pelicula = Pelicula.objects.create(titulo = titulo, tituloOriginal = tituloOriginal, pais = pais, director = director, fechaEstreno = fechaEstreno)

        for genero in todosGeneros:
            pelicula.genero.add(genero)


def inicio(request):
    return render(request, 'inicio.html')