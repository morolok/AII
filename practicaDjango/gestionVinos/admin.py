from django.contrib import admin
from gestionVinos.models import Bodega, Denominacion, Uva, Vino

# Register your models here.

admin.site.register(Bodega)
admin.site.register(Denominacion)
admin.site.register(Uva)
admin.site.register(Vino)