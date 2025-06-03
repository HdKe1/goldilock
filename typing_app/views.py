from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from .models import TypingTest, TestResult, UserProfile
from .serializers import (
    TypingTestSerializer, TestResultSerializer, TestResultCreateSerializer,
    UserProfileSerializer, UserSerializer
)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not all([username, email, password]):
        return Response({'error': 'All fields are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username,
        'email': user.email
    }, status=status.HTTP_201_CREATED)

class TypingTestListView(generics.ListAPIView):
    serializer_class = TypingTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = TypingTest.objects.filter(is_active=True)
        difficulty = self.request.query_params.get('difficulty')
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.order_by('?')  # Random order

class TypingTestDetailView(generics.RetrieveAPIView):
    queryset = TypingTest.objects.filter(is_active=True)
    serializer_class = TypingTestSerializer
    permission_classes = [permissions.IsAuthenticated]

class TestResultCreateView(generics.CreateAPIView):
    serializer_class = TestResultCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class TestResultListView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]
    
    # Recent results (last 10)
    recent_results = TestResult.objects.filter(user=user)[:10]
    
    # Best results
    best_wpm_result = TestResult.objects.filter(user=user).order_by('-wpm').first()
    best_accuracy_result = TestResult.objects.filter(user=user).order_by('-accuracy').first()
    
    return Response({
        'profile': UserProfileSerializer(profile).data,
        'recent_results': TestResultSerializer(recent_results, many=True).data,
        'best_wpm_result': TestResultSerializer(best_wpm_result).data if best_wpm_result else None,
        'best_accuracy_result': TestResultSerializer(best_accuracy_result).data if best_accuracy_result else None,
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def leaderboard(request):
    # Top WPM users
    top_wpm = UserProfile.objects.filter(total_tests__gt=0).order_by('-best_wpm')[:10]
    
    # Top accuracy users
    top_accuracy = UserProfile.objects.filter(total_tests__gt=0).order_by('-best_accuracy')[:10]
    
    return Response({
        'top_wpm': UserProfileSerializer(top_wpm, many=True).data,
        'top_accuracy': UserProfileSerializer(top_accuracy, many=True).data,
    })
