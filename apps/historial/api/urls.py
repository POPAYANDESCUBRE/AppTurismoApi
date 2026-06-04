from rest_framework import routers
from .api import HistorialNavegacionViewset

router = routers.DefaultRouter()
router.register('historial', HistorialNavegacionViewset, 'historial')

urlpatterns = router.urls
