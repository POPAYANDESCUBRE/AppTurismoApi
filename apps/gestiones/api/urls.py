from rest_framework import routers
from django.urls import path
from .api import RedSocialViewset, EnlaceRedSocialViewset, FavoritoViewset, ValoracionComentarioViewset
from .feeds import ConfiguracionView, ExplorarView, MapaPinesView, BuscarView

router = routers.DefaultRouter()

router.register('redes-sociales', RedSocialViewset, 'redes_sociales')
router.register('enlaces-redes-sociales', EnlaceRedSocialViewset, 'enlaces_redes_sociales')
router.register('favoritos', FavoritoViewset, 'favoritos')
router.register('valoraciones', ValoracionComentarioViewset, 'valoraciones')

urlpatterns = [
    path('configuracion/', ConfiguracionView.as_view(), name='configuracion'),
    path('explorar/', ExplorarView.as_view(), name='explorar'),
    path('mapa/pines/', MapaPinesView.as_view(), name='mapa_pines'),
    path('buscar/', BuscarView.as_view(), name='buscar'),
] + router.urls
