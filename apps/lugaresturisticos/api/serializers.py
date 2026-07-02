from apps.lugaresturisticos.models import LugarTuristico, ImagenLugar, EtiquetaLugar, TipoLugarTuristico
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.gestiones.models import Favorito

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
    tipo = serializers.SerializerMethodField()
    promedio_valoracion = serializers.FloatField(source='rating_avg', read_only=True)
    is_favorito = serializers.SerializerMethodField(method_name='get_is_favorito')

    class Meta:
        model = LugarTuristico
        fields = [
            'id', 'nombre', 'descripcion', 'tipo', 'latitud', 'longitud',
            'imagen', 'direccion', 'is_favorito', 'promedio_valoracion',
        ]
        read_only_fields = ('promedio_valoracion',)

    def get_is_favorito(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(LugarTuristico)
            return Favorito.objects.filter(
                usuario=request.user,
                content_type=content_type,
                object_id=obj.id,
                estado=True
            ).exists()
        return False
    
    def get_tipo(self, obj):
        if obj.tipo_lugar_turistico:
            return {
                'id': obj.tipo_lugar_turistico.id,
                'nombre': obj.tipo_lugar_turistico.nombre
            }
        return None
