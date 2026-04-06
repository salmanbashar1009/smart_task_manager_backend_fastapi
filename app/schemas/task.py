from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from typing import Optional

class TaskCreate(BaseModel):
    title:str
    description: Optional[str] = None
    project_id: uuid.UUID | None = None
    assignee_email: Optional[EmailStr] = None
    priority: str = "medium" # low, medium, high
    deadline: datetime | None = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str]= None
    status: Optional[str] = None #todo, in-progress, done
    priority: Optional[str]=None
    assignee_email: Optional[EmailStr]=None
    deadline: Optional[datetime]=None  


class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    priority: str
    deadline:Optional[datetime]

    class config:
        from_attributes = True