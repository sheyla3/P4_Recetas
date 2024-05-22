from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import datetime
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
                messages.error(request, 'Credenciales inválidas.')
                return redirect('/login/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def inicioAdmin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        """""
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            contrasena = form.cleaned_data.get('password')
            admin = authenticate(request, username=usuario, password=contrasena)
            print(admin)
            if admin is not None:
                login(request, admin)
                return redirect('AdminHome')
            else:
                messages.error(request, 'Credenciales inválidas. '+ admin)
                return redirect('/loginAdmin/')"""""
    else:
        form = AdminLoginForm()
    return render(request, 'loginAdmin.html', {'form': form})

def cerrarSesion(request):
    logout(request)
    return redirect('home')

@login_required
def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})

@login_required
def perfilEditar(request):
    user = request.user
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')
    else:
        form = EditarUsuarioForm(instance=user)
    return render(request, 'perfilEditar.html', {'form': form, 'user': user})

@login_required
def receta(request):
    user = request.user
    fechaActual = datetime.date.today()
    if request.method == 'POST':
        form = CrearRecetaForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['ultima_receta'] = receta.id_receta
            return redirect('comprobacionIng')
        else:
            messages.success(request, 'Error al crear receta')
            return redirect('receta')
    else:
        form = CrearRecetaForm()
    return render(request, 'recetas.html', {'form': form, 'user': user, 'fechaActual': fechaActual})

@login_required
def comprobacionIng(request):
    user = request.user
    ingredientes = Ingrediente.objects.all()
    fechaActual = datetime.date.today()
    if request.method == 'POST':
        form = AnadirIngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comprobacionIng')
        else:
            messages.success(request, 'Error al crear receta')
            return redirect('comprobacionIng')
    else:
        form = AnadirIngredienteForm()
    return render(request, 'comprobacionIng.html', {'form': form, 'user': user, 'fechaActual': fechaActual, 'ingredientes': ingredientes})

@login_required
def anadirIng(request):
    if 'ultima_receta' in request.session:
        id_ultima_receta = 1 #request.session['ultima_receta']
    else:
        id_ultima_receta = Receta.objects.last()
    if request.method == 'POST':
        id_receta = request.POST.get('id_receta')
        ingredientes_data = request.POST.getlist('ingredientes')
        
        for ingrediente_data in ingredientes_data:
            id_ingrediente = ingrediente_data.get('id_ingrediente')
            cantidad = ingrediente_data.get('cantidad')

            if id_ingrediente and cantidad:
                IngredienteReceta.objects.create(
                    id_receta_id=id_receta,
                    id_ingrediente_id=id_ingrediente,
                    cantidad=cantidad
                )
        return redirect('anadirIng')

    ingredientes = Ingrediente.objects.all()
    return render(request, 'anadirIng.html', {'ingredientes': ingredientes, 'form': AnadirIngrRecetaForm(), 'id_ultima_receta': id_ultima_receta })


@login_required
def lista(request):
    user = request.user
    ingredientes = Ingrediente.objects.all()
    return render(request, 'perfil.html', {'user': user, 'ingredientes': ingredientes})

def AdminHome(request):
    user = request.user
    recetas = Receta.objects.all()
    return render(request, 'homeAdmin.html', {'recetas': recetas, 'user': user})
