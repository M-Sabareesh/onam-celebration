# Complete Image Loading and Google Photos Fix Guide

## Issues Fixed
1. ✅ Media file serving configuration
2. ✅ Google Photos API integration setup
3. ✅ Environment variables configuration
4. ✅ Directory structure creation

## Image Loading Fix

### 1. Media URL Configuration
- Media serving is configured in `onam_project/urls.py`
- DEBUG=True enables automatic media serving in development
- In production, ensure web server serves media files

### 2. File Structure
```
media/
├── question_images/
│   ├── .gitkeep
│   └── Onma5.jpg
├── treasure_hunt_photos/
│   ├── .gitkeep
│   └── [uploaded photos]
└── avatars/
    └── .gitkeep
```

### 3. URL Access
- Images accessible at: `http://localhost:8000/media/question_images/filename.jpg`
- Template usage: `{{ question.question_image.url }}`

## Google Photos Integration

### 1. Google Cloud Console Setup
1. Go to: https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "Photos Library API"
4. Create OAuth 2.0 Client ID credentials
5. Choose "Desktop application"
6. Download JSON credentials file
7. Save as `google_photos_credentials.json` in project root

### 2. Environment Configuration
Update `.env` file:
```
GOOGLE_PHOTOS_ENABLED=True
GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here
GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos
```

### 3. Get Album ID
1. Create a Google Photos album
2. Share the album and copy the share URL
3. Extract the album ID from the URL
4. Update `GOOGLE_PHOTOS_ALBUM_ID` in `.env`

### 4. Testing
```bash
# Check status
python manage.py enable_google_photos --status

# Test upload (requires credentials)
python manage.py enable_google_photos --test
```

## Troubleshooting

### Image Not Loading
1. Check file exists in media directory
2. Verify URL path matches file location
3. Ensure DEBUG=True in development
4. Check browser console for 404 errors

### Google Photos Upload Fails
1. Verify credentials file exists and is valid
2. Check album ID is correct
3. Ensure API is enabled in Google Cloud Console
4. Check Django logs for error messages

## Production Deployment

### Media Files
- Configure web server (nginx/Apache) to serve media files
- Set `MEDIA_ROOT` and `MEDIA_URL` correctly
- Ensure file permissions are correct

### Google Photos
- Store credentials securely (not in version control)
- Use environment variables for sensitive data
- Consider using service account for server-to-server auth

## Testing Commands

```bash
# Start development server
python manage.py runserver

# Test image access
curl http://localhost:8000/media/question_images/Onma5.jpg

# Check Google Photos status  
python manage.py enable_google_photos --status

# Run media diagnostics
python quick_diagnostics.py
```

## Next Steps
1. ✅ Start Django development server
2. ✅ Test image loading in browser
3. ⏳ Get Google Cloud Console credentials
4. ⏳ Update album ID in .env
5. ⏳ Test Google Photos upload functionality
