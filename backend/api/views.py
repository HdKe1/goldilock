from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics,status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg
from .models import Stats, Attempt

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_attempt(request):
    try:
        # Get WPM from request
        wpm = request.data.get('wpm')
        
        if not wpm or not isinstance(wpm, int) or wpm <= 0:
            return Response(
                {'error': 'Valid WPM value is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        
        # Save individual attempt
        attempt = Attempt.objects.create(
            user=user,
            wpm=wpm
        )
        
        # Calculate new average from all attempts
        avg_wpm = Attempt.objects.filter(user=user).aggregate(
            avg=Avg('wpm')
        )['avg']
        
        # Update or create Stats record
        stats, created = Stats.objects.get_or_create(
            username=user,
            defaults={'avg_wpm': avg_wpm, 'last_wpm': wpm}
        )
        
        if not created:
            stats.avg_wpm = avg_wpm
            stats.last_wpm = wpm
            stats.save()
        
        return Response({
            'success': True,
            'message': 'WPM saved successfully',
            'data': {
                'attempt_id': attempt.id,
                'wpm': wpm,
                'avg_wpm': round(avg_wpm, 2),
                'total_attempts': Attempt.objects.filter(user=user).count()
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    try:
        user = request.user
        
        # Get stats
        try:
            stats = Stats.objects.get(username=user)
            stats_data = {
                'avg_wpm': stats.avg_wpm,
                'last_wpm': stats.last_wpm
            }
        except Stats.DoesNotExist:
            stats_data = {
                'avg_wpm': 0,
                'last_wpm': 0
            }
        
        # Get recent attempts
        recent_attempts = Attempt.objects.filter(user=user)[:10]
        attempts_data = [
            {
                'wpm': attempt.wpm,
                'timestamp': attempt.timestamp.isoformat()
            } for attempt in recent_attempts
        ]
        
        total_attempts = Attempt.objects.filter(user=user).count()
        
        return Response({
            'success': True,
            'data': {
                'stats': stats_data,
                'recent_attempts': attempts_data,
                'total_attempts': total_attempts
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)