from rest_framework import routers
from .api import AlojamientoViewset, TipoAlojamientoViewset, TipoHabitacionViewset

router = routers.DefaultRouter()

router.register('alojamientos/tipos', TipoAlojamientoViewset, 'tipos_alojamiento')
router.register('alojamientos/tipos-habitacion', TipoHabitacionViewset, 'tipos_habitacion')
router.register('alojamientos', AlojamientoViewset, 'alojamientos')

urlpatterns = router.urls