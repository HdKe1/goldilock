from django.core.management.base import BaseCommand
from typing_app.models import TypingTest

class Command(BaseCommand):
    help = 'Populate database with sample typing tests'

    def handle(self, *args, **options):
        sample_texts = [
            {
                'text': 'The quick brown fox jumps over the lazy dog. This pangram contains every letter of the alphabet at least once.',
                'difficulty': 'easy',
                'language': 'english'
            },
            {
                'text': 'Technology has revolutionized the way we communicate, work, and live. From smartphones to artificial intelligence, innovation continues to shape our future.',
                'difficulty': 'medium',
                'language': 'english'
            },
            {
                'text': 'Quantum computing represents a paradigm shift in computational capabilities, leveraging quantum mechanical phenomena like superposition and entanglement to process information exponentially faster than classical computers.',
                'difficulty': 'hard',
                'language': 'english'
            }
        ]

        for text_data in sample_texts:
            TypingTest.objects.get_or_create(**text_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated typing tests'))