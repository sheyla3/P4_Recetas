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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', view=recetasHome, name="home"),
    path('registro/', view=crearUsuario, name="registro"),
    path('login/', view=inicioUsuario, name="login"),
    path('cerrar/', view=cerrarSesion, name="cerrar"),
    path('perfil/', view=perfil, name="perfil"),
    path('perfilEditar/', view=perfilEditar, name="perfilEditar"),
    path('receta/', view=receta, name="receta"),
    path('crearReceta/', view=crearReceta, name="crearReceta"),
    path('editarReceta/<int:id_receta>', view=editarReceta, name="editarReceta"),
    path('eliminarReceta/<int:id_receta>', view=eliminarReceta, name="eliminarReceta"),
    path('comprobacionIng/', view=comprobacionIng, name="comprobacionIng"),
    path('anadirIng/', view=anadirIng, name="anadirIng"),
    path('anadirFoto/', view=anadirFoto, name="anadirFoto"),
    path('detallesReceta/<int:id_receta>/', detallesReceta, name="detallesReceta"),
    path('biblioteca/<str:categoria>/', view=biblioteca, name="biblioteca"),
    path('lista/', view=lista, name="lista"),
    path('lista/crear/', crear_lista, name='crear_lista'),
    path('lista/eliminar/<int:id_lista>/', eliminar_lista, name='eliminar_lista'),
    
    path('reset_password',auth_views.PasswordResetView.as_view(template_name='passwords/password_reset_form.html'),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='passwords/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwords/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='passwords/password_reset_complete.html'),name="password_reset_complete"),
]

