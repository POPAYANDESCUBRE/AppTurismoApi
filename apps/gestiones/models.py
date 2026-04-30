from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import InformacionBase, Usuario
from apps.restaurantes.models import Restaurante
from apps.lugaresturisticos.models import LugarTuristico
from apps.eventos.models import Evento
from apps.alojamientos.models import Alojamiento


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
# Tablas junction RED_SOCIAL ↔ entidad (una por entidad, según el diagrama)
# url_perfil almacena la URL específica de esa entidad en esa red social.
# ---------------------------------------------------------------------------

class RestauranteRedSocial(InformacionBase):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='redes_sociales')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='restaurantes')
    url_perfil = models.URLField()

    def __str__(self):
        return f"{self.restaurante.nombre} — {self.red_social.nombre}"

    class Meta:
        db_table = "gestiones.RestauranteRedSocial"
        verbose_name = "Restaurante Red Social"
        verbose_name_plural = "Restaurantes Redes Sociales"
        unique_together = ('restaurante', 'red_social')


class LugarTuristicoRedSocial(InformacionBase):
    lugar_turistico = models.ForeignKey(LugarTuristico, on_delete=models.CASCADE, related_name='redes_sociales')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='lugares_turisticos')
    url_perfil = models.URLField()

    def __str__(self):
        return f"{self.lugar_turistico.nombre} — {self.red_social.nombre}"

    class Meta:
        db_table = "gestiones.LugarTuristicoRedSocial"
        verbose_name = "Lugar Turistico Red Social"
        verbose_name_plural = "Lugares Turisticos Redes Sociales"
        unique_together = ('lugar_turistico', 'red_social')


class AlojamientoRedSocial(InformacionBase):
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE, related_name='redes_sociales')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='alojamientos')
    url_perfil = models.URLField()

    def __str__(self):
        return f"{self.alojamiento.nombre} — {self.red_social.nombre}"

    class Meta:
        db_table = "gestiones.AlojamientoRedSocial"
        verbose_name = "Alojamiento Red Social"
        verbose_name_plural = "Alojamientos Redes Sociales"
        unique_together = ('alojamiento', 'red_social')


class EventoRedSocial(InformacionBase):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='redes_sociales')
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, related_name='eventos')
    url_perfil = models.URLField()

    def __str__(self):
        return f"{self.evento.nombre} — {self.red_social.nombre}"

    class Meta:
        db_table = "gestiones.EventoRedSocial"
        verbose_name = "Evento Red Social"
        verbose_name_plural = "Eventos Redes Sociales"
        unique_together = ('evento', 'red_social')


# ---------------------------------------------------------------------------
# Valoración / Reseña — patrón polimórfico (tipo_entidad + id_entidad)
# Sustituye los 4 FK nullable anteriores.
# ---------------------------------------------------------------------------

class ValoracionComentario(InformacionBase):
    LUGAR_TURISTICO = 'lugar_turistico'
    EVENTO = 'evento'
    ALOJAMIENTO = 'alojamiento'
    RESTAURANTE = 'restaurante'

    TIPO_ENTIDAD_CHOICES = [
        (LUGAR_TURISTICO, 'Lugar Turístico'),
        (EVENTO, 'Evento'),
        (ALOJAMIENTO, 'Alojamiento'),
        (RESTAURANTE, 'Restaurante'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='valoraciones')
    tipo_entidad = models.CharField(max_length=20, choices=TIPO_ENTIDAD_CHOICES)
    id_entidad = models.PositiveIntegerField()
    texto = models.TextField(blank=True, default='')
    valoracion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    interacciones = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Valoración {self.valoracion}/5 — {self.get_tipo_entidad_display()} #{self.id_entidad}"

    class Meta:
        db_table = "gestiones.ValoracionComentario"
        verbose_name = "Valoracion Comentario"
        verbose_name_plural = "Valoraciones Comentarios"
        indexes = [
            models.Index(fields=['tipo_entidad', 'id_entidad']),
            models.Index(fields=['usuario']),
            models.Index(fields=['valoracion']),
        ]
