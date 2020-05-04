from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from django.shortcuts import render, redirect
from gestionNoticias.models import Autor, Fuente, Noticia
from gestionNoticias.forms import BusquedaPorContenido

# Create your views here.

def poblarBD():
    noticias = []
    url="https://www.meneame.net/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    noticias += s.find_all("div", class_=["news-body"])

    Autor.objects.all().delete()
    Fuente.objects.all().delete()
    Noticia.objects.all().delete()
    
    for n in noticias:
        posibleFuente = n.find("div", class_=["center-content"]).find("div", class_="news-submitted").find("span", class_="showmytitle")
        fechas = n.find_all("span", class_=["ts","visible"])
        
        if ((posibleFuente is not None) and (len(fechas)>1)):
            titulo = n.find("h2").text.strip()
            autor = n.find("div", class_="news-submitted").find_all("a")[1].text.strip()
            fuente = posibleFuente.text.strip()
            fecha = n.find_all("span", class_=["ts","visible"])[1]["data-ts"]
            fechaFormateada = datetime.fromtimestamp(int(fecha)).strftime("%Y-%m-%d %H:%M")
            contenido = n.find("div", class_="news-content").text.strip()
            numeroComentarios = n.find("div", class_=["news-details"]).find("div", class_=["news-details-main"]).find("a", class_=["comments"])["data-comments-number"]
            Autor.objects.create(nombre = autor)
            Fuente.objects.create(nombre = fuente)
            Noticia.objects.create(titulo = titulo, autor = autor, fuenteNoticia = fuente, fechaYHora = fechaFormateada, contenido = contenido, numeroComentario = numeroComentarios)
        
        elif((posibleFuente is None) and (len(fechas)>1)):
            titulo = n.find("h2").text.strip()
            autor = n.find("div", class_="news-submitted").find_all("a")[1].text.strip()
            fecha = n.find_all("span", class_=["ts","visible"])[1]["data-ts"]
            fechaFormateada = datetime.fromtimestamp(int(fecha)).strftime("%d/%m/%Y, %H:%M:%S")
            contenido = n.find("div", class_="news-content").text.strip()
            numeroComentarios = n.find("div", class_=["news-details"]).find("div", class_=["news-details-main"]).find("a", class_=["comments"])["data-comments-number"]
            Autor.objects.create(nombre = autor)
            Fuente.objects.create(nombre = fuente)
            Noticia.objects.create(titulo = titulo, autor = autor, fechaYHora = fechaFormateada, contenido = contenido, numeroComentario = numeroComentarios)


def inicio(request):
    numNoticias = Noticia.objects.all().count()
    contexto = {'numNoticias': numNoticias}
    return render(request, "inicio.html", contexto)


def carga(request):

    if(request.method == 'POST'):
        if 'Aceptar' in request.POST:
            poblarBD()
            return redirect('exitoCargaBD')
        else:
            return redirect("/")

    return render(request, "carga.html")


def exitoCargaBD(request):
    numAutores = Autor.objects.all().count()
    numFuentes = Fuente.objects.all().count()
    numNoticias = Noticia.objects.all().count()
    mensaje = "Se han cargado " + str(numNoticias) + " noticias, " + str(numFuentes) + " fuentes y " + str(numAutores) + " autores."
    contexto = {'mensaje': mensaje}
    return render(request, "exitoCargaBD.html", contexto)


def listaDeNoticias(request):
    noticias = Noticia.objects.all()
    contexto = {'noticias': noticias}
    return render(request, "listaDeNoticias.html", contexto)


def noticiasMasComentadas(request):
    noticias = Noticia.objects.all().order_by('numeroComentario').reverse()[0:5]
    contexto = {'noticias': noticias}
    return render(request, "noticiasMasComentadas.html", contexto)


def busquedaNoticiaPorContenido(request):
    formulario = BusquedaPorContenido()
    contexto = {'formulario': formulario}

    if(request.method == 'POST'):
        formulario = BusquedaPorContenido(request.POST)
        if(formulario.is_valid()):
            contenido = formulario.cleaned_data.get('contenido')
            noticias = Noticia.objects.filter(contenido__icontains=contenido)
            contexto['palabra'] = contenido
            contexto['noticias'] = noticias
            formulario = BusquedaPorContenido()

    return render(request, "busquedaNoticiaPorContenido.html", contexto)