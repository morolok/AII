"""practicaDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import gestionVinos.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('carga/', views.carga, name='carga'),
    path('exitoCargaBD/', views.exitoCargaBD, name='exitoCargaBD'),
    path('listaDeVinos/', views.listaDeVinos, name='listaDeVinos'),
    path('vinosMejorPuntuados/', views.vinosMejorPuntuados, name='vinosMejorPuntuados'),
    path('buscarPorUva/', views.buscarPorUva, name='buscarPorUva'),
    path('vinosAgrupadosPorDenominacion/', views.vinosAgrupadosPorDenominacion, name='vinosAgrupadosPorDenominacion'),
    path('mejorBodega/', views.mejorBodega, name='mejorBodega'),
]
