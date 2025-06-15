from database.database import DatabaseManager
from database.project_repository import ProjectRepository
from database.models import Project

class ProjectService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.project_repo = ProjectRepository(db_manager)

    def create_project():
        # TODO Implementation
        return None
    
    def get_project_by_name():
        # TODO implementation
        return None
    
    def get_all_projects():
        # TODO implementation
        return ['Test name 1', 'Test name 2']
    