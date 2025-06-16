# src/views/pages/new_project.py
import streamlit as st
import numpy as np

def render_new_project(step_name, current_step):
    st.markdown("# New Project")
    st.markdown(f"## Step {current_step + 1}: {step_name}")
    
    # Step-specific content
    if current_step == 0:  # Select files
        st.markdown("### Select your data files")
        st.file_uploader("Choose data files", type=['csv', 'xlsx', 'json', 'txt'], accept_multiple_files=True)
        st.text_input("Project Name", key="project_name")
        st.text_area("Project Description", key="project_description")
        
    elif current_step == 1:  # Detection validation
        st.markdown("### Validate data detection and format")
        # Placeholder for data validation logic
        st.dataframe(np.random.randn(5, 4), use_container_width=True)
        
    # ... add rendering for other steps (2 through 6) here ...