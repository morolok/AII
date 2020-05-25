from django.contrib import admin
from gestionLibros.models import Usuario, Libro, Puntuacion

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Libro)
admin.site.register(Puntuacion)