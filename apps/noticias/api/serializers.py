from rest_framework import serializers
from apps.noticias.models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'extracto', 'cuerpo', 'categoria',
            'imagen', 'nivel_alerta', 'es_destacada', 'publicado_en',
            'fecha_creacion', 'fecha_actualizacion', 'estado',
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado')
