# ✅ API de Navegación RBAC - Implementación Completa

## 🎯 Resumen

Se ha implementado exitosamente una API GET para listar los menús permitidos según el rol del usuario autenticado.

## 📍 Endpoint Creado

```
GET /api/auth/navigation/
Authorization: Bearer {access_token}
```

## 🔧 Cambios Realizados

### 1. **Modelos Actualizados** (`apps/authentication/models.py`)
   - ✅ `Role` - Modelo de roles del sistema
   - ✅ `Menu` - Modelo de menús con soporte para jerarquía (parent/children)
   - ✅ `Section` - Modelo de secciones (ELIMINADO - se usa Menu.parent en su lugar)
   - ✅ `RoleMenuAccess` - Tabla de permisos simplificada (role + menu)
   - ✅ `User.rol` - Cambiado de CharField a ForeignKey(Role)

### 2. **Serializers Creados** (`apps/authentication/serializers.py`)
   - ✅ `RoleSerializer` - Serializa información de roles
   - ✅ `MenuSerializer` - Serializa menús con children anidados
   - ✅ `UserNavigationResponseSerializer` - Respuesta completa de navegación

### 3. **Vista Creada** (`apps/authentication/views.py`)
   - ✅ `UserNavigationView` - Vista que retorna navegación según rol del usuario
   - Lógica implementada:
     1. Obtiene el rol del usuario autenticado (`request.user.rol`)
     2. Consulta `RoleMenuAccess` para ese rol
     3. Filtra menús padre (sin parent)
     4. Para cada padre, obtiene sus children permitidos
     5. Retorna estructura JSON anidada

### 4. **URL Configurada** (`apps/authentication/urls.py`)
   - ✅ Ruta: `navigation/` → `UserNavigationView`

### 5. **Comando de Management Creado**
   - ✅ `python manage.py setup_rbac`
   - Crea datos de prueba:
     - 2 Roles (Administrador, Operador)
     - 8 Menús (3 padres + 5 children)
     - 11 Permisos asignados

## 📊 Estructura de Datos Creada

### Roles
| ID | Code | Name | Description |
|----|------|------|-------------|
| 1 | ADMIN | Administrador | Acceso completo al sistema |
| 2 | OPERADOR | Operador | Acceso a operaciones básicas |

### Menús Padre
| ID | Code | Name | Icon | Route | Order |
|----|------|------|------|-------|-------|
| 1 | dashboard | Dashboard | dashboard | /dashboard | 1 |
| 2 | administration | Administración | settings | null | 2 |
| 3 | operations | Operaciones | work | null | 3 |

### Menús Children
| ID | Code | Name | Parent | Icon | Route | Order |
|----|------|------|--------|------|-------|-------|
| 4 | users | Usuarios | Administración | people | /admin/users | 1 |
| 5 | roles | Roles | Administración | security | /admin/roles | 2 |
| 6 | agencies | Agencias | Administración | business | /admin/agencies | 3 |
| 7 | bets | Apuestas | Operaciones | casino | /operations/bets | 1 |
| 8 | reports | Reportes | Operaciones | assessment | /operations/reports | 2 |

### Permisos (RoleMenuAccess)

**Administrador (8 permisos):**
- Dashboard
- Administración (padre)
- Usuarios, Roles, Agencias (children)
- Operaciones (padre)
- Apuestas, Reportes (children)

**Operador (3 permisos):**
- Dashboard
- Operaciones (padre)
- Apuestas (child)

## 🧪 Cómo Probar la API

### 1. Asignar un rol a un usuario existente

```python
# En Django shell: python manage.py shell
from django.contrib.auth import get_user_model
from apps.authentication.models import Role

User = get_user_model()

# Obtener usuario
user = User.objects.get(username='tu_usuario')

# Asignar rol de Administrador
admin_role = Role.objects.get(code='ADMIN')
user.rol = admin_role
user.save()

print(f"✓ Usuario {user.username} ahora tiene el rol: {user.rol.name}")
```

### 2. Hacer Login y obtener token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "tu_usuario",
    "password": "tu_password"
  }'
```

Respuesta:
```json
{
  "user": {...},
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Login successful"
}
```

### 3. Obtener navegación del usuario

```bash
curl -X GET http://localhost:8000/api/auth/navigation/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

Respuesta esperada para usuario con rol ADMIN:
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@wisebet.com",
    "first_name": "",
    "last_name": "",
    "numero_contacto": null,
    "rol": 1,
    "nombre_completo": "Administrador Principal",
    "created_at": "2026-01-18T20:00:00Z"
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
          "id": 4,
          "name": "Usuarios",
          "code": "users",
          "icon": "people",
          "route": "/admin/users",
          "order": 1,
          "children": []
        },
        {
          "id": 5,
          "name": "Roles",
          "code": "roles",
          "icon": "security",
          "route": "/admin/roles",
          "order": 2,
          "children": []
        },
        {
          "id": 6,
          "name": "Agencias",
          "code": "agencies",
          "icon": "business",
          "route": "/admin/agencies",
          "order": 3,
          "children": []
        }
      ]
    },
    {
      "id": 3,
      "name": "Operaciones",
      "code": "operations",
      "icon": "work",
      "route": null,
      "order": 3,
      "children": [
        {
          "id": 7,
          "name": "Apuestas",
          "code": "bets",
          "icon": "casino",
          "route": "/operations/bets",
          "order": 1,
          "children": []
        },
        {
          "id": 8,
          "name": "Reportes",
          "code": "reports",
          "icon": "assessment",
          "route": "/operations/reports",
          "order": 2,
          "children": []
        }
      ]
    }
  ]
}
```

## 🔍 Lógica de la API

### Flujo de Ejecución

1. **Autenticación**: Verifica que el usuario esté autenticado (JWT token válido)
2. **Verificación de Rol**: Comprueba si `user.rol` existe
3. **Consulta de Permisos**: 
   ```python
   RoleMenuAccess.objects.filter(
       role=user.rol,
       is_active=True,
       menu__is_active=True
   )
   ```
4. **Filtrado de Menús Padre**: Obtiene solo menús sin `parent`
5. **Construcción de Jerarquía**: Para cada padre, obtiene sus children permitidos
6. **Serialización**: Convierte a JSON con estructura anidada
7. **Respuesta**: Retorna user + navigation

### Casos Especiales

- **Usuario sin rol**: Retorna `navigation: []`
- **Rol sin permisos**: Retorna `navigation: []`
- **Menús inactivos**: No se incluyen en la respuesta
- **Permisos inactivos**: No se consideran

## 📝 Gestión de Permisos

### Agregar nuevo menú

```python
from apps.authentication.models import Menu, Role, RoleMenuAccess

# Crear menú
new_menu = Menu.objects.create(
    name='Configuración',
    code='settings',
    icon='tune',
    route='/settings',
    parent=None,  # o especificar un padre
    order=4,
    is_active=True
)

# Asignar a rol
admin_role = Role.objects.get(code='ADMIN')
RoleMenuAccess.objects.create(
    role=admin_role,
    menu=new_menu,
    is_active=True
)
```

### Revocar acceso

```python
# Opción 1: Desactivar (soft delete)
access = RoleMenuAccess.objects.get(role=role, menu=menu)
access.is_active = False
access.save()

# Opción 2: Eliminar permanentemente
access.delete()
```

### Cambiar rol de usuario

```python
user = User.objects.get(username='operador1')
operador_role = Role.objects.get(code='OPERADOR')
user.rol = operador_role
user.save()
```

## 📚 Archivos de Documentación

1. **`rbac_navigation_api_guide.md`** - Guía completa de uso de la API
2. **`rbac_react_integration_guide.md`** - Integración con React
3. **`rbac_models_example.py`** - Ejemplos de modelos y queries
4. **`rbac_api_response_example.json`** - Ejemplo de respuesta JSON
5. **`IMPLEMENTATION_SUMMARY.md`** - Este archivo (resumen completo)

## 🚀 Próximos Pasos Sugeridos

1. **Registrar modelos en Django Admin**
   - Crear `admin.py` para gestionar roles, menús y permisos desde el panel
   
2. **Agregar validaciones**
   - Validar que un menú hijo tenga parent
   - Validar que un menú padre no tenga route si tiene children
   
3. **Crear más roles**
   - Supervisor, Cajero, Gerente, etc.
   
4. **Implementar en React**
   - Seguir la guía en `rbac_react_integration_guide.md`
   - Crear componente de navegación dinámica
   - Proteger rutas según permisos

5. **Testing**
   - Crear tests unitarios para la vista
   - Tests de integración para el flujo completo

## ✅ Checklist de Implementación

- [x] Modelos RBAC creados
- [x] Migraciones aplicadas
- [x] Serializers implementados
- [x] Vista de navegación creada
- [x] URL configurada
- [x] Comando de management creado
- [x] Datos de prueba poblados
- [x] Documentación completa
- [ ] Modelos registrados en Admin
- [ ] Tests unitarios
- [ ] Integración con React

## 🎉 Conclusión

La API de navegación RBAC está **completamente funcional** y lista para usar. Los usuarios recibirán automáticamente solo los menús y secciones a los que tienen acceso según su rol asignado.
