#!/bin/bash

# Google Photos Integration Setup Script for Onam Celebration
echo "🔧 Setting up Google Photos integration for treasure hunt photos..."

# Extract album ID from the provided URL
ALBUM_URL="https://photos.app.goo.gl/sDnZoj5VnkZ4yByS6"
ALBUM_ID="sDnZoj5VnkZ4yByS6"

echo "📸 Album URL: $ALBUM_URL"
echo "🆔 Album ID: $ALBUM_ID"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    touch .env
fi

# Add Google Photos configuration to .env if not already present
if ! grep -q "GOOGLE_PHOTOS_ENABLED" .env; then
    echo "" >> .env
    echo "# Google Photos Integration" >> .env
    echo "GOOGLE_PHOTOS_ENABLED=True" >> .env
    echo "GOOGLE_PHOTOS_ALBUM_ID=$ALBUM_ID" >> .env
    echo "GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos" >> .env
    echo "✅ Added Google Photos configuration to .env"
else
    echo "✅ Google Photos configuration already exists in .env"
fi

# Run the database fix command
echo "🔧 Fixing database schema for Google Photos integration..."
python manage.py fix_google_photos --fix-db

echo ""
echo "🎉 Google Photos integration setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Photos will be stored locally and displayed properly on mobile devices"
echo "2. For full Google Photos integration (optional):"
echo "   - Set up Google Cloud Project and enable Photos Library API"
echo "   - Create OAuth 2.0 credentials"
echo "   - Add credentials to google_photos_credentials.json"
echo "3. Restart your application"
echo ""
echo "💡 The treasure hunt photo upload now works better on mobile devices!"
echo "   Photos are optimized for mobile viewing and include click-to-zoom functionality."
