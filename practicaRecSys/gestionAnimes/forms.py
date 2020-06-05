from django import forms
from gestionAnimes.models import Genero

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')


class GenreForm(forms.Form):
    lsGeneros = Genero.objects.all().values_list("nombre", "nombre")
    nombre = forms.MultipleChoiceField(label='Género', choices=lsGeneros)