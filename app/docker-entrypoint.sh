#!/bin/sh

# Apply database migrations
echo "###   Applying database migrations   ###"
python manage.py makemigrations
python manage.py migrate

# Running django tests
echo "###  Running django tests   ###"
python manage.py test LJPS || exit 1

# Start server
echo "###   Starting server   ###"
python manage.py runserver 0.0.0.0:8000