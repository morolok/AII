from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Noticia(models.Model):
    titulo = models.CharField(max_length=512, verbose_name='Título')
    enlace = models.URLField(validators=[URLValidator()], verbose_name='Enlace')
    autor = models.CharField(max_length=512, verbose_name='Autor')
    fechaHora = models.DateTimeField(verbose_name='Fecha y hora')

    def __str__(self):
        return self.titulo