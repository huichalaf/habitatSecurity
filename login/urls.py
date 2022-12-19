from django.urls import path, include
from .views import login 

urlpatterns = [
	path('', login.as_view(), name='login_url'),
]