from .task import Task
from .user import User

from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from typing import Optional, Any, List
from datetime import datetime
import uuid
from __future__ import annotations

class Comment(SQLModel,table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    #Relationship
    task_id: uuid.UUID = Field(foreign_key="task.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")

    task: Task = Relationship(back_populates='comments')
    user: User = Relationship(back_populates='comments')
