// Admin functionality for Onam Treasure Hunt

function approveAnswer(answerId, action) {
    if (action === 'reject' && !confirm('Are you sure you want to reject this answer?')) {
        return;
    }
    
    const points = document.getElementById(`points_${answerId}`)?.value || 0;
    
    fetch(`/custom-admin/approve-answer/${answerId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `action=${action}&points=${points}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the answer.');
    });
}

// Auto-refresh pending answers every 30 seconds on approve answers page
if (window.location.pathname.includes('approve-answers')) {
    setInterval(() => {
        const pendingCount = document.querySelectorAll('.approve-btn').length;
        if (pendingCount > 0) {
            // Optionally auto-refresh if there are pending answers
            // location.reload();
        }
    }, 30000);
}

// Form validation for question upload
function validateQuestionForm() {
    const questionType = document.getElementById('question_type').value;
    const questionText = document.getElementById('question_text').value.trim();
    
    if (!questionType || !questionText) {
        alert('Please fill in the question type and question text.');
        return false;
    }
    
    if (questionType === 'multiple_choice') {
        const options = ['option_a', 'option_b', 'option_c', 'option_d'];
        const hasEmptyOption = options.some(id => !document.getElementById(id).value.trim());
        
        if (hasEmptyOption) {
            alert('Please fill in all multiple choice options.');
            return false;
        }
        
        const correctAnswer = document.getElementById('correct_answer').value.trim().toUpperCase();
        if (!['A', 'B', 'C', 'D'].includes(correctAnswer)) {
            alert('For multiple choice questions, correct answer must be A, B, C, or D.');
            return false;
        }
    }
    
    return true;
}

// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation to question form
    const questionForm = document.querySelector('form[method="post"]');
    if (questionForm && window.location.pathname.includes('bulk-upload-questions')) {
        questionForm.addEventListener('submit', function(e) {
            if (!validateQuestionForm()) {
                e.preventDefault();
            }
        });
    }
    
    // Add confirmation to delete actions
    document.querySelectorAll('a[href*="delete"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Show/hide image upload section based on question type
    const questionTypeField = document.getElementById('id_question_type');
    const imageSection = document.querySelector('.field-question_image').closest('fieldset');
    
    if (questionTypeField && imageSection) {
        function toggleImageSection() {
            const selectedType = questionTypeField.value;
            if (selectedType === 'image_text') {
                imageSection.style.display = 'block';
                imageSection.style.backgroundColor = '#f0f8ff';
                imageSection.style.border = '2px solid #007cba';
                imageSection.style.borderRadius = '5px';
                imageSection.style.padding = '15px';
                
                // Add helpful text
                const helpText = imageSection.querySelector('.image-help-text');
                if (!helpText) {
                    const help = document.createElement('div');
                    help.className = 'image-help-text';
                    help.style.cssText = 'background: #e7f3ff; padding: 10px; margin: 10px 0; border-radius: 3px; font-style: italic;';
                    help.innerHTML = '<strong>💡 Tip:</strong> Upload an image that players will analyze to answer your question. The image will be displayed prominently above the question text.';
                    imageSection.querySelector('.description').appendChild(help);
                }
            } else {
                imageSection.style.display = 'block';
                imageSection.style.backgroundColor = '';
                imageSection.style.border = '';
                imageSection.style.borderRadius = '';
                imageSection.style.padding = '';
                
                // Remove help text for non-image questions
                const helpText = imageSection.querySelector('.image-help-text');
                if (helpText) {
                    helpText.remove();
                }
            }
        }
        
        // Initial call
        toggleImageSection();
        
        // Listen for changes
        questionTypeField.addEventListener('change', toggleImageSection);
    }
});
