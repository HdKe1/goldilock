from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', views.CustomAuthToken.as_view(), name='auth_login'),
    path('auth/register/', views.register, name='auth_register'),
    
    # Typing tests
    path('tests/', views.TypingTestListView.as_view(), name='test_list'),
    path('tests/<uuid:pk>/', views.TypingTestDetailView.as_view(), name='test_detail'),
    
    # Test results
    path('results/', views.TestResultListView.as_view(), name='result_list'),
    path('results/create/', views.TestResultCreateView.as_view(), name='result_create'),
    
    # User profile and stats
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('stats/', views.user_stats, name='user_stats'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]