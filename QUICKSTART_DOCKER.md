# 🚀 Inicio Rápido - Docker

## Configuración Básica (Desarrollo/Testing)

### 1. Configurar variables de entorno
```bash
cp .env.example .env
nano .env  # Edita las variables según tu configuración
```

### 2. Desplegar con un solo comando
```bash
./deploy.sh deploy
```

¡Listo! Tu aplicación estará corriendo en `http://localhost`

---

## Comandos Útiles

```bash
# Ver estado
./deploy.sh status

# Ver logs
./deploy.sh logs
./deploy.sh logs backend
./deploy.sh logs nginx

# Crear superusuario
./deploy.sh createsuperuser

# Ejecutar migraciones
./deploy.sh migrate

# Detener servicios
./deploy.sh stop

# Reiniciar servicios
./deploy.sh restart

# Ver ayuda completa
./deploy.sh help
```

---

## Despliegue en Producción (Ubuntu 24.04)

### 1. Instalar Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
nano .env
```

**Importante:** Configura estas variables para producción:
- `DEBUG=False`
- `SECRET_KEY=<genera-una-clave-segura>`
- `ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com`
- `DB_HOST=<ip-de-tu-base-de-datos>`

### 3. Opción A: Sin HTTPS (solo HTTP)
```bash
docker compose up -d
```

### 3. Opción B: Con HTTPS (Recomendado)
```bash
# Obtener certificados SSL
./setup-ssl.sh tu-dominio.com tu-email@ejemplo.com

# Desplegar con HTTPS
docker compose -f docker-compose.prod.yml up -d
```

### 4. Verificar
```bash
./deploy.sh health
./deploy.sh status
```

---

## Estructura de Archivos Docker

```
backend_wisebet/
├── Dockerfile                  # Imagen Docker optimizada con Python 3.12
├── .dockerignore              # Archivos excluidos del build
├── docker-compose.yml         # Configuración para desarrollo
├── docker-compose.prod.yml    # Configuración para producción
├── nginx.conf                 # Nginx para HTTP
├── nginx.prod.conf            # Nginx para HTTPS
├── deploy.sh                  # Script de gestión
├── setup-ssl.sh               # Script para SSL
├── .env.example               # Plantilla de variables
└── README_DOCKER.md           # Documentación completa
```

---

## Acceso a la Aplicación

- **API:** `http://tu-servidor/api/`
- **Admin:** `http://tu-servidor/admin/`
- **Docs:** `http://tu-servidor/api/schema/swagger-ui/`
- **Health:** `http://tu-servidor/health/`

---

## Solución Rápida de Problemas

### Error de conexión a la base de datos
```bash
# Verificar variables de entorno
cat .env | grep DB_

# Si la BD está en el mismo servidor
DB_HOST=host.docker.internal
```

### Ver logs de errores
```bash
./deploy.sh logs backend
```

### Reiniciar todo
```bash
./deploy.sh stop
./deploy.sh start
```

---

## 📚 Documentación Completa

Para más detalles, consulta `README_DOCKER.md`
