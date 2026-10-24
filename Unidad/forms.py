from django import forms 
from .models import Oficial,Postgrado
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%d/%m/%Y'
        super().__init__(**kwargs)


class OficialForm(forms.ModelForm):
    
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento (mm/dd/yyyy)',
        widget=DateInput()
    )
    
    class Meta:
        model=Oficial
        fields=["nombre","apellido","apellido2","CI","grado","cargo","graduadoDe","escuelaProcedencia","nivel","telefono","correo","direccion","fecha_nacimiento" ]      
        
class PostgradoForm(forms.ModelForm):
    class Meta:
        model = Postgrado
        fields = [ "nombre"]        