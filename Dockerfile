# Schopenhauer's Will - Docker Image
# Multi-stage build for optimized production image

# ==============================================================================
# Stage 1: Build stage
# ==============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ".[api]"

# ==============================================================================
# Stage 2: Production stage
# ==============================================================================
FROM python:3.11-slim AS production

LABEL maintainer="Schopenhauer Contributors"
LABEL description="Schopenhauer's Will - Word Document Generator API"
LABEL version="0.1.1"

# Security: Run as non-root user
RUN groupadd -r schopenhauer && useradd -r -g schopenhauer schopenhauer

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY pyproject.toml .

# Install the package
RUN pip install --no-cache-dir -e .

# Create temp directory for uploads
RUN mkdir -p /tmp/schopenhauer && \
    chown -R schopenhauer:schopenhauer /tmp/schopenhauer

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Switch to non-root user
USER schopenhauer

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:${PORT}/health')" || exit 1

# Expose port
EXPOSE ${PORT}

# Run the API server
CMD ["sh", "-c", "uvicorn will.api:app --host 0.0.0.0 --port ${PORT}"]

# ==============================================================================
# Stage 3: Development stage (optional)
# ==============================================================================
FROM production AS development

USER root

# Install development dependencies
RUN pip install --no-cache-dir ".[dev]"

USER schopenhauer

# Override CMD for development
CMD ["sh", "-c", "uvicorn will.api:app --host 0.0.0.0 --port ${PORT} --reload"]
