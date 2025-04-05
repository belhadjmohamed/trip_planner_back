#!/usr/bin/env bash

# Install dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files for Django Admin
python manage.py collectstatic --noinput