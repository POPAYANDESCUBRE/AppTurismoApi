from django.contrib import admin
from apps.mascota.models import ConsejoMascota


class ConsejoMascotaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'idioma', 'activo', 'estado')
    list_filter = ('idioma', 'activo', 'estado')
    search_fields = ('texto',)


admin.site.register(ConsejoMascota, ConsejoMascotaAdmin)
