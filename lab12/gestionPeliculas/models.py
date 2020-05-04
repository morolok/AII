from django.db import models

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='País')

    def __str__(self):
        return self.nombre


class Director(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.nombre


class Genero(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Género')

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.TextField(verbose_name='Título')
    tituloOriginal = models.TextField(verbose_name='Título original')
    pais = models.TextField(verbose_name='País')
    director = models.TextField(verbose_name='Director')
    fechaEstreno = models.DateField(verbose_name='Fecha de estreno')
    genero = models.ManyToManyField(Genero)

    def __str__(self):
        return self.titulo