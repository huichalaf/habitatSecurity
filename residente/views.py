from django.shortcuts import render, redirect
from django.views.generic import View

from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import VisitsForm, DeleteVisitFormResidente

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .autentication import *

errorMessage="""<html>
					<body>
						<h1>ERROR</h1>
					</body>
				</html>"""
# Create your views here.
class residente(View):

	def get(self, request, user, password):
		if autenticateUserResidente(user, password): return render(request, 'residente/residenteMain.html')
		else: return HttpResponse(errorMessage)

class newVisit(View):

	def get(self, request, user, password):
		if autenticateUserResidente(user, password):
			form = VisitsForm()
			return render(request, 'residente/agendar.html', context = {'form': form})
		else: return HttpResponse(errorMessage)

	def post(self, request, user, password):
	
		if autenticateUserResidente(user, password) == False:
			return HttpResponse(errorMessage)

		form = VisitsForm(request.POST)

		if form.is_valid():
			new_task = form.save()
			print('formulario: \n',model_to_dict(new_task))
			#JsonResponse({'form': model_to_dict(new_task)}, status=200)
			addVisit(user, password, model_to_dict(new_task))
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		else:
			print("invalido :(")
			print(form)
			return redirect('agendVisit/')

class deleteVisit(View):

	def get(self, request, user, password):
		form = DeleteVisitFormResidente()
		if autenticateUserResidente(user, password):
			data = getReservationsByUser(user, password)
			print(data)
			return render(request, 'administrador/deleteVisit.html', context = {'data': data, 'form': form})
		else: return HttpResponse(errorMessage)
	
	def post(self, request, user, password):
		if autenticateUserResidente(user, password) == False: return HttpResponse(errorMessage)
		form = DeleteVisitFormResidente(request.POST)
		print(form)

		try:
			new_task = form.save()
			print('formulario: \n', model_to_dict(new_task))
			deleteVisitt(user, password, int(model_to_dict(new_task)['Number']))
			return JsonResponse({'form': model_to_dict(new_task)}, status=200)
		except Exception as e:
			print("inválido :(", e)
			return JsonResponse({'form': 'error'})