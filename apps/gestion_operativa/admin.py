from django.contrib import admin
from .models import (
    Distribuidora,
    CasaApuestas,
    Agencia,
    PerfilOperativo,
    ConfiguracionOperativa,
    ProtocoloAuditoria,
    TransaccionFinanciera,
    PlanificacionRotacion,
    AlertaOperativa,
    BitacoraMando,
)


@admin.register(Distribuidora)
class DistribuidoraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "fecha_actualizacion")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(CasaApuestas)
class CasaApuestasAdmin(admin.ModelAdmin):
    list_display = ("nombre", "distribuidora", "capital_activo_hoy", "activo")
    search_fields = ("nombre", "distribuidora__nombre")
    list_filter = ("activo", "distribuidora")


@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "responsable", "activo")
    search_fields = ("nombre", "responsable")
    list_filter = ("activo",)


@admin.register(PerfilOperativo)
class PerfilOperativoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_usuario",
        "casa",
        "agencia",
        "tipo_jugador",
        "nivel_cuenta",
        "activo",
    )
    search_fields = ("nombre_usuario", "casa__nombre", "agencia__nombre")
    list_filter = ("activo", "tipo_jugador", "nivel_cuenta", "casa", "agencia")


@admin.register(ConfiguracionOperativa)
class ConfiguracionOperativaAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "capital_total_activos",
        "perfiles_listos_operar",
        "fecha_actualizacion",
    )


@admin.register(ProtocoloAuditoria)
class ProtocoloAuditoriaAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "perfiles_minimos_por_casa",
        "umbral_saldo_critico",
        "volumen_diario_objetivo",
        "updated_at",
    )


@admin.register(TransaccionFinanciera)
class TransaccionFinancieraAdmin(admin.ModelAdmin):
    list_display = (
        "id_transaccion",
        "perfil",
        "tipo_transaccion",
        "monto",
        "estado",
        "fecha_transaccion",
    )
    list_filter = ("tipo_transaccion", "estado", "fecha_transaccion")
    search_fields = ("perfil__nombre_usuario",)


@admin.register(PlanificacionRotacion)
class PlanificacionRotacionAdmin(admin.ModelAdmin):
    list_display = ("perfil", "fecha", "estado_dia")
    list_filter = ("estado_dia", "fecha")


@admin.register(AlertaOperativa)
class AlertaOperativaAdmin(admin.ModelAdmin):
    list_display = (
        "tipo_alerta",
        "severidad",
        "perfil_afectado",
        "estado",
        "created_at",
    )
    list_filter = ("severidad", "estado", "tipo_alerta")


@admin.register(BitacoraMando)
class BitacoraMandoAdmin(admin.ModelAdmin):
    list_display = ("perfil", "fecha_registro", "usuario_registro")
    search_fields = ("perfil__nombre_usuario", "observacion")
