from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('select-player/', views.SelectPlayerView.as_view(), name='select_player'),
    path('dashboard/', views.GameDashboardView.as_view(), name='game_dashboard'),
    path('treasure-hunt/', views.TreasureHuntView.as_view(), name='treasure_hunt'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('logout/', views.logout_player, name='logout'),
    path('about/', views.AboutOnamView.as_view(), name='about'),
    path('health/', views.health_check, name='health'),
    
    # Events and voting
    path('events/', views.EventsListView.as_view(), name='events_list'),
    path('events/<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),
    
    # API endpoints
    path('api/traditions/', views.traditions_api, name='traditions_api'),
    path('api/team-status/', views.team_status_api, name='team_status_api'),
    path('api/events/<int:event_id>/voting/', views.EventVotingAPI.as_view(), name='event_voting_api'),
    
    # Team Management (works without static files)
    path('team-management/', views.team_management, name='team_management'),
]
