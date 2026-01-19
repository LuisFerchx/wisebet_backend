# API de Navegación RBAC - Guía de Uso

## Endpoint Creado

```
GET /api/auth/navigation/
Authorization: Bearer {access_token}
```

## Descripción

Este endpoint retorna los menús y sub-menús (children) a los que el usuario tiene acceso según su rol asignado.

## Respuesta Exitosa (200 OK)

```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@wisebet.com",
    "first_name": "Admin",
    "last_name": "User",
    "numero_contacto": "1234567890",
    "rol": 1,
    "nombre_completo": "Administrador Principal",
    "created_at": "2026-01-18T15:00:00Z"
  },
  "navigation": [
    {
      "id": 1,
      "name": "Dashboard",
      "code": "dashboard",
      "icon": "dashboard",
      "route": "/dashboard",
      "order": 1,
      "children": []
    },
    {
      "id": 2,
      "name": "Administración",
      "code": "administration",
      "icon": "settings",
      "route": null,
      "order": 2,
      "children": [
        {
          "id": 3,
          "name": "Usuarios",
          "code": "users",
          "icon": "people",
          "route": "/admin/users",
          "order": 1,
          "children": []
        },
        {
          "id": 4,
          "name": "Roles",
          "code": "roles",
          "icon": "security",
          "route": "/admin/roles",
          "order": 2,
          "children": []
        }
      ]
    }
  ]
}
```

## Respuesta cuando el usuario no tiene rol asignado

```json
{
  "user": {
    "id": 2,
    "username": "newuser",
    "email": "newuser@wisebet.com",
    "nombre_completo": "Usuario Nuevo",
    "rol": null
  },
  "navigation": []
}
```

## Cómo funciona

1. **Autenticación**: El usuario debe estar autenticado (token JWT válido)
2. **Obtención del rol**: Se obtiene el rol del usuario desde `user.rol` (ForeignKey a Role)
3. **Consulta de permisos**: Se buscan todos los `RoleMenuAccess` donde:
   - `role = user.rol`
   - `is_active = True`
   - `menu.is_active = True`
4. **Filtrado de menús**: Se obtienen solo los menús padre (sin parent) a los que el usuario tiene acceso
5. **Anidación de children**: Para cada menú padre, se obtienen sus hijos (children) a los que el usuario tiene acceso
6. **Ordenamiento**: Los menús y children se ordenan por `order` y luego por `name`

## Estructura de Datos Necesaria

### 1. Crear Roles

```python
from apps.authentication.models import Role

# Crear rol de Administrador
admin_role = Role.objects.create(
    name='Administrador',
    code='ADMIN',
    description='Acceso completo al sistema',
    is_active=True
)

# Crear rol de Operador
operador_role = Role.objects.create(
    name='Operador',
    code='OPERADOR',
    description='Acceso a operaciones básicas',
    is_active=True
)
```

### 2. Crear Menús Padre

```python
from apps.authentication.models import Menu

# Dashboard (menú con ruta directa, sin children)
dashboard_menu = Menu.objects.create(
    name='Dashboard',
    code='dashboard',
    icon='dashboard',
    route='/dashboard',
    parent=None,  # Es un menú padre
    order=1,
    is_active=True
)

# Administración (menú sin ruta, tendrá children)
admin_menu = Menu.objects.create(
    name='Administración',
    code='administration',
    icon='settings',
    route=None,  # No tiene ruta porque tiene children
    parent=None,  # Es un menú padre
    order=2,
    is_active=True
)

# Operaciones (menú sin ruta, tendrá children)
operations_menu = Menu.objects.create(
    name='Operaciones',
    code='operations',
    icon='work',
    route=None,
    parent=None,
    order=3,
    is_active=True
)
```

### 3. Crear Menús Hijos (Children)

```python
# Children de Administración
users_menu = Menu.objects.create(
    name='Usuarios',
    code='users',
    icon='people',
    route='/admin/users',
    parent=admin_menu,  # Hijo de Administración
    order=1,
    is_active=True
)

roles_menu = Menu.objects.create(
    name='Roles',
    code='roles',
    icon='security',
    route='/admin/roles',
    parent=admin_menu,
    order=2,
    is_active=True
)

agencies_menu = Menu.objects.create(
    name='Agencias',
    code='agencies',
    icon='business',
    route='/admin/agencies',
    parent=admin_menu,
    order=3,
    is_active=True
)

# Children de Operaciones
bets_menu = Menu.objects.create(
    name='Apuestas',
    code='bets',
    icon='casino',
    route='/operations/bets',
    parent=operations_menu,
    order=1,
    is_active=True
)

reports_menu = Menu.objects.create(
    name='Reportes',
    code='reports',
    icon='assessment',
    route='/operations/reports',
    parent=operations_menu,
    order=2,
    is_active=True
)
```

### 4. Asignar Permisos (RoleMenuAccess)

```python
from apps.authentication.models import RoleMenuAccess

# Permisos para ADMIN (acceso completo)
# Dashboard
RoleMenuAccess.objects.create(role=admin_role, menu=dashboard_menu, is_active=True)

# Administración - todos los children
RoleMenuAccess.objects.create(role=admin_role, menu=admin_menu, is_active=True)
RoleMenuAccess.objects.create(role=admin_role, menu=users_menu, is_active=True)
RoleMenuAccess.objects.create(role=admin_role, menu=roles_menu, is_active=True)
RoleMenuAccess.objects.create(role=admin_role, menu=agencies_menu, is_active=True)

# Operaciones - todos los children
RoleMenuAccess.objects.create(role=admin_role, menu=operations_menu, is_active=True)
RoleMenuAccess.objects.create(role=admin_role, menu=bets_menu, is_active=True)
RoleMenuAccess.objects.create(role=admin_role, menu=reports_menu, is_active=True)

# Permisos para OPERADOR (acceso limitado)
# Dashboard
RoleMenuAccess.objects.create(role=operador_role, menu=dashboard_menu, is_active=True)

# Operaciones - solo algunos children
RoleMenuAccess.objects.create(role=operador_role, menu=operations_menu, is_active=True)
RoleMenuAccess.objects.create(role=operador_role, menu=bets_menu, is_active=True)
# Nota: El operador NO tiene acceso a reports_menu ni a ningún menú de Administración
```

### 5. Asignar Rol a Usuario

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# Obtener o crear usuario
user = User.objects.get(username='admin')

# Asignar rol
user.rol = admin_role
user.save()
```

## Script Completo para Poblar Datos

Puedes crear un archivo `apps/authentication/management/commands/setup_rbac.py`:

```python
from django.core.management.base import BaseCommand
from apps.authentication.models import Role, Menu, RoleMenuAccess
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Configura datos iniciales de RBAC'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando roles...')
        
        # Crear roles
        admin_role, _ = Role.objects.get_or_create(
            code='ADMIN',
            defaults={
                'name': 'Administrador',
                'description': 'Acceso completo al sistema',
                'is_active': True
            }
        )
        
        operador_role, _ = Role.objects.get_or_create(
            code='OPERADOR',
            defaults={
                'name': 'Operador',
                'description': 'Acceso a operaciones básicas',
                'is_active': True
            }
        )
        
        self.stdout.write('Creando menús...')
        
        # Menús padre
        dashboard_menu, _ = Menu.objects.get_or_create(
            code='dashboard',
            defaults={
                'name': 'Dashboard',
                'icon': 'dashboard',
                'route': '/dashboard',
                'order': 1,
                'is_active': True
            }
        )
        
        admin_menu, _ = Menu.objects.get_or_create(
            code='administration',
            defaults={
                'name': 'Administración',
                'icon': 'settings',
                'route': None,
                'order': 2,
                'is_active': True
            }
        )
        
        operations_menu, _ = Menu.objects.get_or_create(
            code='operations',
            defaults={
                'name': 'Operaciones',
                'icon': 'work',
                'route': None,
                'order': 3,
                'is_active': True
            }
        )
        
        # Children de Administración
        users_menu, _ = Menu.objects.get_or_create(
            code='users',
            defaults={
                'name': 'Usuarios',
                'icon': 'people',
                'route': '/admin/users',
                'parent': admin_menu,
                'order': 1,
                'is_active': True
            }
        )
        
        roles_menu, _ = Menu.objects.get_or_create(
            code='roles',
            defaults={
                'name': 'Roles',
                'icon': 'security',
                'route': '/admin/roles',
                'parent': admin_menu,
                'order': 2,
                'is_active': True
            }
        )
        
        agencies_menu, _ = Menu.objects.get_or_create(
            code='agencies',
            defaults={
                'name': 'Agencias',
                'icon': 'business',
                'route': '/admin/agencies',
                'parent': admin_menu,
                'order': 3,
                'is_active': True
            }
        )
        
        # Children de Operaciones
        bets_menu, _ = Menu.objects.get_or_create(
            code='bets',
            defaults={
                'name': 'Apuestas',
                'icon': 'casino',
                'route': '/operations/bets',
                'parent': operations_menu,
                'order': 1,
                'is_active': True
            }
        )
        
        reports_menu, _ = Menu.objects.get_or_create(
            code='reports',
            defaults={
                'name': 'Reportes',
                'icon': 'assessment',
                'route': '/operations/reports',
                'parent': operations_menu,
                'order': 2,
                'is_active': True
            }
        )
        
        self.stdout.write('Asignando permisos...')
        
        # Permisos para ADMIN
        admin_menus = [
            dashboard_menu, admin_menu, users_menu, roles_menu, agencies_menu,
            operations_menu, bets_menu, reports_menu
        ]
        
        for menu in admin_menus:
            RoleMenuAccess.objects.get_or_create(
                role=admin_role,
                menu=menu,
                defaults={'is_active': True}
            )
        
        # Permisos para OPERADOR
        operador_menus = [dashboard_menu, operations_menu, bets_menu]
        
        for menu in operador_menus:
            RoleMenuAccess.objects.get_or_create(
                role=operador_role,
                menu=menu,
                defaults={'is_active': True}
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Datos RBAC creados exitosamente'))
```

Ejecutar con:
```bash
python manage.py setup_rbac
```

## Prueba de la API

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin", "password": "tu_password"}'

# 2. Obtener navegación (usar el access token del login)
curl -X GET http://localhost:8000/api/auth/navigation/ \
  -H "Authorization: Bearer {access_token}"
```

## Integración con React

Ver el archivo `rbac_react_integration_guide.md` para detalles completos de integración con React.
