# src/views/components/sidebar.py
import streamlit as st

def render_sidebar(controller, projects):
    with st.sidebar:
        st.markdown("# 🚀 Project Navigator")
        st.divider()

        if st.button("➕ New Project", 
            type="primary" if controller.session_state.current_page == 'new_project' else "secondary",
            use_container_width=True):
            controller.navigate_to_new_project()

        if projects:
            st.markdown("### 📁 Existing Projects")
            for project in projects:
                is_selected = (controller.session_state.current_page == 'existing_project' and 
                               controller.session_state.selected_project == project)
                
                button_type = "primary" if is_selected else "secondary"
                
                if st.button(f"📊 {project}", 
                           type=button_type,
                           use_container_width=True,
                           key=f"btn_{project}"):
                    controller.navigate_to_existing_project(project)
        st.divider()