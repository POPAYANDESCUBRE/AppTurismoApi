from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

# Models
from apps.usuarios.models import Idioma, Nacionalidad, TipoDeCuenta, TipoDocumento
from apps.lugaresturisticos.models import TipoLugarTuristico, LugarTuristico
from apps.eventos.models import TipoEvento, Evento
from apps.alojamientos.models import TipoAlojamiento, TipoHabitacion, Alojamiento
from apps.restaurantes.models import CategoriaMenu, Restaurante
from apps.gestiones.models import RedSocial
from apps.noticias.models import Noticia

# Serializers
from apps.usuarios.api.serializers import IdiomaSerializer, NacionalidadSerializer, TipoDeCuentaSerializer, TipoDocumentoSerializer
from apps.lugaresturisticos.api.serializers import TipoLugarTuristicoSerializer
from apps.eventos.api.serializers import TipoEventoSerializer
from apps.alojamientos.api.serializers import TipoAlojamientoSerializer, TipoHabitacionSerializer
from apps.restaurantes.api.serializers import CategoriaMenuSerializer
from apps.gestiones.api.serializers import RedSocialSerializer


class ConfiguracionView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        return Response({
            "idiomas": IdiomaSerializer(Idioma.objects.filter(estado=True), many=True).data,
            "nacionalidades": NacionalidadSerializer(Nacionalidad.objects.filter(estado=True), many=True).data,
            "tipos_documento": TipoDocumentoSerializer(TipoDocumento.objects.filter(estado=True), many=True).data,
            "tipos_cuenta": TipoDeCuentaSerializer(TipoDeCuenta.objects.filter(estado=True), many=True).data,
            "tipos_lugar": TipoLugarTuristicoSerializer(TipoLugarTuristico.objects.filter(estado=True), many=True).data,
            "tipos_evento": TipoEventoSerializer(TipoEvento.objects.filter(estado=True), many=True).data,
            "tipos_alojamiento": TipoAlojamientoSerializer(TipoAlojamiento.objects.filter(estado=True), many=True).data,
            "tipos_habitacion": TipoHabitacionSerializer(TipoHabitacion.objects.filter(estado=True), many=True).data,
            "categorias_menu": CategoriaMenuSerializer(CategoriaMenu.objects.filter(estado=True), many=True).data,
            "redes_sociales": RedSocialSerializer(RedSocial.objects.filter(estado=True), many=True).data,
        })


def get_compact_dict(obj):
    # Helps return compact serialized dictionaries
    base = {
        "id": obj.id,
        "nombre": getattr(obj, 'nombre', getattr(obj, 'titulo', '')),
        "imagen": obj.imagen.url if obj.imagen else None,
        "es_destacado": getattr(obj, 'es_destacado', getattr(obj, 'es_destacada', False)),
    }
    if hasattr(obj, 'rating_avg'):
        base['rating_avg'] = obj.rating_avg
    if hasattr(obj, 'latitud'):
        base['latitud'] = obj.latitud
        base['longitud'] = obj.longitud
    return base


class ExplorarView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.now()
        next_week = now + timedelta(days=7)

        # Serializers importados
        from apps.lugaresturisticos.api.serializers import LugarTuristicoSerializer
        from apps.eventos.api.serializers import EventoSerializer
        from apps.noticias.api.serializers import NoticiaSerializer
        from apps.restaurantes.api.serializers import RestauranteSerializer
        from apps.alojamientos.api.serializers import AlojamientoSerializer

        # Lugares destacados (top 5 con mejor rating)
        lugares_destacados = LugarTuristico.objects.filter(estado=True, es_destacado=True).order_by('-rating_avg')[:5]

        # Eventos próximos (próxima semana + eventos destacados)
        eventos_semana = Evento.objects.filter(
            estado=True,
            fecha_inicio__gte=now
        ).order_by('fecha_inicio')[:5]

        # Noticias recientes (últimas 3)
        noticias_recientes = Noticia.objects.filter(estado=True).order_by('-publicado_en', '-fecha_creacion')[:3]
        
        # Restaurantes destacados (top 5 con mejor rating)
        restaurante_list = Restaurante.objects.filter(estado=True, es_destacado=True).order_by('-rating_avg')[:5]
        
        # Alojamientos destacados (top 5 con mejor rating)
        alojamiento_list = Alojamiento.objects.filter(estado=True, es_destacado=True).order_by('-rating_avg')[:5]

        # ESTRUCTURA SIMPLE QUE EL FRONTEND ESPERA
        return Response({
            "destacados": LugarTuristicoSerializer(lugares_destacados, many=True).data,
            "eventos": EventoSerializer(eventos_semana, many=True).data,
            "noticias": NoticiaSerializer(noticias_recientes, many=True).data,
            "restaurantes": RestauranteSerializer(restaurante_list, many=True).data,
            "alojamientos": AlojamientoSerializer(alojamiento_list, many=True).data,
        })


class MapaPinesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pines = []
        
        for lugar in LugarTuristico.objects.filter(estado=True):
            if lugar.latitud and lugar.longitud:
                pines.append({"id": lugar.id, "tipo": "lugar", "nombre": lugar.nombre, "latitud": lugar.latitud, "longitud": lugar.longitud, "rating_avg": lugar.rating_avg})
                
        for rest in Restaurante.objects.filter(estado=True):
            if rest.latitud and rest.longitud:
                pines.append({"id": rest.id, "tipo": "restaurante", "nombre": rest.nombre, "latitud": rest.latitud, "longitud": rest.longitud, "rating_avg": rest.rating_avg})
                
        for aloj in Alojamiento.objects.filter(estado=True):
            if aloj.latitud and aloj.longitud:
                pines.append({"id": aloj.id, "tipo": "alojamiento", "nombre": aloj.nombre, "latitud": aloj.latitud, "longitud": aloj.longitud, "rating_avg": aloj.rating_avg})
                
        for ev in Evento.objects.filter(estado=True):
            if ev.latitud and ev.longitud:
                pines.append({"id": ev.id, "tipo": "evento", "nombre": ev.nombre, "latitud": ev.latitud, "longitud": ev.longitud, "rating_avg": ev.rating_avg})
                
        return Response(pines)


class BuscarView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({"detail": "La consulta de búsqueda debe tener al menos 2 caracteres."}, status=400)

        lugares = LugarTuristico.objects.filter(estado=True).filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))[:5]
        restaurantes = Restaurante.objects.filter(estado=True).filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))[:5]
        alojamientos = Alojamiento.objects.filter(estado=True).filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))[:5]
        eventos = Evento.objects.filter(estado=True).filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))[:5]
        noticias = Noticia.objects.filter(estado=True).filter(Q(titulo__icontains=query) | Q(extracto__icontains=query))[:5]

        return Response({
            "lugares": [get_compact_dict(o) for o in lugares],
            "restaurantes": [get_compact_dict(o) for o in restaurantes],
            "alojamientos": [get_compact_dict(o) for o in alojamientos],
            "eventos": [get_compact_dict(o) for o in eventos],
            "noticias": [get_compact_dict(o) for o in noticias],
        })
