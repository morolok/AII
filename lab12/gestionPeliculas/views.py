from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from gestionPeliculas.models import Pais, Director, Genero, Pelicula
#import gestionPeliculas.models as modelos
from django.shortcuts import render, redirect

# Create your views here.


def poblarBD():

    Director.objects.all().delete()
    Pais.objects.all().delete()
    Genero.objects.all().delete()
    Pelicula.objects.all().delete()

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
        lsGeneros = []
        
        for genero in todosGeneros:
            gen, creado = Genero.objects.get_or_create(nombre = genero)
            lsGeneros.append(gen)

        Pais.objects.get_or_create(nombre = pais)
        Director.objects.get_or_create(nombre = director)
        Genero.objects.get_or_create(nombre = genero)
        pelicula = Pelicula.objects.create(titulo = titulo, tituloOriginal = tituloOriginal, pais = pais, director = director, fechaEstreno = fechaEstreno)

        for g in lsGeneros:
            pelicula.genero.add(g)


def inicio(request):
    return render(request, 'inicio.html')


def carga(request):
    contexto = {}
    if(request.method=='POST'):
        if('Aceptar' in request.POST):
            poblarBD()
            peliculas = Pelicula.objects.all()
            mensaje = 'Se han cargado ' + str(len(peliculas)) + ' películas'
            contexto['mensaje'] = mensaje
            return render(request, 'carga.html', contexto)
        else:
            return redirect('inicio')
    return render(request, "carga.html", contexto)


def pelicula(request):
    pelicula = Pelicula.objects.get(titulo = "Personal Assistant")
    print(pelicula.genero)
    contexto = {'pelicula': pelicula}
    return render(request, "pelicula.html", contexto)