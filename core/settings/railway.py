"""
Configuración de Django para Railway
"""
import os
import dj_database_url
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allowed hosts - Railway proporciona RAILWAY_PUBLIC_DOMAIN
ALLOWED_HOSTS = [
    os.environ.get('RAILWAY_PUBLIC_DOMAIN', ''),
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Todos los subdominios de Railway
]

# Database - Railway proporciona DATABASE_URL automáticamente
# Durante el build, usar SQLite temporal
database_url = os.environ.get('DATABASE_URL', '')

# Solo usar PostgreSQL si DATABASE_URL empieza con postgresql://
if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback a SQLite para build/collectstatic o cuando no hay DATABASE_URL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/build.db',
        }
    }

# CORS para producción
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Para apps móviles nativas (Android/iOS)
CORS_ALLOW_ALL_ORIGINS = True  # Apps móviles no envían Origin header estándar

# Static files (whitenoise ya debe estar configurado en base.py)
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')
MEDIA_URL = '/media/'

# Logging para Railway
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
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
