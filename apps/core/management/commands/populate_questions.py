from django.core.management.base import BaseCommand
from apps.core.models import TreasureHuntQuestion


class Command(BaseCommand):
    help = 'Populate treasure hunt questions for Onam celebration'

    def handle(self, *args, **options):
        questions_data = [
            {
                'order': 1,
                'question_text': 'Take selfie with more people and upload one photo here (link to upload photo)',
                'question_type': 'photo',
                'points': 15,
            },
            {
                'order': 2,
                'question_text': '1+1=2 is maths, 1+1=3 is ............... (Fill in the blank)',
                'question_type': 'text',
                'points': 10,
            },
            {
                'order': 3,
                'question_text': 'List at least 10 items in Onam Sadhya (traditional feast)',
                'question_type': 'text',
                'points': 20,
            },
            {
                'order': 4,
                'question_text': 'Who in this function went to India recently and when? (Name and approximate date)',
                'question_type': 'text',
                'points': 15,
            },
            {
                'order': 5,
                'question_text': 'Last Malayalam movie you saw in theater was ............... (Fill in the blank)',
                'question_type': 'text',
                'points': 10,
            },
            {
                'order': 6,
                'question_text': 'What is the name of the legendary king whose return Onam celebrates?',
                'question_type': 'multiple_choice',
                'option_a': 'King Mahabali',
                'option_b': 'King Ravana',
                'option_c': 'King Dasharatha',
                'option_d': 'King Vikramaditya',
                'correct_answer': 'King Mahabali',
                'points': 10,
            },
            {
                'order': 7,
                'question_text': 'Upload a photo of your best Pookalam (flower carpet) or any Onam decoration',
                'question_type': 'photo',
                'points': 15,
            },
            {
                'order': 8,
                'question_text': 'Name 5 traditional Kerala dances performed during Onam',
                'question_type': 'text',
                'points': 15,
            },
            {
                'order': 9,
                'question_text': 'Which month in Malayalam calendar does Onam fall?',
                'question_type': 'multiple_choice',
                'option_a': 'Chingam',
                'option_b': 'Kanni',
                'option_c': 'Tulam',
                'option_d': 'Vrischikam',
                'correct_answer': 'Chingam',
                'points': 10,
            },
            {
                'order': 10,
                'question_text': 'Upload a photo of your team enjoying Onam celebration together',
                'question_type': 'photo',
                'points': 20,
            },
            {
                'order': 11,
                'question_text': 'Complete this traditional Onam greeting: "Onam ___________"',
                'question_type': 'multiple_choice',
                'option_a': 'Ashamsakal',
                'option_b': 'Namaskaram',
                'option_c': 'Vanakkam',
                'option_d': 'Adaab',
                'correct_answer': 'Ashamsakal',
                'points': 10,
            },
            {
                'order': 12,
                'question_text': 'What is the significance of the 10 days of Onam? Describe briefly.',
                'question_type': 'text',
                'points': 15,
            },
            {
                'order': 13,
                'question_text': 'Upload a photo recreating a famous Malayalam movie scene',
                'question_type': 'photo',
                'points': 25,
            },
            {
                'order': 14,
                'question_text': 'Name your favorite Malayalam actor/actress and their best movie',
                'question_type': 'text',
                'points': 10,
            },
            {
                'order': 15,
                'question_text': 'Which spice is known as "Kerala Gold" and is essential in Kerala cuisine?',
                'question_type': 'multiple_choice',
                'option_a': 'Cardamom',
                'option_b': 'Black Pepper',
                'option_c': 'Turmeric',
                'option_d': 'Cinnamon',
                'correct_answer': 'Black Pepper',
                'points': 10,
            },
        ]

        created_count = 0
        for question_data in questions_data:
            question, created = TreasureHuntQuestion.objects.get_or_create(
                order=question_data['order'],
                defaults=question_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created question {question.order}: {question.question_text[:50]}...")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} treasure hunt questions. '
                f'Total questions in database: {TreasureHuntQuestion.objects.count()}'
            )
        )
