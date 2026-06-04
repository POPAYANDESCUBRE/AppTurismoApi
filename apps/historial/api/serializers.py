from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from apps.historial.models import HistorialNavegacion
from apps.gestiones.api.serializers import MODEL_MAPPING


class HistorialNavegacionSerializer(serializers.ModelSerializer):
    tipo_entidad = serializers.ChoiceField(choices=list(MODEL_MAPPING.keys()), write_only=True)
    id_entidad = serializers.IntegerField(write_only=True)

    class Meta:
        model = HistorialNavegacion
        fields = [
            'id', 'usuario', 'tipo_entidad', 'id_entidad', 'visto_en',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('usuario', 'visto_en', 'fecha_creacion', 'fecha_actualizacion', 'estado')

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
