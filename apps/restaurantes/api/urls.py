from rest_framework import routers
from .api import CategoriaMenuViewset, RestauranteViewset, PlatoViewset

router = routers.DefaultRouter()

router.register('api/categorias-menu', CategoriaMenuViewset, 'categorias_menu')
router.register('api/restaurantes', RestauranteViewset, 'restaurantes')
router.register('api/platos', PlatoViewset, 'platos')

urlpatterns = router.urls
