from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.usuarios.models import InformacionBase


class TipoAlojamiento(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "alojamientos.TipoAlojamiento"
        verbose_name = "TipoAlojamiento"
        verbose_name_plural = "TipoAlojamientos"


class TipoHabitacion(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "alojamientos.TipoHabitacion"
        verbose_name = "TipoHabitacion"
        verbose_name_plural = "TiposHabitaciones"


class Alojamiento(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='media/imagenes/alojamientos', null=True, blank=True)
    hora_apertura = models.TimeField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    tipo_alojamiento = models.ForeignKey(TipoAlojamiento, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_personas = models.PositiveIntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True, default='')
    sitio_web = models.URLField(blank=True, default='')

    # Relaciones genéricas (Inversas)
    redes_sociales = GenericRelation('gestiones.EnlaceRedSocial')
    valoraciones = GenericRelation('gestiones.ValoracionComentario')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "alojamientos.Alojamiento"
        verbose_name = "Alojamiento"
        verbose_name_plural = "Alojamientos"
