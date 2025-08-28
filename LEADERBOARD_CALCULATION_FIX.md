# 🔧 LEADERBOARD CALCULATION FIX

## ❌ **ISSUE IDENTIFIED**
The leaderboard was incorrectly double-counting team event scores in the "Chodya Onam" section.

### Problem Description:
The `player.score` field already includes:
- ✅ Treasure hunt points (Chodya Onam)
- ✅ Individual event scores  
- ✅ Team event contributions (calculated in `EventScore.update_single_player_score()`)

However, the `LeaderboardView` was using `player.score` for "Chodya Onam" calculation, then **adding team event scores again**, causing double-counting:

```python
# WRONG - Double counting team events
team_data[team]['treasure_hunt_score'] += player.score  # Includes team events
team_data[team_code]['total_score'] = (
    team_data[team_code]['treasure_hunt_score'] +  # Already has team events
    team_data[team_code]['total_event_score'] +    # Adding team events AGAIN!
    team_data[team_code]['individual_event_score']
)
```

## ✅ **FIX APPLIED**

### Updated LeaderboardView Logic:
**File**: `apps/core/views.py` (Line ~259)

```python
# FIXED - Only count pure Chodya Onam scores
for player in Player.objects.all():
    team = player.team
    if team in team_data:
        # Get ONLY treasure hunt score (not total player.score which includes team events)
        treasure_hunt_only = PlayerAnswer.objects.filter(
            player=player, 
            is_correct=True
        ).aggregate(Sum('points_awarded'))['points_awarded__sum'] or 0
        
        team_data[team]['treasure_hunt_score'] += treasure_hunt_only
        team_data[team]['players'].append(player)
```

### What Changed:
1. **Before**: Used `player.score` (includes team events) for Chodya Onam
2. **After**: Calculate pure treasure hunt score from `PlayerAnswer` model
3. **Result**: Proper separation between Chodya Onam and team event scores

## 📊 **LEADERBOARD SECTIONS NOW CORRECTLY SHOW**

### 🎯 Chodya Onam Scores
- **Only treasure hunt/question points**
- Calculated from `PlayerAnswer.points_awarded` where `is_correct=True`
- No team event contamination

### 🎪 Team Event Scores  
- **Only scores from team events (voting + admin awarded)**
- Calculated from `Event.average_scores`
- No double-counting with Chodya Onam

### 👤 Individual Event Scores
- **Only individual event contributions to team**
- Calculated from `IndividualEventScore.team_points`
- Separate from both above categories

### 📈 Total Team Score
```
Total = Chodya Onam + Team Events + Individual Events
```
Each component is now properly isolated and accurate.

## 🧪 **TESTING**

### Test Script: `test_leaderboard_calculation_fix.py`
Verifies:
- ✅ Chodya Onam shows only treasure hunt points
- ✅ No double-counting of team event scores  
- ✅ Accurate total calculations
- ✅ Proper score separation across all teams

### Manual Testing:
1. **Navigate to `/leaderboard/`**
2. **Check "Team Standings" section**:
   - "Chodya Onam" should show only question/treasure hunt points
   - "Events" should show only team event scores
   - Total should be sum of separate components
3. **Verify no inflated scores** compared to previous version

## 📁 **FILES MODIFIED**

1. **`apps/core/views.py`**:
   - Updated `LeaderboardView.get_context_data()`
   - Added proper Chodya Onam calculation
   - Added `PlayerAnswer` import

2. **`test_leaderboard_calculation_fix.py`**:
   - Comprehensive testing script
   - Validates fix correctness

## 🚀 **DEPLOYMENT**

### No Migration Required
This is a view logic fix only - no database changes needed.

### Steps:
1. **Deploy updated code**
2. **Test leaderboard immediately** 
3. **Verify Chodya Onam scores are lower** (correct behavior)
4. **Confirm team event scores remain accurate**

## ✅ **EXPECTED RESULTS**

After the fix:
- **Chodya Onam sections show realistic point values** (only treasure hunt)
- **Team event scores remain accurate** but separate
- **Total scores are correct** without double-counting
- **Leaderboard rankings may change** (due to corrected calculations)

---

**Status**: 🟢 **FIXED AND READY FOR DEPLOYMENT**  
**Issue**: Double-counting of team event scores in Chodya Onam section  
**Solution**: Separate calculation of pure treasure hunt scores  
**Impact**: More accurate leaderboard with proper score attribution
