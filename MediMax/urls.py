from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('app_bascula.urls')),
    path('', include('app_usuarios.urls')),
    path('', include('app_clientes.urls')),  
    path('', include('app_pedidos.urls')),
]
