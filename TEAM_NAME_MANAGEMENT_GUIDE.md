# Team Name Management Guide 👥

## Current Team Structure
Your system currently has these teams defined in `apps/core/models.py`:

```python
TEAM_CHOICES = [
    ('team_1', 'Team 1'),
    ('team_2', 'Team 2'),
    ('team_3', 'Team 3'),
    ('team_4', 'Team 4'),
    ('unassigned', 'Unassigned'),
]
```

## 🎯 How to Update Team Names

### Option 1: Update in Models.py (Recommended)
This changes the team names throughout the entire system.

**Step 1**: Edit `apps/core/models.py`
```python
TEAM_CHOICES = [
    ('team_1', 'Malapuram Team'),           # Kerala district
    ('team_2', 'Ernakulam Team'),          # Kerala district  
    ('team_3', 'Thiruvananthapuram Team'), # Kerala capital
    ('team_4', 'Kozhikode Team'),          # Kerala district
    ('unassigned', 'Unassigned'),
]
```

**Step 2**: Create and run migration
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 3**: Update the color mapping in `apps/core/views.py`
```python
# Enhanced team colors - update comments to match new names
team_colors = {
    'team_1': '#E53E3E',        # Bright Red - Malapuram
    'team_2': '#3182CE',        # Blue - Ernakulam
    'team_3': '#D69E2E',        # Golden Orange - Thiruvananthapuram
    'team_4': '#38A169',        # Green - Kozhikode
    'unassigned': '#805AD5'     # Purple
}
```

### Option 2: Admin Panel Display Override
If you want to keep the database codes but change display names in admin only.

**Step 1**: Update `apps/core/admin.py`
```python
from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_team_display', 'score', 'is_active', 'created_at')
    list_filter = ('team', 'is_active', 'has_completed_hunt')
    search_fields = ('name',)
    
    # Custom team display
    def get_team_display(self, obj):
        team_display_names = {
            'team_1': 'Malapuram Warriors',
            'team_2': 'Ernakulam Champions', 
            'team_3': 'Thiruvananthapuram Tigers',
            'team_4': 'Kozhikode Knights',
            'unassigned': 'Unassigned Players'
        }
        return team_display_names.get(obj.team, obj.get_team_display())
    get_team_display.short_description = 'Team'
```

## 🎨 Update Chart Colors After Name Change

After updating team names, also update the color mapping comments:

**In `apps/core/views.py`**:
```python
def get_team_progress_data(self, team_data):
    """Generate chart data for team progress by events"""
    import json
    
    # Enhanced team colors - updated for new team names
    team_colors = {
        'team_1': '#E53E3E',        # Bright Red - Malapuram Warriors
        'team_2': '#3182CE',        # Blue - Ernakulam Champions
        'team_3': '#D69E2E',        # Golden Orange - Thiruvananthapuram Tigers
        'team_4': '#38A169',        # Green - Kozhikode Knights
        'unassigned': '#805AD5'     # Purple - Unassigned
    }
    
    # Secondary colors for borders/highlights
    team_border_colors = {
        'team_1': '#C53030',        # Darker Red
        'team_2': '#2C5282',        # Darker Blue  
        'team_3': '#B7791F',        # Darker Orange
        'team_4': '#2F855A',        # Darker Green
        'unassigned': '#6B46C1'     # Darker Purple
    }
    # ... rest of the method
```

## 🏆 Suggested Team Names for Onam Celebration

### Kerala Districts Theme:
```python
TEAM_CHOICES = [
    ('team_1', 'Thiruvananthapuram Tigers'),   # Capital city
    ('team_2', 'Kochi Champions'),             # Commercial hub
    ('team_3', 'Kozhikode Warriors'),          # Historic port city
    ('team_4', 'Thrissur Legends'),           # Cultural capital
    ('unassigned', 'Unassigned'),
]
```

### Onam Festival Theme:
```python
TEAM_CHOICES = [
    ('team_1', 'Maveli Warriors'),             # King Mahabali
    ('team_2', 'Pookalam Artists'),           # Flower carpet
    ('team_3', 'Pulikali Dancers'),           # Tiger dance
    ('team_4', 'Sadya Champions'),            # Feast experts
    ('unassigned', 'Unassigned'),
]
```

### Kerala Culture Theme:
```python
TEAM_CHOICES = [
    ('team_1', 'Kathakali Masters'),          # Classical dance
    ('team_2', 'Mohiniyattam Artists'),      # Classical dance
    ('team_3', 'Theyyam Performers'),        # Ritual art
    ('team_4', 'Kalaripayattu Warriors'),    # Martial arts
    ('unassigned', 'Unassigned'),
]
```

## 📝 Step-by-Step Implementation

### For Kerala Districts Theme:

**1. Update models.py**:
```python
TEAM_CHOICES = [
    ('team_1', 'Thiruvananthapuram Tigers'),
    ('team_2', 'Kochi Champions'),
    ('team_3', 'Kozhikode Warriors'),
    ('team_4', 'Thrissur Legends'),
    ('unassigned', 'Unassigned'),
]
```

**2. Run migrations**:
```bash
python manage.py makemigrations core
python manage.py migrate
```

**3. Update color comments in views.py**:
```python
team_colors = {
    'team_1': '#E53E3E',        # Bright Red - Thiruvananthapuram Tigers
    'team_2': '#3182CE',        # Blue - Kochi Champions
    'team_3': '#D69E2E',        # Golden Orange - Kozhikode Warriors
    'team_4': '#38A169',        # Green - Thrissur Legends
    'unassigned': '#805AD5'     # Purple - Unassigned
}
```

**4. Test the changes**:
- Visit admin panel: `/admin/core/player/`
- Check leaderboard: `/leaderboard/`
- Verify chart shows new team names with correct colors

## 🚨 Important Notes

1. **Database Impact**: Changing TEAM_CHOICES requires migration
2. **Existing Data**: Current player team assignments will remain unchanged
3. **Chart Colors**: Colors are mapped by team code (team_1, team_2, etc.), not names
4. **Admin Panel**: Team names will update automatically after migration
5. **Templates**: Team names will show the new display names throughout the site

## ✅ Verification Checklist

After updating team names:

- [ ] Migration completed successfully
- [ ] Admin panel shows new team names
- [ ] Leaderboard displays new team names
- [ ] Chart legend shows new team names
- [ ] Chart colors remain distinct for each team
- [ ] No JavaScript errors in browser console
- [ ] Player assignment still works correctly

---

Choose your preferred team naming theme and follow the steps above to implement it! 🎯🏆
