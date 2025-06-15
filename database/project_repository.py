class ProjectRepository:
    def __init__(self, db):
        self.db = db

    def get_project(self, project_id):
        return self.db.get_project(project_id)

    def create_project(self, project_data):
        return self.db.create_project(project_data)

    def update_project(self, project_id, project_data):
        return self.db.update_project(project_id, project_data)

    def delete_project(self, project_id):
        return self.db.delete_project(project_id)

    def list_projects(self):
        return self.db.list_projects()