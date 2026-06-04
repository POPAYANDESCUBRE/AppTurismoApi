from rest_framework import serializers
from apps.eventos.models import TipoEvento, Evento


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class EventoSerializer(serializers.ModelSerializer):
    is_favorito = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud',
            'imagen', 'fecha_inicio', 'fecha_fin', 'hora_apertura', 'hora_cierre',
            'tipo_evento', 'precio', 'es_gratuito', 'cupo_maximo',
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
