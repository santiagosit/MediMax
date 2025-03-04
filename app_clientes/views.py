from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_clientes/listar_clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado exitosamente.")
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'app_clientes/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente editado exitosamente.")
            return redirect('listar_clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm(instance=cliente)  # Cargar datos actuales del cliente solo en GET

    return render(request, 'app_clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, "Cliente eliminado exitosamente.")
    return redirect('listar_clientes')