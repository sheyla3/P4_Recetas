from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password as django_check_password

email_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message="Email invalido tiene que tener @ y . ")
string_regex =  RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$', message="Caracteres especiales como (~!#^`'$|{}<>*) no se permiten.")

class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, validators=[string_regex])
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
    pasos = models.CharField(max_length=1000, validators=[string_regex])
    autor = models.CharField(max_length=50, validators=[string_regex])
    fecha_subida = models.DateField()
    activo = models.BooleanField(default=False)

class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    foto = models.ImageField()

class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nombre_ingrediente = models.CharField(max_length=50, validators=[string_regex])
    cantidad = models.CharField(max_length=50)

class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=500)
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, validators=[string_regex])
    apellido = models.CharField(max_length=50, validators=[string_regex])
    correo = models.EmailField(unique=True, validators=[email_regex])
    contrasena = models.CharField(max_length=500)
    def check_password(self, raw_password):
        return django_check_password(raw_password, self.contrasena)

class ListaCompra(models.Model):
    id_lista = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    lista = models.CharField(max_length=1000)

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=500)