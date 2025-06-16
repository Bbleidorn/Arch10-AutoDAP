# src/controllers/project_controller.py
import streamlit as st
from config.app_config import APP_TITLE
from models.session_state import SessionState
from controllers.navigation_controller import NavigationController
from views.components import sidebar, step_bar
from views.pages import new_project, existing_project

class ProjectController:
    def __init__(self, projects):
        self.projects = projects # This would come from a project model/service
        self.session_state = SessionState()
        self.navigation_controller = NavigationController(self.session_state)

    def render(self):
        st.title(APP_TITLE)
        
        # Render sidebar and handle its logic via the controller
        sidebar.render_sidebar(self.navigation_controller, self.projects)
        
        main_container = st.container()
        with main_container:
            self._render_current_page()
            
        # Render the step bar at the bottom
        steps = self.navigation_controller.get_current_steps()
        step_bar.render_step_bar(self.navigation_controller, steps)

    def _render_current_page(self):
        page = self.session_state.current_page
        step_name = self.navigation_controller.get_current_step_name()
        step_index = self.session_state.current_step

        if page == "new_project":
            new_project.render_new_project(step_name, step_index)
        elif page == "existing_project":
            project_name = self.session_state.selected_project
            existing_project.render_existing_project(project_name, step_name, step_index)