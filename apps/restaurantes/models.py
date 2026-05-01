from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.usuarios.models import InformacionBase


class CategoriaMenu(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "restaurantes.CategoriaMenu"
        verbose_name = "Categoria Menu"
        verbose_name_plural = "Categorias Menu"


class Restaurante(InformacionBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, default='')
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='media/imagenes/restaurantes', null=True, blank=True)
    hora_apertura = models.TimeField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True, default='')
    sitio_web = models.URLField(blank=True, default='')

    # Relaciones genéricas (Inversas)
    redes_sociales = GenericRelation('gestiones.EnlaceRedSocial')
    valoraciones = GenericRelation('gestiones.ValoracionComentario')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "restaurantes.Restaurante"
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        indexes = [
            models.Index(fields=['latitud', 'longitud']),
            models.Index(fields=['nombre']),
        ]


class Plato(InformacionBase):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='platos')
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.SET_NULL, null=True, blank=True, related_name='platos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='media/imagenes/platos', null=True, blank=True)

    def __str__(self):
        return f"{self.restaurante.nombre} — {self.nombre}"

    class Meta:
        db_table = "restaurantes.Plato"
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        unique_together = ('restaurante', 'nombre')
