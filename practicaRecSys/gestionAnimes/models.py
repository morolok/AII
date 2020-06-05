from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Genero(models.Model):
    nombre = models.CharField(max_length=512)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    
    def __str__(self):
        return str(self.id)


class Anime(models.Model):
    titulo = models.CharField(max_length=512)
    generos = models.ManyToManyField(Genero)
    formatoEmision = models.CharField(max_length=512)
    numeroEpisodios = models.IntegerField()

    def __str__(self):
        return self.titulo


class Puntuacion(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    idAnime = models.ForeignKey(Anime, on_delete=models.DO_NOTHING)
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.idUsuario) + " - " + str(self.idAnime) + " - " + str(self.puntuacion)