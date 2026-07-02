from rest_framework import serializers
from apps.noticias.models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    contenido = serializers.CharField(source='cuerpo', read_only=True)
    fecha_publicacion = serializers.DateTimeField(source='publicado_en', read_only=True)

    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'contenido', 'imagen', 'fecha_publicacion',
        ]
        read_only_fields = ('fecha_publicacion',)
