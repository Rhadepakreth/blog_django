# syntax=docker/dockerfile:1.4

FROM python:3.13-slim AS base

WORKDIR /app

# Builder stage: install dependencies
FROM base AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

COPY --link requirements.txt ./

# Installer directement dans l'environnement Python du conteneur
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --link blog_django ./blog_django
COPY --link manage.py ./manage.py
RUN mkdir -p /app/media

# Final stage: minimal runtime image
FROM base AS final

RUN useradd -m appuser

WORKDIR /app

# Copier uniquement le code et les dépendances installées
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app/blog_django ./blog_django
COPY --from=builder /app/manage.py ./manage.py
RUN mkdir -p /app/media

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

RUN ls -l /app/staticfiles
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "blog_django.wsgi:application", "--bind", "0.0.0.0:8000"]
