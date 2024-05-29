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
    recetas = Receta.objects.filter(autor=user)
    return render(request, 'recetas.html', {'recetas': recetas, 'user': user})

@login_required
def crearReceta(request):
    user = request.user
    if request.method == 'POST':
        form = CrearRecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = user
            receta.fecha_subida = timezone.now()
            receta.activo = False
            receta.save()
            messages.success(request, 'Receta creada con éxito.')
            return redirect('comprobacionIng')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CrearRecetaForm()
    return render(request, 'crearReceta.html', {'form': form})

@login_required
def editarReceta(request, id_receta):
    user = request.user
    fechaActual = datetime.date.today()
    
    if request.method == 'POST':
        form = CrearRecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = user.apodo  # O el campo correspondiente del usuario
            receta.fecha_subida = fechaActual
            receta.save()
            request.session['ultima_receta'] = receta.id_receta
            return redirect('comprobacionIng')
        else:
            messages.error(request, 'Error al crear receta')
    else:
        form = CrearRecetaForm(initial={'autor': user.apodo, 'fecha_subida': fechaActual, 'activo': True})
    
    return render(request, 'recetas.html', {'form': form, 'user': user, 'fechaActual': fechaActual})

@login_required
def eliminarReceta(request, id_receta):
    user = request.user
    fechaActual = datetime.date.today()
    
    if request.method == 'POST':
        form = CrearRecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = user.apodo  # O el campo correspondiente del usuario
            receta.fecha_subida = fechaActual
            receta.save()
            request.session['ultima_receta'] = receta.id_receta
            return redirect('comprobacionIng')
        else:
            messages.error(request, 'Error al crear receta')
    else:
        form = CrearRecetaForm(initial={'autor': user.apodo, 'fecha_subida': fechaActual, 'activo': True})
    
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
    ultima_receta = Receta.objects.filter(autor=request.user).latest('fecha_subida')
    ultima_receta_id = ultima_receta.id_receta

    if request.method == 'POST':
        id_receta = request.POST.get('id_receta')
        ingredientes_data = request.POST.dict()
        ingredientes = {}
        for key, value in ingredientes_data.items():
            if key.startswith('ingredientes'):
                parts = key.split('[')
                index = parts[1].strip(']')
                field = parts[2].strip(']')

                if index not in ingredientes:
                    ingredientes[index] = {}
                ingredientes[index][field] = value

        for ingrediente in ingredientes.values():
            id_ingrediente = ingrediente.get('id_ingrediente')
            cantidad = ingrediente.get('cantidad')

            if id_ingrediente and cantidad:
                IngredienteReceta.objects.create(
                    id_receta_id=id_receta,
                    id_ingrediente_id=id_ingrediente,
                    cantidad=cantidad
                )
        messages.success(request, 'Ingredientes guardados correctamente')
        return redirect('anadirFoto')

    ingredientes = Ingrediente.objects.all()
    return render(request, 'anadirIng.html', {'ingredientes': ingredientes, 'form': AnadirIngrRecetaForm(), 'ultima_receta_id': ultima_receta_id })

@login_required
def anadirFoto(request):
    ultima_receta = Receta.objects.filter(autor=request.user).latest('fecha_subida')
    ultima_receta_id = ultima_receta.id_receta
    if request.method == 'POST':
        id_receta = request.POST.get('id_receta')
        foto = request.FILES.get('foto')
        Foto.objects.create(
            id_receta_id=id_receta,
            foto=foto
        )
        return redirect('receta')
    return render(request, 'anadirFoto.html', {'form': AnadirFotoForm(), 'ultima_receta_id': ultima_receta_id })

@login_required
def lista(request):
    user = request.user
    listas = ListaCompra.objects.filter(id_usuario=user)
    if not listas:
        message = "No hay listas"
    else:
        message = None
    return render(request, 'lista.html', {'user': user, 'listas': listas, 'message': message})

@login_required
def crear_lista(request):
    if request.method == 'POST':
        form = ListaCompraForm(request.POST)
        if form.is_valid():
            nueva_lista = form.save(commit=False)
            nueva_lista.id_usuario = request.user
            nueva_lista.save()
            return redirect('lista')
    else:
        form = ListaCompraForm()
    return render(request, 'crear_lista.html', {'form': form})

@login_required
def eliminar_lista(request, id_lista):
    lista = get_object_or_404(ListaCompra, id_lista=id_lista, id_usuario=request.user)
    if request.method == 'POST':
        lista.delete()
        return redirect('lista')
    return render(request, 'eliminar_lista.html', {'lista': lista})

def biblioteca(request, categoria):
    user = request.user
    recetas = Receta.objects.filter(tipo=categoria)
    return render(request, 'biblioteca.html', {'recetas': recetas, 'user': user, 'categoria': categoria})

def detallesReceta(request, id_receta):
    user = request.user
    receta = get_object_or_404(Receta, pk=id_receta)
    ingredientes = IngredienteReceta.objects.filter(id_receta=receta)
    fotos = Foto.objects.filter(id_receta=receta)
    comentarios = Comentario.objects.filter(id_receta=receta).order_by('-fecha_creacion')
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.id_receta = receta
            comentario.usuario = user
            comentario.save()
            return redirect('detallesReceta', id_receta=receta.id_receta)
    else:
        form = ComentarioForm()
        calificacion_titulos = [
            ('5', 'Excelente!'),
            ('4', 'Genial!'),
            ('3', 'Bien'),
            ('2', 'Normal'),
            ('1', 'Mal')
        ]
        context = {
            'receta': receta, 'ingredientes': ingredientes,
            'fotos': fotos, 'comentarios': comentarios,
            'form': form, 'user': user, 'calificacion_titulos' : calificacion_titulos
        }
    return render(request, 'detalles_receta.html', context)