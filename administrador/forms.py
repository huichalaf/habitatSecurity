from django import forms
from .models import Visits, DeleteReservations, imageModel

class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['Rut','Tipo','Nombre','Apellido','Celular','FechaInicio','FechaFinal','Observaciones','Patente']
        widgets = {
        'Rut': forms.TextInput(attrs={'class': 'form-control'}),
        'Tipo': forms.TextInput(attrs={'class': 'form-control'}),
        'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
        'Celular': forms.TextInput(attrs={'class': 'form-control'}),
        'FechaInicio': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date' }),
        'FechaFinal': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date' }),
    	'Celular': forms.TextInput(attrs={'class': 'form-control'}),
        'Observaciones': forms.TextInput(attrs={'class': 'form-control'}),
        'Patente': forms.TextInput(attrs={'class': 'form-control'})
    }

class DeleteVisitForm(forms.ModelForm):
    class Meta:
        model = DeleteReservations
        fields = ['Number']
        widgets = {
        'Number': forms.TextInput(attrs={'class': 'form-control'})
        }

class imageForm(forms.ModelForm):
    class Meta:
        model = imageModel
        fields = ['imagen']
        widgets={
            'imagen': forms.TextInput(attrs={'class': 'form-control'})
        }