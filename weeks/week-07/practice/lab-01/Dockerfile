FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATABASE_URL=sqlite:////data/products.sqlite

WORKDIR /app
RUN groupadd --system app && useradd --system --gid app --home-dir /app app \
    && mkdir -p /data \
    && chown app:app /data

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app product_api ./product_api
COPY --chown=app:app wsgi.py ./wsgi.py

USER app
EXPOSE 5000
CMD ["sh", "-c", "flask --app wsgi:app init-db && exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile - --error-logfile - wsgi:app"]
