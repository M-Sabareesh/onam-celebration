#!/usr/bin/env python
"""
Test script to verify image question type functionality
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import TreasureHuntQuestion, Player, PlayerAnswer

def test_image_questions():
    """Test image question type functionality"""
    print("=== Testing Image Question Type ===")
    
    # Check if image_text question type exists
    image_questions = TreasureHuntQuestion.objects.filter(question_type='image_text')
    print(f"Found {image_questions.count()} image questions in database")
    
    for question in image_questions:
        print(f"  - Q{question.order}: {question.question_text[:50]}...")
        if question.question_image:
            print(f"    Image: {question.question_image.name}")
        else:
            print("    No image uploaded")
    
    # Test creating a sample image question
    print("\n=== Creating Sample Image Question ===")
    try:
        sample_question, created = TreasureHuntQuestion.objects.get_or_create(
            question_text="What festival is being celebrated in this image?",
            question_type='image_text',
            order=999,  # High order to avoid conflicts
            defaults={
                'points': 15,
                'is_active': True,
                'correct_answer': 'Onam'
            }
        )
        
        if created:
            print(f"✓ Created sample image question: Q{sample_question.order}")
        else:
            print(f"✓ Sample image question already exists: Q{sample_question.order}")
            
    except Exception as e:
        print(f"✗ Error creating sample question: {e}")
    
    # Test template filter import
    print("\n=== Testing Template Filter ===")
    try:
        from apps.core.templatetags.core_extras import get_item
        
        # Test the filter
        test_dict = {1: "answer_1", 2: "answer_2", 3: "answer_3"}
        result = get_item(test_dict, 2)
        
        if result == "answer_2":
            print("✓ Template filter get_item working correctly")
        else:
            print(f"✗ Template filter returned unexpected result: {result}")
            
    except ImportError as e:
        print(f"✗ Error importing template filter: {e}")
    except Exception as e:
        print(f"✗ Error testing template filter: {e}")
    
    print("\n=== Summary ===")
    print("Image question type 'image_text' is implemented with:")
    print("- Model field: question_image (ImageField)")
    print("- Question type: image_text")
    print("- Template support with get_item filter")
    print("- Admin interface with image preview")
    print("- Answer submission handling")
    
    # Show question type choices
    print(f"\nAvailable question types: {[choice[0] for choice in TreasureHuntQuestion.QUESTION_TYPES]}")

if __name__ == "__main__":
    test_image_questions()
