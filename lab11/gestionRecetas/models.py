from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Receta(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    ingredientes = models.TextField(help_text='Redacta los ingredientes')
    preparacion = models.TextField(verbose_name='Preparacion')
    imagen = models.ImageField(upload_to='imagenes', verbose_name='Imagen')
    fecha_hora_registro = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto