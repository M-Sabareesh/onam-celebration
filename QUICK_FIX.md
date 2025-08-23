# QUICK FIX: Event Models Migration Issue

## 🚨 Problem Identified
The error "no such table: core_event" indicates that the database migrations for the new Event models haven't been applied yet.

## ✅ SOLUTION - Follow These Steps:

### Step 1: Apply Migrations
```bash
cd /mnt/c/Users/SMADAMBA/OneDrive\ -\ Volvo\ Cars/Documents/Testing/Onam2
python manage.py migrate
```

### Step 2: If Migration Fails, Force It
```bash
python manage.py migrate core 0008 --fake
python manage.py migrate
```

### Step 3: Create Sample Events
```bash
python create_sample_events.py
```

### Step 4: Start Server
```bash
python manage.py runserver
```

### Step 5: Test Events Page
Visit: http://127.0.0.1:8000/events/

## 🔧 Alternative Fix (If Migrations Still Fail)

If the automatic migration doesn't work, you can manually create the tables using SQLite:

```bash
# Open SQLite database (install sqlite3 first if needed)
sudo apt install sqlite3
sqlite3 db.sqlite3

# Create Event table
CREATE TABLE IF NOT EXISTS core_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    voting_enabled BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);

# Create EventParticipation table
CREATE TABLE IF NOT EXISTS core_eventparticipation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    team VARCHAR(20) NOT NULL,
    registered_at DATETIME NOT NULL,
    FOREIGN KEY (event_id) REFERENCES core_event (id),
    UNIQUE(event_id, team)
);

# Create EventVote table
CREATE TABLE IF NOT EXISTS core_eventvote (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    voting_team VARCHAR(20) NOT NULL,
    performing_team VARCHAR(20) NOT NULL,
    coordination_score INTEGER NOT NULL,
    selection_score INTEGER NOT NULL,
    overall_score INTEGER NOT NULL,
    enjoyment_score INTEGER NOT NULL,
    comments TEXT,
    voted_at DATETIME NOT NULL,
    FOREIGN KEY (event_id) REFERENCES core_event (id),
    UNIQUE(event_id, voting_team, performing_team)
);

# Exit SQLite
.quit
```

Then mark the migration as applied:
```bash
python manage.py migrate core 0008 --fake
```

## 📋 Verification Steps

1. **Check Migration Status**:
   ```bash
   python manage.py showmigrations core
   ```

2. **Test Model Import**:
   ```bash
   python -c "
   import os, django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
   django.setup()
   from apps.core.models import Event
   print('Event model works!')
   print(f'Events count: {Event.objects.count()}')
   "
   ```

## 🎯 What Should Happen After Fix

1. **Events page loads** at `/events/`
2. **Admin interface shows** Event, EventParticipation, EventVote models  
3. **Sample events can be created** using the script
4. **Voting system works** for team competitions

## 📁 Files Already Created

✅ **Models**: Event, EventParticipation, EventVote in `models.py`
✅ **Admin**: Event management in `admin.py` 
✅ **Views**: EventsListView, EventDetailView in `views.py`
✅ **Templates**: events_list.html, event_detail.html
✅ **URLs**: /events/ routes in `urls.py`
✅ **Migration**: 0008_event_eventvote_eventparticipation.py

The events and voting system is **100% complete** - we just need to get the database tables created!
sudo apt update
sudo apt install python3-venv python3-full

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Now install packages safely
pip install --upgrade pip
pip install -r requirements.txt

# Continue with Django setup
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Option 2: Use the Updated Quickstart Script
```bash
# The quickstart.py script has been updated to handle this automatically
python3 quickstart.py
```

### Option 3: Use Docker (No Python environment issues)
```bash
# Build and run with Docker
docker-compose up --build

# Access the app at http://localhost:8000
```

### Option 4: Use pipx (For application installation)
```bash
# Install pipx if not available
sudo apt install pipx

# This won't work for development but good to know
pipx install django
```

## 🔧 What the Error Means
- **PEP 668**: Python packaging standard that prevents breaking system packages
- **Externally Managed**: Your system Python is managed by apt/package manager
- **Solution**: Always use virtual environments for Python projects

## 🎯 Recommended Workflow
```bash
# 1. Always create virtual environment first
python3 -m venv venv

# 2. Always activate before working
source venv/bin/activate

# 3. Install packages in the virtual environment
pip install -r requirements.txt

# 4. When done, deactivate
deactivate
```

## ⚠️ Never Do This (Unless You Know What You're Doing)
```bash
# DON'T: This breaks system packages
pip install --break-system-packages django

# DON'T: This can mess up your system
sudo pip install django
```

## 🌸 Quick Start Command Sequence
```bash
# Copy and paste these commands in order:
sudo apt update && sudo apt install -y python3-venv python3-full
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 🎉 After Setup
- Access your Onam app: http://localhost:8000
- Admin panel: http://localhost:8000/admin/
- Remember to activate `venv` each time you work on the project

**Happy Coding! ഓണാശംസകൾ! 🌸**
