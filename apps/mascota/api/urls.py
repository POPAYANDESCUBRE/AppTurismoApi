from rest_framework import routers
from .api import ConsejoMascotaViewset

router = routers.DefaultRouter()
router.register('mascota/consejos', ConsejoMascotaViewset, 'consejos_mascota')

urlpatterns = router.urls
