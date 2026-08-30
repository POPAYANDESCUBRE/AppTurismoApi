from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 routes
    path('api/v1/', include('apps.usuarios.api.urls')),
    path('api/v1/', include('apps.lugaresturisticos.api.urls')),
    path('api/v1/', include('apps.restaurantes.api.urls')),
    path('api/v1/', include('apps.alojamientos.api.urls')),
    path('api/v1/', include('apps.eventos.api.urls')),
    path('api/v1/', include('apps.noticias.api.urls')),
    path('api/v1/', include('apps.gestiones.api.urls')),
    path('api/v1/', include('apps.mascota.api.urls')),
    path('api/v1/', include('apps.historial.api.urls')),
    path('api/v1/', include('apps.notificaciones.api.urls')),

    # API Documentation
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
