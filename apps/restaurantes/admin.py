from django.contrib import admin
from apps.restaurantes.models import CategoriaMenu, Restaurante, Plato

admin.site.register(CategoriaMenu)
admin.site.register(Restaurante)
admin.site.register(Plato)
