from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.lugaresturisticos.models import LugarTuristico, ImagenLugar, EtiquetaLugar, TipoLugarTuristico
from apps.gestiones.models import ValoracionComentario
from .serializers import LugarTuristicoSerializer, ImagenLugarSerializer, EtiquetaLugarSerializer
from apps.gestiones.api.serializers import ValoracionComentarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.contenttypes.models import ContentType


class TipoLugarTuristicoViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TipoLugarTuristico.objects.all()
    # Serializer not currently explicitly requested but necessary. Reusing implicit or creating a simple one later.
    # Actually wait, we don't have a TipoLugarTuristicoSerializer, let's just make one inline or rely on one.
    pass  # We need to create a serializer for this in serializers.py


class LugarTuristicoViewset(viewsets.ModelViewSet):
    queryset = LugarTuristico.objects.filter(estado=True).prefetch_related('imagenes', 'etiquetas')
    serializer_class = LugarTuristicoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_lugar_turistico', 'es_destacado']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['rating_avg', 'rating_count', 'nombre']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'imagenes', 'etiquetas', 'valoraciones']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'agregar_valoracion':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()

    @action(detail=True, methods=['get', 'post'])
    def imagenes(self, request, pk=None):
        lugar = self.get_object()
        if request.method == 'GET':
            imagenes = lugar.imagenes.all()
            serializer = ImagenLugarSerializer(imagenes, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['lugar'] = lugar.id
            serializer = ImagenLugarSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path=r'imagenes/(?P<img_id>\d+)')
    def eliminar_imagen(self, request, pk=None, img_id=None):
        lugar = self.get_object()
        try:
            imagen = lugar.imagenes.get(id=img_id)
            imagen.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ImagenLugar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get', 'post'])
    def etiquetas(self, request, pk=None):
        lugar = self.get_object()
        if request.method == 'GET':
            etiquetas = lugar.etiquetas.all()
            serializer = EtiquetaLugarSerializer(etiquetas, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['lugar'] = lugar.id
            serializer = EtiquetaLugarSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path=r'etiquetas/(?P<tag_id>\d+)')
    def eliminar_etiqueta(self, request, pk=None, tag_id=None):
        lugar = self.get_object()
        try:
            etiqueta = lugar.etiquetas.get(id=tag_id)
            etiqueta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EtiquetaLugar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get', 'post'])
    def valoraciones(self, request, pk=None):
        lugar = self.get_object()
        ct = ContentType.objects.get_for_model(LugarTuristico)
        
        if request.method == 'GET':
            valoraciones = ValoracionComentario.objects.filter(content_type=ct, object_id=lugar.id, estado=True)
            page = self.paginate_queryset(valoraciones)
            if page is not None:
                serializer = ValoracionComentarioSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ValoracionComentarioSerializer(valoraciones, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            data = request.data.copy()
            data['tipo_entidad'] = 'lugarturistico'
            data['id_entidad'] = lugar.id

            # Si es un "like" (valoracion=5 y sin texto), verificar que no exista otro like del usuario
            if data.get('valoracion') == 5 and not data.get('texto'):
                if ValoracionComentario.objects.filter(
                    content_type=ct,
                    object_id=lugar.id,
                    usuario=request.user,
                    valoracion=5,
                    texto__isnull=True,
                    estado=True
                ).exists():
                    return Response({"detail": "Ya has dado 'Me gusta' a este lugar."}, status=status.HTTP_400_BAD_REQUEST)

            # Si es un comentario (con texto), permitir múltiples comentarios
            # No hay restricción

            serializer = ValoracionComentarioSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
