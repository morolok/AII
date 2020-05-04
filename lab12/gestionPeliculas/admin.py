from django.contrib import admin
from gestionPeliculas.models import Pais, Director, Genero, Pelicula

# Register your models here.

admin.site.register(Pais)
admin.site.register(Director)
admin.site.register(Genero)
admin.site.register(Pelicula)