# Railway Deployment Dockerfile for SIAPS
# Stock Intelligent Analysis & Prediction System

# Use Python 3.11 slim image for smaller size
FROM python:3.11.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
# curl is needed for health checks
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies including Gunicorn (combined for fewer layers)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create data directory for Railway environment
RUN mkdir -p /tmp/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RAILWAY_ENVIRONMENT=production

# Expose port (Railway will set PORT via environment variable)
EXPOSE 8080

# Health check - uses shell form for reliable PORT variable expansion
# Railway handles network security; binding to 0.0.0.0 is standard for containers
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /bin/sh -c 'curl -f http://127.0.0.1:${PORT:-8080}/ || exit 1'

# Start command using Gunicorn
# - Single worker for Railway's resource limits
# - Sync worker class for simplicity
# - 120s timeout for long-running predictions
# - Preload app for faster startup
# - Bind to 0.0.0.0 with dynamic PORT from Railway
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} \
    --workers 1 \
    --worker-class sync \
    --timeout 120 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
