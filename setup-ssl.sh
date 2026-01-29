#!/bin/bash

# Script para obtener certificados SSL con Let's Encrypt
# Uso: ./setup-ssl.sh tu-dominio.com tu-email@ejemplo.com

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Verificar argumentos
if [ "$#" -ne 2 ]; then
    print_error "Uso: $0 <dominio> <email>"
    echo "Ejemplo: $0 ejemplo.com admin@ejemplo.com"
    exit 1
fi

DOMAIN=$1
EMAIL=$2

print_info "Configurando SSL para: $DOMAIN"
print_info "Email: $EMAIL"

# Crear directorio para certificados
mkdir -p ssl
mkdir -p certbot_www

# Crear configuración temporal de Nginx para validación
cat > nginx.temp.conf << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
EOF

print_info "Iniciando Nginx temporal para validación..."

# Iniciar Nginx temporal
docker run -d \
    --name nginx_temp \
    -p 80:80 \
    -v $(pwd)/nginx.temp.conf:/etc/nginx/conf.d/default.conf:ro \
    -v $(pwd)/certbot_www:/var/www/certbot \
    nginx:1.25-alpine

sleep 3

print_info "Obteniendo certificado SSL..."

# Obtener certificado
docker run --rm \
    -v $(pwd)/ssl:/etc/letsencrypt \
    -v $(pwd)/certbot_www:/var/www/certbot \
    certbot/certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

# Detener Nginx temporal
print_info "Deteniendo Nginx temporal..."
docker stop nginx_temp
docker rm nginx_temp

# Copiar certificados a la ubicación correcta
print_info "Configurando certificados..."
mkdir -p ssl
cp ssl/live/$DOMAIN/fullchain.pem ssl/fullchain.pem
cp ssl/live/$DOMAIN/privkey.pem ssl/privkey.pem

# Actualizar nginx.prod.conf con el dominio
sed -i "s/tu-dominio.com/$DOMAIN/g" nginx.prod.conf

print_success "¡Certificados SSL obtenidos exitosamente!"
print_info "Ahora puedes usar docker-compose.prod.yml para desplegar con HTTPS"
print_info "Comando: docker compose -f docker-compose.prod.yml up -d"

# Limpiar
rm nginx.temp.conf

print_info "Configuración de renovación automática:"
print_info "Los certificados se renovarán automáticamente cada 12 horas"
print_info "cuando uses docker-compose.prod.yml"
