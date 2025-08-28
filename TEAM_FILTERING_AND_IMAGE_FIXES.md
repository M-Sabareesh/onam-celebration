# Team Filtering & Image Display Fixes

## Summary of Issues Fixed

### 1. Team Event Participations Player Filtering ✅
**Problem:** When selecting a team in "Add event score" under Score Information, the player dropdown in "Team event participations" showed all players instead of only players from the selected team.

**Solution Implemented:**
- Added JavaScript (`static/js/admin_team_filter.js`) to dynamically filter players
- Created AJAX endpoint (`/admin/get-team-players/`) to fetch team-specific players
- Updated `EventScoreAdmin` to include the JavaScript file
- Players dropdown now filters automatically when team changes

### 2. Treasure Hunt Images Not Displaying ✅  
**Problem:** Images uploaded as part of treasure hunt questions were not displaying in the UI when players viewed questions.

**Solution Implemented:**
- Updated production settings to properly serve media files
- Configured whitenoise to handle media files in production
- Added explicit media URL patterns for both development and production
- Images are now saved to filesystem (`media/question_images/`) and served correctly

## Technical Details

### Team Filtering Implementation

#### JavaScript Filter (`static/js/admin_team_filter.js`)
- Monitors team selection changes in EventScore admin
- Makes AJAX calls to fetch filtered player list
- Updates all player dropdowns in TeamEventParticipation inlines
- Handles dynamically added inline forms

#### AJAX Endpoint (`apps/core/views.py`)
```python
@staff_member_required
@require_POST  
@csrf_protect
def get_team_players(request):
    # Returns JSON list of players for selected team
```

#### Admin Configuration (`apps/core/admin.py`)
```python
class EventScoreAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_team_filter.js',)
```

### Image Display Implementation

#### Media Files Configuration
**Production Settings (`onam_project/settings/production.py`):**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
WHITENOISE_ROOT = MEDIA_ROOT
```

**URL Configuration (`onam_project/urls.py`):**
```python
# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### Model Configuration (`apps/core/models.py`)
```python
class TreasureHuntQuestion(models.Model):
    question_image = models.ImageField(
        upload_to='question_images/', 
        blank=True, 
        null=True
    )
```

## How to Use

### Team-Based Event Scoring
1. Go to Admin → Event Scores → Add Event Score
2. Select an event and team in "Score Information"
3. In "Team event participations" section, click "Add another Team event participation"
4. The player dropdown will now show only players from the selected team
5. Players are filtered automatically when you change the team selection

### Treasure Hunt with Images
1. Go to Admin → Treasure Hunt Questions → Add/Edit Question
2. Upload an image in the "Question Image" section
3. Image preview will show in admin interface
4. Players will see the image when answering the question
5. Images are stored in `media/question_images/` directory

## Files Modified

### New Files Created:
- `static/js/admin_team_filter.js` - Dynamic player filtering
- `test_both_fixes.py` - Verification script

### Files Modified:
- `apps/core/admin.py` - Added JavaScript to EventScoreAdmin
- `apps/core/views.py` - Added get_team_players AJAX endpoint
- `apps/core/urls.py` - Added AJAX endpoint URL
- `onam_project/settings/production.py` - Media files configuration
- `onam_project/urls.py` - Media URL patterns

## Testing

Run the verification script:
```bash
python test_both_fixes.py
```

### Manual Testing

#### Team Filtering:
1. Access admin interface: `/admin/` or `/custom-admin/`
2. Go to Core → Event Scores → Add Event Score
3. Select a team, then add team event participations
4. Verify player dropdown shows only team members

#### Image Display:
1. Upload an image in Treasure Hunt Questions admin
2. View the question as a player via `/treasure-hunt/`
3. Verify image displays correctly in both admin and player interface

## Troubleshooting

### Team Filtering Issues:
- Check browser console for JavaScript errors
- Verify AJAX endpoint returns player data: `POST /admin/get-team-players/`
- Ensure admin user has proper permissions

### Image Display Issues:
- Check media directory exists: `ls media/question_images/`
- Verify MEDIA_URL is accessible: `/media/question_images/filename.jpg`
- Check file permissions and whitenoise configuration
- For production: ensure media files are uploaded to server

## Production Deployment

Both fixes are production-ready:
- Team filtering works via JavaScript and AJAX
- Image serving is configured for production via whitenoise
- No database schema changes required
- Backward compatible with existing data

Deploy normally and both features will work immediately.
