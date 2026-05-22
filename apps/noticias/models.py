from django.db import models
from apps.usuarios.models import InformacionBase


CATEGORIA_CHOICES = [
    ('eventos', 'Eventos'),
    ('alertas', 'Alertas'),
    ('consejos', 'Consejos'),
    ('cultura', 'Cultura'),
]

NIVEL_ALERTA_CHOICES = [
    ('info', 'Información'),
    ('advertencia', 'Advertencia'),
    ('peligro', 'Peligro'),
]


class Noticia(InformacionBase):
    titulo = models.CharField(max_length=200)
    extracto = models.TextField(blank=True, default='')
    cuerpo = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    imagen = models.URLField(null=True, blank=True)
    nivel_alerta = models.CharField(max_length=20, choices=NIVEL_ALERTA_CHOICES, null=True, blank=True)
    es_destacada = models.BooleanField(default=False)
    publicado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'noticias"."Noticia'
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-publicado_en']
