# Docker configuration for ADK Course

FROM python:3.11-slim

LABEL maintainer="ADK Course Contributors"
LABEL description="Development environment for ADK Scratch Course"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="/app/src"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash adk && \
    chown -R adk:adk /app
USER adk

# Copy requirements first for better caching
COPY --chown=adk:adk requirements*.txt ./

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY --chown=adk:adk . .

# Install package in development mode
RUN pip install --user -e .

# Add user's local bin to PATH
ENV PATH="/home/adk/.local/bin:${PATH}"

# Create necessary directories
RUN mkdir -p /app/{logs,data,credentials,agents}

# Set up default configuration
RUN adk-setup || true

# Expose ports for development
EXPOSE 8000 8080 8888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import adk_course; print('OK')" || exit 1

# Default command
CMD ["bash"]
