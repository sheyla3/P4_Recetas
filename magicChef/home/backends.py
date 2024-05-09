from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request, correo=None, contrasena=None, **kwargs):
        try:
            user = Usuario.objects.get(correo=correo)
            if check_password(contrasena, user.contrasena):
                return user
        except Usuario.DoesNotExist:
            return None
