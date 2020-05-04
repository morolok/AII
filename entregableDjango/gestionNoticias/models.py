from django.db import models

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=256, verbose_name='Nombre')

    def __str__(self):
        return self.nombre

class Fuente(models.Model):
    nombre = models.CharField(max_length=256, verbose_name='Nombre')

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=256, verbose_name='Título')
    autor = models.CharField(max_length=256, verbose_name='Autor')
    fuenteNoticia = models.CharField(max_length=256, null=True, verbose_name='Fuente')
    fechaYHora = models.DateTimeField(verbose_name='Fecha y hora')
    contenido = models.TextField(verbose_name='Contenido')
    numeroComentario = models.IntegerField(verbose_name='Número de comentarios')

    def __str__(self):
        return self.titulo