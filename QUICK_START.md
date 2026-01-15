# 🚀 Guía de Inicio Rápido - WiseBet Backend

## ✅ Estado del Proyecto

El proyecto está **completamente configurado y listo para usar**:

- ✅ Django REST Framework instalado
- ✅ Autenticación JWT configurada
- ✅ PostgreSQL conectado (base de datos: wisebet)
- ✅ Migraciones aplicadas
- ✅ Usuario de prueba creado
- ✅ CORS configurado

## 🎯 Inicio Rápido (3 pasos)

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Iniciar el servidor
```bash
python manage.py runserver
```

### 3. Probar la API
El servidor estará corriendo en: **http://localhost:8000**

## 🧪 Probar la API Inmediatamente

### Opción 1: Usar curl (desde la terminal)

```bash
# Login con el usuario de prueba
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Opción 2: Usar Postman
1. Importa el archivo `WiseBet_API.postman_collection.json`
2. Usa el endpoint "Login" con las credenciales del usuario de prueba
3. Los tokens se guardarán automáticamente en las variables

### Opción 3: Usar el navegador
Visita: http://localhost:8000/admin/
- Usuario: (crea uno con `python manage.py createsuperuser`)

## 👤 Usuario de Prueba

Ya existe un usuario de prueba creado:
- **Username:** testuser
- **Email:** test@example.com
- **Password:** testpass123

## 📋 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Registrar nuevo usuario |
| `/api/auth/login/` | POST | Iniciar sesión |
| `/api/auth/logout/` | POST | Cerrar sesión |
| `/api/auth/profile/` | GET/PUT | Ver/Actualizar perfil |
| `/api/auth/change-password/` | POST | Cambiar contraseña |
| `/api/auth/token/refresh/` | POST | Refrescar token |
| `/admin/` | GET | Panel de administración |

## 🔧 Comandos Útiles

```bash
# Crear superusuario para el admin
python manage.py createsuperuser

# Crear otro usuario de prueba
python manage.py create_test_user

# Ver todas las rutas disponibles
python manage.py show_urls  # (requiere django-extensions)

# Ejecutar tests
python manage.py test

# Verificar configuración
python test_setup.py
```

## 📁 Archivos de Ayuda

- `README.md` - Documentación completa
- `API_EXAMPLES.py` - Ejemplos de uso de la API
- `WiseBet_API.postman_collection.json` - Colección de Postman
- `test_setup.py` - Script de verificación

## 🔐 Configuración de Base de Datos

La configuración actual en `.env`:
```
DB_NAME=wisebet
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Si necesitas cambiar las credenciales, edita el archivo `.env`

## 🌐 CORS

El proyecto acepta peticiones desde:
- http://localhost:3000 (React)
- http://localhost:4200 (Angular)

Para agregar más orígenes, edita `CORS_ALLOWED_ORIGINS` en `settings.py`

## 📦 Próximos Pasos

1. **Crear tu primer endpoint personalizado:**
   ```bash
   python manage.py startapp mi_app
   ```

2. **Agregar la app a INSTALLED_APPS** en `settings.py`

3. **Crear modelos, serializers y views**

4. **Agregar las URLs** a `config/urls.py`

## 🆘 Solución de Problemas

### El servidor no inicia
```bash
# Verifica que el entorno virtual esté activado
source venv/bin/activate

# Verifica que PostgreSQL esté corriendo
sudo systemctl status postgresql
```

### Error de base de datos
```bash
# Verifica la conexión
python test_setup.py
```

### Reinstalar dependencias
```bash
pip install -r requirements.txt --force-reinstall
```

## 📞 Estructura del Proyecto

```
backend_wisebet/
├── authentication/              # App de autenticación
│   ├── models.py               # Modelo de Usuario
│   ├── serializers.py          # Serializadores
│   ├── views.py                # Vistas de API
│   └── urls.py                 # URLs
├── config/                     # Configuración
│   ├── settings.py             # Configuración principal
│   └── urls.py                 # URLs principales
├── manage.py                   # Comando de Django
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
└── README.md                   # Documentación
```

---

**¡Listo para desarrollar! 🎉**
