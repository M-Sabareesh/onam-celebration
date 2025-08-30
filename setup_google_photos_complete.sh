#!/bin/bash

echo "🔗 Google Photos Integration Setup for Onam App"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Checking current setup...${NC}"

# Check if Python environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅ Virtual environment is active: $VIRTUAL_ENV${NC}"
else
    echo -e "${YELLOW}⚠️  No virtual environment detected${NC}"
    echo "Consider activating your virtual environment first"
fi

# Check Django
if command_exists python && python -c "import django" 2>/dev/null; then
    echo -e "${GREEN}✅ Django is available${NC}"
else
    echo -e "${RED}❌ Django not found${NC}"
    exit 1
fi

# Check Google Photos API packages
echo -e "\n${BLUE}Step 2: Checking Google Photos API dependencies...${NC}"

MISSING_PACKAGES=""

if ! python -c "import google.auth" 2>/dev/null; then
    MISSING_PACKAGES="$MISSING_PACKAGES google-auth"
fi

if ! python -c "import google_auth_oauthlib" 2>/dev/null; then
    MISSING_PACKAGES="$MISSING_PACKAGES google-auth-oauthlib"
fi

if ! python -c "import googleapiclient" 2>/dev/null; then
    MISSING_PACKAGES="$MISSING_PACKAGES google-api-python-client"
fi

if [[ -n "$MISSING_PACKAGES" ]]; then
    echo -e "${YELLOW}⚠️  Missing packages: $MISSING_PACKAGES${NC}"
    echo "Installing missing packages..."
    pip install $MISSING_PACKAGES
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ Packages installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install packages${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ All Google Photos API packages are available${NC}"
fi

echo -e "\n${BLUE}Step 3: Checking Google Photos integration status...${NC}"

# Run Django management command to check status
python manage.py enable_google_photos --status

echo -e "\n${BLUE}Step 4: Setting up environment variables...${NC}"

# Create or update .env file
if [[ ! -f .env ]]; then
    echo "Creating .env file..."
    touch .env
fi

# Check if Google Photos settings exist
if ! grep -q "GOOGLE_PHOTOS_ENABLED" .env; then
    echo "GOOGLE_PHOTOS_ENABLED=True" >> .env
    echo -e "${GREEN}✅ Added GOOGLE_PHOTOS_ENABLED=True to .env${NC}"
fi

if ! grep -q "GOOGLE_PHOTOS_ALBUM_ID" .env; then
    echo "GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here" >> .env
    echo -e "${YELLOW}⚠️  Added placeholder GOOGLE_PHOTOS_ALBUM_ID to .env - update with your actual album ID${NC}"
fi

echo -e "\n${BLUE}Step 5: Setup instructions...${NC}"

echo -e "${YELLOW}📝 To complete Google Photos integration:${NC}"
echo ""
echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
echo "2. Create a new project or select existing one"
echo "3. Enable the 'Photos Library API'"
echo "4. Go to 'Credentials' and create 'OAuth 2.0 Client ID'"
echo "5. Choose 'Desktop application' as application type"
echo "6. Download the JSON credentials file"
echo "7. Save it as 'google_photos_credentials.json' in your project root"
echo "8. Create a Google Photos album and get its ID from the share URL"
echo "9. Update GOOGLE_PHOTOS_ALBUM_ID in your .env file"
echo ""

echo -e "${BLUE}Step 6: Testing setup...${NC}"

# Test media serving
if [[ -d "media/treasure_hunt_photos" ]]; then
    PHOTO_COUNT=$(find media/treasure_hunt_photos -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | wc -l)
    echo -e "${GREEN}✅ Found $PHOTO_COUNT photos in media directory${NC}"
else
    echo -e "${YELLOW}⚠️  Media directory not found, creating...${NC}"
    mkdir -p media/treasure_hunt_photos
    mkdir -p media/question_images
    mkdir -p media/avatars
fi

# Run media diagnostics
if [[ -f "test_media_fix.py" ]]; then
    echo "Running media diagnostics..."
    python test_media_fix.py
fi

echo -e "\n${BLUE}Step 7: Quick setup verification...${NC}"

# Test Django command
python manage.py enable_google_photos --status

echo -e "\n${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Place your Google Photos credentials file in the project root"
echo "2. Update the GOOGLE_PHOTOS_ALBUM_ID in .env"
echo "3. Run: python manage.py enable_google_photos --test"
echo "4. Start your Django server: python manage.py runserver"
echo ""
echo -e "${BLUE}For troubleshooting, check the logs in Django admin or console output.${NC}"
