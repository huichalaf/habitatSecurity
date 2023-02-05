from django import forms
from .models import Visits, DeleteReservations

class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['Rut','Tipo','Empresa','Nombre','Apellido','Celular','FechaInicio','FechaFinal', 'HoraInicio', 'HoraFinal', 'Observaciones','Patente']
        widgets = {
        'Rut': forms.TextInput(attrs={'class': 'form-control'}),
        'Tipo': forms.TextInput(attrs={'class': 'form-control'}),
        'Empresa': forms.TextInput(attrs={'class': 'form-control'}),
        'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
        'Celular': forms.TextInput(attrs={'class': 'form-control'}),
        'FechaInicio': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'dia/mes/año hora:minuto', 'type': 'date' }),
        'FechaFinal': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'dia/mes/año hora:minuto', 'type': 'date' }),
    	'HoraInicio': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
        'HoraFinal': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
        'Celular': forms.TextInput(attrs={'class': 'form-control'}),
        'Observaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'Patente': forms.TextInput(attrs={'class': 'form-control'})
    }
class DeleteVisitFormResidente(forms.ModelForm):
    class Meta:
        model = DeleteReservations
        fields = ['Number']
        widgets = {
        'Number': forms.TextInput(attrs={'class': 'form-control'})
        }