from rest_framework import serializers
from .models import (
    Distribuidora, CasaApuestas, Agencia, PerfilOperativo,
    ConfiguracionOperativa, TransaccionFinanciera, PlanificacionRotacion,
    AlertaOperativa, BitacoraMando
)


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
    class Meta:
        model = Agencia
        fields = '__all__'


# ============================================================================
# PERFILES OPERATIVOS SERIALIZERS
# ============================================================================

class PerfilOperativoSerializer(serializers.ModelSerializer):
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    casa_nombre = serializers.ReadOnlyField(source='casa.nombre')
    agencia_nombre = serializers.ReadOnlyField(source='agencia.nombre')

    class Meta:
        model = PerfilOperativo
        fields = '__all__'


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
