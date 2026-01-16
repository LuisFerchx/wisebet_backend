from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    # Roles choices
    ADMIN = 'ADMIN'
    OPERADOR = 'OPERADOR'
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (OPERADOR, 'Operador'),
    ]

    email = models.EmailField(unique=True)
    numero_contacto = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default=OPERADOR)
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
