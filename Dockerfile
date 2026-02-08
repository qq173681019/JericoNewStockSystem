# Railway Deployment Dockerfile
# This Dockerfile provides a reliable alternative to Nixpacks
# which has been deprecated by Railway

FROM python:3.11.7-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Create /tmp/data directory for cloud environment
RUN mkdir -p /tmp/data

# Expose port for documentation (Railway sets PORT at runtime)
EXPOSE 8080

# Start command using gunicorn
# Railway will provide the PORT environment variable at runtime
# Using shell form to enable environment variable expansion
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - --log-level info app:app"
