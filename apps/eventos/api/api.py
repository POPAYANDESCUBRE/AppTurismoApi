from .serializers import TipoEventoSerializer, EventoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from apps.eventos.models import TipoEvento, Evento


class TipoEventoViewset(viewsets.ModelViewSet):
    queryset = TipoEvento.objects.activos()
    serializer_class = TipoEventoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Tipo de evento creado.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Los datos han sido actualizados",
            "updated_data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({
            'status': 'success',
            'message': 'Tipo de evento ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)


class EventoViewset(viewsets.ModelViewSet):
    queryset = Evento.objects.activos()
    serializer_class = EventoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Evento creado.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Los datos han sido actualizados",
            "updated_data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({
            'status': 'success',
            'message': 'Evento ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)
