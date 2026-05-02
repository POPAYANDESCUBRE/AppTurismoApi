from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': gcp_secrets_dict.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': gcp_secrets_dict.get('DB_NAME', 'postgres'),
        'USER': gcp_secrets_dict.get('DB_USER', ''),
        'PASSWORD': gcp_secrets_dict.get('DB_PASSWORD', ''),
        'HOST': gcp_secrets_dict.get('DB_HOST', 'localhost'),
        'PORT': gcp_secrets_dict.get('DB_PORT', '5432'),
        'OPTIONS': {
            'options': f"-c search_path={gcp_secrets_dict.get('DB_SCHEMA', 'public')}"
        }
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
