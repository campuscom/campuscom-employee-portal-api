#!/bin/bash

cd /opt/app/employee_portal_api
# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Creating database migrations
echo "Applying database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start the server
echo "Starting gunicorn"
gunicorn --workers=3 \
    --threads=6 \
    --worker-class=gthread \
    --chdir=/opt/app/employee_portal_api \
    -b :5002 \
    --log-level=info \
    app.wsgi:application

cd -
