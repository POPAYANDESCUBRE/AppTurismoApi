from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.restaurantes.api.urls')),
    path('', include('apps.usuarios.api.urls')),
    path('', include('apps.lugaresturisticos.api.urls')),
    path('', include('apps.gestiones.api.urls')),
    path('', include('apps.eventos.api.urls')),
    path('', include('apps.alojamientos.api.urls')),
    path('api-token-auth/', obtain_auth_token),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # AÑADE ESTA LÍNEA CLAVE para el Restablecimiento de Contraseña
    # La URL base será /api/auth/password_reset/
    path('api/auth/', include('django.contrib.auth.urls'))
]
