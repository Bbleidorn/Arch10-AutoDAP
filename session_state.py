# src/models/session_state.py
import streamlit as st

class SessionState:
    def __init__(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "new_project"
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'selected_project' not in st.session_state:
            st.session_state.selected_project = None

    @property
    def current_page(self):
        return st.session_state.current_page

    @current_page.setter
    def current_page(self, value):
        st.session_state.current_page = value

    @property
    def current_step(self):
        return st.session_state.current_step

    @current_step.setter
    def current_step(self, value):
        st.session_state.current_step = value
        
    @property
    def selected_project(self):
        return st.session_state.selected_project

    @selected_project.setter
    def selected_project(self, value):
        st.session_state.selected_project = value

    def reset_step(self):
        self.current_step = 0
        
    def next_step(self, max_steps):
        if self.current_step < max_steps - 1:
            self.current_step += 1

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1