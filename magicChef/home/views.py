from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import RegistroUsuarioForm
# Create your views here.

def recetasHome(request):
    recetas = Receta.objects.all()
    return render(request, 'index.html', {'recetas': recetas})

def crearUsuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})
