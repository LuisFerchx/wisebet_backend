from django.db import models


class DeportesChoices(models.TextChoices):
    FUTBOL = "FUTBOL", "Fútbol"
    BASKETBALL = "BASKETBALL", "Basketball"
    TENNIS = "TENNIS", "Tennis"
    BEISBOL = "BEISBOL", "Béisbol"
    AMERICANO = "AMERICANO", "Fútbol Americano"
    HOCKEY = "HOCKEY", "Hockey"
    BOXEO = "BOXEO", "Boxeo"
    UFC = "UFC", "UFC"
    OTROS = "OTROS", "Otros"


class TipoJugadorChoices(models.TextChoices):
    PROFESIONAL = "PROFESIONAL", "Profesional"
    RECREATIVO = "RECREATIVO", "Recreativo"
    CASUAL = "CASUAL", "Casual"
    HIGH_ROLLER = "HIGH_ROLLER", "High Roller"


class NivelCuentaChoices(models.TextChoices):
    BRONCE = "BRONCE", "Bronce"
    PLATA = "PLATA", "Plata"
    ORO = "ORO", "Oro"
    PLATINO = "PLATINO", "Platino"
    DIAMANTE = "DIAMANTE", "Diamante"


class TipoDocumentoChoices(models.TextChoices):
    CEDULA = "CEDULA", "Cédula de Identidad"
    PASAPORTE = "PASAPORTE", "Pasaporte"
    LICENCIA = "LICENCIA", "Licencia de Conducir"
    DNI = "DNI", "DNI"
    OTRO = "OTRO", "Otro"


class TipoTransaccionChoices(models.TextChoices):
    DEPOSITO = "DEPOSITO", "Depósito"
    RETIRO = "RETIRO", "Retiro"
    AJUSTE = "AJUSTE", "Ajuste"
    BONO = "BONO", "Bono"


class MetodoPagoChoices(models.TextChoices):
    USDT = "USDT", "USDT (Tether)"
    SKRILL = "SKRILL", "Skrill"
    NETELLER = "NETELLER", "Neteller"
    BANCO = "BANCO", "Transferencia Bancaria"
    EFECTIVO = "EFECTIVO", "Efectivo"
    PAYPAL = "PAYPAL", "PayPal"
    CRIPTO_OTRO = "CRIPTO_OTRO", "Otra Criptomoneda"


class EstadoTransaccionChoices(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    COMPLETADA = "COMPLETADA", "Completada"
    RECHAZADA = "RECHAZADA", "Rechazada"
    CANCELADA = "CANCELADA", "Cancelada"


class TipoAlertaChoices(models.TextChoices):
    SALDO_CRITICO = "SALDO_CRITICO", "Saldo Crítico"
    ESCASEZ_OPERATIVA = "ESCASEZ_OPERATIVA", "Escasez Operativa"
    CAPITAL_INSUFICIENTE = "CAPITAL_INSUFICIENTE", "Capital Insuficiente"
    META_NO_ALCANZADA = "META_NO_ALCANZADA", "Meta No Alcanzada"
    INACTIVIDAD = "INACTIVIDAD", "Inactividad Prolongada"


class SeveridadChoices(models.TextChoices):
    BAJA = "BAJA", "Baja"
    MEDIA = "MEDIA", "Media"
    ALTA = "ALTA", "Alta"
    CRITICA = "CRITICA", "Crítica"


class EstadoAlertaChoices(models.TextChoices):
    ACTIVA = "ACTIVA", "Activa"
    EN_REVISION = "EN_REVISION", "En Revisión"
    RESUELTA = "RESUELTA", "Resuelta"


class EstadoOperacionChoices(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    GANADA = "GANADA", "Ganada"
    PERDIDA = "PERDIDA", "Perdida"
    ANULADA = "ANULADA", "Anulada"


class EstadoDiaChoices(models.TextChoices):
    ACTIVO = "A", "Activo"
    DESCANSO = "D", "Descanso"
