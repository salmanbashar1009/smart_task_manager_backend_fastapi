from pydantic import BaseModel
from datetime import datetime
import uuid

class TaskCreate(BaseModel):
    title:str
    description: str | None = None
    project_id: uuid.UUID | None = None
    assignee_id: uuid.UUID | None = None
    priority: str = "medium"
    deadline: datetime | None = None

class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    priority: str

    class config:
        from_attributes = True