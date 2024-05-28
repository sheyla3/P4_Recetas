from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password as django_check_password , make_password
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator

email_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message="Email invalido tiene que tener @ y . ")
string_regex =  RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$', message="Caracteres especiales como (~!#^`'$|{}<>*) no se permiten.")

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, contrasena=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico debe ser proporcionado')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    apodo = models.CharField(max_length=50, default='apodo')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=500)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="usuarios",
        related_query_name="usuario",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="usuarios",
        related_query_name="usuario",
    )

    def __str__(self):
        return self.correo

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.contrasena)

class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=5000)
    TIPOS_CHOICES = (
        ('Postres', 'Postres'),
        ('Pollo y Carne', 'Pollo y Carne'),
        ('Recetas a la Parrilla', 'Recetas a la Parrilla'),
        ('Ensaladas', 'Ensaladas'),
        ('Guarniciones', 'Guarniciones'),
        ('Pescados y Mariscos', 'Pescados y Mariscos'),
        ('Recetas de Pastas', 'Recetas de Pastas'),
        ('Sopas', 'Sopas'),
        ('Desayunos', 'Desayunos'),
        ('Panes', 'Panes'),
        ('Salsas', 'Salsas'),
        ('Bebidas', 'Bebidas'),
    )
    tipo = models.CharField(max_length=50, choices=TIPOS_CHOICES)
    pasos = models.CharField(max_length=5000)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=False)

class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    foto = models.ImageField()
    
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre_ingrediente = models.CharField(max_length=50, validators=[string_regex])

class IngredienteReceta(models.Model):
    id_ingrediente_receta = models.AutoField(primary_key=True)
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    id_ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=50)

class ListaCompra(models.Model):
    id_lista = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    lista = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.lista

class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=5000)
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    id_receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(auto_now=True)

"""
class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=500, unique=True)
    contrasena = models.CharField(max_length=500)
    last_login = models.DateTimeField(auto_now=True)
"""