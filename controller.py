import streamlit as st
import numpy as np

class Controller:

    def __init__(self, projects):
        self.initialize_session_state()
        new_project_page = {'New project': self.render_new_project}
        projects_pages = { name: self.render_existing_project(name) for name in projects}

        self.pages = new_project_page | projects_pages

        self.render_sidebar()
        self.render()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "New project"

    def render_sidebar(self):
        st.sidebar.title("AutoDAP")
         # Navigation
        st.sidebar.subheader("Projects")
        selected_page = st.sidebar.radio(
            "Go to:",
            list(self.pages.keys()),
            key="page_selector"
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page

        st.sidebar.divider()
        self.render()


    def render_new_project(self):
        st.markdown("New Project")

    def render_existing_project(self, projectname: str):
        st.markdown(f"{projectname}")

    def render(self):
        st.markdown("# AutoDAP")
        # Render current page
        current_page = st.session_state.current_page
        if current_page in self.pages:
            self.pages[current_page]()