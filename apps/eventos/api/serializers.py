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
    tipo = serializers.SerializerMethodField()
    promedio_valoracion = serializers.FloatField(source='rating_avg', read_only=True)
    lugar = serializers.CharField(source='direccion', read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id', 'nombre', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin',
            'imagen', 'lugar', 'promedio_valoracion',
        ]
        read_only_fields = ('promedio_valoracion', 'lugar')

    def get_tipo(self, obj):
        if obj.tipo_evento:
            return {
                'id': obj.tipo_evento.id,
                'nombre': obj.tipo_evento.nombre
            }
        return None
