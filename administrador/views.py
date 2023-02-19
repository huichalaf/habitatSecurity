from django.shortcuts import render, redirect
from django.views.generic import View

from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from .forms import VisitsForm, DeleteVisitForm, imageForm
from .functions import *
from sqlConnect import *

from datetime import datetime, date
from urllib.request import urlopen
# Create your views here.

errorMessage="""<html>
					<body>
						<h1>ERROR</h1>
					</body>
				</html>"""
#-----------------diferentes sub-webs-----------------#
class admin(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		#print(user, password)
		if autenticateUserAdmin(user, token): return render(request, 'administrador/admin.html')
		else: return HttpResponse(errorMessage)

class aVisita(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		if autenticateUserAdmin(user, password): return render(request, 'administrador/agendVisit.html')
		else: return HttpResponse(errorMessage)

class cVisita(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		if autenticateUserAdmin(user, password): return render(request, 'administrador/deleteVisit.html')
		else: return HttpResponse(errorMessage)

class estacionamiento(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		if autenticateUserAdmin(user, password): return render(request, 'administrador/parking.html')
		else: return HttpResponse(errorMessage)

class agenda(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserAdmin(user, token):
			data = getReservationsByUserDay(user, password)
			print(data)
			return render(request, 'administrador/agenda.html', context = {'data': data})
		else: return HttpResponse(errorMessage)

class controlQr(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		if autenticateUserAdmin(user, password): return render(request, 'administrador/controlVisit.html')
		else: return HttpResponse(errorMessage)
	def post(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserAdmin(user, token) == False: return HttpResponse(errorMessage)
		form = imageForm(request.POST)
		if form.is_valid():
			new_task = form.save()
			dicto = model_to_dict(new_task)
			#print('formulario: \n',dicto)
			with urlopen(dicto['imagen']) as response:
				dataT = response.read()
			path = f"administrador/media/RECEIVED_{user}_{datetime.now()}_qr_.png"
			with open(path, "wb") as f:
				f.write(dataT)
			data = compareQrCode(path, user, password)
			#print(data)
			if data == 404:
				print("no coincide con ninguna :(")
				respuesta = JsonResponse({"success": False, "error": "there was an error"})
				respuesta.status_code = 403
				return respuesta
			if data!=False and 404:
				changeStateVisit(user, password, data['id'])
				return JsonResponse({'data': data}, status=200)
			if data==False:
				respuesta = JsonResponse({"success": False, "error": "there was an error"})
				respuesta.status_code = 404
				return respuesta
		else:
			print("invalido :(")
			print(form)
			return JsonResponse({'form': 'error'})


class bitacora(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserAdmin(user, token):
			data = getReservationsByUserBitacora(user, password)
			#print(data)
			return render(request, 'administrador/bitacora.html', context = {'data': data})
		else: return HttpResponse(errorMessage)

class configuracion(View):
	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		if autenticateUserAdmin(user, password): return render(request, 'administrador/configuracion.html')
		else: return HttpResponse(errorMessage)

#-----------------------cosas de las reservas---------------------------#
class newVisit(View):

	def get(self, request):
		user = request.COOKIES.get('usuario')
		password = request.COOKIES.get('token')
		form = VisitsForm()
		if autenticateUserAdmin(user, password): return render(request, 'administrador/agendVisit.html', context = {'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserAdmin(user, token) == False: return HttpResponse(errorMessage)

		form = VisitsForm(request.POST)

		if form.is_valid():
			new_task = form.save()
			if verifyForm(model_to_dict(new_task)) == False: return JsonResponse({'form': model_to_dict(new_task)}, status=406)
			#print('formulario: \n',model_to_dict(new_task))
			if model_to_dict(new_task)['FechaInicio'] < date.today() or model_to_dict(new_task)['FechaInicio'] > model_to_dict(new_task)['FechaFinal']: return JsonResponse({'form': model_to_dict(new_task)}, status=412)
			try:
				addVisit(user, password, model_to_dict(new_task))
				return JsonResponse({'form': model_to_dict(new_task)}, status=200)
			except:
				return JsonResponse({'form': model_to_dict(new_task)}, status=500)
		else:
			print("invalido formulario :(")
			respuesta = JsonResponse({'form': {'error': True}}, status=417)
			print(respuesta)
			return respuesta

class deleteVisit(View):

	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		form = DeleteVisitForm()
		if autenticateUserAdmin(user, token):
			data = getReservationsByUserAdmin(user, password)
			print(data)
			return render(request, 'administrador/deleteVisit.html', context = {'data': data, 'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserAdmin(user, token) == False: return HttpResponse(errorMessage)
		form = DeleteVisitForm(request.POST)
		print(form)

		try:
			new_task = form.save()
			print('formulario: \n', model_to_dict(new_task))
			deleteVisitt(user, password, int(model_to_dict(new_task)['Number']))
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		except Exception as e:
			print("inválido :(", e)
			return JsonResponse({'form': False}, status=500)