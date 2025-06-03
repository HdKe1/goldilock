from django.contrib import admin
from .models import TypingTest, TestResult, UserProfile

@admin.register(TypingTest)
class TypingTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'difficulty', 'word_count', 'is_active', 'created_at']
    list_filter = ['difficulty', 'is_active']
    search_fields = ['text']
    readonly_fields = ['word_count', 'created_at']

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'wpm', 'accuracy', 'duration_seconds', 'completed_at']
    list_filter = ['test__difficulty', 'completed_at']
    search_fields = ['user__username']
    readonly_fields = ['completed_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_tests', 'best_wpm', 'best_accuracy', 'average_wpm']
    readonly_fields = ['total_tests', 'best_wpm', 'best_accuracy', 'average_wpm', 
                      'average_accuracy', 'total_time_typed', 'created_at', 'updated_at']