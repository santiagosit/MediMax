from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Manager personalizado para gestionar los usuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, username, nombre, apellido, correo, password=None, rol='repartidor'):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        usuario = self.model(
            username=username,
            nombre=nombre,
            apellido=apellido,
            correo=self.normalize_email(correo),
            rol=rol
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, username, nombre, apellido, correo, password):
        usuario = self.create_user(username, nombre, apellido, correo, password, rol='administrador')
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario

# Modelo de usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('administrador', 'Administrador'),
        ('repartidor', 'Repartidor'),
    ]

    username = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='repartidor')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nombre", "apellido", "correo"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"
