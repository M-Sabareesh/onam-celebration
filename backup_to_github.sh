#!/bin/bash
"""
MANUAL BACKUP SCRIPT - Run this locally when you want to backup data
"""

echo "🗄️  Creating backup of Onam Celebration data..."

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
fi

# Create backup
echo "📋 Running backup command..."
python manage.py backup_data --output-dir=data_backup

if [ $? -eq 0 ]; then
    echo "✅ Backup created successfully!"
    echo ""
    echo "📁 Files created in data_backup/ folder:"
    ls -la data_backup/
    echo ""
else
    echo "❌ Backup failed!"
    exit 1
fi

# Check if git is available and we're in a git repo
if command -v git &> /dev/null && [ -d ".git" ]; then
    echo "🔄 Auto-committing backup files..."
    
    # Add backup files to git
    git add data_backup/
    git commit -m "🔄 Backup data - $(date)"
    
    echo "✅ Backup committed to git"
    echo "💡 Remember to push to GitHub: git push"
else
    echo "ℹ️  Not in a git repository. Manual upload required."
fi

echo ""
echo "🌐 NEXT STEPS:"
echo "=============="
echo ""
echo "📤 UPLOAD TO GITHUB:"
echo "1. Go to your onam-celebration-data repository"
echo "2. Upload the data_backup/ folder contents"
echo "3. Or push this repository if you committed the files"
echo ""
echo "🔗 GITHUB DATA REPO STRUCTURE:"
echo "onam-celebration-data/"
echo "└── data_backup/"
echo "    ├── questions.json"
echo "    ├── events.json"
echo "    └── backup_info.json"
echo ""
echo "⚙️  RENDER ENVIRONMENT VARIABLE:"
echo "GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/YOUR_USERNAME/onam-celebration-data/main/data_backup/"
echo ""
echo "🎉 After setup, your Render app will auto-restore data on startup!"
