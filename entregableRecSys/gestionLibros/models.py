from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Usuario(models.Model):

    def __str__(self):
        return self.id


class Libro(models.Model):
    isbn = models.IntegerField()
    titulo = models.CharField(max_length=512)
    autor = models.CharField(max_length=512)
    añoPublicacion = models.CharField(max_length=512)
    editor = models.CharField(max_length=512)
    puntuaciones = models.ManyToManyField(Usuario, through='Puntuacion')

    def __str__(self):
        return self.titulo


class Puntuacion(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    isbn = models.ForeignKey(Libro, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return str(self.isbn) + " - " + str(self.puntuacion)