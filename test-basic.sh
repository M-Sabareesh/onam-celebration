#!/bin/bash
# Simple Django test script

echo "=== Testing Django Setup ==="

# Set environment variables
export DJANGO_SETTINGS_MODULE=onam_project.settings.development
export DEBUG=True
export SECRET_KEY=django-insecure-test-key
export DATABASE_URL=sqlite:///db.sqlite3

echo "Installing basic requirements..."
pip install -r requirements-basic.txt

echo "Testing Django imports..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "Testing settings..."
python manage.py check --settings=onam_project.settings.development

echo "Making migrations..."
python manage.py makemigrations --settings=onam_project.settings.development

echo "Running migrations..."
python manage.py migrate --settings=onam_project.settings.development

echo "Testing server start (dry run)..."
python manage.py check --deploy --settings=onam_project.settings.development

echo "=== All tests completed ==="
