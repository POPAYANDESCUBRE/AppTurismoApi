from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import InformacionBase, Usuario


# ---------------------------------------------------------------------------
# Red Social — catálogo de plataformas (Facebook, Instagram, TikTok…)
# ---------------------------------------------------------------------------

class RedSocial(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)
    icono_url = models.URLField(blank=True, default='')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "gestiones.RedSocial"
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"


# ---------------------------------------------------------------------------
# Enlace Red Social — Vínculo genérico con cualquier entidad
# ---------------------------------------------------------------------------

class EnlaceRedSocial(InformacionBase):
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='vinculos')
    
    # Configuración de Relación Genérica (Polimórfica)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    url_perfil = models.URLField()

    def __str__(self):
        return f"{self.content_object} — {self.red_social.nombre}"

    class Meta:
        db_table = "gestiones.EnlaceRedSocial"
        verbose_name = "Enlace Red Social"
        verbose_name_plural = "Enlaces Redes Sociales"
        unique_together = ('content_type', 'object_id', 'red_social')
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]


# ---------------------------------------------------------------------------
# Valoración / Reseña — Vínculo genérico con cualquier entidad
# ---------------------------------------------------------------------------

class ValoracionComentario(InformacionBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='valoraciones')
    
    # Configuración de Relación Genérica (Polimórfica)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    texto = models.TextField(blank=True, default='')
    valoracion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    interacciones = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Valoración {self.valoracion}/5 por {self.usuario} en {self.content_object}"

    class Meta:
        db_table = "gestiones.ValoracionComentario"
        verbose_name = "Valoracion Comentario"
        verbose_name_plural = "Valoraciones Comentarios"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['usuario']),
            models.Index(fields=['valoracion']),
        ]


# ---------------------------------------------------------------------------
# Favorito — Vínculo genérico para guardar lugares preferidos
# ---------------------------------------------------------------------------

class Favorito(InformacionBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    
    # Configuración de Relación Genérica (Polimórfica)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.usuario} marcó como favorito {self.content_object}"

    class Meta:
        db_table = "gestiones.Favorito"
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        unique_together = ('usuario', 'content_type', 'object_id')
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['usuario']),
        ]
