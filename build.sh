#!/usr/bin/env bash

# Install dependencies
pip install --only-binary :all: backports.zoneinfo psycopg2-binary -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files for Django Admin
python manage.py collectstatic --noinput