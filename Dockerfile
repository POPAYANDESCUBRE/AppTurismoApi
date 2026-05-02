# Stage 1: Builder
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies normally in the builder stage
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app code
COPY . .

# Run collectstatic (Whitenoise will use these)
# We set a dummy secret key to avoid errors during the build
RUN DJANGO_SECRET_KEY=collectstatic_dummy_key \
    python3 manage.py collectstatic --noinput


# Stage 2: Final Production Image (Distroless)
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copy the entire python environment from the builder
COPY --from=builder /usr/local /usr/local
# Copy the application source (including the collected staticfiles)
COPY --from=builder /app /app

# Set environment variables
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Cloud Run injects $PORT. 
CMD ["/usr/local/bin/gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "core.wsgi:application"]
