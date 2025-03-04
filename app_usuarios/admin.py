from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nombre', 'apellido', 'correo', 'rol', 'is_active')
    search_fields = ('username', 'correo')
    list_filter = ('rol',)
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellido', 'correo', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nombre', 'apellido', 'correo', 'rol', 'password1', 'password2'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)
