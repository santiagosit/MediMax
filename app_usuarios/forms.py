from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'correo', 'password', 'rol']

class RepartidorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'correo', 'password']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = 'repartidor'  # Se asigna el rol de repartidor automáticamente
        if commit:
            usuario.save()
        return usuario