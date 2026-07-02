from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from apps.gestiones.models import RedSocial, EnlaceRedSocial, ValoracionComentario, Favorito
from apps.restaurantes.models import Restaurante
from apps.lugaresturisticos.models import LugarTuristico
from apps.alojamientos.models import Alojamiento
from apps.eventos.models import Evento
from apps.noticias.models import Noticia

MODEL_MAPPING = {
    'restaurante': Restaurante,
    'lugarturistico': LugarTuristico,
    'alojamiento': Alojamiento,
    'evento': Evento,
    'noticia': Noticia,
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
        
        if tipo and id_ent:
            model_class = MODEL_MAPPING.get(tipo)
            if not model_class.objects.filter(id=id_ent).exists():
                raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
                
            data['content_type'] = ContentType.objects.get_for_model(model_class)
            data['object_id'] = id_ent
            
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
        read_only_fields = ('usuario', 'fecha_creacion', 'fecha_actualizacion', 'estado', 'interacciones')

    def validate(self, data):
        tipo = data.get('tipo_entidad')
        id_ent = data.get('id_entidad')
        
        if tipo and id_ent:
            model_class = MODEL_MAPPING.get(tipo)
            if not model_class.objects.filter(id=id_ent).exists():
                raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
                
            data['content_type'] = ContentType.objects.get_for_model(model_class)
            data['object_id'] = id_ent
            
            data.pop('tipo_entidad')
            data.pop('id_entidad')
            
        return data


class FavoritoSerializer(serializers.ModelSerializer):
    #WRITE: Para crear favoritos
    tipo_entidad = serializers.ChoiceField(choices=list(MODEL_MAPPING.keys()), write_only=True)
    id_entidad = serializers.IntegerField(write_only=True)
    
    #Read: Para mostrar favoritos
    tipo_entidad_display = serializers.SerializerMethodField(read_only=True)
    id_entidad_display = serializers.IntegerField(source='object_id', read_only=True)

    class Meta:
        model = Favorito
        fields = [
            'id', 'usuario', 'tipo_entidad', 'id_entidad', 'tipo_entidad_display', 'id_entidad_display',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('usuario', 'fecha_creacion', 'fecha_actualizacion', 'estado')

    def get_tipo_entidad_display(self, obj):
        content_type = obj.content_type
        for key, model_class in MODEL_MAPPING.items():
            if content_type.model_class() == model_class:
                return key
        return None
            
    def validate(self, data):
        tipo = data.get('tipo_entidad')
        id_ent = data.get('id_entidad')
        
        if tipo and id_ent:
            model_class = MODEL_MAPPING.get(tipo)
            if not model_class.objects.filter(id=id_ent).exists():
                raise serializers.ValidationError(f"No existe un {tipo} con el ID {id_ent}.")
                
            data['content_type'] = ContentType.objects.get_for_model(model_class)
            data['object_id'] = id_ent
            
            data.pop('tipo_entidad')
            data.pop('id_entidad')
            
        return data
