# Ejemplos de Configuración .env

Este archivo contiene ejemplos de configuración del archivo `.env` para diferentes escenarios.

## 📋 Escenario 1: Desarrollo Local

```env
# Django Settings
SECRET_KEY=django-insecure-dev-key-change-in-production-abc123xyz
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL local)
DB_NAME=wisebet_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=host.docker.internal
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200,http://127.0.0.1:3000,http://127.0.0.1:4200
```

**Notas:**
- `DEBUG=True` para desarrollo
- `DB_HOST=host.docker.internal` para conectarse a PostgreSQL en el host
- CORS permite localhost en varios puertos

---

## 🧪 Escenario 2: Servidor de Testing

```env
# Django Settings
SECRET_KEY=your-unique-secret-key-for-testing-server-xyz789
DEBUG=False
ALLOWED_HOSTS=testing.wisebet.com,192.168.1.100

# Database Configuration (PostgreSQL en servidor remoto)
DB_NAME=wisebet_testing
DB_USER=wisebet_test_user
DB_PASSWORD=SecureTestPassword123!
DB_HOST=192.168.1.50
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://testing.wisebet.com,https://testing.wisebet.com
```

**Notas:**
- `DEBUG=False` incluso en testing
- `DB_HOST` apunta a servidor de BD remoto
- ALLOWED_HOSTS incluye dominio de testing e IP

---

## 🚀 Escenario 3: Producción (Base de datos en el mismo servidor)

```env
# Django Settings
SECRET_KEY=super-secure-random-key-generated-for-production-abc123xyz789
DEBUG=False
ALLOWED_HOSTS=wisebet.com,www.wisebet.com,api.wisebet.com

# Database Configuration (PostgreSQL en el mismo servidor)
DB_NAME=wisebet_production
DB_USER=wisebet_prod_user
DB_PASSWORD=VerySecureProductionPassword456!@#
DB_HOST=host.docker.internal
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://wisebet.com,https://www.wisebet.com,https://app.wisebet.com
```

**Notas:**
- `SECRET_KEY` único y complejo
- `DEBUG=False` obligatorio
- Solo HTTPS en CORS
- `DB_HOST=host.docker.internal` para BD local

---

## ☁️ Escenario 4: Producción (Base de datos en la nube - AWS RDS)

```env
# Django Settings
SECRET_KEY=production-secret-key-aws-deployment-xyz123abc456
DEBUG=False
ALLOWED_HOSTS=api.wisebet.com,wisebet.com,www.wisebet.com

# Database Configuration (AWS RDS PostgreSQL)
DB_NAME=wisebet_prod
DB_USER=wisebet_admin
DB_PASSWORD=AWSRDSSecurePassword789!@#$
DB_HOST=wisebet-db.c9akl5nqvqwe.us-east-1.rds.amazonaws.com
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://wisebet.com,https://www.wisebet.com,https://app.wisebet.com
```

**Notas:**
- `DB_HOST` es el endpoint de RDS
- Asegúrate de que el security group de RDS permita conexiones desde tu servidor

---

## 🔵 Escenario 5: Producción (Base de datos en Azure)

```env
# Django Settings
SECRET_KEY=azure-production-secret-key-unique-xyz789abc123
DEBUG=False
ALLOWED_HOSTS=wisebet.azurewebsites.net,wisebet.com,www.wisebet.com

# Database Configuration (Azure Database for PostgreSQL)
DB_NAME=wisebet_prod
DB_USER=wisebet_admin@wisebet-db-server
DB_PASSWORD=AzureSecurePassword123!@#
DB_HOST=wisebet-db-server.postgres.database.azure.com
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://wisebet.com,https://www.wisebet.com,https://app.wisebet.com
```

**Notas:**
- Usuario de Azure incluye `@server-name`
- `DB_HOST` es el FQDN del servidor Azure

---

## 🐳 Escenario 6: Desarrollo con Docker Compose completo (con BD)

Si decides dockerizar también la base de datos para desarrollo:

```env
# Django Settings
SECRET_KEY=dev-docker-compose-secret-key-abc123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL en Docker Compose)
DB_NAME=wisebet_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200
```

**Notas:**
- `DB_HOST=db` (nombre del servicio en docker-compose.yml)
- Necesitarías agregar un servicio `db` en docker-compose.yml

---

## 🔐 Generación de SECRET_KEY

Para generar un SECRET_KEY seguro:

### Método 1: Python
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Método 2: OpenSSL
```bash
openssl rand -base64 50
```

### Método 3: Online (no recomendado para producción)
- https://djecrety.ir/

---

## 📝 Notas Importantes

### Seguridad
- ⚠️ **NUNCA** commitees el archivo `.env` al repositorio
- ✅ Usa contraseñas diferentes para cada ambiente
- ✅ Rota las credenciales regularmente
- ✅ Usa `DEBUG=False` en producción SIEMPRE

### ALLOWED_HOSTS
- Debe incluir todos los dominios desde los que se accederá
- Separar múltiples hosts con comas (sin espacios)
- Incluir tanto dominio con y sin `www` si es necesario

### DB_HOST
- `host.docker.internal` → BD en el mismo servidor (fuera de Docker)
- `192.168.x.x` → BD en servidor local de red
- `db.example.com` → BD en servidor remoto
- `db` → BD en otro contenedor Docker (mismo docker-compose)

### CORS_ALLOWED_ORIGINS
- En producción, usar solo HTTPS
- Separar múltiples orígenes con comas (sin espacios)
- No incluir trailing slash
- Incluir protocolo completo (http:// o https://)

---

## 🧪 Validación de Configuración

Para validar tu configuración:

```bash
# 1. Verificar que Django puede leer las variables
docker compose exec backend python manage.py check

# 2. Verificar conexión a la base de datos
docker compose exec backend python manage.py check --database default

# 3. Verificar configuración de Django
docker compose exec backend python manage.py diffsettings
```

---

## 🔄 Migración entre Ambientes

### De Desarrollo a Testing
1. Cambiar `DEBUG=False`
2. Generar nuevo `SECRET_KEY`
3. Actualizar `ALLOWED_HOSTS`
4. Actualizar credenciales de BD
5. Actualizar `CORS_ALLOWED_ORIGINS`

### De Testing a Producción
1. Generar nuevo `SECRET_KEY` único
2. Usar contraseñas más seguras
3. Configurar dominio real en `ALLOWED_HOSTS`
4. Usar solo HTTPS en `CORS_ALLOWED_ORIGINS`
5. Verificar configuración de BD de producción

---

## 📞 Troubleshooting

### Error: "Invalid HTTP_HOST header"
**Solución:** Agrega el host a `ALLOWED_HOSTS`

### Error: "CORS policy: No 'Access-Control-Allow-Origin'"
**Solución:** Agrega el origen a `CORS_ALLOWED_ORIGINS`

### Error: "could not connect to server"
**Solución:** Verifica `DB_HOST`, `DB_PORT` y firewall

### Error: "FATAL: password authentication failed"
**Solución:** Verifica `DB_USER` y `DB_PASSWORD`

---

**Última actualización:** 2026-01-28  
**Compatible con:** Django 5.0+, PostgreSQL 12+
