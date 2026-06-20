#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Ensure data directory exists (GCP VM: set DATA_DIR=/var/data)
if [ "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
fi

# Run migrations on both databases
echo "Applying migrations to global.db..."
python manage.py migrate --database=default --noinput

echo "Applying migrations to user.db..."
python manage.py migrate --database=user_db --noinput

# Create superuser if environment variables are set
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || echo "Superuser already exists or creation failed"
fi

# Ensure staticfiles directory exists
mkdir -p /app/staticfiles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start the application using daphne (ASGI)
echo "Starting Daphne server..."
exec daphne pu_mp.asgi:application --port 8000 --bind 0.0.0.0
