from django import forms
from gestionVinos.models import Uva

class BusquedaPorUvaForm(forms.Form):
    lsUvas=[(uva.id, uva.nombre) for uva in Uva.objects.all()]
    uva = forms.ChoiceField(label="Seleccione la uva", choices=lsUvas)