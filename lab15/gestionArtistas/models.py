from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator

# Create your models here.


class Usuario(models.Model):

    def __str__(self):
        return self.id


class Artista(models.Model):
    nombre = models.CharField(max_length=512, verbose_name='Nombre')
    url = models.URLField(validators=[URLValidator()])
    pictureUrl = models.URLField(validators=[URLValidator()])

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    tagValue = models.CharField(max_length=512, verbose_name='TagValue')

    def __str__(self):
        return self.tagValue


class UsuarioArtista(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idArtista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    tiempoEscucha = models.IntegerField(verbose_name='TiempoEscucha')

    def __str__(self):
        return self.idUsuario + " - " + self.idArtista + " - " + str(self.tiempoEscucha)


class UsuarioEtiquetaArtista(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idArtista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    idTag = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    dia = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    mes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    año  = models.IntegerField(max_length=4, verbose_name='Año')

    def __str__(self):
        return self.idUsuario + " - " + self.idArtista + " - " + self.idTag