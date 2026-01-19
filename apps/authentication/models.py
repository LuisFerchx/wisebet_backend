from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Role model for RBAC system
    Defines different roles in the system (Admin, Operador, etc.)
    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Rol")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "roles"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """

    # Roles choices
    ADMIN = "ADMIN"
    OPERADOR = "OPERADOR"
    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (OPERADOR, "Operador"),
    ]

    email = models.EmailField(unique=True)
    numero_contacto = models.CharField(max_length=20, blank=True, null=True)
    rol = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="Rol",
        null=True,
        blank=True,
    )
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Menu(models.Model):
    """
    Menu model representing main navigation items
    """

    name = models.CharField(max_length=100, verbose_name="Nombre del Menú")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    route = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ruta")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Menú Padre",
    )
    order = models.IntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "menus"
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Section(models.Model):
    """
    Section model representing sub-items within a menu
    """

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="sections", verbose_name="Menú"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre de la Sección")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icono")
    route = models.CharField(max_length=255, verbose_name="Ruta")
    order = models.IntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sections"
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ["menu", "order", "name"]

    def __str__(self):
        return f"{self.menu.name} - {self.name}"


class RoleMenuAccess(models.Model):
    """
    Role-Menu Access model defining which menus and sections are accessible by each role
    Simple active/inactive permission model (no granular permissions)
    """

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="menu_accesses", verbose_name="Rol"
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="role_accesses",
        verbose_name="Menú",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "role_menu_accesses"
        verbose_name = "Acceso de Rol a Menú"
        verbose_name_plural = "Accesos de Roles a Menús"
        unique_together = [["role", "menu"]]
        ordering = ["role", "menu"]

    def __str__(self):
        return f"{self.role.name} - {self.menu.name}"
