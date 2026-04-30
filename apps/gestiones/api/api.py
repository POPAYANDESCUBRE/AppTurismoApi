from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .serializers import (
    RedSocialSerializer,
    RestauranteRedSocialSerializer,
    LugarTuristicoRedSocialSerializer,
    AlojamientoRedSocialSerializer,
    EventoRedSocialSerializer,
    ValoracionComentarioSerializer,
)
from apps.gestiones.models import (
    RedSocial,
    RestauranteRedSocial,
    LugarTuristicoRedSocial,
    AlojamientoRedSocial,
    EventoRedSocial,
    ValoracionComentario,
)


class RedSocialViewset(viewsets.ModelViewSet):
    queryset = RedSocial.objects.activos()
    serializer_class = RedSocialSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Red Social creada.",
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
            'message': 'Red Social ha sido Eliminada.'
        }, status=status.HTTP_204_NO_CONTENT)


class RestauranteRedSocialViewset(viewsets.ModelViewSet):
    queryset = RestauranteRedSocial.objects.activos().select_related('restaurante', 'red_social')
    serializer_class = RestauranteRedSocialSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        restaurante_id = self.request.query_params.get('restaurante')
        if restaurante_id:
            qs = qs.filter(restaurante_id=restaurante_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Eliminado.'}, status=status.HTTP_204_NO_CONTENT)


class LugarTuristicoRedSocialViewset(viewsets.ModelViewSet):
    queryset = LugarTuristicoRedSocial.objects.activos().select_related('lugar_turistico', 'red_social')
    serializer_class = LugarTuristicoRedSocialSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        lugar_id = self.request.query_params.get('lugar_turistico')
        if lugar_id:
            qs = qs.filter(lugar_turistico_id=lugar_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Eliminado.'}, status=status.HTTP_204_NO_CONTENT)


class AlojamientoRedSocialViewset(viewsets.ModelViewSet):
    queryset = AlojamientoRedSocial.objects.activos().select_related('alojamiento', 'red_social')
    serializer_class = AlojamientoRedSocialSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        alojamiento_id = self.request.query_params.get('alojamiento')
        if alojamiento_id:
            qs = qs.filter(alojamiento_id=alojamiento_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Eliminado.'}, status=status.HTTP_204_NO_CONTENT)


class EventoRedSocialViewset(viewsets.ModelViewSet):
    queryset = EventoRedSocial.objects.activos().select_related('evento', 'red_social')
    serializer_class = EventoRedSocialSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        evento_id = self.request.query_params.get('evento')
        if evento_id:
            qs = qs.filter(evento_id=evento_id)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Eliminado.'}, status=status.HTTP_204_NO_CONTENT)


class ValoracionComentarioViewset(viewsets.ModelViewSet):
    queryset = ValoracionComentario.objects.activos().select_related('usuario')
    serializer_class = ValoracionComentarioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo = self.request.query_params.get('tipo_entidad')
        id_ent = self.request.query_params.get('id_entidad')
        if tipo:
            qs = qs.filter(tipo_entidad=tipo)
        if id_ent:
            qs = qs.filter(id_entidad=id_ent)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Valoración creada.",
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
            'message': 'La valoración ha sido Eliminada.'
        }, status=status.HTTP_204_NO_CONTENT)
