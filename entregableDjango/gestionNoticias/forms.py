from django import forms
from gestionNoticias.models import Noticia

class BusquedaPorContenido(forms.Form):
    contenido = forms.CharField(label='Escriba una palabra', required=True)