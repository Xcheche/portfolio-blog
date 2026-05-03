#!/bin/sh
set -e

# Wait for PostgreSQL only when using a PostgreSQL backend.
if [ "${DB_ENGINE}" = "django.db.backends.postgresql" ] || [ "${DB_ENGINE}" = "django.db.backends.postgresql_psycopg2" ]; then
  DB_HOST="${DB_HOST:-db}"
  DB_PORT="${DB_PORT:-5432}"

  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
  until python -c "import socket; s=socket.create_connection(('${DB_HOST}', int('${DB_PORT}')), 2); s.close()" 2>/dev/null; do
    sleep 1
  done
  echo "PostgreSQL is available."
fi

exec "$@"
