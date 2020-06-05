from django.contrib import admin
from gestionAnimes.models import Genero, Usuario, Anime, Puntuacion

# Register your models here.

admin.site.register(Genero)
admin.site.register(Usuario)
admin.site.register(Anime)
admin.site.register(Puntuacion)