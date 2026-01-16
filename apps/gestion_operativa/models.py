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
    url_backoffice = models.URLField()
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

class Agencia(models.Model):
    id_agencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    responsable = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'agencias'
        verbose_name = 'Agencia'
        verbose_name_plural = 'Agencias'

    def __str__(self):
        return self.nombre

class PerfilOperativo(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfiles_operativos')
    casa = models.ForeignKey(CasaApuestas, on_delete=models.CASCADE, related_name='perfiles')
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE, related_name='perfiles')
    nombre_usuario = models.CharField(max_length=100)
    tipo_jugador = models.CharField(max_length=50, choices=TipoJugadorChoices.choices)
    deporte_dna = models.CharField(max_length=50, choices=DeportesChoices.choices)
    ip_operativa = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    ciudad_sede = models.CharField(max_length=100)
    preferencias = models.TextField(blank=True, null=True)
    nivel_cuenta = models.CharField(max_length=50, choices=NivelCuentaChoices.choices)
    saldo_real = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stake_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ops_semanales_actuales = models.IntegerField(default=0)
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
