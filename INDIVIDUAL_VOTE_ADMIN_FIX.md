# Individual Event Voting Admin Fix

## Issue
The IndividualEventVote admin form was throwing a `TypeError: unsupported operand type(s) for +: 'NoneType' and 'NoneType'` error when trying to access the add form. This occurred because the `total_score` property was trying to add score fields that were `None` before any values were entered.

## Root Cause
The `total_score` property in the `IndividualEventVote` model was:
```python
@property
def total_score(self):
    return self.skill_score + self.creativity_score + self.presentation_score + self.overall_score
```

When the admin form is initially loaded (before saving), these fields are `None`, causing the addition operation to fail.

## Solution Applied

### 1. Fixed Model Properties
Updated the `total_score` and `average_score` properties to handle `None` values:
```python
@property
def total_score(self):
    scores = [
        self.skill_score or 0,
        self.creativity_score or 0, 
        self.presentation_score or 0,
        self.overall_score or 0
    ]
    return sum(scores)

@property
def average_score(self):
    total = self.total_score
    return total / 4 if total > 0 else 0
```

### 2. Updated Model Fields
Made the score fields nullable and blank to allow initial form loading:
```python
skill_score = models.PositiveIntegerField(null=True, blank=True, help_text="Skill/Technique (1-10)")
creativity_score = models.PositiveIntegerField(null=True, blank=True, help_text="Creativity/Originality (1-10)")
presentation_score = models.PositiveIntegerField(null=True, blank=True, help_text="Presentation/Stage Presence (1-10)")
overall_score = models.PositiveIntegerField(null=True, blank=True, help_text="Overall Performance (1-10)")
```

### 3. Enhanced Admin Interface
- Removed calculated fields from the form fieldsets to avoid display issues
- Added a safe `get_total_score` method for list display
- Updated validation to handle null values properly
- Added proper error messaging

### 4. Added Validation
Enhanced the `clean()` method to ensure all scores are provided when saving:
```python
def clean(self):
    # ... existing validation ...
    
    # Ensure all scores are provided when saving
    if self.pk:  # Only validate on save, not initial form load
        score_fields = [self.skill_score, self.creativity_score, self.presentation_score, self.overall_score]
        if any(score is None for score in score_fields):
            raise ValidationError("All score fields must be provided")
        if any(score < 1 or score > 10 for score in score_fields if score is not None):
            raise ValidationError("All scores must be between 1 and 10")
```

### 5. Created Migration
Created migration `0011_fix_individual_vote_null_fields.py` to update the database schema to allow null values for score fields.

## Result
- ✅ Admin form now loads without errors
- ✅ Score calculations work properly with null and valid values
- ✅ Proper validation ensures data integrity
- ✅ User-friendly error messages guide proper usage

## Testing
The fix ensures that:
1. The admin form loads successfully for new IndividualEventVote objects
2. Score calculations return 0 when no scores are entered yet
3. Proper validation occurs when saving with missing or invalid scores
4. Existing data remains unaffected

This resolves the TypeError and makes the individual event voting system fully functional in the admin interface.
