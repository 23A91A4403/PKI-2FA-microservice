# =============================
# Stage 1: Builder
# =============================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python packages locally
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# =============================
# Stage 2: Runtime
# =============================
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install cron and timezone
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application and scripts
COPY . .

# Setup cron
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

# Create directories for data and cron logs
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose API port
EXPOSE 8080

# Start cron and FastAPI
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
