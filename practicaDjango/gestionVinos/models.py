from django.db import models

# Create your models here.

class Bodega(models.Model):
    nombre = models.CharField(max_length=1024, verbose_name='Nombre')

    def __str__(self):
        return self.nombre


class Denominacion(models.Model):
    nombre = models.CharField(max_length=1024, verbose_name='Nombre')

    def __str__(self):
        return self.nombre


class Uva(models.Model):
    nombre = models.CharField(max_length=1024, verbose_name='Nombre')

    def __str__(self):
        return self.nombre


class Vino(models.Model):
    nombre = models.CharField(max_length=1024, verbose_name='Nombre')
    precio = models.CharField(max_length=1024, verbose_name='Precio')
    bodega = models.TextField(verbose_name='Bodega')
    denominacion = models.TextField(verbose_name='Denomicación de origen')
    uvas = models.ManyToManyField(Uva)
    estrellas = models.DecimalField(max_digits=10,decimal_places=1, null=True, verbose_name='Estrellas')


    def __str__(self):
        return self.nombre