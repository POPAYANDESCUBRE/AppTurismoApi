from rest_framework import routers
from .api import (
    RedSocialViewset,
    RestauranteRedSocialViewset,
    LugarTuristicoRedSocialViewset,
    AlojamientoRedSocialViewset,
    EventoRedSocialViewset,
    ValoracionComentarioViewset,
)

router = routers.DefaultRouter()

router.register('api/redes-sociales', RedSocialViewset, 'redes_sociales')
router.register('api/restaurantes-redes-sociales', RestauranteRedSocialViewset, 'restaurantes_redes_sociales')
router.register('api/lugares-redes-sociales', LugarTuristicoRedSocialViewset, 'lugares_redes_sociales')
router.register('api/alojamientos-redes-sociales', AlojamientoRedSocialViewset, 'alojamientos_redes_sociales')
router.register('api/eventos-redes-sociales', EventoRedSocialViewset, 'eventos_redes_sociales')
router.register('api/valoraciones', ValoracionComentarioViewset, 'valoraciones')

urlpatterns = router.urls
