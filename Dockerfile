FROM python:3.13

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN echo '#!/bin/sh' > /app/docker-entrypoint.sh && \
    echo 'set -e' >> /app/docker-entrypoint.sh && \
    echo 'if [ ! -f "/app/aperture.db" ]; then' >> /app/docker-entrypoint.sh && \
    echo '    echo "Creating database tables..."' >> /app/docker-entrypoint.sh && \
    echo '    python run_db.py' >> /app/docker-entrypoint.sh && \
    echo 'else' >> /app/docker-entrypoint.sh && \
    echo '    echo "Database already exists, skipping creation..."' >> /app/docker-entrypoint.sh && \
    echo 'fi' >> /app/docker-entrypoint.sh && \
    echo 'exec "$@"' >> /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

RUN ls -la /app/docker-entrypoint.sh && \
    cat /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8000"]