from django.urls import path
from .views import iniciar_sesion, cerrar_sesion, admin_dashboard, repartidor_dashboard, lista_repartidores, crear_repartidor, editar_repartidor, eliminar_repartidor

urlpatterns = [
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='cerrar_sesion'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('repartidor_dashboard/', repartidor_dashboard, name='repartidor_dashboard'),
    path('repartidores/', lista_repartidores, name='lista_repartidores'),
    path('repartidores/crear/', crear_repartidor, name='crear_repartidor'),
    path('repartidores/editar/<int:pk>/', editar_repartidor, name='editar_repartidor'),
    path('repartidores/eliminar/<int:pk>/', eliminar_repartidor, name='eliminar_repartidor'),    
]