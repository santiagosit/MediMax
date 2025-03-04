from django.db import models
from django.utils.timezone import now
from django.conf import settings
import random
import string

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    peso = models.FloatField()  # Peso en kg
    valor_unitario = models.FloatField()  # Precio por kg

    def __str__(self):
        return f"{self.nombre} ({self.peso} kg)"
    
def generar_numero_orden():
    return ''.join(random.choices(string.digits, k=8))

class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En camino', 'En camino'),
        ('Entregado', 'Entregado'),
    ]

    numero_orden = models.CharField(max_length=10, unique=True, default=generar_numero_orden)
    cliente = models.ForeignKey('app_clientes.Cliente', on_delete=models.CASCADE)  # Relación con Cliente
    productos = models.ManyToManyField(Producto, related_name="pedidos")  # Relación ManyToMany
    valor_total = models.FloatField(default=0)  # Se calculará automáticamente
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    repartidor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relacionamos con la tabla Usuario
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol': 'repartidor'}  # Solo usuarios con rol de repartidor
    )

    def __str__(self):
        return f"Pedido {self.numero_orden} - Cliente: {self.cliente.nombre} - Estado: {self.estado}"