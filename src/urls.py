"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', login.as_view(), name='login_url'),
    path('residente/<user>/<password>/', include('residente.urls'), name='residente_url'),
    path('administrador/<user>/<password>/', include('administrador.urls'), name='administrador_url')
]
