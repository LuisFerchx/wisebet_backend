from rest_framework import serializers
from django.db.models import Avg, Sum, Count
from django.utils import timezone
from .models import (
    Distribuidora, CasaApuestas, Ubicacion, Agencia, PerfilOperativo,
    ConfiguracionOperativa, TransaccionFinanciera, PlanificacionRotacion,
    AlertaOperativa, BitacoraMando, Operacion
)


# ============================================================================
# UBICACIÓN SERIALIZERS
# ============================================================================

class UbicacionSerializer(serializers.ModelSerializer):
    """Serializer para ubicaciones normalizadas."""
    
    class Meta:
        model = Ubicacion
        fields = '__all__'


# ============================================================================
# CASAS DE APUESTAS SERIALIZERS
# ============================================================================

class CasaApuestasSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para casas (usado en anidados)."""
    
    class Meta:
        model = CasaApuestas
        fields = ['id_casa', 'nombre', 'url_backoffice', 'activo']


class CasaApuestasSerializer(serializers.ModelSerializer):
    """Serializer completo para casas con nombre de distribuidora."""
    distribuidora_nombre = serializers.ReadOnlyField(source='distribuidora.nombre')
    
    class Meta:
        model = CasaApuestas
        fields = '__all__'


# ============================================================================
# DISTRIBUIDORAS SERIALIZERS
# ============================================================================

class DistribuidoraSerializer(serializers.ModelSerializer):
    """Serializer base para distribuidoras."""
    casas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Distribuidora
        fields = '__all__'
    
    def get_casas_count(self, obj):
        """Retorna cantidad de casas sin cargar todas."""
        return obj.casas.count()


class DistribuidoraExpandedSerializer(DistribuidoraSerializer):
    """Serializer expandido que incluye las casas anidadas."""
    casas = CasaApuestasSimpleSerializer(many=True, read_only=True)
    
    class Meta(DistribuidoraSerializer.Meta):
        pass


# ============================================================================
# AGENCIAS SERIALIZERS
# ============================================================================

class AgenciaSerializer(serializers.ModelSerializer):
    """Serializer para agencias con ubicación expandida."""
    ubicacion_detalle = UbicacionSerializer(source='ubicacion', read_only=True)
    casa_madre_nombre = serializers.ReadOnlyField(source='casa_madre.nombre')
    
    class Meta:
        model = Agencia
        fields = '__all__'


# ============================================================================
# OPERACIONES SERIALIZERS
# ============================================================================

class OperacionSerializer(serializers.ModelSerializer):
    """Serializer para operaciones/apuestas."""
    perfil_nombre = serializers.ReadOnlyField(source='perfil.nombre_usuario')
    
    class Meta:
        model = Operacion
        fields = '__all__'


# ============================================================================
# PERFILES OPERATIVOS SERIALIZERS
# ============================================================================

class PerfilOperativoSerializer(serializers.ModelSerializer):
    """Serializer para perfiles con campos calculados dinámicamente."""
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    casa_nombre = serializers.ReadOnlyField(source='casa.nombre')
    agencia_nombre = serializers.ReadOnlyField(source='agencia.nombre')
    ubicacion_ciudad = serializers.ReadOnlyField(source='agencia.ubicacion.ciudad')
    
    # Campos calculados dinámicamente desde Operacion
    saldo_real = serializers.SerializerMethodField()
    stake_promedio = serializers.SerializerMethodField()
    ops_semanales = serializers.SerializerMethodField()
    ops_mensuales = serializers.SerializerMethodField()
    ops_historicas = serializers.SerializerMethodField()

    class Meta:
        model = PerfilOperativo
        fields = '__all__'
    
    def get_saldo_real(self, obj):
        """Calcula saldo desde TransaccionFinanciera."""
        depositos = obj.transacciones.filter(
            tipo_transaccion__icontains='deposito'
        ).aggregate(total=Sum('monto'))['total'] or 0
        retiros = obj.transacciones.filter(
            tipo_transaccion__icontains='retiro'
        ).aggregate(total=Sum('monto'))['total'] or 0
        return float(depositos - retiros)
    
    def get_stake_promedio(self, obj):
        """Calcula stake promedio desde Operacion."""
        avg = obj.operaciones_reales.aggregate(promedio=Avg('importe'))['promedio']
        return float(avg) if avg else 0.0
    
    def get_ops_semanales(self, obj):
        """Cuenta operaciones de la semana actual."""
        hoy = timezone.now().date()
        inicio_semana = hoy - timezone.timedelta(days=hoy.weekday())
        return obj.operaciones_reales.filter(fecha_registro__date__gte=inicio_semana).count()
    
    def get_ops_mensuales(self, obj):
        """Cuenta operaciones del mes actual."""
        hoy = timezone.now()
        return obj.operaciones_reales.filter(
            fecha_registro__year=hoy.year,
            fecha_registro__month=hoy.month
        ).count()
    
    def get_ops_historicas(self, obj):
        """Cuenta total de operaciones."""
        return obj.operaciones_reales.count()


# ============================================================================
# CONFIGURACIÓN OPERATIVA SERIALIZERS
# ============================================================================

class ConfiguracionOperativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionOperativa
        fields = '__all__'


# ============================================================================
# TRANSACCIONES FINANCIERAS SERIALIZERS
# ============================================================================

class TransaccionFinancieraSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source='perfil.nombre_usuario')

    class Meta:
        model = TransaccionFinanciera
        fields = '__all__'


# ============================================================================
# PLANIFICACIÓN ROTACIÓN SERIALIZERS
# ============================================================================

class PlanificacionRotacionSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source='perfil.nombre_usuario')

    class Meta:
        model = PlanificacionRotacion
        fields = '__all__'


# ============================================================================
# ALERTAS OPERATIVAS SERIALIZERS
# ============================================================================

class AlertaOperativaSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source='perfil_afectado.nombre_usuario')
    casa_nombre = serializers.ReadOnlyField(source='casa_afectada.nombre')

    class Meta:
        model = AlertaOperativa
        fields = '__all__'


# ============================================================================
# BITÁCORA DE MANDO SERIALIZERS
# ============================================================================

class BitacoraMandoSerializer(serializers.ModelSerializer):
    usuario_registro_username = serializers.ReadOnlyField(source='usuario_registro.username')

    class Meta:
        model = BitacoraMando
        fields = '__all__'
