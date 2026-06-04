from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.usuarios.models import InformacionBase


class TipoLugarTuristico(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "lugaresturisticos.TipoLugarTuristico"
        verbose_name = "TipoLugarTuristico"
        verbose_name_plural = "TiposLugaresTuristicos"


class LugarTuristico(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='media/imagenes/lugares-turisticos', null=True, blank=True)
    hora_apertura = models.TimeField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    tipo_lugar_turistico = models.ForeignKey(TipoLugarTuristico, on_delete=models.SET_NULL, null=True, blank=True)
    precio_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True, default='')
    sitio_web = models.URLField(blank=True, default='')
    rating_avg = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    es_destacado = models.BooleanField(default=False)

    # Relaciones genéricas (Inversas)
    redes_sociales = GenericRelation('gestiones.EnlaceRedSocial')
    valoraciones = GenericRelation('gestiones.ValoracionComentario')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "lugaresturisticos.LugarTuristico"
        verbose_name = "LugarTuristico"
        verbose_name_plural = "LugaresTuristicos"


class ImagenLugar(models.Model):
    lugar = models.ForeignKey(LugarTuristico, on_delete=models.CASCADE, related_name='imagenes')
    url = models.URLField()
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lugar.nombre} — imagen {self.orden}"

    class Meta:
        db_table = 'lugaresturisticos"."ImagenLugar'
        verbose_name = "Imagen Lugar"
        verbose_name_plural = "Imágenes Lugar"
        ordering = ['orden']


class EtiquetaLugar(models.Model):
    lugar = models.ForeignKey(LugarTuristico, on_delete=models.CASCADE, related_name='etiquetas')
    etiqueta = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lugar.nombre} — {self.etiqueta}"

    class Meta:
        db_table = 'lugaresturisticos"."EtiquetaLugar'
        verbose_name = "Etiqueta Lugar"
        verbose_name_plural = "Etiquetas Lugar"
        unique_together = ('lugar', 'etiqueta')
