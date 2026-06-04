from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import InformacionBase


IDIOMA_CHOICES = [
    ('es', 'Español'),
    ('en', 'English'),
]


class ConsejoMascota(InformacionBase):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    texto = models.CharField(max_length=500)
    idioma = models.CharField(max_length=5, choices=IDIOMA_CHOICES, default='es')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Consejo: {self.texto[:50]}..."

    class Meta:
        db_table = 'mascota"."ConsejoMascota'
        verbose_name = "Consejo Mascota"
        verbose_name_plural = "Consejos Mascota"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
