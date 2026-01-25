from rest_framework import routers
from .api import IdiomaViewset, NacionalidadViewSet, TipoDeCuentaViewSet, TipoDocumentoViewSet, UsuarioViewSet
from .password_reset import ForgotPasswordView, ResetPasswordView
from django.urls import path

router = routers.DefaultRouter()

router.register('api/idiomas', IdiomaViewset, 'idiomas')
router.register('api/nacionalidades', NacionalidadViewSet, 'nacionalidades')
router.register('api/tipos_de_cuenta', TipoDeCuentaViewSet, 'tipos_de_cuenta')
router.register('api/tipos_documentos', TipoDocumentoViewSet, 'tipos_documentos')
router.register('api/usuarios', UsuarioViewSet, 'usuarios')

# Rutas adicionales para recuperación de contraseña
urlpatterns = [
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]


urlpatterns += router.urls
