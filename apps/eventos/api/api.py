from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.eventos.models import Evento, TipoEvento
from apps.gestiones.models import ValoracionComentario
from .serializers import EventoSerializer, TipoEventoSerializer
from apps.gestiones.api.serializers import ValoracionComentarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.contenttypes.models import ContentType


class TipoEventoViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer


class EventoViewset(viewsets.ModelViewSet):
    queryset = Evento.objects.filter(estado=True)
    serializer_class = EventoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'tipo_evento': ['exact'],
        'es_destacado': ['exact'],
        'es_gratuito': ['exact'],
        'fecha_inicio': ['gte', 'lte'],
    }
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_inicio', 'precio', 'rating_avg']

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
        evento = self.get_object()
        ct = ContentType.objects.get_for_model(Evento)
        
        if request.method == 'GET':
            valoraciones = ValoracionComentario.objects.filter(content_type=ct, object_id=evento.id, estado=True)
            page = self.paginate_queryset(valoraciones)
            if page is not None:
                serializer = ValoracionComentarioSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ValoracionComentarioSerializer(valoraciones, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            if ValoracionComentario.objects.filter(content_type=ct, object_id=evento.id, usuario=request.user, estado=True).exists():
                return Response({"detail": "Ya has valorado este evento."}, status=status.HTTP_400_BAD_REQUEST)
                
            data = request.data.copy()
            data['tipo_entidad'] = 'evento'
            data['id_entidad'] = evento.id
            
            serializer = ValoracionComentarioSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
