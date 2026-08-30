from rest_framework import routers
from .api import RestauranteViewset, CategoriaMenuViewset, TipoRestauranteViewset

router = routers.DefaultRouter()

router.register('restaurantes/tipos', TipoRestauranteViewset, 'tipos_restaurantes')
router.register('restaurantes/categorias-menu', CategoriaMenuViewset, 'categorias_menu')
router.register('restaurantes', RestauranteViewset, 'restaurantes')

urlpatterns = router.urls
