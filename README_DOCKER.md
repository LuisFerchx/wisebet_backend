# Guía de Despliegue con Docker - WiseBet Backend

Esta guía te ayudará a desplegar el backend de WiseBet usando Docker en un servidor Ubuntu 24.04.

## 📋 Requisitos Previos

- Ubuntu 24.04 LTS
- Docker Engine 24.0+
- Docker Compose 2.0+
- Base de datos PostgreSQL externa (no dockerizada)

## 🔧 Instalación de Docker en Ubuntu 24.04

Si aún no tienes Docker instalado, ejecuta:

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y ca-certificates curl gnupg lsb-release

# Agregar la clave GPG oficial de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verificar instalación
sudo docker --version
sudo docker compose version

# Agregar tu usuario al grupo docker (opcional, para no usar sudo)
sudo usermod -aG docker $USER
newgrp docker
```

## ⚙️ Configuración

### 1. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
cp .env.example .env
nano .env
```

**Importante:** Configura `DB_HOST` para conectarte a tu base de datos externa:

```env
# Para base de datos en el mismo servidor (fuera de Docker)
DB_HOST=host.docker.internal

# Para base de datos en otro servidor
DB_HOST=192.168.1.100  # IP de tu servidor de BD

# Para base de datos en la nube
DB_HOST=tu-db.postgres.database.azure.com
```

### 2. Configurar ALLOWED_HOSTS

En tu archivo `.env`, actualiza `ALLOWED_HOSTS` con tu dominio o IP:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com,tu-ip-publica
```

## 🚀 Despliegue

### Construcción y Ejecución

```bash
# Construir las imágenes
docker compose build

# Iniciar los servicios en segundo plano
docker compose up -d

# Ver los logs
docker compose logs -f

# Ver logs solo del backend
docker compose logs -f backend

# Ver logs solo de nginx
docker compose logs -f nginx
```

### Verificar el Estado

```bash
# Ver servicios en ejecución
docker compose ps

# Verificar health checks
docker compose ps --format "table {{.Name}}\t{{.Status}}"
```

## 🔍 Comandos Útiles

### Gestión de Contenedores

```bash
# Detener los servicios
docker compose down

# Detener y eliminar volúmenes
docker compose down -v

# Reiniciar un servicio específico
docker compose restart backend
docker compose restart nginx

# Ver logs en tiempo real
docker compose logs -f --tail=100
```

### Ejecutar Comandos Django

```bash
# Crear superusuario
docker compose exec backend python manage.py createsuperuser

# Ejecutar migraciones manualmente
docker compose exec backend python manage.py migrate

# Recolectar archivos estáticos
docker compose exec backend python manage.py collectstatic --noinput

# Acceder al shell de Django
docker compose exec backend python manage.py shell

# Acceder al shell del contenedor
docker compose exec backend bash
```

### Base de Datos

```bash
# Conectarse a la base de datos desde el contenedor
docker compose exec backend psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```

## 🌐 Acceso a la Aplicación

Una vez desplegado, tu aplicación estará disponible en:

- **API Backend:** `http://tu-servidor/api/`
- **Admin Django:** `http://tu-servidor/admin/`
- **Documentación API:** `http://tu-servidor/api/schema/swagger-ui/`
- **Health Check:** `http://tu-servidor/health/`

## 🔒 Configuración de Producción

### 1. Configurar HTTPS con SSL/TLS

Para producción, debes configurar HTTPS. Actualiza `nginx.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... resto de la configuración
}

server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

Y actualiza `docker-compose.yml` para montar los certificados:

```yaml
nginx:
  volumes:
    - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    - ./ssl:/etc/nginx/ssl:ro  # Añadir esta línea
```

### 2. Usar Let's Encrypt (Certbot)

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com
```

### 3. Configurar Firewall

```bash
# Permitir tráfico HTTP y HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📊 Monitoreo

### Ver Uso de Recursos

```bash
# Ver estadísticas de contenedores
docker stats

# Ver uso de espacio en disco
docker system df
```

### Logs

```bash
# Ver logs de Nginx
docker compose logs nginx

# Ver logs del backend
docker compose logs backend

# Seguir logs en tiempo real
docker compose logs -f
```

## 🔄 Actualización de la Aplicación

```bash
# 1. Detener los servicios
docker compose down

# 2. Actualizar el código (git pull, etc.)
git pull origin main

# 3. Reconstruir las imágenes
docker compose build --no-cache

# 4. Iniciar los servicios
docker compose up -d

# 5. Verificar que todo funcione
docker compose ps
docker compose logs -f
```

## 🐛 Solución de Problemas

### El backend no puede conectarse a la base de datos

1. Verifica que `DB_HOST` esté correctamente configurado en `.env`
2. Si la BD está en el mismo servidor, usa `host.docker.internal`
3. Verifica que el firewall permita la conexión al puerto de PostgreSQL
4. Prueba la conexión desde el contenedor:

```bash
docker compose exec backend python manage.py check --database default
```

### Error 502 Bad Gateway

```bash
# Verificar que el backend esté corriendo
docker compose ps backend

# Ver logs del backend
docker compose logs backend

# Reiniciar el backend
docker compose restart backend
```

### Archivos estáticos no se cargan

```bash
# Recolectar archivos estáticos
docker compose exec backend python manage.py collectstatic --noinput

# Verificar permisos
docker compose exec backend ls -la /app/staticfiles/
```

## 📝 Notas Importantes

1. **Base de Datos Externa:** Este setup asume que tienes una base de datos PostgreSQL corriendo fuera de Docker. Asegúrate de que sea accesible desde los contenedores.

2. **Seguridad:** 
   - Cambia `SECRET_KEY` en producción
   - Usa `DEBUG=False` en producción
   - Configura `ALLOWED_HOSTS` correctamente
   - Usa contraseñas seguras para la base de datos

3. **Backups:** Asegúrate de hacer backups regulares de:
   - Base de datos
   - Archivos media (si los usas)
   - Variables de entorno (`.env`)

4. **Escalabilidad:** Para escalar, puedes aumentar el número de workers de Gunicorn en el `Dockerfile`:
   ```bash
   --workers 8  # Aumentar según CPU disponible
   ```

## 🆘 Soporte

Si encuentras problemas, revisa:
- Logs de Docker: `docker compose logs`
- Logs de Nginx: `docker compose logs nginx`
- Logs del backend: `docker compose logs backend`
- Estado de los contenedores: `docker compose ps`
