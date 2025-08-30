# Google Cloud Setup for Render Deployment

## Overview
To enable Google Photos upload through your Render deployment, you need to configure Google Cloud Console properly and set up authentication for a production environment.

## Step-by-Step Setup

### 1. Google Cloud Console Configuration

#### A. Create/Select Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your project ID (you'll need this)

#### B. Enable APIs
1. Go to **APIs & Services > Library**
2. Enable these APIs:
   - **Photos Library API** ✅
   - **Google Drive API** (optional, for additional storage)

#### C. Create Service Account (Recommended for Production)
1. Go to **IAM & Admin > Service Accounts**
2. Click **"Create Service Account"**
3. Fill details:
   - **Name**: `onam-photos-service`
   - **Description**: `Service account for Onam app Google Photos integration`
4. Click **"Create and Continue"**
5. **Skip role assignment** (Photos Library API doesn't require special roles)
6. Click **"Done"**

#### D. Generate Service Account Key
1. Click on the created service account
2. Go to **"Keys"** tab
3. Click **"Add Key" > "Create New Key"**
4. Choose **JSON** format
5. Download the JSON file (keep it secure!)

### 2. Render Environment Configuration

#### A. Add Environment Variables in Render
In your Render dashboard, go to your app settings and add these environment variables:

```bash
# Google Photos Configuration
GOOGLE_PHOTOS_ENABLED=true
GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here
GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos

# Service Account Authentication (paste entire JSON content)
GOOGLE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"your-project-id",...}
```

#### B. Alternative: Upload Service Account File
If you prefer using a file instead of environment variable:

1. Add the JSON file to your repository (NOT recommended for security)
2. Or use Render's file upload feature
3. Set environment variable:
   ```bash
   GOOGLE_SERVICE_ACCOUNT_FILE=/opt/render/project/src/service-account.json
   ```

### 3. Create Google Photos Album

#### A. Create Album
1. Go to [Google Photos](https://photos.google.com/)
2. Create a new album: **"Onam Celebration - Treasure Hunt Photos"**
3. Share the album (make it accessible)

#### B. Get Album ID
1. Share the album and copy the share URL
2. The URL looks like: `https://photos.app.goo.gl/ALBUM_ID_HERE`
3. Extract the album ID from the URL
4. Add to Render environment variables:
   ```bash
   GOOGLE_PHOTOS_ALBUM_ID=your_extracted_album_id
   ```

### 4. Service Account Permissions

#### A. Share Album with Service Account
1. In Google Photos, open your album
2. Click **"Share"**
3. Add the service account email as a collaborator:
   ```
   onam-photos-service@your-project-id.iam.gserviceaccount.com
   ```
4. Give **"Can add photos"** permission

### 5. Update Django Settings

#### A. Production Settings
Add to your `onam_project/settings/production.py`:

```python
# Google Photos Integration
GOOGLE_PHOTOS_ENABLED = env.bool('GOOGLE_PHOTOS_ENABLED', default=False)
GOOGLE_PHOTOS_ALBUM_ID = env('GOOGLE_PHOTOS_ALBUM_ID', default=None)
GOOGLE_PHOTOS_ALBUM_NAME = env('GOOGLE_PHOTOS_ALBUM_NAME', default='Onam Celebration')

# Service Account Configuration
GOOGLE_SERVICE_ACCOUNT_KEY = env('GOOGLE_SERVICE_ACCOUNT_KEY', default=None)
GOOGLE_SERVICE_ACCOUNT_FILE = env('GOOGLE_SERVICE_ACCOUNT_FILE', default=None)
```

### 6. Update Google Photos Service

Update your imports to use the production-ready service:

```python
# In apps/core/views.py
try:
    from .google_photos_render import google_photos_service
    GOOGLE_PHOTOS_AVAILABLE = True
except ImportError:
    from .google_photos import google_photos_service
    GOOGLE_PHOTOS_AVAILABLE = False
```

### 7. Testing on Render

#### A. Deploy and Test
1. Deploy your app to Render
2. Check logs for authentication status
3. Test photo upload through the app

#### B. Debug Commands
Add these to check status:

```bash
# In Render console or logs
python manage.py shell

# Test authentication
from apps.core.google_photos_render import google_photos_service
print("Configured:", google_photos_service.is_configured())
print("Auth type:", google_photos_service.auth_type)
service.authenticate()
```

### 8. Security Best Practices

#### A. Environment Variables (Recommended)
- Store service account JSON in `GOOGLE_SERVICE_ACCOUNT_KEY` environment variable
- Never commit credentials to repository
- Use Render's encrypted environment variables

#### B. Service Account Permissions
- Use dedicated service account for this app only
- Don't give unnecessary permissions
- Regularly rotate service account keys

#### C. Album Security
- Make album private or limited sharing
- Only share with necessary service accounts
- Monitor album access logs

### 9. Troubleshooting

#### Common Issues:

**Authentication Fails**
- Check service account JSON is valid
- Verify environment variable is set correctly
- Ensure APIs are enabled in Google Cloud Console

**Album Access Denied**
- Verify album is shared with service account email
- Check album ID is correct
- Ensure service account has "Can add photos" permission

**Upload Fails**
- Check Photos Library API quotas
- Verify file format is supported (JPEG/PNG)
- Check Render logs for detailed error messages

#### Debug Commands:
```python
# Check configuration
python manage.py enable_google_photos --status

# Test upload
python manage.py enable_google_photos --test
```

### 10. Production Deployment Checklist

- [ ] Google Cloud project created
- [ ] Photos Library API enabled
- [ ] Service account created with JSON key
- [ ] Google Photos album created and shared
- [ ] Album ID extracted and configured
- [ ] Service account key added to Render environment
- [ ] Production settings updated
- [ ] App deployed to Render
- [ ] Photo upload tested in production

## Environment Variables Summary

```bash
# Required for Google Photos on Render
GOOGLE_PHOTOS_ENABLED=true
GOOGLE_PHOTOS_ALBUM_ID=ABcdEf1234567890
GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos

# Service Account Authentication (choose one)
GOOGLE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}
# OR
GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
```

This setup will enable real Google Photos uploads through your Render deployment!
