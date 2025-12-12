# ARCHITECT AI — Dockerfile (2025)
# Monero Only • No Refunds • No Leaks

FROM python:3.12-slim AS builder

# System deps (minimal, no Tor, no bloat)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user (security)
RUN adduser --disabled-password --gecos '' architect
WORKDIR /home/architect

# Copy only what we need
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app + assets
COPY app.py .
COPY assets/ ./assets/
COPY Modelfile ./

# Switch to non-root
USER architect

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the empire
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
