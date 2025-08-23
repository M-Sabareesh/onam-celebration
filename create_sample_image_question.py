#!/usr/bin/env python
"""
Script to create a sample image question for testing
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import TreasureHuntQuestion

def create_sample_image_question():
    """Create a sample image question"""
    print("Creating sample image question...")
    
    # Check if sample question already exists
    existing = TreasureHuntQuestion.objects.filter(order=100).first()
    if existing:
        print(f"Sample question already exists: Q{existing.order}")
        print(f"Question type: {existing.question_type}")
        print(f"Question text: {existing.question_text}")
        return existing
    
    # Create new sample image question
    question = TreasureHuntQuestion.objects.create(
        question_text="What traditional Kerala festival celebrates the return of King Mahabali? (Look at the image for clues)",
        question_type='image_text',
        order=100,
        points=20,
        is_active=True,
        correct_answer='Onam'
    )
    
    print(f"✓ Created sample image question: Q{question.order}")
    print(f"  Type: {question.question_type}")
    print(f"  Text: {question.question_text}")
    print(f"  Points: {question.points}")
    print()
    print("Note: You can add an image to this question through the Django admin interface.")
    print("Go to: http://127.0.0.1:8000/admin/core/treasurehuntquestion/")
    
    return question

if __name__ == "__main__":
    create_sample_image_question()
