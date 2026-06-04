from rest_framework import serializers
from apps.restaurantes.models import CategoriaMenu, Restaurante, Plato


class CategoriaMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMenu
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class RestauranteSerializer(serializers.ModelSerializer):
    is_favorito = serializers.SerializerMethodField()

    class Meta:
        model = Restaurante
        fields = [
            'id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud',
            'imagen', 'hora_apertura', 'hora_cierre', 'telefono', 'sitio_web',
            'rating_avg', 'rating_count', 'es_destacado', 'is_favorito',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado', 'rating_avg', 'rating_count')

    def get_is_favorito(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from django.contrib.contenttypes.models import ContentType
            from apps.gestiones.models import Favorito
            ct = ContentType.objects.get_for_model(obj)
            return Favorito.objects.filter(usuario=request.user, content_type=ct, object_id=obj.id).exists()
        return False


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = [
            'id', 'restaurante', 'categoria', 'nombre', 'descripcion',
            'precio', 'disponible', 'imagen',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')
