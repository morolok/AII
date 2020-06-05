from django import forms


class FormularioTitulo(forms.Form):
    palabra = forms.CharField(label='Palabra que desea buscar en el título')