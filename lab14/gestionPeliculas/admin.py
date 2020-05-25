from django.contrib import admin
from gestionPeliculas.models import Occupation, Genre, UserInformation, Film, Rating

# Register your models here.

admin.site.register(Occupation)
admin.site.register(Genre)
admin.site.register(UserInformation)
admin.site.register(Film)
admin.site.register(Rating)