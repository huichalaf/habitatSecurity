from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Users
from .forms import UsersForm

from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict

from .manageUsers import *
from sqlConnect import *

import json

def ipaddress(request):
	user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
	if user_ip:
		ip = user_ip.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
# Create your views here.
class login(View):
	def get(self, request):
		form = UsersForm()
		return render(request, 'login/login_list.html', context={'form': form})

	def post(self, request):
		form = UsersForm(request.POST)

		if form.is_valid():
			
			new_task = form.save()
			new_task = model_to_dict(new_task)
			#print('formulario: \n',new_task)
			resultado = autenticateUser(new_task['user'], new_task['password'])
			#print("devuelvo")
			#print({'user': new_task, 'result': resultado})
			#code_to_table = generateCode(64)
			token = generateToken(new_task['user'], new_task['password'])
			response = HttpResponse()

			ip_direction = ipaddress(request)
			expiration_date = datetime.now() + timedelta(minutes=30)
			
			response.set_cookie("usuario", new_task['user'], expires=expiration_date)
			response.set_cookie("token", token, expires=expiration_date)
			response.set_cookie("ip", ip_direction, expires=expiration_date)
			response['Content-Type'] = 'application/json'
			print(ip_direction)
			response.write(json.dumps({'user': new_task['user'], 'result': resultado, 'token': token}))
			return response

		else:
			print("invalido :(")
			return redirect('/main/')
