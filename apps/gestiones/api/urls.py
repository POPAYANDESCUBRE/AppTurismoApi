from rest_framework import routers
from .api import (
    RedSocialViewset,
    EnlaceRedSocialViewset,
    ValoracionComentarioViewset,
    FavoritoViewset,
)

router = routers.DefaultRouter()

router.register('api/redes-sociales', RedSocialViewset, 'redes_sociales')
router.register('api/enlaces-redes-sociales', EnlaceRedSocialViewset, 'enlaces_redes_sociales')
router.register('api/valoraciones', ValoracionComentarioViewset, 'valoraciones')
router.register('api/favoritos', FavoritoViewset, 'favoritos')

urlpatterns = router.urls
