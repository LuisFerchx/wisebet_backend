from django.db import models
from django.conf import settings
from .choices import (
    TipoJugadorChoices,
    NivelCuentaChoices,
    TipoDocumentoChoices,
    TipoTransaccionChoices,
    MetodoPagoChoices,
    EstadoTransaccionChoices,
    TipoAlertaChoices,
    SeveridadChoices,
    EstadoAlertaChoices,
    EstadoOperacionChoices,
    EstadoDiaChoices,
)


class Deporte(models.Model):
    """Catálogo normalizado de deportes para apuestas."""

    id_deporte = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    icono = models.CharField(
        max_length=50, blank=True, null=True, help_text="Nombre del icono para UI"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "deportes"
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Distribuidora(models.Model):
    id_distribuidora = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    deportes = models.ManyToManyField(
        Deporte, blank=True, related_name="distribuidoras"
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
    nro_perfiles = models.IntegerField(default=0)
    url_backoffice = models.URLField(blank=True, null=True)
    capital_activo_hoy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_actualizacion_capital = models.DateTimeField(auto_now=True)
    perfiles_minimos_req = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "casas_apuestas"
        verbose_name = "Casa de Apuestas"
        verbose_name_plural = "Casas de Apuestas"

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=100, default="Perú")
    provincia_estado = models.CharField(
        max_length=100, verbose_name="Provincia / Estado"
    )
    ciudad = models.CharField(max_length=100)
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

    # Auditoría
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

    # Ubicación Normalizada
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.SET_NULL, null=True, related_name="agencias"
    )

    # Gestión
    responsable = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)

    # Operatividad
    casa_madre = models.ForeignKey(
        CasaApuestas, on_delete=models.SET_NULL, null=True, related_name="agencias"
    )
    rake_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, help_text="% Rake"
    )
    perfiles_minimos = models.IntegerField(default=5)
    url_backoffice = models.URLField(blank=True, null=True)

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "agencias"
        verbose_name = "Agencia"
        verbose_name_plural = "Agencias"

    def __str__(self):
        return self.nombre


class PerfilOperativo(models.Model):
    """Cuenta creada en una casa de apuestas usando datos de una Persona."""

    id_perfil = models.AutoField(primary_key=True)

    # Operador que gestiona este perfil
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfiles_operativos",
    )

    # Persona cuyos datos se usaron para crear la cuenta
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="perfiles",
        help_text="Datos de identidad usados para crear esta cuenta",
    )

    # Casa de apuestas donde está la cuenta
    casa = models.ForeignKey(
        CasaApuestas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfiles",
    )

    # Agencia donde se creó la cuenta
    agencia = models.ForeignKey(
        Agencia, on_delete=models.CASCADE, related_name="perfiles"
    )

    # Acceso directo al backoffice de la cuenta
    url_acceso_backoffice = models.URLField(
        blank=True, null=True, help_text="Link al backoffice de la cuenta"
    )

    nombre_usuario = models.CharField(max_length=100)
    tipo_jugador = models.CharField(max_length=50, choices=TipoJugadorChoices.choices)
    deporte_dna = models.ForeignKey(
        Deporte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfiles_dna",
        help_text="Deporte principal del perfil",
    )
    ip_operativa = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    # ciudad_sede ELIMINADO - Se obtiene de agencia.ubicacion
    preferencias = models.TextField(blank=True, null=True)
    nivel_cuenta = models.CharField(max_length=50, choices=NivelCuentaChoices.choices)
    # Campos eliminados: saldo_real, stake_promedio, ops_semanales_actuales, ops_mensuales, ops_historicas
    # Ahora se calculan dinámicamente desde la tabla Operacion
    meta_ops_semanales = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "perfiles_operativos"
        verbose_name = "Perfil Operativo"
        verbose_name_plural = "Perfiles Operativos"
        # Una persona solo puede tener UNA cuenta por casa de apuestas
        unique_together = ["persona", "casa"]

    def __str__(self):
        casa_nombre = self.casa.nombre if self.casa else "Sin casa"
        return f"{self.nombre_usuario} - {casa_nombre}"


class ConfiguracionOperativa(models.Model):
    """Métricas operativas diarias del sistema (Singleton).

    Estos valores se CALCULAN y actualizan automáticamente.
    """

    id_configuracion = models.AutoField(primary_key=True)

    # Métricas calculadas diariamente
    capital_total_activos = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="SUM de saldos de perfiles activos hoy",
    )
    perfiles_listos_operar = models.IntegerField(
        default=0, help_text="COUNT de perfiles activos hoy"
    )
    perfiles_en_descanso = models.IntegerField(
        default=0, help_text="COUNT de perfiles en descanso hoy"
    )
    volumen_apostado_hoy = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="SUM de importe de operaciones de hoy",
    )

    # Última actualización
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "configuracion_operativa"
        verbose_name = "Configuración Operativa"
        verbose_name_plural = "Configuraciones Operativas"

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionOperativa.objects.exists():
            return
        return super(ConfiguracionOperativa, self).save(*args, **kwargs)

    def __str__(self):
        return "Métricas Operativas"


class ProtocoloAuditoria(models.Model):
    """Umbrales de auditoría para alertas automáticas (Singleton).

    Estos valores los CONFIGURA el usuario desde el frontend.
    """

    id_protocolo = models.AutoField(primary_key=True)

    # Umbrales configurables
    perfiles_minimos_por_casa = models.IntegerField(
        default=3, help_text="Mínimo de perfiles activos por casa"
    )
    umbral_saldo_critico = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=300,
        help_text="Saldo mínimo por perfil antes de alerta",
    )
    capital_seguridad_por_casa = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=2000,
        help_text="Capital mínimo total por casa",
    )
    volumen_diario_objetivo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=6000,
        help_text="Meta de volumen de apuestas diario",
    )

    # Auditoría
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="protocolos_modificados",
    )

    class Meta:
        db_table = "protocolo_auditoria"
        verbose_name = "Protocolo de Auditoría"
        verbose_name_plural = "Protocolos de Auditoría"

    def save(self, *args, **kwargs):
        if not self.pk and ProtocoloAuditoria.objects.exists():
            return
        return super(ProtocoloAuditoria, self).save(*args, **kwargs)

    def __str__(self):
        return "Protocolo de Auditoría"


class TransaccionFinanciera(models.Model):
    """Movimientos de dinero (depósitos/retiros) de un perfil."""

    id_transaccion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="transacciones"
    )
    tipo_transaccion = models.CharField(
        max_length=20,
        choices=TipoTransaccionChoices.choices,
        help_text="Tipo de movimiento financiero",
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(
        max_length=20,
        choices=MetodoPagoChoices.choices,
        help_text="Método de pago utilizado",
    )
    estado = models.CharField(
        max_length=20, choices=EstadoTransaccionChoices.choices, default="PENDIENTE"
    )
    referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número de comprobante o referencia bancaria",
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transacciones_financieras"
        verbose_name = "Transacción Financiera"
        verbose_name_plural = "Transacciones Financieras"
        ordering = ["-fecha_transaccion"]

    def __str__(self):
        return f"{self.tipo_transaccion} - ${self.monto} - {self.perfil}"


class PlanificacionRotacion(models.Model):
    id_planificacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="planificaciones"
    )
    fecha = models.DateField()
    estado_dia = models.CharField(max_length=1, choices=EstadoDiaChoices.choices)
    mes = models.IntegerField()
    anio = models.IntegerField()

    class Meta:
        db_table = "planificacion_rotacion"
        verbose_name = "Planificación Rotación"
        verbose_name_plural = "Planificaciones de Rotación"


class AlertaOperativa(models.Model):
    """Alertas generadas automáticamente por el sistema de auditoría."""

    id_alerta = models.AutoField(primary_key=True)
    tipo_alerta = models.CharField(
        max_length=30,
        choices=TipoAlertaChoices.choices,
        help_text="Tipo de alerta detectada",
    )
    descripcion = models.TextField(help_text="Descripción detallada de la alerta")
    severidad = models.CharField(
        max_length=10, choices=SeveridadChoices.choices, default="MEDIA"
    )

    # Entidades afectadas (una o ambas pueden ser null)
    perfil_afectado = models.ForeignKey(
        PerfilOperativo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alertas",
    )
    casa_afectada = models.ForeignKey(
        CasaApuestas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alertas",
    )

    # Estado y resolución
    estado = models.CharField(
        max_length=15, choices=EstadoAlertaChoices.choices, default="ACTIVA"
    )

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    resuelta_at = models.DateTimeField(null=True, blank=True)
    resuelta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alertas_resueltas",
    )

    class Meta:
        db_table = "alertas_operativas"
        verbose_name = "Alerta Operativa"
        verbose_name_plural = "Alertas Operativas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.severidad}] {self.tipo_alerta}"


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
    """Registro de cada apuesta realizada por un perfil."""

    id_operacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(
        PerfilOperativo, on_delete=models.CASCADE, related_name="operaciones_reales"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, help_text="Fecha y hora exacta de la operación"
    )
    importe = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Stake o monto apostado"
    )
    cuota = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Odds de la apuesta"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoOperacionChoices.choices,
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
        help_text="Deporte de la apuesta",
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
