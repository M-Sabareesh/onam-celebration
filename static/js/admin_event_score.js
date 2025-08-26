/**
 * Enhanced admin interface for Team Event Participation
 * Provides better UX for selecting participants and calculating points
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeEventScoreEnhancements();
    });

    function initializeEventScoreEnhancements() {
        // Only run on EventScore admin pages
        if (!isEventScoreAdminPage()) {
            return;
        }

        // Initialize features
        addSelectAllParticipantsButton();
        addParticipationCounter();
        addAutoCalculationToggle();
        addQuickParticipationStats();
    }

    function isEventScoreAdminPage() {
        return window.location.pathname.includes('eventscore/') ||
               document.querySelector('[name="auto_calculate_points"]') !== null;
    }

    function addSelectAllParticipantsButton() {
        const participationSection = document.querySelector('#teamEventParticipation_set-group');
        if (!participationSection) return;

        // Create control buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'participation-controls';
        buttonContainer.style.cssText = 'margin-bottom: 10px; padding: 10px; background: #f8f9fa; border-radius: 4px;';

        buttonContainer.innerHTML = `
            <div style="display: flex; gap: 10px; align-items: center;">
                <strong>Quick Actions:</strong>
                <button type="button" id="select-all-participants" class="btn btn-sm btn-outline-primary">
                    ✓ Select All
                </button>
                <button type="button" id="deselect-all-participants" class="btn btn-sm btn-outline-secondary">
                    ✗ Deselect All
                </button>
                <button type="button" id="toggle-all-participants" class="btn btn-sm btn-outline-info">
                    ⇄ Toggle All
                </button>
                <span id="participation-counter" style="margin-left: auto; font-weight: bold; color: #0066cc;">
                    0 participants selected
                </span>
            </div>
        `;

        // Insert before the participation inline forms
        const inlineGroup = participationSection.querySelector('.inline-group');
        if (inlineGroup) {
            participationSection.insertBefore(buttonContainer, inlineGroup);
        }

        // Add event listeners
        document.getElementById('select-all-participants').addEventListener('click', function() {
            setAllParticipation(true);
            updateParticipationCounter();
            updateAutoCalculatedPoints();
        });

        document.getElementById('deselect-all-participants').addEventListener('click', function() {
            setAllParticipation(false);
            updateParticipationCounter();
            updateAutoCalculatedPoints();
        });

        document.getElementById('toggle-all-participants').addEventListener('click', function() {
            toggleAllParticipation();
            updateParticipationCounter();
            updateAutoCalculatedPoints();
        });
    }

    function setAllParticipation(participated) {
        const checkboxes = document.querySelectorAll('[name*="participated"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = participated;
        });
    }

    function toggleAllParticipation() {
        const checkboxes = document.querySelectorAll('[name*="participated"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = !checkbox.checked;
        });
    }

    function addParticipationCounter() {
        // Add change listeners to all participation checkboxes
        const checkboxes = document.querySelectorAll('[name*="participated"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                updateParticipationCounter();
                updateAutoCalculatedPoints();
            });
        });

        // Initial count
        updateParticipationCounter();
    }

    function updateParticipationCounter() {
        const counter = document.getElementById('participation-counter');
        if (!counter) return;

        const checkboxes = document.querySelectorAll('[name*="participated"]');
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        const totalCount = checkboxes.length;

        counter.textContent = `${checkedCount} of ${totalCount} participants selected`;
        
        // Update counter color based on participation rate
        const rate = totalCount > 0 ? checkedCount / totalCount : 0;
        if (rate === 1) {
            counter.style.color = '#28a745'; // Green for 100%
        } else if (rate >= 0.75) {
            counter.style.color = '#17a2b8'; // Blue for 75%+
        } else if (rate >= 0.5) {
            counter.style.color = '#ffc107'; // Yellow for 50%+
        } else {
            counter.style.color = '#dc3545'; // Red for <50%
        }
    }

    function addAutoCalculationToggle() {
        const autoCalcCheckbox = document.querySelector('[name="auto_calculate_points"]');
        const pointsField = document.querySelector('[name="points"]');
        const pointsPerParticipantField = document.querySelector('[name="points_per_participant"]');

        if (!autoCalcCheckbox || !pointsField || !pointsPerParticipantField) return;

        // Add change listener to auto-calculation checkbox
        autoCalcCheckbox.addEventListener('change', function() {
            toggleCalculationMode();
            updateAutoCalculatedPoints();
        });

        // Add change listener to points per participant
        pointsPerParticipantField.addEventListener('input', function() {
            updateAutoCalculatedPoints();
        });

        // Initial setup
        toggleCalculationMode();
    }

    function toggleCalculationMode() {
        const autoCalcCheckbox = document.querySelector('[name="auto_calculate_points"]');
        const pointsField = document.querySelector('[name="points"]');
        const pointsPerParticipantField = document.querySelector('[name="points_per_participant"]');

        if (!autoCalcCheckbox || !pointsField || !pointsPerParticipantField) return;

        const isAutoMode = autoCalcCheckbox.checked;

        // Toggle field states
        pointsField.readOnly = isAutoMode;
        pointsPerParticipantField.readOnly = !isAutoMode;

        // Visual feedback
        pointsField.style.backgroundColor = isAutoMode ? '#f8f9fa' : '';
        pointsPerParticipantField.style.backgroundColor = isAutoMode ? '' : '#f8f9fa';

        // Add help text
        updateCalculationHelpText(isAutoMode);
    }

    function updateCalculationHelpText(isAutoMode) {
        // Remove existing help text
        const existingHelp = document.getElementById('calculation-mode-help');
        if (existingHelp) {
            existingHelp.remove();
        }

        const pointsField = document.querySelector('[name="points"]');
        if (!pointsField) return;

        // Add new help text
        const helpDiv = document.createElement('div');
        helpDiv.id = 'calculation-mode-help';
        helpDiv.style.cssText = 'margin-top: 5px; padding: 8px; border-radius: 4px; font-size: 12px;';

        if (isAutoMode) {
            helpDiv.style.backgroundColor = '#d1ecf1';
            helpDiv.style.color = '#0c5460';
            helpDiv.innerHTML = '🤖 <strong>Auto-calculation enabled:</strong> Points will be calculated as (Participants × Points per participant)';
        } else {
            helpDiv.style.backgroundColor = '#f8d7da';
            helpDiv.style.color = '#721c24';
            helpDiv.innerHTML = '✋ <strong>Manual mode:</strong> Enter fixed points regardless of participant count';
        }

        pointsField.parentNode.appendChild(helpDiv);
    }

    function updateAutoCalculatedPoints() {
        const autoCalcCheckbox = document.querySelector('[name="auto_calculate_points"]');
        const pointsField = document.querySelector('[name="points"]');
        const pointsPerParticipantField = document.querySelector('[name="points_per_participant"]');

        if (!autoCalcCheckbox || !pointsField || !pointsPerParticipantField) return;

        if (!autoCalcCheckbox.checked) return;

        // Calculate points based on participation
        const participantCount = getSelectedParticipantCount();
        const pointsPerParticipant = parseFloat(pointsPerParticipantField.value) || 0;
        const calculatedPoints = participantCount * pointsPerParticipant;

        pointsField.value = calculatedPoints.toFixed(2);

        // Show calculation preview
        showCalculationPreview(participantCount, pointsPerParticipant, calculatedPoints);
    }

    function getSelectedParticipantCount() {
        const checkboxes = document.querySelectorAll('[name*="participated"]');
        return Array.from(checkboxes).filter(cb => cb.checked).length;
    }

    function showCalculationPreview(participants, pointsPerParticipant, total) {
        // Remove existing preview
        const existingPreview = document.getElementById('calculation-preview');
        if (existingPreview) {
            existingPreview.remove();
        }

        const pointsField = document.querySelector('[name="points"]');
        if (!pointsField) return;

        // Add calculation preview
        const previewDiv = document.createElement('div');
        previewDiv.id = 'calculation-preview';
        previewDiv.style.cssText = 'margin-top: 5px; padding: 6px 10px; background: #d4edda; color: #155724; border-radius: 4px; font-size: 12px; font-family: monospace;';
        previewDiv.innerHTML = `📊 Calculation: ${participants} participants × ${pointsPerParticipant} points = <strong>${total.toFixed(2)} total points</strong>`;

        pointsField.parentNode.appendChild(previewDiv);
    }

    function addQuickParticipationStats() {
        // Add a stats section to show participation overview
        const form = document.querySelector('form');
        if (!form) return;

        const statsContainer = document.createElement('div');
        statsContainer.id = 'participation-stats';
        statsContainer.style.cssText = 'position: fixed; top: 10px; right: 10px; background: white; border: 1px solid #ddd; border-radius: 6px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1000; max-width: 250px;';
        
        statsContainer.innerHTML = `
            <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #333;">📊 Participation Stats</h4>
            <div id="stats-content">
                <div id="participant-count-stat">Participants: -</div>
                <div id="participation-rate-stat">Rate: -</div>
                <div id="calculated-points-stat">Points: -</div>
            </div>
            <button type="button" id="hide-stats" style="margin-top: 10px; font-size: 11px; padding: 2px 6px;">Hide</button>
        `;

        document.body.appendChild(statsContainer);

        // Add hide functionality
        document.getElementById('hide-stats').addEventListener('click', function() {
            statsContainer.style.display = 'none';
        });

        // Update stats regularly
        setInterval(updateParticipationStats, 1000);
        updateParticipationStats(); // Initial update
    }

    function updateParticipationStats() {
        const statsContent = document.getElementById('stats-content');
        if (!statsContent) return;

        const participantCount = getSelectedParticipantCount();
        const totalPlayers = document.querySelectorAll('[name*="participated"]').length;
        const rate = totalPlayers > 0 ? ((participantCount / totalPlayers) * 100).toFixed(1) : 0;
        
        const pointsPerParticipant = parseFloat(document.querySelector('[name="points_per_participant"]')?.value) || 0;
        const calculatedPoints = participantCount * pointsPerParticipant;

        document.getElementById('participant-count-stat').textContent = `Participants: ${participantCount}/${totalPlayers}`;
        document.getElementById('participation-rate-stat').textContent = `Rate: ${rate}%`;
        document.getElementById('calculated-points-stat').textContent = `Points: ${calculatedPoints.toFixed(1)}`;
    }

    // Add CSS styles
    const style = document.createElement('style');
    style.textContent = `
        .participation-controls .btn {
            font-size: 11px;
            padding: 4px 8px;
            border-radius: 3px;
            border: 1px solid;
            background: white;
            cursor: pointer;
            transition: all 0.2s;
        }
        .participation-controls .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .btn-outline-primary { border-color: #007bff; color: #007bff; }
        .btn-outline-primary:hover { background: #007bff; color: white; }
        .btn-outline-secondary { border-color: #6c757d; color: #6c757d; }
        .btn-outline-secondary:hover { background: #6c757d; color: white; }
        .btn-outline-info { border-color: #17a2b8; color: #17a2b8; }
        .btn-outline-info:hover { background: #17a2b8; color: white; }
    `;
    document.head.appendChild(style);

})();
