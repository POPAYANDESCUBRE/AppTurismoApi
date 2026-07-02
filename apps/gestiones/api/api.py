from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from apps.gestiones.models import Favorito, ValoracionComentario, RedSocial, EnlaceRedSocial
from .serializers import FavoritoSerializer, ValoracionComentarioSerializer, RedSocialSerializer, EnlaceRedSocialSerializer


class RedSocialViewset(viewsets.ReadOnlyModelViewSet):
    queryset = RedSocial.objects.all()
    serializer_class = RedSocialSerializer


class EnlaceRedSocialViewset(viewsets.ModelViewSet):
    queryset = EnlaceRedSocial.objects.all()
    serializer_class = EnlaceRedSocialSerializer
    
    def get_permissions(self):
        return [permissions.IsAdminUser()]

    def perform_destroy(self, instance):
        instance.estado = False
        instance.eliminado_en = timezone.now()
        instance.save()


class FavoritoViewset(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user, estado=True)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Ensure user can only create for themselves
        serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.delete()  # Hard delete

class ValoracionComentarioViewset(viewsets.ModelViewSet):
    serializer_class = ValoracionComentarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return current user's own reviews
        return ValoracionComentario.objects.filter(usuario=self.request.user, estado=True)

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
