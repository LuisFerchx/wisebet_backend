# Arquitectura de Despliegue Docker - WiseBet Backend

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Cliente                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS (Puerto 80/443)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Nginx Container                             │
│  - Proxy Inverso                                             │
│  - Manejo de SSL/TLS                                         │
│  - Servir archivos estáticos                                 │
│  - Load Balancing (futuro)                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP (Puerto 8000)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Django Backend Container                        │
│  - Python 3.12                                               │
│  - Gunicorn (4 workers)                                      │
│  - Django REST Framework                                     │
│  - JWT Authentication                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ PostgreSQL Protocol (Puerto 5432)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL Database (Externa)                   │
│  - NO dockerizada                                            │
│  - Puede estar en:                                           │
│    * Mismo servidor (host.docker.internal)                   │
│    * Servidor remoto                                         │
│    * Servicio en la nube (AWS RDS, Azure, etc.)             │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

### Request Flow (Cliente → Backend)
```
1. Cliente → Nginx (Puerto 80/443)
2. Nginx → Backend (Puerto 8000)
3. Backend → PostgreSQL (Puerto 5432)
4. PostgreSQL → Backend (Respuesta)
5. Backend → Nginx (Respuesta)
6. Nginx → Cliente (Respuesta)
```

### Static Files Flow
```
Cliente → Nginx → /app/staticfiles/ (Volumen compartido)
```

## 🐳 Contenedores Docker

### 1. Backend Container
- **Imagen Base:** `python:3.12-slim`
- **Puerto Expuesto:** 8000
- **Servidor:** Gunicorn
- **Workers:** 4 workers, 2 threads cada uno
- **Usuario:** appuser (no-root)
- **Volúmenes:**
  - `static_volume:/app/staticfiles`
  - `media_volume:/app/mediafiles`

### 2. Nginx Container
- **Imagen Base:** `nginx:1.25-alpine`
- **Puertos Expuestos:** 80, 443
- **Volúmenes:**
  - `nginx.conf` → `/etc/nginx/conf.d/default.conf`
  - `static_volume:/app/staticfiles` (read-only)
  - `media_volume:/app/mediafiles` (read-only)
  - `ssl/` → `/etc/nginx/ssl/` (producción)

### 3. Certbot Container (Producción)
- **Imagen Base:** `certbot/certbot:latest`
- **Función:** Renovación automática de certificados SSL
- **Frecuencia:** Cada 12 horas

## 📦 Volúmenes Docker

```
static_volume    → Archivos estáticos de Django
media_volume     → Archivos subidos por usuarios
certbot_www      → Validación ACME de Let's Encrypt
```

## 🌐 Red Docker

```
wisebet_network (bridge)
├── backend (wisebet_backend)
├── nginx (wisebet_nginx)
└── certbot (wisebet_certbot) [solo producción]
```

## 🔒 Seguridad

### Implementada
- ✅ Usuario no-root en contenedor backend
- ✅ Volúmenes read-only donde sea posible
- ✅ Health checks para todos los servicios
- ✅ SSL/TLS con Let's Encrypt
- ✅ Headers de seguridad en Nginx
- ✅ CORS configurado
- ✅ Variables de entorno para secretos

### Recomendaciones Adicionales
- 🔐 Usar secrets de Docker Swarm/Kubernetes
- 🔐 Implementar rate limiting en Nginx
- 🔐 Configurar fail2ban
- 🔐 Usar firewall (UFW)
- 🔐 Implementar logging centralizado

## 📊 Recursos

### Desarrollo
```yaml
Backend:
  CPU: ~0.5 cores
  RAM: ~512MB
  
Nginx:
  CPU: ~0.1 cores
  RAM: ~50MB
```

### Producción (Recomendado)
```yaml
Backend:
  CPU: 2-4 cores
  RAM: 2-4GB
  Workers: 2 * CPU_CORES + 1
  
Nginx:
  CPU: 1 core
  RAM: 256MB
```

## 🔄 Escalabilidad

### Horizontal (Múltiples instancias)
```yaml
backend:
  deploy:
    replicas: 3
```

### Vertical (Más recursos)
```bash
# Aumentar workers en Dockerfile
--workers 8 --threads 4
```

## 📝 Variables de Entorno Críticas

```env
# Django
SECRET_KEY=<secreto>
DEBUG=False
ALLOWED_HOSTS=dominio.com

# Database
DB_HOST=host.docker.internal  # o IP externa
DB_NAME=wisebet_db
DB_USER=wisebet_user
DB_PASSWORD=<password>

# CORS
CORS_ALLOWED_ORIGINS=https://dominio.com
```

## 🚀 Comandos de Despliegue

### Desarrollo
```bash
docker compose up -d
```

### Producción
```bash
docker compose -f docker-compose.prod.yml up -d
```

### Con Script
```bash
./deploy.sh deploy
```

## 📈 Monitoreo

### Health Checks
- Backend: `http://localhost:8000/api/schema/`
- Nginx: `http://localhost/health/`

### Logs
```bash
docker compose logs -f backend
docker compose logs -f nginx
```

### Métricas
```bash
docker stats
```

## 🔧 Mantenimiento

### Backups
```bash
./deploy.sh backup
```

### Actualizaciones
```bash
./deploy.sh update
```

### Limpieza
```bash
docker system prune -a
```

## 📚 Referencias

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)
