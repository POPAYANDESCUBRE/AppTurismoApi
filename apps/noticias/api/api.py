from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from apps.noticias.models import Noticia
from .serializers import NoticiaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class NoticiaViewset(viewsets.ModelViewSet):
    queryset = Noticia.objects.filter(estado=True)
    serializer_class = NoticiaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'nivel_alerta', 'es_destacada']
    search_fields = ['titulo', 'extracto']
    ordering_fields = ['publicado_en', 'fecha_creacion']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
