from django.db import models
from apps.usuarios.models import InformacionBase, Usuario


TIPO_NOTIFICACION_CHOICES = [
    ('sistema', 'Sistema'),
    ('lugar', 'Lugar Turístico'),
    ('evento', 'Evento'),
    ('alerta', 'Alerta'),
    ('promocion', 'Promoción'),
    ('recordatorio', 'Recordatorio'),
]

PRIORIDAD_CHOICES = [
    ('baja', 'Baja'),
    ('media', 'Media'),
    ('alta', 'Alta'),
]


class Notificacion(InformacionBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_NOTIFICACION_CHOICES, default='sistema')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media')

    # Datos adicionales opcionales
    icono = models.URLField(null=True, blank=True)
    imagen = models.URLField(null=True, blank=True)
    enlace = models.CharField(max_length=500, null=True, blank=True)  # Enlace interno de la app

    # Estado de lectura
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    # Metadata
    datos_extra = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"{self.usuario.correo} - {self.titulo}"

    class Meta:
        db_table = 'notificaciones"."Notificacion'
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']


class PreferenciaNotificacion(InformacionBase):
    """
    Preferencias de notificaciones del usuario
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='preferencias_notificacion')

    # Tipos de notificaciones habilitadas
    notificaciones_sistema = models.BooleanField(default=True)
    notificaciones_lugares = models.BooleanField(default=True)
    notificaciones_eventos = models.BooleanField(default=True)
    notificaciones_alertas = models.BooleanField(default=True)
    notificaciones_promociones = models.BooleanField(default=True)
    notificaciones_recordatorios = models.BooleanField(default=True)

    # Métodos de notificación
    push_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)

    # Horarios (opcional)
    no_molestar_inicio = models.TimeField(null=True, blank=True)
    no_molestar_fin = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Preferencias de {self.usuario.correo}"

    class Meta:
        db_table = 'notificaciones"."PreferenciaNotificacion'
        verbose_name = "Preferencia de Notificación"
        verbose_name_plural = "Preferencias de Notificaciones"
