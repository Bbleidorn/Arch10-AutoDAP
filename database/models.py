from datetime import datetime

from sqlalchemy import (
    Column, String, DateTime
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Project(Base):
    """Project model."""
    __tablename__ = 'projects'

    id = Column(UUID, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    project_json = Column(String, nullable=True)

    def __repr__(self):
        return f"<Project(id='{self.id}', name='{self.name}', description='{self.description}')>"
