from rest_framework import routers
from .api import EventoViewset, TipoEventoViewset

router = routers.DefaultRouter()

router.register('eventos/tipos', TipoEventoViewset, 'tipos_evento')
router.register('eventos', EventoViewset, 'eventos')

urlpatterns = router.urls