from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
from django.shortcuts import render
import gestionPeliculas.models as modelos

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
        print(ficha)
    


poblarBD()