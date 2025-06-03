from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TypingTest, TestResult, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user', 'total_tests', 'best_wpm', 'best_accuracy', 
                           'average_wpm', 'average_accuracy', 'total_time_typed']

class TypingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypingTest
        fields = '__all__'
        read_only_fields = ['id', 'word_count', 'created_at']

class TestResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    test = TypingTestSerializer(read_only=True)
    
    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ['id', 'user', 'completed_at']

class TestResultCreateSerializer(serializers.ModelSerializer):
    test_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = TestResult
        fields = ['test_id', 'duration_seconds', 'wpm', 'raw_wpm', 'accuracy',
                 'total_characters', 'correct_characters', 'incorrect_characters',
                 'total_words', 'correct_words', 'incorrect_words', 'started_at']
    
    def create(self, validated_data):
        test_id = validated_data.pop('test_id')
        test = TypingTest.objects.get(id=test_id)
        user = self.context['request'].user
        
        result = TestResult.objects.create(
            user=user,
            test=test,
            **validated_data
        )
        
        # Update user profile stats
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.update_stats()
        
        return result
