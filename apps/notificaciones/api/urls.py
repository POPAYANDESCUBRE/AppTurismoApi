from rest_framework import routers
from .api import NotificacionViewset, PreferenciaNotificacionViewset

router = routers.DefaultRouter()
router.register('notificaciones', NotificacionViewset, 'notificaciones')
router.register('preferencias-notificaciones', PreferenciaNotificacionViewset, 'preferencias_notificaciones')

urlpatterns = router.urls
