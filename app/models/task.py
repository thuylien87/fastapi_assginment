from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from schemas.task import TaskMode

class SearchTaskModel():
    def __init__(self, user_id) -> None:
        self.user_id = user_id     

class TaskModel(BaseModel):    
    summary: str = Field(min_length=2)
    description: str = Field(min_length=2)
    status: TaskMode = Field(default=TaskMode.ACTIVE)
    priority: int = Field(default=0)
    user_id: UUID


class TaskViewModel(BaseModel):
    id: UUID 
    summary: str
    description: str    
    priority: int
    created_at: datetime | None = None
    user_id: UUID | None = None
    
    class Config:
        from_attributes = True
