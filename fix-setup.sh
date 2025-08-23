#!/bin/bash

# Step-by-step fix for Django setup issues
echo "🔧 Fixing Django setup step by step..."

# Activate virtual environment
source venv/bin/activate

echo "Step 1: Install core Django packages first..."
pip install -r requirements-core.txt

echo "Step 2: Test basic Django setup..."
python manage.py check --settings=onam_project.settings.development

echo "Step 3: Create initial migrations..."
python manage.py makemigrations --settings=onam_project.settings.development

echo "Step 4: Run migrations..."
python manage.py migrate --settings=onam_project.settings.development

echo "Step 5: Install additional packages..."
pip install django-bootstrap5 django-phonenumber-field phonenumbers

echo "Step 6: Test with additional packages..."
python manage.py check --settings=onam_project.settings.development

echo "Step 7: Create superuser (optional)..."
echo "Create superuser? (y/n)"
read create_user
if [ "$create_user" = "y" ]; then
    python manage.py createsuperuser --settings=onam_project.settings.development
fi

echo "Step 8: Start development server..."
echo "Starting server at http://localhost:8000"
python manage.py runserver --settings=onam_project.settings.development
