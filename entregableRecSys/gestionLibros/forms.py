from django import forms

class FormularioUsuario(forms.Form):
    id = forms.CharField(label='ID del usuario')


class FormularioLibro(forms.Form):
    isbn = forms.CharField(label='ISBN del libro')