import streamlit as st
import logging

from config import AppConfig
from styles import CSS
from database.database import DatabaseManager
from services.project_service import ProjectService
from controller import Controller

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def st_setup(config: AppConfig) -> None:
    st.set_page_config(
        page_title=config.title,
        page_icon=config.icon,
        layout=config.layout,
        initial_sidebar_state=config.sidebar_state
        )

def main():
    config = AppConfig.from_env()
    st_setup(config)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)

    db_manager = DatabaseManager(config.database_url)
    project_service = ProjectService(db_manager)
    all_projects = project_service.get_all_projects()

    controller = Controller(all_projects)
    controller.render()








if __name__ == '__main__':
    main()
