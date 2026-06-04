from rest_framework import generics, permissions, status
from rest_framework.response import Response
from apps.usuarios.models import Usuario
from apps.usuarios.api.serializers import UsuarioSerializer
from rest_framework.views import APIView
from django.utils import timezone


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]


class CurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    # Permission is globally IsAuthenticated, but let's be explicit
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Soft delete: deactivate account
        instance.is_active = False
        instance.eliminado_en = timezone.now()
        instance.save()
