from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.notificaciones.models import Notificacion, PreferenciaNotificacion
from .serializers import NotificacionSerializer, PreferenciaNotificacionSerializer


class NotificacionViewset(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user, estado=True)

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()

    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """
        Marca todas las notificaciones no leídas como leídas
        """
        notificaciones = self.get_queryset().filter(leida=False)
        count = notificaciones.update(leida=True, fecha_lectura=timezone.now())
        return Response({
            'message': f'{count} notificaciones marcadas como leídas',
            'count': count
        })

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """
        Marca una notificación específica como leída
        """
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.fecha_lectura = timezone.now()
        notificacion.save()
        serializer = self.get_serializer(notificacion)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """
        Obtiene todas las notificaciones no leídas
        """
        notificaciones = self.get_queryset().filter(leida=False)
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def contador(self, request):
        """
        Obtiene el contador de notificaciones no leídas
        """
        count = self.get_queryset().filter(leida=False).count()
        return Response({'count': count})


class PreferenciaNotificacionViewset(viewsets.ModelViewSet):
    serializer_class = PreferenciaNotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PreferenciaNotificacion.objects.filter(usuario=self.request.user)

    def get_object(self):
        """
        Obtiene o crea las preferencias del usuario actual
        """
        obj, created = PreferenciaNotificacion.objects.get_or_create(
            usuario=self.request.user
        )
        return obj

    def list(self, request, *args, **kwargs):
        """
        Retorna las preferencias del usuario actual
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Actualiza las preferencias del usuario actual
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
