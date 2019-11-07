#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z users-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py recreate_db
python manage.py seed_db
gunicorn --config src/users/gunicorn_hooks.py --workers 4 --worker-class gevent --preload --timeout 5 --bind 0.0.0.0:$PORT --access-logfile - --log-file - manage:app
