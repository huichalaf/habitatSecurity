from django.shortcuts import render
from django.views.generic import View

from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import VisitsForm, DeleteVisitFormResidente

from django.http import HttpResponse
from .autentication import *
from sqlConnect import *

errorMessage="""<html>
					<body>
						<h1>ERROR</h1>
					</body>
				</html>"""
# Create your views here.
class residente(View):

	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		print(user, token)
		if autenticateUserResidente(user, token): return render(request, 'residente/residenteMain.html')
		else: return HttpResponse(errorMessage)

class newVisit(View):

	def get(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		if autenticateUserResidente(user, token):
			form = VisitsForm()
			return render(request, 'residente/agendar.html', context = {'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserResidente(user, token) == False:
			return HttpResponse(errorMessage)

		form = VisitsForm(request.POST)

		if form.is_valid():
			new_task = form.save()
			print('formulario: \n',model_to_dict(new_task))
			if model_to_dict(new_task)['FechaInicio'] < date.today() or model_to_dict(new_task)['FechaInicio'] > model_to_dict(new_task)['FechaFinal']: return JsonResponse({'form': model_to_dict(new_task)}, status=412)
			try:
				addVisit(user, password, model_to_dict(new_task))
				return JsonResponse({'form': model_to_dict(new_task)}, status=200)
			except Exception as e:
				print(e)
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
		form = DeleteVisitFormResidente()
		if autenticateUserResidente(user, token):
			data = getReservationsByUserResidente(user, password)
			print(data)
			return render(request, 'residente/eliminar.html', context = {'data': data, 'form': form})
		else: return HttpResponse(errorMessage)
	
	def post(self, request):
		user = request.COOKIES.get('usuario')
		token = request.COOKIES.get('token')
		password = getPasswordWithToken(user, token)
		if autenticateUserResidente(user, token) == False: return HttpResponse(errorMessage)
		form = DeleteVisitFormResidente(request.POST)
		print(form)

		try:
			new_task = form.save()
			print('formulario: \n', model_to_dict(new_task))
			deleteVisitt(user, password, int(model_to_dict(new_task)['Number']))
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		except Exception as e:
			print("inválido :(", e)
			return JsonResponse({'form': False}, status=500)