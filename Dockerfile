# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set environment variables for building
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a temporary directory
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


# Stage 2: Final Production Image (Distroless)
FROM gcr.io/distroless/python3-debian12

# Set work directory
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /install /usr/local
# Copy the application source code
COPY . .

# Set environment variables for production
# We need to explicitly set PYTHONPATH so the distroless runtime finds our packages
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Cloud Run injects $PORT. 
# Since Distroless has NO SHELL, we cannot use 'exec' or shell expansion in CMD.
# We must use the JSON array format and hardcode the default port or use the entrypoint carefully.
# Note: In Cloud Run, the $PORT is usually 8080, but gunicorn will listen on the port we specify.
CMD ["/usr/local/bin/gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "core.wsgi:application"]
