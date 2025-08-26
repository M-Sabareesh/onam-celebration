# ഓണാഘോഷം (Onam Celebration) 🌟

A beautiful Django-based Onam celebration website with Malayalam branding, Maveli imagery, dramatic leaderboard reveals, and comprehensive event scoring systems.

## ✨ Features

🎨 **Malayalam Branding:** Site title displays "ഓണാഘോഷം" with Noto Sans Malayalam font  
🖼️ **Maveli Images:** Traditional Maveli imagery throughout the site  
🏆 **Dramatic Leaderboard:** Animated score reveals with confetti and podiums  
👥 **Team & Individual Events:** Support for both team and individual event scoring  
📊 **Auto Point Calculation:** Points calculated based on participant count  
🎯 **Comprehensive Admin:** Easy event management and score tracking  
📱 **Responsive Design:** Works beautifully on all devices  

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

## 🚨 Production Issue Fix

If you see the error: `relation "core_individualeventscore" does not exist`

**Quick Fix:**
```bash
# Windows
fix_production_migrations.bat

# Linux/Mac  
./fix_production_migrations.sh

# Manual
python manage.py migrate core 0010
python manage.py migrate core 0011
python manage.py migrate core 0012
```

See `PRODUCTION_FIX_README.md` for detailed instructions.

## 📋 Event Types

1. **Individual Events:** Players compete individually, scores contribute to team totals
2. **Team Events:** Entire teams participate, can select specific participants  
3. **Hybrid Events:** Mix of individual and team participation

## 🎯 Admin Features

- **Event Management:** Create and configure different event types
- **Individual Scoring:** Score individual participants with point calculations
- **Team Participation:** Select which team members participate in team events
- **Live Calculations:** See point previews as you make scoring decisions
- **Bulk Operations:** Select all/deselect all participant checkboxes

## 🌟 Visual Elements

- **Maveli Images:** Traditional Kerala King Maveli throughout the site
- **Malayalam Typography:** Authentic Malayalam fonts and text
- **Animated Leaderboard:** Dramatic reveals with CSS animations
- **Confetti Effects:** Celebration animations for winners
- **Responsive Design:** Beautiful on mobile and desktop

## 📁 Project Structure

```
onam-celebration/
├── apps/
│   ├── core/          # Main app with events, players, scoring
│   ├── accounts/      # User authentication  
│   └── games/         # Game-specific functionality
├── static/
│   ├── images/        # Maveli images and other assets
│   ├── css/          # Styling with Malayalam fonts
│   └── js/           # Admin enhancements and animations
├── templates/         # HTML templates with Malayalam branding
└── media/            # User uploaded content
```

## 🛠️ Development Scripts

- `create_sample_events.py` - Generate sample event data
- `team_event_participation_demo.py` - Demo team participation features  
- `copy_maveli_images.py` - Copy Maveli images to static folder
- `verify_maveli_setup.py` - Verify image setup is correct

## 📚 Documentation

- `INDIVIDUAL_EVENT_SCORING_GUIDE.md` - Individual event scoring system
- `TEAM_EVENT_PARTICIPATION_GUIDE.md` - Team participation features
- `LEADERBOARD_REVEAL_SYSTEM.md` - Dramatic leaderboard animations
- `MAVELI_IMAGES_SETUP.md` - Maveli image configuration
- `PRODUCTION_MIGRATION_FIX_GUIDE.md` - Database migration troubleshooting

## 🎊 Deployment

The site is designed for easy deployment on platforms like Render, Heroku, or any Django-compatible hosting service. All static files and database migrations are properly configured.

## 📸 Screenshots

Visit the live site to see:
- Beautiful Malayalam "ഓണാഘོഷം" branding
- Traditional Maveli images
- Animated leaderboard with team rankings
- Comprehensive admin interface for event management

## 🤝 Contributing

This is a personal Onam celebration project. Feel free to fork and adapt for your own celebrations!

---

**Happy Onam! ഓണാസംസകൾ!** 🌸✨
