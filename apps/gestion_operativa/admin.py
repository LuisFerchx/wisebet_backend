from django.contrib import admin
from .models import (
    Distribuidora,
    CasaApuestas,
    Agencia,
    PerfilOperativo,
    ConfiguracionOperativa,
    TransaccionFinanciera,
    PlanificacionRotacion,
    AlertaOperativa,
    BitacoraMando,
    Deporte,
    Pais,
    ProvinciaEstado,
    Ciudad,
    Ubicacion,
)


@admin.register(Deporte)
class DeporteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "activo")
    search_fields = ("nombre", "codigo")
    list_filter = ("activo",)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_iso", "activo")
    search_fields = ("nombre", "codigo_iso")
    list_filter = ("activo",)


@admin.register(ProvinciaEstado)
class ProvinciaEstadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais")
    search_fields = ("nombre", "pais__nombre")
    list_filter = ("pais",)


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "provincia")
    search_fields = ("nombre", "provincia__nombre")
    list_filter = ("provincia__pais", "provincia")


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("ciudad", "direccion", "referencia")
    search_fields = ("ciudad__nombre", "direccion", "provincia_estado__nombre")
    list_filter = ("ciudad__provincia__pais", "ciudad__provincia")


@admin.register(Distribuidora)
class DistribuidoraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "fecha_actualizacion")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(CasaApuestas)
class CasaApuestasAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "distribuidora",
        "capital_activo_hoy",
        "nro_agencias",
        "activo",
    )
    search_fields = ("nombre", "distribuidora__nombre")
    list_filter = ("activo", "distribuidora")


@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "responsable", "perfiles_totales", "activo")
    search_fields = ("nombre", "responsable")
    list_filter = ("activo", "casa_madre")


@admin.register(PerfilOperativo)
class PerfilOperativoAdmin(admin.ModelAdmin):
    # 'casa' removed, 'agencia' remains. 'deporte_dna' is now FK.
    list_display = (
        "nombre_usuario",
        "agencia",
        "tipo_jugador",
        "deporte_dna",
        "nivel_cuenta",
        "activo",
    )
    search_fields = ("nombre_usuario", "agencia__nombre", "deporte_dna__nombre")
    list_filter = ("activo", "tipo_jugador", "nivel_cuenta", "deporte_dna", "agencia")


@admin.register(ConfiguracionOperativa)
class ConfiguracionOperativaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "capital_total_activos", "actualizar_meta_diariamente")


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
    list_display = ("tipo_alerta", "severidad", "perfil_afectado", "estado")
    list_filter = ("severidad", "estado")


@admin.register(BitacoraMando)
class BitacoraMandoAdmin(admin.ModelAdmin):
    list_display = ("perfil", "fecha_registro", "usuario_registro")
    search_fields = ("perfil__nombre_usuario", "observacion")
