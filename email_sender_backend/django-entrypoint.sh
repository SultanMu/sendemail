#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be available
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Django server
echo "Starting Django server on port 5000..."
exec python manage.py runserver 0.0.0.0:5000
