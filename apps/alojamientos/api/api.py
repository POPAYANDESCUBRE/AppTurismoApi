from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.alojamientos.models import Alojamiento, TipoAlojamiento, TipoHabitacion
from apps.gestiones.models import ValoracionComentario
from .serializers import AlojamientoSerializer, TipoAlojamientoSerializer, TipoHabitacionSerializer
from apps.gestiones.api.serializers import ValoracionComentarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.contenttypes.models import ContentType


class TipoAlojamientoViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TipoAlojamiento.objects.all()
    serializer_class = TipoAlojamientoSerializer


class TipoHabitacionViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TipoHabitacion.objects.all()
    serializer_class = TipoHabitacionSerializer


class AlojamientoViewset(viewsets.ModelViewSet):
    queryset = Alojamiento.objects.filter(estado=True)
    serializer_class = AlojamientoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_alojamiento', 'tipo_habitacion', 'es_destacado']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'rating_avg', 'nombre']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'valoraciones']:
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
    def valoraciones(self, request, pk=None):
        alojamiento = self.get_object()
        ct = ContentType.objects.get_for_model(Alojamiento)
        
        if request.method == 'GET':
            valoraciones = ValoracionComentario.objects.filter(content_type=ct, object_id=alojamiento.id, estado=True)
            page = self.paginate_queryset(valoraciones)
            if page is not None:
                serializer = ValoracionComentarioSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ValoracionComentarioSerializer(valoraciones, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            data = request.data.copy()
            data['tipo_entidad'] = 'alojamiento'
            data['id_entidad'] = alojamiento.id

            # Si es un "like" (valoracion=5 y sin texto), verificar que no exista otro like del usuario
            if data.get('valoracion') == 5 and not data.get('texto'):
                if ValoracionComentario.objects.filter(
                    content_type=ct,
                    object_id=alojamiento.id,
                    usuario=request.user,
                    valoracion=5,
                    texto__isnull=True,
                    estado=True
                ).exists():
                    return Response({"detail": "Ya has dado 'Me gusta' a este alojamiento."}, status=status.HTTP_400_BAD_REQUEST)

            # Si es un comentario (con texto), permitir múltiples comentarios
            # No hay restricción

            serializer = ValoracionComentarioSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
