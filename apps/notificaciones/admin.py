from django.contrib import admin
from .models import Notificacion, PreferenciaNotificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'titulo', 'tipo', 'prioridad', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'prioridad', 'leida', 'fecha_creacion')
    search_fields = ('titulo', 'mensaje', 'usuario__correo')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    fieldsets = (
        ('Información Principal', {
            'fields': ('usuario', 'titulo', 'mensaje', 'tipo', 'prioridad')
        }),
        ('Multimedia', {
            'fields': ('icono', 'imagen', 'enlace')
        }),
        ('Estado', {
            'fields': ('leida', 'fecha_lectura', 'estado')
        }),
        ('Metadata', {
            'fields': ('datos_extra', 'fecha_creacion', 'fecha_actualizacion', 'eliminado_en')
        }),
    )


@admin.register(PreferenciaNotificacion)
class PreferenciaNotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'push_enabled', 'email_enabled')
    search_fields = ('usuario__correo',)

    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Tipos de Notificaciones', {
            'fields': (
                'notificaciones_sistema',
                'notificaciones_lugares',
                'notificaciones_eventos',
                'notificaciones_alertas',
                'notificaciones_promociones',
                'notificaciones_recordatorios',
            )
        }),
        ('Métodos', {
            'fields': ('push_enabled', 'email_enabled')
        }),
        ('Horarios', {
            'fields': ('no_molestar_inicio', 'no_molestar_fin')
        }),
    )
