from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import InformacionBase, Usuario


class HistorialNavegacion(InformacionBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    visto_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.correo} vió {self.content_object}"

    class Meta:
        db_table = 'historial"."HistorialNavegacion'
        verbose_name = "Historial de Navegación"
        verbose_name_plural = "Historiales de Navegación"
        ordering = ['-visto_en']
        indexes = [
            models.Index(fields=['usuario', 'visto_en']),
            models.Index(fields=['content_type', 'object_id']),
        ]
