
import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\Usuario\Documents\GitHub\wisebet_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User
from apps.gestion_operativa.models import (
    Distribuidora, CasaApuestas, Agencia, PerfilOperativo, 
    BitacoraMando, ConfiguracionOperativa
)
from apps.gestion_operativa.choices import DeportesChoices, TipoJugadorChoices, NivelCuentaChoices

def verify_schema():
    print("Verifying Schema...")
    
    # 1. User with new fields
    username = 'test_user_schema'
    if User.objects.filter(username=username).exists():
        User.objects.get(username=username).delete()
        
    user = User.objects.create_user(
        username=username, 
        email='test_schema@example.com', 
        password='password123',
        numero_contacto='+1234567890',
        rol='OPERADOR',
        nombre_completo='Test User Schema'
    )
    print(f"User created: {user.username} (Rol: {user.rol}, Contacto: {user.numero_contacto})")

    # 2. Distribuidora with Enum list
    dist = Distribuidora.objects.create(
        nombre='Test Dist',
        deportes=[DeportesChoices.FUTBOL, DeportesChoices.BASKETBALL],
        descripcion='Test Desc'
    )
    print(f"Distribuidora created: {dist.nombre} (Deportes: {dist.deportes})")

    # 3. Agencia
    agencia = Agencia.objects.create(
        nombre='Test Agencia',
        ubicacion='Test Location',
        responsable='Test Manager'
    )
    print(f"Agencia created: {agencia.nombre}")

    # 4. CasaApuestas
    casa = CasaApuestas.objects.create(
        distribuidora=dist,
        nombre='Test Casa',
        url_backoffice='http://example.com'
    )
    print(f"CasaApuestas created: {casa.nombre}")

    # 5. PerfilOperativo
    perfil = PerfilOperativo.objects.create(
        usuario=user,
        casa=casa,
        agencia=agencia,
        nombre_usuario='player1',
        tipo_jugador=TipoJugadorChoices.PROFESIONAL,
        deporte_dna=DeportesChoices.TENNIS,
        ip_operativa='192.168.1.1',
        ciudad_sede='Madrid',
        nivel_cuenta=NivelCuentaChoices.ORO,
        saldo_real=100.00
    )
    print(f"PerfilOperativo created: {perfil.nombre_usuario} (DNA: {perfil.deporte_dna})")

    # 6. BitacoraMando
    bitacora = BitacoraMando.objects.create(
        perfil=perfil,
        observacion='Test Observation',
        usuario_registro=user
    )
    print(f"BitacoraMando created for perfil: {bitacora.perfil.nombre_usuario}")

    print("\nVERIFICATION SUCCESSFUL: All models and relationships tested.")

if __name__ == '__main__':
    try:
        verify_schema()
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
