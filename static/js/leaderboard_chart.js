/* Leaderboard Chart Enhancements */

function initTeamProgressChart(chartData) {
    console.log('🎨 Chart Data Received:', chartData);
    console.log('📊 Datasets:', chartData.datasets);
    
    // Check if each dataset has colors
    if (chartData.datasets && Array.isArray(chartData.datasets)) {
        chartData.datasets.forEach((dataset, index) => {
            console.log(`🎯 Team ${index + 1} (${dataset.label}):`, {
                borderColor: dataset.borderColor,
                backgroundColor: dataset.backgroundColor
            });
        });
    }
    
    const ctx = document.getElementById('teamProgressChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: chartData.datasets
        },
    
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
                    labels: {
                        padding: 20,
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 15,
                        boxHeight: 15
                    }
                },
                title: {
                    display: true,
                    text: 'Team Performance Progress by Event',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    },
                    color: '#2D3748'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.9)',
                    titleColor: '#FFFFFF',
                    bodyColor: '#FFFFFF',
                    borderColor: '#FFFFFF',
                    borderWidth: 2,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + ' points';
                        },
                        title: function(context) {
                            return 'After Event: ' + context[0].label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Events Timeline',
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        color: '#2D3748'
                    },
                    grid: {
                        color: 'rgba(0,0,0,0.1)',
                        borderColor: '#4A5568',
                        borderWidth: 2
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 0,
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        color: '#4A5568'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total Points (Cumulative)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        color: '#2D3748'
                    },
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)',
                        borderColor: '#4A5568',
                        borderWidth: 2
                    },
                    ticks: {
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        color: '#4A5568',
                        callback: function(value) {
                            return value + ' pts';
                        }
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
                    tension: 0.3,
                    borderWidth: 4
                },
                point: {
                    radius: 7,
                    hoverRadius: 10,
                    borderWidth: 3,
                    hoverBorderWidth: 4
                }
            },
            animation: {
                duration: 2500,
                easing: 'easeInOutQuart'
            },
            onHover: (event, activeElements) => {
                event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
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
