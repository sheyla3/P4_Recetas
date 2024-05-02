from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def recetasHome(request):
    recetas = Receta.objects.all()
    return render(request, 'index.html', {'recetas': recetas})
