from .base import *
from .gcp_secrets import get_secrets_from_gcp
from django.core.exceptions import ImproperlyConfigured

# Obtener secrets de GCP
gcp_secrets_dict = get_secrets_from_gcp()

# SECRET_KEY - CRÍTICO: Sin fallback para forzar configuración correcta
SECRET_KEY = gcp_secrets_dict.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY no configurado en GCP Secrets")

DEBUG = False

ALLOWED_HOSTS = [
    'appturismo-backend-414542781310.us-central1.run.app',
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': gcp_secrets_dict.get('DB_NAME'),
        'USER': gcp_secrets_dict.get('DB_USER'),
        'PASSWORD': gcp_secrets_dict.get('DB_PASSWORD'),
        'HOST': gcp_secrets_dict.get('DB_HOST'),
        'PORT': '5432',
        'OPTIONS': {
            'options': f"-c search_path={gcp_secrets_dict.get('DB_SCHEMA', 'public')}"
        }
    }
}

# CORS para producción
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Desarrollo
    "http://127.0.0.1:8080",
]

# Para apps móviles nativas (Android/iOS)
CORS_ALLOW_ALL_ORIGINS = True  # Apps móviles no envían Origin header estándar

# Logging para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
  }