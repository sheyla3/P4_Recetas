from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.
def recetasHome(request):
    user = request.user
    recetas = Receta.objects.all()
    return render(request, 'index.html', {'recetas': recetas, 'user': user})

def crearUsuario(request):
    if request.method == 'GET':
        form = RegistroUsuarioForm()
        return render(request, 'registro.html', {'form': form})
    elif request.method == 'POST':
        apodo = request.POST.get('apodo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        contraHash = make_password(contrasena)
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Correo existente')
            return redirect('/registro/')
        
        user = Usuario.objects.create(
            apodo=apodo,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contraHash
        )
        user.save
        messages.success(request, 'Creado correctamente. Ya puedes iniciar sesion.')
        return redirect('/registro/')
        
"""
def inicioUsuario(request):
    if request.method == 'GET':
        form = RegistroUsuarioForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        usuarios = Usuario.objects.filter(correo=correo)
        apodo = usuarios.values_list('apodo', flat=True).first()
        user = authenticate(request, username=apodo, password=contrasena)
        
        if user is None:
            messages.error(request, 'Credenciales inválidas.')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')
"""
def inicioUsuario(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('correo')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def inicioAdmin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            admin_user = Admin.objects.get(usuario__correo=usuario)
            login(request, admin_user.usuario)
            return redirect('home')
    else:
        form = AdminLoginForm()
    return render(request, 'loginAdmin.html', {'form': form})

def cerrarSesion(request):
    logout(request)
    return redirect('home')