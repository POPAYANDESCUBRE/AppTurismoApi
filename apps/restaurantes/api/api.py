from .serializers import CategoriaMenuSerializer, RestauranteSerializer, PlatoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from apps.restaurantes.models import CategoriaMenu, Restaurante, Plato


class CategoriaMenuViewset(viewsets.ModelViewSet):
    queryset = CategoriaMenu.objects.activos()
    serializer_class = CategoriaMenuSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Categoria de menu creada.",
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
            'message': 'Categoria de menu ha sido Eliminada.'
        }, status=status.HTTP_204_NO_CONTENT)


class RestauranteViewset(viewsets.ModelViewSet):
    queryset = Restaurante.objects.activos()
    serializer_class = RestauranteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Restaurante creado.",
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
            'message': 'El Restaurante ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)


class PlatoViewset(viewsets.ModelViewSet):
    queryset = Plato.objects.activos().select_related('restaurante', 'categoria')
    serializer_class = PlatoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        restaurante_id = self.request.query_params.get('restaurante')
        if restaurante_id:
            qs = qs.filter(restaurante_id=restaurante_id)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Plato creado.",
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
            'message': 'El Plato ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)
