from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from .choices import (
    TipoJugadorChoices,
    TipoDocumentoChoices,
    NivelCuentaChoices,
    DeportesChoices,
)


class Deporte(models.Model):
    """Catálogo de deportes disponibles para apuestas."""

    id_deporte = models.AutoField(primary_key=True)
    codigo = models.CharField(
        max_length=50,
        unique=True,
        choices=DeportesChoices.choices,
    )
    nombre = models.CharField(max_length=100)  # Ej: "Fútbol"
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "deportes"
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    """Catálogo de países."""

    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    codigo_iso = models.CharField(
        max_length=3, blank=True, null=True
    )  # ISO 3166-1 alpha-3
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "paises"
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre


class ProvinciaEstado(models.Model):
    """Provincias o estados que pertenecen a un país."""

    id_provincia = models.AutoField(primary_key=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="provincias")
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "provincias_estados"
        verbose_name = "Provincia / Estado"
        verbose_name_plural = "Provincias / Estados"
        unique_together = ["pais", "nombre"]

    def __str__(self):
        return f"{self.nombre}, {self.pais.nombre}"


class Ciudad(models.Model):
    """Ciudades que pertenecen a una provincia o estado."""

    id_ciudad = models.AutoField(primary_key=True)
    provincia = models.ForeignKey(
        ProvinciaEstado, on_delete=models.CASCADE, related_name="ciudades"
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "ciudades"
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        unique_together = ["provincia", "nombre"]

    def __str__(self):
        return f"{self.nombre}, {self.provincia.nombre}"


class Distribuidora(models.Model):
    id_distribuidora = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    deportes = models.ManyToManyField(
        Deporte, related_name="distribuidoras", blank=True
    )
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "distribuidoras_datos"
        verbose_name = "Distribuidora"
        verbose_name_plural = "Distribuidoras"

    def __str__(self):
        return self.nombre


class CasaApuestas(models.Model):
    id_casa = models.AutoField(primary_key=True)
    distribuidora = models.ForeignKey(
        Distribuidora, on_delete=models.CASCADE, related_name="casas"
    )
    nombre = models.CharField(max_length=100)
    url_backoffice = models.URLField(blank=True, null=True)
    capital_activo_hoy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_actualizacion_capital = models.DateTimeField(auto_now=True)
    perfiles_minimos_req = models.IntegerField(default=0)
    puede_tener_agencia = models.BooleanField(
        default=True, help_text="¿Esta casa puede tener agencias?"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "casas_apuestas"
        verbose_name = "Casa de Apuestas"
        verbose_name_plural = "Casas de Apuestas"

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    pais = models.ForeignKey(
        Pais, on_delete=models.SET_NULL, null=True, related_name="ubicaciones"
    )
    provincia_estado = models.ForeignKey(
        ProvinciaEstado,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ubicaciones",
        verbose_name="Provincia / Estado",
    )
    ciudad = models.ForeignKey(
        Ciudad, on_delete=models.SET_NULL, null=True, related_name="ubicaciones"
    )
    direccion = models.CharField(
        max_length=255, verbose_name="Dirección exacta (Calles)"
    )
    referencia = models.CharField(
        max_length=255, blank=True, null=True, help_text="Ej: Frente al parque..."
    )
    link_google_maps = models.URLField(
        blank=True, null=True, help_text="Enlace exacto a Google Maps"
    )

    # Campo activo eliminado pues "una ubicación siempre existe"

    class Meta:
        db_table = "ubicaciones"
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"{self.ciudad} - {self.direccion}"


class Persona(models.Model):
    """Datos de identidad de una persona para crear cuentas en casas de apuestas."""

    id_persona = models.AutoField(primary_key=True)

    # Datos personales
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)

    # Documento de identidad
    tipo_documento = models.CharField(
        max_length=20, choices=TipoDocumentoChoices.choices
    )
    numero_documento = models.CharField(max_length=50, unique=True)

    # Contacto y ubicación
    fecha_nacimiento = models.DateField()
    pais = models.CharField(max_length=100, default="Ecuador")
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    # Documentos KYC (archivos)
    foto_rostro = models.ImageField(upload_to="personas/fotos/", blank=True, null=True)
    documento_frente = models.ImageField(
        upload_to="personas/documentos/", blank=True, null=True
    )
    documento_reverso = models.ImageField(
        upload_to="personas/documentos/", blank=True, null=True
    )

    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "personas"
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} - {self.numero_documento}"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo de la persona."""
        nombres = [
            self.primer_nombre,
            self.segundo_nombre,
            self.primer_apellido,
            self.segundo_apellido,
        ]
        return " ".join(filter(None, nombres))


class Agencia(models.Model):
    id_agencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.SET_NULL, null=True, related_name="agencias"
    )
    responsable = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    casa_madre = models.ForeignKey(
        CasaApuestas, on_delete=models.SET_NULL, null=True, related_name="agencias"
    )
    rake_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, help_text="% Rake"
    )
    url_backoffice = models.URLField(blank=True, null=True)
    tiene_arrastre = models.BooleanField(
        default=False, help_text="¿Esta agencia tiene arrastre?"
    )

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "agencias"
        verbose_name = "Agencia"
        verbose_name_plural = "Agencias"

    def __str__(self):
        return self.nombre

    @property
    def perfiles_totales(self):
        """
        Cuenta dinámicamente el total de perfiles asociados a esta agencia.
        Retorna el número de perfiles activos y no activos.
        """
        return self.perfiles.count()

    def calcular_ggr(self):
        """
        Calcula GGR (Gross Gaming Revenue) del mes actual.
        GGR = -(Suma de profit_loss de todos los perfiles de esta agencia en el mes actual)
        
        Si profit_loss es positivo (perfiles ganaron), GGR es negativo (casa pierde).
        Si profit_loss es negativo (perfiles perdieron), GGR es positivo (casa gana).
        """
        hoy = timezone.now()
        perfiles_agencia = self.perfiles.all()
        
        # Filtrar solo operaciones del mes actual
        total_profit_loss = 0
        for perfil in perfiles_agencia:
            mes_profit_loss = perfil.operaciones_reales.filter(
                fecha_registro__year=hoy.year,
                fecha_registro__month=hoy.month
            ).aggregate(total=Sum("profit_loss"))["total"] or 0
            total_profit_loss += mes_profit_loss
        
        # GGR es negativo del profit_loss (lo contrario)
        return -float(total_profit_loss)


class PerfilOperativo(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfiles_operativos",
        null=True,
        blank=True,
    )
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="perfiles",
        help_text="Datos de identidad usados para crear esta cuenta",
    )

    # Agencia obligatoria (se selecciona de las disponibles)
    agencia = models.ForeignKey(
        Agencia, on_delete=models.CASCADE, related_name="perfiles"
    )
    url_acceso_backoffice = models.URLField(
        blank=True, null=True, help_text="Link al backoffice de la cuenta"
    )

    nombre_usuario = models.CharField(max_length=100)
    tipo_jugador = models.CharField(max_length=50, choices=TipoJugadorChoices.choices)
    deporte_dna = models.ForeignKey(
        Deporte, on_delete=models.SET_NULL, null=True, related_name="perfiles_dna"
    )
    
    ip_operativa = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    preferencias = models.TextField(blank=True, null=True)
    nivel_cuenta = models.CharField(max_length=50, choices=NivelCuentaChoices.choices)
    saldo_actual = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Dinero disponible en la cuenta"
    )
    
    # Rango de stake (configurable)
    stake_minimo = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Monto mínimo a apostar"
    )
    stake_maximo = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Monto máximo a apostar"
    )
    
    meta_ops_semanales = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        null=True,
        help_text="Fecha y hora de creación del perfil"
    )

    class Meta:
        db_table = "perfiles_operativos"
        verbose_name = "Perfil Operativo"
        verbose_name_plural = "Perfiles Operativos"

    def __str__(self):
        casa_nombre = (
            self.agencia.casa_madre.nombre if self.agencia.casa_madre else "Sin Casa"
        )
        return f"{self.nombre_usuario} - {casa_nombre}"


class ConfiguracionOperativa(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    # capital_total_activos se calcula dinámicamente en el serializer (suma de saldos de perfiles activos)
    meta_volumen_diario = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Meta de volumen diario de operaciones"
    )
    perfiles_listos_operar = models.IntegerField(
        default=0, help_text="Número de perfiles listos para operar"
    )
    perfiles_en_descanso = models.IntegerField(
        default=0, help_text="Número de perfiles en descanso"
    )
    umbral_saldo_critico = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Saldo mínimo que dispara alerta"
    )
    actualizar_meta_diariamente = models.BooleanField(
        default=False, help_text="¿Actualizar meta diariamente?"
    )

    class Meta:
        db_table = "configuracion_operativa"
        verbose_name = "Configuración Operativa"
        verbose_name_plural = "Configuraciones Operativas"

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionOperativa.objects.exists():
            # Ensures only one instance exists
            return
        return super(ConfiguracionOperativa, self).save(*args, **kwargs)

    def __str__(self):
        return "Configuración Global"


class TransaccionFinanciera(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="transacciones"
    )
    tipo_transaccion = models.CharField(
        max_length=50
    )  # Consider adding choices for this too
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_transaccion = models.DateTimeField()
    metodo_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)  # Consider adding choices for this

    class Meta:
        db_table = "transacciones_financieras"
        verbose_name = "Transacción Financiera"
        verbose_name_plural = "Transacciones Financieras"


class PlanificacionRotacion(models.Model):
    id_planificacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="planificaciones"
    )
    fecha = models.DateField()
    estado_dia = models.CharField(
        max_length=1, choices=[("A", "Activo"), ("D", "Descanso")]
    )
    mes = models.IntegerField()
    anio = models.IntegerField()

    class Meta:
        db_table = "planificacion_rotacion"
        verbose_name = "Planificación Rotación"
        verbose_name_plural = "Planificaciones de Rotación"


class AlertaOperativa(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    tipo_alerta = models.CharField(max_length=100)
    descripcion = models.TextField()
    severidad = models.CharField(max_length=20)
    perfil_afectado = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, null=True, blank=True
    )
    casa_afectada = models.ForeignKey(
        CasaApuestas, on_delete=models.CASCADE, null=True, blank=True
    )
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = "alertas_operativas"
        verbose_name = "Alerta Operativa"
        verbose_name_plural = "Alertas Operativas"


class BitacoraMando(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="entradas_bitacora"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField()
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "bitacora_mando"
        verbose_name = "Bitácora de Mando"
        verbose_name_plural = "Bitácoras de Mando"


class Operacion(models.Model):
    id_operacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="operaciones_reales"
    )
    fecha_registro = models.DateTimeField(
        null=True, blank=True, help_text="Fecha y hora exacta de la operación"
    )
    importe = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Stake o monto apostado"
    )
    cuota = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Odds de la apuesta"
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("PENDIENTE", "Pendiente"),
            ("GANADA", "Ganada"),
            ("PERDIDA", "Perdida"),
            ("ANULADA", "Anulada"),
        ],
        default="PENDIENTE",
    )
    payout = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Retorno total (Stake + Profit)",
    )
    profit_loss = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado neto (P&L)",
    )

    deporte = models.ForeignKey(
        Deporte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operaciones",
    )
    mercado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ej: Ganador del partido, Over 2.5",
    )

    class Meta:
        db_table = "operaciones"
        verbose_name = "Operación"
        verbose_name_plural = "Operaciones"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"Op {self.id_operacion} - {self.perfil} - ${self.importe}"

    def save(self, *args, **kwargs):
        # Auto-calc P&L if payout is set
        if self.payout is not None and self.importe:
            self.profit_loss = self.payout - self.importe
        super(Operacion, self).save(*args, **kwargs)


class ObjetivoCreacionPerfiles(models.Model):
    """Sistema de planificación para creación de perfiles en agencias."""

    id_objetivo = models.AutoField(primary_key=True)
    agencia = models.ForeignKey(
        Agencia,
        on_delete=models.CASCADE,
        related_name="objetivos_perfiles",
        help_text="Agencia a la que pertenece este objetivo"
    )
    cantidad_objetivo = models.PositiveIntegerField(
        help_text="Cantidad total de perfiles que se planea crear"
    )
    cantidad_completada = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad de perfiles ya creados para este objetivo"
    )
    plazo_dias = models.PositiveIntegerField(
        help_text="Plazo en días para completar el objetivo"
    )
    fecha_inicio = models.DateField(
        auto_now_add=True,
        help_text="Fecha en que se creó el objetivo"
    )
    fecha_limite = models.DateField(
        help_text="Fecha límite para cumplir el objetivo (calculada automáticamente)"
    )
    completado = models.BooleanField(
        default=False,
        help_text="Indica si el objetivo ya fue cumplido"
    )
    planificacion = models.JSONField(
        default=dict,
        blank=True,
        help_text="Planificación de creación: {'YYYY-MM-DD': cantidad, ...}"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "objetivos_creacion_perfiles"
        ordering = ["-fecha_creacion"]
        verbose_name = "Objetivo de Creación de Perfiles"
        verbose_name_plural = "Objetivos de Creación de Perfiles"

    def __str__(self):
        return f"{self.agencia.nombre}: {self.cantidad_completada}/{self.cantidad_objetivo} perfiles"

    @property
    def perfiles_restantes(self):
        """Calcula cuántos perfiles faltan por crear."""
        return max(0, self.cantidad_objetivo - self.cantidad_completada)

    @property
    def porcentaje_completado(self):
        """Calcula el porcentaje de avance del objetivo."""
        if self.cantidad_objetivo == 0:
            return 0
        return round((self.cantidad_completada / self.cantidad_objetivo) * 100, 2)

    def save(self, *args, **kwargs):
        """Override save para calcular fecha_limite automáticamente."""
        if not self.fecha_limite and not self.pk:
            from datetime import date, timedelta
            self.fecha_limite = date.today() + timedelta(days=self.plazo_dias)

        # Auto-marcar como completado si se alcanzó el objetivo
        if self.cantidad_completada >= self.cantidad_objetivo:
            self.completado = True

        super().save(*args, **kwargs)
