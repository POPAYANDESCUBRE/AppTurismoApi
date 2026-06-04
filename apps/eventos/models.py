from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.usuarios.models import InformacionBase


class TipoEvento(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "eventos.TipoEvento"
        verbose_name = "TipoEvento"
        verbose_name_plural = "TiposEventos"


class Evento(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='media/imagenes/eventos', null=True, blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    hora_apertura = models.TimeField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    es_gratuito = models.BooleanField(default=False)
    cupo_maximo = models.PositiveIntegerField(null=True, blank=True)
    rating_avg = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    es_destacado = models.BooleanField(default=False)

    # Relaciones genéricas (Inversas)
    redes_sociales = GenericRelation('gestiones.EnlaceRedSocial')
    valoraciones = GenericRelation('gestiones.ValoracionComentario')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "eventos.Evento"
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
