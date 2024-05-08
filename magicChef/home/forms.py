# forms.py

from django import forms
from .models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contrasena']

