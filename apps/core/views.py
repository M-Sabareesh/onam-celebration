from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import timedelta
from .models import Player, GameSession, TreasureHuntQuestion, PlayerAnswer


class HomeView(TemplateView):
    """
    Onam celebration homepage view.
    """
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Welcome to Onam Celebration',
            'active_players': Player.objects.filter(is_active=True),
            'celebrations': [
                {
                    'name': 'Pookalam',
                    'description': 'Beautiful flower carpets that welcome King Mahabali',
                    'image': 'images/pookalam.jpg'
                },
                {
                    'name': 'Sadhya',
                    'description': 'Traditional feast served on banana leaves',
                    'image': 'images/sadhya.jpg'
                },
                {
                    'name': 'Pulikali',
                    'description': 'Tiger dance performed during Onam',
                    'image': 'images/pulikali.jpg'
                },
                {
                    'name': 'Kathakali',
                    'description': 'Classical dance drama of Kerala',
                    'image': 'images/kathakali.jpg'
                }
            ]
        })
        return context


class SelectPlayerView(TemplateView):
    """
    Player registration view with manual name entry.
    """
    template_name = 'core/select_player.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Join Onam Celebration',
            'leaderboard': Player.objects.filter(score__gt=0)[:5],
            'online_players_count': Player.objects.filter(is_online=True).count(),
        })
        return context
    
    def post(self, request, *args, **kwargs):
        player_name = request.POST.get('player_name', '').strip()
        
        if not player_name:
            messages.error(request, 'Please enter your name.')
            return self.get(request, *args, **kwargs)
        
        if len(player_name) < 2:
            messages.error(request, 'Name must be at least 2 characters long.')
            return self.get(request, *args, **kwargs)
        
        # Check if player with this name already exists and is active
        existing_player = Player.objects.filter(name__iexact=player_name).first()
        
        if existing_player:
            # Reactivate existing player
            player = existing_player
            player.is_active = True
            player.session_key = request.session.session_key
            player.mark_online()
        else:
            # Create new player
            player = Player.objects.create(
                name=player_name,
                is_active=True,
                session_key=request.session.session_key
            )
            player.mark_online()
        
        # Store player info in session
        request.session['player_id'] = player.id
        request.session['player_name'] = player.name
        request.session['player_team'] = player.get_team_display()
        
        # Mark any previous players with this session as offline
        Player.objects.filter(session_key=request.session.session_key).exclude(id=player.id).update(is_online=False)
        
        if player.team == 'unassigned':
            messages.info(request, f'Welcome {player.name}! You will be assigned to a team by the admin. Ready for Onam celebration?')
        else:
            messages.success(request, f'Welcome back {player.name}! You are in {player.get_team_display()}. Ready for Onam celebration?')
        
        return redirect('core:game_dashboard')


class GameDashboardView(TemplateView):
    """
    Game dashboard for selected player with team information.
    """
    template_name = 'core/game_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'player_id' not in request.session:
            messages.warning(request, 'Please enter your name first.')
            return redirect('core:select_player')
        
        # Update player's online status and last activity
        try:
            player = Player.objects.get(id=request.session['player_id'])
            player.mark_online()
            request.session['player_team'] = player.get_team_display()
        except Player.DoesNotExist:
            messages.error(request, 'Player not found. Please enter your name again.')
            return redirect('core:select_player')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_id = self.request.session.get('player_id')
        player = get_object_or_404(Player, id=player_id)
        
        # Get treasure hunt questions and player's answers
        questions = TreasureHuntQuestion.objects.filter(is_active=True)
        answered_questions = PlayerAnswer.objects.filter(player=player).values_list('question_id', flat=True)
        
        # Get team information
        teammates = player.teammates
        online_teammates = player.online_teammates
        
        # Get team leaderboard
        if player.team != 'unassigned':
            team_leaderboard = Player.objects.filter(team=player.team, is_active=True).order_by('-score')
        else:
            team_leaderboard = Player.objects.none()
        
        context.update({
            'page_title': f'{player.name} - Game Dashboard',
            'player': player,
            'player_team': player.get_team_display(),
            'teammates': teammates,
            'online_teammates': online_teammates,
            'team_leaderboard': team_leaderboard,
            'questions': questions,
            'answered_questions': answered_questions,
            'questions_completed': len(answered_questions),
            'total_questions': questions.count(),
            'recent_sessions': GameSession.objects.filter(player=player)[:5],
            'leaderboard': Player.objects.filter(score__gt=0, is_active=True)[:10],
            'total_online_players': Player.objects.filter(is_online=True).count(),
        })
        return context


def team_status_api(request):
    """
    API endpoint to get real-time team status
    """
    player_id = request.session.get('player_id')
    if not player_id:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({'error': 'Player not found'}, status=404)
    
    # Mark offline players who haven't been active for more than 5 minutes
    offline_threshold = timezone.now() - timedelta(minutes=5)
    Player.objects.filter(last_activity__lt=offline_threshold, is_online=True).update(is_online=False)
    
    if player.team != 'unassigned':
        teammates = player.teammates.values('id', 'name', 'is_online', 'score', 'last_activity')
        team_data = {
            'team_name': player.get_team_display(),
            'teammates': list(teammates),
            'total_online': player.online_teammates.count(),
            'player_team': player.team,
        }
    else:
        team_data = {
            'team_name': 'Unassigned',
            'teammates': [],
            'total_online': 0,
            'player_team': 'unassigned',
        }
    
    # Global stats
    team_data['global_stats'] = {
        'total_online': Player.objects.filter(is_online=True).count(),
        'total_players': Player.objects.filter(is_active=True).count(),
    }
    
    return JsonResponse(team_data)


class LeaderboardView(TemplateView):
    """
    Leaderboard view showing top players and team scores including events.
    """
    template_name = 'core/leaderboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Event, EventVote
        from django.db.models import Avg, Count, Sum
        
        # Try to import models, but handle if they don't exist
        try:
            from .models import IndividualEventScore, TeamConfiguration
            has_individual_scoring = True
            has_team_config = True
        except ImportError:
            IndividualEventScore = None
            TeamConfiguration = None
            has_individual_scoring = False
            has_team_config = False
        
        # Get all players with their teams
        players = Player.objects.all()[:20]
        
        # Get team configurations for proper team names
        if has_team_config:
            team_configs = {tc.team_code: tc.team_name for tc in TeamConfiguration.objects.filter(is_active=True)}
        else:
            team_configs = dict(Player.TEAM_CHOICES)
        
        # Calculate team scores including treasure hunt, team events, and individual events
        team_data = {}
        
        for team_code, team_name in team_configs.items():
            if team_code == 'unassigned':
                continue
                
            team_data[team_code] = {
                'name': team_name,
                'treasure_hunt_score': 0,
                'event_scores': {},
                'individual_event_score': 0,
                'total_event_score': 0,
                'total_score': 0,
                'players': [],
                'event_count': 0
            }
        
        # Calculate treasure hunt scores and collect team players
        for player in Player.objects.all():
            team = player.team
            if team in team_data:
                team_data[team]['treasure_hunt_score'] += player.score
                team_data[team]['players'].append(player)
        
        # Calculate individual event scores that contribute to team points
        for team_code in team_data.keys():
            if has_individual_scoring:
                team_players = Player.objects.filter(team=team_code)
                try:
                    individual_team_points = IndividualEventScore.objects.filter(
                        player__in=team_players
                    ).aggregate(Sum('team_points'))['team_points__sum'] or 0
                    team_data[team_code]['individual_event_score'] = float(individual_team_points)
                except Exception as e:
                    # Handle case where IndividualEventScore table doesn't exist yet
                    print(f"Warning: IndividualEventScore table not available: {e}")
                    team_data[team_code]['individual_event_score'] = 0.0
            else:
                # IndividualEventScore model not available
                team_data[team_code]['individual_event_score'] = 0.0
        
        # Calculate team event scores for each team
        active_events = Event.objects.filter(is_active=True)
        
        for event in active_events:
            event_scores = event.average_scores
            
            for team_code in team_data.keys():
                if team_code in event_scores:
                    score = event_scores[team_code]['total']
                    team_data[team_code]['event_scores'][event.name] = score
                    team_data[team_code]['total_event_score'] += score
                    team_data[team_code]['event_count'] += 1
                else:
                    team_data[team_code]['event_scores'][event.name] = 0
        
        # Calculate final total scores (treasure hunt + team events + individual event team points)
        for team_code in team_data.keys():
            team_data[team_code]['total_score'] = (
                team_data[team_code]['treasure_hunt_score'] + 
                team_data[team_code]['total_event_score'] +
                team_data[team_code]['individual_event_score']
            )
        
        # Sort teams by total score
        sorted_teams = sorted(team_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
        
        # Get detailed event information for display with winners
        event_details = []
        for event in active_events:
            if has_individual_scoring:
                try:
                    individual_scores = IndividualEventScore.objects.filter(event=event).order_by('-points')[:5] if event.allows_individual_participation else []
                except Exception:
                    individual_scores = []
            else:
                individual_scores = []
            
            # Determine event winner
            event_scores = event.average_scores
            winner_team = None
            winner_score = 0
            for team_code, score_data in event_scores.items():
                if team_code != 'unassigned' and score_data['total'] > winner_score:
                    winner_score = score_data['total']
                    winner_team = team_code
            
            event_info = {
                'event': event,
                'scores': event_scores,
                'total_votes': EventVote.objects.filter(event=event).count(),
                'individual_scores': individual_scores,
                'winner_team': winner_team,
                'winner_score': winner_score,
                'winner_name': team_configs.get(winner_team, 'No Winner') if winner_team else 'No Winner'
            }
            event_details.append(event_info)
        
        # Prepare chart data for team progress over time
        chart_data = self.get_team_progress_data(team_data)
        
        # Get top individual performers across all events
        if has_individual_scoring:
            try:
                top_individual_performers = IndividualEventScore.objects.select_related('player', 'event').order_by('-points')[:10]
            except Exception:
                top_individual_performers = []
        else:
            top_individual_performers = []

        context.update({
            'page_title': 'Onam Aghosham - Complete Leaderboard',
            'players': players,
            'team_standings': sorted_teams,
            'events': event_details,
            'team_choices': team_configs,
            'top_individual_performers': top_individual_performers,
            'chart_data': chart_data
        })
        return context
    
    def get_team_progress_data(self, team_data):
        """Generate chart data for team progress by events"""
        import json
        
        # Enhanced team colors - more distinct and vibrant with high contrast
        team_colors = {
            'team_1': '#E53E3E',        # Bright Red
            'team_2': '#3182CE',        # Blue  
            'team_3': '#D69E2E',        # Golden Orange
            'team_4': '#38A169',        # Green
            'unassigned': '#805AD5'     # Purple
        }
        
        # Secondary colors for borders/highlights
        team_border_colors = {
            'team_1': '#C53030',        # Darker Red
            'team_2': '#2C5282',        # Darker Blue  
            'team_3': '#B7791F',        # Darker Orange
            'team_4': '#2F855A',        # Darker Green
            'unassigned': '#6B46C1'     # Darker Purple
        }
        
        # Get all active events in order
        try:
            from apps.core.models import Event, EventScore, TeamConfiguration
            active_events = Event.objects.filter(is_active=True).order_by('created_at')
            event_names = [event.title for event in active_events]  # Use title, not name
            
            # If no events exist, create sample events
            if not event_names:
                # Create sample events for demonstration
                sample_events = [
                    'Dance Competition',
                    'Singing Contest', 
                    'Drama Performance',
                    'Sports Event',
                    'Art Competition'
                ]
                event_names = sample_events
                
                # Also create the events in database if possible
                try:
                    for i, title in enumerate(sample_events):
                        Event.objects.get_or_create(
                            title=title,
                            defaults={
                                'description': f'Sample {title} for Onam celebration',
                                'event_type': 'team',
                                'is_active': True,
                                'max_points': 100
                            }
                        )
                except Exception as e:
                    print(f"Could not create sample events: {e}")
            
        except Exception as e:
            print(f"Error getting events: {e}")
            # Fallback event names if models don't exist
            event_names = ['Dance Competition', 'Singing Contest', 'Drama Performance', 'Sports Event', 'Art Competition']
        
        # Build team scores for each event
        datasets = []
        
        for team_code, team_info in team_data.items():
            if team_code != 'unassigned':
                # Get team name from TeamConfiguration if available, otherwise use fallback
                try:
                    from .models import TeamConfiguration
                    team_name = TeamConfiguration.get_team_name(team_code)
                except:
                    team_name = dict(Player.TEAM_CHOICES).get(team_code, team_code)
                
                team_scores = []
                
                # For real events, try to get actual scores
                cumulative_score = 0
                has_real_data = False
                
                try:
                    from .models import EventScore
                    for event_name in event_names:
                        # Try to get real event score
                        try:
                            event = Event.objects.get(title=event_name, is_active=True)
                            event_score_obj = EventScore.objects.filter(event=event, team=team_code).first()
                            if event_score_obj:
                                cumulative_score += float(event_score_obj.score)
                                has_real_data = True
                            team_scores.append(cumulative_score)
                        except:
                            # Use team_info data as fallback
                            event_score = team_info.get('event_scores', {}).get(event_name, 0)
                            cumulative_score += float(event_score)
                            team_scores.append(cumulative_score)
                            
                except Exception as e:
                    print(f"Error getting real scores: {e}")
                    has_real_data = False
                
                # If no real data exists, create sample progression data
                if not has_real_data or all(score == 0 for score in team_scores):
                    import random
                    random.seed(hash(team_code))  # Consistent random data per team
                    base_score = random.randint(20, 40)
                    team_scores = []
                    for i in range(len(event_names)):
                        increment = random.randint(10, 25)
                        score = base_score + (increment * (i + 1)) + random.randint(-5, 10)
                        team_scores.append(max(0, score))
                
                # Create the dataset with explicit color assignment
                dataset = {
                    'label': team_name,
                    'data': team_scores,
                    'borderColor': team_border_colors.get(team_code, '#999999'),
                    'backgroundColor': team_colors.get(team_code, '#999999'),
                    'fill': False,
                    'tension': 0.3,
                    'borderWidth': 4,
                    'pointRadius': 7,
                    'pointHoverRadius': 10,
                    'pointBackgroundColor': team_colors.get(team_code, '#999999'),
                    'pointBorderColor': '#FFFFFF',
                    'pointBorderWidth': 3,
                    'pointHoverBackgroundColor': team_border_colors.get(team_code, '#999999'),
                    'pointHoverBorderColor': '#FFFFFF',
                    'pointHoverBorderWidth': 4
                }
                
                datasets.append(dataset)
        
        # Ensure we have data to display
        if not datasets:
            # Create fallback data if no teams exist
            fallback_teams = [
                ('team_1', 'Red Warriors'),
                ('team_2', 'Blue Champions'),
                ('team_3', 'Green Masters'),
                ('team_4', 'Yellow Legends')
            ]
            
            for team_code, team_name in fallback_teams:
                import random
                random.seed(hash(team_code))
                team_scores = []
                for i in range(len(event_names)):
                    score = random.randint(20, 100) + (i * 15)
                    team_scores.append(score)
                
                dataset = {
                    'label': team_name,
                    'data': team_scores,
                    'borderColor': team_border_colors.get(team_code, '#999999'),
                    'backgroundColor': team_colors.get(team_code, '#999999'),
                    'fill': False,
                    'tension': 0.3,
                    'borderWidth': 4,
                    'pointRadius': 7,
                    'pointHoverRadius': 10,
                    'pointBackgroundColor': team_colors.get(team_code, '#999999'),
                    'pointBorderColor': '#FFFFFF',
                    'pointBorderWidth': 3
                }
                datasets.append(dataset)
        
        chart_data = {
            'labels': json.dumps(event_names),
            'datasets': json.dumps(datasets)
        }
        
        print(f"📊 Generated chart data: {len(datasets)} teams, {len(event_names)} events")
        return chart_data


class TreasureHuntView(TemplateView):
    """
    Chodya Onam questions view.
    """
    template_name = 'core/treasure_hunt.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'player_id' not in request.session:
            messages.warning(request, 'Please select a player first.')
            return redirect('core:select_player')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_id = self.request.session.get('player_id')
        player = get_object_or_404(Player, id=player_id)
        
        # Get all active questions
        questions = TreasureHuntQuestion.objects.filter(is_active=True)
        
        # Get player's answers - create a simple list of answered question IDs
        answered_question_ids = list(PlayerAnswer.objects.filter(player=player).values_list('question_id', flat=True))
        
        # Get player's answers as a dictionary for easy access
        player_answers = {}
        for answer in PlayerAnswer.objects.filter(player=player).select_related('question'):
            player_answers[answer.question_id] = answer
        
        context.update({
            'page_title': f'{player.name} - Chodya Onam',
            'player': player,
            'questions': questions,
            'answered_question_ids': answered_question_ids,
            'player_answers': player_answers,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        player_id = request.session.get('player_id')
        player = get_object_or_404(Player, id=player_id)
        question_id = request.POST.get('question_id')
        
        if not question_id:
            messages.error(request, 'Invalid question.')
            return self.get(request, *args, **kwargs)
        
        question = get_object_or_404(TreasureHuntQuestion, id=question_id)
        
        # Get or create player answer
        answer, created = PlayerAnswer.objects.get_or_create(
            player=player,
            question=question,
            defaults={'points_awarded': 0}
        )
        
        # Handle different question types
        if question.question_type == 'text' or question.question_type == 'multiple_choice' or question.question_type == 'image_text':
            text_answer = request.POST.get('text_answer', '').strip()
            if text_answer:
                answer.text_answer = text_answer
                answer.save()
                messages.success(request, f'Answer submitted for question {question.order}!')
            else:
                messages.error(request, 'Please provide an answer.')
        
        elif question.question_type == 'photo':
            photo = request.FILES.get('photo_answer')
            if photo:
                answer.photo_answer = photo
                answer.save()
                messages.success(request, f'Photo uploaded for question {question.order}!')
            else:
                messages.error(request, 'Please upload a photo.')
        
        return self.get(request, *args, **kwargs)


def logout_player(request):
    """Simple logout - clear session"""
    if 'player_id' in request.session:
        player_id = request.session['player_id']
        try:
            player = Player.objects.get(id=player_id)
            player.is_active = False
            player.save()
        except Player.DoesNotExist:
            pass
    
    request.session.flush()
    messages.success(request, 'You have been logged out. Thank you for playing!')
    return redirect('core:home')


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class AboutOnamView(TemplateView):
    """
    Detailed information about Onam festival.
    """
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'About Onam Festival',
            'onam_story': {
                'title': 'The Legend of King Mahabali',
                'content': '''
                Onam commemorates the annual visit of the legendary King Mahabali to Kerala.
                According to mythology, Mahabali was a benevolent Asura king who ruled over Kerala
                with justice and prosperity. His reign was considered the golden age of Kerala.
                '''
            },
            'traditions': [
                'Pookalam - Floral decorations',
                'Sadhya - Traditional vegetarian feast',
                'Pulikali - Tiger dance',
                'Kaikottikali - Group dance',
                'Vallamkali - Boat races',
                'Kathakali - Classical dance drama'
            ]
        })
        return context


def health_check(request):
    """
    Health check endpoint for monitoring.
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Onam app is running successfully!'
    })


def traditions_api(request):
    """
    API endpoint for Onam traditions.
    """
    traditions = [
        {
            'id': 1,
            'name': 'Pookalam',
            'description': 'Intricate floral patterns created in front of homes',
            'day': 'All 10 days of Onam',
            'significance': 'Welcomes King Mahabali'
        },
        {
            'id': 2,
            'name': 'Sadhya',
            'description': 'Grand vegetarian feast with multiple courses',
            'day': 'Thiruvonam (main day)',
            'significance': 'Celebration of abundance and prosperity'
        },
        {
            'id': 3,
            'name': 'Thiruvathira Kali',
            'description': 'Traditional dance performed by women',
            'day': 'Various days during Onam',
            'significance': 'Cultural expression and community bonding'
        },
        {
            'id': 4,
            'name': 'Pulikali',
            'description': 'Colorful tiger dance street performance',
            'day': 'Fourth day of Onam',
            'significance': 'Entertainment and cultural showcase'
        }
    ]
    
    return JsonResponse({
        'traditions': traditions,
        'total_count': len(traditions)
    })


# Events and Voting Views

class EventsListView(View):
    """View to display list of events"""
    
    def get(self, request):
        from .models import Event, EventParticipation
        
        player_id = request.session.get('player_id')
        player = None
        user_team = None
        
        if player_id:
            try:
                player = Player.objects.get(id=player_id)
                user_team = player.team if player.team != 'unassigned' else None
            except Player.DoesNotExist:
                pass
        
        events = Event.objects.filter(is_active=True).prefetch_related('eventparticipation_set')
        
        events_data = []
        for event in events:
            participating_teams = list(event.eventparticipation_set.values_list('team', flat=True))
            
            events_data.append({
                'event': event,
                'participating_teams': participating_teams,
                'user_team_participating': user_team in participating_teams if user_team else False,
                'can_vote': event.voting_enabled and user_team and user_team in participating_teams,
                'scores': event.average_scores if event.voting_enabled else {}
            })
        
        context = {
            'page_title': 'Onam Events - Team Competitions',
            'events_data': events_data,
            'player': player,
            'user_team': user_team,
        }
        
        return render(request, 'core/events_list.html', context)


class EventDetailView(View):
    """View to display event details and voting interface"""
    
    def get(self, request, event_id):
        from .models import Event, EventParticipation, EventVote
        
        event = get_object_or_404(Event, id=event_id, is_active=True)
        
        player_id = request.session.get('player_id')
        player = None
        user_team = None
        
        if player_id:
            try:
                player = Player.objects.get(id=player_id)
                user_team = player.team if player.team != 'unassigned' else None
            except Player.DoesNotExist:
                pass
        
        # Get participating teams
        participating_teams = list(event.eventparticipation_set.values_list('team', flat=True))
        
        # Check if user can vote
        can_vote = (event.voting_enabled and user_team and 
                   user_team in participating_teams)
        
        # Get teams user can vote for (all participating teams except their own)
        votable_teams = [team for team in participating_teams if team != user_team] if user_team else []
        
        # Get existing votes from user's team
        existing_votes = {}
        if user_team:
            votes = EventVote.objects.filter(event=event, voting_team=user_team)
            existing_votes = {vote.performing_team: vote for vote in votes}
        
        # Get average scores
        scores = event.average_scores
        
        context = {
            'page_title': f'{event.name} - Team Competition',
            'event': event,
            'player': player,
            'user_team': user_team,
            'participating_teams': participating_teams,
            'can_vote': can_vote,
            'votable_teams': votable_teams,
            'existing_votes': existing_votes,
            'scores': scores,
            'team_choices': dict(Player.TEAM_CHOICES)
        }
        
        return render(request, 'core/event_detail.html', context)
    
    def post(self, request, event_id):
        from .models import Event, EventVote
        
        event = get_object_or_404(Event, id=event_id, is_active=True, voting_enabled=True)
        
        player_id = request.session.get('player_id')
        if not player_id:
            messages.error(request, 'Please select a player first.')
            return redirect('core:select_player')
        
        try:
            player = Player.objects.get(id=player_id)
            user_team = player.team
            
            if user_team == 'unassigned':
                messages.error(request, 'You must be assigned to a team to vote.')
                return redirect('core:events_list')
            
        except Player.DoesNotExist:
            messages.error(request, 'Player not found.')
            return redirect('core:select_player')
        
        # Get form data
        performing_team = request.POST.get('performing_team')
        coordination_score = int(request.POST.get('coordination_score', 0))
        selection_score = int(request.POST.get('selection_score', 0))
        overall_score = int(request.POST.get('overall_score', 0))
        enjoyment_score = int(request.POST.get('enjoyment_score', 0))
        comments = request.POST.get('comments', '').strip()
        
        # Validate scores
        scores = [coordination_score, selection_score, overall_score, enjoyment_score]
        if any(score < 1 or score > 10 for score in scores):
            messages.error(request, 'All scores must be between 1 and 10.')
            return redirect('core:event_detail', event_id=event_id)
        
        # Validate teams
        if user_team == performing_team:
            messages.error(request, 'Teams cannot vote for themselves.')
            return redirect('core:event_detail', event_id=event_id)
        
        # Create or update vote
        vote, created = EventVote.objects.update_or_create(
            event=event,
            voting_team=user_team,
            performing_team=performing_team,
            defaults={
                'coordination_score': coordination_score,
                'selection_score': selection_score,
                'overall_score': overall_score,
                'enjoyment_score': enjoyment_score,
                'comments': comments,
            }
        )
        
        action = 'submitted' if created else 'updated'
        total_score = vote.total_score
        
        messages.success(request, 
            f'Vote {action} successfully! Total score: {total_score}/40 for {dict(Player.TEAM_CHOICES)[performing_team]}')
        
        return redirect('core:event_detail', event_id=event_id)


class EventVotingAPI(View):
    """API endpoint for real-time voting updates"""
    
    def get(self, request, event_id):
        from .models import Event
        
        try:
            event = get_object_or_404(Event, id=event_id, is_active=True)
            scores = event.average_scores
            
            # Format scores for display
            formatted_scores = {}
            for team, team_scores in scores.items():
                team_name = dict(Player.TEAM_CHOICES)[team]
                formatted_scores[team] = {
                    'name': team_name,
                    'coordination': team_scores['coordination'],
                    'selection': team_scores['selection'],
                    'overall': team_scores['overall'],
                    'enjoyment': team_scores['enjoyment'],
                    'total': team_scores['total']
                }
            
            return JsonResponse({
                'status': 'success',
                'scores': formatted_scores,
                'voting_enabled': event.voting_enabled
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
