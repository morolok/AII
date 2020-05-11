from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from django.shortcuts import render, redirect
from gestionVinos.models import Bodega, Denominacion, Uva, Vino
from gestionVinos.forms import BusquedaPorUvaForm
from django.db.models import Count

# Create your views here.


def poblarBD():

    Bodega.objects.all().delete()
    Denominacion.objects.all().delete()
    Uva.objects.all().delete()
    Vino.objects.all().delete()

    vinos = []
    cursor = ["0", "24"]
    for i in cursor:
        url = "https://www.vinissimus.com/es/vinos/tinto/?cursor=" + i
        fichero = urllib.request.urlopen(url)
        s = BeautifulSoup(fichero, "lxml")
        vinos += s.find_all("div", class_=["product-list-item", "large with-badges"])
    
    raizUrl = "https://www.vinissimus.com"
    for vino in vinos:
        enlace = vino.find("div", class_="info").find("div", class_="details").find("a")["href"].strip()
        link = raizUrl + enlace
        fichero = urllib.request.urlopen(link)
        s = BeautifulSoup(fichero, "lxml")
        bodega = s.find("div", class_="cellar").find("a").text.strip()
        nombreVino = vino.find("div", class_="info").find("div", class_="details").find("a")["title"].strip()
        precio = vino.find("div", class_=["quantity-widget", "small"]).find("p").text.strip()
        denominacion = vino.find("div", class_="info").find("div", class_="details").find("div", class_="region").text.strip()
        uvas = vino.find("div", class_="info").find("div", class_="details").find("div", class_="tags").text.strip().split("/")
        if(vino.find("div", class_="info").find("div", class_="badges") is None):
            estrellas = None
        else:
            estrellas = vino.find("div", class_="info").find("div", class_="badges").find("span", class_=["badge", "small", "opinion-badge"]).find("span", class_=["opinion-star"])
            if(estrellas is None):
                estrellas = None
            else:
                estrellas = float(vino.find("div", class_="info").find("div", class_="badges").find("span", class_=["badge", "small", "opinion-badge"]).text.strip()[1:])
            
        Bodega.objects.get_or_create(nombre = bodega)
        Denominacion.objects.get_or_create(nombre = denominacion)
        
        lsUvas = []
        for uva in uvas:
            nombreUva = uva.strip()
            uvaBD, creada = Uva.objects.get_or_create(nombre = nombreUva)
            lsUvas.append(uvaBD)
        
        vinoBD = Vino.objects.create(nombre = nombreVino, precio = precio, bodega = bodega, denominacion = denominacion, estrellas = estrellas)

        for uva in lsUvas:
            vinoBD.uvas.add(uva)


def inicio(request):
    numVinos = Vino.objects.all().count()
    contexto = {'numVinos': numVinos}
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
    numBodegas = Bodega.objects.all().count()
    numDenominaciones = Denominacion.objects.all().count()
    numUvas = Uva.objects.all().count()
    numVinos = Vino.objects.all().count()
    mensaje = "Se han cargado " + str(numBodegas) + " bodegas, " + str(numDenominaciones) + " denominaciones, " + str(numUvas) + " uvas y " + str(numVinos) + " vinos."
    contexto = {'mensaje': mensaje}
    return render(request, "exitoCargaBD.html", contexto)


def listaDeVinos(request):
    vinos = Vino.objects.all()
    contexto = {'vinos': vinos}
    return render(request, "listaDeVinos.html", contexto)


def vinosMejorPuntuados(request):
    vinos = Vino.objects.all().order_by('estrellas').reverse()[0:3]
    contexto = {'vinos': vinos}
    return render(request, "vinosMejorPuntuados.html", contexto)


def buscarPorUva(request):
    formulario = BusquedaPorUvaForm()
    vinos = None
    if request.method=='POST':
        formulario = BusquedaPorUvaForm(request.POST)      
        if formulario.is_valid():
            uva = Uva.objects.get(id=formulario.cleaned_data['uva'])
            vinos = uva.vino_set.all()
    contexto = {'formulario': formulario, 'vinos': vinos}
    return render(request, "buscarPorUva.html", contexto)


def vinosAgrupadosPorDenominacion(request):
    denominaciones = Denominacion.objects.all()
    denomacionVinos = {}
    for denominacion in denominaciones:
        lsVinos = []
        vinos = Vino.objects.filter(denominacion=denominacion)
        sumaPrecio = 0.0
        for vino in vinos:
            lsVinos.append([vino.nombre, vino.bodega, vino.precio])
            precio = float(vino.precio.split(" ")[0].replace(",","."))
            sumaPrecio += precio
        mediaPrecio = round(sumaPrecio/(len(lsVinos)), 2)
        denomacionVinos[denominacion] = [lsVinos, mediaPrecio]
    contexto = {'denomacionVinos': denomacionVinos}
    return render(request, "vinosAgrupadosPorDenominacion.html", contexto)


def mejorBodega(request):
    bodegas = Bodega.objects.all()
    bodegaRelacion = {}
    for bodega in bodegas:
        lsEstrellasPrecio = []
        lsVinos = []
        vinos = Vino.objects.filter(bodega=bodega)
        sumaEstrellas = 0.0
        sumaPrecio = 0.0
        for vino in vinos:
            estrellas = vino.estrellas
            if(estrellas is not None):
                precio = float(vino.precio.split(" ")[0].replace(",","."))
                estrellas = float(estrellas)
                sumaPrecio += precio
                sumaEstrellas += estrellas
                lsVinos.append(vino)
        if(len(lsVinos) != 0):
            mediaPrecio = round(sumaPrecio/(len(lsVinos)), 2)
            mediaEstrellas = round(sumaEstrellas/(len(lsVinos)), 2)
            relacionCalidadPrecio = round(mediaEstrellas/mediaPrecio, 2)
            bodegaRelacion[bodega] = relacionCalidadPrecio
    maximaRelacion = 0.0
    mejorBodega = None
    for bodega, relacionCalidadPrecio in bodegaRelacion.items():
        if(relacionCalidadPrecio > maximaRelacion):
            mejorBodega = bodega
            maximaRelacion = relacionCalidadPrecio
    contexto = {'maximaRelacion': maximaRelacion, 'mejorBodega': mejorBodega}
    return render(request, "mejorBodega.html", contexto)








