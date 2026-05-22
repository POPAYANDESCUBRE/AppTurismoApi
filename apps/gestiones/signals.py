from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from apps.gestiones.models import ValoracionComentario


@receiver([post_save, post_delete], sender=ValoracionComentario)
def actualizar_rating_entidad(sender, instance, **kwargs):
    # La entidad a la que pertenece esta valoración (ej: LugarTuristico, Restaurante, etc.)
    entidad = instance.content_object
    
    # Verificamos si la entidad tiene los campos de rating
    if hasattr(entidad, 'rating_avg') and hasattr(entidad, 'rating_count'):
        # Recalcular el promedio y conteo de valoraciones activas para esta entidad
        agregados = ValoracionComentario.objects.filter(
            content_type=instance.content_type,
            object_id=instance.object_id,
            estado=True
        ).aggregate(
            promedio=Avg('valoracion'),
            total=Count('id')
        )
        
        entidad.rating_avg = agregados['promedio'] or 0.0
        entidad.rating_count = agregados['total'] or 0
        entidad.save(update_fields=['rating_avg', 'rating_count'])
