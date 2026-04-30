from rest_framework import serializers
from apps.gestiones.models import (
    RedSocial,
    RestauranteRedSocial,
    LugarTuristicoRedSocial,
    AlojamientoRedSocial,
    EventoRedSocial,
    ValoracionComentario,
)


class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = ['id', 'nombre', 'icono_url', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class RestauranteRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestauranteRedSocial
        fields = ['id', 'restaurante', 'red_social', 'url_perfil', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class LugarTuristicoRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LugarTuristicoRedSocial
        fields = ['id', 'lugar_turistico', 'red_social', 'url_perfil', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class AlojamientoRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlojamientoRedSocial
        fields = ['id', 'alojamiento', 'red_social', 'url_perfil', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class EventoRedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoRedSocial
        fields = ['id', 'evento', 'red_social', 'url_perfil', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class ValoracionComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValoracionComentario
        fields = [
            'id', 'usuario', 'tipo_entidad', 'id_entidad',
            'texto', 'valoracion', 'interacciones',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado', 'interacciones')

    def validate(self, data):
        tipo = data.get('tipo_entidad')
        id_ent = data.get('id_entidad')
        if not tipo or not id_ent:
            raise serializers.ValidationError("tipo_entidad e id_entidad son obligatorios.")
        return data
