from rest_framework import serializers
from django.db.models import Avg, Sum
from django.utils import timezone
from .models import (
    Distribuidora,
    CasaApuestas,
    Ubicacion,
    Agencia,
    PerfilOperativo,
    ConfiguracionOperativa,
    TransaccionFinanciera,
    PlanificacionRotacion,
    AlertaOperativa,
    BitacoraMando,
    Operacion,
    Deporte,
    Pais,
    ProvinciaEstado,
    Ciudad,
    Persona,
    ObjetivoCreacionPerfiles,
)


# ============================================================================
# CATALOGOS SERIALIZERS
# ============================================================================


class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = "__all__"


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = "__all__"


class ProvinciaEstadoSerializer(serializers.ModelSerializer):
    pais_nombre = serializers.ReadOnlyField(source="pais.nombre")

    class Meta:
        model = ProvinciaEstado
        fields = "__all__"


class CiudadSerializer(serializers.ModelSerializer):
    provincia_nombre = serializers.ReadOnlyField(source="provincia.nombre")
    pais_nombre = serializers.ReadOnlyField(source="provincia.pais.nombre")

    class Meta:
        model = Ciudad
        fields = "__all__"


# ============================================================================
# PERSOANA SERIALIZERS
# ============================================================================


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"


# ============================================================================
# UBICACIÓN SERIALIZERS
# ============================================================================


class UbicacionSerializer(serializers.ModelSerializer):
    """Serializer para ubicaciones normalizadas."""

    pais_detalle = PaisSerializer(source="pais", read_only=True)
    provincia_detalle = ProvinciaEstadoSerializer(
        source="provincia_estado", read_only=True
    )
    ciudad_detalle = CiudadSerializer(source="ciudad", read_only=True)

    class Meta:
        model = Ubicacion
        fields = "__all__"


# ============================================================================
# CASAS DE APUESTAS SERIALIZERS
# ============================================================================


class CasaApuestasSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para casas (usado en anidados)."""

    class Meta:
        model = CasaApuestas
        fields = ["id_casa", "nombre", "url_backoffice", "activo"]


class CasaApuestasExpandedSerializer(serializers.ModelSerializer):
    """Serializer para casas anidadas en distribuidoras (con booleanos)."""

    class Meta:
        model = CasaApuestas
        fields = [
            "id_casa",
            "nombre",
            "url_backoffice",
            "puede_tener_agencia",
            "activo",
        ]

class CasaApuestasCreateSerializer(serializers.ModelSerializer):
    """Serializer para creación de casas de apuestas (solo campos iniciales)."""

    class Meta:
        model = CasaApuestas
        fields = [
            "nombre",
            "url_backoffice",
            "puede_tener_agencia",
            "activo",
            "distribuidora",
        ]


class CasaApuestasSerializer(serializers.ModelSerializer):
    """Serializer completo para casas con nombre de distribuidora."""

    distribuidora_nombre = serializers.ReadOnlyField(source="distribuidora.nombre")
    nro_agencias = serializers.SerializerMethodField()

    class Meta:
        model = CasaApuestas
        fields = "__all__"

    def get_nro_agencias(self, obj):
        """Calcula dinámicamente el número de agencias activas."""
        return obj.agencias.count()


# ============================================================================
# DISTRIBUIDORAS SERIALIZERS
# ============================================================================


class DistribuidoraSerializer(serializers.ModelSerializer):
    """Serializer base para distribuidoras."""

    casas_count = serializers.SerializerMethodField()
    deportes_detalle = DeporteSerializer(source="deportes", many=True, read_only=True)

    class Meta:
        model = Distribuidora
        fields = "__all__"

    def get_casas_count(self, obj):
        """Retorna cantidad de casas sin cargar todas."""
        return obj.casas.count()


class DistribuidoraExpandedSerializer(DistribuidoraSerializer):
    """Serializer expandido que incluye las casas anidadas con booleanos."""

    casas = CasaApuestasExpandedSerializer(many=True, read_only=True)

    class Meta(DistribuidoraSerializer.Meta):
        pass


# ============================================================================
# AGENCIAS SERIALIZERS
# ============================================================================


class AgenciaSerializer(serializers.ModelSerializer):
    """Serializer para agencias con ubicación expandida."""

    ubicacion_detalle = UbicacionSerializer(source="ubicacion", read_only=True)
    casa_madre_nombre = serializers.ReadOnlyField(source="casa_madre.nombre")
    ggr = serializers.SerializerMethodField()
    perfiles_totales = serializers.ReadOnlyField()

    class Meta:
        model = Agencia
        fields = "__all__"

    def get_ggr(self, obj):
        """Calcula GGR (Gross Gaming Revenue) del mes actual."""
        return round(obj.calcular_ggr(), 2)

    def get_fields(self):
        """Filtra casas_madre para mostrar solo aquellas que pueden tener agencias."""
        fields = super().get_fields()
        if 'casa_madre' in fields:
            fields['casa_madre'].queryset = CasaApuestas.objects.filter(
                puede_tener_agencia=True,
                activo=True
            )
        return fields


class ObjetivoCreacionPerfilesSerializer(serializers.ModelSerializer):
    """Serializer para objetivos de creación de perfiles."""

    agencia_nombre = serializers.CharField(source="agencia.nombre", read_only=True)
    perfiles_restantes = serializers.IntegerField(read_only=True)
    porcentaje_completado = serializers.FloatField(read_only=True)

    class Meta:
        model = ObjetivoCreacionPerfiles
        fields = [
            "id_objetivo",
            "agencia",
            "agencia_nombre",
            "cantidad_objetivo",
            "cantidad_completada",
            "plazo_dias",
            "fecha_inicio",
            "fecha_limite",
            "completado",
            "perfiles_restantes",
            "porcentaje_completado",
            "planificacion",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = [
            "id_objetivo",
            "fecha_inicio",
            "fecha_limite",
            "fecha_creacion",
            "fecha_actualizacion",
            "cantidad_completada",
            "completado",
            "planificacion",
        ]

    def validate_cantidad_objetivo(self, value):
        """Valida que la cantidad objetivo sea válida."""
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad objetivo debe ser mayor a 0"
            )
        if value > 100:
            raise serializers.ValidationError(
                "La cantidad objetivo no puede exceder 100 perfiles"
            )
        return value

    def validate_plazo_dias(self, value):
        """Valida que el plazo sea válido."""
        if value <= 0:
            raise serializers.ValidationError("El plazo debe ser mayor a 0 días")
        if value > 365:
            raise serializers.ValidationError("El plazo no puede exceder 365 días")
        return value


# ============================================================================
# OPERACIONES SERIALIZERS
# ============================================================================


class OperacionSerializer(serializers.ModelSerializer):
    """Serializer para operaciones/apuestas."""

    perfil_nombre = serializers.ReadOnlyField(source="perfil.nombre_usuario")
    deporte_nombre = serializers.ReadOnlyField(source="deporte.nombre")

    class Meta:
        model = Operacion
        fields = "__all__"


# ============================================================================
# PERFILES OPERATIVOS SERIALIZERS
# ============================================================================


class PerfilOperativoSerializer(serializers.ModelSerializer):
    """Serializer para perfiles con campos calculados dinámicamente."""

    usuario_username = serializers.ReadOnlyField(source="usuario.username", allow_null=True)
    casa_nombre = serializers.SerializerMethodField()
    distribuidora_nombre = serializers.SerializerMethodField()
    agencia_nombre = serializers.ReadOnlyField(source="agencia.nombre")
    deporte_nombre = serializers.ReadOnlyField(source="deporte_dna.nombre")

    # Campos calculados dinámicamente desde Operacion
    stake_promedio = serializers.SerializerMethodField()
    ops_semanales = serializers.SerializerMethodField()
    ops_mensuales = serializers.SerializerMethodField()
    ops_historicas = serializers.SerializerMethodField()
    profit_loss_total = serializers.SerializerMethodField()

    class Meta:
        model = PerfilOperativo
        fields = "__all__"
        extra_kwargs = {
            "usuario": {"required": False, "allow_null": True},  # Se asigna dinámicamente después
        }

    def get_casa_nombre(self, obj):
        if obj.agencia and obj.agencia.casa_madre:
            return obj.agencia.casa_madre.nombre
        return None

    def get_distribuidora_nombre(self, obj):
        if (
            obj.agencia
            and obj.agencia.casa_madre
            and obj.agencia.casa_madre.distribuidora
        ):
            return obj.agencia.casa_madre.distribuidora.nombre
        return None

    def get_stake_promedio(self, obj):
        """Calcula stake promedio desde Operacion."""
        avg = obj.operaciones_reales.aggregate(promedio=Avg("importe"))["promedio"]
        return float(avg) if avg else 0.0

    def get_ops_semanales(self, obj):
        """Cuenta operaciones de la semana actual."""
        hoy = timezone.now().date()
        inicio_semana = hoy - timezone.timedelta(days=hoy.weekday())
        return obj.operaciones_reales.filter(
            fecha_registro__date__gte=inicio_semana
        ).count()

    def get_ops_mensuales(self, obj):
        """Cuenta operaciones del mes actual."""
        hoy = timezone.now()
        return obj.operaciones_reales.filter(
            fecha_registro__year=hoy.year, fecha_registro__month=hoy.month
        ).count()

    def get_ops_historicas(self, obj):
        """Cuenta total de operaciones."""
        return obj.operaciones_reales.count()

    def get_profit_loss_total(self, obj):
        """Calcula ganancia/pérdida total desde Operacion."""
        total = obj.operaciones_reales.aggregate(total=Sum("profit_loss"))["total"]
        return float(total) if total else 0.0


# ============================================================================
# CONFIGURACIÓN OPERATIVA SERIALIZERS
# ============================================================================


class ConfiguracionOperativaSerializer(serializers.ModelSerializer):
    """Serializer para configuración operativa con campos calculados."""
    
    capital_total_activos = serializers.SerializerMethodField()

    class Meta:
        model = ConfiguracionOperativa
        fields = "__all__"

    def get_capital_total_activos(self, obj):
        """
        Calcula la suma de saldos de todos los perfiles ACTIVOS.
        """
        total = PerfilOperativo.objects.filter(
            activo=True
        ).aggregate(total=Sum("saldo_actual"))["total"] or 0
        return float(total)


# ============================================================================
# TRANSACCIONES FINANCIERAS SERIALIZERS
# ============================================================================


class TransaccionFinancieraSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source="perfil.nombre_usuario")

    class Meta:
        model = TransaccionFinanciera
        fields = "__all__"


# ============================================================================
# PLANIFICACIÓN ROTACIÓN SERIALIZERS
# ============================================================================


class PlanificacionRotacionSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source="perfil.nombre_usuario")

    class Meta:
        model = PlanificacionRotacion
        fields = "__all__"


# ============================================================================
# ALERTAS OPERATIVAS SERIALIZERS
# ============================================================================


class AlertaOperativaSerializer(serializers.ModelSerializer):
    perfil_usuario = serializers.ReadOnlyField(source="perfil_afectado.nombre_usuario")
    casa_nombre = serializers.ReadOnlyField(source="casa_afectada.nombre")

    class Meta:
        model = AlertaOperativa
        fields = "__all__"


# ============================================================================
# BITÁCORA DE MANDO SERIALIZERS
# ============================================================================


class BitacoraMandoSerializer(serializers.ModelSerializer):
    usuario_registro_username = serializers.ReadOnlyField(
        source="usuario_registro.username"
    )

    class Meta:
        model = BitacoraMando
        fields = "__all__"
