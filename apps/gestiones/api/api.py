from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .serializers import (
    RedSocialSerializer,
    EnlaceRedSocialSerializer,
    ValoracionComentarioSerializer,
    FavoritoSerializer,
    MODEL_MAPPING
)
from apps.gestiones.models import (
    RedSocial,
    EnlaceRedSocial,
    ValoracionComentario,
    Favorito,
)


class RedSocialViewset(viewsets.ModelViewSet):
    queryset = RedSocial.objects.all()
    serializer_class = RedSocialSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Red Social creada.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @transaction.atomic
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


class EnlaceRedSocialViewset(viewsets.ModelViewSet):
    queryset = EnlaceRedSocial.objects.all().select_related('red_social', 'content_type')
    serializer_class = EnlaceRedSocialSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo = self.request.query_params.get('tipo_entidad')
        id_ent = self.request.query_params.get('id_entidad')
        
        if tipo in MODEL_MAPPING:
            ct = ContentType.objects.get_for_model(MODEL_MAPPING[tipo])
            qs = qs.filter(content_type=ct)
        if id_ent:
            qs = qs.filter(object_id=id_ent)
            
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Eliminado.'}, status=status.HTTP_204_NO_CONTENT)


class ValoracionComentarioViewset(viewsets.ModelViewSet):
    queryset = ValoracionComentario.objects.all().select_related('usuario', 'content_type')
    serializer_class = ValoracionComentarioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo = self.request.query_params.get('tipo_entidad')
        id_ent = self.request.query_params.get('id_entidad')
        
        if tipo in MODEL_MAPPING:
            ct = ContentType.objects.get_for_model(MODEL_MAPPING[tipo])
            qs = qs.filter(content_type=ct)
        if id_ent:
            qs = qs.filter(object_id=id_ent)
            
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Valoración creada.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @transaction.atomic
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


class FavoritoViewset(viewsets.ModelViewSet):
    queryset = Favorito.objects.all().select_related('usuario', 'content_type')
    serializer_class = FavoritoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()
        return Response({'status': 'success', 'message': 'Favorito eliminado.'}, status=status.HTTP_204_NO_CONTENT)
