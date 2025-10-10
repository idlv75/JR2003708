# =============================================================================
# Knight Journey - Production-ready Dockerfile
# =============================================================================
# Multi-stage build for optimized image size
# Supports configurable Python version via build arg
# =============================================================================

ARG PY_VER=3.13

# -----------------------------------------------------------------------------
# Stage 1: Builder - Install dependencies
# -----------------------------------------------------------------------------
FROM python:${PY_VER}-slim AS builder

LABEL maintainer="Knight Journey Team"
LABEL description="Knight Journey CLI Application"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy dependency files and source code
COPY pyproject.toml ./
COPY src/ ./src/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install .

# -----------------------------------------------------------------------------
# Stage 2: Test - Include test dependencies
# -----------------------------------------------------------------------------
FROM builder AS test

# Install test dependencies
RUN pip install pytest pytest-cov

# Copy tests
COPY tests/ ./tests/

# Default test command
CMD ["pytest", "-v", "--cov=knight_journey", "--cov-report=term-missing"]

# -----------------------------------------------------------------------------
# Stage 3: Runtime - Minimal production image
# -----------------------------------------------------------------------------
FROM python:${PY_VER}-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser pyproject.toml ./

# Install package in editable mode
USER appuser
RUN pip install --user -e .

# Set entrypoint
ENTRYPOINT ["python", "-m", "knight_journey"]

# Default command (can be overridden)
CMD ["--input", "/app/input.yaml"]

# Healthcheck (optional, useful for orchestration)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import knight_journey; print('healthy')" || exit 1

# Expose metadata
LABEL version="0.1.0"
LABEL org.opencontainers.image.title="Knight Journey"
LABEL org.opencontainers.image.description="Optimized knight journey path finder"
LABEL org.opencontainers.image.source="https://github.com/yourusername/knight_journey"

