# Usar Python 3.12 slim como base única
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    DJANGO_SETTINGS_MODULE=core.settings.railway

WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

# Copiar el código de la aplicación
COPY . .

# Recolectar archivos estáticos
# Usar una base de datos SQLite temporal para evitar requerir PostgreSQL durante el build
RUN DJANGO_SECRET_KEY=build-time-secret \
    DATABASE_URL=sqlite:///tmp/build.db \
    python manage.py collectstatic --noinput

# Exponer el puerto (Railway usa la variable $PORT)
EXPOSE 8080

# Comando para iniciar la aplicación
# Usar sh -c para que Railway pueda expandir la variable $PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 120 core.wsgi:application"]
