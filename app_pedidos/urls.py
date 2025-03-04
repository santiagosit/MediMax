from django.urls import path
from .views import (listar_pedidos, crear_pedido, editar_pedido, eliminar_pedido, ver_pedido, asignar_pedido)

urlpatterns = [
    path('pedidos/', listar_pedidos, name='listar_pedidos'),
    path('pedidos/crear/', crear_pedido, name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', eliminar_pedido, name='eliminar_pedido'),
    path('<int:pedido_id>/', ver_pedido, name='ver_pedido'),
    path('asignar_pedido/', asignar_pedido, name='asignar_pedido'),    
]