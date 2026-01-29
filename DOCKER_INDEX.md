# 📚 Índice de Documentación Docker - WiseBet Backend

Bienvenido a la documentación de despliegue con Docker para WiseBet Backend. Esta guía te ayudará a encontrar rápidamente la información que necesitas.

## 🚀 Inicio Rápido

**¿Primera vez desplegando?** → Lee [`QUICKSTART_DOCKER.md`](QUICKSTART_DOCKER.md)

**Comando más rápido:**
```bash
./deploy.sh deploy
```

---

## 📖 Documentación Disponible

### 1. 🎯 [QUICKSTART_DOCKER.md](QUICKSTART_DOCKER.md)
**Para:** Desarrolladores que quieren desplegar rápidamente  
**Contenido:**
- Comandos esenciales
- Configuración básica
- Despliegue en 3 pasos
- Solución rápida de problemas

**Lee esto si:** Quieres desplegar lo más rápido posible

---

### 2. 📘 [README_DOCKER.md](README_DOCKER.md)
**Para:** Guía completa de despliegue  
**Contenido:**
- Instalación de Docker en Ubuntu 24.04
- Configuración detallada
- Comandos útiles
- Configuración de producción con HTTPS
- Troubleshooting completo
- Mejores prácticas

**Lee esto si:** Necesitas entender todo el proceso de despliegue

---

### 3. 🏗️ [ARCHITECTURE_DOCKER.md](ARCHITECTURE_DOCKER.md)
**Para:** DevOps y arquitectos  
**Contenido:**
- Diagrama de arquitectura
- Flujo de datos
- Configuración de contenedores
- Seguridad
- Escalabilidad
- Monitoreo

**Lee esto si:** Necesitas entender la arquitectura completa

---

### 4. ✅ [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
**Para:** Checklist de despliegue paso a paso  
**Contenido:**
- Pre-requisitos
- Configuración
- Despliegue
- Post-despliegue
- Seguridad
- Monitoreo
- Backup
- Rollback plan

**Lee esto si:** Vas a hacer un despliegue a producción

---

## 🔧 Archivos de Configuración

### Archivos Docker

| Archivo | Propósito | Cuándo usar |
|---------|-----------|-------------|
| `Dockerfile` | Imagen Docker del backend | Siempre (automático) |
| `docker-compose.yml` | Configuración para desarrollo | Desarrollo/Testing |
| `docker-compose.prod.yml` | Configuración para producción | Producción con HTTPS |
| `.dockerignore` | Archivos excluidos del build | Siempre (automático) |

### Archivos Nginx

| Archivo | Propósito | Cuándo usar |
|---------|-----------|-------------|
| `nginx.conf` | Nginx para HTTP | Desarrollo/Testing |
| `nginx.prod.conf` | Nginx para HTTPS | Producción |

### Scripts de Utilidad

| Script | Propósito | Uso |
|--------|-----------|-----|
| `deploy.sh` | Gestión de despliegue | `./deploy.sh [comando]` |
| `setup-ssl.sh` | Obtener certificados SSL | `./setup-ssl.sh dominio.com email@ejemplo.com` |

### Configuración

| Archivo | Propósito |
|---------|-----------|
| `.env.example` | Plantilla de variables de entorno |
| `.env` | Variables de entorno (crear desde .env.example) |

---

## 🎓 Guías por Escenario

### Escenario 1: Desarrollo Local
```bash
# 1. Configurar
cp .env.example .env
nano .env  # Configurar DB_HOST=host.docker.internal

# 2. Desplegar
./deploy.sh deploy

# 3. Acceder
http://localhost/admin/
```

**Documentación:** [`QUICKSTART_DOCKER.md`](QUICKSTART_DOCKER.md)

---

### Escenario 2: Servidor de Testing (HTTP)
```bash
# 1. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Configurar
cp .env.example .env
nano .env  # DEBUG=False, configurar variables

# 3. Desplegar
docker compose up -d

# 4. Crear superusuario
./deploy.sh createsuperuser
```

**Documentación:** [`README_DOCKER.md`](README_DOCKER.md) → Sección "Despliegue"

---

### Escenario 3: Producción (HTTPS)
```bash
# 1. Configurar DNS
# Apuntar dominio.com a la IP del servidor

# 2. Configurar variables
cp .env.example .env
nano .env  # DEBUG=False, SECRET_KEY único, etc.

# 3. Obtener SSL
./setup-ssl.sh dominio.com email@ejemplo.com

# 4. Desplegar
docker compose -f docker-compose.prod.yml up -d

# 5. Verificar
./deploy.sh health
```

**Documentación:** 
- [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) - Checklist completo
- [`README_DOCKER.md`](README_DOCKER.md) → Sección "Configuración de Producción"

---

## 🔍 Búsqueda Rápida

### ¿Cómo...?

| Pregunta | Respuesta | Documento |
|----------|-----------|-----------|
| ¿Instalar Docker en Ubuntu 24.04? | Ver sección "Instalación de Docker" | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Configurar variables de entorno? | Ver `.env.example` y sección "Configuración" | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Obtener certificados SSL? | Usar `./setup-ssl.sh` | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Ver logs? | `./deploy.sh logs` | [`QUICKSTART_DOCKER.md`](QUICKSTART_DOCKER.md) |
| ¿Hacer backup? | `./deploy.sh backup` | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Actualizar la aplicación? | `./deploy.sh update` | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Conectar a BD externa? | Configurar `DB_HOST` en `.env` | [`README_DOCKER.md`](README_DOCKER.md) |
| ¿Escalar la aplicación? | Ver sección "Escalabilidad" | [`ARCHITECTURE_DOCKER.md`](ARCHITECTURE_DOCKER.md) |

---

## 🆘 Solución de Problemas

### Problemas Comunes

| Problema | Solución | Documento |
|----------|----------|-----------|
| Error de conexión a BD | Verificar `DB_HOST` y firewall | [`README_DOCKER.md`](README_DOCKER.md) → Troubleshooting |
| 502 Bad Gateway | Ver logs del backend | [`README_DOCKER.md`](README_DOCKER.md) → Troubleshooting |
| Archivos estáticos no cargan | Ejecutar `collectstatic` | [`README_DOCKER.md`](README_DOCKER.md) → Troubleshooting |
| SSL no funciona | Verificar certificados | [`README_DOCKER.md`](README_DOCKER.md) → Configuración SSL |

**Documentación completa:** [`README_DOCKER.md`](README_DOCKER.md) → Sección "Solución de Problemas"

---

## 📋 Comandos Más Usados

```bash
# Despliegue completo
./deploy.sh deploy

# Ver estado
./deploy.sh status

# Ver logs
./deploy.sh logs
./deploy.sh logs backend

# Crear superusuario
./deploy.sh createsuperuser

# Ejecutar migraciones
./deploy.sh migrate

# Actualizar aplicación
./deploy.sh update

# Verificar salud
./deploy.sh health

# Detener servicios
./deploy.sh stop

# Ver ayuda
./deploy.sh help
```

---

## 🔐 Seguridad

**Checklist de seguridad:** [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) → Sección "Seguridad"

**Configuración de seguridad:** [`ARCHITECTURE_DOCKER.md`](ARCHITECTURE_DOCKER.md) → Sección "Seguridad"

---

## 📊 Arquitectura

**Diagrama completo:** [`ARCHITECTURE_DOCKER.md`](ARCHITECTURE_DOCKER.md)

**Resumen:**
```
Cliente → Nginx (80/443) → Backend (8000) → PostgreSQL (5432)
```

---

## 🎯 Próximos Pasos

1. **Primera vez:** Lee [`QUICKSTART_DOCKER.md`](QUICKSTART_DOCKER.md)
2. **Despliegue completo:** Lee [`README_DOCKER.md`](README_DOCKER.md)
3. **Producción:** Usa [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)
4. **Entender arquitectura:** Lee [`ARCHITECTURE_DOCKER.md`](ARCHITECTURE_DOCKER.md)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la sección de troubleshooting en [`README_DOCKER.md`](README_DOCKER.md)
2. Verifica los logs: `./deploy.sh logs`
3. Consulta el checklist: [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)

---

## 📝 Notas Importantes

- ⚠️ **Base de datos:** Este setup NO dockeriza la base de datos. Debes tener PostgreSQL corriendo externamente.
- 🔒 **Seguridad:** Siempre usa `DEBUG=False` y `SECRET_KEY` único en producción.
- 📦 **Backups:** Configura backups regulares de tu base de datos.
- 🔄 **Actualizaciones:** Usa `./deploy.sh update` para actualizar la aplicación.

---

**Versión:** 1.0  
**Última actualización:** 2026-01-28  
**Compatible con:** Ubuntu 24.04, Docker 24.0+, Python 3.12
