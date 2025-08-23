from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from apps.core.models import Player


class PlayerOnlineStatusMiddleware(MiddlewareMixin):
    """
    Middleware to track player online status based on session activity
    """
    
    def process_request(self, request):
        # Update last activity for logged-in players
        player_id = request.session.get('player_id')
        if player_id:
            try:
                player = Player.objects.get(id=player_id)
                player.last_activity = timezone.now()
                if not player.is_online:
                    player.is_online = True
                player.save(update_fields=['last_activity', 'is_online'])
            except Player.DoesNotExist:
                # Clear invalid session
                if 'player_id' in request.session:
                    del request.session['player_id']
                if 'player_name' in request.session:
                    del request.session['player_name']
                if 'player_team' in request.session:
                    del request.session['player_team']
        
        return None
    
    def process_response(self, request, response):
        return response
