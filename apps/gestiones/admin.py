from django.contrib import admin
from apps.gestiones.models import (
    RedSocial,
    RestauranteRedSocial,
    LugarTuristicoRedSocial,
    AlojamientoRedSocial,
    EventoRedSocial,
    ValoracionComentario,
)

admin.site.register(RedSocial)
admin.site.register(RestauranteRedSocial)
admin.site.register(LugarTuristicoRedSocial)
admin.site.register(AlojamientoRedSocial)
admin.site.register(EventoRedSocial)
admin.site.register(ValoracionComentario)
