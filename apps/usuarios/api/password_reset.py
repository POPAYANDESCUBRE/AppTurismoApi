from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.usuarios.models import Usuario
from rest_framework.permissions import AllowAny

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        correo = request.data.get("correo")

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "Correo no registrado."}, status=status.HTTP_404_NOT_FOUND)

        token = get_random_string(length=32)
        cache.set(token, usuario.id, timeout=900)  # 15 minutos

        reset_link = f"https://tuapp.com/reset-password?token={token}"

        send_mail(
            subject="Recuperación de contraseña",
            message=f"Hola {usuario.nombre}, usa el siguiente enlace para restablecer tu contraseña:\n\n{reset_link}",
            from_email="no-reply@tuapp.com",
            recipient_list=[correo],
            fail_silently=False,
        )

        return Response({"message": "Se ha enviado un correo de recuperación."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get("token")
        nueva_contraseña = request.data.get("password")

        if not token or not nueva_contraseña:
            return Response({"error": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        usuario_id = cache.get(token)
        if not usuario_id:
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = Usuario.objects.get(id=usuario_id)
        usuario.set_password(nueva_contraseña)
        usuario.save()

        cache.delete(token)

        return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)
