from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.html import format_html
from django.db.models import Q
from .models import Player, GameSession, TreasureHuntQuestion, PlayerAnswer, Event, EventParticipation, EventVote, EventScore


class CustomAdminSite(admin.AdminSite):
    site_header = "Onam Aghosham - Thantha Vibe Admin"
    site_title = "Onam Aghosham Admin"
    index_title = "Welcome to Onam Aghosham - Thantha Vibe Administration"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve-answers/', self.admin_view(self.approve_answers_view), name='approve_answers'),
            path('bulk-upload-questions/', self.admin_view(self.bulk_upload_questions_view), name='bulk_upload_questions'),
            path('dashboard/', self.admin_view(self.dashboard_view), name='admin_dashboard'),
            path('approve-answer/<int:answer_id>/', self.admin_view(self.approve_single_answer), name='approve_single_answer'),
            path('manage-events/', self.admin_view(self.manage_events_view), name='manage_events'),
            path('event-scoring/<int:event_id>/', self.admin_view(self.event_scoring_view), name='event_scoring'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view"""
        pending_answers = PlayerAnswer.objects.filter(is_correct=False, points_awarded=0).count()
        total_questions = TreasureHuntQuestion.objects.filter(is_active=True).count()
        total_players = Player.objects.filter(is_active=True).count()
        online_players = Player.objects.filter(is_online=True).count()
        unassigned_players = Player.objects.filter(team='unassigned', is_active=True).count()
        
        # Team statistics
        team_stats = []
        for team_key, team_name in Player.TEAM_CHOICES:
            if team_key != 'unassigned':
                team_count = Player.objects.filter(team=team_key, is_active=True).count()
                team_online = Player.objects.filter(team=team_key, is_online=True).count()
                team_stats.append({
                    'name': team_name,
                    'total': team_count,
                    'online': team_online,
                })
        
        context = {
            'title': 'Admin Dashboard',
            'pending_answers': pending_answers,
            'total_questions': total_questions,
            'total_players': total_players,
            'online_players': online_players,
            'unassigned_players': unassigned_players,
            'team_stats': team_stats,
            'opts': self.model._meta if hasattr(self, 'model') else None,
        }
        return render(request, 'admin/custom_dashboard.html', context)
    
    def approve_answers_view(self, request):
        """View to approve player answers"""
        if request.method == 'POST':
            answer_id = request.POST.get('answer_id')
            action = request.POST.get('action')
            points = request.POST.get('points', 0)
            
            answer = get_object_or_404(PlayerAnswer, id=answer_id)
            
            if action == 'approve':
                answer.is_correct = True
                answer.points_awarded = int(points) if points else answer.question.points
                answer.save()
                
                # Update player score
                player = answer.player
                player.score += answer.points_awarded
                player.save()
                
                messages.success(request, f'Answer approved for {player.name}')
            elif action == 'reject':
                answer.is_correct = False
                answer.points_awarded = 0
                answer.save()
                messages.info(request, f'Answer rejected for {answer.player.name}')
        
        # Get pending answers (not yet approved/rejected)
        pending_answers = PlayerAnswer.objects.filter(
            Q(is_correct=False, points_awarded=0)
        ).select_related('player', 'question').order_by('-submitted_at')
        
        context = {
            'title': 'Approve Answers',
            'pending_answers': pending_answers,
            'opts': PlayerAnswer._meta,
        }
        return render(request, 'admin/approve_answers.html', context)
    
    def approve_single_answer(self, request, answer_id):
        """AJAX endpoint to approve single answer"""
        if request.method == 'POST':
            answer = get_object_or_404(PlayerAnswer, id=answer_id)
            action = request.POST.get('action')
            points = request.POST.get('points', answer.question.points)
            
            if action == 'approve':
                answer.is_correct = True
                answer.points_awarded = int(points)
                answer.save()
                
                # Update player score
                player = answer.player
                player.score += answer.points_awarded
                player.save()
                
                return JsonResponse({'status': 'success', 'message': 'Answer approved'})
            elif action == 'reject':
                answer.is_correct = False
                answer.points_awarded = 0
                answer.save()
                return JsonResponse({'status': 'success', 'message': 'Answer rejected'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    
    def bulk_upload_questions_view(self, request):
        """View to bulk upload questions"""
        if request.method == 'POST':
            # Handle form submission for adding questions
            question_text = request.POST.get('question_text')
            question_type = request.POST.get('question_type')
            points = request.POST.get('points', 10)
            order = request.POST.get('order')
            correct_answer = request.POST.get('correct_answer', '')
            
            # Handle multiple choice options
            option_a = request.POST.get('option_a', '')
            option_b = request.POST.get('option_b', '')
            option_c = request.POST.get('option_c', '')
            option_d = request.POST.get('option_d', '')
            
            if question_text and question_type:
                question = TreasureHuntQuestion.objects.create(
                    question_text=question_text,
                    question_type=question_type,
                    points=int(points),
                    order=int(order) if order else TreasureHuntQuestion.objects.count() + 1,
                    correct_answer=correct_answer,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                )
                messages.success(request, f'Question {question.order} added successfully')
                return redirect('admin:bulk_upload_questions')
        
        questions = TreasureHuntQuestion.objects.all().order_by('order')
        next_order = questions.count() + 1
        
        context = {
            'title': 'Manage Questions',
            'questions': questions,
            'next_order': next_order,
            'question_types': TreasureHuntQuestion.QUESTION_TYPES,
            'opts': TreasureHuntQuestion._meta,
        }
        return render(request, 'admin/bulk_upload_questions.html', context)
    
    def manage_events_view(self, request):
        """View to manage events and assign teams"""
        if request.method == 'POST':
            # Handle event creation
            if 'create_event' in request.POST:
                name = request.POST.get('name')
                event_type = request.POST.get('event_type')
                description = request.POST.get('description', '')
                voting_enabled = request.POST.get('voting_enabled') == 'on'
                
                if name and event_type:
                    event = Event.objects.create(
                        name=name,
                        event_type=event_type,
                        description=description,
                        voting_enabled=voting_enabled
                    )
                    messages.success(request, f'Event "{name}" created successfully')
                    return redirect('admin:manage_events')
            
            # Handle team participation
            elif 'add_participation' in request.POST:
                event_id = request.POST.get('event_id')
                team = request.POST.get('team')
                
                if event_id and team:
                    event = get_object_or_404(Event, id=event_id)
                    participation, created = EventParticipation.objects.get_or_create(
                        event=event,
                        team=team
                    )
                    if created:
                        messages.success(request, f'Team {participation.get_team_display()} added to {event.name}')
                    else:
                        messages.info(request, f'Team {participation.get_team_display()} already participating in {event.name}')
                    return redirect('admin:manage_events')
        
        events = Event.objects.all().order_by('-created_at')
        team_choices = Player.TEAM_CHOICES
        
        # Get participation data
        event_data = []
        for event in events:
            participations = EventParticipation.objects.filter(event=event)
            participating_teams = [p.team for p in participations]
            
            event_data.append({
                'event': event,
                'participations': participations,
                'participating_teams': participating_teams,
                'available_teams': [t for t in team_choices if t[0] not in participating_teams and t[0] != 'unassigned']
            })
        
        context = {
            'title': 'Manage Events',
            'event_data': event_data,
            'team_choices': team_choices,
            'event_types': Event.EVENT_TYPES,
            'opts': Event._meta,
        }
        return render(request, 'admin/manage_events.html', context)
    
    def event_scoring_view(self, request, event_id):
        """View to assign points to teams for specific event"""
        event = get_object_or_404(Event, id=event_id)
        
        if request.method == 'POST':
            team = request.POST.get('team')
            points = request.POST.get('points')
            notes = request.POST.get('notes', '')
            
            if team and points:
                try:
                    points = float(points)
                    score, created = EventScore.objects.get_or_create(
                        event=event,
                        team=team,
                        defaults={
                            'points': points,
                            'notes': notes,
                            'awarded_by': request.user.username
                        }
                    )
                    
                    if not created:
                        score.points = points
                        score.notes = notes
                        score.awarded_by = request.user.username
                        score.save()
                        messages.success(request, f'Updated score for {score.get_team_display()}: {points} points')
                    else:
                        messages.success(request, f'Awarded {points} points to {score.get_team_display()}')
                    
                    return redirect('admin:event_scoring', event_id=event_id)
                except ValueError:
                    messages.error(request, 'Please enter a valid number for points')
        
        # Get participating teams and their scores
        participations = EventParticipation.objects.filter(event=event)
        team_scores = {}
        
        for participation in participations:
            try:
                score = EventScore.objects.get(event=event, team=participation.team)
                team_scores[participation.team] = score
            except EventScore.DoesNotExist:
                team_scores[participation.team] = None
        
        # Get all teams for dropdown (in case admin wants to add score for non-participating team)
        all_teams = [(code, name) for code, name in Player.TEAM_CHOICES if code != 'unassigned']
        
        context = {
            'title': f'Event Scoring - {event.name}',
            'event': event,
            'team_scores': team_scores,
            'all_teams': all_teams,
            'opts': Event._meta,
        }
        return render(request, 'admin/event_scoring.html', context)
    
    class Media:
        js = ('js/admin_custom.js',)
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'question_type':
            kwargs['help_text'] = 'Select "Image Question (Text Answer)" if you want to upload an image that players will analyze.'
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'question_image':
            kwargs['help_text'] = 'Upload an image for image-based questions. Supported formats: JPG, PNG, GIF. Recommended size: 800x600px or larger.'
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Player, site=admin_site)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'get_online_status', 'score', 'current_level', 'is_active', 'created_at']
    list_filter = ['team', 'is_active', 'is_online', 'has_completed_hunt', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'last_activity', 'session_key']
    actions = ['activate_players', 'deactivate_players', 'reset_scores', 'assign_to_team_1', 'assign_to_team_2', 'assign_to_team_3', 'assign_to_team_4']
    
    def get_online_status(self, obj):
        if obj.is_online:
            return format_html('<span style="color: green;">🟢 Online</span>')
        else:
            return format_html('<span style="color: red;">⚫ Offline</span>')
    get_online_status.short_description = 'Status'
    
    def activate_players(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} players")
    activate_players.short_description = "Activate selected players"
    
    def deactivate_players(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} players")
    deactivate_players.short_description = "Deactivate selected players"
    
    def reset_scores(self, request, queryset):
        queryset.update(score=0, current_level=1, has_completed_hunt=False)
        self.message_user(request, f"Reset scores for {queryset.count()} players")
    reset_scores.short_description = "Reset scores for selected players"
    
    def assign_to_team_1(self, request, queryset):
        queryset.update(team='team_1')
        self.message_user(request, f"Assigned {queryset.count()} players to Team 1")
    assign_to_team_1.short_description = "Assign to Team 1"
    
    def assign_to_team_2(self, request, queryset):
        queryset.update(team='team_2')
        self.message_user(request, f"Assigned {queryset.count()} players to Team 2")
    assign_to_team_2.short_description = "Assign to Team 2"
    
    def assign_to_team_3(self, request, queryset):
        queryset.update(team='team_3')
        self.message_user(request, f"Assigned {queryset.count()} players to Team 3")
    assign_to_team_3.short_description = "Assign to Team 3"
    
    def assign_to_team_4(self, request, queryset):
        queryset.update(team='team_4')
        self.message_user(request, f"Assigned {queryset.count()} players to Team 4")
    assign_to_team_4.short_description = "Assign to Team 4"


@admin.register(GameSession, site=admin_site)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['player', 'level', 'completed', 'started_at', 'completed_at']
    list_filter = ['completed', 'level', 'started_at']
    search_fields = ['player__name']
    readonly_fields = ['started_at']


@admin.register(TreasureHuntQuestion, site=admin_site)
class TreasureHuntQuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'question_text_short', 'question_type', 'image_preview', 'points', 'is_active', 'answers_count']
    list_filter = ['question_type', 'is_active']
    search_fields = ['question_text']
    ordering = ['order']
    actions = ['activate_questions', 'deactivate_questions']
    
    # Use fieldsets for better organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('order', 'question_text', 'question_type', 'points', 'is_active')
        }),
        ('Question Image', {
            'fields': ('question_image', 'image_preview_large'),
            'description': 'Upload an image for image-based questions. The image will be displayed to players.',
            'classes': ('wide',),
        }),
        ('Multiple Choice Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'),
            'description': 'Only fill these fields for multiple choice questions.',
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['image_preview_large']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'
    
    def image_preview(self, obj):
        if obj.question_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;"/>', 
                obj.question_image.url
            )
        return format_html('<span style="color: #999;">No Image</span>')
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.question_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: contain; border: 1px solid #ddd; border-radius: 5px;"/>', 
                obj.question_image.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    image_preview_large.short_description = 'Image Preview'
    
    def answers_count(self, obj):
        return obj.playeranswer_set.count()
    answers_count.short_description = 'Answers Received'
    
    def activate_questions(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} questions")
    activate_questions.short_description = "Activate selected questions"
    
    def deactivate_questions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} questions")
    deactivate_questions.short_description = "Deactivate selected questions"
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.question_image:
            return readonly_fields
        else:
            # Don't show image preview for new objects without images
            return ['image_preview_large'] if 'image_preview_large' in readonly_fields else readonly_fields
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Add a success message when image is uploaded
        if obj.question_image and obj.question_type == 'image_text':
            self.message_user(request, f'Image question created successfully! Image: {obj.question_image.name}')
        elif obj.question_type == 'image_text' and not obj.question_image:
            self.message_user(request, 'Note: This is an image question but no image was uploaded. Consider adding an image.', level='warning')


@admin.register(PlayerAnswer, site=admin_site)
class PlayerAnswerAdmin(admin.ModelAdmin):
    list_display = ['player', 'question_order', 'answer_preview', 'approval_status', 'points_awarded', 'submitted_at', 'action_buttons']
    list_filter = ['is_correct', 'submitted_at', 'question__question_type']
    search_fields = ['player__name', 'question__question_text', 'text_answer']
    readonly_fields = ['submitted_at']
    actions = ['approve_answers', 'reject_answers']
    
    def question_order(self, obj):
        return f"Q{obj.question.order}"
    question_order.short_description = 'Question'
    
    def answer_preview(self, obj):
        if obj.text_answer:
            preview = obj.text_answer[:50] + "..." if len(obj.text_answer) > 50 else obj.text_answer
            return preview
        elif obj.photo_answer:
            return format_html('<a href="{}" target="_blank">View Photo</a>', obj.photo_answer.url)
        return "No answer"
    answer_preview.short_description = 'Answer'
    
    def approval_status(self, obj):
        if obj.is_correct:
            return format_html('<span style="color: green;">✓ Approved</span>')
        elif obj.points_awarded == 0:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
        else:
            return format_html('<span style="color: red;">✗ Rejected</span>')
    approval_status.short_description = 'Status'
    
    def action_buttons(self, obj):
        """Action buttons for approving/rejecting answers - only available in custom admin"""
        if not obj.is_correct and obj.points_awarded == 0:
            return format_html(
                '<span style="color: orange;">Pending Review</span>'
            )
        elif obj.is_correct:
            return format_html('<span style="color: green;">✓ Approved</span>')
        else:
            return format_html('<span style="color: red;">✗ Rejected</span>')
    action_buttons.short_description = 'Status'
    
    def approve_answers(self, request, queryset):
        for answer in queryset:
            if not answer.is_correct:
                answer.is_correct = True
                answer.points_awarded = answer.question.points
                answer.save()
                # Update player score
                answer.player.score += answer.points_awarded
                answer.player.save()
        self.message_user(request, f"Approved {queryset.count()} answers")
    approve_answers.short_description = "Approve selected answers"
    
    def reject_answers(self, request, queryset):
        queryset.update(is_correct=False, points_awarded=0)
        self.message_user(request, f"Rejected {queryset.count()} answers")
    reject_answers.short_description = "Reject selected answers"


@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'is_active', 'voting_enabled', 'participating_teams_count', 'total_votes']
    list_filter = ['event_type', 'is_active', 'voting_enabled']
    search_fields = ['name', 'description']
    ordering = ['name']
    actions = ['enable_voting', 'disable_voting', 'activate_events', 'deactivate_events']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'event_type', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'voting_enabled'),
            'description': 'Enable voting when teams are ready to vote for each other.'
        }),
    )
    
    def participating_teams_count(self, obj):
        return obj.eventparticipation_set.count()
    participating_teams_count.short_description = 'Teams Participating'
    
    def total_votes(self, obj):
        return obj.eventvote_set.count()
    total_votes.short_description = 'Total Votes Received'
    
    def enable_voting(self, request, queryset):
        queryset.update(voting_enabled=True)
        self.message_user(request, f"Enabled voting for {queryset.count()} events")
    enable_voting.short_description = "Enable voting for selected events"
    
    def disable_voting(self, request, queryset):
        queryset.update(voting_enabled=False)
        self.message_user(request, f"Disabled voting for {queryset.count()} events")
    disable_voting.short_description = "Disable voting for selected events"
    
    def activate_events(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} events")
    activate_events.short_description = "Activate selected events"
    
    def deactivate_events(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} events")
    deactivate_events.short_description = "Deactivate selected events"


@admin.register(EventParticipation, site=admin_site)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ['event', 'team', 'registered_at']
    list_filter = ['event', 'team', 'registered_at']
    search_fields = ['event__name']
    ordering = ['event', 'team']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'team' in form.base_fields:
            form.base_fields['team'].help_text = 'Select which team is participating in this event'
        return form


@admin.register(EventVote, site=admin_site)
class EventVoteAdmin(admin.ModelAdmin):
    list_display = ['event', 'voting_team', 'performing_team', 'coordination_score', 'selection_score', 
                   'overall_score', 'enjoyment_score', 'total_score_display', 'voted_at']
    list_filter = ['event', 'voting_team', 'performing_team', 'voted_at']
    search_fields = ['event__name', 'comments']
    ordering = ['-voted_at']
    readonly_fields = ['total_score_display', 'average_score_display', 'voted_at']
    
    fieldsets = (
        ('Vote Information', {
            'fields': ('event', 'voting_team', 'performing_team')
        }),
        ('Scores (1-10 scale)', {
            'fields': ('coordination_score', 'selection_score', 'overall_score', 'enjoyment_score'),
            'description': 'Rate each criteria from 1 (poor) to 10 (excellent)'
        }),
        ('Additional Information', {
            'fields': ('comments', 'total_score_display', 'average_score_display'),
            'classes': ('collapse',)
        }),
    )
    
    def total_score_display(self, obj):
        if obj.pk:
            return f"{obj.total_score}/40"
        return "-"
    total_score_display.short_description = 'Total Score'
    
    def average_score_display(self, obj):
        if obj.pk:
            return f"{obj.average_score:.2f}/10"
        return "-"
    average_score_display.short_description = 'Average Score'
    
    def save_model(self, request, obj, form, change):
        # Validate scores are between 1-10
        for field in ['coordination_score', 'selection_score', 'overall_score', 'enjoyment_score']:
            score = getattr(obj, field)
            if score < 1 or score > 10:
                messages.error(request, f"{field.replace('_', ' ').title()} must be between 1 and 10")
                return
        
        super().save_model(request, obj, form, change)
        messages.success(request, f"Vote saved successfully! Total score: {obj.total_score}/40")


@admin.register(EventScore, site=admin_site)
class EventScoreAdmin(admin.ModelAdmin):
    list_display = ['event', 'team', 'points', 'awarded_by', 'awarded_at', 'notes_preview']
    list_filter = ['event', 'team', 'awarded_at']
    search_fields = ['event__name', 'notes', 'awarded_by']
    ordering = ['-awarded_at', 'event', '-points']
    readonly_fields = ['awarded_at']
    
    fieldsets = (
        ('Score Information', {
            'fields': ('event', 'team', 'points')
        }),
        ('Additional Details', {
            'fields': ('notes', 'awarded_by'),
            'description': 'Optional notes about the scoring decision'
        }),
    )
    
    def notes_preview(self, obj):
        if obj.notes:
            return obj.notes[:50] + "..." if len(obj.notes) > 50 else obj.notes
        return "No notes"
    notes_preview.short_description = 'Notes'
    
    def save_model(self, request, obj, form, change):
        if not obj.awarded_by:
            obj.awarded_by = request.user.username
        super().save_model(request, obj, form, change)
        messages.success(request, f"Score awarded: {obj.points} points to {obj.get_team_display()} for {obj.event.name}")


# Register with default admin as well for compatibility
admin.site.register(Player, PlayerAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(TreasureHuntQuestion, TreasureHuntQuestionAdmin)
admin.site.register(PlayerAnswer, PlayerAnswerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipation, EventParticipationAdmin)
admin.site.register(EventVote, EventVoteAdmin)
admin.site.register(EventScore, EventScoreAdmin)