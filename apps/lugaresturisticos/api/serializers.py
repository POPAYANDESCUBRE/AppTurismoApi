from apps.lugaresturisticos.models import LugarTuristico, ImagenLugar, EtiquetaLugar, TipoLugarTuristico
from rest_framework import serializers


class ImagenLugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenLugar
        fields = ['id', 'lugar', 'url', 'orden', 'fecha_creacion']
        read_only_fields = ('fecha_creacion',)


class EtiquetaLugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtiquetaLugar
        fields = ['id', 'lugar', 'etiqueta', 'fecha_creacion']
        read_only_fields = ('fecha_creacion',)


class TipoLugarTuristicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLugarTuristico
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class LugarTuristicoSerializer(serializers.ModelSerializer):
    imagenes = ImagenLugarSerializer(many=True, read_only=True)
    etiquetas = EtiquetaLugarSerializer(many=True, read_only=True)
    is_favorito = serializers.SerializerMethodField()

    class Meta:
        model = LugarTuristico
        fields = [
            'id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud',
            'imagen', 'hora_apertura', 'hora_cierre', 'precio_entrada', 'telefono', 'sitio_web',
            'rating_avg', 'rating_count', 'es_destacado', 'tipo_lugar_turistico',
            'imagenes', 'etiquetas', 'is_favorito',
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
