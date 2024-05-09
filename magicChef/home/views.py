from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm

# Create your views here.
def recetasHome(request):
    recetas = Receta.objects.all()
    return render(request, 'index.html', {'recetas': recetas})

def crearUsuario(request):
    if request.method == 'GET':
        form = RegistroUsuarioForm()
        return render(request, 'registro.html', {'form': form})
    elif request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        contraHash = make_password(contrasena)
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Correo existente')
            return redirect('/registro/')
        
        user = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contraHash
        )
        user.save
        messages.success(request, 'Creado correctamente. Ya puedes iniciar sesion.')
        return redirect('/registro/')
        
