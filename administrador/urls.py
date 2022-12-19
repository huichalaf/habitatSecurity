from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
	path('', admin.as_view()),
	path('agendVisit/', newVisit.as_view(), name='agendarAdmin'),
	path('deleteVisit/', deleteVisit.as_view(), name='deletevisit'),
	path('parking/', estacionamiento.as_view()),
	path('agenda/', agenda.as_view()),
	path('bitacora/', bitacora.as_view()),
	path('configuracion/', configuracion.as_view()),
	path('controlVisit/', controlQr.as_view())
]