from django.db import models
from django import forms

# Create your models here.
class Visits(models.Model):

	Rut = models.CharField(max_length=255, editable=True)
	Tipo = models.CharField(max_length=255, editable=True)
	Empresa = models.CharField(max_length=255, editable=True, blank=True)
	Nombre = models.CharField(max_length=255, editable=True)
	Apellido = models.CharField(max_length=255, editable=True)
	Celular = models.CharField(max_length=255, editable=True)
	FechaInicio = models.DateField(editable=True)
	FechaFinal = models.DateField(editable=True)
	HoraInicio = models.TimeField(editable=True)
	HoraFinal = models.TimeField(editable=True)
	Observaciones = models.CharField(max_length=255, editable=True, blank=True)
	Patente = models.CharField(max_length=8, editable=True, blank=True)
	
	def __str__(self):
		return self.user

class DeleteReservations(models.Model):#
	
	Number = models.CharField(db_column = 'Number',max_length=3, editable=True)
	
	def __str__(self):
		return self.Number