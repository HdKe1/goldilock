from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class TypingTest(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    word_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.word_count:
            self.word_count = len(self.text.split())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Test {self.id} - {self.difficulty} ({self.word_count} words)"

class TestResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(TypingTest, on_delete=models.CASCADE, related_name='results')
    
    # Test configuration
    duration_seconds = models.IntegerField(validators=[MinValueValidator(15), MaxValueValidator(300)])
    
    # Results
    wpm = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    raw_wpm = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    accuracy = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Detailed stats
    total_characters = models.IntegerField()
    correct_characters = models.IntegerField()
    incorrect_characters = models.IntegerField()
    total_words = models.IntegerField()
    correct_words = models.IntegerField()
    incorrect_words = models.IntegerField()
    
    # Timestamps
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.wpm} WPM ({self.accuracy}%)"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_tests = models.IntegerField(default=0)
    best_wpm = models.FloatField(default=0)
    best_accuracy = models.FloatField(default=0)
    average_wpm = models.FloatField(default=0)
    average_accuracy = models.FloatField(default=0)
    total_time_typed = models.IntegerField(default=0)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_stats(self):
        """Update user statistics based on all test results"""
        results = self.user.test_results.all()
        if results.exists():
            self.total_tests = results.count()
            self.best_wpm = results.aggregate(models.Max('wpm'))['wpm__max'] or 0
            self.best_accuracy = results.aggregate(models.Max('accuracy'))['accuracy__max'] or 0
            self.average_wpm = results.aggregate(models.Avg('wpm'))['wpm__avg'] or 0
            self.average_accuracy = results.aggregate(models.Avg('accuracy'))['accuracy__avg'] or 0
            self.total_time_typed = results.aggregate(models.Sum('duration_seconds'))['duration_seconds__sum'] or 0
            self.save()
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
