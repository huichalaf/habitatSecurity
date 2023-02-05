from django import forms
from .models import Visits, DeleteReservations, imageModel

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
        'FechaInicio': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date' }),
        'FechaFinal': forms.DateInput(format={'%d/%m/%Y'},attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date' }),
        'HoraInicio': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
        'HoraFinal': forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
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