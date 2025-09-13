#!/bin/sh
set -e

if [ ! -f "/app/aperture.db" ]; then
    echo "Creating database tables..."
    python run_db.py
else
    echo "Database already exists, skipping creation..."
fi

exec "$@"
