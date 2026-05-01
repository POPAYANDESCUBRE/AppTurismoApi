from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from apps.gestiones.models import RedSocial, EnlaceRedSocial, ValoracionComentario, Favorito
from apps.restaurantes.models import Restaurante
from apps.lugaresturisticos.models import LugarTuristico
from apps.alojamientos.models import Alojamiento
from apps.eventos.models import Evento

MODEL_MAPPING = {
    'restaurante': Restaurante,
    'lugar_turistico': LugarTuristico,
    'alojamiento': Alojamiento,
    'evento': Evento,
}

class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = ['id', 'nombre', 'icono_url', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')


class EnlaceRedSocialSerializer(serializers.ModelSerializer):
    tipo_entidad = serializers.ChoiceField(choices=list(MODEL_MAPPING.keys()), write_only=True)
    id_entidad = serializers.IntegerField(write_only=True)

    class Meta:
        model = EnlaceRedSocial
        fields = [
            'id', 'red_social', 'url_perfil', 
            'tipo_entidad', 'id_entidad',
            'fecha_creacion', 'fecha_actualizacion', 'estado'
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')

    def validate(self, data):
        tipo = data.get('tipo_entidad')
        id_ent = data.get('id_entidad')
        
        model_class = MODEL_MAPPING.get(tipo)
        if not model_class.objects.filter(id=id_ent).exists():
            raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
            
        data['content_type'] = ContentType.objects.get_for_model(model_class)
        data['object_id'] = id_ent
        
        # Limpiar campos auxiliares antes de crear la instancia
        data.pop('tipo_entidad')
        data.pop('id_entidad')
        
        return data


class ValoracionComentarioSerializer(serializers.ModelSerializer):
    tipo_entidad = serializers.ChoiceField(choices=list(MODEL_MAPPING.keys()), write_only=True)
    id_entidad = serializers.IntegerField(write_only=True)

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
        
        model_class = MODEL_MAPPING.get(tipo)
        if not model_class.objects.filter(id=id_ent).exists():
            raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
            
        data['content_type'] = ContentType.objects.get_for_model(model_class)
        data['object_id'] = id_ent
        
        # Limpiar campos auxiliares
        data.pop('tipo_entidad')
        data.pop('id_entidad')
        
        return data


class FavoritoSerializer(serializers.ModelSerializer):
    tipo_entidad = serializers.ChoiceField(choices=list(MODEL_MAPPING.keys()), write_only=True)
    id_entidad = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorito
        fields = [
            'id', 'usuario', 'tipo_entidad', 'id_entidad',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')

    def validate(self, data):
        tipo = data.get('tipo_entidad')
        id_ent = data.get('id_entidad')
        
        model_class = MODEL_MAPPING.get(tipo)
        if not model_class.objects.filter(id=id_ent).exists():
            raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
            
        data['content_type'] = ContentType.objects.get_for_model(model_class)
        data['object_id'] = id_ent
        
        # Limpiar campos auxiliares
        data.pop('tipo_entidad')
        data.pop('id_entidad')
        
        return data
