from unittest.util import _MAX_LENGTH
from django.db import models
from django import forms

# Create your models here.

class Visits(models.Model):

	Rut = models.CharField(max_length=255, editable=True)
	Tipo = models.CharField(max_length=255, editable=True)
	Nombre = models.CharField(max_length=255, editable=True)
	Apellido = models.CharField(max_length=255, editable=True)
	Celular = models.CharField(max_length=255, editable=True)
	FechaInicio = models.DateField(editable=True)
	FechaFinal = models.DateField(editable=True)
	Observaciones = models.CharField(max_length=255, editable=True)
	Patente = models.CharField(max_length=8, editable=True)
	
	def __str__(self):
		return self.user

class DeleteReservations(models.Model):
	
	Number = models.CharField(db_column = 'Number',max_length=3, editable=True)
	
	def __str__(self):
		return self.Number

class imageModel(models.Model):

	imagen = models.TextField(max_length=15000, editable=True)
	def __str__(self):
		return self.imagen
