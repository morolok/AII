from django.contrib import admin
from gestionNoticias.models import Autor, Fuente, Noticia

# Register your models here.

admin.site.register(Autor)
admin.site.register(Fuente)
admin.site.register(Noticia)