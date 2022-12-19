from django.db import models
from django import forms

# Create your models here.

class Users(models.Model):

	user = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.user