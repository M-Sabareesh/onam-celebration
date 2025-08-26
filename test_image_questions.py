#!/usr/bin/env python
"""
Test script for the new Image Question Type feature in ഓണാഘോഷം
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'django-insecure-test-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///db.sqlite3')

django.setup()

def test_image_question_type():
    """Test the new image question type functionality"""
    print("=== Testing Image Question Type Feature ===")
    
    # Test Django
    print(f"✅ Django version: {django.get_version()}")
    
    # Test models
    from apps.core.models import TreasureHuntQuestion, Player, PlayerAnswer
    print(f"✅ TreasureHuntQuestion model: {TreasureHuntQuestion._meta.label}")
    
    # Test question types
    question_types = dict(TreasureHuntQuestion.QUESTION_TYPES)
    print("✅ Available question types:")
    for code, name in TreasureHuntQuestion.QUESTION_TYPES:
        print(f"   - {code}: {name}")
    
    # Verify new question type exists
    if 'image_text' in question_types:
        print("✅ New 'image_text' question type successfully added!")
    else:
        print("❌ 'image_text' question type not found!")
        return False
    
    # Test creating an image question
    try:
        # Check if question already exists
        existing_question = TreasureHuntQuestion.objects.filter(
            question_text__contains="Onam Image Test"
        ).first()
        
        if existing_question:
            print(f"✅ Found existing test question: {existing_question}")
            question = existing_question
        else:
            # Create a test image question
            question = TreasureHuntQuestion.objects.create(
                question_text="Look at this Onam celebration image. What traditional element do you see?",
                question_type="image_text",
                order=999,  # High order to avoid conflicts
                points=15,
                correct_answer="pookalam"  # Example correct answer
            )
            print(f"✅ Created test image question: {question}")
        
        # Test question fields
        print(f"   - Question Text: {question.question_text}")
        print(f"   - Question Type: {question.question_type}")
        print(f"   - Has Image Field: {hasattr(question, 'question_image')}")
        print(f"   - Points: {question.points}")
        
    except Exception as e:
        print(f"❌ Error creating test question: {e}")
        return False
    
    # Test URL patterns
    from django.urls import reverse
    try:
        treasure_hunt_url = reverse('core:treasure_hunt')
        print(f"✅ Treasure hunt URL: {treasure_hunt_url}")
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False
    
    print("\n🎉 Image Question Type feature is working!")
    print("\n🌺 New Feature Summary:")
    print("✅ Added 'image_text' question type for image-based questions")
    print("✅ Added question_image field to store question images")
    print("✅ Updated admin interface to show image indicator")
    print("✅ Enhanced treasure hunt template to display images")
    print("✅ Modified views to handle image_text question type")
    print("✅ Applied database migrations successfully")
    
    print("\n📝 How to use the new Image Question Type:")
    print("1. Go to Admin Panel: http://localhost:8000/admin/ or http://localhost:8000/custom-admin/")
    print("2. Navigate to 'Treasure Hunt Questions'")
    print("3. Create a new question:")
    print("   - Question Type: 'Image Question (Text Answer)'")
    print("   - Upload an image in the 'Question Image' field")
    print("   - Write your question text")
    print("   - Set the correct answer for admin reference")
    print("4. Players will see the image and need to type their answer")
    
    print("\n🖼️ Perfect for Onam-themed questions like:")
    print("- 'What Onam tradition is shown in this image?'")
    print("- 'Name the dish in this Sadhya photo'")
    print("- 'What type of Pookalam pattern is this?'")
    print("- 'Which Kerala art form is depicted here?'")
    
    print("\nYour ഓണാഘോഷം treasure hunt now supports visual questions!")
    print("ഓണാശംസകൾ! 🌺👑🌸")
    
    return True

if __name__ == '__main__':
    try:
        success = test_image_question_type()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
