/**
 * Enhanced team-based player filtering for EventScore admin
 * Filters players in Team Event Participation inlines based on selected team
 */

(function($) {
    'use strict';
    
    function initializeTeamFiltering() {
        console.log('Initializing team-based player filtering...');
        
        // Find the team select field
        var $teamSelect = $('#id_team');
        if ($teamSelect.length === 0) {
            console.log('Team select field not found');
            return;
        }
        
        console.log('Team select found, setting up change handler');
        
        // Set up event listener for team changes
        $teamSelect.off('change.teamfilter').on('change.teamfilter', function() {
            var selectedTeam = $(this).val();
            console.log('Team changed to:', selectedTeam);
            filterPlayersByTeam(selectedTeam);
        });
        
        // Apply initial filtering if team is already selected
        var initialTeam = $teamSelect.val();
        if (initialTeam) {
            console.log('Initial team:', initialTeam);
            filterPlayersByTeam(initialTeam);
        }
        
        // Handle dynamically added inlines
        $(document).on('formset:added', function(event, $row, formsetName) {
            if (formsetName === 'teameventparticipation_set') {
                console.log('New inline added, applying filtering');
                var currentTeam = $teamSelect.val();
                if (currentTeam) {
                    setTimeout(function() {
                        filterPlayersByTeam(currentTeam);
                    }, 100);
                }
            }
        });
    }
    
    function filterPlayersByTeam(selectedTeam) {
        console.log('Filtering players for team:', selectedTeam);
        
        if (!selectedTeam) {
            console.log('No team selected, restoring all players');
            restoreAllPlayers();
            return;
        }
        
        // Find all player select elements in team event participation inlines
        var playerSelects = $('.inline-group select[name$="-player"], .inline-group select[id$="-player"]');
        console.log('Found player selects:', playerSelects.length);
        
        if (playerSelects.length === 0) {
            console.log('No player select fields found');
            return;
        }
        
        // Make AJAX request to get filtered players
        $.ajax({
            url: '/admin/get-team-players/',
            method: 'POST',
            data: {
                'team': selectedTeam,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Received players for team ' + selectedTeam + ':', data.players);
                updatePlayerSelects(playerSelects, data.players || []);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching team players:', error);
                console.error('Response:', xhr.responseText);
            }
        });
    }
    
    function updatePlayerSelects(playerSelects, players) {
        playerSelects.each(function() {
            var $select = $(this);
            var currentValue = $select.val();
            
            // Store original options if not already stored
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
    
    function restoreAllPlayers() {
        var playerSelects = $('.inline-group select[name$="-player"], .inline-group select[id$="-player"]');
        
        playerSelects.each(function() {
            var $select = $(this);
            var originalOptions = $select.data('original-options');
            
            if (originalOptions) {
                $select.html(originalOptions);
            }
        });
    }
    
    // Wait for Django admin to be ready
    $(document).ready(function() {
        console.log('Document ready, initializing team filtering');
        initializeTeamFiltering();
        
        // Also initialize when new inlines are added
        $(document).on('formset:added', function() {
            setTimeout(function() {
                initializeTeamFiltering();
            }, 100);
        });
    });
    
    // Also try to initialize after Django admin loads
    $(window).on('load', function() {
        console.log('Window loaded, ensuring team filtering is set up');
        setTimeout(initializeTeamFiltering, 500);
    });
    
    // Global function for debugging
    window.debugTeamFiltering = function() {
        console.log('=== Team Filtering Debug ===');
        console.log('Team select:', $('#id_team').length);
        console.log('Player selects:', $('.inline-group select[name$="-player"]').length);
        console.log('Current team:', $('#id_team').val());
    };
    
})(window.django && window.django.jQuery || window.jQuery);
