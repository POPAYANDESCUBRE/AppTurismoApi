from rest_framework import routers
from .api import NoticiaViewset

router = routers.DefaultRouter()

router.register('noticias', NoticiaViewset, 'noticias')

urlpatterns = router.urls
