#!/bin/bash
# Production deployment script for Render
# This script handles database migrations and static files

echo "🚀 Starting Onam Celebration deployment..."

# Set environment
export DJANGO_SETTINGS_MODULE=onam_project.settings.production

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Apply database migrations
echo "🗄️  Applying database migrations..."
python manage.py migrate --noinput

# Create database cache table
echo "💾 Creating cache table..."
python manage.py createcachetable

# Collect static files (clear old ones first)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create placeholder Maveli images if they don't exist
echo "🖼️  Setting up Maveli images..."
mkdir -p staticfiles/images

# Copy Maveli images from media to static if they exist
if [ -f "media/Maveli/Maveli.jpg" ]; then
    cp media/Maveli/*.jpg staticfiles/images/ 2>/dev/null || true
    cp media/Maveli/*.png staticfiles/images/ 2>/dev/null || true
    echo "✅ Copied Maveli images from media to static"
else
    # Create placeholder files if media images don't exist
    touch staticfiles/images/Maveli.jpg
    touch staticfiles/images/Maveli2.jpg
    touch staticfiles/images/Maveli2.png
    touch staticfiles/images/Maveli4.jpg
    echo "📝 Created Maveli image placeholders"
fi

# Also copy to static directory for local development
mkdir -p static/images
if [ -f "media/Maveli/Maveli.jpg" ]; then
    cp media/Maveli/*.jpg static/images/ 2>/dev/null || true
    cp media/Maveli/*.png static/images/ 2>/dev/null || true
    echo "✅ Copied Maveli images to static/images for development"
fi

echo "✅ Deployment completed successfully!"
echo "🎉 Onam celebration website is ready!"
