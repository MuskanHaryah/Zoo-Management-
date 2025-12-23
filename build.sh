#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate --noinput

# Load initial data (if data.json exists)
if [ -f "data.json" ]; then
    python manage.py loaddata data.json || echo "Data already loaded or error occurred"
fi

# Create caretaker user (will skip if already exists)
python manage.py create_caretaker_user
