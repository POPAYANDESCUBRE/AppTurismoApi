from django.contrib import admin
from apps.gestiones.models import (
    RedSocial,
    EnlaceRedSocial,
    ValoracionComentario,
    Favorito,
)

admin.site.register(RedSocial)
admin.site.register(EnlaceRedSocial)
admin.site.register(ValoracionComentario)
admin.site.register(Favorito)
