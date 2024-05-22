# forms.py
from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.core.exceptions import ValidationError
import datetime

class RegistroUsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['apodo', 'nombre', 'apellido', 'correo', 'contrasena']
        
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['apodo', 'nombre', 'apellido', 'correo']
        
class CambiarContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    nueva_contrasena = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirmar_nueva_contrasena = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

class UserLoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    def clean(self):
        correo = self.cleaned_data.get('correo')
        password = self.cleaned_data.get('password')
        user = authenticate(username=correo, password=password)
        if not user:
            raise forms.ValidationError("Correo o contraseña incorrectos")
        return self.cleaned_data

class AdminLoginForm(forms.Form):
    usuario = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    def clean(self):
        usuario = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('contrasena')
        try:
            admin_user = Admin.objects.get(usuario__correo=usuario)
            if not admin_user.check_password(password):
                raise forms.ValidationError("Usuario o contraseña incorrectos")
        except Admin.DoesNotExist:
            raise forms.ValidationError("Usuario o contraseña incorrectos")
        return self.cleaned_data

class CrearRecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'tipo', 'pasos', 'autor', 'fecha_subida', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input'}),
            'descripcion': forms.Textarea(attrs={'class': 'textarea'}),
            'tipo': forms.Select(attrs={'class': 'select'}),
            'pasos': forms.Textarea(attrs={'class': 'textarea'}),
            'autor': forms.HiddenInput(),
            'fecha_subida': forms.HiddenInput(),
            'activo': forms.HiddenInput(),
        }
    
class AnadirIngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre_ingrediente']
        
class AnadirIngrRecetaForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceta
        fields = ['id_receta', 'id_ingrediente', 'cantidad']
        
class ListaCompraForm(forms.ModelForm):
    class Meta:
        model = ListaCompra
        fields = ['lista']
        widgets = {'lista': forms.Textarea(attrs={'class': 'textarea'})}