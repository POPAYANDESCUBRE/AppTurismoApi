from django.contrib import admin
from apps.noticias.models import Noticia


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'es_destacada', 'publicado_en', 'estado')
    list_filter = ('categoria', 'es_destacada', 'nivel_alerta', 'estado')
    search_fields = ('titulo', 'extracto')


admin.site.register(Noticia, NoticiaAdmin)
