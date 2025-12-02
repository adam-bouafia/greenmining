# Multi-stage build for greenmining
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN pip install --upgrade pip build wheel

# Copy source code
COPY . .

# Build wheel
RUN python -m build

# Production stage
FROM python:3.11-slim

LABEL maintainer="Green Mining Team"
LABEL description="Green Microservices Mining - Analyze sustainability patterns in microservices"
LABEL version="0.1.0"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        && rm -rf /var/lib/apt/lists/*

# Copy wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/

# Install greenmining
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data

# Add non-root user
RUN useradd -m -u 1000 greenmining && \
    chown -R greenmining:greenmining /app

USER greenmining

# Default command
ENTRYPOINT ["greenmining"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD greenmining --version || exit 1
