#!/usr/bin/env bash
set -e  # Exit on error

# Redirect all output to stdout and stderr
exec > >(tee -a /tmp/render-build.log) 2>&1

echo "===== STARTING BUILD ====="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# 1. Debug: List all files (verify build.sh exists)
echo "Current directory contents:"
ls -al

# 2. Install dependencies
echo "Installing requirements..."
pip install -r requirements.txt

# 3. Database checks
echo "Checking database connection..."
python manage.py check --database default

# 4. Migrations (with verbose output)
echo "Migration status before:"
python manage.py showmigrations

echo "Creating migrations..."
python manage.py makemigrations --noinput --verbosity 3

echo "Applying migrations..."
python manage.py migrate --noinput --verbosity 3

echo "Migration status after:"
python manage.py showmigrations

# 5. Final verification
echo "Checking if trips_trip exists..."
python manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(\"SELECT to_regclass('trips_trip')\")
    print('trips_trip exists?', cursor.fetchone()[0])
"

echo "===== BUILD FINISHED ====="