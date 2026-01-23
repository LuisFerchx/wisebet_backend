"""
Signals para la app gestion_operativa.

Siguiendo las mejores prácticas de Django para signals:
https://docs.djangoproject.com/en/stable/topics/signals/
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PerfilOperativo, ObjetivoCreacionPerfiles


@receiver(post_save, sender=PerfilOperativo)
def actualizar_objetivo_al_crear_perfil(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se crea un nuevo PerfilOperativo.
    
    Busca objetivos activos (no completados) de la agencia del perfil
    y actualiza automáticamente el contador del objetivo más urgente.
    
    Args:
        sender: El modelo que envió la señal (PerfilOperativo)
        instance: La instancia del perfil que fue guardada
        created: Boolean que indica si fue creada (True) o actualizada (False)
        **kwargs: Argumentos adicionales
    """
    if created:  # Solo cuando se CREA un perfil, no cuando se actualiza
        # Buscar objetivos NO completados de esta agencia, ordenados por urgencia
        objetivo = ObjetivoCreacionPerfiles.objects.filter(
            agencia=instance.agencia,
            completado=False
        ).order_by('fecha_limite').first()  # El más urgente primero
        
        if objetivo:
            # Incrementar el contador
            objetivo.cantidad_completada += 1
            
            # El método save() del modelo marcará completado=True si corresponde
            objetivo.save()
            
            # Log para debugging (opcional, puede quitarse en producción)
            print(
                f"✅ Objetivo actualizado: {objetivo.agencia.nombre} - "
                f"{objetivo.cantidad_completada}/{objetivo.cantidad_objetivo} perfiles"
            )
