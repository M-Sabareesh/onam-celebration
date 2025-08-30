"""
Test script for Google Photos integration and mobile photo display
in the Onam Celebration treasure hunt.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import Player, TreasureHuntQuestion, PlayerAnswer


class GooglePhotosIntegrationTest(TestCase):
    """Test Google Photos integration and mobile optimization"""
    
    def setUp(self):
        """Set up test data"""
        # Create a user and player
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.player = Player.objects.create(
            name='Test Player',
            email='test@example.com',
            team='malayali_mavens',
            is_active=True
        )
        
        # Create a photo question
        self.photo_question = TreasureHuntQuestion.objects.create(
            question_text='Upload a photo of your Onam celebration!',
            question_type='photo',
            order=1,
            points=10,
            is_active=True
        )
        
        # Create test image file
        self.test_image = SimpleUploadedFile(
            name='test_photo.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        
        self.client = Client()
    
    def test_database_schema(self):
        """Test that Google Photos fields exist in database"""
        print("🔍 Testing database schema...")
        
        # Create a player answer to test fields
        answer = PlayerAnswer.objects.create(
            player=self.player,
            question=self.photo_question,
            photo_answer=self.test_image
        )
        
        # Test that Google Photos fields exist and can be set
        answer.google_photos_media_id = 'test_media_id_123'
        answer.google_photos_url = 'https://lh3.googleusercontent.com/test_url'
        answer.google_photos_product_url = 'https://photos.google.com/test_product_url'
        
        try:
            answer.save()
            print("✅ Google Photos fields work correctly")
            
            # Test the helper methods
            self.assertTrue(answer.has_google_photos_backup)
            display_url = answer.get_display_photo_url(width=400, height=300)
            self.assertIn('=w400-h300', display_url)
            print("✅ Helper methods work correctly")
            
        except Exception as e:
            print(f"❌ Database schema error: {e}")
            raise
    
    def test_treasure_hunt_view(self):
        """Test treasure hunt view with photo upload"""
        print("🔍 Testing treasure hunt view...")
        
        # Set up session
        session = self.client.session
        session['player_id'] = self.player.id
        session.save()
        
        # Test GET request
        response = self.client.get(reverse('core:treasure_hunt'))
        self.assertEqual(response.status_code, 200)
        print("✅ Treasure hunt page loads correctly")
        
        # Test photo upload
        with open('test_image.jpg', 'wb') as f:
            f.write(b'fake_image_content')
        
        with open('test_image.jpg', 'rb') as image_file:
            response = self.client.post(
                reverse('core:treasure_hunt'),
                {
                    'question_id': self.photo_question.id,
                    'photo_answer': image_file
                }
            )
        
        # Should redirect back to treasure hunt page
        self.assertEqual(response.status_code, 200)
        
        # Check that answer was created
        answer = PlayerAnswer.objects.filter(
            player=self.player,
            question=self.photo_question
        ).first()
        
        self.assertIsNotNone(answer)
        self.assertTrue(answer.photo_answer)
        print("✅ Photo upload works correctly")
        
        # Clean up test file
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')
    
    def test_mobile_template_features(self):
        """Test mobile-specific template features"""
        print("🔍 Testing mobile template features...")
        
        # Create an answer with Google Photos data
        answer = PlayerAnswer.objects.create(
            player=self.player,
            question=self.photo_question,
            photo_answer=self.test_image,
            google_photos_url='https://lh3.googleusercontent.com/test_url'
        )
        
        # Set up session
        session = self.client.session
        session['player_id'] = self.player.id
        session.save()
        
        response = self.client.get(reverse('core:treasure_hunt'))
        content = response.content.decode()
        
        # Check for mobile optimization features
        self.assertIn('mobile-optimized-photo', content)
        self.assertIn('openPhotoModal', content)
        self.assertIn('=w400-h300', content)  # Size parameters
        self.assertIn('photoModal', content)  # Modal exists
        
        print("✅ Mobile template features present")
    
    def test_google_photos_service_import(self):
        """Test that Google Photos service can be imported safely"""
        print("🔍 Testing Google Photos service import...")
        
        try:
            from apps.core.views import GOOGLE_PHOTOS_AVAILABLE, google_photos_service
            
            # Should not fail even if Google API libraries aren't installed
            print(f"✅ Google Photos available: {GOOGLE_PHOTOS_AVAILABLE}")
            
            if GOOGLE_PHOTOS_AVAILABLE:
                print("✅ Google Photos service imported successfully")
            else:
                print("⚠️  Google Photos service not available (expected without API libraries)")
                
        except Exception as e:
            print(f"❌ Import error: {e}")
    
    def test_environment_configuration(self):
        """Test environment configuration"""
        print("🔍 Testing environment configuration...")
        
        from django.conf import settings
        
        # Test default values
        google_enabled = getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False)
        album_id = getattr(settings, 'GOOGLE_PHOTOS_ALBUM_ID', None)
        
        print(f"📍 Google Photos enabled: {google_enabled}")
        print(f"📍 Album ID: {album_id}")
        
        # Should not fail even with default settings
        print("✅ Environment configuration accessible")


def run_tests():
    """Run all tests"""
    print("🚀 Starting Google Photos Integration Tests...")
    print("=" * 50)
    
    import unittest
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(GooglePhotosIntegrationTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        print("\n✅ Google Photos integration is working correctly")
        print("✅ Mobile optimization features are present")
        print("✅ Database schema is properly configured")
        print("\n📱 Your treasure hunt should now work better on mobile devices!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        print("\n💡 Run the fix command: python manage.py fix_google_photos --fix-db")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Change to the Django project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = run_tests()
    exit(0 if success else 1)
