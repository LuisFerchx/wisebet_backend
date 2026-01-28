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
    Persona,
    ObjetivoCreacionPerfiles,
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
    list_display = ("__str__", "meta_volumen_diario", "actualizar_meta_diariamente")


@admin.register(TransaccionFinanciera)
class TransaccionFinancieraAdmin(admin.ModelAdmin):
    list_display = (
        "id_transaccion",
        "perfil",
        "tipo",
        "metodo",
        "monto",
        "estado",
        "referencia",
        "created_at",
        "updated_at",
    )
    list_filter = ("tipo", "metodo", "estado", "created_at")
    search_fields = ("perfil__nombre_usuario", "referencia")


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

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_completo',
        'tipo_documento', 
        'numero_documento',
        'pais',
        'telefono',
        'activo'
    )
    search_fields = (
        'primer_nombre', 
        'segundo_nombre',
        'primer_apellido', 
        'segundo_apellido',
        'numero_documento',
        'correo_electronico'
    )
    list_filter = ('tipo_documento', 'pais', 'activo', 'fecha_registro')
    readonly_fields = ('nombre_completo', 'fecha_registro')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('primer_nombre', 'segundo_nombre', 'primer_apellido', 
                      'segundo_apellido', 'fecha_nacimiento')
        }),
        ('Documentación', {
            'fields': ('tipo_documento', 'numero_documento', 'pais')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo_electronico', 'direccion')
        }),
        ('Documentos KYC', {
            'fields': ('foto_rostro', 'documento_frente', 'documento_reverso'),
            'classes': ('collapse',)  # Se muestra colapsado por defecto
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_registro')
        }),
    )


@admin.register(ObjetivoCreacionPerfiles)
class ObjetivoCreacionPerfilesAdmin(admin.ModelAdmin):
    """Admin para objetivos de creación de perfiles."""

    list_display = (
        "id_objetivo",
        "agencia",
        "cantidad_objetivo",
        "cantidad_completada",
        "perfiles_restantes_display",
        "porcentaje_completado_display",
        "fecha_limite",
        "completado_display",
    )
    list_filter = ("completado", "fecha_creacion", "agencia")
    search_fields = ("agencia__nombre",)
    readonly_fields = (
        "fecha_inicio",
        "fecha_limite",
        "fecha_creacion",
        "fecha_actualizacion",
        "perfiles_restantes_display",
        "porcentaje_completado_display",
    )
    ordering = ("-fecha_creacion",)

    fieldsets = (
        (
            "Información Básica",
            {"fields": ("agencia", "cantidad_objetivo", "plazo_dias")},
        ),
        (
            "Progreso",
            {
                "fields": (
                    "cantidad_completada",
                    "perfiles_restantes_display",
                    "porcentaje_completado_display",
                    "completado",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "fecha_inicio",
                    "fecha_limite",
                    "fecha_creacion",
                    "fecha_actualizacion",
                )
            },
        ),
    )

    def perfiles_restantes_display(self, obj):
        """Muestra perfiles restantes en el admin."""
        return obj.perfiles_restantes

    perfiles_restantes_display.short_description = "Faltan"

    def porcentaje_completado_display(self, obj):
        """Muestra porcentaje completado en el admin."""
        return f"{obj.porcentaje_completado}%"

    porcentaje_completado_display.short_description = "% Completado"

    def completado_display(self, obj):
        """Muestra un icono visual para el estado completado."""
        return "✅" if obj.completado else "❌"

    completado_display.short_description = "Estado"