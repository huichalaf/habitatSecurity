from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Users
from .forms import UsersForm

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse

from .manageUsers import *
from .sqlConnection import *

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
			print('formulario: \n',new_task)
			resultado = autenticateUser(new_task['user'], new_task['password'])
			print("devuelvo")
			print({'user': new_task, 'result': resultado})
			return JsonResponse({'user': new_task, 'result': resultado}, status=200)
		else:
			print("invalido :(")
			return redirect('/main/')
