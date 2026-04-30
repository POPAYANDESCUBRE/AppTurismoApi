from rest_framework import serializers
from apps.restaurantes.models import CategoriaMenu, Restaurante, Plato


class CategoriaMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMenu
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = [
            'id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud',
            'imagen', 'hora_apertura', 'hora_cierre', 'telefono', 'sitio_web',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = [
            'id', 'restaurante', 'categoria', 'nombre', 'descripcion',
            'precio', 'disponible', 'imagen',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')
