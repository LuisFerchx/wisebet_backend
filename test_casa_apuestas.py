"""Test rápido de creación de CasaApuestas con estrategia híbrida."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gestion_operativa.models import Distribuidora, CasaApuestas
from apps.gestion_operativa.serializers import CasaApuestasCreateSerializer

# 1. Obtener una distribuidora existente
distribuidoras = list(Distribuidora.objects.all()[:1])
if not distribuidoras:
    print("❌ No hay distribuidoras. Crea una primero.")
    exit(1)

distrib = distribuidoras[0]
print(f"✓ Usando distribuidora: {distrib.nombre} (ID: {distrib.id_distribuidora})")

# 2. Test 1: Crear casa con distribuidora en el data (body)
print("\n=== TEST 1: Distribuidora en body ===")
data_body = {
    "nombre": "Casa Test Body",
    "url_backoffice": "https://testbody.com",
    "puede_tener_agencia": True,
    "tiene_arrastre": False,
    "activo": True,
    "distribuidora": distrib.id_distribuidora
}

serializer = CasaApuestasCreateSerializer(data=data_body)
if serializer.is_valid():
    casa = serializer.save()
    print(f"✓ Casa creada: {casa.nombre} (ID: {casa.id_casa}, Distribuidora: {casa.distribuidora.nombre})")
    casa.delete()  # Limpiar
    print("✓ Casa eliminada (cleanup)")
else:
    print(f"❌ Error: {serializer.errors}")

# 3. Test 2: Crear casa SIN distribuidora (debe fallar con validación clara)
print("\n=== TEST 2: Sin distribuidora (debe fallar) ===")
data_sin = {
    "nombre": "Casa Sin Distrib",
    "url_backoffice": "https://sindistrib.com",
    "puede_tener_agencia": False,
    "tiene_arrastre": True,
    "activo": True
}

serializer_sin = CasaApuestasCreateSerializer(data=data_sin)
if serializer_sin.is_valid():
    print("❌ No debería validar sin distribuidora")
else:
    print(f"✓ Validación correcta: {serializer_sin.errors}")

print("\n=== Tests completados ===")
