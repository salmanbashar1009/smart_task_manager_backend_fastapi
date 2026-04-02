from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Any, List
from datetime import datetime
import uuid
from __future__ import annotations
from .user import User
from .project import Project
from .comment import Comment

class Task(SQLModel, table= True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default= "todo") #todo,in-progress,done
    priority: str = Field(default="medium") #low,medium,high
    deadline: Optional[datetime] = None

    # Relationship

    project_id: uuid.UUID = Field(foreign_key="project.id")
    assignee_id: Optional[uuid.UUID] = Field(foreign_key='user.id')

    assignee: Optional["User"] = Relationship(back_populates='tasks')
    project: "Project" = Relationship(back_populates='tasks')
    comments: List['Comment'] = Relationship(back_populates= 'task')
