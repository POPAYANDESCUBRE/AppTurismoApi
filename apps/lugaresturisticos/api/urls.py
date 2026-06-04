from rest_framework import routers
from .api import LugarTuristicoViewset, TipoLugarTuristicoViewset

router = routers.DefaultRouter()

router.register('lugares/tipos', TipoLugarTuristicoViewset, 'tipos_lugar')
router.register('lugares', LugarTuristicoViewset, 'lugares')

urlpatterns = router.urls
