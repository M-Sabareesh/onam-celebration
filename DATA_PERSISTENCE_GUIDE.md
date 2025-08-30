# 🗄️ Data Persistence Solution for Render Free Tier

## Problem
Render's free tier databases are ephemeral - they get wiped when your app goes to sleep. This means you lose all your treasure hunt questions, events, and player data.

## Solution
We've implemented a GitHub-based backup and restore system that automatically preserves your data.

## 🚀 Quick Setup Guide

### Step 1: Create Local Backup
Run this command locally (where you have your data):
```bash
python manage.py backup_data --output-dir=data_backup
```

### Step 2: Create GitHub Repository
1. Go to GitHub and create a new **public** repository
2. Name it: `onam-celebration-data`
3. Upload the `data_backup/` folder to this repository

### Step 3: Configure Render
Add this environment variable in your Render dashboard:
```
GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/YOUR_USERNAME/onam-celebration-data/main/data_backup/
```

### Step 4: Update Build Command
In Render, set your build command to:
```bash
./start.sh
```

## ✅ What Gets Backed Up

### Always Backed Up (Structure):
- ✅ Treasure Hunt Questions
- ✅ Events and Event Types
- ✅ Admin Configuration

### Optionally Backed Up (Data):
- 📝 Player Records
- 📝 Player Answers
- 📝 Event Votes
- 📝 Event Scores

## 🔄 How It Works

### Backup Process:
1. Run `python manage.py backup_data` locally
2. Upload JSON files to GitHub
3. GitHub serves as your persistent storage

### Restore Process (Automatic):
1. App starts on Render
2. Checks if database is empty
3. Downloads data from GitHub
4. Restores questions and events
5. App is ready with your content!

## 📋 Management Commands

### Backup Data
```bash
# Backup structure only (recommended)
python manage.py backup_data

# Backup everything including player data
python manage.py backup_data --include-players

# Custom output directory
python manage.py backup_data --output-dir=my_backup
```

### Restore Data
```bash
# Restore from environment variable URL
python manage.py restore_data

# Restore with custom URL
python manage.py restore_data --github-base-url=https://raw.githubusercontent.com/user/repo/main/data_backup/

# Force restore (overwrite existing)
python manage.py restore_data --force

# Restore only questions and events
python manage.py restore_data --structure-only
```

## 🎯 Recommended Workflow

### For Development:
1. Add new questions/events locally
2. Run backup command
3. Push to GitHub
4. Deploy to Render

### For Production:
1. Questions and events restore automatically
2. Players re-register when they visit
3. Fresh start with preserved structure

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Required: Base URL for your GitHub backup files
GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/username/repo/main/data_backup/

# Optional: Auto-restore on startup (default: True)
AUTO_RESTORE_DATA=True

# Optional: Admin user password
ADMIN_PASSWORD=your_secure_password
```

### File Structure in GitHub
```
data_backup/
├── questions.json          # Treasure hunt questions
├── events.json            # Events and competitions
├── backup_info.json       # Backup metadata
└── players_20240825.json  # Optional: Player data
```

## 🚨 Important Notes

### Free Tier Limitations:
- Database resets when app sleeps (every ~30 minutes of inactivity)
- GitHub repository must be public for free raw file access
- Questions/events restore automatically
- Players need to re-register after each reset

### Security Considerations:
- Don't store sensitive data in public GitHub repos
- Player data is regenerated (users re-register)
- Admin credentials are set via environment variables

### Performance:
- Restore takes ~10-30 seconds on startup
- Only happens when database is empty
- Cached for subsequent requests

## 🐛 Troubleshooting

### If Restore Fails:
1. Check GitHub URL is correct and public
2. Verify JSON files are valid
3. Check Render logs for specific errors
4. Fallback: Default questions will be created

### Manual Recovery:
```bash
# Create default questions if restore fails
python manage.py populate_questions

# Check what's in database
python manage.py shell -c "from apps.core.models import TreasureHuntQuestion; print(f'Questions: {TreasureHuntQuestion.objects.count()}')"
```

## 💡 Pro Tips

1. **Keep GitHub Updated**: Regularly backup new questions/events
2. **Monitor Logs**: Check Render logs to ensure restore works
3. **Test Locally**: Use restore command locally to test your backup
4. **Version Control**: Use dated backups for different versions
5. **Hybrid Approach**: Store structure in GitHub, let users recreate accounts

## 🎉 Benefits

✅ **Persistent Structure**: Questions and events survive database resets  
✅ **Zero Downtime**: Automatic restore on startup  
✅ **Version Control**: GitHub provides backup history  
✅ **Free Solution**: No additional costs  
✅ **Easy Updates**: Update GitHub to deploy new content  
✅ **Portable**: Move between hosting providers easily

This solution ensures your Onam Celebration app maintains its core functionality even with Render's free tier limitations!
