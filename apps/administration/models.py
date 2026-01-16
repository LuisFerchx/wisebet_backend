from django.db import models
from django.conf import settings

class Agency(models.Model):
    responsible = models.ForeignKey(
        'Profile', 
        on_delete=models.CASCADE, 
        related_name='agencies',
        verbose_name='Dueño Responsable'
    )
    betting_house = models.CharField(
        max_length=100, 
        verbose_name='Casa de Apuestas'
    )
    rake_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name='Rake %'
    )
    min_recommended_profiles = models.IntegerField(
        verbose_name='Perfiles Mín. Recomendados'
    )
    backoffice_link = models.URLField(
        verbose_name='Enlace Backoffice',
        blank=True, 
        null=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Agencia'
        verbose_name_plural = 'Agencias'
        db_table = 'agencies'

    def __str__(self):
        return f"{self.betting_house} - {self.responsible}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Agencia'
    )
    username = models.CharField(max_length=100, verbose_name='Nombre de Usuario')
    betting_house_id = models.CharField(max_length=100, verbose_name='ID Casa', blank=True, null=True)
    
    player_type = models.CharField(max_length=100, verbose_name='Tipo de Jugador', blank=True, null=True)
    sport_dna = models.CharField(max_length=100, verbose_name='Deporte DNA', blank=True, null=True)
    operational_ip = models.GenericIPAddressField(verbose_name='IP Operativa', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Ciudad Sede', blank=True, null=True)
    preferences = models.TextField(verbose_name='Preferencias', blank=True, null=True)
    
    account_level = models.CharField(max_length=50, verbose_name='Nivel de Cuenta', blank=True, null=True)
    real_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Saldo Real')
    avg_stake = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Stake Promedio')
    
    current_weekly_ops = models.IntegerField(default=0, verbose_name='Ops Semanales Actuales')
    weekly_ops_goal = models.IntegerField(default=0, verbose_name='Meta Ops Semanales')
    
    observations = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil Operativo'
        verbose_name_plural = 'Perfiles Operativos'
        db_table = 'operational_profiles'

    def __str__(self):
        return self.username
