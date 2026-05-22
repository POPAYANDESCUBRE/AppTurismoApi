from rest_framework import viewsets, permissions
from django.utils import timezone
from apps.mascota.models import ConsejoMascota
from .serializers import ConsejoMascotaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ConsejoMascotaViewset(viewsets.ModelViewSet):
    queryset = ConsejoMascota.objects.filter(estado=True)
    serializer_class = ConsejoMascotaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['idioma', 'activo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
