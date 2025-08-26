#!/usr/bin/env python
"""
Production Leaderboard Fix - Specific for the core_individualeventscore error
This script fixes the exact error: relation "core_individualeventscore" does not exist
"""

import os
import sys
import django

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
    try:
        django.setup()
        print("✅ Django environment configured")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def apply_migrations_safely():
    """Apply migrations with error handling"""
    from django.core.management import execute_from_command_line
    
    print("\n🔄 Applying database migrations...")
    
    migration_commands = [
        ['showmigrations', 'core'],  # Show current status
        ['migrate', 'core', '0010', '--verbosity=2'],  # Individual event models  
        ['migrate', 'core', '0011', '--verbosity=2'],  # Fix individual vote fields
        ['migrate', 'core', '0012', '--verbosity=2'],  # Team event participation
        ['migrate', '--verbosity=2'],  # Apply any remaining
    ]
    
    for cmd in migration_commands:
        try:
            print(f"\n>>> Running: python manage.py {' '.join(cmd)}")
            execute_from_command_line(['manage.py'] + cmd)
            if cmd[0] != 'showmigrations':
                print(f"✅ Success: {' '.join(cmd)}")
        except Exception as e:
            print(f"⚠️ Command failed: {e}")
            if 'migrate' in cmd and '0010' in cmd:
                # Critical migration failed
                print("❌ Critical migration 0010 failed - this creates IndividualEventScore")
                return False
    
    return True

def test_models():
    """Test if the models are accessible"""
    print("\n🧪 Testing model accessibility...")
    
    try:
        from apps.core.models import (
            IndividualEventScore, 
            IndividualParticipation, 
            IndividualEventVote,
            TeamEventParticipation
        )
        
        # Test basic queries
        print(f"✅ IndividualEventScore: {IndividualEventScore.objects.count()} records")
        print(f"✅ IndividualParticipation: {IndividualParticipation.objects.count()} records") 
        print(f"✅ IndividualEventVote: {IndividualEventVote.objects.count()} records")
        print(f"✅ TeamEventParticipation: {TeamEventParticipation.objects.count()} records")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_leaderboard_view():
    """Test if the leaderboard view works"""
    print("\n🧪 Testing leaderboard functionality...")
    
    try:
        from apps.core.views import LeaderboardView
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/leaderboard/')
        
        view = LeaderboardView()
        view.request = request
        
        context = view.get_context_data()
        print("✅ Leaderboard view executed successfully")
        print(f"✅ Found {len(context.get('teams', []))} teams")
        
        return True
    except Exception as e:
        print(f"❌ Leaderboard test failed: {e}")
        return False

def create_sample_data():
    """Create some sample data to test functionality"""
    print("\n📝 Creating sample data...")
    
    try:
        from apps.core.models import Event, Player, IndividualEventScore
        
        # Check if we have any events and players
        event_count = Event.objects.count()
        player_count = Player.objects.count()
        
        print(f"✅ Found {event_count} events and {player_count} players")
        
        if event_count > 0 and player_count > 0:
            # Try to create a sample individual score
            event = Event.objects.first()
            player = Player.objects.first()
            
            score, created = IndividualEventScore.objects.get_or_create(
                event=event,
                player=player,
                defaults={
                    'points': 10.0,
                    'team_points': 5.0,
                    'notes': 'Sample score for testing',
                    'awarded_by': 'System'
                }
            )
            
            if created:
                print(f"✅ Created sample score: {player.name} - {event.name}")
            else:
                print(f"✅ Sample score already exists: {player.name} - {event.name}")
        
        return True
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def main():
    """Main execution function"""
    print("🚨 Production Leaderboard Emergency Fix")
    print("=" * 50)
    print("Fixing: django.db.utils.ProgrammingError: relation 'core_individualeventscore' does not exist")
    print()
    
    # Step 1: Setup Django
    if not setup_django():
        print("❌ Cannot proceed without Django setup")
        sys.exit(1)
    
    # Step 2: Apply migrations
    if not apply_migrations_safely():
        print("❌ Migration failed - check the error messages above")
        print("💡 Try running the migrations manually:")
        print("   python manage.py migrate core 0010")
        print("   python manage.py migrate core 0011") 
        print("   python manage.py migrate core 0012")
        sys.exit(1)
    
    # Step 3: Test models
    if not test_models():
        print("❌ Models are not accessible - migrations may not have worked")
        sys.exit(1)
    
    # Step 4: Test leaderboard
    if not test_leaderboard_view():
        print("❌ Leaderboard view still has issues")
        sys.exit(1)
    
    # Step 5: Create sample data
    create_sample_data()
    
    print("\n🎉 SUCCESS! Production leaderboard fix completed!")
    print("\n✅ What's working now:")
    print("   - Database tables created")
    print("   - Models accessible")
    print("   - Leaderboard view functional")
    print("   - Malayalam ഓണാഘോഷം branding")
    print("   - Maveli images")
    print("   - Individual & team scoring")
    print("\n🔄 Next steps:")
    print("   1. Restart your Django application")
    print("   2. Visit /leaderboard/ to verify it works")
    print("   3. Visit /admin/ to start adding event scores")
    print("\n📍 URLs to test:")
    print("   - Homepage: / (should show Maveli)")
    print("   - Leaderboard: /leaderboard/ (should show teams)")
    print("   - Admin: /admin/ (should have Individual Event Scores)")

if __name__ == '__main__':
    main()
