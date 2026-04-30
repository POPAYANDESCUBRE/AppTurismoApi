from apps.usuarios.models import Idioma, Nacionalidad, TipoDeCuenta, TipoDocumento, Usuario
from rest_framework import serializers

class IdiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idioma
        fields = ['id', 'nombre', 'codigo', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        #campos de solo lectura
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado', )
        
class NacionalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nacionalidad
        fields = ['id', 'nombre', 'codigo', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        #campos de solo lectura
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado',)

class TipoDeCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeCuenta
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        #campos de solo lectura
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado', )

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'fecha_creacion', 'fecha_actualizacion', 'estado']
        #campos de solo lectura
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion', 'estado', )

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tipo_documento = serializers.PrimaryKeyRelatedField(
        queryset=TipoDocumento.objects.activos() ,
        required=False,
        allow_null=True 
    )
    idioma = serializers.PrimaryKeyRelatedField(
        queryset=Idioma.objects.activos(),
        required=False,
        allow_null=True
    )
    nacionalidad = serializers.PrimaryKeyRelatedField(
        queryset=Nacionalidad.objects.activos(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Usuario
        fields = ['id', 'tipo_de_cuenta', 'tipo_documento', 'identificacion', 'correo', 'password', 'nombre', 'apellido', 'fecha_nacimiento', 'idioma', 'nacionalidad', 'fecha_creacion', 'fecha_actualizacion', 'is_active']
        read_only_fields = ('tipo_de_cuenta', 'fecha_creacion', 'fecha_actualizacion', 'is_active')
        
    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)