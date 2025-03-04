from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, Producto
from .forms import PedidoForm 
from app_usuarios.models import Usuario
from datetime import datetime, timedelta
from .models import Pedido
import json

def listar_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    
    # Obtener parámetros del filtro
    fecha = request.GET.get('fecha')
    filtro_tiempo = request.GET.get('filtro_tiempo')
    cliente = request.GET.get('cliente')
    repartidor = request.GET.get('repartidor')
    estado = request.GET.get('estado')

    # Aplicar filtros dinámicamente
    if fecha:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            pedidos = pedidos.filter(fecha_creacion__date=fecha_obj)
        except ValueError:
            pass  # Evita errores si la fecha no tiene el formato correcto
    hoy = datetime.today().date()
    if filtro_tiempo == "semana":
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de la semana actual
        pedidos = pedidos.filter(fecha_creacion__date__gte=inicio_semana)
    elif filtro_tiempo == "mes":
        pedidos = pedidos.filter(fecha_creacion__year=hoy.year, fecha_creacion__month=hoy.month)
    elif filtro_tiempo == "año":
        pedidos = pedidos.filter(fecha_creacion__year=hoy.year)
    if cliente:
        pedidos = pedidos.filter(cliente__nombre__icontains=cliente)
    if repartidor:
        pedidos = pedidos.filter(repartidor__nombre__icontains=repartidor)
    if estado:
        pedidos = pedidos.filter(estado=estado)
    
    return render(request, 'app_pedidos/listar_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.valor_total = 0  # Se recalcula luego
            pedido.save()

            # Obtener los productos desde el formulario (JSON)
            productos_json = request.POST.get('productos')
            if productos_json:
                productos_data = json.loads(productos_json)
                for producto in productos_data:
                    nuevo_producto = Producto.objects.create(
                        nombre=producto['nombre'],
                        peso=producto['peso'],
                        valor_unitario=producto['valorUnitario']
                    )
                    pedido.productos.add(nuevo_producto)  # Relaciona el producto con el pedido
                    pedido.valor_total += (float(nuevo_producto.peso) * float(nuevo_producto.valor_unitario))

            pedido.save()
            return redirect('listar_pedidos')  # Ajusta con tu URL correcta

    else:
        form = PedidoForm()

    return render(request, 'app_pedidos/crear_pedido.html', {'pedido_form': form})

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido actualizado exitosamente')
            return redirect('listar_pedidos')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'app_pedidos/editar_pedido.html', {'form': form})       

def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.delete()
    messages.success(request, 'Pedido eliminado exitosamente')
    return redirect('listar_pedidos')

def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'app_pedidos/ver_pedido.html', {'pedido': pedido})

def asignar_pedido(request):
    pedidos_sin_asignar = Pedido.objects.filter(repartidor__isnull=True, estado="Pendiente")
    pedidos_asignados = Pedido.objects.filter(repartidor__isnull=False)
    repartidores = Usuario.objects.filter(rol='repartidor')

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        repartidor_id = request.POST.get('repartidor_id')

        pedido = get_object_or_404(Pedido, id=pedido_id)
        repartidor = get_object_or_404(Usuario, id=repartidor_id)

        # Contar pedidos asignados al repartidor
        pedidos_asignados_count = Pedido.objects.filter(repartidor=repartidor, estado="En camino").count()

        if pedidos_asignados_count >= 3:
            messages.error(request, "Este repartidor ya tiene 3 pedidos asignados.")
        else:
            pedido.repartidor = repartidor
            pedido.estado = "En camino"  # Cambia el estado a "En camino"
            pedido.save()
            messages.success(request, f"Pedido {pedido.numero_orden} asignado a {repartidor.nombre} y marcado como 'En camino'.")

        return redirect('asignar_pedido')

    return render(request, 'app_pedidos/asignar_pedido.html', {
        'pedidos_sin_asignar': pedidos_sin_asignar,
        'pedidos_asignados': pedidos_asignados,
        'repartidores': repartidores
    })
