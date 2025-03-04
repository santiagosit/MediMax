import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UsuarioForm, RepartidorForm
from .models import Usuario
from app_pedidos.models import Pedido 
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Decorador para restringir acceso solo a administradores
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != "administrador":
            return redirect('repartidor_dashboard')  # Redirigir a home del repartidor
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorador para restringir acceso solo a repartidores
def repartidor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != "repartidor":
            return redirect('admin_dashboard')  # Redirigir a home del admin
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_protect
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:  # Administrador
                return redirect('admin_dashboard')
            else:
                return redirect('repartidor_dashboard')
        else:
            return render(request, 'index.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'index.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'usuario/homeAdmin.html')

@login_required
@repartidor_required
def repartidor_dashboard(request):
    # Obtener el usuario actual (repartidor)
    repartidor = request.user

    # Filtrar los pedidos asignados a este repartidor
    pedidos = Pedido.objects.filter(repartidor=repartidor)

    # Pasar los pedidos a la plantilla
    return render(request, 'usuario/homeRepartidor.html', {'pedidos': pedidos})

def es_administrador(usuario):
    return usuario.rol == 'administrador'

@login_required
@admin_required
def lista_repartidores(request):
    repartidores = Usuario.objects.filter(rol='repartidor')
    return render(request, 'usuario/repartidores.html', {'repartidores': repartidores})


@login_required
@admin_required
def crear_repartidor(request):
    if request.method == "POST":
        print("Datos recibidos en el formulario:", request.POST)
        form = RepartidorForm(request.POST)
        if form.is_valid():
            # Crear usuario utilizando el manager personalizado
            nuevo_usuario = Usuario.objects.create_user(  # <-- Usar un nombre diferente evita sobrescribir el modelo
                username=form.cleaned_data['username'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                correo=form.cleaned_data['correo'],
                password=form.cleaned_data['password'],  # Encriptación automática
                rol='repartidor'  # Forzar rol
            )    
            print("Usuario creado:", nuevo_usuario)
            messages.success(request, "Repartidor creado exitosamente.")
            return redirect('lista_repartidores')
        else:
            print("Errores en el formulario:", form.errors)
    else:
        form = UsuarioForm()
    
    return render(request, 'usuario/crear_repartidor.html', {'form': form})


@login_required
@admin_required
def editar_repartidor(request, pk):
    repartidor = get_object_or_404(Usuario, pk=pk, rol='repartidor')
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=repartidor)
        if form.is_valid():
            repartidor = form.save(commit=False)
            if form.cleaned_data['password']:  # Solo actualizar si se ingresa nueva contraseña
                repartidor.set_password(form.cleaned_data['password'])
            repartidor.save()
            messages.success(request, "Repartidor actualizado exitosamente.")
            return redirect('lista_repartidores')
    else:
        form = UsuarioForm(instance=repartidor)
    return render(request, 'usuario/editar_repartidor.html', {'form': form})

@login_required
@admin_required
def eliminar_repartidor(request, pk):
    repartidor = get_object_or_404(Usuario, pk=pk, rol='repartidor')
    repartidor.delete()
    messages.success(request, "Repartidor eliminado exitosamente.")
    return redirect('lista_repartidores')