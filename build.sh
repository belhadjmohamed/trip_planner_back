#!/usr/bin/env bash
set -e  # Exit immediately if any command fails

echo "=== Starting deployment build ==="

# 1. Install dependencies
pip install -r requirements.txt

# 2. Check database connection
echo "Verifying database connection..."
python manage.py check --database default

# 3. Make and apply migrations
echo "Creating and applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# 4. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build completed successfully ==="