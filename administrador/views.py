from django.shortcuts import render, redirect
from django.views.generic import View

from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from .forms import VisitsForm, DeleteVisitForm, imageForm

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .autenticacion import *
from .functions import getReservationsByUser, addVisit, deleteVisitt, getReservationsByUserDay, compareQrCode

from datetime import datetime
from urllib.request import urlopen
# Create your views here.

errorMessage="""<html>
					<body>
						<h1>ERROR</h1>
					</body>
				</html>"""
#-----------------diferentes sub-webs-----------------#
class admin(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/admin.html')
		else: return HttpResponse(errorMessage)

class aVisita(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/agendVisit.html')
		else: return HttpResponse(errorMessage)

class cVisita(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/deleteVisit.html')
		else: return HttpResponse(errorMessage)

class estacionamiento(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/parking.html')
		else: return HttpResponse(errorMessage)

class agenda(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password):
			data = getReservationsByUserDay(user, password)
			print(data)
			return render(request, 'administrador/agenda.html', context = {'data': data})
		else: return HttpResponse(errorMessage)

class controlQr(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/controlVisit.html')
		else: return HttpResponse(errorMessage)
	def post(self, request, user, password):
		if autenticateUserAdmin(user, password) == False: return HttpResponse(errorMessage)
		form = imageForm(request.POST)
		if form.is_valid():
			new_task = form.save()
			dicto = model_to_dict(new_task)
			print('formulario: \n',dicto)
			with urlopen(dicto['imagen']) as response:
			    data = response.read()
			path = f"administrador/media/RECEIVED_{user}_{datetime.now()}_qr_.png"
			with open(path, "wb") as f:
			    f.write(data)
			data = compareQrCode(path, user, password)
			print(data)
			if data == 404:
				print("no coincide con ninguna :(")
				respuesta = JsonResponse({"success": False, "error": "there was an error"})
				respuesta.status_code = 403
				return respuesta
			if data!=False and 404:
				deleteVisitt(user, password, data[0])
				return JsonResponse({'form': model_to_dict(new_task)}, status=200)
			if data==False:
				respuesta = JsonResponse({"success": False, "error": "there was an error"})
				respuesta.status_code = 404
				return respuesta
		else:
			print("invalido :(")
			print(form)
			return JsonResponse({'form': 'error'})


class bitacora(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/bitacora.html')
		else: return HttpResponse(errorMessage)

class configuracion(View):
	def get(self, request, user, password):
		if autenticateUserAdmin(user, password): return render(request, 'administrador/configuracion.html')
		else: return HttpResponse(errorMessage)

#-----------------------cosas de las reservas---------------------------#
class newVisit(View):

	def get(self, request, user, password):
		form = VisitsForm()
		if autenticateUserAdmin(user, password): return render(request, 'administrador/agendVisit.html', context = {'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request, user, password):
		if autenticateUserAdmin(user, password) == False: return HttpResponse(errorMessage)

		form = VisitsForm(request.POST)

		if form.is_valid():
			new_task = form.save()
			print('formulario: \n',model_to_dict(new_task))
			addVisit(user, password, model_to_dict(new_task))
			#JsonResponse({'form': model_to_dict(new_task)}, status=200)
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		else:
			print("invalido :(")
			print(form)
			return redirect('agendVisit/')

class deleteVisit(View):

	def get(self, request, user, password):
		form = DeleteVisitForm()
		if autenticateUserAdmin(user, password):
			data = getReservationsByUser(user, password)
			print(data)
			return render(request, 'administrador/deleteVisit.html', context = {'data': data, 'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request, user, password):
		if autenticateUserAdmin(user, password) == False: return HttpResponse(errorMessage)
		form = DeleteVisitForm(request.POST)
		print(form)

		try:
			new_task = form.save()
			print('formulario: \n', model_to_dict(new_task))
			deleteVisitt(user, password, int(model_to_dict(new_task)['Number']))
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		except Exception as e:
			print("inválido :(", e)
			return HttpResponse(errorMessage)