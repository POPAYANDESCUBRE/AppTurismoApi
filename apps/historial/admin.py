from django.contrib import admin
from apps.historial.models import HistorialNavegacion


class HistorialNavegacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'content_object', 'visto_en', 'estado')
    list_filter = ('visto_en', 'estado')
    search_fields = ('usuario__correo',)
    readonly_fields = ('visto_en',)


admin.site.register(HistorialNavegacion, HistorialNavegacionAdmin)
