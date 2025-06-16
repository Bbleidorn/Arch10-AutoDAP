# src/views/components/step_bar.py
import streamlit as st
from styles import get_step_html

def render_step_bar(controller, steps):
    if not steps:
        return

    st.markdown("---")
    current_step = controller.session_state.current_step
    
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("← Previous", 
                    disabled=(current_step == 0),
                    use_container_width=True):
            controller.go_to_previous_step()

    with col2:
        step_cols = st.columns(len(steps))
        for i, step_name in enumerate(steps):
            with step_cols[i]:
                if i == current_step:
                    status = "current"
                elif i < current_step:
                    status = "completed"
                else:
                    status = "future"
                st.markdown(get_step_html(i + 1, step_name, status), unsafe_allow_html=True)

    with col3:
        if st.button("Next →", 
                    disabled=(current_step >= len(steps) - 1),
                    use_container_width=True):
            controller.go_to_next_step()