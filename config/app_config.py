import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    
    title = 'AutoDAP'
    icon = 'imgs/a10.png'
    layout = 'wide'
    sidebar_state = 'collapsed'

    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            database_url = "DUMMY"#os.getenv("DATABASE_URL")
            # Add env_var = os.getenv() for every required env_var 
        )
    
    def __init__(self, database_url: str):
        self.database_url = database_url