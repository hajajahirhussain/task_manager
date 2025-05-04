#!/bin/bash

# Wait for the database to be ready
./wait-for-it.sh "$DB_HOST:$DB_PORT" --timeout=30 --strict -- echo "Database is up!"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the app with Gunicorn
gunicorn taskmanager.wsgi:application --bind 0.0.0.0:8000
