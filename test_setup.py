#!/usr/bin/env python
"""
Script de prueba para verificar la configuración del proyecto
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("✅ Conexión a PostgreSQL exitosa!")
            print(f"   Versión: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def test_user_model():
    """Prueba el modelo de usuario"""
    try:
        count = User.objects.count()
        print(f"✅ Modelo de Usuario funcionando correctamente!")
        print(f"   Usuarios en la base de datos: {count}")
        return True
    except Exception as e:
        print(f"❌ Error con el modelo de Usuario: {e}")
        return False

def main():
    print("=" * 50)
    print("PRUEBAS DE CONFIGURACIÓN - WISEBET BACKEND")
    print("=" * 50)
    print()
    
    # Prueba de conexión a la base de datos
    print("1. Probando conexión a PostgreSQL...")
    db_ok = test_database_connection()
    print()
    
    # Prueba del modelo de usuario
    print("2. Probando modelo de Usuario...")
    user_ok = test_user_model()
    print()
    
    # Resumen
    print("=" * 50)
    print("RESUMEN")
    print("=" * 50)
    if db_ok and user_ok:
        print("✅ Todas las pruebas pasaron exitosamente!")
        print("   El proyecto está listo para usar.")
    else:
        print("❌ Algunas pruebas fallaron.")
        print("   Revisa la configuración.")
    print()

if __name__ == "__main__":
    main()
