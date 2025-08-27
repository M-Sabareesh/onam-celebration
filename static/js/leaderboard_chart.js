/* Leaderboard Chart Enhancements */

function initTeamProgressChart(chartData) {
    const ctx = document.getElementById('teamProgressChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: chartData.datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Team Score Progress Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' points';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Cumulative Score',
                        font: {
                            weight: 'bold'
                        }
                    },
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            elements: {
                line: {
                    tension: 0.3
                },
                point: {
                    radius: 4,
                    hoverRadius: 6
                }
            }
        }
    });
}

// Enhanced winner display animations
function animateWinnerBadges() {
    const winnerBadges = document.querySelectorAll('.winner-badge');
    winnerBadges.forEach((badge, index) => {
        setTimeout(() => {
            badge.style.opacity = '0';
            badge.style.transform = 'scale(0.8)';
            badge.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                badge.style.opacity = '1';
                badge.style.transform = 'scale(1)';
            }, 100);
        }, index * 200);
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Animate winner badges
    animateWinnerBadges();
    
    // Chart will be initialized by inline script with data
});
