import streamlit as st


class Controller:

    def __init__(self, projects):
        
        new_projects_page = {'Create new project': self.render_new_project}
        projects_pages = { '{name}': self.render_existing_project(name) for name in projects}

        self.pages = new_projects_page + projects_pages
        
        st.set_page_config(
            page_title="AutoDAP",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        self.render_sidebar()
        self.render()


    def render_sidebar(self):
        st.sidebar.title("AutoDAP")
         # Navigation
        st.sidebar.subheader("Navigation")
        selected_page = st.sidebar.radio(
            "Go to:",
            list(self.pages.keys()),
            key="page_selector"
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page

        st.sidebar.divider()
        st.render


    def render_new_project():
        st.markdown("New Project")

    def render_existing_project(projectname: str):
        st.markdown(projectname)

    def render(self):
        st.markdown("# AutoDAP")
        # Render current page
        current_page = st.session_state.current_page
        if current_page in self.pages:
            self.pages[current_page]()