from django.contrib import admin
from gestionRecetas.models import Receta, Comentario

# Register your models here.

admin.site.register(Receta)
admin.site.register(Comentario)