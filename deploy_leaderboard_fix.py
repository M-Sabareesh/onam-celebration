#!/usr/bin/env python
"""
Emergency Leaderboard Fix Deployment Script
This script provides immediate fixes for the leaderboard database issues.
"""

import os
import subprocess
import sys

def deploy_leaderboard_fix():
    """Deploy the leaderboard fix"""
    print("🚨 Deploying Emergency Leaderboard Fix...")
    
    # List of commands to run
    commands = [
        "git add apps/core/views.py",
        "git commit -m 'Emergency fix: Add robust error handling for missing IndividualEventScore table'",
        "git push origin main"
    ]
    
    print("\n📦 Committing and pushing the fix...")
    
    for cmd in commands:
        try:
            print(f"Running: {cmd}")
            result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
            print(f"✅ Success: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning for '{cmd}': {e}")
            if e.stderr:
                print(f"Error: {e.stderr}")
    
    print("\n🚀 Fix deployed! Render will automatically redeploy.")
    print("⏱️ Wait 2-3 minutes for the deployment to complete.")

def create_manual_migration_guide():
    """Create a guide for manual migration"""
    guide = """
# 🚨 Manual Database Migration Guide

## If the leaderboard is still failing, run these commands on Render:

### 1. Access Render Shell
Go to your Render dashboard > Your service > Shell

### 2. Run Migrations
```bash
python manage.py migrate core 0010
python manage.py migrate core 0011  
python manage.py migrate core 0012
python manage.py migrate
```

### 3. Restart Service
Restart your Render service after migrations.

## Alternative: Emergency SQL Commands
If migrations fail, run these SQL commands directly:

```sql
-- Add missing Event table columns
ALTER TABLE core_event ADD COLUMN IF NOT EXISTS participation_type VARCHAR(20) DEFAULT 'team';
ALTER TABLE core_event ADD COLUMN IF NOT EXISTS individual_points_multiplier DECIMAL(5,2) DEFAULT 1.0;

-- Add missing EventScore table columns  
ALTER TABLE core_eventscore ADD COLUMN IF NOT EXISTS points_per_participant DECIMAL(5,2) DEFAULT 0;
ALTER TABLE core_eventscore ADD COLUMN IF NOT EXISTS auto_calculate_points BOOLEAN DEFAULT FALSE;

-- Create IndividualEventScore table
CREATE TABLE IF NOT EXISTS core_individualeventscore (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES core_event(id),
    player_id BIGINT NOT NULL REFERENCES core_player(id),
    points DECIMAL(5,2) DEFAULT 0,
    team_points DECIMAL(5,2) DEFAULT 0,
    notes TEXT DEFAULT '',
    awarded_by VARCHAR(100) DEFAULT '',
    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(event_id, player_id)
);

-- Create TeamEventParticipation table
CREATE TABLE IF NOT EXISTS core_teameventparticipation (
    id BIGSERIAL PRIMARY KEY,
    event_score_id BIGINT NOT NULL REFERENCES core_eventscore(id),
    player_id BIGINT NOT NULL REFERENCES core_player(id),
    participated BOOLEAN DEFAULT FALSE,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(event_score_id, player_id)
);
```

## Expected Result
- ✅ Leaderboard loads without errors
- ✅ Team participation system works
- ✅ Individual scoring available
- ✅ Auto-calculation: participants × points_per_participant
"""
    
    with open('EMERGENCY_MIGRATION_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("📝 Created EMERGENCY_MIGRATION_GUIDE.md")

def main():
    """Main function"""
    print("🔧 Emergency Leaderboard Fix Deployment")
    print("=" * 50)
    
    # Deploy the fix
    deploy_leaderboard_fix()
    
    # Create migration guide
    create_manual_migration_guide()
    
    print("\n✅ Emergency fixes applied!")
    print("\n📋 Next steps:")
    print("1. Wait for Render deployment (2-3 minutes)")
    print("2. Test leaderboard: https://onam-celebration.onrender.com/leaderboard/")
    print("3. If still failing, use EMERGENCY_MIGRATION_GUIDE.md")
    print("\n🎉 Your website should be fully functional soon!")

if __name__ == '__main__':
    main()
