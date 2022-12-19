from django.contrib import admin
from django.urls import path, include

from .views import residente, newVisit, deleteVisit

urlpatterns = [
	path('', residente.as_view()),
	path('agendVisit/', newVisit.as_view(), name='agendar'),
	path('deleteVisit/', deleteVisit.as_view(), name='eliminar'),
]