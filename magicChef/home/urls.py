"""
URL configuration for magicChef project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path
from home.views import *

urlpatterns = [
    path('', view=recetasHome, name="home"),
    path('registro/', view=crearUsuario, name="registro"),
    path('login/', view=inicioUsuario, name="login"),
    path('cerrar/', view=cerrarSesion, name="cerrar"),
    path('perfil/', view=perfil, name="perfil"),
    path('receta/', view=receta, name="receta"),
    path('perfilEditar/', view=perfilEditar, name="perfilEditar"),
    path('lista/', view=lista, name="lista"),
    
    
    path('AdminHome/', view=AdminHome, name="AdminHome"),
    path('loginAdmin/', view=inicioAdmin, name="loginAdmin"),
    
]