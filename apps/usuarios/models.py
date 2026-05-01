from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import PersonalizacionUsuario


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(estado=True)

class GlobalManager(models.Manager):
    pass


class InformacionBase(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)
    
    objects = BaseManager()
    objects_all = GlobalManager()

    class Meta:
        abstract = True


class Idioma(InformacionBase):
    nombre = models.CharField(verbose_name="Nombre", max_length=50, unique=True)
    codigo = models.CharField(verbose_name="Codigo", max_length=10, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuarios.Idioma"
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"


class Nacionalidad(InformacionBase):
    nombre = models.CharField(verbose_name="Nombre", max_length=50, unique=True)
    codigo = models.CharField(verbose_name="Codigo", max_length=10, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuarios.Nacionalidad"
        verbose_name = "Nacionalidad"
        verbose_name_plural = "Nacionalidades"


class TipoDeCuenta(InformacionBase):
    nombre = models.CharField(verbose_name="Nombre", max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuarios.TipoDeCuenta"
        verbose_name = "TipoDeCuenta"
        verbose_name_plural = "TiposDeCuentas"


class TipoDocumento(InformacionBase):
    nombre = models.CharField(verbose_name="Nombre", max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuarios.TipoDocumento"
        verbose_name = "TipoDocumento"
        verbose_name_plural = "TiposDocumentos"


class Usuario(AbstractBaseUser, PermissionsMixin):
    tipo_de_cuenta = models.ForeignKey(TipoDeCuenta, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    identificacion = models.CharField(max_length=100, null=True, blank=True, unique=True)
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True, blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField("Habilitado", default=True)
    is_staff = models.BooleanField("Acceso al admin", default=False)

    objects = PersonalizacionUsuario()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return self.correo

    class Meta:
        db_table = "usuarios.Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
