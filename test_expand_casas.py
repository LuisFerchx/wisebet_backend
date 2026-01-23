"""Test GET /api/gestion-operativa/distribuidoras/?expand=casas para verificar booleanos."""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gestion_operativa.models import Distribuidora
from apps.gestion_operativa.serializers import DistribuidoraExpandedSerializer

# Obtener una distribuidora con casas
distribuidoras = Distribuidora.objects.prefetch_related('casas').filter(casas__isnull=False).distinct()[:1]

if not distribuidoras:
    print("❌ No hay distribuidoras con casas.")
    exit(1)

distrib = distribuidoras[0]
serializer = DistribuidoraExpandedSerializer(distrib)
data = serializer.data

print("\n=== GET /api/gestion-operativa/distribuidoras/?expand=casas ===\n")
print(json.dumps(data, indent=2, default=str))

print("\n=== Verificación de campos en casas anidadas ===\n")
if "casas" in data and data["casas"]:
    for idx, casa in enumerate(data["casas"]):
        print(f"Casa #{idx + 1}: {casa.get('nombre')}")
        print(f"  - id_casa: {casa.get('id_casa')}")
        print(f"  - puede_tener_agencia: {casa.get('puede_tener_agencia')} ✓" if 'puede_tener_agencia' in casa else f"  - puede_tener_agencia: MISSING ❌")
        print(f"  - tiene_arrastre: {casa.get('tiene_arrastre')} ✓" if 'tiene_arrastre' in casa else f"  - tiene_arrastre: MISSING ❌")
        print(f"  - url_backoffice: {casa.get('url_backoffice')}")
        print(f"  - activo: {casa.get('activo')}")
else:
    print("❌ No hay casas en la distribuidora.")
