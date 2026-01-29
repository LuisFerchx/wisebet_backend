# ✅ Checklist de Despliegue - WiseBet Backend

## Pre-Despliegue

### Servidor Ubuntu 24.04
- [ ] Servidor Ubuntu 24.04 LTS instalado y actualizado
- [ ] Acceso SSH configurado
- [ ] Usuario con permisos sudo
- [ ] Firewall configurado (UFW)
  ```bash
  sudo ufw allow 22/tcp   # SSH
  sudo ufw allow 80/tcp   # HTTP
  sudo ufw allow 443/tcp  # HTTPS
  sudo ufw enable
  ```

### Docker
- [ ] Docker Engine instalado (versión 24.0+)
  ```bash
  docker --version
  ```
- [ ] Docker Compose instalado (versión 2.0+)
  ```bash
  docker compose version
  ```
- [ ] Usuario agregado al grupo docker
  ```bash
  sudo usermod -aG docker $USER
  ```

### Base de Datos PostgreSQL
- [ ] PostgreSQL instalado o servicio en la nube configurado
- [ ] Base de datos creada
- [ ] Usuario de base de datos creado con permisos
- [ ] Conexión verificada desde el servidor
  ```bash
  psql -h <DB_HOST> -U <DB_USER> -d <DB_NAME>
  ```
- [ ] Firewall permite conexiones al puerto 5432 (si es remoto)

### Código Fuente
- [ ] Repositorio clonado en el servidor
  ```bash
  git clone <repo-url>
  cd backend_wisebet
  ```
- [ ] Rama correcta seleccionada (main/production)
  ```bash
  git checkout main
  ```

## Configuración

### Variables de Entorno
- [ ] Archivo `.env` creado desde `.env.example`
  ```bash
  cp .env.example .env
  ```
- [ ] `SECRET_KEY` generado y configurado
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] `DEBUG=False` configurado
- [ ] `ALLOWED_HOSTS` configurado con dominio/IP
- [ ] Variables de base de datos configuradas:
  - [ ] `DB_NAME`
  - [ ] `DB_USER`
  - [ ] `DB_PASSWORD`
  - [ ] `DB_HOST` (usar `host.docker.internal` si está en el mismo servidor)
  - [ ] `DB_PORT`
- [ ] `CORS_ALLOWED_ORIGINS` configurado con orígenes permitidos

### Archivos Docker
- [ ] `Dockerfile` revisado
- [ ] `docker-compose.yml` o `docker-compose.prod.yml` seleccionado
- [ ] `nginx.conf` o `nginx.prod.conf` configurado
- [ ] Scripts tienen permisos de ejecución
  ```bash
  chmod +x deploy.sh setup-ssl.sh
  ```

## Despliegue

### Opción A: Despliegue HTTP (Desarrollo/Testing)
- [ ] Construir imágenes
  ```bash
  docker compose build
  ```
- [ ] Iniciar servicios
  ```bash
  docker compose up -d
  ```
- [ ] Verificar contenedores corriendo
  ```bash
  docker compose ps
  ```
- [ ] Verificar logs sin errores
  ```bash
  docker compose logs
  ```

### Opción B: Despliegue HTTPS (Producción)
- [ ] Dominio apuntando al servidor (DNS configurado)
- [ ] Puerto 80 y 443 abiertos en firewall
- [ ] Obtener certificados SSL
  ```bash
  ./setup-ssl.sh tu-dominio.com tu-email@ejemplo.com
  ```
- [ ] Verificar certificados obtenidos
  ```bash
  ls -la ssl/
  ```
- [ ] Desplegar con configuración de producción
  ```bash
  docker compose -f docker-compose.prod.yml up -d
  ```

### Opción C: Usar Script de Despliegue
- [ ] Ejecutar despliegue automatizado
  ```bash
  ./deploy.sh deploy
  ```

## Post-Despliegue

### Verificación de Servicios
- [ ] Backend respondiendo
  ```bash
  curl http://localhost:8000/api/schema/
  ```
- [ ] Nginx respondiendo
  ```bash
  curl http://localhost/health/
  ```
- [ ] Health checks pasando
  ```bash
  ./deploy.sh health
  ```
- [ ] Logs sin errores críticos
  ```bash
  ./deploy.sh logs
  ```

### Base de Datos
- [ ] Migraciones ejecutadas
  ```bash
  ./deploy.sh migrate
  ```
- [ ] Superusuario creado
  ```bash
  ./deploy.sh createsuperuser
  ```
- [ ] Archivos estáticos recolectados
  ```bash
  ./deploy.sh collectstatic
  ```

### Acceso Web
- [ ] API accesible: `http://tu-servidor/api/`
- [ ] Admin accesible: `http://tu-servidor/admin/`
- [ ] Documentación accesible: `http://tu-servidor/api/schema/swagger-ui/`
- [ ] Login funcional
- [ ] CORS funcionando correctamente

### SSL/HTTPS (si aplica)
- [ ] HTTPS funcionando: `https://tu-dominio.com`
- [ ] Redirección HTTP → HTTPS funcionando
- [ ] Certificado válido (sin advertencias)
- [ ] Renovación automática configurada

## Seguridad

### Configuración de Seguridad
- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` único y seguro
- [ ] Contraseñas seguras para base de datos
- [ ] `.env` NO está en el repositorio
- [ ] Firewall configurado correctamente
- [ ] Solo puertos necesarios abiertos

### Headers de Seguridad
- [ ] HSTS configurado (si usa HTTPS)
- [ ] X-Frame-Options configurado
- [ ] X-Content-Type-Options configurado
- [ ] X-XSS-Protection configurado

### Acceso
- [ ] SSH con autenticación por clave (no contraseña)
- [ ] Acceso root deshabilitado
- [ ] Fail2ban instalado (opcional pero recomendado)

## Monitoreo

### Configuración de Monitoreo
- [ ] Logs configurados
  ```bash
  docker compose logs -f
  ```
- [ ] Health checks funcionando
- [ ] Alertas configuradas (opcional)
- [ ] Backup automático configurado (opcional)

### Métricas
- [ ] Uso de CPU monitoreado
  ```bash
  docker stats
  ```
- [ ] Uso de memoria monitoreado
- [ ] Uso de disco monitoreado
  ```bash
  df -h
  ```

## Backup

### Estrategia de Backup
- [ ] Backup de base de datos configurado
  ```bash
  ./deploy.sh backup
  ```
- [ ] Backup de archivos media (si aplica)
- [ ] Backup de variables de entorno (`.env`)
- [ ] Backup de certificados SSL
- [ ] Frecuencia de backup definida
- [ ] Ubicación de backups segura

## Documentación

### Documentación del Proyecto
- [ ] README actualizado
- [ ] Credenciales documentadas (en lugar seguro)
- [ ] Procedimientos de despliegue documentados
- [ ] Contactos de emergencia documentados
- [ ] Runbook de operaciones creado

## Mantenimiento

### Plan de Mantenimiento
- [ ] Procedimiento de actualización definido
- [ ] Ventana de mantenimiento definida
- [ ] Rollback plan definido
- [ ] Monitoreo post-actualización definido

### Actualizaciones Regulares
- [ ] Actualización de dependencias de Python
- [ ] Actualización de imágenes Docker
- [ ] Actualización del sistema operativo
- [ ] Renovación de certificados SSL

## Testing Post-Despliegue

### Tests Funcionales
- [ ] Login funciona
- [ ] APIs principales responden
- [ ] Admin panel accesible
- [ ] Documentación API accesible
- [ ] CORS funciona con frontend

### Tests de Carga (Opcional)
- [ ] Test de carga básico ejecutado
- [ ] Tiempos de respuesta aceptables
- [ ] Manejo de concurrencia verificado

## Rollback Plan

### En caso de problemas
- [ ] Backup reciente disponible
- [ ] Procedimiento de rollback documentado
  ```bash
  # Detener servicios actuales
  docker compose down
  
  # Restaurar versión anterior
  git checkout <commit-anterior>
  docker compose up -d
  
  # Restaurar base de datos si es necesario
  psql -h $DB_HOST -U $DB_USER $DB_NAME < backup.sql
  ```

## Contactos

### Equipo
- [ ] DevOps: _______________
- [ ] Backend: _______________
- [ ] DBA: _______________
- [ ] Soporte: _______________

## Notas Adicionales

```
Fecha de despliegue: _______________
Versión desplegada: _______________
Desplegado por: _______________
Notas especiales: 
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## ✅ Checklist Rápido

Para despliegue rápido en desarrollo:

```bash
☐ cp .env.example .env
☐ nano .env  # Configurar variables
☐ ./deploy.sh deploy
☐ ./deploy.sh createsuperuser
☐ Verificar: http://localhost/admin/
```

Para despliegue en producción:

```bash
☐ Configurar DNS
☐ cp .env.example .env
☐ nano .env  # DEBUG=False, configurar todo
☐ ./setup-ssl.sh dominio.com email@ejemplo.com
☐ docker compose -f docker-compose.prod.yml up -d
☐ ./deploy.sh createsuperuser
☐ Verificar: https://dominio.com/admin/
```
