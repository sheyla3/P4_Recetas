from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def recetasHome(request):
    obj=Receta.objects.all().values('titulo')
    lista = "<h2>Receta </h2>"
    for i in obj:
        lista += f"{i}"
    return HttpResponse(lista)
