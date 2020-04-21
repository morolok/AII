from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from gestionRecetas.models import Receta, Comentario
from django.conf import settings

# Create your views here.

def inicio(request):
    recetas = Receta.objects.all()
    return render(request, "inicio.html", {'recetas': recetas})

def usuarios(request):
    usuarios = User.objects.all()
    recetas = Receta.objects.all()
    return render(request, "usuarios.html", {'recetas': recetas, 'usuarios': usuarios})

def sobre(request):
    return render(request, "sobre.html")

def recetas(request):
    recetas = Receta.objects.all()
    return render(request, "recetas.html", {'recetas': recetas, 'MEDIA_URL': settings.MEDIA_URL})