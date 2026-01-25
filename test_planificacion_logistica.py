"""
Script de prueba para el sistema de planificación logística.
Crea datos de ejemplo para demostrar el flujo completo.

Uso:
    python test_planificacion_logistica.py
"""

import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gestion_operativa.models import (
    Agencia,
    ObjetivoCreacionPerfiles,
    TareaPlanificada,
    CapacidadEquipo,
)

User = get_user_model()


def crear_datos_prueba():
    """Crea datos de prueba para el sistema de planificación."""
    
    print("=" * 60)
    print("CREANDO DATOS DE PRUEBA - PLANIFICACIÓN LOGÍSTICA")
    print("=" * 60)
    
    # 1. Crear usuarios de prueba
    print("\n1️⃣ Creando usuarios del equipo...")
    usuarios = []
    for i in range(1, 4):
        username = f"operador_{i}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': f'Operador',
                'last_name': f'#{i}',
                'email': f'operador{i}@wisebet.com'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"   ✅ Usuario creado: {username}")
        else:
            print(f"   ℹ️  Usuario ya existe: {username}")
        usuarios.append(user)
    
    # 2. Crear capacidades para los usuarios
    print("\n2️⃣ Configurando capacidades del equipo...")
    capacidades = [8, 6, 5]  # Capacidades diferentes por usuario
    for user, capacidad in zip(usuarios, capacidades):
        cap, created = CapacidadEquipo.objects.get_or_create(
            usuario=user,
            defaults={
                'capacidad_diaria': capacidad,
                'activo': True,
                'notas': f'Usuario con capacidad de {capacidad} perfiles/día'
            }
        )
        if created:
            print(f"   ✅ Capacidad configurada: {user.username} - {capacidad} perfiles/día")
        else:
            print(f"   ℹ️  Capacidad ya existe: {user.username}")
    
    # 3. Obtener o crear agencias
    print("\n3️⃣ Verificando agencias disponibles...")
    agencias = Agencia.objects.filter(activo=True)[:3]
    
    if agencias.count() < 1:
        print("   ⚠️  No hay agencias activas. Por favor crea al menos una agencia primero.")
        return
    
    print(f"   ✅ Encontradas {agencias.count()} agencias activas")
    
    # 4. Crear objetivos de creación de perfiles
    print("\n4️⃣ Creando objetivos de creación de perfiles...")
    objetivos_creados = []
    
    for agencia in agencias:
        # Verificar si ya existe un objetivo activo
        objetivo_existente = ObjetivoCreacionPerfiles.objects.filter(
            agencia=agencia,
            completado=False
        ).first()
        
        if objetivo_existente:
            print(f"   ℹ️  Objetivo ya existe para {agencia.nombre}")
            objetivos_creados.append(objetivo_existente)
            continue
        
        objetivo = ObjetivoCreacionPerfiles.objects.create(
            agencia=agencia,
            cantidad_objetivo=20,  # 20 perfiles por agencia
            plazo_dias=30  # 30 días
        )
        objetivos_creados.append(objetivo)
        print(f"   ✅ Objetivo creado: {agencia.nombre} - 20 perfiles en 30 días")
        print(f"      → {objetivo.tareas.count()} tareas generadas automáticamente")
    
    # 5. Planificar algunas tareas (sacar del backlog)
    print("\n5️⃣ Planificando tareas del backlog...")
    hoy = date.today()
    
    for objetivo in objetivos_creados:
        tareas_backlog = objetivo.tareas.filter(
            fecha_programada__isnull=True,
            estado='PENDIENTE'
        )[:10]  # Planificar 10 tareas
        
        contador = 0
        for i, tarea in enumerate(tareas_backlog):
            # Distribuir tareas en los próximos 5 días
            fecha = hoy + timedelta(days=(i % 5) + 1)
            # Asignar rotativamente a los usuarios
            usuario = usuarios[i % len(usuarios)]
            
            tarea.fecha_programada = fecha
            tarea.usuario_asignado = usuario
            tarea.save()
            contador += 1
        
        if contador > 0:
            print(f"   ✅ {contador} tareas planificadas para {objetivo.agencia.nombre}")
    
    # 6. Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE DATOS CREADOS")
    print("=" * 60)
    
    total_tareas = TareaPlanificada.objects.count()
    tareas_planificadas = TareaPlanificada.objects.filter(fecha_programada__isnull=False).count()
    tareas_backlog = TareaPlanificada.objects.filter(fecha_programada__isnull=True).count()
    
    print(f"\n📊 Estadísticas:")
    print(f"   • Usuarios creados: {len(usuarios)}")
    print(f"   • Agencias con objetivos: {len(objetivos_creados)}")
    print(f"   • Total tareas: {total_tareas}")
    print(f"   • Tareas planificadas: {tareas_planificadas}")
    print(f"   • Tareas en backlog: {tareas_backlog}")
    
    print("\n🎯 Próximos pasos:")
    print("   1. Accede a /api/redviva/resumen/ para ver el resumen")
    print("   2. Usa /api/tareas-planificadas/calendario/ para ver el calendario")
    print("   3. Crea perfiles operativos para completar tareas automáticamente")
    print("   4. Revisa /api/redviva/alertas/ para ver alertas")
    
    print("\n✅ Datos de prueba creados exitosamente!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        crear_datos_prueba()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
