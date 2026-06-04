from .base import *
from pathlib import Path

DEBUG = True

ALLOWED_HOSTS = ['*']

# SQLite para desarrollo local (fácil y sin configuración adicional)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Si prefieres PostgreSQL local, descomenta esto y comenta SQLite arriba:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'turismoapp_db',
#         'USER': 'postgres',
#         'PASSWORD': '12345',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Si prefieres MySQL local, descomenta esto y comenta SQLite y PostgreSQL arriba:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'popayandescubre',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_correo@gmail.com'
# EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicación'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def set_search_path(sender, connection, **kwargs):
    if connection.vendor == 'postgresql':
        schema = gcp_secrets_dict.get('DB_SCHEMA', 'public')
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema}, public;")
