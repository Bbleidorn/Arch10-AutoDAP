# src/controllers/navigation_controller.py
import streamlit as st
from config.steps_config import PROJECT_STEPS

class NavigationController:
    def __init__(self, session_state):
        self.session_state = session_state
        self.project_steps = PROJECT_STEPS

    def get_current_steps(self):
        return self.project_steps.get(self.session_state.current_page, [])

    def get_current_step_name(self):
        steps = self.get_current_steps()
        current_step_index = self.session_state.current_step
        if current_step_index < len(steps):
            return steps[current_step_index]
        return "Unknown Step"

    def navigate_to_new_project(self):
        self.session_state.current_page = 'new_project'
        self.session_state.selected_project = None
        self.session_state.reset_step()
        st.rerun()

    def navigate_to_existing_project(self, project_name):
        self.session_state.current_page = 'existing_project'
        self.session_state.selected_project = project_name
        self.session_state.reset_step()
        st.rerun()
        
    def go_to_next_step(self):
        max_steps = len(self.get_current_steps())
        self.session_state.next_step(max_steps)
        st.rerun()
        
    def go_to_previous_step(self):
        self.session_state.previous_step()
        st.rerun()