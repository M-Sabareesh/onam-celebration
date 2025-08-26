# 🖼️ Maveli Images Setup Guide

## Problem
Your Maveli images are in `media/Maveli/` but the templates expect them in `static/images/` for production static file serving.

## Solution Options

### Option 1: Quick Copy (Windows)
Run the batch script I created:
```cmd
copy_maveli_images.bat
```

### Option 2: Manual Copy (Windows)
```cmd
# Create the directory
mkdir static\images

# Copy the images
copy "media\Maveli\*.jpg" "static\images\"
copy "media\Maveli\*.png" "static\images\"
```

### Option 3: Manual Copy (Linux/Mac)
```bash
# Create the directory
mkdir -p static/images

# Copy the images
cp media/Maveli/*.jpg static/images/
cp media/Maveli/*.png static/images/
```

### Option 4: Python Script
```python
# Run the Python copy script
python copy_images.py
```

## After Copying Images

### 1. Verify the Copy
Check that you now have:
```
static/images/
├── Maveli.jpg
├── Maveli2.jpg
├── Maveli2.png
└── Maveli4.jpg
```

### 2. Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Test Locally
```bash
python manage.py runserver
```
Visit http://localhost:8000 and check if the Maveli image loads on the homepage.

### 4. Deploy to Production
Your `deploy.sh` script now automatically:
- Copies Maveli images from media to static
- Runs collectstatic
- Sets up everything for production

## Template Update

I've updated `templates/core/index.html` to:
- ✅ **Try to load the real Maveli.jpg image first**
- ✅ **Fall back to the emoji design if image fails**
- ✅ **Provide graceful error handling**

## Current Status

### What's Fixed:
- ✅ Template now tries to load real Maveli image
- ✅ Graceful fallback to emoji if image missing
- ✅ Copy scripts created for local development
- ✅ Deploy script updated for production
- ✅ Error handling in place

### What You Need to Do:
1. **Copy the images** using one of the methods above
2. **Run collectstatic** to include them in production files
3. **Deploy** and enjoy your real Maveli images!

## Expected Result

After setup:
- 🖼️ **Homepage shows real Maveli image** (if copy successful)
- 🤴🏾 **Falls back to emoji** (if image missing)
- ✅ **No more static file errors**
- 🎉 **Beautiful Malayalam-branded website**

## Troubleshooting

### If images still don't show:
1. Check `static/images/` contains the files
2. Run `python manage.py collectstatic --clear`
3. Check browser console for any errors
4. Verify the emoji fallback is working

### If you prefer just the emoji:
The current template will automatically show the emoji if the image fails to load, so you don't need to do anything!

Your team event participation system is ready to use either way! 🎊
