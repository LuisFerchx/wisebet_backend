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
    TENIS_DE_MESA = "TENIS_DE_MESA", "Tennis de Mesa"
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
