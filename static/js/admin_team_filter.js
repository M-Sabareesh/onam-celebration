/**
 * Enhanced team-based player filtering for admin interfaces
 * Supports both EventScore and SimpleEventScore admin forms
 * Filters players in dropdowns based on selected team
 */

(function($) {
    'use strict';
    
    // Initialize when document is ready
    $(document).ready(function() {
        console.log('Initializing admin team filtering...');
        initializeAllFiltering();
        
        // Handle Django admin inline additions
        $(document).on('formset:added', function() {
            setTimeout(function() {
                initializeAllFiltering();
            }, 100);
        });
        
        // Handle auto-calculation changes
        setupAutoCalculationToggle();
    });
    
    function initializeAllFiltering() {
        // Initialize team-based participant filtering for SimpleEventScore
        initializeSimpleEventFiltering();
        
        // Initialize team-based participant filtering for EventScore inlines
        initializeEventScoreFiltering();
    }
    
    function initializeSimpleEventFiltering() {
        var $teamSelect = $('#id_team');
        var $participantsSelect = $('#id_participants_to, #id_participants_from');
        
        if ($teamSelect.length === 0 || $participantsSelect.length === 0) {
            return;
        }
        
        console.log('Setting up SimpleEventScore team filtering');
        
        $teamSelect.off('change.simpleevent').on('change.simpleevent', function() {
            var selectedTeam = $(this).val();
            console.log('SimpleEventScore team changed to:', selectedTeam);
            
            if (selectedTeam) {
                filterParticipantsByTeam(selectedTeam, $participantsSelect);
            } else {
                restoreAllParticipants($participantsSelect);
            }
        });
        
        // Apply initial filtering
        var initialTeam = $teamSelect.val();
        if (initialTeam) {
            filterParticipantsByTeam(initialTeam, $participantsSelect);
        }
    }
    
    function initializeEventScoreFiltering() {
        var $teamSelect = $('#id_team');
        
        if ($teamSelect.length === 0) {
            return;
        }
        
        console.log('Setting up EventScore inline team filtering');
        
        $teamSelect.off('change.eventscore').on('change.eventscore', function() {
            var selectedTeam = $(this).val();
            console.log('EventScore team changed to:', selectedTeam);
            filterInlinePlayersByTeam(selectedTeam);
        });
        
        // Apply initial filtering
        var initialTeam = $teamSelect.val();
        if (initialTeam) {
            filterInlinePlayersByTeam(initialTeam);
        }
    }
    
    function filterParticipantsByTeam(selectedTeam, $participantsSelects) {
        if (!selectedTeam) {
            restoreAllParticipants($participantsSelects);
            return;
        }
        
        $.ajax({
            url: '/admin/get-team-players/',
            method: 'POST',
            data: {
                'team': selectedTeam,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Received players for team ' + selectedTeam + ':', data.players);
                updateParticipantSelects($participantsSelects, data.players || []);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching team players:', error);
            }
        });
    }
    
    function filterInlinePlayersByTeam(selectedTeam) {
        var playerSelects = $('.inline-group select[name$="-player"], .inline-group select[id$="-player"]');
        
        if (playerSelects.length === 0) {
            return;
        }
        
        if (!selectedTeam) {
            restoreInlinePlayerSelects(playerSelects);
            return;
        }
        
        $.ajax({
            url: '/admin/get-team-players/',
            method: 'POST',
            data: {
                'team': selectedTeam,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Received players for inline team ' + selectedTeam + ':', data.players);
                updateInlinePlayerSelects(playerSelects, data.players || []);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching team players for inlines:', error);
            }
        });
    }
    
    function updateParticipantSelects($selects, players) {
        $selects.each(function() {
            var $select = $(this);
            var selectedValues = $select.val() || [];
            
            // Store original options if not stored
            if (!$select.data('original-options')) {
                var originalOptions = [];
                $select.find('option').each(function() {
                    originalOptions.push({
                        value: $(this).val(),
                        text: $(this).text(),
                        selected: $(this).prop('selected')
                    });
                });
                $select.data('original-options', originalOptions);
            }
            
            // Clear and rebuild options
            $select.empty();
            
            // Add filtered players
            $.each(players, function(index, player) {
                var option = $('<option></option>')
                    .attr('value', player.id)
                    .text(player.name);
                
                // Restore selection if this was previously selected
                if (selectedValues.includes(player.id.toString())) {
                    option.prop('selected', true);
                }
                
                $select.append(option);
            });
            
            // Show message if no players found
            if (players.length === 0) {
                $select.append('<option value="" disabled>No players in this team</option>');
            }
        });
    }
    
    function updateInlinePlayerSelects(playerSelects, players) {
        playerSelects.each(function() {
            var $select = $(this);
            var currentValue = $select.val();
            
            // Store original options if not stored
            if (!$select.data('original-options')) {
                $select.data('original-options', $select.html());
            }
            
            // Clear and rebuild select options
            $select.empty();
            $select.append('<option value="">---------</option>');
            
            // Add filtered players
            $.each(players, function(index, player) {
                var option = $('<option></option>')
                    .attr('value', player.id)
                    .text(player.name);
                
                // Restore selection if this was previously selected
                if (player.id == currentValue) {
                    option.prop('selected', true);
                }
                
                $select.append(option);
            });
            
            // Show helpful message if no players found
            if (players.length === 0) {
                $select.append('<option value="" disabled>No players in this team</option>');
            }
        });
    }
    
    function restoreAllParticipants($selects) {
        $selects.each(function() {
            var $select = $(this);
            var originalOptions = $select.data('original-options');
            
            if (originalOptions) {
                $select.empty();
                $.each(originalOptions, function(index, option) {
                    var $option = $('<option></option>')
                        .attr('value', option.value)
                        .text(option.text);
                    
                    if (option.selected) {
                        $option.prop('selected', true);
                    }
                    
                    $select.append($option);
                });
            }
        });
    }
    
    function restoreInlinePlayerSelects(playerSelects) {
        playerSelects.each(function() {
            var $select = $(this);
            var originalOptions = $select.data('original-options');
            
            if (originalOptions) {
                $select.html(originalOptions);
            }
        });
    }
    
    function setupAutoCalculationToggle() {
        var $autoCalcCheckbox = $('#id_auto_calculate_points');
        var $pointsField = $('#id_points');
        var $pointsPerParticipantField = $('#id_points_per_participant');
        
        if ($autoCalcCheckbox.length === 0) {
            return;
        }
        
        function togglePointsField() {
            var isAutoCalc = $autoCalcCheckbox.prop('checked');
            
            if (isAutoCalc) {
                $pointsField.prop('readonly', true)
                    .closest('.form-row').addClass('auto-calculated')
                    .find('label').append(' <span style="color: orange;">(Auto-calculated)</span>');
                $pointsPerParticipantField.focus();
            } else {
                $pointsField.prop('readonly', false)
                    .closest('.form-row').removeClass('auto-calculated')
                    .find('label span').remove();
            }
        }
        
        $autoCalcCheckbox.on('change', togglePointsField);
        togglePointsField(); // Apply initial state
    }
    
    // Debug function
    window.debugAdminFiltering = function() {
        console.log('=== Admin Filtering Debug ===');
        console.log('Team select:', $('#id_team').length);
        console.log('Participants selects:', $('#id_participants_to, #id_participants_from').length);
        console.log('Inline player selects:', $('.inline-group select[name$="-player"]').length);
        console.log('Current team:', $('#id_team').val());
        console.log('Auto calculate checkbox:', $('#id_auto_calculate_points').length);
    };
    
})(window.django && window.django.jQuery || window.jQuery);
