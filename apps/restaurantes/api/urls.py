from rest_framework import routers
from .api import RestauranteViewset, CategoriaMenuViewset

router = routers.DefaultRouter()

router.register('restaurantes/categorias-menu', CategoriaMenuViewset, 'categorias_menu')
router.register('restaurantes', RestauranteViewset, 'restaurantes')

urlpatterns = router.urls
