# WiseBet Backend - Django REST Framework with JWT Authentication

Este proyecto es un backend desarrollado con Django REST Framework que incluye autenticación JWT y está conectado a una base de datos PostgreSQL.

## Características

- ✅ Django 5.0.1
- ✅ Django REST Framework 3.14.0
- ✅ Autenticación JWT (Simple JWT)
- ✅ PostgreSQL Database
- ✅ CORS Headers configurado
- ✅ Modelo de Usuario personalizado
- ✅ Endpoints de autenticación completos

## Requisitos Previos

- Python 3.8+
- PostgreSQL
- pip
- virtualenv

## Configuración de la Base de Datos

Asegúrate de tener PostgreSQL instalado y crea la base de datos:

```bash
# Accede a PostgreSQL
sudo -u postgres psql

# Crea la base de datos
CREATE DATABASE wisebet;

# Crea un usuario (opcional, si no usas el usuario postgres por defecto)
CREATE USER tu_usuario WITH PASSWORD 'tu_contraseña';

# Otorga privilegios
GRANT ALL PRIVILEGES ON DATABASE wisebet TO tu_usuario;

# Sal de PostgreSQL
\q
```

## Instalación

1. **Activa el entorno virtual:**
```bash
source venv/bin/activate
```

2. **Las dependencias ya están instaladas, pero si necesitas reinstalarlas:**
```bash
pip install -r requirements.txt
```

3. **Configura las variables de entorno:**

Edita el archivo `.env` con tus credenciales de PostgreSQL:
```
DB_NAME=wisebet
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

4. **Ejecuta las migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crea un superusuario:**
```bash
python manage.py createsuperuser
```

6. **Ejecuta el servidor:**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Endpoints de API

### Autenticación

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Registro de usuario | No |
| POST | `/api/auth/login/` | Inicio de sesión | No |
| POST | `/api/auth/logout/` | Cerrar sesión | Sí |
| GET/PUT | `/api/auth/profile/` | Ver/Actualizar perfil | Sí |
| POST | `/api/auth/change-password/` | Cambiar contraseña | Sí |
| POST | `/api/auth/token/refresh/` | Refrescar token | No |

### Ejemplos de Uso

#### 1. Registro de Usuario
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_test",
    "email": "test@example.com",
    "password": "contraseña_segura123",
    "password2": "contraseña_segura123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Respuesta:
```json
{
  "user": {
    "id": 1,
    "username": "usuario_test",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "User registered successfully"
}
```

#### 2. Inicio de Sesión
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_test",
    "password": "contraseña_segura123"
  }'
```

#### 3. Acceder al Perfil (con token)
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

#### 4. Refrescar Token
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "TU_REFRESH_TOKEN"
  }'
```

## Estructura del Proyecto

```
backend_wisebet/
├── authentication/          # App de autenticación
│   ├── models.py           # Modelo de Usuario personalizado
│   ├── serializers.py      # Serializadores
│   ├── views.py            # Vistas de API
│   ├── urls.py             # URLs de autenticación
│   └── admin.py            # Configuración del admin
├── config/                 # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .env                    # Variables de entorno
└── README.md
```

## Configuración JWT

Los tokens JWT están configurados con:
- **Access Token Lifetime**: 60 minutos
- **Refresh Token Lifetime**: 1 día
- **Algorithm**: HS256

Puedes modificar estos valores en `settings.py` en la sección `SIMPLE_JWT`.

## Panel de Administración

Accede al panel de administración de Django en:
```
http://localhost:8000/admin/
```

Usa las credenciales del superusuario que creaste.

## CORS

El proyecto está configurado para aceptar peticiones desde:
- `http://localhost:3000` (React)
- `http://localhost:4200` (Angular)

Puedes modificar estos orígenes en `settings.py` en la variable `CORS_ALLOWED_ORIGINS`.

## Desarrollo

Para desarrollo, asegúrate de que `DEBUG=True` en tu archivo `.env`.

Para producción, cambia a `DEBUG=False` y configura `ALLOWED_HOSTS` apropiadamente.

## Solución de Problemas

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL esté corriendo: `sudo systemctl status postgresql`
- Verifica las credenciales en el archivo `.env`
- Asegúrate de que la base de datos `wisebet` existe

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Reinstalar dependencias
```bash
pip install -r requirements.txt --force-reinstall
```

## Licencia

Este proyecto es de código abierto.
