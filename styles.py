CSS = """
<style>
.stAppViewContainer{
    margin-left: auto;
    margin-right: auto;
}

.block-container {
    padding-top: 0rem!important;
}

/* Stepbar styles */
.step-current {
    background-color: #1f77b4;
    color: white;
    padding: 8px;
    border-radius: 20px;
    text-align: center;
    font-size: 12px;
    font-weight: bold;
    margin: 2px;
}

.step-completed {
    background-color: #28a745;
    color: white;
    padding: 8px;
    border-radius: 20px;
    text-align: center;
    font-size: 12px;
    margin: 2px;
}

.step-future {
    background-color: #e9ecef;
    color: #6c757d;
    padding: 8px;
    border-radius: 20px;
    text-align: center;
    font-size: 12px;
    margin: 2px;
    border: 1px solid #dee2e6;
}
.step-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding: 10px 0;
}

.step-bar {
    display: flex;
    flex-grow: 1;
    justify-content: space-evenly;
    margin: 0 20px;
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
    .step-current, .step-completed, .step-future {
        font-size: 10px;
        padding: 6px;
    }
}

</style>
"""

# Function to generate step HTML with classes
def get_step_html(step_number, step_name, step_type="future"):
    """
    Generate HTML for a step indicator
    
    Args:
        step_number (int): The step number (1-indexed)
        step_name (str): The name of the step
        step_type (str): Type of step - 'current', 'completed', or 'future'
    
    Returns:
        str: HTML string for the step
    """
    if step_type == "current":
        return f'<div class="step-current">{step_number}. {step_name}</div>'
    elif step_type == "completed":
        return f'<div class="step-completed">✓ {step_name}</div>'
    else:  # future
        return f'<div class="step-future">{step_number}. {step_name}</div>'

# Color constants for customization
COLORS = {
    'primary': '#1f77b4',      # Current step blue
    'success': '#28a745',      # Completed step green
    'secondary': '#e9ecef',    # Future step light gray
    'muted': '#6c757d',        # Future step text color
    'border': '#dee2e6'        # Future step border
}