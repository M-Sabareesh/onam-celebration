# Google Photos Integration for Onam Celebration - Treasure Hunt

This implementation provides enhanced mobile photo visibility for treasure hunt answers by integrating with Google Photos. Photos are optimized for mobile viewing and can be backed up to a Google Photos album.

## Quick Fix for Current Issue

The database error you're seeing is because the new Google Photos fields need to be added to the database. Run this command to fix it immediately:

```bash
# Linux/Mac
python manage.py fix_google_photos --fix-db

# Or use the setup script
chmod +x setup_google_photos.sh
./setup_google_photos.sh

# Windows
python manage.py fix_google_photos --fix-db

# Or use the batch file
setup_google_photos.bat
```

## Features Implemented

### 1. Enhanced Mobile Photo Display
- **Responsive Images**: Photos are automatically resized for mobile devices
- **Click-to-Zoom**: Users can tap photos to view them in full-screen modal
- **Loading States**: Shows loading animation while photos load
- **Error Handling**: Graceful fallback if photos fail to load
- **Mobile-Optimized UI**: Better spacing and sizing for mobile screens

### 2. Google Photos Integration (Optional)
- **Automatic Backup**: Photos uploaded to treasure hunt are backed up to Google Photos
- **Album Organization**: All photos go to a specific album: https://photos.app.goo.gl/sDnZoj5VnkZ4yByS6
- **Dual Storage**: Photos stored locally AND in Google Photos for redundancy
- **Google Photos URLs**: Mobile-optimized URLs with size parameters for faster loading

### 3. Database Schema Updates
Added new fields to `PlayerAnswer` model:
- `google_photos_media_id`: Store Google Photos media item ID
- `google_photos_url`: Direct Google Photos URL for display
- `google_photos_product_url`: Link to view in Google Photos app

## Mobile Optimizations

### Photo Display Improvements
```html
<!-- Before: Basic thumbnail -->
<img src="{{ answer.photo_answer.url }}" class="img-thumbnail" style="max-width: 200px;">

<!-- After: Mobile-optimized with Google Photos -->
<img src="{{ answer.google_photos_url }}=w400-h300" 
     class="img-thumbnail mobile-optimized-photo" 
     onclick="openPhotoModal('{{ answer.google_photos_url }}=w800-h600', '{{ player.name }}', '{{ question.order }}')">
```

### Responsive Breakpoints
- **Desktop**: Full-size photos with hover effects
- **Tablet**: Medium-sized photos with touch-friendly interface
- **Mobile**: Compressed photos optimized for mobile networks

### Performance Features
- **Lazy Loading**: Photos load only when needed
- **Size Optimization**: Different photo sizes for different screen sizes
- **Caching**: Google Photos URLs include size parameters for CDN caching

## Configuration

### Environment Variables
```bash
# Enable Google Photos integration
GOOGLE_PHOTOS_ENABLED=True

# Album ID from your Google Photos album URL
GOOGLE_PHOTOS_ALBUM_ID=sDnZoj5VnkZ4yByS6

# Optional: Custom album name
GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos
```

### For Render Deployment
Add these environment variables in your Render dashboard:
1. Go to your service settings
2. Add environment variables:
   - `GOOGLE_PHOTOS_ENABLED=True`
   - `GOOGLE_PHOTOS_ALBUM_ID=sDnZoj5VnkZ4yByS6`

## Google Photos API Setup (Optional)

For full integration with automatic uploads to Google Photos:

### 1. Google Cloud Setup
```bash
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "Photos Library API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure consent screen if needed
6. Add authorized redirect URIs: http://localhost:8080/callback
7. Download credentials JSON file
```

### 2. Credentials File
Save the downloaded file as `google_photos_credentials.json` in your project root:
```json
{
  "web": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost:8080/callback"]
  }
}
```

### 3. Authentication Flow
```bash
# Run the setup command to authenticate
python manage.py setup_google_photos --setup-credentials

# This will guide you through the OAuth flow
```

## Immediate Solution (No Google API Required)

The integration works without Google API credentials:

1. **Photos stored locally**: All photos continue to work as before
2. **Mobile optimization**: Enhanced display and interaction on mobile devices
3. **Manual album management**: You can manually add photos to the Google Photos album
4. **Progressive enhancement**: Add Google API later if needed

## File Structure

```
apps/core/
├── google_photos.py              # Google Photos API service
├── management/commands/
│   ├── fix_google_photos.py      # Database fix command
│   └── setup_google_photos.py    # Setup command
├── migrations/
│   └── 0002_add_google_photos_fields.py  # Database migration
├── models.py                     # Updated PlayerAnswer model
└── views.py                      # Updated TreasureHuntView

templates/core/
└── treasure_hunt.html            # Enhanced mobile UI

setup_google_photos.sh            # Unix setup script  
setup_google_photos.bat           # Windows setup script
```

## Mobile UI Features

### Photo Modal
- Full-screen photo viewing
- Swipe-friendly interface
- Bootstrap modal with mobile optimizations
- Player and question information overlay

### Touch-Friendly Interface
- Larger tap targets for mobile
- Responsive button sizing
- Optimized form layouts
- Mobile-first design approach

### Loading States
- Photo upload progress indicators
- Loading animations for photo display
- Error handling with user-friendly messages
- Progressive image loading

## Testing

### Mobile Testing
1. Test photo upload on various mobile devices
2. Verify photos display correctly in different orientations
3. Test modal functionality on touch devices
4. Verify responsive breakpoints

### Photo Quality Testing
```bash
# Test different image sizes and formats
curl -X POST -F "photo_answer=@test_large.jpg" /treasure-hunt/
curl -X POST -F "photo_answer=@test_mobile.jpg" /treasure-hunt/
```

## Troubleshooting

### Database Issues
```bash
# If you see "column does not exist" errors:
python manage.py fix_google_photos --fix-db

# Force migration
python manage.py migrate --fake-initial
```

### Photo Display Issues
```bash
# Check media settings
python manage.py collectstatic
python manage.py check --deploy

# Verify file permissions
ls -la media/treasure_hunt_photos/
```

### Mobile Performance
- Ensure photos are compressed before upload
- Check network connectivity on mobile devices
- Verify CDN configuration for static files

## Future Enhancements

1. **Automatic Photo Compression**: Compress photos before upload
2. **Progressive Web App**: Add PWA features for better mobile experience
3. **Offline Support**: Cache photos for offline viewing
4. **Push Notifications**: Notify when photos are uploaded to album
5. **Social Sharing**: Direct sharing to social media platforms

## Support

For issues or questions:
1. Check the treasure hunt page for photo display
2. Verify database schema with the fix command
3. Test mobile responsiveness on different devices
4. Review Google Photos album for manual verification

The solution provides immediate mobile improvements without requiring Google API setup, with the option to add full integration later.
