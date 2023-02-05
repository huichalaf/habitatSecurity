from django.views.generic import View
import base64
from django.shortcuts import render, redirect

class imagen(View):
    def get(self, request):
        imagen = None
        with open('static/imagenes/fondo_real.jpg', "rb") as archivo_imagen:
            imagen = base64.b64encode(archivo_imagen.read()).decode('utf-8')

        context = {'imagen': imagen}

        return render(request, 'imagen.html', context)