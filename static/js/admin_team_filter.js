/**
 * Dynamic team-based player filtering for EventScore admin
 * Filters players in TeamEventParticipation inline based on selected team
 */

(function($) {
    'use strict';
    
    // Store original player options for each inline
    var originalPlayerOptions = {};
    
    function initializePlayerFilter() {
        // Store original options for all player selects
        $('.inline-group select[name$="-player"]').each(function(index) {
            var $select = $(this);
            var inlineId = 'inline_' + index;
            originalPlayerOptions[inlineId] = $select.html();
        });
        
        // Filter players when team changes
        $('#id_team').on('change', function() {
            filterPlayersByTeam($(this).val());
        });
        
        // Initial filter on page load
        var initialTeam = $('#id_team').val();
        if (initialTeam) {
            filterPlayersByTeam(initialTeam);
        }
    }
    
    function filterPlayersByTeam(selectedTeam) {
        if (!selectedTeam) {
            // If no team selected, show all players
            restoreAllPlayerOptions();
            return;
        }
        
        // Make AJAX request to get players for the selected team
        $.ajax({
            url: '/admin/get-team-players/',
            data: {
                'team': selectedTeam,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                updatePlayerSelects(data.players);
            },
            error: function() {
                console.error('Failed to fetch team players');
                restoreAllPlayerOptions();
            }
        });
    }
    
    function updatePlayerSelects(players) {
        $('.inline-group select[name$="-player"]').each(function() {
            var $select = $(this);
            var currentValue = $select.val();
            
            // Clear current options except empty option
            $select.find('option').remove();
            $select.append('<option value="">---------</option>');
            
            // Add filtered players
            $.each(players, function(index, player) {
                var $option = $('<option></option>')
                    .attr('value', player.id)
                    .text(player.name);
                
                // Keep selection if player is in the filtered list
                if (player.id == currentValue) {
                    $option.attr('selected', 'selected');
                }
                
                $select.append($option);
            });
            
            // If current selection is not in filtered list, clear it
            if (currentValue && !players.some(p => p.id == currentValue)) {
                $select.val('');
            }
        });
    }
    
    function restoreAllPlayerOptions() {
        $('.inline-group select[name$="-player"]').each(function(index) {
            var $select = $(this);
            var inlineId = 'inline_' + index;
            var currentValue = $select.val();
            
            if (originalPlayerOptions[inlineId]) {
                $select.html(originalPlayerOptions[inlineId]);
                $select.val(currentValue);
            }
        });
    }
    
    // Handle dynamically added inlines
    function handleNewInlines() {
        $('.add-row a').on('click', function() {
            setTimeout(function() {
                // Re-initialize for new inlines
                var selectedTeam = $('#id_team').val();
                if (selectedTeam) {
                    filterPlayersByTeam(selectedTeam);
                }
            }, 100);
        });
    }
    
    // Initialize when DOM is ready
    $(document).ready(function() {
        initializePlayerFilter();
        handleNewInlines();
        
        // Handle Django admin inline events
        $(document).on('formset:added', function(event, $row, formsetName) {
            if (formsetName === 'teameventparticipation_set') {
                var selectedTeam = $('#id_team').val();
                if (selectedTeam) {
                    setTimeout(function() {
                        filterPlayersByTeam(selectedTeam);
                    }, 100);
                }
            }
        });
    });
    
})(django.jQuery || jQuery);
