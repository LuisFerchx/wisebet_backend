from django.db import models
from django.conf import settings
from .choices import DeportesChoices, TipoJugadorChoices, NivelCuentaChoices

class Distribuidora(models.Model):
    id_distribuidora = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    deportes = models.JSONField(default=list)  # Stores list of DeportesChoices values
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'distribuidoras_datos'
        verbose_name = 'Distribuidora'
        verbose_name_plural = 'Distribuidoras'

    def __str__(self):
        return self.nombre

class CasaApuestas(models.Model):
    id_casa = models.AutoField(primary_key=True)
    distribuidora = models.ForeignKey(Distribuidora, on_delete=models.CASCADE, related_name='casas')
    nombre = models.CharField(max_length=100)
    nro_perfiles = models.IntegerField(default=0)
    url_backoffice = models.URLField(blank=True, null=True)
    capital_activo_hoy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_actualizacion_capital = models.DateTimeField(auto_now=True)
    perfiles_minimos_req = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'casas_apuestas'
        verbose_name = 'Casa de Apuestas'
        verbose_name_plural = 'Casas de Apuestas'

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=100, default='Perú')
    provincia_estado = models.CharField(max_length=100, verbose_name="Provincia / Estado")
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, verbose_name="Dirección exacta (Calles)")
    referencia = models.CharField(max_length=255, blank=True, null=True, help_text="Ej: Frente al parque...")
    link_google_maps = models.URLField(blank=True, null=True, help_text="Enlace exacto a Google Maps")
    
    # Campo activo eliminado pues "una ubicación siempre existe"

    class Meta:
        db_table = 'ubicaciones'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return f"{self.ciudad} - {self.direccion}"

class Agencia(models.Model):
    id_agencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    # Ubicación Normalizada
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, related_name='agencias')
    
    # Gestión
    responsable = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    
    # Operatividad
    casa_madre = models.ForeignKey(CasaApuestas, on_delete=models.SET_NULL, null=True, related_name='agencias')
    rake_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="% Rake")
    perfiles_minimos = models.IntegerField(default=5)
    url_backoffice = models.URLField(blank=True, null=True)
    
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'agencias'
        verbose_name = 'Agencia'
        verbose_name_plural = 'Agencias'

    def __str__(self):
        return self.nombre

class PerfilOperativo(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfiles_operativos')
    
    # Casa opcional (perfiles sueltos no tienen casa, se selecciona de las disponibles)
    casa = models.ForeignKey(CasaApuestas, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfiles')
    
    # Agencia obligatoria (se selecciona de las disponibles)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name='perfiles')
    
    # Acceso directo al backoffice de la cuenta
    url_acceso_backoffice = models.URLField(blank=True, null=True, help_text="Link al backoffice de la cuenta")
    
    nombre_usuario = models.CharField(max_length=100)
    tipo_jugador = models.CharField(max_length=50, choices=TipoJugadorChoices.choices)
    deporte_dna = models.CharField(max_length=50, choices=DeportesChoices.choices)
    ip_operativa = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    # ciudad_sede ELIMINADO - Se obtiene de agencia.ubicacion
    preferencias = models.TextField(blank=True, null=True)
    nivel_cuenta = models.CharField(max_length=50, choices=NivelCuentaChoices.choices)
    # Campos eliminados: saldo_real, stake_promedio, ops_semanales_actuales, ops_mensuales, ops_historicas
    # Ahora se calculan dinámicamente desde la tabla Operacion
    meta_ops_semanales = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'perfiles_operativos'
        verbose_name = 'Perfil Operativo'
        verbose_name_plural = 'Perfiles Operativos'

    def __str__(self):
        return f"{self.nombre_usuario} - {self.casa.nombre}"

class ConfiguracionOperativa(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    capital_total_activos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    meta_volumen_diario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    perfiles_listos_operar = models.IntegerField(default=0)
    perfiles_en_descanso = models.IntegerField(default=0)
    umbral_saldo_critico = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actualizar_meta_diariamente = models.BooleanField(default=False)

    class Meta:
        db_table = 'configuracion_operativa'
        verbose_name = 'Configuración Operativa'
        verbose_name_plural = 'Configuraciones Operativas'

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionOperativa.objects.exists():
             # Ensures only one instance exists
            return
        return super(ConfiguracionOperativa, self).save(*args, **kwargs)

    def __str__(self):
        return "Configuración Global"

class TransaccionFinanciera(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(PerfilOperativo, on_delete=models.CASCADE, related_name='transacciones')
    tipo_transaccion = models.CharField(max_length=50) # Consider adding choices for this too
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_transaccion = models.DateTimeField()
    metodo_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=50) # Consider adding choices for this

    class Meta:
        db_table = 'transacciones_financieras'
        verbose_name = 'Transacción Financiera'
        verbose_name_plural = 'Transacciones Financieras'

class PlanificacionRotacion(models.Model):
    id_planificacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(PerfilOperativo, on_delete=models.CASCADE, related_name='planificaciones')
    fecha = models.DateField()
    estado_dia = models.CharField(max_length=1, choices=[('A', 'Activo'), ('D', 'Descanso')])
    mes = models.IntegerField()
    anio = models.IntegerField()

    class Meta:
        db_table = 'planificacion_rotacion'
        verbose_name = 'Planificación Rotación'
        verbose_name_plural = 'Planificaciones de Rotación'

class AlertaOperativa(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    tipo_alerta = models.CharField(max_length=100)
    descripcion = models.TextField()
    severidad = models.CharField(max_length=20)
    perfil_afectado = models.ForeignKey(PerfilOperativo, on_delete=models.CASCADE, null=True, blank=True)
    casa_afectada = models.ForeignKey(CasaApuestas, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'alertas_operativas'
        verbose_name = 'Alerta Operativa'
        verbose_name_plural = 'Alertas Operativas'

class BitacoraMando(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(PerfilOperativo, on_delete=models.CASCADE, related_name='entradas_bitacora')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField()
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'bitacora_mando'
        verbose_name = 'Bitácora de Mando'
        verbose_name_plural = 'Bitácoras de Mando'

class Operacion(models.Model):
    id_operacion = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(PerfilOperativo, on_delete=models.CASCADE, related_name='operaciones_reales')
    fecha_registro = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora exacta de la operación")
    importe = models.DecimalField(max_digits=12, decimal_places=2, help_text="Stake o monto apostado")
    cuota = models.DecimalField(max_digits=6, decimal_places=2, help_text="Odds de la apuesta")
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('GANADA', 'Ganada'),
        ('PERDIDA', 'Perdida'),
        ('ANULADA', 'Anulada')
    ], default='PENDIENTE')
    payout = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Retorno total (Stake + Profit)")
    profit_loss = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Resultado neto (P&L)")
    
    deporte = models.CharField(max_length=50, blank=True, null=True)
    mercado = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: Ganador del partido, Over 2.5")

    class Meta:
        db_table = 'operaciones'
        verbose_name = 'Operación'
        verbose_name_plural = 'Operaciones'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"Op {self.id_operacion} - {self.perfil} - ${self.importe}"

    def save(self, *args, **kwargs):
        # Auto-calc P&L if payout is set
        if self.payout is not None and self.importe:
            self.profit_loss = self.payout - self.importe
        super(Operacion, self).save(*args, **kwargs)
