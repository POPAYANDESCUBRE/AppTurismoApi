from django.contrib import admin
from apps.lugaresturisticos.models import LugarTuristico, TipoLugarTuristico, ImagenLugar, EtiquetaLugar


class ImagenLugarInline(admin.TabularInline):
    model = ImagenLugar
    extra = 1


class EtiquetaLugarInline(admin.TabularInline):
    model = EtiquetaLugar
    extra = 1


class LugarTuristicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rating_avg', 'rating_count', 'es_destacado', 'estado')
    list_filter = ('es_destacado', 'estado', 'tipo_lugar_turistico')
    inlines = [ImagenLugarInline, EtiquetaLugarInline]


# Register your models here.
admin.site.register(LugarTuristico, LugarTuristicoAdmin)
admin.site.register(TipoLugarTuristico)