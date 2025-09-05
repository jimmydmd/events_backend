# --- Etapa 1: instalar dependencias ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copiar dependencias y código antes de instalar
COPY pyproject.toml poetry.lock* README.md /app/
COPY src/ /app/src

# Configurar Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "events_app_backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
