"""
Script para crear datos de prueba para la aplicación TurismoAPP
Ejecutar con: python manage.py shell < create_sample_data.py
"""

from apps.lugaresturisticos.models import LugarTuristico, TipoLugarTuristico
from apps.usuarios.models import Usuario, TipoDeCuenta

# Crear tipos de lugares si no existen
tipos_lugares = [
    "Iglesia",
    "Museo",
    "Parque",
    "Plaza",
    "Monumento Histórico",
    "Centro Cultural"
]

print("📍 Creando tipos de lugares turísticos...")
for tipo_nombre in tipos_lugares:
    tipo, created = TipoLugarTuristico.objects.get_or_create(
        nombre=tipo_nombre,
        defaults={'estado': True}
    )
    if created:
        print(f"  ✓ Creado: {tipo_nombre}")
    else:
        print(f"  - Ya existe: {tipo_nombre}")

# Crear lugares turísticos de prueba
lugares_prueba = [
    {
        "nombre": "Puente del Humilladero",
        "descripcion": "Puente histórico de ladrillo construido en 1873, uno de los símbolos más representativos de Popayán. Conecta el centro histórico con el barrio El Callejón.",
        "direccion": "Calle 2 con Carrera 6, Popayán",
        "latitud": 2.4419,
        "longitud": -76.6063,
        "tipo_lugar_turistico": "Monumento Histórico",
        "hora_apertura": "06:00:00",
        "hora_cierre": "22:00:00",
        "precio_entrada": 0,
        "telefono": "",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Parque Caldas",
        "descripcion": "Plaza principal de Popayán, rodeada de edificaciones coloniales. Centro neurálgico de la ciudad con árboles centenarios y bancos de piedra.",
        "direccion": "Carrera 6 con Calle 5, Popayán",
        "latitud": 2.4422,
        "longitud": -76.6066,
        "tipo_lugar_turistico": "Plaza",
        "hora_apertura": "00:00:00",
        "hora_cierre": "23:59:00",
        "precio_entrada": 0,
        "telefono": "",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Iglesia de San Francisco",
        "descripcion": "Templo colonial del siglo XVIII, considerado uno de los más hermosos de Popayán. Destaca por su arquitectura barroca y su torre campanario.",
        "direccion": "Calle 4 No. 9-52, Popayán",
        "latitud": 2.4425,
        "longitud": -76.6070,
        "tipo_lugar_turistico": "Iglesia",
        "hora_apertura": "07:00:00",
        "hora_cierre": "18:00:00",
        "precio_entrada": 0,
        "telefono": "+57 2 824 2759",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Morro del Tulcán",
        "descripcion": "Pirámide precolombina de la cultura Nasa, ubicada en un cerro con vista panorámica de Popayán. Sitio arqueológico y ceremonial indígena.",
        "direccion": "Calle 2 Norte, Popayán",
        "latitud": 2.4506,
        "longitud": -76.6030,
        "tipo_lugar_turistico": "Monumento Histórico",
        "hora_apertura": "08:00:00",
        "hora_cierre": "17:00:00",
        "precio_entrada": 5000,
        "telefono": "",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Museo Nacional Guillermo Valencia",
        "descripcion": "Casa museo del poeta payanés Guillermo Valencia. Exhibe mobiliario colonial, obras de arte y documentos históricos de la familia Valencia.",
        "direccion": "Carrera 6 No. 2-69, Popayán",
        "latitud": 2.4418,
        "longitud": -76.6065,
        "tipo_lugar_turistico": "Museo",
        "hora_apertura": "09:00:00",
        "hora_cierre": "17:00:00",
        "precio_entrada": 3000,
        "telefono": "+57 2 824 0683",
        "sitio_web": "https://www.museonacionalguillermovalencia.gov.co",
        "es_destacado": False
    },
    {
        "nombre": "Torre del Reloj",
        "descripcion": "Emblemático campanario del siglo XVII ubicado en el corazón de Popayán. Su reloj marca el paso del tiempo en la ciudad blanca.",
        "direccion": "Carrera 6 con Calle 5, Popayán",
        "latitud": 2.4423,
        "longitud": -76.6067,
        "tipo_lugar_turistico": "Monumento Histórico",
        "hora_apertura": "00:00:00",
        "hora_cierre": "23:59:00",
        "precio_entrada": 0,
        "telefono": "",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Pueblito Patojo",
        "descripcion": "Recreación en miniatura de los principales monumentos de Popayán. Ideal para conocer la arquitectura colonial de la ciudad en un solo lugar.",
        "direccion": "Vereda Las Piedras, Popayán",
        "latitud": 2.4650,
        "longitud": -76.5850,
        "tipo_lugar_turistico": "Parque",
        "hora_apertura": "09:00:00",
        "hora_cierre": "17:00:00",
        "precio_entrada": 8000,
        "telefono": "+57 311 747 8965",
        "sitio_web": "",
        "es_destacado": False
    },
    {
        "nombre": "Catedral Basílica de Nuestra Señora de la Asunción",
        "descripcion": "Catedral metropolitana de estilo neoclásico, reconstruida tras el terremoto de 1983. Alberga importantes obras de arte religioso.",
        "direccion": "Carrera 6 con Calle 5, Popayán",
        "latitud": 2.4424,
        "longitud": -76.6068,
        "tipo_lugar_turistico": "Iglesia",
        "hora_apertura": "06:30:00",
        "hora_cierre": "19:00:00",
        "precio_entrada": 0,
        "telefono": "+57 2 824 1924",
        "sitio_web": "",
        "es_destacado": True
    },
    {
        "nombre": "Parque Mosquera",
        "descripcion": "Parque tradicional con estatua del General Tomás Cipriano de Mosquera. Rodeado de casonas coloniales y árboles centenarios.",
        "direccion": "Carrera 5 con Calle 4, Popayán",
        "latitud": 2.4415,
        "longitud": -76.6072,
        "tipo_lugar_turistico": "Parque",
        "hora_apertura": "00:00:00",
        "hora_cierre": "23:59:00",
        "precio_entrada": 0,
        "telefono": "",
        "sitio_web": "",
        "es_destacado": False
    },
    {
        "nombre": "Casa Museo Negret",
        "descripcion": "Museo dedicado al escultor Edgar Negret, uno de los artistas colombianos más importantes del siglo XX. Exhibe esculturas modernistas en metal.",
        "direccion": "Calle 5 No. 10-23, Popayán",
        "latitud": 2.4428,
        "longitud": -76.6078,
        "tipo_lugar_turistico": "Museo",
        "hora_apertura": "09:00:00",
        "hora_cierre": "17:00:00",
        "precio_entrada": 4000,
        "telefono": "+57 2 824 4546",
        "sitio_web": "https://museocasanegret.com",
        "es_destacado": False
    }
]

print("\n🏛️ Creando lugares turísticos de prueba...")
created_count = 0
existing_count = 0

for lugar_data in lugares_prueba:
    tipo_nombre = lugar_data.pop("tipo_lugar_turistico")
    tipo = TipoLugarTuristico.objects.get(nombre=tipo_nombre)

    lugar, created = LugarTuristico.objects.get_or_create(
        nombre=lugar_data["nombre"],
        defaults={
            **lugar_data,
            "tipo_lugar_turistico": tipo,
            "estado": True
        }
    )

    if created:
        print(f"  ✓ Creado: {lugar.nombre}")
        created_count += 1
    else:
        print(f"  - Ya existe: {lugar.nombre}")
        existing_count += 1

print(f"\n✅ Proceso completado:")
print(f"   - Lugares creados: {created_count}")
print(f"   - Lugares existentes: {existing_count}")
print(f"   - Total de lugares: {LugarTuristico.objects.count()}")
print(f"\n🌐 Puedes ver los lugares en: http://127.0.0.1:8000/api/v1/lugares/")