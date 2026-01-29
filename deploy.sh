#!/bin/bash

# Script de utilidad para gestionar el despliegue de WiseBet Backend con Docker
# Uso: ./deploy.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Verificar que Docker esté instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor, instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor, instala Docker Compose primero."
        exit 1
    fi
    
    print_success "Docker y Docker Compose están instalados"
}

# Verificar archivo .env
check_env() {
    if [ ! -f .env ]; then
        print_warning "Archivo .env no encontrado"
        print_info "Copiando .env.example a .env..."
        cp .env.example .env
        print_warning "Por favor, edita el archivo .env con tus configuraciones antes de continuar"
        exit 1
    fi
    print_success "Archivo .env encontrado"
}

# Construir imágenes
build() {
    print_info "Construyendo imágenes Docker..."
    docker compose build --no-cache
    print_success "Imágenes construidas exitosamente"
}

# Iniciar servicios
start() {
    print_info "Iniciando servicios..."
    docker compose up -d
    print_success "Servicios iniciados"
    print_info "Esperando que los servicios estén listos..."
    sleep 5
    status
}

# Detener servicios
stop() {
    print_info "Deteniendo servicios..."
    docker compose down
    print_success "Servicios detenidos"
}

# Reiniciar servicios
restart() {
    print_info "Reiniciando servicios..."
    docker compose restart
    print_success "Servicios reiniciados"
}

# Ver estado de servicios
status() {
    print_info "Estado de los servicios:"
    docker compose ps
}

# Ver logs
logs() {
    if [ -z "$1" ]; then
        docker compose logs -f --tail=100
    else
        docker compose logs -f --tail=100 "$1"
    fi
}

# Ejecutar migraciones
migrate() {
    print_info "Ejecutando migraciones..."
    docker compose exec backend python manage.py migrate
    print_success "Migraciones completadas"
}

# Crear superusuario
createsuperuser() {
    print_info "Creando superusuario..."
    docker compose exec backend python manage.py createsuperuser
}

# Recolectar archivos estáticos
collectstatic() {
    print_info "Recolectando archivos estáticos..."
    docker compose exec backend python manage.py collectstatic --noinput
    print_success "Archivos estáticos recolectados"
}

# Despliegue completo
deploy() {
    print_info "Iniciando despliegue completo..."
    check_docker
    check_env
    build
    start
    migrate
    collectstatic
    print_success "¡Despliegue completado exitosamente!"
    print_info "La aplicación está disponible en http://localhost"
}

# Actualizar aplicación
update() {
    print_info "Actualizando aplicación..."
    stop
    print_info "Descargando últimos cambios..."
    git pull origin main || print_warning "No se pudo hacer git pull, continuando..."
    build
    start
    migrate
    collectstatic
    print_success "¡Actualización completada!"
}

# Limpiar todo
clean() {
    print_warning "Esto eliminará todos los contenedores, volúmenes e imágenes"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Limpiando..."
        docker compose down -v
        docker system prune -af
        print_success "Limpieza completada"
    else
        print_info "Operación cancelada"
    fi
}

# Backup de base de datos (desde contenedor)
backup() {
    print_info "Creando backup de la base de datos..."
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker compose exec -T backend pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > "$BACKUP_FILE"
    print_success "Backup creado: $BACKUP_FILE"
}

# Shell de Django
shell() {
    print_info "Abriendo shell de Django..."
    docker compose exec backend python manage.py shell
}

# Bash del contenedor
bash() {
    print_info "Abriendo bash del contenedor backend..."
    docker compose exec backend bash
}

# Health check
health() {
    print_info "Verificando salud de los servicios..."
    
    # Verificar backend
    if curl -f http://localhost/health/ &> /dev/null; then
        print_success "Nginx está respondiendo"
    else
        print_error "Nginx no está respondiendo"
    fi
    
    # Verificar API
    if curl -f http://localhost/api/schema/ &> /dev/null; then
        print_success "Backend API está respondiendo"
    else
        print_error "Backend API no está respondiendo"
    fi
}

# Mostrar ayuda
help() {
    cat << EOF
WiseBet Backend - Script de Gestión Docker

Uso: ./deploy.sh [comando]

Comandos disponibles:

  deploy          Despliegue completo (build, start, migrate, collectstatic)
  update          Actualizar aplicación (pull, build, restart, migrate)
  
  build           Construir imágenes Docker
  start           Iniciar servicios
  stop            Detener servicios
  restart         Reiniciar servicios
  status          Ver estado de servicios
  
  logs [servicio] Ver logs (opcional: backend, nginx)
  health          Verificar salud de los servicios
  
  migrate         Ejecutar migraciones de Django
  collectstatic   Recolectar archivos estáticos
  createsuperuser Crear superusuario de Django
  
  shell           Abrir shell de Django
  bash            Abrir bash del contenedor backend
  
  backup          Crear backup de la base de datos
  clean           Limpiar contenedores, volúmenes e imágenes
  
  help            Mostrar esta ayuda

Ejemplos:
  ./deploy.sh deploy              # Despliegue completo
  ./deploy.sh logs backend        # Ver logs del backend
  ./deploy.sh update              # Actualizar aplicación
  ./deploy.sh health              # Verificar salud

EOF
}

# Main
case "$1" in
    deploy)
        deploy
        ;;
    update)
        update
        ;;
    build)
        check_docker
        build
        ;;
    start)
        check_docker
        check_env
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs "$2"
        ;;
    migrate)
        migrate
        ;;
    collectstatic)
        collectstatic
        ;;
    createsuperuser)
        createsuperuser
        ;;
    shell)
        shell
        ;;
    bash)
        bash
        ;;
    backup)
        backup
        ;;
    clean)
        clean
        ;;
    health)
        health
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "Comando no reconocido: $1"
        echo ""
        help
        exit 1
        ;;
esac
