from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from apps.historial.models import HistorialNavegacion
from .serializers import HistorialNavegacionSerializer


class HistorialNavegacionViewset(viewsets.ModelViewSet):
    serializer_class = HistorialNavegacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HistorialNavegacion.objects.filter(usuario=self.request.user, estado=True)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
