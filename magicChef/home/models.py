from django.db import models

# Create your models here.
from django.db import models

class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    TIPOS_CHOICES = (
        ('Fáciles', 'Fáciles'),
        ('Postres', 'Postres'),
        ('Pollo y Carne', 'Pollo y Carne'),
        ('Recetas a la Parrilla', 'Recetas a la Parrilla'),
        ('Ensaladas', 'Ensaladas'),
        ('Guarniciones', 'Guarniciones'),
        ('Pescados y Mariscos', 'Pescados y Mariscos'),
        ('Recetas de Pastas', 'Recetas de Pastas'),
        ('Comida para Niños', 'Comida para Niños'),
        ('Postres para Niños', 'Postres para Niños'),
        ('Sopas', 'Sopas'),
        ('Desayunos', 'Desayunos'),
        ('Panes', 'Panes'),
        ('Salsas', 'Salsas'),
        ('Bebidas', 'Bebidas'),
        ('Platos Fuertes', 'Platos Fuertes'),
        ('Recetas Navideñas', 'Recetas Navideñas'),
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_CHOICES)
    pasos = models.CharField(max_length=1000)
    autor = models.CharField(max_length=50)
    fecha_subida = models.DateField()
    activo = models.BooleanField(default=False)

class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    foto = models.CharField(max_length=500)

class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nombre_ingrediente = models.CharField(max_length=50)
    cantidad = models.CharField(max_length=50)

class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=500)
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=500)

class ListaCompra(models.Model):
    id_lista = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    lista = models.CharField(max_length=1000)

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=500)