web: python manage.py migrate --noinput && python -m gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
