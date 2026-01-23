from django.apps import AppConfig


class GestionOperativaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.gestion_operativa"

    def ready(self):
        """
        Importar signals cuando la app está lista.
        
        Siguiendo las mejores prácticas de Django:
        https://docs.djangoproject.com/en/stable/topics/signals/#connecting-receiver-functions
        """
        import apps.gestion_operativa.signals  # noqa: F401
