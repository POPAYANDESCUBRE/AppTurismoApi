from django.contrib import admin
from apps.usuarios.models import *

# Register your models here.
admin.site.register(Idioma)
admin.site.register(Nacionalidad)
admin.site.register(TipoDeCuenta)
admin.site.register(TipoDocumento)

class UsuarioAdmin(admin.ModelAdmin):
    list_display=("tipo_documento","identificacion","correo","password","nombre","apellido","fecha_nacimiento","idioma","nacionalidad","avatar_url")
    fields=["tipo_documento","identificacion","correo","password","nombre","apellido","fecha_nacimiento","idioma","nacionalidad","avatar_url"]

admin.site.register(Usuario,UsuarioAdmin)
