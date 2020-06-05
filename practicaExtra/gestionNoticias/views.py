from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from django.shortcuts import render
from gestionNoticias.models import Noticia
from gestionNoticias.forms import FormularioTitulo


def poblarBD():
    Noticia.objects.all().delete()
    noticias = []
    lsNoticias = []
    url = "https://as.com/"
    fichero = urllib.request.urlopen(url)
    s = BeautifulSoup(fichero, "lxml")
    noticias += s.find("div", class_=["container content home"]).find_all("article", class_=["cf"])
    
    for n in noticias:
        titulo = None
        tituloNoticia = n.find("h2", class_=["title"])
        if(tituloNoticia is None):
            tituloNoticia = n.find("h3", class_=["title"])
            if(tituloNoticia is None):
                titulo = n.find("h4", class_=["title"]).text.strip()
            else:
                titulo = n.find("h3", class_=["title"]).find("a").text.strip()
        else:
            titulo = n.find("h2", class_=["title"]).find("a").text.strip()
        
        enlace = n.find("a")["href"].strip()
        
        autor = None
        autorNoticia = n.find("span", class_=["autor-nombre"])
        if(autorNoticia is None):
            pass
        else:
            autorNoticia = n.find("span", class_=["autor-nombre"]).find("a", class_=["nom"])
            if(autorNoticia is None):
                autor = n.find("span", class_=["autor-nombre"]).text.strip()
            else:
                autor = n.find("span", class_=["autor-nombre"]).find("a", class_=["nom"]).text.strip()
        
        fechaHora = None
        if ((n.find("span", class_=["fecha"]) is None) or (n.find("span", class_=["hora"]) is None)):
            pass
        else:
            fechaNoticia = n.find("span", class_=["fecha"]).text.strip()
            campos = fechaNoticia.split("/")
            if(len(campos[0])==4):
                fechaNoticia = campos[2] + "/" + campos[1] + "/" + campos[0]
            horaNoticia = n.find("span", class_=["hora"]).text.strip()
        fechaHoraNoticia = fechaNoticia + " " + horaNoticia
        fechaHora = datetime.strptime(fechaHoraNoticia, "%d/%m/%Y %H:%M")
        if((titulo is None) or (enlace is None) or (autor is None) or (fechaHora is None)):
            pass
        else:
            noticia = Noticia(titulo=titulo, enlace=enlace, autor=autor, fechaHora=fechaHora)
            lsNoticias.append(noticia)

    Noticia.objects.bulk_create(lsNoticias)


# Create your views here.


def inicio(request):
    return render(request, 'inicio.html')


def almacenar(request):
    poblarBD()
    numNoticias = str(Noticia.objects.all().count())
    mensaje = "Se han cargado un total de " + numNoticias + " noticias."
    contexto = {'mensaje': mensaje}
    return render(request, 'almacenar.html', contexto)


def mostrar(request):
    noticias = Noticia.objects.all()
    contexto = {'noticias': noticias}
    return render(request, 'mostrar.html', contexto)


def buscar(request):
    if request.method=='GET':
        form = FormularioTitulo(request.GET, request.FILES)
        if(form.is_valid()):
            palabra = form.cleaned_data['palabra']
            noticias = Noticia.objects.filter(titulo__contains=palabra)
            contexto = {'noticias': noticias, 'palabra': palabra}
            return render(request, 'noticiasEncontradas.html', contexto)
    form = FormularioTitulo()
    contexto = {'form': form}
    return render(request, 'buscar.html', contexto)



