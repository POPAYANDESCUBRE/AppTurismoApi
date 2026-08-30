from django.contrib import admin
from apps.restaurantes.models import CategoriaMenu, Restaurante, Plato, TipoRestaurante

admin.site.register(TipoRestaurante)
admin.site.register(CategoriaMenu)
admin.site.register(Restaurante)
admin.site.register(Plato)
