from rest_framework import serializers
from apps.notificaciones.models import Notificacion, PreferenciaNotificacion


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = [
            'id',
            'titulo',
            'mensaje',
            'tipo',
            'prioridad',
            'icono',
            'imagen',
            'enlace',
            'leida',
            'fecha_lectura',
            'datos_extra',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'usuario']


class PreferenciaNotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciaNotificacion
        fields = [
            'id',
            'notificaciones_sistema',
            'notificaciones_lugares',
            'notificaciones_eventos',
            'notificaciones_alertas',
            'notificaciones_promociones',
            'notificaciones_recordatorios',
            'push_enabled',
            'email_enabled',
            'no_molestar_inicio',
            'no_molestar_fin',
        ]
        read_only_fields = ['id']
